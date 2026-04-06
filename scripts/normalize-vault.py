#!/usr/bin/env python3
"""
normalize-vault.py — Normalise le frontmatter des articles du vault Obsidian.

Transforme WP export + format Obsidian → format hybride uniforme :
  - excerpt → description
  - date → pubDatetime
  - rank_math_focus_keyword / mot_cle_principal → focusKeyword
  - status → draft (bool)
  - Supprime les champs WP/analytics
  - Conserve les champs éditoriaux Obsidian

Usage:
  python3 scripts/normalize-vault.py --dry-run   # Affiche les diffs sans écrire
  python3 scripts/normalize-vault.py              # Applique les changements
  python3 scripts/normalize-vault.py path/to/article.md  # Un seul fichier
"""

import sys
import re
import yaml
from pathlib import Path
from datetime import datetime, timezone

# ── Répertoires cibles ────────────────────────────────────────────────────────

VAULT_ROOT = Path.home() / "Documents/brandon-knowledge"
TARGETS = [
    VAULT_ROOT / "Content/Articles/04-Publies",
    VAULT_ROOT / "Content/Articles/03-Pret-Publication",
]

# ── Champs à supprimer ────────────────────────────────────────────────────────

WP_FIELDS = {
    # WordPress core
    "status", "permalink", "type", "id", "postId", "postType", "profileName",
    "thumbnail", "category", "categories", "categories_wp", "post_format",
    "tag",  # WP tag (distinct de tags array)
    # Analytics
    "date_publie", "views_30j",
    # Doublon/obsolète
    "featured_image", "url_wordpress", "date_publication_prevue",
    "excerpt",  # → description
    "mot_cle_principal",  # → focusKeyword
    # Rank Math
    "rank_math_seo_score", "rank_math_internal_links_processed",
    "rank_math_primary_category", "rank_math_focus_keyword",
    "rank_math_analytic_object_id", "rank_math_title",
}

# ── Champs éditoriaux Obsidian à conserver ────────────────────────────────────

KEEP_EDITORIAL = {
    "cluster", "sous_cluster", "intention", "difficulte", "temps_lecture",
    "priorite", "series", "articles_lies", "mots_cles_secondaires",
}

# ── Normalisation des tags ─────────────────────────────────────────────────────

FORBIDDEN_TAGS = {"autres", "self-hosting", "productivity", "other"}

ACCENTED_TAGS = {
    "productivité": "productivite",
    "vidéos": "multimedia",
    "récupération": "depannage",
    "luminosité": None,   # supprimer
    "ddc": None,
    "écrans-externes": None,
    "auto-hébergement": "auto-hebergement",
    "sécurité": "securite",
    "réseau": "reseau",
    "macos": "macos",    # déjà correct
}

TAG_CASE_MAP = {
    "MacOS": "macos",
    "macOS": "macos",
    "Linux": "linux",
    "Docker": "docker",
    "Windows": "windows",
    "Launcher": "launcher",
    "Productivité": "productivite",
    "Productivite": "productivite",
}

PENDING_MERGE = {
    "office365": "microsoft-365",
    "tutoriel": "guide",
}


def normalize_tag(tag: str) -> str | None:
    """Normalise un tag : lowercase, sans accent, mappings."""
    tag = str(tag).strip()

    # Mappings case
    if tag in TAG_CASE_MAP:
        return TAG_CASE_MAP[tag]

    tag_lower = tag.lower()

    if tag_lower in FORBIDDEN_TAGS:
        return None

    if tag_lower in ACCENTED_TAGS:
        return ACCENTED_TAGS[tag_lower]

    if tag_lower in PENDING_MERGE:
        return PENDING_MERGE[tag_lower]

    # Remplacer accents courants
    replacements = [
        ("é", "e"), ("è", "e"), ("ê", "e"), ("ë", "e"),
        ("à", "a"), ("â", "a"), ("ä", "a"),
        ("î", "i"), ("ï", "i"),
        ("ô", "o"), ("ö", "o"),
        ("ù", "u"), ("û", "u"), ("ü", "u"),
        ("ç", "c"), ("ñ", "n"),
        ("É", "e"), ("È", "e"), ("À", "a"),
    ]
    result = tag_lower
    for accent, replacement in replacements:
        result = result.replace(accent, replacement)

    return result


def normalize_tags(raw_tags) -> list[str]:
    """Normalise une liste de tags, déduplique, trie."""
    if not raw_tags:
        return []

    if isinstance(raw_tags, str):
        raw_tags = [t.strip() for t in raw_tags.split(",")]

    normalized = []
    seen = set()
    for tag in raw_tags:
        n = normalize_tag(str(tag))
        if n and n not in seen:
            normalized.append(n)
            seen.add(n)

    return normalized


# ── Extraction du mot-clé focus ───────────────────────────────────────────────

