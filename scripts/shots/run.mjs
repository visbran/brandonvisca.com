#!/usr/bin/env node
/**
 * pnpm shots <slug> [--force] [--keep]
 *
 * Takes the screenshots for an article on the shots LXC and drops them in
 * src/data/blog/ as WebP, printing the Markdown with alt text.
 *
 * Recipe files, all in scripts/shots/ and all optional but the first:
 *   <slug>.yml          shot-scraper shots (plus our own alt: and auth: keys)
 *   <slug>.compose.yml  throwaway instance started before the shots, destroyed after
 *   <slug>.setup.sh     runs on the LXC once the instance is up: wait, seed demo data
 *
 * Prefer a throwaway instance over the production service: the reader sees
 * what they will get after following the tutorial, and no personal data can
 * leak into an image.
 */
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const HOST = "shots";
const REMOTE = "/opt/shots";
const ROOT = resolve(import.meta.dirname, "../..");

const args = process.argv.slice(2);
const slug = args.find((a) => !a.startsWith("--"));
const force = args.includes("--force");
const keep = args.includes("--keep"); // leave the instance running, to debug a recipe
if (!slug) {
  console.error("usage: pnpm shots <slug> [--force] [--keep]");
  process.exit(1);
}

const recipe = resolve(ROOT, `scripts/shots/${slug}.yml`);
const composeFile = resolve(ROOT, `scripts/shots/${slug}.compose.yml`);
const setupFile = resolve(ROOT, `scripts/shots/${slug}.setup.sh`);
if (!existsSync(recipe)) {
  console.error(`recette introuvable : scripts/shots/${slug}.yml`);
  process.exit(1);
}

const job = `${REMOTE}/jobs/${slug}`;
// Short and neutral: the project name is visible in some UIs (Dozzle, Portainer).
// One run at a time as a result — two recipes in parallel would collide.
const project = "demo";

const ssh = (cmd, opts = {}) =>
  execFileSync("ssh", [HOST, cmd], { encoding: "utf8", stdio: ["ignore", "inherit", "inherit"], ...opts });
const push = (cmd, input) =>
  execFileSync("ssh", [HOST, cmd], { input, stdio: ["pipe", "inherit", "inherit"] });

// alt: and auth: are ours; shot-scraper would reject them.
const source = readFileSync(recipe, "utf8");
const authName = source.match(/^\s*auth:\s*(\S+)\s*$/m)?.[1];
const alts = [...source.matchAll(/^\s*(?:-\s*)?output:\s*(\S+)|^\s*alt:\s*["']?(.+?)["']?\s*$/gm)].reduce(
  (acc, m) => {
    if (m[1]) acc.last = m[1];
    else if (acc.last) acc.map[acc.last] = m[2];
    return acc;
  },
  { map: {}, last: null }
).map;
const shots = [...source.matchAll(/^\s*-?\s*output:\s*(\S+)/gm)].map((m) => m[1]);
const cleaned = source.replace(/^\s*(alt|auth):.*$/gm, "");

const hasCompose = existsSync(composeFile);
console.log(`→ ${shots.length} capture(s) pour ${slug}${hasCompose ? " (instance jetable)" : ""}`);

push(`mkdir -p ${job} && cat > ${job}/shots.yml`, cleaned);
if (hasCompose) push(`cat > ${job}/docker-compose.yml`, readFileSync(composeFile, "utf8"));
if (existsSync(setupFile)) push(`cat > ${job}/setup.sh`, readFileSync(setupFile, "utf8"));

const teardown = () => {
  if (!hasCompose || keep) return;
  try {
    ssh(`cd ${job} && docker compose -p ${project} down -v --remove-orphans >/dev/null 2>&1`);
    console.log("  instance détruite");
  } catch {
    console.error(`  ⚠ destruction échouée — vérifier : ssh ${HOST} "docker compose -p ${project} ps"`);
  }
};
process.on("SIGINT", () => {
  teardown();
  process.exit(130);
});

const outputs = [];
try {
  if (hasCompose) {
    ssh(`cd ${job} && docker compose -p ${project} up -d --quiet-pull`);
    if (existsSync(setupFile)) ssh(`cd ${job} && bash setup.sh`);
  }

  if (authName) {
    // A stale session silently produces screenshots of the login page.
    try {
      ssh(`test -s ${REMOTE}/auth/${authName}.json`, { stdio: ["ignore", "ignore", "ignore"] });
    } catch {
      console.error(
        `session "${authName}" absente sur le runner.\n` +
          `  → ssh shots /opt/shots/${authName}_login.py   (identifiants dans /etc/shots/${authName}.env)`
      );
      process.exit(1);
    }
  }
  const authFlag = authName ? `--auth ${REMOTE}/auth/${authName}.json` : "";
  ssh(`cd ${job} && /opt/shots-venv/bin/shot-scraper multi shots.yml --retina ${authFlag} --fail`);

  // 2x capture -> 1600px WebP q82: sharp on retina, light enough for the page.
  shots.forEach((png, i) => {
    const webp = `${slug}-${i + 1}.webp`;
    const target = resolve(ROOT, "src/data/blog", webp);
    if (existsSync(target) && !force) {
      console.log(`  = ${webp} existe déjà (--force pour écraser)`);
      return;
    }
    ssh(`cd ${job} && cwebp -quiet -resize 1600 0 -q 82 "${png}" -o "${webp}"`);
    const b64 = execFileSync("ssh", [HOST, `base64 -w0 ${job}/${webp}`], {
      encoding: "utf8",
      maxBuffer: 64 * 1024 * 1024,
    });
    writeFileSync(target, Buffer.from(b64, "base64"));
    outputs.push({ webp, alt: alts[png] || "" });
    console.log(`  + src/data/blog/${webp}`);
  });
} finally {
  teardown();
}

if (outputs.length) {
  console.log("\nMarkdown à coller :\n");
  for (const { webp, alt } of outputs) {
    if (!alt) console.log(`<!-- alt manquant : ajoute "alt:" dans ${slug}.yml -->`);
    console.log(`![${alt}](./${webp})\n`);
  }
  console.log("Relis les images avant de committer (IP, e-mails, jetons).");
}
