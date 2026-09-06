---
title: "Restic Docker : sauvegarde moderne vers S3 et plus"
description: "Guide complet restic docker : sauvegarde tes conteneurs avec déduplication, chiffrement AES-256, stockage S3 et cron automatisé."
pubDatetime: "2026-08-10T08:00:00.000Z"
modDatetime: "2026-08-10T08:00:00.000Z"
author: Brandon Visca
tags:
  - intermediaire
  - auto-hebergement
  - docker
  - restic
  - sauvegarde
featured: false
draft: false
focusKeyword: restic docker
ogImage: ""
---
> 💡 **TL;DR**
> - Restic est un client de sauvegarde en Go qui déduplique, chiffre et envoie tes backups vers S3, B2, Azure ou SFTP sans serveur distant
> - Un seul conteneur Docker suffit : initialisation du repo, backup incrémental, gestion de snapshots et nettoyage automatique
> - Stack Docker Compose complète avec cron intégré pour des backups quotidiens sans intervention

## Table des matières

## Pourquoi Restic et pas rsync ou tar ?

Tu as probablement déjà écrit un script shell qui fait `tar czvf` suivi d'un `rsync -avz` vers un NAS. Ça marche. Jusqu'au jour où ton volume pèse 500 Go, que la bande passante sature, et que tu découvres que tes backups prennent trois fois la taille originale parce que chaque archive contient l'intégralité des fichiers.

Restic change la donne. C'est un outil de sauvegarde écrit en Go, distribué sous licence BSD-2-Clause, avec plus de 26 000 stars sur GitHub (`restic/restic`). La version stable actuelle est la v0.19.1 (juillet 2026). Pas de serveur à installer. Pas de base de données. Juste un binaire qui parle HTTP(S) vers ton stockage.

La magie de Restic repose sur trois piliers :

- **Déduplication par chunking** : les fichiers sont découpés en blocs de contenu. Si tu modifies un seul octet d'un fichier de 10 Go, Restic ne stocke que ce bloc modifié. Pas le fichier entier. Pas l'archive complète. Le ratio de compression peut atteindre 10:1 sur des données de code source ou textuelles.
- **Chiffrement AES-256-GCM** : tout est chiffré localement avant l'envoi. Ton mot de passe est la seule clé. Même si ton bucket S3 se fait compromis, les données sont illisibles.
- **Multi-backend natif** : S3, MinIO, Backblaze B2, Wasabi, Azure Blob, Google Cloud Storage, SFTP, REST, et même disque local. Tu changes de fournisseur en modifiant une URL, pas en réinstallant quoi que ce soit.

Contrairement à [BorgBackup](/borgbackup-docker-sauvegarde/) qui nécessite un serveur distant avec SSH et un accès spécifique au système de fichiers, Restic est **client-only**. Tu initialises un repo sur n'importe quel stockage compatible S3, tu pousses tes backups, et tu peux les restaurer depuis n'importe quelle machine disposant du mot de passe. Si tu cherches une alternative plus légère et moderne que BorgBackup, Restic est probablement le meilleur choix pour un homelab Dockerisé.

Et si tu héberges déjà ton propre stockage S3 avec [MinIO](/minio-docker-stockage-objet-s3/), la combinaison Restic + MinIO te donne une solution de backup complètement auto-hébergée, chiffrée et dédupliquée, sans dépendre d'aucun cloud tiers.

## Restic vs les alternatives : le comparatif réaliste

|| Outil | Déduplication | Chiffrement | Mode | Serveur requis | Docker | Compétence |
||-------|---------------|-------------|------|----------------|--------|------------|
|| **Restic** | Chunking bloc | AES-256-GCM | Client-only | Non | `restic/restic` | Intermédiaire |
|| **BorgBackup** | Bloc à bloc | AES-256-CTR | Client-serveur | Oui (SSH) | `borgbackup/borg` | Avancée |
|| **Duplicati** | Bloc variable | AES-256 | Client + Web UI | Non | `duplicati/duplicati` | Débutant |
|| **Kopia** | Chunking | AES-256-GCM | Client + UI optionnelle | Non | `kopia/kopia` | Intermédiaire |
|| **rsync + tar** | Aucune | Aucun | Client | Non | Non | Avancée |