def extract_focus_keyword(fm: dict) -> str:
    """Extrait le mot-clé principal depuis rank_math ou mot_cle_principal."""

    # RankMath : liste de listes ou liste de strings
    rm = fm.get("rank_math_focus_keyword")
    if rm:
        if isinstance(rm, list) and rm:
            raw = str(rm[0])
        else:
            raw = str(rm)
        # Souvent "keyword1,keyword2,keyword3" → prendre le premier
        first = raw.split(",")[0].strip()
        if first:
            return first

    # Format Obsidian
    mkp = fm.get("mot_cle_principal", "")
    if mkp:
        return str(mkp).strip()

    return ""


# ── Normalisation du statut → draft ──────────────────────────────────────────

def extract_draft(fm: dict) -> bool:
    status = str(fm.get("status", "")).lower()
    if status in ("publish", "publié", "publie", "published"):
        return False
    return True  # draft, future, brouillon, etc.


# ── Normalisation de la date → pubDatetime ───────────────────────────────────

def normalize_pubdatetime(date_val) -> str:
    """Convertit une valeur date en string ISO 8601."""
    if date_val is None:
        return ""

    # Déjà un string
    if isinstance(date_val, str):
        d = date_val.strip().strip("'\"")
        # Date seule YYYY-MM-DD
        if re.match(r"^\d{4}-\d{2}-\d{2}$", d):
            return f"{d}T00:00:00+01:00"
        return d

    # datetime object (PyYAML parse les dates ISO 8601)
    if isinstance(date_val, datetime):
        if date_val.tzinfo is None:
            # Assume Europe/Paris
            return date_val.strftime("%Y-%m-%dT%H:%M:%S+01:00")
        return date_val.isoformat()

    # date object
    try:
        from datetime import date as date_type
        if isinstance(date_val, date_type):
            return f"{date_val.isoformat()}T00:00:00+01:00"
    except Exception:
        pass

    return str(date_val)


# ── Parsing du frontmatter ────────────────────────────────────────────────────

def parse_frontmatter(content: str) -> tuple[dict | None, str, str]:
    """
    Returns (frontmatter_dict, raw_frontmatter_str, body_str).
    """
    if not content.startswith("---"):
        return None, "", content

    end = content.find("\n---", 3)
    if end == -1:
        return None, "", content

    fm_raw = content[4:end]  # strip "---\n"
    body = content[end + 4:]  # skip "\n---"

    try:
        fm = yaml.safe_load(fm_raw) or {}
    except yaml.YAMLError as e:
        print(f"  ⚠️  Erreur YAML : {e}", file=sys.stderr)
        fm = {}

    return fm, fm_raw, body


# ── Construction du nouveau frontmatter ──────────────────────────────────────

def build_normalized_frontmatter(fm: dict, source_path: Path) -> dict:
    """Construit le frontmatter normalisé."""
    result = {}

    # ── Champs Astro Blog ──────────────────────────────────────
    result["title"] = fm.get("title", "")

    # description : depuis excerpt ou champ existant
    description = fm.get("description", "") or fm.get("excerpt", "")
    if description:
        description = str(description).strip()
        # Nettoyer les trailing "..." ou "...."
        description = re.sub(r'\.{2,}$', '', description).strip()
    result["description"] = description

    # pubDatetime : depuis date
    date_val = fm.get("date") or fm.get("pubDatetime")
    result["pubDatetime"] = normalize_pubdatetime(date_val)

    # author
    author = str(fm.get("author", "Brandon Visca")).strip()
    if author.lower() in ("brandon", "brandon visca", ""):
        author = "Brandon Visca"
    result["author"] = author

    # tags
    raw_tags = fm.get("tags", fm.get("tag", []))
    result["tags"] = normalize_tags(raw_tags)
    if not result["tags"]:
        result["tags"] = ["homelab"]  # fallback par défaut

    # featured
    result["featured"] = bool(fm.get("featured", False))

    # draft
    result["draft"] = extract_draft(fm)

    # focusKeyword (optionnel)
    focus = extract_focus_keyword(fm)
    if focus:
        result["focusKeyword"] = focus

    # faqs (si présent dans l'article src/data/blog/)
    if fm.get("faqs"):
        result["faqs"] = fm["faqs"]

    # ── Champs éditoriaux Obsidian (conservés) ─────────────────
    editorial = {}
    for field in KEEP_EDITORIAL:
        val = fm.get(field)
        if val is not None and val != "" and val != [] and val != {}:
            editorial[field] = val

    result["_editorial"] = editorial  # on les sépare pour l'ordre

    return result


def quote_yaml_string(value: str) -> str:
    """Met entre guillemets doubles si la valeur YAML l'exige."""
    SPECIAL = [':', '#', '[', ']', '{', '}', ',', '&', '*', '!', '|', '>', '%', '@']
    needs_quote = any(c in value for c in SPECIAL) or value.startswith(("'", '"'))
    if needs_quote:
        escaped = value.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{escaped}"'
    return value


