#!/usr/bin/env python3
"""Lot 2 Phase 2 : reecriture TL;DR. Dry-run par defaut, --apply pour ecrire."""
import sys
from pathlib import Path

VAULT = Path("/opt/brandon-knowledge/Projects/Content/Articles/04-Publies")
SITE = Path("/opt/2026-brandonvisca.com/src/data/blog")

# --- 5 fichiers vault legacy (non deployes) : remplacement par plage de lignes ---
# (nom_fichier, nb_lignes_a_remplacer_depuis_le_header_TLDR, nouveau_bloc)
VAULT_RANGE = [
 ("Alt-SendMe Arme Secrète pour Partager des Fichiers Sans Espionnage (Guide 2025).md", 14,
  "> 💡 **TL;DR**\n"
  "> - Transfert P2P direct entre deux machines, sans serveur cloud intermédiaire (WeTransfer + LocalSend réunis)\n"
  "> - Chiffrement end-to-end, aucune limite de taille, pas d'inscription, open source et gratuit\n"
  "> - Compatible Windows, macOS, Linux, plus une CLI, installation en 5 minutes\n"
  "\n"
  "**Alt-SendMe** est une solution de transfert de fichiers en peer-to-peer. Contrairement à WeTransfer ou Google Drive, elle transfère les fichiers directement entre deux machines, sans passer par un serveur cloud intermédiaire : vitesse maximale, chiffrement total et zéro limite de taille."),

 ("Handy La Transcription Vocale Open Source qui Respecte ta Vie Privée (Guide 2025).md", 12,
  "> 💡 **TL;DR**\n"
  "> - Transcription vocale open source (GPL-3.0), un Dragon NaturallySpeaking gratuit\n"
  "> - 100% local, propulsé par Whisper (OpenAI), aucune donnée envoyée au cloud\n"
  "> - Push-to-talk ou toggle, compatible Linux, macOS et Windows"),

 ("Iroh Stack Technique Comment QUIC, TLS 1.3 et Blake3 Rendent le P2P Possible (Deep Dive 2025).md", 11,
  "> 💡 **TL;DR**\n"
  "> - Bibliothèque Rust qui combine QUIC (transport UDP multiplexé) et TLS 1.3 (chiffrement bout en bout)\n"
  "> - Blake3 pour vérifier l'intégrité ultra-vite, NAT traversal pour traverser les routeurs sans config\n"
  "> - Résultat : des transferts P2P qui saturent une connexion 4 Gbps, utilisés par Alt-SendMe et Sendme CLI"),

 ("ITSM pour débutants pourquoi votre Excel va finalement vous rendre fou.md", 1,
  "> 💡 **TL;DR**\n"
  "> - Gérer son inventaire IT dans Excel finit toujours mal (fichier perdu, données périmées, zéro traçabilité)\n"
  "> - L'ITSM structure le suivi du matériel, des licences et des garanties à la place du tableur\n"
  "> - SnipeIT est l'outil open source qui remplace ton Excel d'inventaire sans prise de tête"),

 ("Launchie macOS Alternative Moderne à Launchpad (Gratuit 2025).md", 2,
  "> 💡 **TL;DR**\n"
  "> - Apple a supprimé Launchpad dans macOS Tahoe (2025), beaucoup ont perdu leur launcher visuel\n"
  "> - Launchie le ramène : grille moderne, recherche rapide, dossiers, hot corners (version Pro)\n"
  "> - App légère et gratuite, avec un upgrade Pro optionnel"),
]

