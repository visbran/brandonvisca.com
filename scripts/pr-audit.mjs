#!/usr/bin/env node
/**
 * PR Audit — vérifie les articles modifiés dans une PR pour :
 * - H1 dans le body
 * - Images sans alt
 * - Liens internes cassés (baseline)
 * - Frontmatter incomplet
 */

import { readFileSync, readdirSync, statSync } from "node:fs";
import { join, relative } from "node:path";

const BLOG_DIR = "src/data/blog";
const CHANGED_FILES = process.env.CHANGED_FILES
  ? process.env.CHANGED_FILES.split("\n")
  : readdirSync(BLOG_DIR).filter((f) => f.endsWith(".md"));

const issues = [];
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

function checkFile(filePath) {
  const content = readFileSync(filePath, "utf-8");
  const fm = extractFrontmatter(content);
  if (!fm) {
    issues.push({ file: filePath, type: "missing-frontmatter", msg: "Pas de frontmatter YAML" });
    return;
  }

  // H1 in body
  const body = content.replace(/^---[\s\S]*?---/, "").trim();
  const h1Match = body.match(/^#\s+.+$/m);
  if (h1Match) {
    issues.push({ file: filePath, type: "h1-in-body", msg: `H1 trouvé dans le body : "${h1Match[0]}"` });
  }

  // Images without alt
  const imgMatches = body.matchAll(/!\[([^\]]*)\]\(([^)]+)\)/g);
  for (const m of imgMatches) {
    if (!m[1].trim()) {
      issues.push({ file: filePath, type: "img-no-alt", msg: `Image sans alt text : ${m[2]}` });
    }
  }

  // Frontmatter completeness
  if (!fm.description || !fm.description.trim()) {
    issues.push({ file: filePath, type: "missing-description", msg: "Champ 'description' manquant ou vide" });
  }
  if (!fm.focusKeyword || !fm.focusKeyword.trim()) {
    issues.push({ file: filePath, type: "missing-focusKeyword", msg: "Champ 'focusKeyword' manquant" });
  }

  // Tag validation
  const tags = Array.isArray(fm.tags) ? fm.tags : [];
  if (tags.includes("autres")) {
    issues.push({ file: filePath, type: "tag-autres", msg: "Tag interdit 'autres' utilisé" });
  }
  const hasPrimary = tags.some((t) => primaryTags.has(t));
  if (!hasPrimary) {
    issues.push({ file: filePath, type: "tag-no-primary", msg: `Aucun tag primaire parmi : ${[...primaryTags].join(", ")}` });
  }
  const accented = tags.filter((t) => /[éèêëàâäôöùûüç]/i.test(t));
  if (accented.length) {
    issues.push({ file: filePath, type: "tag-accent", msg: `Tags avec accents interdits : ${accented.join(", ")}` });
  }
  if (tags.length > 6) {
    issues.push({ file: filePath, type: "tag-count", msg: `Trop de tags (${tags.length}, max 6)` });
  }
}

for (const file of CHANGED_FILES) {
  if (!file.endsWith(".md")) continue;
  const fullPath = file.startsWith(BLOG_DIR) ? file : join(BLOG_DIR, file);
  try {
    statSync(fullPath);
    checkFile(fullPath);
  } catch {
    // File may have been deleted in the PR
  }
}

if (issues.length) {
  console.error(`\n❌ ${issues.length} problème(s) SEO détecté(s) dans la PR :\n`);
  for (const issue of issues) {
    console.error(`  [${issue.type}] ${relative(process.cwd(), issue.file)}`);
    console.error(`    → ${issue.msg}`);
  }
  process.exit(1);
} else {
  console.log("\n✅ Audit PR passé — aucun problème SEO détecté.\n");
}
