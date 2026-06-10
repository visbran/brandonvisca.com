#!/usr/bin/env python3
"""Phase 3 lot 3 (final) : insere un TL;DR canonique en tete de body. Dry-run defaut, --apply."""
import re, sys
from pathlib import Path

VAULT = Path("/opt/brandon-knowledge/Projects/Content/Articles/04-Publies")
SITE = Path("/opt/2026-brandonvisca.com/src/data/blog")
_TLDR = re.compile(r"TL\W?DR", re.IGNORECASE)
_FM = re.compile(r"^(---\n.*?\n---\n)", re.S)

ITEMS = [
 ("outils-low-tech-macos",
  "> 💡 **TL;DR**\n> - 10 outils macOS gratuits, légers et sans abonnement, chacun fait une chose et la fait bien\n> - rcmd (switch d'apps), Clop (compression), Lunar (luminosité) et 7 autres du quotidien\n> - Brewfile inclus pour tout installer d'un coup, environ 453€/an économisés vs les alternatives"),
 ("proteger-nginx-fichiers-sensibles",
  "> 💡 **TL;DR**\n> - La sécurité Nginx commence dans la config, pas seulement avec les headers ou le pare-feu\n> - Bloquer l'accès aux fichiers sensibles et interdire l'exécution de scripts dans les dossiers d'uploads\n> - Limiter les méthodes HTTP aux seules actions légitimes"),
 ("raycast-vs-alfred",
  "> 💡 **TL;DR**\n> - Test de Raycast, Alfred et Spotlight pendant 30 jours, comparatif objectif\n> - Tableaux détaillés, prix réels et verdict par profil d'utilisateur\n> - De quoi choisir ton launcher macOS sans y passer un mois toi-même"),
 ("restaurer-vm-hyperv",
  "> 💡 **TL;DR**\n> - VM Hyper-V qui démarre encore mais `Export-VM` plante et les sauvegardes VSS refusent\n> - Reconstruis un VHDX OS sain via WinPE + robocopy + bcdboot, sans réinstaller Windows Server\n> - Procédure pas à pas, sans perdre tes données"),
 ("securiser-nginx-avec-headers",
  "> 💡 **TL;DR**\n> - Sécuriser Nginx avec les headers HTTP recommandés par l'OWASP\n> - Protection contre XSS, clickjacking et vol de session\n> - Exemples de configuration concrets et bonnes pratiques"),
 ("securite-de-votre-serveur-linux",
  "> 💡 **TL;DR**\n> - Durcir un serveur Linux de bout en bout : SSH, pare-feu ufw, fail2ban, mises à jour auto\n> - Renforcement réseau via sysctl, anti-spoofing IP et surveillance des logs\n> - Guide pratique testé en production"),
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
                    print(f"  ⏭️  déjà TL;DR: {root.name}/{path.name[:40]}"); continue
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
