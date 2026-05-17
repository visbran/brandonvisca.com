---
title: "S3cmd : synchronise et sauvegarde vers Amazon S3 gratuitement (guide 2026)"
description: "S3cmd : installer, configurer et utiliser ce client CLI pour Amazon S3. Commandes essentielles, sync, backup et chiffrement. Guide complet 2026."
pubDatetime: "2025-02-17T17:37:40+01:00"
modDatetime: "2026-05-17T00:00:00+01:00"
author: Brandon Visca
tags:
  - linux
  - sysadmin
  - aws
  - backup
  - intermediaire
  - guide
featured: false
draft: false
focusKeyword: S3cmd
faqs:
  - question: "S3cmd fonctionne-t-il avec autre chose qu'Amazon S3 ?"
    answer: "Oui. S3cmd est compatible avec tout service S3-compatible : MinIO, Backblaze B2, OVH Object Storage, Scaleway Object Storage, Cloudflare R2 et d'autres."
  - question: "Comment chiffrer les fichiers uploadés avec S3cmd ?"
    answer: "Ajoute l'option --encrypt (chiffrement côté client GPG) ou --server-side-encryption (chiffrement côté serveur AWS). Configure la passphrase GPG lors de s3cmd --configure."
  - question: "S3cmd sauvegarde-t-il uniquement les fichiers modifiés ?"
    answer: "Oui avec s3cmd sync --skip-existing. S3cmd compare les checksums MD5 et ne retransmet que les fichiers modifiés ou nouveaux."
  - question: "Comment automatiser des sauvegardes S3cmd ?"
    answer: "Ajoute une ligne cron : '0 2 * * * s3cmd sync /chemin/local/ s3://mon-bucket/backup/' pour une sauvegarde quotidienne à 2h du matin."
---
> 💡 **TL;DR** : Installe S3cmd (`sudo apt install s3cmd`), configure avec `s3cmd --configure` (clés AWS + région), puis utilise `s3cmd sync /local/ s3://bucket/` pour synchroniser. Compatible MinIO, Backblaze B2, OVH. Gratuit et open source.

![S3cmd — gérer Amazon S3 en CLI](friends-episode-15-friends-tv-the-one-where-estelle-dies-w3a0zo282fubpsqqyd.gif)

Tu veux uploader, synchroniser ou sauvegarder des fichiers vers Amazon S3 (ou un service compatible) sans passer par la console AWS ? **S3cmd** est le client CLI qu'il te faut. Open source, gratuit, compatible avec tous les services S3-like, il tourne parfaitement dans des scripts cron ou des pipelines de déploiement.

J'utilise S3cmd pour sauvegarder mes dumps MySQL et configs Proxmox vers un bucket S3-compatible. Ça tourne en cron chaque nuit depuis 2 ans sans accroc.

## Table des matières

- - - - - -

## Pourquoi choisir S3cmd

S3cmd n'est pas le seul client S3 CLI (il y a aussi le AWS CLI officiel, rclone...), mais il a quelques atouts :

- **Open source et gratuit** — pas de licence, pas d'abonnement
- **Compatible S3-like** — fonctionne avec MinIO, Backblaze B2, OVH Object Storage, Scaleway, Cloudflare R2
- **Syntaxe simple** — proche de cp/rsync, facile à mémoriser
- **Chiffrement intégré** — GPG côté client ou SSE côté serveur
- **Idéal pour les scripts** — dry-run, output parseable, pas d'interaction

Pour la gestion des permissions et des clés AWS, pense à appliquer les bonnes pratiques de [sécurisation de ton serveur Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/) — les clés IAM méritent autant d'attention que les accès SSH.

- - - - - -

## Installation

### Ubuntu / Debian

```bash
sudo apt update && sudo apt install s3cmd
```

### Via pip (toutes plateformes, Python requis)

```bash
pip install s3cmd
```

### macOS (Homebrew)

```bash
brew install s3cmd
```

Vérifie l'installation :

```bash
s3cmd --version
```

- - - - - -

## Configuration

Lance l'assistant de configuration :

```bash
s3cmd --configure
```

Il te demande :

- **Access Key** et **Secret Key** (depuis IAM AWS ou ton service S3)
- **Default Region** — `us-east-1` pour AWS standard
- **S3 Endpoint** — laisser vide pour AWS, ou spécifier pour un service alternatif
- **Encryption passphrase** — pour le chiffrement GPG côté client

La configuration est sauvegardée dans `~/.s3cfg`.

### Exemple pour un service S3-compatible (ex. MinIO)

```bash
s3cmd --configure \
  --access_key=TON_ACCESS_KEY \
  --secret_key=TON_SECRET_KEY \
  --host=minio.ton-serveur.com \
  --host-bucket="%(bucket)s.minio.ton-serveur.com" \
  --no-ssl
```

Ou édite directement `~/.s3cfg` :

```ini
[default]
access_key = TON_ACCESS_KEY
secret_key = TON_SECRET_KEY
host_base = minio.ton-serveur.com
host_bucket = %(bucket)s.minio.ton-serveur.com
use_https = False
```

> ⚠️ **Sécurité :** Le fichier `~/.s3cfg` contient tes clés en clair. Assure-toi que seul ton utilisateur peut le lire : `chmod 600 ~/.s3cfg`.

- - - - - -

## Commandes essentielles

### Lister tes buckets et fichiers

```bash
# Lister tous les buckets
s3cmd ls

# Lister le contenu d'un bucket
s3cmd ls s3://mon-bucket/

# Lister récursivement
s3cmd ls --recursive s3://mon-bucket/
```

