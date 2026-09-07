#!/usr/bin/env python3
"""Vérifie que chaque lien interne d'un article pointe vers un slug qui existe.

C'est le contrôle qui manquait le 2026-09-07 : le commit 045f37d a ajouté des liens
vers `/betterdisplay-macos-hidpi-ddc/` alors que l'article venait d'être reverté, et
rien ne l'a signalé avant la mise en ligne.

Usage :
    python3 scripts/check-internal-links.py                # tous les articles
    python3 scripts/check-internal-links.py fichier.md ... # une sélection

Sort en 1 s'il reste au moins un lien mort — utilisable comme garde de CI.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BLOG_DIR = Path(__file__).resolve().parent.parent / "src" / "data" / "blog"

# Liens markdown internes absolus, hors ancres.
LINK_RE = re.compile(r"\]\((/[^)\s#]+?)/?\)")
SKIP_PREFIXES = ("/images/", "/assets/", "/posts/", "/tags/", "/rss", "/llms", "/api/")


def known_slugs() -> set[str]:
    return {p.stem for p in BLOG_DIR.glob("*.md")} | {p.stem for p in BLOG_DIR.glob("*.mdx")}


def internal_targets(text: str) -> list[str]:
    body = re.sub(r"```[\s\S]*?```", "", text)
    targets = []
    for match in LINK_RE.finditer(body):
        target = match.group(1)
        if target.startswith(SKIP_PREFIXES) or target.count("/") > 1:
            continue
        slug = target.strip("/")
        if slug:
            targets.append(slug)
    return targets


def check(paths: list[Path]) -> list[tuple[str, str]]:
    known = known_slugs()
    dead: list[tuple[str, str]] = []
    for path in paths:
        if not path.is_file():
            continue
        for slug in internal_targets(path.read_text(encoding="utf-8")):
            if slug not in known:
                dead.append((path.name, slug))
    return dead


def main(argv: list[str]) -> int:
    paths = [Path(a) for a in argv] if argv else sorted(BLOG_DIR.glob("*.md")) + sorted(
        BLOG_DIR.glob("*.mdx")
    )
    dead = check(paths)
    if not dead:
        print(f"✅ {len(paths)} fichiers, aucun lien interne mort")
        return 0
    print(f"❌ {len(dead)} lien(s) interne(s) mort(s) :")
    for filename, slug in dead:
        print(f"  {filename} -> /{slug}/")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
