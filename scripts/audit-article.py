#!/usr/bin/env python3
"""
audit-article.py — Analyseur statique des articles brandonvisca.com

Usage:
  python3 scripts/audit-article.py [article.md]   # Audite un article
  python3 scripts/audit-article.py --all           # Audite tous les articles
  python3 scripts/audit-article.py --hook          # Mode hook (stdin JSON)
"""

import sys
import json
import re
import os
from pathlib import Path
from datetime import datetime

BLOG_DIR = Path("/Users/brandon/Documents/2026-brandonvisca.com/src/data/blog")

# ── Tag convention (tag-convention.md) ────────────────────────────────────────

PRIMARY_TAGS = {
    "homelab", "auto-hebergement", "linux", "macos", "windows",
    "docker", "securite", "reseau", "productivite", "sysadmin",
    "developpement", "microsoft-365",
}
LEVEL_TAGS = {"debutant", "intermediaire", "avance"}
FORBIDDEN_TAGS = {"autres", "self-hosting", "productivity"}
PENDING_MERGE = {
    "office365": "microsoft-365",
    "tutoriel": "guide",
}

FAQ_PLACEHOLDERS = {"", "Question fréquente 1 ?", "Question fréquente 2 ?", "Réponse détaillée"}

TOC_HEADING_RE = re.compile(
    r"^##\s+(?:📑\s*)?(?:Table des matières|Sommaire|Table of contents)\s*$",
    re.MULTILINE | re.IGNORECASE,
)
ACCENTED_TAGS = {
    "productivité": "productivite",
    "vidéos": "multimedia",
    "récupération": "depannage",
    "luminosité": None,  # supprimer
    "ddc": None,
    "écrans-externes": None,
    "auto-hébergement": "auto-hebergement",
    "sécurité": "securite",
    "réseau": "reseau",
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def _heading_anchor(text: str) -> str:
    """Génère un ancre GitHub-style depuis un texte de titre."""
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[\s_]+", "-", text.strip())
    return re.sub(r"-+", "-", text).strip("-")


def get_all_slugs() -> set:
    return {f.stem for f in BLOG_DIR.glob("*.md")}


def has_accent(s: str) -> bool:
    return any(c in s for c in "àáâãäåèéêëìíîïòóôõöùúûüýÿçñ")


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Returns (frontmatter_raw_str, body_str). frontmatter is the raw block."""
    if not content.startswith("---"):
        return None, content
    end = content.find("\n---", 3)
    if end == -1:
        return None, content
    fm_raw = content[3:end].strip()
    body = content[end + 4:]
    return fm_raw, body


def extract_tags(fm_raw: str) -> list[str]:
    match = re.search(r"^tags:\s*\n((?:[ \t]+-[ \t]+\S[^\n]*\n?)+)", fm_raw, re.MULTILINE)
    if not match:
        return []
    return re.findall(r"^[ \t]+-[ \t]+(\S[^\n]*)", match.group(0), re.MULTILINE)


def extract_field(fm_raw: str, field: str) -> str | None:
    m = re.search(rf"^{re.escape(field)}:\s*(.+)", fm_raw, re.MULTILINE)
    return m.group(1).strip().strip('"\'') if m else None


# ── Audit functions ───────────────────────────────────────────────────────────

def audit_frontmatter(fm_raw: str, issues: list):
    if fm_raw is None:
        issues.append({"type": "error", "cat": "frontmatter", "msg": "Pas de bloc frontmatter YAML"})
        return

    for field in ("title", "description", "pubDatetime", "tags"):
        if not re.search(rf"^{field}:", fm_raw, re.MULTILINE):
            issues.append({"type": "error", "cat": "frontmatter", "msg": f"Champ requis manquant : `{field}`"})

    desc = extract_field(fm_raw, "description")
    if desc and not (120 <= len(desc) <= 155):
        issues.append({
            "type": "warning", "cat": "frontmatter",
            "msg": f"description : {len(desc)} chars (attendu 120-155) — \"{desc[:60]}...\""
        })

    if not re.search(r"^focusKeyword:", fm_raw, re.MULTILINE):
        issues.append({"type": "info", "cat": "seo", "msg": "focusKeyword absent — SEO non optimisé"})


def audit_focus_keyword(fm_raw: str, body: str, issues: list):
    """Vérifie la présence et la densité du mot-clé cible (équivalent RankMath)."""
    if fm_raw is None:
        return

    focus = extract_field(fm_raw, "focusKeyword")
    if not focus:
        return

    focus_lower = focus.lower()

    title = extract_field(fm_raw, "title") or ""
    if focus_lower not in title.lower():
        issues.append({
            "type": "warning", "cat": "seo",
            "msg": f"focusKeyword absent du titre — ajouter \"{focus}\" dans le title"
        })

    desc = extract_field(fm_raw, "description") or ""
    if focus_lower not in desc.lower():
        issues.append({
            "type": "warning", "cat": "seo",
            "msg": f"focusKeyword absent de la description — mentionner \"{focus}\" dans la meta"
        })

    h2_titles = re.findall(r"^##\s+(.+)$", body, re.MULTILINE)
    if h2_titles and not any(focus_lower in h.lower() for h in h2_titles):
        issues.append({
            "type": "info", "cat": "seo",
            "msg": f"focusKeyword absent des titres H2 — idéalement mentionner \"{focus}\" dans un sous-titre"
        })

    # Densité dans le corps (hors code blocks)
    body_no_code = re.sub(r"```[\s\S]*?```", "", body)
    words = re.findall(r"\b\w+\b", body_no_code.lower())
    if words:
        focus_words = focus_lower.split()
        # Compter les occurrences de la séquence complète
        body_text = body_no_code.lower()
        occurrences = body_text.count(focus_lower)
        density = (occurrences * len(focus_words) / len(words)) * 100
        if density < 0.5:
            issues.append({
                "type": "info", "cat": "seo",
                "msg": f"Densité focusKeyword trop faible : {density:.1f}% ({occurrences} fois) — cible 1-2%"
            })
        elif density > 3.0:
            issues.append({
                "type": "warning", "cat": "seo",
                "msg": f"Densité focusKeyword trop élevée : {density:.1f}% — risque de sur-optimisation (cible 1-2%)"
            })


def audit_faqs(fm_raw: str, issues: list):
    """Vérifie la présence et la qualité des FAQs (schema FAQPage JSON-LD)."""
    if fm_raw is None:
        return

    has_faqs = re.search(r"^faqs:", fm_raw, re.MULTILINE)
    if not has_faqs:
        issues.append({"type": "info", "cat": "faq",
                       "msg": "Pas de FAQs — ajouter pour le schema FAQPage JSON-LD (SEO)"})
        return

    questions = re.findall(r'^\s+(?:-\s+)?question:\s*["\']?(.*?)["\']?\s*$', fm_raw, re.MULTILINE)
    answers   = re.findall(r'^\s+(?:-\s+)?answer:\s*["\']?(.*?)["\']?\s*$',   fm_raw, re.MULTILINE)

    if not questions:
        issues.append({"type": "warning", "cat": "faq",
                       "msg": "Bloc faqs présent mais sans questions"})
        return

    empty_q = [q for q in questions if not q.strip() or q.strip() in FAQ_PLACEHOLDERS]
    if empty_q:
        issues.append({"type": "warning", "cat": "faq",
                       "msg": f"{len(empty_q)} FAQ(s) avec question vide ou placeholder — à remplir"})

    empty_a = [a for a in answers if not a.strip() or a.strip() in FAQ_PLACEHOLDERS]
    if empty_a:
        issues.append({"type": "warning", "cat": "faq",
                       "msg": f"{len(empty_a)} FAQ(s) avec réponse vide ou placeholder — à remplir"})

    short_a = [a for a in answers if a.strip() and a.strip() not in FAQ_PLACEHOLDERS and len(a.strip()) < 50]
    if short_a:
        issues.append({"type": "info", "cat": "faq",
                       "msg": f"{len(short_a)} réponse(s) FAQ < 50 chars — développer pour plus de valeur SEO"})

    count = len(questions)
    if count == 1:
        issues.append({"type": "info", "cat": "faq",
                       "msg": "1 seule FAQ — ajouter 2-3 questions supplémentaires pour le schema FAQPage"})
    elif count > 6:
        issues.append({"type": "info", "cat": "faq",
                       "msg": f"{count} FAQs — Google affiche généralement 3-4 max dans les résultats"})


def audit_toc(body: str, issues: list):
    """Vérifie la table des matières si présente."""
    toc_match = TOC_HEADING_RE.search(body)
    if not toc_match:
        return

    toc_start = toc_match.end()
    next_h = re.search(r"^##\s+", body[toc_start:], re.MULTILINE)
    toc_body = body[toc_start: toc_start + next_h.start()] if next_h else body[toc_start:]

    # Wiki-links dans la TOC
    wiki_in_toc = re.findall(r"\[\[[^\]]+\]\]", toc_body)
    if wiki_in_toc:
        issues.append({"type": "error", "cat": "toc",
                       "msg": f"Table des matières : {len(wiki_in_toc)} wiki-link(s) non convertis"})
        return

    toc_anchors = re.findall(r"\(#[\w%.-]+\)", toc_body)
    if not toc_anchors:
        issues.append({"type": "warning", "cat": "toc",
                       "msg": "Table des matières sans ancres `(#anchor)` — vérifier le format des liens"})


def audit_tags(fm_raw: str, issues: list):
    if fm_raw is None:
        return
    tags = extract_tags(fm_raw)
    if not tags:
        return

    if len(tags) > 6:
        issues.append({"type": "error", "cat": "tags", "msg": f"Trop de tags : {len(tags)} (max 6) — {tags}"})

    for tag in tags:
        if tag in FORBIDDEN_TAGS:
            issues.append({"type": "error", "cat": "tags", "msg": f"Tag interdit : `{tag}` — remplacer par le vrai tag thématique"})
        elif tag in ACCENTED_TAGS:
            replacement = ACCENTED_TAGS[tag]
            fix = f"→ `{replacement}`" if replacement else "→ supprimer"
            issues.append({"type": "error", "cat": "tags", "msg": f"Tag avec accent/invalide : `{tag}` {fix}"})
        elif has_accent(tag):
            issues.append({"type": "error", "cat": "tags", "msg": f"Tag avec accent : `{tag}` — convertir en kebab-case sans accent"})
        elif tag in PENDING_MERGE:
            issues.append({"type": "info", "cat": "tags", "msg": f"Tag à fusionner : `{tag}` → `{PENDING_MERGE[tag]}`"})

    if not any(t in PRIMARY_TAGS for t in tags):
        issues.append({"type": "warning", "cat": "tags", "msg": f"Aucun tag primaire — choisir parmi : {', '.join(sorted(PRIMARY_TAGS))}"})

    if not any(t in LEVEL_TAGS for t in tags):
        issues.append({"type": "warning", "cat": "tags", "msg": "Pas de tag de niveau : ajouter `debutant`, `intermediaire` ou `avance`"})


def audit_tables(body: str, issues: list):
    body_lines = body.split("\n")
    # Single-line table artifact from WordPress export
    for i, line in enumerate(body_lines, 1):
        pipe_count = line.count("|")
        if pipe_count >= 4 and len(line) > 180 and not line.strip().startswith("```"):
            issues.append({
                "type": "error", "cat": "tables",
                "msg": f"Ligne {i} : table potentiellement sur une seule ligne ({len(line)} chars, {pipe_count} pipes)"
            })

    # Detect table blocks and validate header separator
    in_table = False
    table_start = 0
    table_lines_buf = []
    for i, line in enumerate(body_lines, 1):
        stripped = line.strip()
        is_table_row = stripped.startswith("|") and stripped.endswith("|")
        if is_table_row:
            if not in_table:
                in_table = True
                table_start = i
                table_lines_buf = []
            table_lines_buf.append(stripped)
        else:
            if in_table and len(table_lines_buf) >= 2:
                # Check second row is separator
                sep_row = table_lines_buf[1] if len(table_lines_buf) > 1 else ""
                if not re.match(r"^\|[-| :]+\|$", sep_row):
                    issues.append({
                        "type": "error", "cat": "tables",
                        "msg": f"Ligne {table_start} : table sans ligne séparateur valide (ex: `|---|---|`)"
                    })
            in_table = False
            table_lines_buf = []


def audit_code_blocks(body: str, issues: list):
    # Count triple-backtick fences (not inside inline code)
    fences = re.findall(r"^```", body, re.MULTILINE)
    if len(fences) % 2 != 0:
        issues.append({
            "type": "error", "cat": "code",
            "msg": f"Nombre impair de \\`\\`\\` ({len(fences)}) — bloc de code non fermé"
        })

    # Code blocks without language identifier
    no_lang = re.findall(r"^```[ \t]*$", body, re.MULTILINE)
    if no_lang:
        issues.append({
            "type": "info", "cat": "code",
            "msg": f"{len(no_lang)} bloc(s) de code sans identifiant de langage — ajouter bash/yaml/json/etc."
        })


def audit_hr_separators(body: str, issues: list):
    hrs = re.findall(r"^---\s*$", body, re.MULTILINE)
    if len(hrs) >= 3:
        issues.append({
            "type": "warning", "cat": "formatting",
            "msg": f"{len(hrs)} séparateurs `---` dans le corps — vérifier si intentionnel ou double-frontmatter accidentel"
        })
    elif len(hrs) == 2:
        # Two consecutive --- is almost always an accident
        if re.search(r"^---\s*\n---\s*$", body, re.MULTILINE):
            issues.append({
                "type": "error", "cat": "formatting",
                "msg": "Double `---` consécutifs détectés — probablement un artefact de conversion"
            })


def audit_images(body: str, issues: list):
    # WordPress upload paths
    wp_imgs = re.findall(r"!\[[^\]]*\]\([^\)]*(?:uploads|wp-content)[^\)]*\)", body)
    if wp_imgs:
        issues.append({
            "type": "error", "cat": "images",
            "msg": f"{len(wp_imgs)} image(s) WordPress non migrée(s) : {wp_imgs[:2]}"
        })

    # Relative upload refs
    rel_imgs = re.findall(r"!\[[^\]]*\]\(\.\./uploads/[^\)]*\)", body)
    if rel_imgs:
        issues.append({
            "type": "error", "cat": "images",
            "msg": f"{len(rel_imgs)} référence(s) image relative(s) cassée(s) : {rel_imgs[:2]}"
        })

    # Local images that should be in public/
    local_imgs = re.findall(r"!\[[^\]]*\]\((?!https?://)(?!\./public/)([^\)]+)\)", body)
    for img in local_imgs:
        if not img.startswith("/") and not img.startswith("http"):
            public_path = Path("/Users/brandon/Documents/2026-brandonvisca.com/public") / img.lstrip("./")
            if not public_path.exists():
                issues.append({
                    "type": "warning", "cat": "images",
                    "msg": f"Image locale introuvable dans public/ : `{img}`"
                })


def audit_links(body: str, issues: list):
    all_slugs = get_all_slugs()

    # Obsidian wiki-links
    wiki = re.findall(r"\[\[[^\]]+\]\]", body)
    if wiki:
        issues.append({
            "type": "error", "cat": "links",
            "msg": f"{len(wiki)} wiki-link(s) Obsidian non convertis : {wiki[:3]}"
        })

    # Internal links — check slug exists
    KNOWN_PAGES = {"blog", "tags", "archives", "search", "about", "galleries"}
    internal = re.findall(r"\[[^\]]*\]\(/([\w-]+)/?(?:#[^\)]*)?\)", body)
    for slug in internal:
        if slug not in all_slugs and slug not in KNOWN_PAGES:
            issues.append({
                "type": "warning", "cat": "links",
                "msg": f"Lien interne potentiellement cassé : `/{slug}/`"
            })

    # Plain-text Obsidian article references (bold text that looks like article titles)
    # These are typically "Articles connexes" sections with **Titre** instead of links
    connexes_section = re.search(r"## Articles connexes\n([\s\S]+?)(?=\n##|\Z)", body)
    if connexes_section:
        section_body = connexes_section.group(1)
        bold_items = re.findall(r"\*\*([^*]+)\*\*(?!\()", section_body)
        real_links = re.findall(r"\[([^\]]+)\]\(", section_body)
        if bold_items and len(bold_items) > len(real_links):
            issues.append({
                "type": "warning", "cat": "links",
                "msg": f"Section 'Articles connexes' : {len(bold_items)} item(s) en gras sans lien — convertir en `[titre](/slug/)`"
            })


# ── Main audit ────────────────────────────────────────────────────────────────

def audit_file(filepath: Path) -> dict:
    """Audit a single markdown file. Returns structured result."""
    issues = []

    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return {"file": filepath.name, "issues": [{"type": "error", "cat": "io", "msg": str(e)}]}

    fm_raw, body = parse_frontmatter(content)

    if fm_raw is None:
        issues.append({"type": "error", "cat": "frontmatter", "msg": "Frontmatter manquant ou non fermé"})
        # Still analyze body
    else:
        audit_frontmatter(fm_raw, issues)
        audit_tags(fm_raw, issues)
        audit_focus_keyword(fm_raw, body, issues)
        audit_faqs(fm_raw, issues)

    audit_toc(body, issues)
    audit_tables(body, issues)
    audit_code_blocks(body, issues)
    audit_hr_separators(body, issues)
    audit_images(body, issues)
    audit_links(body, issues)

    return {"file": filepath.name, "issues": issues}


# ── Report formatting ─────────────────────────────────────────────────────────

ICONS = {"error": "❌", "warning": "⚠️ ", "info": "ℹ️ "}


def format_report(results: list, verbose: bool = True) -> str:
    lines = []
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    total_files = len(results)
    files_with_issues = [r for r in results if r["issues"]]
    total_errors = sum(len([i for i in r["issues"] if i["type"] == "error"]) for r in results)
    total_warnings = sum(len([i for i in r["issues"] if i["type"] == "warning"]) for r in results)
    total_infos = sum(len([i for i in r["issues"] if i["type"] == "info"]) for r in results)

    lines.append(f"# Rapport d'audit — brandonvisca.com — {date_str}")
    lines.append(f"\n**{total_files} articles** analysés · {len(files_with_issues)} avec des issues · "
                 f"{total_errors} erreurs · {total_warnings} avertissements · {total_infos} infos\n")

    if not files_with_issues:
        lines.append("✅ Aucun problème détecté.")
        return "\n".join(lines)

    # Group all issues by category for summary
    by_cat: dict[str, list] = {}
    for r in results:
        for issue in r["issues"]:
            cat = issue["cat"]
            by_cat.setdefault(cat, []).append((r["file"], issue))

    if verbose:
        # Per-file detail
        lines.append("## Détail par article\n")
        for r in sorted(files_with_issues, key=lambda x: (-len(x["issues"]), x["file"])):
            errors = [i for i in r["issues"] if i["type"] == "error"]
            warnings = [i for i in r["issues"] if i["type"] == "warning"]
            infos = [i for i in r["issues"] if i["type"] == "info"]
            summary = f"({len(errors)}❌ {len(warnings)}⚠️  {len(infos)}ℹ️ )"
            lines.append(f"### `{r['file']}` {summary}\n")
            for issue in r["issues"]:
                icon = ICONS.get(issue["type"], "•")
                lines.append(f"- {icon} **[{issue['cat']}]** {issue['msg']}")
            lines.append("")
    else:
        # Summary by category
        lines.append("## Résumé par catégorie\n")
        for cat, items in sorted(by_cat.items()):
            errors = [i for f, i in items if i["type"] == "error"]
            lines.append(f"- **{cat}** : {len(items)} issue(s) ({len(errors)} erreurs)")

    return "\n".join(lines)


# ── Hook mode ─────────────────────────────────────────────────────────────────

def hook_mode():
    """PostToolUse hook: reads JSON from stdin, audits if file is a blog article."""
    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
    except Exception:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # React to Write and Edit tool calls only
    if tool_name not in ("Write", "Edit"):
        sys.exit(0)

    file_path_str = tool_input.get("file_path", "")
    if "/src/data/blog/" not in file_path_str or not file_path_str.endswith(".md"):
        sys.exit(0)

    filepath = Path(file_path_str)
    if not filepath.exists():
        sys.exit(0)

    result = audit_file(filepath)
    issues = result["issues"]

    if not issues:
        sys.exit(0)

    errors = [i for i in issues if i["type"] == "error"]
    warnings = [i for i in issues if i["type"] == "warning"]

    output = [f"\n⚡ Audit automatique — `{filepath.name}`"]
    shown = 0
    for i in errors[:4]:
        output.append(f"  {ICONS['error']} [{i['cat']}] {i['msg']}")
        shown += 1
    for i in warnings[:2]:
        output.append(f"  {ICONS['warning']} [{i['cat']}] {i['msg']}")
        shown += 1

    remaining = len(issues) - shown
    if remaining > 0:
        output.append(f"  … et {remaining} autre(s). Lancer `/article-audit {filepath.name}` pour le rapport complet.")

    print("\n".join(output))


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]

    if "--hook" in args:
        hook_mode()
    elif "--all" in args:
        results = [audit_file(f) for f in sorted(BLOG_DIR.glob("*.md"))]
        verbose = "--summary" not in args
        print(format_report(results, verbose=verbose))
    elif args:
        target = args[0]
        filepath = Path(target)
        if not filepath.is_absolute():
            filepath = BLOG_DIR / target
        if not filepath.exists():
            print(f"Fichier introuvable : {filepath}", file=sys.stderr)
            sys.exit(1)
        result = audit_file(filepath)
        print(format_report([result]))
    else:
        print(__doc__)
        sys.exit(1)
