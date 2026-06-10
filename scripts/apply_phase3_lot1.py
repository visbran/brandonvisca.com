#!/usr/bin/env python3
"""Phase 3 lot 1 : insere un TL;DR canonique en tete de body. Dry-run defaut, --apply."""
import re, sys
from pathlib import Path

VAULT = Path("/opt/brandon-knowledge/Projects/Content/Articles/04-Publies")
SITE = Path("/opt/2026-brandonvisca.com/src/data/blog")
_TLDR = re.compile(r"TL\W?DR", re.IGNORECASE)
_FM = re.compile(r"^(---\n.*?\n---\n)", re.S)

# (fragment_slug, bloc_TLDR)
ITEMS = [
 ("10-extensions-raycast",
  "> 💡 **TL;DR**\n> - Le Store Raycast compte plus de 1000 extensions gratuites et open source\n> - 10 incontournables pour dev et sysadmin : Docker, GitHub, SSH, Brew et compagnie\n> - Installation en un clic depuis le Store, et tu peux même créer la tienne"),
 ("paperless-ngx-docker-guide",
  "> 💡 **TL;DR**\n> - Paperless-ngx archive, numérise et indexe tous tes documents avec OCR, fini le tiroir à paperasse\n> - Déploiement avec Docker Compose, un fichier complet fourni dans le guide\n> - Au quotidien : tu scannes, il classe et rend tout cherchable en plein texte"),
 ("activedirectory-transfere-des-roles-fsmo",
  "> 💡 **TL;DR**\n> - Les rôles FSMO sont 5 fonctions critiques d'un domaine Active Directory, portées par un ou plusieurs DC\n> - On les transfère proprement entre contrôleurs via l'interface graphique ou PowerShell\n> - Ce guide couvre le transfert (Maître RID en exemple) et la vérification post-transfert"),
 ("clop-compression-images-videos",
  "> 💡 **TL;DR**\n> - Clop compresse automatiquement tes images et vidéos dès que tu les copies, sur macOS\n> - Fini les fichiers trop lourds pour les emails ou Slack, sans manipulation manuelle\n> - Gratuit, installation en 3 méthodes, configuration essentielle en 5 minutes"),
 ("configuration-avancee-snipeit",
  "> 💡 **TL;DR**\n> - Configuration SnipeIT niveau pro : intégration Active Directory LDAP et portail libre-service\n> - Scan réseau automatique du parc avec Nmap et sécurité avancée\n> - Notifications Teams et email pour suivre l'inventaire sans y penser"),
 ("content-security-policy-nginx",
  "> 💡 **TL;DR**\n> - La Content-Security-Policy est l'un des headers les plus puissants contre les attaques XSS\n> - Mal configurée, elle bloque tes propres scripts et casse le site\n> - Ce guide montre comment la configurer dans Nginx pas à pas, sans casser le frontend"),
 ("depannage-montage-partition-raid",
  "> 💡 **TL;DR**\n> - Erreur `wrong fs type, bad superblock` au montage d'une matrice RAID mdadm en mode secours\n> - Cause : l'array RAID contenait une table de partitions, pas directement un système de fichiers\n> - Solution : monter la bonne partition de l'array plutôt que le périphérique RAID brut"),
 ("exploration-de-super-so",
  "> 💡 **TL;DR**\n> - Super.so transforme tes pages Notion en site web personnalisé et optimisé pour le SEO\n> - Personnalisation avancée du design sans quitter ton workflow Notion\n> - Une solution simple pour publier un vrai site à partir de contenu Notion"),
 ("installation-homebrew-macos",
  "> 💡 **TL;DR**\n> - Homebrew, le gestionnaire de paquets macOS, s'installe en une seule commande\n> - Commandes essentielles (`brew install`, `update`, `upgrade`) et premières apps à installer\n> - Section dépannage pour les erreurs courantes après l'installation"),
 ("installation-snipeit-ubuntu",
  "> 💡 **TL;DR**\n> - Installation complète de SnipeIT sur Ubuntu 22.04/24.04 : stack LAMP, MySQL, Git\n> - Permissions et sécurité gérées proprement pour ne rien casser\n> - Guide pas à pas pensé pour les débutants"),
]


def run(apply):
    n = 0
    for frag, block in ITEMS:
        for root in (VAULT, SITE):
            for path in root.glob(f"*{frag}*.md"):
                content = path.read_text(encoding="utf-8")
                m = _FM.match(content)
                if not m:
                    print(f"  ⚠️  pas de frontmatter: {path.name}"); continue
                body = content[m.end():]
                if _TLDR.search(body):
                    print(f"  ⏭️  a déjà un TL;DR: {root.name}/{path.name[:40]}"); continue
                new = m.group(1) + "\n" + block + "\n\n" + body.lstrip("\n")
                if apply:
                    try:
                        path.write_text(new, encoding="utf-8"); n += 1
                        print(f"  ✏️  {root.name}/{path.name[:43]}")
                    except PermissionError:
                        print(f"  ⛔ PERM {root.name}/{path.name[:43]}")
                else:
                    print(f"  🔍 {root.name}/{path.name[:43]}"); n += 1
    return n


def main(argv):
    apply = "--apply" in argv
    n = run(apply)
    print(f"\n→ {n} {'inséré(s)' if apply else 'à insérer'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
