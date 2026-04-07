#!/usr/bin/env python3
"""
inject-toc.py — Injecte le titre "## Table des matières" dans les articles du blog.

Le thème utilise remark-toc + remark-collapse (astro.config.ts) :
  heading: "Table des matières" → le plugin génère automatiquement le contenu.
  Il ne faut PAS écrire les items manuellement — juste le titre.

Format injecté (le plugin fait le reste) :

  ## Table des matières

Règles :
  - Seuls les titres H2 (## ou Setext ----) sont comptés
  - TOC insérée avant le premier H2 du corps
  - Articles avec "## Table des matières" existant : ignorés (sauf --force)
  - Articles avec < 4 sections H2 : ignorés
  - Dry-run par défaut — écriture avec --confirm

Usage :
  python3 scripts/inject-toc.py                          # Liste les articles éligibles sans TOC
  python3 scripts/inject-toc.py article.md               # Dry-run sur un article
  python3 scripts/inject-toc.py article.md --confirm     # Injecte la TOC
  python3 scripts/inject-toc.py --all --confirm          # Traite tous les articles éligibles
  python3 scripts/inject-toc.py --all --force --confirm  # Remplace les TOC non conformes aussi
"""

import sys
import re
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / "src/data/blog"
TOC_MIN_H2 = 4

# Correspondance exacte avec la config remark-toc dans astro.config.ts
TOC_HEADING_RE = re.compile(r"^##\s+Table des matières\s*$", re.MULTILINE)

# Aussi détecter les TOC non conformes (emoji, items manuels) pour --force
TOC_NONCONFORM_RE = re.compile(
    r"^##\s+(?:📑\s*)?(?:Table des matières|Sommaire|Table of contents)\s*$",
    re.MULTILINE | re.IGNORECASE,
)

ATX_H2_RE    = re.compile(r"^##\s+(?!#)", re.MULTILINE)
SETEXT_H2_RE = re.compile(r"^([^\n`#>|\-][^\n]+)\n-{3,}\s*$", re.MULTILINE)


def parse_frontmatter(content: str) -> tuple[str, str]:
    """Retourne (bloc_frontmatter, body_str)."""
    if not content.startswith("---"):
        return "", content
    end = content.find("\n---", 3)
    if end == -1:
        return "", content
    return content[:end + 4], content[end + 4:]


def count_h2(body: str) -> int:
    """Compte les H2 ATX et Setext dans le body (hors blocs de code)."""
    body_no_code = re.sub(r"```[\s\S]*?```", lambda m: "\n" * m.group().count("\n"), body)
    atx_count = len(ATX_H2_RE.findall(body_no_code))
    # Exclure les séparateurs --- (>= 3 tirets précédés d'une ligne vide)
    setext_count = len(SETEXT_H2_RE.findall(body_no_code))
    return atx_count + setext_count


def find_first_h2_pos(body: str) -> int:
    """Position dans le body avant laquelle insérer la TOC."""
    body_no_code = re.sub(r"```[\s\S]*?```", lambda m: "\n" * m.group().count("\n"), body)
    candidates = []
    m_atx = ATX_H2_RE.search(body_no_code)
    if m_atx:
        candidates.append(m_atx.start())
    m_set = SETEXT_H2_RE.search(body_no_code)
    if m_set:
        candidates.append(m_set.start())
    return min(candidates) if candidates else len(body)


def remove_nonconform_toc(body: str) -> str:
    """Supprime une TOC non conforme (emoji ou items manuels) et retourne le body nettoyé."""
    m = TOC_NONCONFORM_RE.search(body)
    if not m:
        return body

    toc_start = m.start()
    after_heading = body[m.end():]

    # Chercher le prochain H2 (ATX seulement pour la délimitation de la TOC)
    next_h2 = re.search(r"^##\s+", after_heading, re.MULTILINE)
    if next_h2:
        toc_end = m.end() + next_h2.start()
    else:
        toc_end = len(body)

    return body[:toc_start] + body[toc_end:]


