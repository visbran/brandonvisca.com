#!/usr/bin/env python3
"""Lot 3 Phase 2 : reecriture TL;DR (vault + site). Dry-run defaut, --apply."""
import re, sys
from pathlib import Path

VAULT = Path("/opt/brandon-knowledge/Projects/Content/Articles/04-Publies")
SITE = Path("/opt/2026-brandonvisca.com/src/data/blog")
_TLDR = re.compile(r"TL\W?DR", re.IGNORECASE)
CANON = "> 💡 **TL;DR**"

# (fragment, nb_lignes_remplacees_depuis_header, nouveau_bloc)
RANGE_PAIRS = [
 ("hyperv-gen1-vs-gen2", 1,
  "> 💡 **TL;DR**\n> - Gen2 (UEFI) gagne presque partout : boot plus rapide, Secure Boot, disques OS jusqu'à 64 To (GPT)\n> - Gen1 (BIOS legacy) ne garde l'avantage que pour les OS 32 bits et les vieux Linux (< RHEL 6)\n> - Pour toute VM moderne (Windows Server 2012+, Linux récent), choisis Gen2 sans hésiter"),
 ("independance-numerique", "list",
  "> 💡 **TL;DR**\n> - Google Drive + Netflix + 1Password = 534€/an que tu peux ramener à 0€ (serveur existant) ou 30€/an (VPS)\n> - Remplace-les par Nextcloud (cloud), Jellyfin (streaming) et Vaultwarden (mots de passe)\n> - Contrôle total de tes données, 5 340€ économisés sur 10 ans"),
 ("jellyfin-docker-alternative", "list",
  "> 💡 **TL;DR**\n> - Netflix + Disney+ + Prime = 378€/an que tu remplaces par ton propre Jellyfin (0€ si tu as déjà un serveur)\n> - Installation Docker en 20 minutes, bibliothèque films/séries organisée automatiquement (metadata, posters, sous-titres)\n> - Streaming sur TV, mobile, tablette et navigateur, transcoding 4K en temps réel si ton serveur suit"),
 ("music-decoy", 2,
  "> 💡 **TL;DR**\n> - La touche Play du clavier Mac lance Apple Music par défaut, même si tu utilises Spotify\n> - Music Decoy intercepte la touche Play et empêche Apple Music de se lancer, sans configuration\n> - Micro-app installée en 3 secondes, peut démarrer automatiquement au login"),
 ("nextcloud-docker-installation", "list",
  "> 💡 **TL;DR**\n> - Google Drive / Dropbox / OneDrive à 10-20€/mois remplacés par ton Nextcloud à 3-5€/mois sur un petit VPS\n> - Installation Docker en 30 minutes, HTTPS automatique (Let's Encrypt), synchro multi-appareils\n> - Contrôle total de tes données, 120-240€/an économisés"),
]

