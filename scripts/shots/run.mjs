#!/usr/bin/env node
/**
 * pnpm shots <slug> [--force]
 *
 * Sends scripts/shots/<slug>.yml to the shots LXC, takes the screenshots with
 * shot-scraper (retina), converts them to WebP 1600px wide, and drops them in
 * src/data/blog/ as <slug>-<n>.webp. Prints the Markdown to paste, alt text
 * included, so images never land in an article without one.
 */
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const HOST = "root@192.168.50.9";
const REMOTE = "/opt/shots";
const ROOT = resolve(import.meta.dirname, "../..");

const [slug, ...flags] = process.argv.slice(2);
const force = flags.includes("--force");
if (!slug) {
  console.error("usage: pnpm shots <slug> [--force]");
  process.exit(1);
}

const recipe = resolve(ROOT, `scripts/shots/${slug}.yml`);
if (!existsSync(recipe)) {
  console.error(`recette introuvable : scripts/shots/${slug}.yml`);
  process.exit(1);
}

const ssh = (cmd) =>
  execFileSync("ssh", [HOST, cmd], { encoding: "utf8", stdio: ["ignore", "pipe", "inherit"] });

// alt: is ours, shot-scraper would choke on it — strip it before sending.
const source = readFileSync(recipe, "utf8");
const alts = [...source.matchAll(/^\s*(?:-\s*)?output:\s*(\S+)|^\s*alt:\s*["']?(.+?)["']?\s*$/gm)]
  .reduce(
    (acc, m) => {
      if (m[1]) acc.last = m[1];
      else if (acc.last) acc.map[acc.last] = m[2];
      return acc;
    },
    { map: {}, last: null }
  ).map;
// auth: is ours too — shot-scraper takes it as a CLI flag, not a YAML key.
const authName = source.match(/^\s*auth:\s*(\S+)\s*$/m)?.[1];
const cleaned = source.replace(/^\s*(alt|auth):.*$/gm, "");

const shots = Object.keys(alts).length
  ? Object.keys(alts)
  : [...source.matchAll(/^\s*-?\s*output:\s*(\S+)/gm)].map((m) => m[1]);

console.log(`→ ${shots.length} capture(s) pour ${slug}`);

execFileSync("ssh", [HOST, `mkdir -p ${REMOTE}/jobs/${slug} && cat > ${REMOTE}/jobs/${slug}/shots.yml`], {
  input: cleaned,
  stdio: ["pipe", "inherit", "inherit"],
});

const authFlag = authName ? `--auth ${REMOTE}/auth/${authName}.json` : "";
if (authName) {
  // A stale session silently yields screenshots of the login page.
  ssh(`test -s ${REMOTE}/auth/${authName}.json || { echo "session ${authName} absente"; exit 1; }`);
}
ssh(
  `cd ${REMOTE}/jobs/${slug} && /opt/shots-venv/bin/shot-scraper multi shots.yml --retina ${authFlag} --fail 2>&1 | grep -E "^Screenshot|^Error" || true`
);

// 2x capture -> 1600px WebP, quality 82: sharp enough for a blog, light enough to load.
const outputs = [];
shots.forEach((png, i) => {
  const webp = `${slug}-${i + 1}.webp`;
  ssh(`cd ${REMOTE}/jobs/${slug} && cwebp -quiet -resize 1600 0 -q 82 "${png}" -o "${webp}"`);
  const target = resolve(ROOT, "src/data/blog", webp);
  if (existsSync(target) && !force) {
    console.log(`  = ${webp} existe déjà (--force pour écraser)`);
    return;
  }
  const b64 = execFileSync("ssh", [HOST, `base64 -w0 ${REMOTE}/jobs/${slug}/${webp}`], {
    encoding: "utf8",
    maxBuffer: 64 * 1024 * 1024,
  });
  writeFileSync(target, Buffer.from(b64, "base64"));
  outputs.push({ webp, alt: alts[png] || "" });
  console.log(`  + src/data/blog/${webp}`);
});

if (outputs.length) {
  console.log("\nMarkdown à coller :\n");
  for (const { webp, alt } of outputs) {
    if (!alt) console.log(`<!-- alt manquant : ajoute "alt:" dans ${slug}.yml -->`);
    console.log(`![${alt}](./${webp})\n`);
  }
  console.log("Relis les images avant de committer (IP, e-mails, jetons).");
}
