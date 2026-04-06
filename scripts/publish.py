#!/usr/bin/env python3
"""
publish.py — Publie un article du vault Obsidian vers src/data/blog/.

Workflow :
  1. Lit un article depuis Content/Articles/03-Pret-Publication/
  2. Convertit le frontmatter hybride → frontmatter Astro pur
  3. Détermine le slug (strip préfixe date YYYY-MM-DD-)
  4. Valide (description 120-155 chars, champs requis)
  5. Dry-run par défaut — écrit avec --confirm
  6. Déplace l'article vault → 04-Publies/ après publication

Usage:
  python3 scripts/publish.py                          # Liste les articles prêts
  python3 scripts/publish.py article.md               # Dry-run d'un article
  python3 scripts/publish.py article.md --confirm     # Publie
  python3 scripts/publish.py --all --confirm          # Publie tous les prêts
  python3 scripts/publish.py article.md --draft       # Publie en draft (preview)
"""

import sys
import re
import shutil
import yaml
from pathlib import Path
from datetime import datetime

# ── Chemins ───────────────────────────────────────────────────────────────────

VAULT_ROOT = Path.home() / "Documents/brandon-knowledge"
READY_DIR  = VAULT_ROOT / "Content/Articles/03-Pret-Publication"
DONE_DIR   = VAULT_ROOT / "Content/Articles/04-Publies"
BLOG_DIR   = Path(__file__).parent.parent / "src/data/blog"

# ── Champs Astro à conserver (depuis le vault hybrid) ─────────────────────────

ASTRO_FIELDS = {
    "title", "description", "pubDatetime", "modDatetime",
    "author", "tags", "featured", "draft", "focusKeyword",
    "faqs", "ogImage", "canonicalURL", "timezone",
}

# ── Constantes de validation ───────────────────────────────────────────────────

PRIMARY_TAGS = {
    "homelab", "auto-hebergement", "linux", "macos", "windows",
    "docker", "securite", "reseau", "productivite", "sysadmin",
    "developpement", "microsoft-365",
}
LEVEL_TAGS = {"debutant", "intermediaire", "avance"}

EDITORIAL_SECTIONS_RE = re.compile(
    r"^## (?:📊 Paramètres Rank Math|🔗 Maillage interne|📝 Articles complémentaires"
    r"|🔄 Maillage inverse|Maillage inverse|Articles complémentaires suggérés)",
    re.MULTILINE,
)
WIKI_LINK_RE = re.compile(r"\[\[[^\]]+\]\]")

FAQ_PLACEHOLDERS = {"", "Question fréquente 1 ?", "Question fréquente 2 ?", "Réponse détaillée"}

TOC_HEADING_RE = re.compile(
    r"^##\s+(?:📑\s*)?(?:Table des matières|Sommaire|Table of contents)\s*$",
    re.MULTILINE | re.IGNORECASE,
)

# ── Helpers ───────────────────────────────────────────────────────────────────

DATE_PREFIX_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")


def _heading_anchor(text: str) -> str:
    """Génère un ancre GitHub-style depuis un texte de titre."""
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[\s_]+", "-", text.strip())
    return re.sub(r"-+", "-", text).strip("-")


def slugify_title(title: str) -> str:
    """Crée un slug kebab-case depuis un titre."""
    import unicodedata
    # Normalisation unicode → ASCII
    title = unicodedata.normalize("NFKD", title)
    title = "".join(c for c in title if not unicodedata.combining(c))
    title = title.lower()
    # Remplacer tout ce qui n'est pas alphanumérique par -
    title = re.sub(r"[^a-z0-9]+", "-", title)
    title = title.strip("-")
    # Limiter la longueur du slug à 70 chars
    if len(title) > 70:
        title = title[:70].rsplit("-", 1)[0]
    return title