Restic se situe dans le sweet spot : plus rapide et moderne que Duplicati sur les gros volumes, plus simple à déployer que BorgBackup (pas de SSH, pas de permissions distantes), et infiniment plus intelligent que rsync. [Duplicati](/duplicati-docker-sauvegarde/) reste la meilleure option si tu veux une interface web sans toucher à la ligne de commande. Mais si tu es à l'aise avec quelques commandes et que tu veux la meilleure performance, Restic est le roi.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose installés
- Une destination de stockage : compte S3 (AWS, Wasabi, Scaleway), bucket Backblaze B2, ou [MinIO auto-hébergé](/minio-docker-stockage-objet-s3/)
- Les identifiants d'accès (clé d'accès + clé secrète pour S3, ou mot de passe pour SFTP)
- Un mot de passe fort pour chiffrer le repo Restic (garde-le dans ton gestionnaire de mots de passe)

## Architecture et concepts clés

Avant de copier le Docker Compose, il faut comprendre comment Restic organise ses données :

**Repository** : c'est le conteneur logique sur ton stockage distant (S3 bucket, répertoire SFTP, etc.). Un repo contient toutes les snapshots, les chunks dédupliqués et les index. Tu initialises un repo une seule fois avec `restic init`.

**Snapshot** : une version point-in-time de tes données. Chaque exécution de `restic backup` crée un snapshot. Les snapshots partagent les chunks identiques grâce à la déduplication. Supprimer un snapshot ne supprime pas les chunks utilisés par d'autres snapshots.

**Chunk** : un bloc de contenu haché (SHA-256). La déduplication fonctionne au niveau des chunks, pas des fichiers. Si deux fichiers contiennent les mêmes données, elles ne sont stockées qu'une fois.

**Forget + Prune** : `restic forget` supprime les snapshots selon une politique de rétention (garder 7 quotidiens, 4 hebdomadaires, 12 mensuels). `restic prune` supprime les chunks orphelins pour récupérer l'espace. Ces deux commandes sont essentielles pour éviter que ton repo n'explose.

## Déploiement Docker Compose

Voici une stack complète qui tourne Restic dans un conteneur, avec un cron quotidien pour automatiser les backups.

Crée un dossier `~/restic-backup` et un fichier `docker-compose.yml` :

```yaml
version: "3.8"

services:
  restic:
    image: restic/restic:0.19.1
    container_name: restic-backup
    environment:
      # Backend S3 (adapter selon ton fournisseur)
      RESTIC_REPOSITORY: "s3:https://s3.fr-par.scw.cloud/backup-homelab"
      AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
      AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
      # Mot de passe de chiffrement du repo (OBLIGATOIRE)
      RESTIC_PASSWORD: "${RESTIC_PASSWORD}"
      # Options pour le cron
      BACKUP_CRON: "0 3 * * *"
      BACKUP_RETENTION_DAYS: "7"
      BACKUP_RETENTION_WEEKS: "4"
      BACKUP_RETENTION_MONTHS: "12"
    volumes:
      # Données à sauvegarder (adapter selon ton homelab)
      - /var/lib/docker/volumes:/data/docker-volumes:ro
      - /opt/homelab:/data/homelab:ro
      - /etc:/data/etc:ro
      # Cache Restic pour accélérer les backups incrémentaux
      - restic-cache:/cache
    command:
      - /bin/sh
      - -c
      - |
        # Initialisation du repo si nécessaire
        restic init || echo "Repo déjà initialisé"
        # Configuration du cron
        echo "$$BACKUP_CRON restic backup /data --exclude-if-present .nobackup --tag docker-daily && restic forget --keep-daily $$BACKUP_RETENTION_DAYS --keep-weekly $$BACKUP_RETENTION_WEEKS --keep-monthly $$BACKUP_RETENTION_MONTHS --prune" | crontab -
        # Lancement du daemon cron
        crond -f -l 2
    restart: unless-stopped

volumes:
  restic-cache:
```

Et le fichier `.env` associé :

```bash
# Fournisseur S3 (Scaleway, AWS, Wasabi, MinIO...)
AWS_ACCESS_KEY_ID=SCWXXXXXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
RESTIC_PASSWORD=un-mot-de-passe-tres-fort-de-32-caracteres!
```

Déploie la stack :

```bash
cd ~/restic-backup
docker compose up -d
```

Le conteneur va initialiser le repo Restic au premier démarrage, puis configurer un cron qui lance un backup tous les jours à 3h du matin. Les tags `--exclude-if-present .nobackup` permettent d'ignorer les dossiers contenant un fichier `.nobackup` (utile pour les caches et logs).

## Vérifier que ça marche

### Premier backup manuel

Si tu veux tester avant d'attendre le cron :

```bash
docker exec -it restic-backup restic backup /data --tag test-manuel
```

