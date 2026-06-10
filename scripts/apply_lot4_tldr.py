#!/usr/bin/env python3
"""Lot 4 Phase 2 : reecriture TL;DR (vault + site). Dry-run defaut, --apply."""
import re, sys
from pathlib import Path

VAULT = Path("/opt/brandon-knowledge/Projects/Content/Articles/04-Publies")
SITE = Path("/opt/2026-brandonvisca.com/src/data/blog")
_TLDR = re.compile(r"TL\W?DR", re.IGNORECASE)
CANON = "> 💡 **TL;DR**"

RANGE_PAIRS = [
 ("partager-mot-de-passe", 1,
  "> 💡 **TL;DR**\n> - Password.link : le plus simple pour les équipes IT (chiffrement client AES-256-GCM, notifications), mais pas self-hosted\n> - OneTimeSecret : illimité et open source, idéal pour les particuliers et les devs\n> - PrivateBin : self-hosted zéro connaissance, le choix des homelabbers (installation requise)"),
 ("rcmd-alternative", 5,
  "> 💡 **TL;DR**\n> - Cmd+Tab est lent (3 à 4 Tab à chaque fois pour atteindre la bonne app)\n> - rcmd remplace ça par Right Command + la lettre de l'app : accès direct en 0,2 s\n> - Un raccourci dédié par app (Right Cmd + S pour Safari, + V pour VS Code)"),
 ("shutter-encoder", 2,
  "> 💡 **TL;DR**\n> - HandBrake ne fait qu'une chose, la compression : impossible de trimmer, sous-titrer ou étalonner\n> - Shutter Encoder ajoute l'édition non-destructive, les sous-titres, les filtres et le batch processing\n> - Interface gratuite qui embarque FFmpeg, le couteau suisse de la vidéo"),
 ("yopass-vs-privatebin", 1,
  "> 💡 **TL;DR**\n> - Yopass : chiffrement côté client, CLI dispo, partage de fichiers, backend Memcached ou Redis\n> - PrivateBin : chiffrement côté client sans backend (fichiers), le plus simple à déployer\n> - Password Pusher : chiffrement côté serveur, autodestruction par vues ou durée, base de données requise"),
 ("quitter-google", "list",
  "> 💡 **TL;DR**\n> - J'ai viré Google Drive, Photos, Gmail et Calendar, remplacés par Nextcloud, Immich, Mailcow et Jellyfin\n> - Économie de 240€/an après un investissement de 200€, installé en un weekend\n> - Résultat : 100% fonctionnel, contrôle total de mes données"),
]

