#!/usr/bin/env python3
"""
normalize_tldr.py — Normalise le bloc TL;DR au format canonique :

    > 💡 **TL;DR**
    > - point
    > - point
    > - point

N'agit QUE si des puces existent deja dans le bloc (>=2). Les TL;DR en prose
(sans puces) sont laisses tels quels et signales (= reecriture editoriale).
Preserve le texte des puces. Idempotent.

Usage :
  python3 scripts/normalize_tldr.py fichier.md             # dry-run (apercu)
  python3 scripts/normalize_tldr.py dossier/ --apply
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_TLDR = re.compile(r"TL\W?DR", re.IGNORECASE)
_CANON = re.compile(r"^>\s*💡\s*\*\*TL;DR\*\*\s*$")
_BULLET = re.compile(r"^\s*>?\s*[-*]\s+(\S.*)$")
_SETEXT = re.compile(r"^\s*[-=]{3,}\s*$")
_FM = re.compile(r"^---\n.*?\n---\n", re.S)
_HASWORD = re.compile(r"[A-Za-zÀ-ÿ0-9]")


def _bullet_text(line: str) -> str | None:
    m = _BULLET.match(line)
    if not m:
        return None
    txt = m.group(1).strip()
    # ignorer les pseudo-puces (HR « - - - - », tirets seuls)
    return txt if _HASWORD.search(txt) else None


def normalize_tldr(text: str) -> tuple[str, str]:
    """Retourne (nouveau_texte, statut). statut: ok|deja|prose|absent."""
    fm = _FM.match(text)
    head = text[: fm.end()] if fm else ""
    body = text[fm.end():] if fm else text
    lines = body.split("\n")

    idx = next((i for i, l in enumerate(lines) if _TLDR.search(l)), None)
    if idx is None:
        return text, "absent"

    # Collecte des puces : sauter underline setext / lignes vides apres le header
    j = idx + 1
    n = len(lines)
    while j < n and (lines[j].strip() == "" or _SETEXT.match(lines[j])):
        j += 1
    bullets: list[str] = []
    last = idx
    while j < n:
        t = _bullet_text(lines[j])
        if t is not None:
            bullets.append(t)
            last = j
            j += 1
        elif lines[j].strip() == "":
            j += 1
        else:
            break

    if len(bullets) < 2:
        return text, "prose"

    # Deja canonique ?
    already = bool(_CANON.match(lines[idx])) and all(
        re.match(r"^>\s*-\s", lines[k]) for k in range(idx + 1, last + 1)
        if lines[k].strip()
    )
    if already:
        return text, "deja"

    new_block = ["> 💡 **TL;DR**"] + [f"> - {b}" for b in bullets]
    new_lines = lines[:idx] + new_block + lines[last + 1:]
    return head + "\n".join(new_lines), "ok"


def _targets(arg: str):
    p = Path(arg)
    if p.is_dir():
        yield from sorted(p.rglob("*.md"))
    elif p.exists():
        yield p


def main(argv: list[str]) -> int:
    apply = "--apply" in argv
    args = [a for a in argv if not a.startswith("-")]
    if not args:
        print(__doc__)
        return 1
    n_ok = n_prose = n_deja = n_absent = 0
    for arg in args:
        for path in _targets(arg):
            original = path.read_text(encoding="utf-8")
            new, status = normalize_tldr(original)
            if status == "ok":
                n_ok += 1
                tag = "✏️  APPLIQUÉ" if apply else "🔍 dry-run"
                print(f"  {tag}  {path.name}")
                if not apply:
                    # apercu du nouveau bloc
                    blk = [l for l in new.split("\n") if l.startswith("> ")][:5]
                    for l in blk:
                        print(f"        {l}")
                else:
                    try:
                        path.write_text(new, encoding="utf-8")
                    except PermissionError:
                        n_ok -= 1
                        print(f"  ⛔ IGNORÉ (permission)  {path.name}")
            elif status == "prose":
                n_prose += 1
                print(f"  ⏭️  PROSE (réécriture)  {path.name}")
            elif status == "deja":
                n_deja += 1
            else:
                n_absent += 1
    mode = "appliqué" if apply else "dry-run (relancer avec --apply)"
    print(f"\n→ {n_ok} normalisé(s), {n_deja} déjà conforme(s), "
          f"{n_prose} en prose (à réécrire), {n_absent} sans TL;DR — {mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
