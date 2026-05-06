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

const forbiddenTags = new Set(["autres"]);
const englishReplacements = {
  "self-hosting": "auto-hebergement",
  troubleshooting: "depannage",
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
  for (const line of raw.split("\n")) {
    const idx = line.indexOf(":");
    if (idx > 0) {
      const key = line.slice(0, idx).trim();
      let val = line.slice(idx + 1).trim();
      if (val.startsWith('"') && val.endsWith('"')) val = val.slice(1, -1);
      if (val.startsWith("[") && val.endsWith("]")) {
        val = val
          .slice(1, -1)
          .split(",")
          .map((v) => v.trim().replace(/^["']|["']$/g, ""));
      }
      fm[key] = val;
    }
  }
  return fm;
}

for (const file of getAllMdFiles(BLOG_DIR)) {
  const content = readFileSync(file, "utf-8");
  const fm = extractFrontmatter(content);
  if (!fm || !Array.isArray(fm.tags)) continue;

  const tags = fm.tags;

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