Restic va scanner tes données, calculer les chunks, dédupliquer, chiffrer et pousser vers S3. Le premier backup est forcément long (tout est nouveau). Les suivants sont quasi instantanés sur les fichiers inchangés.

### Lister les snapshots

```bash
docker exec -it restic-backup restic snapshots
```

Tu verras quelque chose comme :

```bash
ID        Time                 Host        Tags           Paths
------------------------------------------------------------------
3a21f8b2  2026-08-10 03:00:01  restic      docker-daily   /data
9c7e4d51  2026-08-09 03:00:02  restic      docker-daily   /data
```

### Vérifier l'intégrité du repo

```bash
docker exec -it restic-backup restic check
```

Cette commande vérifie que tous les chunks sont accessibles et que les index sont cohérents. Lance-la une fois par mois.

### Restaurer un fichier ou un dossier

```bash
# Restaurer un dossier spécifique depuis le dernier snapshot
docker exec -it restic-backup restic restore latest --target /tmp/restore --include /data/homelab/nextcloud

# Ou restaurer depuis un snapshot précis
docker exec -it restic-backup restic restore 3a21f8b2 --target /tmp/restore --include /data/docker-volumes
```

Restic restaure en conservant les permissions et les horodatages originaux. Tu peux copier les fichiers restaurés vers leur emplacement définitif avec un simple `cp -a`.

### Monter un snapshot (accès direct aux fichiers)

Restic peut monter un repo en FUSE pour naviguer dans les snapshots comme dans un filesystem :

```bash
docker exec --privileged -it restic-backup restic mount /mnt
# Depuis un autre terminal
docker exec -it restic-backup ls /mnt/snapshots/latest/data/
```

C'est particulièrement pratique pour récupérer un seul fichier sans extraire tout un snapshot.

## Politique de rétention et nettoyage automatique

Sans rétention, ton repo grandit indéfiniment. La commande `forget` avec `--prune` est ton ami.

Le cron dans le Docker Compose ci-dessus exécute automatiquement :

```bash
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 12 --prune
```

Ce qui signifie : garder les 7 derniers backups quotidiens, les 4 derniers hebdomadaires (un par semaine), et les 12 derniers mensuels (un par mois). Le reste est supprimé, et `prune` nettoie les chunks orphelins.

Tu peux vérifier ce qui serait supprimé avant d'exécuter pour de vrai :

```bash
docker exec -it restic-backup restic forget --keep-daily 7 --keep-weekly 4 --dry-run
```

## Utiliser Restic avec MinIO (S3 local)

Si tu as déployé [MinIO avec Docker](/minio-docker-stockage-objet-s3/), tu peux utiliser Restic vers ton propre serveur S3 sans sortir de ton réseau local. C'est la configuration que j'utilise en production pour mes backups sensibles.

Modifie simplement l'URL du repo dans le Docker Compose :

```yaml
environment:
  RESTIC_REPOSITORY: "s3:http://minio:9000/backup-restic"
  AWS_ACCESS_KEY_ID: "${MINIO_ACCESS_KEY}"
  AWS_SECRET_ACCESS_KEY: "${MINIO_SECRET_KEY}"
  RESTIC_PASSWORD: "${RESTIC_PASSWORD}"
```

Et ajoute le réseau Docker si MinIO tourne dans une stack séparée :

```yaml
networks:
  default:
    external: true
    name: homelab
```

Avantage majeur : tes backups ne quittent jamais ton infrastructure. Tu gardes le contrôle total des données, la latence est minimale, et tu n'es dépendant d'aucun fournisseur externe.

## Sauvegarde de bases de données (MariaDB, PostgreSQL)

Pour sauvegarder une base de données, le plus robuste est de dumper SQL avant de le passer à Restic. Tu peux ajouter un service de dump dans ton Docker Compose :

```yaml
services:
  db-dump:
    image: mariadb:11
    container_name: db-dump
    environment:
      MYSQL_PWD: "${DB_ROOT_PASSWORD}"
    volumes:
      - /opt/restic-dumps:/dumps
    command:
      - /bin/sh
      - -c
      - |
        echo "0 2 * * * mysqldump -h mariadb -u root --all-databases > /dumps/mariadb-$$(date +\%Y\%m\%d).sql && find /dumps -name '*.sql' -mtime +7 -delete" | crontab -
        crond -f -l 2
    restart: unless-stopped
```

Ensuite, inclue `/dumps` dans les chemins que Restic sauvegarde. Restic déduplique très bien les dumps SQL incrémentaux (seules les lignes modifiées génèrent de nouveaux chunks).

Pour PostgreSQL, remplace `mysqldump` par `pg_dumpall -h postgres -U postgres`.

