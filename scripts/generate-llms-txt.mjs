#!/usr/bin/env node
/**
 * Génère public/llms.txt depuis les frontmatter des articles du blog.
 * Format : titre, URL, description, tags, date de publication.
 */

import { readFileSync, writeFileSync, readdirSync } from "node:fs";
import { join } from "node:path";

const BLOG_DIR = "src/data/blog";
const OUTPUT = "public/llms.txt";

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

function slugFromPath(filePath) {
  // src/data/blog/2025-02-16-android-file-transfer-mac-alternatives-test-2025.md
  // or src/data/blog/proxmox/lxc-containers-guide.md
  const base = filePath.replace(BLOG_DIR + "/", "").replace(/\.md$/, "");
  // Remove date prefix if present (YYYY-MM-DD-)
  return base.replace(/^\d{4}-\d{2}-\d{2}-/, "");
}

const articles = [];
for (const file of getAllMdFiles(BLOG_DIR)) {
  const content = readFileSync(file, "utf-8");
  const fm = extractFrontmatter(content);
  if (!fm || fm.draft === "true" || fm.draft === true) continue;
  const slug = slugFromPath(file);
  articles.push({
    title: fm.title || "Sans titre",
    slug,
    description: fm.description || "",
    tags: Array.isArray(fm.tags) ? fm.tags : [],
    pubDatetime: fm.pubDatetime || "",
  });
}

articles.sort((a, b) => new Date(b.pubDatetime) - new Date(a.pubDatetime));

let out = `# llms.txt — Brandon Visca\n`;
out += `# Blog tech francophone : homelab, auto-hébergement, Linux, macOS et indépendance numérique.\n`;
out += `# Dernière mise à jour : ${new Date().toISOString().split("T")[0]}\n`;
out += `# Total articles : ${articles.length}\n\n`;

for (const a of articles) {
  out += `## ${a.title}\n`;
  out += `URL: https://brandonvisca.com/${a.slug}/\n`;
  out += `Description: ${a.description}\n`;
  out += `Tags: ${a.tags.join(", ")}\n`;
  out += `Publié: ${a.pubDatetime}\n\n`;
}

writeFileSync(OUTPUT, out, "utf-8");
console.log(`✅ llms.txt régénéré : ${articles.length} articles`);
