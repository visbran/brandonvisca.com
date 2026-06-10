#!/usr/bin/env python3
"""Phase 3 lot 2 : insere un TL;DR canonique en tete de body. Dry-run defaut, --apply."""
import re, sys
from pathlib import Path

VAULT = Path("/opt/brandon-knowledge/Projects/Content/Articles/04-Publies")
SITE = Path("/opt/2026-brandonvisca.com/src/data/blog")
_TLDR = re.compile(r"TL\W?DR", re.IGNORECASE)
_FM = re.compile(r"^(---\n.*?\n---\n)", re.S)

ITEMS = [
 ("installer-localwp",
  "> 💡 **TL;DR**\n> - LocalWP monte un lab WordPress en local en 5 minutes, sans galérer avec XAMPP ou MAMP\n> - Tu testes, tu casses tout, tu déploies en prod quand c'est carré\n> - Guide complet avec troubleshooting et migration vers la prod gratuite"),
 ("itsm-snipeit-alternative-excel",
  "> 💡 **TL;DR**\n> - Gérer son inventaire IT dans Excel finit toujours mal (fichier perdu, données périmées)\n> - SnipeIT est l'alternative gratuite et open source pour suivre tes actifs IT sans stress\n> - Tu sais enfin ce que tu as, où ça se trouve et dans quel état"),
 ("ladybird-browser",
  "> 💡 **TL;DR**\n> - Ladybird est un navigateur open source construit from scratch, pas un énième fork de Chromium\n> - Ses propres moteurs maison (LibWeb, LibJS), indépendants de Google\n> - Architecture, financement et timeline d'un projet qui veut rebattre les cartes du web"),
 ("ldap-filtrage-utilisateurs-snipeit",
  "> 💡 **TL;DR**\n> - Filtrer les utilisateurs LDAP importés dans Snipe-IT depuis Active Directory\n> - Filtres sécurisés et exclusions par OU pour ne synchroniser que les bons comptes\n> - Cas d'usage avancés et bonnes pratiques 2025"),
 ("lunar-luminosite",
  "> 💡 **TL;DR**\n> - Lunar contrôle la luminosité de tes écrans externes sur macOS, ce que le système refuse de faire\n> - Il utilise le protocole DDC natif : tes touches F1/F2 fonctionnent enfin, avec sync auto\n> - Indispensable sur Mac Mini, installation en 3 méthodes"),
 ("magnet-macos",
  "> 💡 **TL;DR**\n> - Magnet est le gestionnaire de fenêtres n°1 sur macOS : snap au clavier ou par glisser\n> - Comparatif complet avec Rectangle (gratuit), BetterSnapTool et Moom\n> - Retour d'expérience après 2 ans, plus un guide d'installation détaillé"),
 ("masquer-utilisateurs-gal",
  "> 💡 **TL;DR**\n> - Masquer des utilisateurs de la GAL Office 365 synchronisés depuis Active Directory local\n> - Sans étendre le schéma AD (l'attribut `msExchHideFromAddressLists` manque en hybride)\n> - Solution testée avec Azure AD Connect"),
 ("nginx-location-bloc",
  "> 💡 **TL;DR**\n> - Les blocs `location` de Nginx définissent le comportement du serveur selon l'URL demandée\n> - Types de location, gestion des priorités et pièges de sécurité courants\n> - Bien utilisés ils organisent tes routes ; mal utilisés ils ouvrent des failles"),
 ("nginx-permissions-policy",
  "> 💡 **TL;DR**\n> - Après HSTS, CSP et X-Frame-Options, le header Permissions-Policy affine ta sécurité\n> - Il restreint les API navigateur (caméra, micro, géolocalisation) accessibles à ton site\n> - Plus des protections anti-bots intégrées à Nginx pour limiter les abus"),
 ("notion-sites-creation",
  "> 💡 **TL;DR**\n> - Notion Sites transforme tes pages Notion en vrais sites web avec un CMS intégré\n> - Personnalisation facile et gestion de domaines personnalisés\n> - Une approche intuitive pour publier en ligne sans quitter Notion"),
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