def derive_slug(filepath: Path, frontmatter: dict) -> str:
    """Détermine le slug à partir du nom de fichier."""
    name = filepath.stem  # sans .md

    # Fichier WP type p{id} → slugifier le titre
    if re.match(r"^p\d+$", name):
        title = frontmatter.get("title", "")
        if title:
            return slugify_title(title)
        return name

    # Supprimer le préfixe date YYYY-MM-DD-
    slug = DATE_PREFIX_RE.sub("", name)
    return slug


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Retourne (dict_frontmatter, body_str)."""
    if not content.startswith("---"):
        return {}, content

    end = content.find("\n---", 3)
    if end == -1:
        return {}, content

    fm_raw = content[4:end]
    body = content[end + 4:]

    try:
        fm = yaml.safe_load(fm_raw) or {}
    except yaml.YAMLError as e:
        print(f"  ❌ Erreur YAML : {e}", file=sys.stderr)
        fm = {}

    return fm, body


def build_astro_frontmatter(vault_fm: dict, slug: str, keep_draft: bool) -> dict:
    """Extrait et construit le frontmatter Astro pur depuis le vault hybride."""
    astro = {}

    # Champs directs
    for field in ASTRO_FIELDS:
        if field in vault_fm and vault_fm[field] is not None:
            astro[field] = vault_fm[field]

    # draft : false par défaut à la publication, sauf si --draft
    astro["draft"] = keep_draft

    # Assurer les champs par défaut
    if "author" not in astro:
        astro["author"] = "Brandon Visca"
    if "featured" not in astro:
        astro["featured"] = False
    if "tags" not in astro or not astro["tags"]:
        astro["tags"] = ["homelab"]

    return astro


def quote_yaml(value: str) -> str:
    SPECIAL = [':', '#', '[', ']', '{', '}', '&', '*', '!', '|', '>', '%', '@', "'"]
    if any(c in value for c in SPECIAL) or value.startswith('"'):
        escaped = value.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{escaped}"'
    return value


def serialize_astro_frontmatter(fm: dict) -> str:
    """Sérialise le frontmatter Astro en YAML ordonné."""
    ORDER = [
        "title", "description", "pubDatetime", "modDatetime",
        "author", "tags", "featured", "draft",
        "focusKeyword", "faqs",
        "ogImage", "canonicalURL", "timezone",
    ]

    lines = ["---"]
    for key in ORDER:
        if key not in fm:
            continue
        value = fm[key]

        if key == "faqs" and isinstance(value, list) and value:
            lines.append("faqs:")
            for faq in value:
                q = str(faq.get("question", "")).replace('"', '\\"')
                a = str(faq.get("answer", "")).replace('"', '\\"')
                lines.append(f'  - question: "{q}"')
                lines.append(f'    answer: "{a}"')
            continue

        if key == "tags" and isinstance(value, list):
            lines.append("tags:")
            for tag in value:
                lines.append(f"  - {tag}")
            continue

        if isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        elif isinstance(value, str):
            lines.append(f"{key}: {quote_yaml(value)}")
        elif value is not None:
            lines.append(f"{key}: {value}")

    lines.append("---")
    return "\n".join(lines)


# ── Validation ────────────────────────────────────────────────────────────────

def validate(fm: dict, slug: str, body: str = "") -> list[dict]:
    """Retourne une liste d'issues {type, msg}."""
    issues = []

    # ── Champs requis ──────────────────────────────────────────────────────────
    for field in ("title", "description", "pubDatetime", "tags"):
        if not fm.get(field):
            issues.append({"type": "error", "msg": f"Champ requis manquant : `{field}`"})

    # ── Description longueur ──────────────────────────────────────────────────
    desc = fm.get("description", "")
    if desc:
        length = len(str(desc))
        if not (120 <= length <= 155):
            issues.append({
                "type": "warning",
                "msg": f"description : {length} chars (attendu 120-155)"
            })

    # ── Slug conflit ──────────────────────────────────────────────────────────
    target = BLOG_DIR / f"{slug}.md"
    if target.exists():
        issues.append({
            "type": "warning",
            "msg": f"Fichier existant dans blog : `{slug}.md` (sera écrasé)"
        })

    # ── focusKeyword ──────────────────────────────────────────────────────────
    if not fm.get("focusKeyword"):
        issues.append({"type": "info", "msg": "Pas de focusKeyword — SEO non optimisé"})

    # ── Tags ──────────────────────────────────────────────────────────────────
    tags = fm.get("tags") or []
    if tags:
        if len(tags) > 6:
            issues.append({"type": "warning", "msg": f"Trop de tags : {len(tags)} (max 6) — {tags}"})
        if not any(t in PRIMARY_TAGS for t in tags):
            issues.append({"type": "warning", "msg": f"Aucun tag primaire — choisir parmi : homelab, macos, linux, docker, securite…"})
        if not any(t in LEVEL_TAGS for t in tags):
            issues.append({"type": "warning", "msg": "Tag de niveau manquant — ajouter `debutant`, `intermediaire` ou `avance`"})

    # ── FAQs ──────────────────────────────────────────────────────────────────
    faqs = fm.get("faqs") or []
    if faqs:
        empty_q = [f for f in faqs if not str(f.get("question", "")).strip()
                   or str(f.get("question", "")).strip() in FAQ_PLACEHOLDERS]
        empty_a = [f for f in faqs if not str(f.get("answer", "")).strip()
                   or str(f.get("answer", "")).strip() in FAQ_PLACEHOLDERS]
        if empty_q:
            issues.append({"type": "warning", "msg": f"{len(empty_q)} FAQ(s) avec question vide ou placeholder — à remplir"})
        if empty_a:
            issues.append({"type": "warning", "msg": f"{len(empty_a)} FAQ(s) avec réponse vide ou placeholder — à remplir"})
        if len(faqs) > 6:
            issues.append({"type": "info", "msg": f"{len(faqs)} FAQs — Google affiche généralement 3-4 max dans les résultats"})
    else:
        issues.append({"type": "info", "msg": "Pas de FAQs — ajouter pour le schema FAQPage JSON-LD (SEO)"})

    # ── Corps : sections éditorielles ─────────────────────────────────────────
    if body:
        if EDITORIAL_SECTIONS_RE.search(body):
            issues.append({"type": "error",
                           "msg": "Section éditoriale détectée (Rank Math / Maillage interne) — supprimer avant publication"})

        wiki_links = WIKI_LINK_RE.findall(body)
        if wiki_links:
            issues.append({"type": "error",
                           "msg": f"{len(wiki_links)} wiki-link(s) [[...]] non convertis — liens cassés en production"})

    # ── Table des matières ────────────────────────────────────────────────────
    if body:
        toc_match = TOC_HEADING_RE.search(body)
        if toc_match:
            toc_start = toc_match.end()
            next_h = re.search(r"^##\s+", body[toc_start:], re.MULTILINE)
            toc_body = body[toc_start: toc_start + next_h.start()] if next_h else body[toc_start:]
            toc_anchors = re.findall(r"\(#[\w%.-]+\)", toc_body)
            if not toc_anchors:
                issues.append({"type": "warning",
                               "msg": "Table des matières sans ancres `(#anchor)` — vérifier le format des liens"})

    return issues


