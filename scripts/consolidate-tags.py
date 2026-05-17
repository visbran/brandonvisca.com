#!/usr/bin/env python3
"""
Consolide 119 tags → ~35 tags.
Mapping: tag_ancien → tag_cible (None = supprimer).
"""

import os, re, sys

BLOG_DIR = "src/data/blog"

# Tags à conserver tels quels (primaires + méta + secondaires)
KEEP = {
    # Primaires
    "homelab", "auto-hebergement", "linux", "macos", "windows",
    "docker", "securite", "reseau", "productivite", "sysadmin",
    "developpement", "microsoft-365",
    # Méta (masqués dans /tags/)
    "guide", "debutant", "intermediaire", "avance",
    # Secondaires
    "snipeit", "nginx", "active-directory", "powershell", "windows-server",
    "dns", "homebrew", "terminal", "monitoring", "raycast", "ssh",
    "hardening", "ldap", "hyper-v", "backup", "nextcloud", "vim",
    "multimedia", "wordpress",
}

TAG_MAP = {
    # → linux
    "ubuntu": "linux",
    "ntp": "linux",
    "fuseau-horaire": "linux",
    "timedatectl": "linux",
    "hyprland": "linux",
    "arch-linux": "linux",
    "android": "linux",
    "file-transfer": "linux",
    "openmtp": "linux",
    "swap": "linux",
    "memoire": "linux",
    "performance": "linux",
    "swappiness": "linux",
    # → macos
    "magnet": "macos",
    "barre-menu": "macos",
    "raccourcis": "macos",
    "appcleaner": "macos",
    "music-decoy": "macos",
    "navigateur": "macos",
    "webp": "macos",
    "automator": "macos",
    "gestion-fenetres": "macos",
    "launcher": "macos",
    # → windows
    "winpe": "windows",
    "uefi": "windows",
    # → homelab
    "proxmox": "homelab",
    "lxc": "homelab",
    "raid": "homelab",
    "virtualisation": "homelab",
    # → docker
    "traefik": "docker",
    "reverse-proxy": "docker",
    "docker-compose": "docker",
    "watchtower": "docker",
    # → securite
    "vie-privee": "securite",
    "https": "securite",
    "password": "securite",
    "csp": "securite",
    "firewall": "securite",
    "protection": "securite",
    # → hardening
    "headers": "hardening",
    # → reseau
    "pfsense": "reseau",
    "pihole": "reseau",
    # → auto-hebergement
    "nebula-sync": "auto-hebergement",
    "aws": "auto-hebergement",
    # → productivite
    "no-code": "productivite",
    "notion": "productivite",
    "calendrier": "productivite",
    "gestion-temps": "productivite",
    # → sysadmin
    "devops": "sysadmin",
    "migration": "sysadmin",
    "outils-systeme": "macos",
    "automatisation": "sysadmin",
    "depannage": "sysadmin",
    # → developpement
    "python": "developpement",
    "mysql": "developpement",
    # → terminal
    "oh-my-zsh": "terminal",
    "powerlevel10k": "terminal",
    "zsh": "terminal",
    "iterm2": "terminal",
    "cli": "terminal",
    # → active-directory
    "fsmo": "active-directory",
    # → snipeit
    "snipeagent": "snipeit",
    "itsm": "snipeit",
    "inventaire-it": "snipeit",
    # → monitoring
    "uptimerobot": "monitoring",
    "uptime-kuma": "monitoring",
    # → backup
    "sauvegarde": "backup",
    "vanderplanki": "backup",
    "sauvegarde-email": "backup",
    # → microsoft-365
    "outlook": "microsoft-365",
    "email": "microsoft-365",
    "exchange-online": "microsoft-365",
    # → multimedia
    "ffmpeg": "multimedia",
    # → hyper-v
    "vhdx": "hyper-v",
    # → guide
    "guide-complet": "guide",
    # → None (supprimer)
    "low-tech": None,
    "comparatif": None,
    "open-source": None,
    "outils": None,
    "utilitaire": None,
    "configuration": None,
    "theme": None,
    "catppuccin": None,
    "gratuit": None,
}


def parse_frontmatter_tags(content):
    """Extrait (pre_tags, tags_lines, post_tags) du fichier markdown."""
    lines = content.split("\n")
    # Trouver la zone frontmatter
    fm_start = fm_end = -1
    for i, line in enumerate(lines):
        if line == "---":
            if fm_start == -1:
                fm_start = i
            elif fm_end == -1:
                fm_end = i
                break

    if fm_start == -1 or fm_end == -1:
        return None, None, None, content

    # Trouver le bloc tags:
    tags_start = tags_end = -1
    for i in range(fm_start, fm_end):
        if lines[i].startswith("tags:"):
            tags_start = i
        elif tags_start != -1 and i > tags_start:
            if lines[i].startswith("  - "):
                tags_end = i
            else:
                break

    if tags_start == -1:
        return None, None, None, content

    tags_lines = lines[tags_start : tags_end + 1]
    return fm_start, tags_start, tags_end, lines


def extract_tags(tags_lines):
    tags = []
    for line in tags_lines:
        if line.startswith("  - "):
            tags.append(line[4:].strip())
    return tags


def apply_map(tags):
    result = []
    seen = set()
    for tag in tags:
        if tag in TAG_MAP:
            new_tag = TAG_MAP[tag]
            if new_tag is not None and new_tag not in seen:
                result.append(new_tag)
                seen.add(new_tag)
        elif tag in KEEP:
            if tag not in seen:
                result.append(tag)
                seen.add(tag)
        else:
            # Tag inconnu non mappé — conserver avec avertissement
            print(f"  WARN: tag inconnu non mappé '{tag}' — conservé", file=sys.stderr)
            if tag not in seen:
                result.append(tag)
                seen.add(tag)
    return result


def rebuild_tags_block(new_tags):
    lines = ["tags:"]
    for tag in new_tags:
        lines.append(f"  - {tag}")
    return lines


def process_file(path, dry_run=False):
    content = open(path, encoding="utf-8").read()
    lines = content.split("\n")

    fm_start, tags_start, tags_end, lines = parse_frontmatter_tags(content)
    if tags_start is None:
        return False, [], []

    tags_lines = lines[tags_start : tags_end + 1]
    old_tags = extract_tags(tags_lines)
    new_tags = apply_map(old_tags)

    if old_tags == new_tags:
        return False, old_tags, new_tags

    if not dry_run:
        new_tags_block = rebuild_tags_block(new_tags)
        new_lines = lines[:tags_start] + new_tags_block + lines[tags_end + 1 :]
        open(path, "w", encoding="utf-8").write("\n".join(new_lines))

    return True, old_tags, new_tags


def main(dry_run=False):
    changed = 0
    all_new_tags = set()

    for fname in sorted(os.listdir(BLOG_DIR)):
        if not fname.endswith(".md"):
            continue
        path = os.path.join(BLOG_DIR, fname)
        modified, old, new = process_file(path, dry_run)
        all_new_tags.update(new)

        if modified:
            changed += 1
            removed = set(old) - set(new)
            added = set(new) - set(old)
            print(f"  {fname}")
            if removed:
                print(f"    - {sorted(removed)}")
            if added:
                print(f"    + {sorted(added)}")

    print(f"\n{'[DRY RUN] ' if dry_run else ''}{changed} articles modifiés")
    print(f"Tags uniques résultants : {len(all_new_tags)}")
    print(f"Tags : {sorted(all_new_tags)}")


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv or "-n" in sys.argv
    main(dry_run=dry)
