#!/usr/bin/env node
/**
 * Redirects Validation — garde-fou sur `public/_redirects`.
 *
 * Cloudflare documente 2 000 redirections statiques et 100 dynamiques, mais le
 * 2026-09-24 un fichier de 148 règles n'a vu que ses ~120 premières appliquées :
 * les 28 dernières renvoyaient un 404 en production, sans le moindre
 * avertissement au déploiement. On reste donc sous un plafond prudent, et les
 * règles les plus anciennes (URLs WordPress, celles qui portent du trafic réel)
 * restent en tête de fichier.
 */

import { readFileSync } from "node:fs";

const FILE = "public/_redirects";
/** Plafond prudent : constaté cassant autour de 120 règles. */
const MAX_RULES = 110;
/** Limite Cloudflare documentée pour les règles dynamiques (splat, :placeholder). */
const MAX_DYNAMIC = 100;
/** Limite Cloudflare documentée par déclaration. */
const MAX_LINE_LENGTH = 1000;

const issues = [];
const lines = readFileSync(FILE, "utf-8").split(/\r?\n/);
const rules = [];

lines.forEach((line, index) => {
  const trimmed = line.trim();
  if (!trimmed || trimmed.startsWith("#")) return;

  const parts = trimmed.split(/\s+/);
  const lineNo = index + 1;

  if (parts.length < 2) {
    issues.push(`${FILE}:${lineNo} — règle incomplète : "${trimmed}"`);
    return;
  }
  if (line.length > MAX_LINE_LENGTH) {
    issues.push(`${FILE}:${lineNo} — déclaration de ${line.length} caractères (max ${MAX_LINE_LENGTH})`);
  }

  const [from, to, status] = parts;
  if (status && !/^\d{3}$/.test(status)) {
    issues.push(`${FILE}:${lineNo} — code de statut invalide : "${status}"`);
  }
  rules.push({ from, to, lineNo, dynamic: from.includes("*") || from.includes(":") });
});

const seen = new Map();
for (const { from, lineNo } of rules) {
  if (seen.has(from)) {
    issues.push(
      `${FILE}:${lineNo} — source en doublon "${from}" (déjà ligne ${seen.get(from)}) : ` +
        `seule la première règle s'applique.`
    );
  } else {
    seen.set(from, lineNo);
  }
}

const dynamic = rules.filter(r => r.dynamic);

if (rules.length > MAX_RULES) {
  issues.push(
    `${rules.length} règles (plafond prudent ${MAX_RULES}) — au-delà, Cloudflare en ignore ` +
      `silencieusement une partie. Regrouper les règles, ou passer par Bulk Redirects.`
  );
}
if (dynamic.length > MAX_DYNAMIC) {
  issues.push(`${dynamic.length} règles dynamiques (max ${MAX_DYNAMIC} chez Cloudflare)`);
}

if (issues.length) {
  console.error(`\n❌ ${issues.length} problème(s) dans ${FILE} :\n`);
  for (const issue of issues) console.error(`  → ${issue}`);
  process.exit(1);
}

console.log(
  `\n✅ ${FILE} valide — ${rules.length} règles dont ${dynamic.length} dynamiques ` +
    `(plafond prudent ${MAX_RULES}).\n`
);