## Monitoring et alertes

Restic ne notifie pas en cas d'échec. Il faut le lui apprendre. Le moyen le plus simple est d'envoyer les logs vers un service de monitoring.

Avec le Docker Compose de base, les logs sont envoyés sur stdout. Tu peux les récupérer avec :

```bash
docker logs --tail 100 restic-backup
```

Pour une solution plus robuste, ajoute un conteneur sidecar qui surveille les logs et envoie une alerte en cas d'erreur. Ou utilise simplement `curl` vers un webhook dans le cron :

```bash
restic backup /data --tag docker-daily && curl -fsS -m 10 --retry 5 -o /dev/null "https://healthchecks.io/ping/ton-uuid" || curl -fsS -m 10 --retry 5 --data "Restic backup failed" "https://ntfy.sh/ton-topic"
```

## Sécurité : les bonnes pratiques

Le chiffrement Restic est solide (AES-256-GCM), mais la sécurité globale dépend de toi :

- **Le mot de passe RESTIC_PASSWORD** est la clé de tout. Perds-le, et tes backups sont définitivement inaccessibles. Stocke-le dans ton gestionnaire de mots de passe, et garde une copie hors ligne (CleverCrypt, KeePassXC sur une clé USB chiffrée).
- **Ne jamais versionner `.env`** : ajoute `.env` dans ton `.gitignore`. Même règle pour `docker-compose.yml` s'il contient des secrets en dur.
- **Permissions S3 restrictives** : crée un utilisateur IAM dédié pour Restic avec accès en écriture seule sur le bucket de backup. Pas de lecture sur les autres buckets, pas de suppression (sauf si tu veux pouvoir faire du prune depuis la machine de backup).
- **Repo sur disque local** : si tu backups vers un disque USB local, chiffre-le avec LUKS. Un disque non chiffré volé = toutes tes données en clair.
- **Teste tes restaurations** : un backup non testé n'est qu'une promesse. Restaure un fichier par semaine pour vérifier que tout fonctionne.

## Dépannage des erreurs courantes

### "Fatal: wrong password or no key found"
Tu as saisi un mauvais mot de passe, ou le repo n'est pas initialisé. Vérifie `RESTIC_PASSWORD` et relance `restic init`.

### "The AWS Access Key Id you provided does not exist in our records"
Vérifie tes credentials S3. Sur Scaleway, les clés API ne sont pas des clés IAM : il faut utiliser les clés de l'espace de stockage (Object Storage).

### "Fatal: unable to open config file: blob is not available"
Le repo est corrompu ou inaccessible. Vérifie la connectivité réseau et l'intégrité du bucket avec `restic check --read-data`.

### "no space left on device" sur le cache
Restic utilise un cache local pour accélérer les opérations. Par défaut, il est dans `/root/.cache/restic`. Monte un volume Docker pour le cache comme dans l'exemple ci-dessus, ou nettoie régulièrement avec `restic cache --cleanup`.

### Le backup est lent sur S3
Vérifie que le cache est bien monté. Sans cache, Restic doit télécharger les index à chaque exécution. Utilise aussi `--limit-upload` si ta bande passante montante est faible.

## Pour aller plus loin

Restic est un outil extrêmement complet. Quelques commandes utiles pour creuser :

```bash
# Voir les différences entre deux snapshots
docker exec -it restic-backup restic diff 3a21f8b2 9c7e4d51

# Lister les fichiers d'un snapshot
docker exec -it restic-backup restic ls 3a21f8b2

# Rechercher un fichier dans tous les snapshots
docker exec -it restic-backup restic find "important.sql"

# Stats du repo
docker exec -it restic-backup restic stats

# Dédupliquer un repo (supprime les doublons internes)
docker exec -it restic-backup restic prune --max-repack-size 1G
```

La documentation officielle sur [restic.readthedocs.io](https://restic.readthedocs.io/) est excellente et à jour. Le projet est actif, les releases sortent régulièrement, et la communauté est réactive sur GitHub Discussions.

Restic est le choix idéal si tu veux un système de backup moderne, rapide, chiffré et complètement contrôlable. Combine-le avec [MinIO](/minio-docker-stockage-objet-s3/) pour une solution 100 % auto-hébergée, ou pousse vers le cloud de ton choix sans changer une ligne de ton workflow. Le principal travail consiste à bien choisir son mot de passe, à tester ses restaurations régulièrement, et à ne jamais croire qu'un backup non vérifié est un backup valide. Ton homelab mérite une sauvegarde à la hauteur de ses services.
