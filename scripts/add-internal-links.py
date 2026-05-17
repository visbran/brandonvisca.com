#!/usr/bin/env python3
"""
Ajoute une section "## Articles connexes" aux articles qui n'en ont pas.
Sélection par overlap de tags (Jaccard), au moins 3 suggestions par article.
"""

import os
import re
import yaml
import sys
from collections import defaultdict

BLOG_DIR = "src/data/blog"
MIN_SUGGESTIONS = 3
MAX_SUGGESTIONS = 4


def parse_article(path):
    content = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)", content, re.DOTALL)
    if not m:
        return None, content
    try:
        fm = yaml.safe_load(m.group(1))
    except Exception as e:
        print(f"  YAML error in {path}: {e}", file=sys.stderr)
        return None, content
    return fm, content


def jaccard(tags_a, tags_b):
    a, b = set(tags_a), set(tags_b)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def build_index():
    articles = []
    for fname in sorted(os.listdir(BLOG_DIR)):
        if not fname.endswith(".md"):
            continue
        path = os.path.join(BLOG_DIR, fname)
        fm, content = parse_article(path)
        if fm is None:
            continue
        slug = fname.replace(".md", "")
        articles.append(
            {
                "slug": slug,
                "title": fm.get("title", slug),
                "tags": fm.get("tags", []) or [],
                "has_section": "## Articles connexes" in content,
                "path": path,
                "content": content,
            }
        )
    return articles


def find_related(article, all_articles, n=MAX_SUGGESTIONS):
    scored = []
    for other in all_articles:
        if other["slug"] == article["slug"]:
            continue
        score = jaccard(article["tags"], other["tags"])
        scored.append((score, other["slug"], other["title"]))
    scored.sort(key=lambda x: -x[0])
    # At least MIN_SUGGESTIONS even if score=0
    top = scored[:n]
    if len(top) < MIN_SUGGESTIONS:
        top = scored[:MIN_SUGGESTIONS]
    return top


def make_section(related):
    lines = ["\n\n## Articles connexes\n"]
    for score, slug, title in related:
        lines.append(f"- [{title}](/{slug}/)")
    return "\n".join(lines) + "\n"


def main(dry_run=False):
    articles = build_index()
    missing = [a for a in articles if not a["has_section"]]

    print(f"Total articles : {len(articles)}")
    print(f"Sans Articles connexes : {len(missing)}")
    print()

    for article in missing:
        related = find_related(article, articles)
        section = make_section(related)

        print(f"  → {article['slug']}")
        for score, slug, title in related:
            print(f"       ({score:.2f}) {slug}")

        if not dry_run:
            new_content = article["content"].rstrip("\n") + section
            open(article["path"], "w", encoding="utf-8").write(new_content)

    if dry_run:
        print("\n[DRY RUN] Aucune modification effectuée.")
    else:
        print(f"\n{len(missing)} articles mis à jour.")


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv or "-n" in sys.argv
    main(dry_run=dry)
