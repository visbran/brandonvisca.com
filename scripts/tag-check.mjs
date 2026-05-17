#!/usr/bin/env node
/**
 * Tag Validation — vérifie la conformité des tags sur tous les articles
 */

import { readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";

const BLOG_DIR = "src/data/blog";

const primaryTags = new Set([
  "homelab",
  "auto-hebergement",
  "linux",
  "macos",
  "windows",
  "docker",
  "securite",
  "reseau",
  "productivite",
  "sysadmin",
  "developpement",
  "microsoft-365",
]);

const forbiddenTags = new Set(["autres", "others"]);
const englishReplacements = {
  "self-hosting": "auto-hebergement",
  productivity: "productivite",
};

const issues = [];

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

if (issues.length) {
  console.error(`\n❌ ${issues.length} problème(s) de tags détecté(s) :\n`);
  for (const issue of issues) {
    console.error(`  [${issue.type}] ${issue.file}`);
    console.error(`    → ${issue.msg}`);
  }
  process.exit(1);
} else {
  console.log("\n✅ Validation des tags passée — aucun problème.\n");
}
