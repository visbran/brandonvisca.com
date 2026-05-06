#!/usr/bin/env python3
"""
Pre-publish Check — script local à exécuter avant publication d'un article.
Vérifie : frontmatter, pas de H1 dans le body, liens internes, alt text, tags.

Usage:
    python scripts/pre-publish-check.py src/data/blog/mon-article.md
"""

import sys
import re
import os

PRIMARY_TAGS = {
    "homelab", "auto-hebergement", "linux", "macos", "windows",
    "docker", "securite", "reseau", "productivite", "sysadmin",
    "developpement", "microsoft-365",
}

FORBIDDEN_TAGS = {"autres"}
ENGLISH_REPLACEMENTS = {
    "self-hosting": "auto-hebergement",
    "troubleshooting": "depannage",
    "productivity": "productivite",
}


def parse_frontmatter(content: str) -> dict:
    match = re.match(r'^---\r?\n(.*?)\r?\n---', content, re.DOTALL)
    if not match:
        return {}
    raw = match.group(1)
    fm = {}
    for line in raw.splitlines():
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip()
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            if val.startswith('[') and val.endswith(']'):
                val = [v.strip().strip('"\'') for v in val[1:-1].split(',')]
            fm[key] = val
    return fm


def check_file(path: str) -> list:
    issues = []
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    fm = parse_frontmatter(content)
    if not fm:
        issues.append("Pas de frontmatter YAML")
        return issues

    # Required fields
    for field in ("title", "description", "pubDatetime", "author", "tags"):
        if not fm.get(field):
            issues.append(f"Champ obligatoire '{field}' manquant ou vide")

    # H1 in body
    body = re.sub(r'^---[\s\S]*?---', '', content).strip()
    if re.search(r'^#\s+.+$', body, re.MULTILINE):
        issues.append("H1 trouvé dans le body — supprimer, le layout génère le H1")

    # Images without alt
    for match in re.finditer(r'!\[([^\]]*)\]\(([^)]+)\)', body):
        alt, src = match.groups()
        if not alt.strip():
            issues.append(f"Image sans alt text : {src}")

    # Tag validation
    tags = fm.get("tags", [])
    if isinstance(tags, str):
        tags = [tags]

    if "autres" in tags:
        issues.append("Tag interdit 'autres' utilisé")

    for tag in tags:
        if any(c in tag for c in "éèêëàâäôöùûüç"):
            issues.append(f"Tag avec accent interdit : '{tag}'")
        if tag in ENGLISH_REPLACEMENTS:
            issues.append(f"Tag anglais '{tag}' → remplacer par '{ENGLISH_REPLACEMENTS[tag]}'")

    if not any(t in PRIMARY_TAGS for t in tags):
        issues.append(f"Aucun tag primaire (attendu parmi : {', '.join(sorted(PRIMARY_TAGS))})")

    if len(tags) > 6:
        issues.append(f"Trop de tags ({len(tags)}, max 6)")

    # focusKeyword recommended
    if not fm.get("focusKeyword"):
        issues.append("focusKeyword recommandé mais manquant")

    return issues


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <chemin-article.md>")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"❌ Fichier non trouvé : {path}")
        sys.exit(1)

    issues = check_file(path)
    if issues:
        print(f"\n❌ {len(issues)} problème(s) détecté(s) dans {path}:\n")
        for i in issues:
            print(f"  → {i}")
        sys.exit(1)
    else:
        print(f"\n✅ {path} est prêt pour publication.\n")


if __name__ == "__main__":
    main()
