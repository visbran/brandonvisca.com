#!/usr/bin/env python3
"""
apply_phase2_tldr.py — Applique les TL;DR reecrits (Phase 2) sur le vault ET le
site. Scope par fragment de slug (present dans les deux noms de fichier).
Remplace l'ancien bloc (old) par le bloc canonique (new) si old est present.

Usage : python3 scripts/apply_phase2_tldr.py [--apply]   (dry-run par defaut)
"""
import sys
from pathlib import Path

ROOTS = [
    Path("/opt/brandon-knowledge/Projects/Content/Articles/04-Publies"),
    Path("/opt/2026-brandonvisca.com/src/data/blog"),
]

# (fragment_slug, old_text, new_block)
PAIRS = [
 ("tianji",
  "> 💡 **TL;DR** : Tianji analytics est une alternative open-source à Google Analytics, 100% self-hosted. Il combine analytics, uptime monitoring et server status dans un seul container Docker. Pas de cookie, pas de bannière RGPD, zéro coût.",
  "> 💡 **TL;DR**\n> - Alternative open-source à Google Analytics, 100% auto-hébergée, sans cookie ni bannière RGPD\n> - Combine analytics, uptime monitoring et server status dans un seul container Docker\n> - Zéro coût, tes données de visiteurs restent chez toi"),

 ("miniflux",
  "> 💡 **TL;DR**, Miniflux Docker en 4 points :\n>\n> - **C'est quoi ?** Un lecteur RSS minimaliste et auto-hébergé qui lit les flux sans tracking ni pub\n> - **Pourquoi ?** Google Reader est mort, Feedly te piste, et tes flux méritent un toit privé\n> - **Comment ?** Un `docker-compose.yml` avec Miniflux + PostgreSQL = opérationnel en 5 minutes\n> - **Coût ?** Zéro euro si tu as déjà un serveur avec Docker",
  "> 💡 **TL;DR**\n> - Lecteur RSS minimaliste et auto-hébergé, sans tracking ni pub, contrairement à Feedly\n> - Un `docker-compose.yml` avec Miniflux + PostgreSQL : opérationnel en 5 minutes\n> - Zéro euro si tu as déjà un serveur avec Docker"),

 ("linkding",
  "> 💡 **TL;DR**, Linkding Docker en 4 points :\n>\n> - **C'est quoi ?** Un gestionnaire de bookmarks open-source, auto-hébergé et minimaliste qui archive tes liens automatiquement\n> - **Pourquoi ?** Pinboard est payant, Pocket te piste, et tes bookmarks méritent un toit privé que tu contrôles\n> - **Comment ?** Un `docker-compose.yml` de 20 lignes = opérationnel en 2 minutes, SQLite intégré\n> - **Coût ?** Zéro euro, licence MIT, environ 100 Mo de RAM",
  "> 💡 **TL;DR**\n> - Gestionnaire de bookmarks open-source et auto-hébergé qui archive tes liens automatiquement\n> - Un `docker-compose.yml` de 20 lignes avec SQLite : opérationnel en 2 minutes\n> - Zéro euro, licence MIT, environ 100 Mo de RAM (tourne sur un Raspberry Pi)"),

 ("ajouter-un-programme-au-path",
  "> 💡 **TL;DR** : Pour ajouter un programme au PATH Windows, lance `sysdm.cpl` → Avancé → Variables d'environnement → modifie `Path`. Pour automatiser : utilise `[Environment]::SetEnvironmentVariable` en PowerShell. Ferme et rouvre ton terminal après chaque modif.",
  "> 💡 **TL;DR**\n> - Interface graphique : `sysdm.cpl` puis Variables d'environnement, modifie `Path`\n> - Automatisation : `[Environment]::SetEnvironmentVariable` en PowerShell\n> - Ferme et rouvre ton terminal après chaque modification pour qu'elle soit prise en compte"),

 ("android-file-transfer",
  "## 🎯 TL;DR : Le verdict en 30 secondes",
  "> 💡 **TL;DR**\n> - Android File Transfer est gratuit mais lent (4 Mo/s), instable et plafonné à 4 Go par fichier\n> - OpenMTP : gratuit, open-source, 2x plus rapide, sans limite de taille, mon choix pour 90% des cas\n> - MacDroid (19.99$) : payant mais stable, pour qui veut le support et l'interface la plus léchée"),

 ("appcleaner",
  "TL;DR\n-----",
  "> 💡 **TL;DR**\n> - Désinstaller une app en la glissant à la Corbeille laisse des résidus (`~/Library`, caches, préférences)\n> - AppCleaner supprime tous les fichiers liés en un glisser-déposer, 100% gratuit\n> - SmartDelete automatise le nettoyage à chaque désinstallation, sans payer CleanMyMac 40€/an"),

 ("appcleaner",
  "TL;DR\n\n",
  "> 💡 **TL;DR**\n> - Désinstaller une app en la glissant à la Corbeille laisse des résidus (`~/Library`, caches, préférences)\n> - AppCleaner supprime tous les fichiers liés en un glisser-déposer, 100% gratuit\n> - SmartDelete automatise le nettoyage à chaque désinstallation, sans payer CleanMyMac 40€/an\n"),

 ("calendrier-et-gestion-des-taches-unifies-morgen",
  "> 💡 **TL;DR** : Morgen connecte tous tes calendriers (Google, Outlook, Apple) et tes outils de tâches (Notion, Todoist, Linear) dans une seule interface. L'AI Planner planifie ta semaine automatiquement. Disponible sur macOS, Windows, Linux, iOS, Android.",
  "> 💡 **TL;DR**\n> - Réunit tous tes calendriers (Google, Outlook, Apple) et tes outils de tâches (Notion, Todoist, Linear) dans une seule interface\n> - L'AI Planner planifie ta semaine automatiquement en priorisant tes tâches dans le calendrier\n> - Disponible sur macOS, Windows, Linux, iOS et Android"),

 ("cling-recherche-fuzzy",
  "## TL;DR : Cling en 30 secondes\n\n**Le problème** : Spotlight lent + pas de tolérance aux fautes\n\n**La solution** : Cling = Recherche fuzzy ultra-rapide",
  "> 💡 **TL;DR**\n> - Spotlight est lent (2 à 5 s) et ne tolère pas les fautes de frappe\n> - Cling fait de la recherche fuzzy ultra-rapide (moins de 0,5 s), tolérante aux fautes\n> - Il trouve les dotfiles et fichiers système que Spotlight ignore"),

 ("connecter-les-systemes-ubuntu-a-active-directory",
  "> 💡 **TL;DR** : Intègre Ubuntu à Active Directory via SSSD en 5 étapes : installe realmd + sssd-ad, configure le DNS vers ton DC, `realm join`, ajuste sssd.conf et krb5.conf, active mkhomedir. Authentification centralisée opérationnelle en 15 min.",
  "> 💡 **TL;DR**\n> - Intègre Ubuntu à Active Directory via SSSD : realmd + sssd-ad, DNS pointé vers ton DC, puis `realm join`\n> - Ajuste `sssd.conf` et `krb5.conf`, active `mkhomedir` pour créer les home au premier login\n> - Authentification centralisée Kerberos avec cache hors ligne, opérationnelle en 15 min"),

 ("duplicati",
  "**TL;DR**, Duplicati via Docker te permet de sauvegarder chiffrées tes données vers n'importe quel stockage local ou cloud. Docker Compose complet, UI web sur le port 8200, chiffrement AES-256 et aucune ligne de commande nécessaire après l'install.",
  "> 💡 **TL;DR**\n> - Sauvegardes chiffrées AES-256 vers n'importe quel stockage local ou cloud (S3, B2, SFTP, Drive)\n> - Stack Docker Compose complète, interface web sur le port 8200\n> - Aucune ligne de commande nécessaire après l'installation, restauration en trois clics"),
]


def main(argv):
    apply = "--apply" in argv
    done = 0
    for frag, old, new in PAIRS:
        for root in ROOTS:
            for path in root.glob(f"*{frag}*.md"):
                content = path.read_text(encoding="utf-8")
                if old not in content:
                    continue
                if apply:
                    try:
                        path.write_text(content.replace(old, new, 1), encoding="utf-8")
                        print(f"  ✏️  {root.name}/{path.name}")
                        done += 1
                    except PermissionError:
                        print(f"  ⛔ PERM  {root.name}/{path.name}")
                else:
                    print(f"  🔍 MATCH  {root.name}/{path.name}")
                    done += 1
    print(f"\n→ {done} fichier(s) {'modifié(s)' if apply else 'à modifier'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