def serialize_frontmatter(normalized: dict) -> str:
    """Sérialise en YAML avec ordre maîtrisé."""
    lines = ["---"]

    editorial = normalized.pop("_editorial", {})

    # Ordre des champs Astro
    blog_order = [
        "title", "description", "pubDatetime", "author",
        "tags", "featured", "draft", "focusKeyword", "faqs",
    ]

    # Champs Astro
    for key in blog_order:
        if key not in normalized:
            continue
        value = normalized[key]
        if value is None or value == "":
            continue
        if isinstance(value, list) and not value and key != "tags":
            continue

        if key == "faqs" and isinstance(value, list):
            lines.append("faqs:")
            for faq in value:
                q = faq.get("question", "").replace('"', '\\"')
                a = faq.get("answer", "").replace('"', '\\"')
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
            lines.append(f"{key}: {quote_yaml_string(value)}")
        else:
            lines.append(f"{key}: {value}")

    # Séparateur éditorial — ordre fixe
    EDITORIAL_ORDER = [
        "cluster", "sous_cluster", "intention", "difficulte",
        "temps_lecture", "priorite", "series",
        "articles_lies", "mots_cles_secondaires",
    ]

    if editorial:
        lines.append("")
        lines.append("# Obsidian — workflow éditorial")
        for key in EDITORIAL_ORDER:
            if key not in editorial:
                continue
            value = editorial[key]
            if isinstance(value, list):
                if value:
                    lines.append(f"{key}:")
                    for item in value:
                        # Pas de yaml.dump sur les strings — écriture directe
                        if isinstance(item, str):
                            lines.append(f"  - {quote_yaml_string(item)}")
                        else:
                            lines.append(f"  - {item}")
                else:
                    lines.append(f"{key}: []")
            elif isinstance(value, str):
                lines.append(f"{key}: {quote_yaml_string(value)}")
            elif isinstance(value, bool):
                lines.append(f"{key}: {'true' if value else 'false'}")
            else:
                lines.append(f"{key}: {value}")

    lines.append("---")
    return "\n".join(lines)


# ── Normalisation d'un fichier ────────────────────────────────────────────────

def normalize_file(filepath: Path, dry_run: bool = True) -> bool:
    """
    Normalise un fichier. Retourne True si modifié.
    """
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  ❌ Lecture impossible : {e}")
        return False

    fm, fm_raw, body = parse_frontmatter(content)
    if fm is None:
        print(f"  ⚠️  Pas de frontmatter valide — ignoré")
        return False

    normalized = build_normalized_frontmatter(fm, filepath)
    new_fm = serialize_frontmatter(normalized)
    new_content = new_fm + "\n" + body.lstrip("\n")

    if new_content.strip() == content.strip():
        return False  # Pas de changement

    if dry_run:
        # Afficher le diff du frontmatter uniquement
        old_lines = content.split("\n")
        new_lines = new_content.split("\n")

        # Trouver la fin du frontmatter pour limiter le diff
        old_fm_end = next((i for i, l in enumerate(old_lines[1:], 1) if l.strip() == "---"), 20) + 1
        new_fm_end = next((i for i, l in enumerate(new_lines[1:], 1) if l.strip() == "---"), 20) + 1

        old_fm_display = "\n".join(old_lines[:old_fm_end])
        new_fm_display = "\n".join(new_lines[:new_fm_end])

        print(f"\n  --- AVANT ---")
        print(old_fm_display)
        print(f"\n  --- APRÈS ---")
        print(new_fm_display)
    else:
        filepath.write_text(new_content, encoding="utf-8")
        print(f"  ✅ Normalisé")

    return True


# ── Point d'entrée ────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    args = [a for a in args if not a.startswith("--")]

    if dry_run:
        print("🔍 MODE DRY-RUN — aucune écriture\n")
    else:
        print("✍️  MODE ÉCRITURE — application des changements\n")

    if args:
        # Fichier unique
        files = [Path(args[0])]
        if not files[0].is_absolute():
            # Essayer dans les dossiers cibles
            for target in TARGETS:
                candidate = target / args[0]
                if candidate.exists():
                    files = [candidate]
                    break
    else:
        # Tous les fichiers des dossiers cibles
        files = []
        for target in TARGETS:
            if target.exists():
                files.extend(sorted(target.glob("*.md")))

    total = len(files)
    modified = 0

    for filepath in files:
        print(f"\n📄 {filepath.name}")
        changed = normalize_file(filepath, dry_run=dry_run)
        if changed:
            modified += 1

    print(f"\n{'─' * 50}")
    print(f"Total : {total} fichiers — {modified} {'à modifier' if dry_run else 'modifiés'}")

    if dry_run and modified > 0:
        print(f"\nPour appliquer : python3 scripts/normalize-vault.py")


if __name__ == "__main__":
    main()