def process_file(filepath: Path, confirm: bool, force: bool) -> bool:
    """Traite un article. Retourne True si TOC injectée ou prévue."""
    content = filepath.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)

    has_correct_toc = bool(TOC_HEADING_RE.search(body))
    has_any_toc     = bool(TOC_NONCONFORM_RE.search(body))

    if has_correct_toc and not force:
        print(f"  ⏭️  TOC conforme déjà présente")
        return False

    if has_any_toc and not force:
        print(f"  ⚠️  TOC non conforme (emoji/items manuels) — utiliser --force pour corriger")
        return False

    h2_count = count_h2(body)
    if h2_count < TOC_MIN_H2:
        print(f"  ℹ️  {h2_count} section(s) H2 — TOC non nécessaire (seuil : {TOC_MIN_H2})")
        return False

    # Nettoyer la TOC non conforme si --force
    if has_any_toc and force:
        body = remove_nonconform_toc(body)
        print(f"  🗑️  TOC non conforme supprimée")

    # Insérer ## Table des matières avant le premier H2
    insert_pos = find_first_h2_pos(body)
    prefix = body[:insert_pos].rstrip("\n") + "\n\n"
    suffix = body[insert_pos:]
    new_body = prefix + "## Table des matières\n\n" + suffix

    print(f"  📑 TOC '{filepath.name}' — {h2_count} sections H2 détectées")
    print(f"     → remark-toc générera le contenu automatiquement")

    if not confirm:
        print(f"  [Dry-run] Pour injecter : python3 scripts/inject-toc.py {filepath.name} --confirm")
        return True

    filepath.write_text(fm + new_body, encoding="utf-8")
    print(f"  ✅ TOC injectée → {filepath.name}")
    return True


def list_candidates() -> None:
    """Affiche les articles éligibles sans TOC conforme."""
    files = sorted(BLOG_DIR.glob("*.md"))
    missing, nonconform = [], []

    for f in files:
        content = f.read_text(encoding="utf-8")
        _, body = parse_frontmatter(content)
        h2 = count_h2(body)
        if h2 < TOC_MIN_H2:
            continue
        if TOC_HEADING_RE.search(body):
            continue
        if TOC_NONCONFORM_RE.search(body):
            nonconform.append((f, h2))
        else:
            missing.append((f, h2))

    if nonconform:
        print(f"⚠️  TOC non conforme (emoji/items manuels) — {len(nonconform)} article(s) :\n")
        for f, h2 in nonconform:
            print(f"  • {f.name} ({h2} H2)")
        print(f"\n  → Corriger : python3 scripts/inject-toc.py --all --force --confirm\n")

    if missing:
        print(f"📋 Sans TOC (≥{TOC_MIN_H2} H2) — {len(missing)} article(s) :\n")
        for f, h2 in missing:
            print(f"  • {f.name} ({h2} H2)")
        print(f"\n  → Injecter : python3 scripts/inject-toc.py --all --confirm")

    if not missing and not nonconform:
        print("✅ Tous les articles éligibles ont une TOC conforme.")


def main():
    args = sys.argv[1:]
    confirm  = "--confirm" in args
    force    = "--force"   in args
    all_mode = "--all"     in args
    args = [a for a in args if not a.startswith("--")]

    if not args and not all_mode:
        list_candidates()
        return

    files = (sorted(BLOG_DIR.glob("*.md")) if all_mode
             else [BLOG_DIR / args[0] if not Path(args[0]).is_absolute() else Path(args[0])])

    for f in files:
        if not f.exists():
            print(f"❌ Fichier introuvable : {f}")
            continue

    if not confirm:
        print("🔍 MODE DRY-RUN — utiliser --confirm pour écrire\n")

    processed = 0
    for filepath in files:
        if not filepath.exists():
            continue
        print(f"\n📄 {filepath.name}")
        ok = process_file(filepath, confirm=confirm, force=force)
        if ok and confirm:
            processed += 1

    if confirm and all_mode:
        print(f"\n{'─' * 50}")
        print(f"✅ {processed} article(s) mis à jour")


if __name__ == "__main__":
    main()