# ── Traitement d'un fichier ───────────────────────────────────────────────────

def process_file(filepath: Path, confirm: bool, keep_draft: bool) -> bool:
    """
    Traite un article vault. Retourne True si publication réussie/prévue.
    """
    print(f"\n📄 {filepath.name}")

    content = filepath.read_text(encoding="utf-8")
    vault_fm, body = parse_frontmatter(content)

    if not vault_fm:
        print("  ❌ Frontmatter manquant — ignoré")
        return False

    # Déterminer le slug
    slug = derive_slug(filepath, vault_fm)
    print(f"  → Slug : {slug}")

    # Construire le frontmatter Astro
    astro_fm = build_astro_frontmatter(vault_fm, slug, keep_draft=keep_draft)

    # Valider
    issues = validate(astro_fm, slug, body=body)
    errors = [i for i in issues if i["type"] == "error"]
    warnings = [i for i in issues if i["type"] == "warning"]
    infos = [i for i in issues if i["type"] == "info"]

    ICONS = {"error": "❌", "warning": "⚠️ ", "info": "ℹ️ "}
    for issue in issues:
        print(f"  {ICONS[issue['type']]} {issue['msg']}")

    if errors:
        print(f"  🛑 {len(errors)} erreur(s) bloquante(s) — publication annulée")
        return False

    # Sérialiser le contenu final
    new_fm = serialize_astro_frontmatter(astro_fm)

    # Nettoyer le body : supprimer les éventuels titres H1 en double (déjà dans title)
    clean_body = body.lstrip("\n")

    new_content = new_fm + "\n" + clean_body

    target_path = BLOG_DIR / f"{slug}.md"

    if not confirm:
        # Afficher le frontmatter produit
        print(f"\n  --- Frontmatter Astro ---")
        print(new_fm)
        print(f"\n  → Destination : src/data/blog/{slug}.md")
        print(f"  → Vault cible : 04-Publies/{filepath.name}")
        if warnings:
            print(f"  ⚠️  {len(warnings)} avertissement(s) — publication possible")
        print(f"\n  [Dry-run] Pour publier : python3 scripts/publish.py {filepath.name} --confirm")
        return True

    # Écriture
    target_path.write_text(new_content, encoding="utf-8")
    print(f"  ✅ Écrit → src/data/blog/{slug}.md")

    # Déplacer vers 04-Publies/
    dest_vault = DONE_DIR / filepath.name
    if dest_vault.exists():
        dest_vault.unlink()
    shutil.move(str(filepath), str(dest_vault))
    print(f"  📦 Déplacé → 04-Publies/{filepath.name}")

    return True


