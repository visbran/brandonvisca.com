#!/usr/bin/env node
/**
 * Tag Validation — vérifie la conformité des tags sur tous les articles
 */

import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";

const BLOG_DIR = "src/data/blog";
const TAGS_FILE = "src/data/tags.json";
const TAG_META_FILE = "src/utils/tagMeta.ts";

/**
 * Vocabulaire fermé : `src/data/tags.json` est la seule source de vérité.
 * Un tag absent de ce fichier fait échouer la validation — c'est ce qui empêche
 * la taxonomie de dériver article après article (171 tags en septembre 2026,
 * dont 112 utilisés une seule fois, avant consolidation).
 */
const vocabulary = JSON.parse(readFileSync(TAGS_FILE, "utf-8"));
const primaryTags = new Set(vocabulary.primary);
const metaTags = new Set(vocabulary.meta);
const allowedTags = new Set([
  ...vocabulary.primary,
  ...vocabulary.meta,
  ...vocabulary.secondary,
]);

/** Seuil de tags orphelins (1 seul article) toléré avant échec. */
const MAX_ORPHAN_TAGS = 3;
/** À partir de ce nombre d'articles, un tag doit avoir ses meta SEO. */
const TAG_META_THRESHOLD = 3;

/** Distance de Levenshtein, pour suggérer le tag existant le plus proche. */
function distance(a, b) {
  const d = Array.from({ length: a.length + 1 }, (_, i) => [i, ...Array(b.length).fill(0)]);
  for (let j = 0; j <= b.length; j++) d[0][j] = j;
  for (let i = 1; i <= a.length; i++) {
    for (let j = 1; j <= b.length; j++) {
      d[i][j] = Math.min(
        d[i - 1][j] + 1,
        d[i][j - 1] + 1,
        d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1)
      );
    }
  }
  return d[a.length][b.length];
}

function suggest(tag) {
  const ranked = [...allowedTags]
    .map((t) => ({ t, d: distance(tag, t) }))
    .sort((x, y) => x.d - y.d)
    .filter(({ d }) => d <= Math.max(3, Math.floor(tag.length / 2)));
  return ranked.length ? ranked.slice(0, 3).map(({ t }) => t).join(", ") : null;
}

const forbiddenTags = new Set(["autres", "others"]);
const englishReplacements = {
  "self-hosting": "auto-hebergement",
  productivity: "productivite",
};

const issues = [];
const usage = new Map();

function getAllMdFiles(dir) {
  const files = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...getAllMdFiles(path));
    } else if (entry.name.endsWith(".md")) {
      files.push(path);
    }
  }
  return files;
}

function extractFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return null;
  const raw = match[1];
  const fm = {};
  const lines = raw.split(/\r?\n/);
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];
    const idx = line.indexOf(":");
    if (idx <= 0) {
      i++;
      continue;
    }
    const key = line.slice(0, idx).trim();
    let val = line.slice(idx + 1).trim();

    if (key === "tags") {
      const tags = [];
      if (val === "") {
        // Format multi-ligne : tags:\n  - foo\n  - bar
        i++;
        while (i < lines.length && lines[i].trim().startsWith("- ")) {
          tags.push(lines[i].trim().replace(/^- /, "").replace(/^["']|["']$/g, ""));
          i++;
        }
        fm.tags = tags;
        continue;
      } else if (val.startsWith("[") && val.endsWith("]")) {
        // Format inline : tags: [foo, bar]
        fm.tags = val
          .slice(1, -1)
          .split(",")
          .map((v) => v.trim().replace(/^["']|["']$/g, ""));
        i++;
        continue;
      } else {
        // Format simple : tags: foo
        fm.tags = [val.replace(/^["']|["']$/g, "")];
        i++;
        continue;
      }
    }

    if (val.startsWith('"') && val.endsWith('"')) val = val.slice(1, -1);
    fm[key] = val;
    i++;
  }
  return fm;
}

for (const file of getAllMdFiles(BLOG_DIR)) {
  const content = readFileSync(file, "utf-8");
  const fm = extractFrontmatter(content);
  if (!fm) {
    issues.push({ file, type: "no-frontmatter", msg: "Pas de frontmatter" });
    continue;
  }
  if (!Array.isArray(fm.tags)) {
    issues.push({ file, type: "invalid-tags", msg: "Champ tags absent ou mal formaté" });
    continue;
  }

  const tags = fm.tags;

  if (tags.length === 0) {
    issues.push({ file, type: "empty-tags", msg: "Tags vides" });
    continue;
  }

  const uniqueTags = new Set(tags);
  if (uniqueTags.size !== tags.length) {
    issues.push({ file, type: "duplicates", msg: `Tags en doublon : ${tags.filter((t, i) => tags.indexOf(t) !== i).join(", ")}` });
  }

  for (const tag of tags) {
    usage.set(tag, (usage.get(tag) ?? 0) + 1);

    if (!allowedTags.has(tag)) {
      const near = suggest(tag);
      issues.push({
        file,
        type: "unknown",
        tag,
        msg: `Tag hors vocabulaire "${tag}"${near ? ` — plus proche : ${near}` : ""}. `
          + `Utiliser un tag de ${TAGS_FILE}, ou l'y ajouter volontairement s'il couvre au moins 2 articles.`,
      });
    }
    if (forbiddenTags.has(tag)) {
      issues.push({ file, type: "forbidden", tag, msg: `Tag interdit "${tag}"` });
    }
    if (/[éèêëàâäôöùûüç]/i.test(tag)) {
      issues.push({ file, type: "accent", tag, msg: `Tag avec accent "${tag}"` });
    }
    if (englishReplacements[tag]) {
      issues.push({
        file,
        type: "english",
        tag,
        msg: `Tag anglais "${tag}" → remplacer par "${englishReplacements[tag]}"`,
      });
    }
  }

  const hasPrimary = tags.some((t) => primaryTags.has(t));
  if (!hasPrimary) {
    issues.push({ file, type: "no-primary", msg: "Aucun tag primaire" });
  }

  if (tags.length > 6) {
    issues.push({ file, type: "count", msg: `${tags.length} tags (max 6)` });
  }
}

// ---------------------------------------------------------------------------
// Vérifications au niveau du corpus : c'est là que se voit la dérive, pas
// article par article.
// ---------------------------------------------------------------------------

const orphanTags = [...usage.entries()]
  .filter(([tag, count]) => count === 1 && !metaTags.has(tag))
  .map(([tag]) => tag)
  .sort();

if (orphanTags.length) {
  const msg = `${orphanTags.length} tag(s) sur un seul article : ${orphanTags.join(", ")}`;
  if (orphanTags.length > MAX_ORPHAN_TAGS) {
    issues.push({
      file: TAGS_FILE,
      type: "orphans",
      msg: `${msg} — au-delà de ${MAX_ORPHAN_TAGS}, ce sont des pages de tag en thin content. `
        + `Fusionner dans un tag parent ou retirer le tag de l'article.`,
    });
  } else {
    console.warn(`⚠️  ${msg} (toléré jusqu'à ${MAX_ORPHAN_TAGS})`);
  }
}

const unusedTags = [...allowedTags].filter((tag) => !usage.has(tag)).sort();
if (unusedTags.length) {
  console.warn(
    `⚠️  ${unusedTags.length} tag(s) déclaré(s) dans ${TAGS_FILE} sans aucun article : `
      + `${unusedTags.join(", ")} — à retirer du vocabulaire.`
  );
}

const tagMetaSource = readFileSync(TAG_META_FILE, "utf-8");
const documentedTags = new Set(
  [...tagMetaSource.matchAll(/^ {2}"?([a-z0-9-]+)"?: \{/gm)].map((m) => m[1])
);
const missingMeta = [...usage.entries()]
  .filter(([tag, count]) => count >= TAG_META_THRESHOLD && !documentedTags.has(tag))
  .map(([tag, count]) => `${tag} (${count})`)
  .sort();
if (missingMeta.length) {
  issues.push({
    file: TAG_META_FILE,
    type: "missing-meta",
    msg: `Tag(s) à ${TAG_META_THRESHOLD}+ articles sans entrée TAG_META : ${missingMeta.join(", ")}. `
      + `Sans entrée, la page de tag tombe sur un title et une description génériques.`,
  });
}

if (issues.length) {
  console.error(`\n❌ ${issues.length} problème(s) de tags détecté(s) :\n`);
  for (const issue of issues) {
    console.error(`  [${issue.type}] ${issue.file}`);
    console.error(`    → ${issue.msg}`);
  }
  process.exit(1);
} else {
  console.log(
    `\n✅ Validation des tags passée — ${usage.size} tags utilisés sur ${allowedTags.size} déclarés, aucun problème.\n`
  );
}