### Créer et supprimer un bucket

```bash
# Créer
s3cmd mb s3://mon-nouveau-bucket

# Supprimer (doit être vide)
s3cmd rb s3://mon-bucket-vide
```

### Uploader et télécharger

```bash
# Upload un fichier
s3cmd put fichier.txt s3://mon-bucket/

# Upload dans un sous-dossier
s3cmd put fichier.txt s3://mon-bucket/dossier/

# Télécharger un fichier
s3cmd get s3://mon-bucket/fichier.txt ./

# Upload récursif d'un dossier
s3cmd put --recursive /chemin/local/ s3://mon-bucket/dossier/
```

### Copier, déplacer, supprimer

```bash
# Copier entre buckets
s3cmd cp s3://bucket-source/fichier.txt s3://bucket-dest/

# Déplacer
s3cmd mv s3://mon-bucket/ancien.txt s3://mon-bucket/nouveau.txt

# Supprimer un fichier
s3cmd del s3://mon-bucket/fichier.txt

# Supprimer récursivement
s3cmd del --recursive s3://mon-bucket/dossier/
```

### Infos et taille

```bash
# Infos sur un objet (taille, hash, ACL...)
s3cmd info s3://mon-bucket/fichier.txt

# Taille totale d'un bucket
s3cmd du s3://mon-bucket/
```

- - - - - -

## Synchronisation et sauvegardes automatiques

### Sync de base

```bash
# Sync local → S3 (upload uniquement les nouveaux/modifiés)
s3cmd sync /chemin/local/ s3://mon-bucket/backup/

# Sync S3 → local (download)
s3cmd sync s3://mon-bucket/backup/ /chemin/local/

# Dry run (aperçu sans exécuter)
s3cmd sync --dry-run /chemin/local/ s3://mon-bucket/backup/

# Supprimer les fichiers supprimés en local
s3cmd sync --delete-removed /chemin/local/ s3://mon-bucket/backup/
```

### Automatiser avec cron

Ajoute dans `crontab -e` :

```bash
# Sauvegarde quotidienne à 2h du matin
0 2 * * * s3cmd sync /var/backups/ s3://mon-bucket/backups/ >> /var/log/s3backup.log 2>&1

# Sauvegarde dump MySQL + upload
0 3 * * * mysqldump -u root -p monpass ma_bdd > /tmp/dump.sql && s3cmd put /tmp/dump.sql s3://mon-bucket/dumps/dump-$(date +\%Y\%m\%d).sql
```

> 💡 **Astuce :** Utilise `--skip-existing` pour ignorer les fichiers déjà présents et accélérer les syncs sur de gros volumes.

Pour surveiller que tes syncs S3 tournent bien, [UptimeRobot](https://brandonvisca.com/uptimerobot-guide-complet-monitoring-infrastructure/) peut monitorer un endpoint ou un heartbeat déclenché en fin de script.

- - - - - -

## Sécurité et bonnes pratiques

### Chiffrement côté client (GPG)

```bash
# Upload chiffré
s3cmd put --encrypt fichier_sensible.sql s3://mon-bucket/

# Download + déchiffrement automatique
s3cmd get s3://mon-bucket/fichier_sensible.sql
```

### Chiffrement côté serveur (AWS SSE)

```bash
s3cmd put --server-side-encryption fichier.txt s3://mon-bucket/
```

### Utilise un fichier de config par projet

```bash
# Config dédiée pour un projet
s3cmd -c ~/.s3cfg-projet-client sync /data/ s3://bucket-client/
```

### Vérifie les permissions avant de mettre en prod

```bash
# Afficher les ACL d'un objet
s3cmd info s3://mon-bucket/fichier.txt | grep ACL
```

### Sauvegarde de configuration

Si tu gères plusieurs serveurs, la [gestion de sauvegardes multi-plateformes avec Vanderplanki](https://brandonvisca.com/vanderplanki-sauvegarde-emails-gratuit-multiplateforme/) peut compléter ta stratégie S3 pour d'autres types de données.

- - - - - -

## Conclusion

S3cmd fait le boulot sans fioriture : upload, sync, backup automatisé, chiffrement. C'est l'outil parfait pour intégrer S3 dans tes scripts cron ou tes pipelines de déploiement. Si tu bosses avec MinIO en self-hosted ou Backblaze B2 pour les coûts, ça marche pareil — change juste l'endpoint dans `~/.s3cfg`. La référence complète des commandes est dans la [documentation officielle S3cmd](https://s3tools.org/usage).

## Pour aller plus loin

- [Sécuriser son serveur Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/)
- [UptimeRobot : monitorer ton infrastructure](https://brandonvisca.com/uptimerobot-guide-complet-monitoring-infrastructure/)
- [Documentation officielle S3cmd](https://s3tools.org/usage)

## Articles connexes

- [Sendme CLI : Transfert Fichiers P2P en 2 Commandes (Alternative scp Moderne)](/sendme-cli-transfert-fichiers-p2p-terminal/)
- [Ubuntu Active Directory SSSD : intègre tes machines Linux en 5 étapes](/connecter-les-systemes-ubuntu-a-active-directory-en-utilisant-sssd/)
- [Dépannage montage RAID mdadm en mode secours Linux : wrong fs type et partition cachée](/depannage-montage-partition-raid-linux-mode-secours/)
- [DNS Scavenging Windows Server : automatiser le nettoyage DNS](/dns-scavenging-windows-server-guide-complet/)