# (fragment, ancienne_ligne, nouveau_bloc)
TEXT_PAIRS = [
 ("installation-theme-vim",
  "> 💡 **TL;DR**, Catppuccin est le thème Vim le plus populaire en 2025. Installe vim-plug, ajoute 2 lignes dans ton `.vimrc`, lance `:PlugInstall`. C'est tout. Si les couleurs ne s'affichent pas, ajoute `set termguicolors` dans ton `.vimrc`.",
  "> 💡 **TL;DR**\n> - Catppuccin est le thème Vim le plus populaire : installe vim-plug, ajoute 2 lignes au `.vimrc`, lance `:PlugInstall`\n> - Catppuccin Mocha tient le mieux sur fond sombre sans fatiguer les yeux sur de longues sessions\n> - Si les couleurs ne s'affichent pas, ajoute `set termguicolors` dans ton `.vimrc`"),
 ("installation-vim-guide-complet",
  "> 💡 **TL;DR**, Vim est disponible sur macOS via Homebrew (`brew install vim`) et sur Linux via le gestionnaire de paquets natif. Un `.vimrc` de 15 lignes suffit pour un éditeur fonctionnel. Ajoute vim-plug pour les plugins, NERDTree pour l'arbre de fichiers, FZF pour la recherche.",
  "> 💡 **TL;DR**\n> - Vim s'installe via Homebrew sur macOS (`brew install vim`) et le gestionnaire de paquets natif sous Linux\n> - Un `.vimrc` de 15 lignes suffit pour un éditeur fonctionnel\n> - Ajoute vim-plug pour les plugins, NERDTree pour l'arbre de fichiers, FZF pour la recherche"),
 ("migration-wordpress-all-in-one",
  "> 💡 **TL;DR** : Installe All-in-One WP Migration v6.77 (la dernière version qui importe gratuitement), exporte depuis l'ancien site, importe sur le nouveau. Augmente la limite dans `constants.php` si ton site dépasse 512 MB. [Télécharge directement la v6.77 ici.](/downloads/all-in-one-wp-migration.6.77.zip)",
  "> 💡 **TL;DR**\n> - All-in-One WP Migration v6.77 (dernière version qui importe gratuitement) : exporte l'ancien site, importe sur le nouveau\n> - Augmente la limite dans `constants.php` si ton site dépasse 512 Mo\n> - [Télécharge directement la v6.77 ici](/downloads/all-in-one-wp-migration.6.77.zip)"),
 ("mise-a-jour-pfsense",
  "> 💡 **TL;DR** : Télécharge pfSense 2.8.1 (CE) sur [netgate.com](https://www.netgate.com/pfsense-plus-software/how-to-buy#pfsense-ce). Mise à jour depuis 2.7.x : sauvegarde config → System > Update → sélectionne CE 2.8.1 → redémarre. Sous Proxmox, préfère une clean install + import config.xml. WireGuard est intégré nativement, réimporte tes clés si tu migres depuis 2.7.x.",
  "> 💡 **TL;DR**\n> - pfSense 2.8.1 (CE) se télécharge sur netgate.com ; mise à jour depuis 2.7.x : sauvegarde config, System > Update, redémarre\n> - Sous Proxmox, préfère une clean install puis import du `config.xml`\n> - WireGuard est intégré nativement, réimporte tes clés si tu migres depuis 2.7.x"),
 ("nebula-sync-pihole",
  "> 💡 **TL;DR**, Nebula-Sync est le successeur de Gravity Sync compatible Pi-hole v6. Il synchronise automatiquement tes Pi-hole (listes noires, config DNS, groupes) via Docker ou binaire Go. Un docker-compose de 10 lignes suffit pour démarrer.",
  "> 💡 **TL;DR**\n> - Nebula-Sync est le successeur de Gravity Sync, compatible Pi-hole v6\n> - Il synchronise automatiquement tes Pi-hole (listes noires, config DNS, groupes) via Docker ou binaire Go\n> - Un `docker-compose.yml` de 10 lignes suffit pour démarrer"),
]


def run_range(apply):
    n = 0
    for frag, length, block in RANGE_PAIRS:
        for root in (VAULT, SITE):
            for path in root.glob(f"*{frag}*.md"):
                lines = path.read_text(encoding="utf-8").split("\n")
                h = next((i for i, l in enumerate(lines) if _TLDR.search(l)), None)
                if h is None:
                    continue
                if lines[h].strip() == CANON:
                    continue  # idempotence
                if length == "list":
                    # consomme header + prose + la liste de puces complete qui suit
                    j = h + 1
                    last = h
                    entered = False
                    while j < len(lines):
                        s = lines[j].strip()
                        if re.match(r"^[-*]\s+\S", s) or s.startswith("✅"):
                            entered = True; last = j; j += 1
                        elif s == "":
                            j += 1
                        elif not entered:
                            last = j; j += 1
                        else:
                            break
                    end = last + 1
                else:
                    end = h + length
                new = "\n".join(lines[:h] + block.split("\n") + lines[end:])
                if apply:
                    try:
                        path.write_text(new, encoding="utf-8"); n += 1
                        print(f"  ✏️  {root.name}/{path.name[:45]}")
                    except PermissionError:
                        print(f"  ⛔ PERM {root.name}/{path.name[:45]}")
                else:
                    print(f"  🔍 {root.name}/{path.name[:45]} (-{length}L @ {h})"); n += 1
    return n


def run_text(apply):
    n = 0
    for frag, old, new in TEXT_PAIRS:
        for root in (VAULT, SITE):
            for path in root.glob(f"*{frag}*.md"):
                c = path.read_text(encoding="utf-8")
                if old not in c:
                    continue
                if apply:
                    try:
                        path.write_text(c.replace(old, new, 1), encoding="utf-8"); n += 1
                        print(f"  ✏️  {root.name}/{path.name[:45]}")
                    except PermissionError:
                        print(f"  ⛔ PERM {root.name}/{path.name[:45]}")
                else:
                    print(f"  🔍 {root.name}/{path.name[:45]}"); n += 1
    return n


def main(argv):
    apply = "--apply" in argv
    n = run_range(apply) + run_text(apply)
    print(f"\n→ {n} {'modifié(s)' if apply else 'à modifier'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