# ── Listing ───────────────────────────────────────────────────────────────────

def list_ready() -> None:
    """Affiche les articles prêts à publier."""
    files = sorted(READY_DIR.glob("*.md"))
    if not files:
        print("📭 Aucun article dans 03-Pret-Publication/")
        return

    print(f"📋 Articles prêts à publier ({len(files)}) :\n")
    for f in files:
        content = f.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(content)
        title = fm.get("title", "(pas de titre)")
        slug = derive_slug(f, fm)
        desc_len = len(str(fm.get("description", "")))
        focus = fm.get("focusKeyword", "—")

        status_icons = []
        if not fm.get("description"):
            status_icons.append("❌ desc manquante")
        elif not (120 <= desc_len <= 155):
            status_icons.append(f"⚠️  desc {desc_len}c")
        if not fm.get("focusKeyword"):
            status_icons.append("ℹ️  pas de focusKeyword")

        status = " | ".join(status_icons) if status_icons else "✅ prêt"
        print(f"  • {f.name}")
        print(f"    Titre    : {title[:60]}")
        print(f"    Slug     : {slug}")
        print(f"    Keyword  : {focus}")
        print(f"    Statut   : {status}")
        print()


# ── Point d'entrée ────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    confirm   = "--confirm" in args
    keep_draft = "--draft" in args
    all_mode  = "--all" in args
    args = [a for a in args if not a.startswith("--")]

    if not args and not all_mode:
        list_ready()
        return

    if all_mode:
        files = sorted(READY_DIR.glob("*.md"))
        if not files:
            print("📭 Aucun article dans 03-Pret-Publication/")
            return
    else:
        target = args[0]
        filepath = Path(target)
        if not filepath.is_absolute():
            filepath = READY_DIR / target
        if not filepath.exists():
            print(f"❌ Fichier introuvable : {filepath}")
            sys.exit(1)
        files = [filepath]

    if not confirm:
        print("🔍 MODE DRY-RUN — utiliser --confirm pour publier\n")

    published = 0
    for filepath in files:
        ok = process_file(filepath, confirm=confirm, keep_draft=keep_draft)
        if ok and confirm:
            published += 1

    if confirm:
        print(f"\n{'─' * 50}")
        print(f"✅ {published}/{len(files)} article(s) publié(s)")
        print(f"\nEtape suivante :")
        print(f"  pnpm build          # valider")
        print(f"  git add src/data/blog/ && git commit -m 'feat(blog): publish ...'")
        print(f"  git push            # → Cloudflare Pages déploie")


if __name__ == "__main__":
    main()
