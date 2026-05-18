#!/usr/bin/env node
/**
 * Extrait les hashes SHA-256 des inline scripts depuis dist/ HTML
 * et met à jour dist/_headers avec les hashes corrects.
 *
 * Exécuté en post-build (build:cf dans package.json).
 * Évite la maintenance manuelle des hashes CSP après chaque rebuild.
 */

import { createHash } from "crypto";
import { readFileSync, writeFileSync, readdirSync, statSync } from "fs";
import { join } from "path";

const DIST_DIR = "dist";
const SOURCE_HEADERS = "public/_headers";
const OUTPUT_HEADERS = `${DIST_DIR}/_headers`;

function collectHtmlFiles(dir) {
  const files = [];
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    const st = statSync(full);
    if (st.isDirectory()) files.push(...collectHtmlFiles(full));
    else if (entry.endsWith(".html")) files.push(full);
  }
  return files;
}

function extractInlineScriptHashes(htmlFiles) {
  const hashes = new Set();
  // Matches <script> without src= and not type=application/ld+json
  const re =
    /<script(?![^>]*\bsrc\s*=)(?![^>]*type=['"]application\/ld\+json['"])[^>]*>([\s\S]*?)<\/script>/gi;

  for (const file of htmlFiles) {
    const html = readFileSync(file, "utf-8");
    let m;
    while ((m = re.exec(html)) !== null) {
      const content = m[1];
      if (!content.trim()) continue;
      const hash = createHash("sha256").update(content).digest("base64");
      hashes.add(`'sha256-${hash}'`);
    }
  }
  return [...hashes];
}

const htmlFiles = collectHtmlFiles(DIST_DIR);
const hashes = extractInlineScriptHashes(htmlFiles);

if (hashes.length === 0) {
  console.warn("update-csp-hashes: aucun inline script trouvé — vérifier le build.");
  process.exit(0);
}

// Lire _headers source (public/_headers) comme base
let headers = readFileSync(SOURCE_HEADERS, "utf-8");

// Remplacer la liste de hashes dans script-src
// Pattern : tout ce qui est 'sha256-...' dans la directive script-src
headers = headers.replace(
  /('sha256-[A-Za-z0-9+/=]+'(\s+'sha256-[A-Za-z0-9+/=]+')*)/g,
  hashes.join(" ")
);

writeFileSync(OUTPUT_HEADERS, headers, "utf-8");
console.log(
  `update-csp-hashes: ${hashes.length} hash(es) injectés dans ${OUTPUT_HEADERS}`
);
hashes.forEach(h => console.log(`  ${h}`));
