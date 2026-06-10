#!/usr/bin/env python3
"""
strip_emdash.py — Supprime les tirets cadratin (—, U+2014) et demi-cadratin
(–, U+2013) utilisés comme ponctuation. Marqueur IA majeur sur brandonvisca.com.

Règles :
  - Ligne de titre (#…)  : « — » / « – »  ->  « : »
  - Corps du texte       : « — » (incise) ->  « , »
                           « – » (incise espacée) -> « , »
  - Demi-cadratin entre chiffres (plages 2020–2025) : PRÉSERVÉ
  - Blocs de code clôturés (``` / ~~~) : PRÉSERVÉS tels quels

Usage :
  python3 scripts/strip_emdash.py fichier.md            # dry-run (diff + compte)
  python3 scripts/strip_emdash.py 'dossier/*.md' --apply
  python3 scripts/strip_emdash.py dossier/ --apply      # récursif sur *.md

Importable : from strip_emdash import normalize_text
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

EM = "—"  # —
EN = "–"  # –

_HEADING = re.compile(r"\s{0,3}#{1,6}\s")
_FENCE = re.compile(r"\s*(```|~~~)")


def _normalize_line(line: str, is_heading: bool) -> str:
    if is_heading:
        # titre sans deux-points : tiret séparateur -> deux-points
        # titre avec deux-points déjà présent : -> virgule (évite le double « : »)
        repl = ", " if ":" in line else " : "
        return re.sub(r"\s*[—–]\s*", repl, line)
    # corps : cadratin (incise) -> virgule
    line = re.sub(r"\s*—\s*", ", ", line)
    # demi-cadratin espacé (incise) -> virgule, mais on garde les plages 2020–2025
    line = re.sub(r"(?<!\d)\s*–\s*(?!\d)", ", ", line)
    return line


def normalize_text(text: str) -> str:
    """Remplace les tirets cadratin/demi-cadratin de ponctuation. Idempotent."""
    out: list[str] = []
    in_fence = False
    for line in text.split("\n"):
        if _FENCE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        is_heading = bool(_HEADING.match(line))
        out.append(_normalize_line(line, is_heading))
    return "\n".join(out)


def _iter_targets(arg: str):
    p = Path(arg)
    if p.is_dir():
        yield from sorted(p.rglob("*.md"))
    elif any(c in arg for c in "*?["):
        from glob import glob
        for g in sorted(glob(arg, recursive=True)):
            yield Path(g)
    elif p.exists():
        yield p


def main(argv: list[str]) -> int:
    apply = "--apply" in argv
    args = [a for a in argv if not a.startswith("-")]
    if not args:
        print(__doc__)
        return 1

    total_files = 0
    total_hits = 0
    changed_files = 0

    for arg in args:
        for path in _iter_targets(arg):
            total_files += 1
            original = path.read_text(encoding="utf-8")
            hits = original.count(EM) + original.count(EN)
            if hits == 0:
                continue
            normalized = normalize_text(original)
            if normalized == original:
                continue
            remaining = normalized.count(EM) + normalized.count(EN)
            removed = hits - remaining
            total_hits += removed
            changed_files += 1
            extra = f" (reste {remaining} en plage chiffrée)" if remaining else ""
            if apply:
                try:
                    path.write_text(normalized, encoding="utf-8")
                except PermissionError:
                    print(f"  ⛔ IGNORÉ (permission)  {path}  : {removed} tiret(s) non retiré(s)")
                    changed_files -= 1
                    total_hits -= removed
                    continue
            tag = "✏️  APPLIQUÉ" if apply else "🔍 dry-run"
            print(f"  {tag}  {path}  : {removed} tiret(s) retiré(s){extra}")

    mode = "appliqué" if apply else "dry-run (relancer avec --apply)"
    print(f"\n→ {changed_files} fichier(s) modifié(s), {total_hits} tiret(s) retiré(s) — {mode}")
    print(f"  ({total_files} fichier(s) scanné(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