TEXT_PAIRS = [
 ("omarchy-distribution",
  "> 💡 **TL;DR** : Omarchy Linux v3.8.0 installe Arch + Hyprland clé en main. 11 thèmes, météo live, rappels intégrés, choix du browser/terminal/éditeur par défaut, outils dev prêts. Zéro config de départ.",
  "> 💡 **TL;DR**\n> - Omarchy Linux v3.8.0 installe Arch + Hyprland clé en main, zéro config de départ\n> - 11 thèmes, météo live, rappels intégrés, choix du browser/terminal/éditeur par défaut\n> - Outils de dev prêts à l'emploi, esprit « omakase » : tout fonctionne out-of-the-box"),
 ("photoprism-docker",
  "> 💡 **TL;DR**, PhotoPrism Docker en 4 points :\n>\n> - **C'est quoi ?** Une galerie photo auto-hébergée avec reconnaissance faciale, classification par IA et import automatique\n> - **Pourquoi ?** Google Photos te facture 2 To à 10€/mois, piste tes métadonnées GPS et te bloque si tu dépasses les quotas\n> - **Comment ?** Un `docker-compose.yml` avec PhotoPrism + MariaDB = opérationnel en 10 minutes\n> - **Coût ?** Zéro euro si tu as déjà un serveur avec Docker",
  "> 💡 **TL;DR**\n> - Galerie photo auto-hébergée avec reconnaissance faciale, classification par IA et import automatique\n> - Alternative à Google Photos, qui facture 2 To à 10€/mois et piste tes métadonnées GPS\n> - Un `docker-compose.yml` avec PhotoPrism + MariaDB : opérationnel en 10 minutes, zéro euro si tu as déjà un serveur"),
 ("snipeit-vs-glpi",
  "> 💡 **TL;DR**, SnipeIT gagne pour 90% des cas : installation en 45 min, interface moderne, codes QR natifs. GLPI vaut le coup uniquement si tu as besoin d’un helpdesk intégré et d’une CMDB complète. J’ai utilisé les deux pendant 3 ans, SnipeIT reste mon choix par défaut.",
  "> 💡 **TL;DR**\n> - SnipeIT gagne pour 90% des cas : installation en 45 min, interface moderne, codes QR natifs\n> - GLPI ne vaut le coup que si tu as besoin d'un helpdesk intégré et d'une CMDB complète\n> - Après 3 ans avec les deux, SnipeIT reste mon choix par défaut pour l'asset management"),
 ("termius-client-ssh",
  "> 💡 **TL;DR**, Termius est l'alternative moderne à PuTTY sur Windows : interface claire, clés SSH intégrées, SFTP natif. La version gratuite suffit pour 1-3 serveurs sur un seul poste. Le plan Pro (100$/an) débloque la sync cloud multi-appareils et s'amortit en 2 semaines pour un admin sys.",
  "> 💡 **TL;DR**\n> - Termius est l'alternative moderne à PuTTY sur Windows : interface claire, clés SSH intégrées, SFTP natif\n> - La version gratuite suffit pour 1 à 3 serveurs sur un seul poste\n> - Le plan Pro (100$/an) débloque la sync cloud multi-appareils, amorti en 2 semaines pour un admin sys"),
 ("ufw-docker-pare-feu",
  "**TL;DR**, UFW est le pare-feu le plus simple sous Linux, mais Docker contourne ses règles en manipulant iptables directement. Résultat : tes ports exposés restent accessibles depuis l'extérieur même si UFW dit le contraire. On va configurer UFW correctement avec Docker pour que tes règles de pare-feu soient réellement respectées, sans bloquer les conteneurs qui doivent communiquer entre eux.",
  "> 💡 **TL;DR**\n> - UFW est le pare-feu le plus simple sous Linux, mais Docker contourne ses règles via iptables\n> - Résultat : tes ports exposés restent accessibles de l'extérieur même si UFW dit le contraire\n> - On configure UFW correctement avec Docker pour que tes règles soient respectées sans casser les conteneurs"),
]


def region_end(lines, h, length):
    if length != "list":
        return h + length
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
    return last + 1


def run(apply):
    n = 0
    for frag, length, block in [(f, l, b) for f, l, b in RANGE_PAIRS]:
        for root in (VAULT, SITE):
            for path in root.glob(f"*{frag}*.md"):
                lines = path.read_text(encoding="utf-8").split("\n")
                h = next((i for i, l in enumerate(lines) if _TLDR.search(l)), None)
                if h is None or lines[h].strip() == CANON:
                    continue
                end = region_end(lines, h, length)
                new = "\n".join(lines[:h] + block.split("\n") + lines[end:])
                if apply:
                    try:
                        path.write_text(new, encoding="utf-8"); n += 1
                        print(f"  ✏️  {root.name}/{path.name[:43]}")
                    except PermissionError:
                        print(f"  ⛔ PERM {root.name}/{path.name[:43]}")
                else:
                    print(f"  🔍 {root.name}/{path.name[:43]} (end={end}, h={h})"); n += 1
    for frag, old, new in TEXT_PAIRS:
        for root in (VAULT, SITE):
            for path in root.glob(f"*{frag}*.md"):
                c = path.read_text(encoding="utf-8")
                if old not in c:
                    continue
                if apply:
                    try:
                        path.write_text(c.replace(old, new, 1), encoding="utf-8"); n += 1
                        print(f"  ✏️  {root.name}/{path.name[:43]}")
                    except PermissionError:
                        print(f"  ⛔ PERM {root.name}/{path.name[:43]}")
                else:
                    print(f"  🔍 {root.name}/{path.name[:43]}"); n += 1
    return n


def main(argv):
    apply = "--apply" in argv
    n = run(apply)
    print(f"\n→ {n} {'modifié(s)' if apply else 'à modifier'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