# --- 5 articles normaux (vault + site) : remplacement texte d'une ligne ---
TEXT_PAIRS = [
 ("exchange-online-bloquer-transferts",
  "> 💡 **TL;DR** : Crée une Transport Rule PowerShell (`-MessageType AutoForward -SentToScope NotInOrganization`) pour bloquer tous les transferts externes en une commande. Le RBAC ne bloque rien, c'est cosmétique. Audite ensuite avec `Get-Mailbox` + `Get-InboxRule` pour nettoyer les redirections existantes.",
  "> 💡 **TL;DR**\n> - Une Transport Rule PowerShell (`-MessageType AutoForward -SentToScope NotInOrganization`) bloque tous les transferts externes en une commande\n> - Le RBAC ne bloque rien, c'est cosmétique : ne compte pas dessus\n> - Audite l'existant avec `Get-Mailbox` et `Get-InboxRule` pour nettoyer les redirections déjà en place"),

 ("fail2ban-docker-securite",
  "**TL;DR**, On va installer Fail2Ban via Docker pour bloquer automatiquement les IP qui s'acharnent sur tes services. Container officiel `crazymax/fail2ban`, un `docker-compose.yml`, trois fichiers de config et tu dors tranquille. Pas besoin d'installer quoique ce soit sur l'hôte, sauf Docker.",
  "> 💡 **TL;DR**\n> - Fail2Ban via Docker bannit automatiquement les IP qui s'acharnent sur tes services (SSH, web)\n> - Image officielle `crazymax/fail2ban`, un `docker-compose.yml` et trois fichiers de config\n> - Rien à installer sur l'hôte à part Docker : service isolé, versionné, reproductible"),

 ("gerer-fichiers-amazon-s3-avec-s3cmd",
  "> 💡 **TL;DR** : Installe S3cmd (`sudo apt install s3cmd`), configure avec `s3cmd --configure` (clés AWS + région), puis utilise `s3cmd sync /local/ s3://bucket/` pour synchroniser. Compatible MinIO, Backblaze B2, OVH. Gratuit et open source.",
  "> 💡 **TL;DR**\n> - Installe S3cmd (`sudo apt install s3cmd`) puis configure-le avec `s3cmd --configure` (clés AWS + région)\n> - `s3cmd sync /local/ s3://bucket/` synchronise tes fichiers, parfait en cron ou pipeline\n> - Compatible MinIO, Backblaze B2 et OVH, gratuit et open source"),

 ("guide-swap-linux",
  "> 💡 **TL;DR** : Le swap sous Linux se configure mieux avec un fichier qu'une partition. Abaisse la swappiness à 10 sur un serveur, surveille avec `free -h` et `swapon --show`. Même avec 8 Go de RAM, 1 à 2 Go de swap restent une bonne pratique.",
  "> 💡 **TL;DR**\n> - Le swap se configure mieux avec un fichier qu'avec une partition (plus souple, sans toucher au disque)\n> - Abaisse la `swappiness` à 10 sur un serveur, surveille avec `free -h` et `swapon --show`\n> - Même avec 8 Go de RAM, garder 1 à 2 Go de swap reste une bonne pratique"),

 ("hardening-linux-10-commandes",
  "**TL;DR**, Tu peux durcir un serveur Linux en dix minutes avec dix commandes. Pas besoin d'être expert en sécurité offensive : un pare-feu actif, SSH verrouillé, mises à jour auto et un audit rapide suffisent à éliminer 90 % des attaques automatisées.",
  "> 💡 **TL;DR**\n> - Durcir un serveur Linux prend dix minutes avec dix commandes, sans être expert en sécurité\n> - Pare-feu actif, SSH verrouillé, mises à jour automatiques et un audit rapide\n> - Ces basiques éliminent 90 % des attaques automatisées qui scannent internet"),
]

import re
_TLDR = re.compile(r"TL\W?DR", re.IGNORECASE)


def apply_range(apply: bool) -> int:
    done = 0
    for fname, length, block in VAULT_RANGE:
        path = VAULT / fname
        if not path.exists():
            print(f"  ⚠️  absent: {fname[:40]}"); continue
        lines = path.read_text(encoding="utf-8").split("\n")
        h = next((i for i, l in enumerate(lines) if _TLDR.search(l)), None)
        if h is None:
            print(f"  ⚠️  pas de TL;DR: {fname[:40]}"); continue
        # idempotence : si deja canonique, ne pas re-remplacer (sinon on mange du contenu)
        if lines[h].strip() == "> 💡 **TL;DR**":
            print(f"  ⏭️  déjà canonique: {fname[:40]}"); continue
        new_lines = lines[:h] + block.split("\n") + lines[h + length:]
        if apply:
            try:
                path.write_text("\n".join(new_lines), encoding="utf-8"); done += 1
                print(f"  ✏️  vault/{fname[:45]}")
            except PermissionError:
                print(f"  ⛔ PERM vault/{fname[:45]}")
        else:
            print(f"  🔍 vault/{fname[:45]} (remplace {length} lignes @ {h})")
            done += 1
    return done


def apply_text(apply: bool) -> int:
    done = 0
    for frag, old, new in TEXT_PAIRS:
        for root in (VAULT, SITE):
            for path in root.glob(f"*{frag}*.md"):
                c = path.read_text(encoding="utf-8")
                if old not in c:
                    continue
                if apply:
                    try:
                        path.write_text(c.replace(old, new, 1), encoding="utf-8"); done += 1
                        print(f"  ✏️  {root.name}/{path.name}")
                    except PermissionError:
                        print(f"  ⛔ PERM {root.name}/{path.name}")
                else:
                    print(f"  🔍 {root.name}/{path.name}"); done += 1
    return done


def main(argv):
    apply = "--apply" in argv
    n = apply_range(apply) + apply_text(apply)
    print(f"\n→ {n} {'modifié(s)' if apply else 'à modifier'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
