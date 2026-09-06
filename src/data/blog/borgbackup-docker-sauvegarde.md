---
title: "BorgBackup Docker : sauvegarde dédupliquée et chiffrée pour ton homelab"
description: "Guide borgbackup docker complet : déploie BorgBackup en conteneur pour des sauvegardes dédupliquées, compressées et chiffrées AES-256."
pubDatetime: "2026-08-08T08:00:00.000Z"
modDatetime: "2026-08-08T08:00:00.000Z"
author: Brandon
tags:
  - docker
  - auto-hebergement
  - sauvegarde
  - borgbackup
  - intermediaire
  - homelab
featured: false
draft: false
focusKeyword: borgbackup docker
faqs:
  - question: "Quelle est la différence entre BorgBackup et Duplicati ?"
    answer: "BorgBackup est un outil en ligne de commande axé sur la performance, la déduplication bloc à bloc et le chiffrement AES-256-CTR. Duplicati propose une interface web complète mais est plus lourd et moins performant sur les gros volumes."
  - question: "Puis-je stocker mes backups BorgBackup sur un NAS distant ?"
    answer: "Oui, BorgBackup supporte nativement SSH pour pousser les archives vers un NAS ou un serveur distant. Tu peux aussi monter un partage NFS/SMB et cibler un répertoire local."
  - question: "La déduplication BorgBackup fonctionne-t-elle entre plusieurs machines ?"
    answer: "Non, la déduplication est locale à chaque dépôt. Si tu sauvegardes plusieurs machines vers le même dépôt distant via SSH, chaque dépôt reste indépendant."
ogImage: ""
---
> 💡 **TL;DR**
> - BorgBackup crée des sauvegardes dédupliquées, compressées et chiffrées en AES-256
> - L'image Docker officielle `borgbackup/borg` te permet d'isoler l'outil sans polluer l'hôte
> - Stack Docker Compose prête à copier, avec montage des volumes et cron d'automatisation

## Table des matières

## Pourquoi choisir BorgBackup dans ton homelab ?

Tu as déjà testé Duplicati, peut-être même joué avec rsync et des scripts maison. Mais quand tes volumes Docker commencent à peser plusieurs centaines de gigaoctets, tu remarques vite que la bande passante et l'espace disque deviennent des problèmes réels. BorgBackup est un outil de sauvegarde écrit en Python qui résout ces deux problèmes d'une manière brutalement efficace : la **déduplication bloc à bloc**, la **compression** et le **chiffrement** intégré.

Le projet vit sur GitHub sous `borgbackup/borg` avec plus de 11 000 stars et une maintenance active. La dernière version stable au moment où j'écris ces lignes est la 1.4.x, avec un support étendu sur plusieurs années. C'est un outil que tu peux installer sur n'importe quel système Linux, mais pour un homelab Dockerisé, l'image officielle `borgbackup/borg` est le choix le plus propre.

Ce qui distingue BorgBackup des solutions comme [Duplicati](/duplicati-docker-sauvegarde/) ou rsync, c'est la déduplication par défaut. Si tu as un fichier de 10 Go que tu modifies de 1 Mo, BorgBackup ne stocke que ce 1 Mo supplémentaire. Pas de recopie intégrale. Pas de stockage de versions entières à chaque backup. Le résultat : un ratio de compression souvent supérieur à 5:1 sur des données textuelles ou de code source. Pour des données multimédias, la compression est moins agressive mais la déduplication reste pertinente.

Contrairement à [Duplicati](/duplicati-docker-sauvegarde/) qui mise tout sur son interface web, BorgBackup est un outil en ligne de commande. Cela signifie moins de surface d'attaque, moins de dépendances, et une exécution scriptable dans n'importe quel pipeline CI/CD ou cron. Si tu cherches une solution sans interface graphique, rapide, et qui consomme peu de ressources, BorgBackup est probablement le meilleur choix pour ton stack Docker.

## BorgBackup vs les alternatives : le match

|| Outil | Déduplication | Chiffrement | Interface | Docker | Compétence |
||-------|---------------|-------------|-----------|--------|------------|
|| **BorgBackup** | Bloc à bloc, locale | AES-256-CTR | CLI | `borgbackup/borg` | Intermédiaire |
|| **Duplicati** | Bloc, variable | AES-256 | Web UI complète | `duplicati/duplicati` | Débutant |
|| **Restic** | Bloc à bloc | AES-256-GCM | CLI + scripts | `restic/restic` | Avancée |
|| **Kopia** | Bloc à bloc | AES-256-GCM | CLI + UI optionnelle | `kopia/kopia` | Intermédiaire |
|| **rsync** | Aucune | Aucun | Aucune | Non (natif) | Avancée |

Mon verdict pour un homelab Dockerisé : **BorgBackup** si tu veux de la performance brute avec un minimum de complexité. Duplicati reste pertinent pour ceux qui préfèrent cliquer. Restic est excellent mais sa syntaxe et son écosystème sont plus verbeux. Si tu cherches une alternative plus moderne et performante avec une déduplication avancée et un chiffrement robuste, [Restic avec Docker](/restic-docker-sauvegarde-moderne/) mérite sérieusement ton attention. rsync n'est pas un système de backup : zéro versioning, zéro chiffrement, zéro compression native.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose installés
- Un dossier source contenant tes données à sauvegarder (volumes Docker, dossiers hôte, bases de données)
- Une destination de stockage : répertoire local, NAS, ou serveur distant en SSH
- Un mot de passe solide pour le chiffrement (stocke-le dans ton gestionnaire de mots de passe)

## Installation avec Docker Compose

Crée un dossier dédié et le fichier `docker-compose.yml` :

```yaml
services:
  borgbackup:
    image: borgbackup/borg:1.4
    container_name: borgbackup
    restart: unless-stopped
    environment:
      - BORG_PASSPHRASE=change_moi_maintenant_avec_un_truc_long
      - BORG_REPO=/backups/repo
      - TZ=Europe/Paris
    volumes:
      - ./repo:/backups/repo
      - /path/to/your/data:/source/data:ro
      - /var/lib/docker/volumes:/source/docker-volumes:ro
    entrypoint: ["sh", "-c", "while true; do sleep 3600; done"]
```

Quelques précisions essentielles :

- `BORG_PASSPHRASE` : définit la clé de chiffrement. Si tu perds cette passphrase, tu perds tes backups. Point final. Mets-la dans ton [Vaultwarden](/vaultwarden-docker-gestionnaire-mots-de-passe/).
- `BORG_REPO` : chemin vers le dépôt de sauvegarde à l'intérieur du conteneur.
- `/source/data` : monte en lecture seule (`:ro`) les dossiers à sauvegarder.
- `/source/docker-volumes` : astuce utile pour sauvegarder les volumes nommés Docker.
- L'entrypoint `while true; do sleep 3600; done` maintient le conteneur actif en permanence pour exécuter des commandes via `docker exec`.

Lance le conteneur :

```bash
cd /opt/borgbackup && docker compose up -d
```

## Initialiser le dépôt de sauvegarde

Avant de pouvoir sauvegarder, tu dois initialiser le dépôt. Cette opération se fait une seule fois :

```bash
docker exec -e BORG_PASSPHRASE="change_moi_maintenant_avec_un_truc_long" \
  borgbackup borg init --encryption=repokey-blake2 /backups/repo
```

L'option `--encryption=repokey-blake2` est le choix recommandé : la clé de chiffrement est stockée dans le dépôt (chiffrée par la passphrase), ce qui te permet de restaurer depuis n'importe quelle machine disposant de BorgBackup et de la passphrase. Les algorithmes Blake2 sont plus rapides que les SHA-256 classiques sur les architectures modernes.

Vérifie que le dépôt est initialisé :

```bash
docker exec -e BORG_PASSPHRASE="change_moi_maintenant_avec_un_truc_long" \
  borgbackup borg info /backups/repo
```

Tu dois voir apparaître des informations sur le dépôt, notamment le type de chiffrement et la taille.

## Créer une sauvegarde manuelle

Crée ton premier backup avec une commande simple :

```bash
docker exec -e BORG_PASSPHRASE="change_moi_maintenant_avec_un_truc_long" \
  borgbackup borg create --compression zstd,5 \
  /backups/repo::backup-$(date +%Y%m%d-%H%M%S) \
  /source/data /source/docker-volumes
```

Explication des options :

- `--compression zstd,5` : utilise l'algorithme Zstandard au niveau 5. C'est un excellent compromis entre vitesse et taux de compression. Pour des données déjà compressées (vidéos, images), tu peux passer à `--compression none`.
- `/backups/repo::backup-...` : syntaxe BorgBackup pour nommer l'archive. Le double deux-points sépare le dépôt du nom d'archive.
- `/source/data /source/docker-volumes` : chemins source à sauvegarder.

Le premier backup prendra le plus de temps car BorgBackup doit indexer tous les blocs. Les suivants serent incrémentaux et quasi instantanés si peu de données ont changé.

## Lister et vérifier les archives

Pour voir l'historique de tes sauvegardes :

```bash
docker exec -e BORG_PASSPHRASE="change_moi_maintenant_avec_un_truc_long" \
  borgbackup borg list /backups/repo
```

Pour vérifier l'intégrité d'une archive spécifique :

```bash
docker exec -e BORG_PASSPHRASE="change_moi_maintenant_avec_un_truc_long" \
  borgbackup borg check /backups/repo
```

La commande `check` est indispensable à exécuter régulièrement. Elle vérifie la cohérence du dépôt et détecte d'éventuelles corruptions. Sur un gros dépôt, cette opération peut être longue ; exécule-la pendant les heures creuses.

## Restaurer des fichiers ou un volume complet

La restauration est un point fort de BorgBackup. Tu peux extraire un fichier unique, un répertoire, ou tout le contenu d'une archive.

Extraire un fichier spécifique dans `/tmp/restore` :

```bash
docker exec -e BORG_PASSPHRASE="change_moi_maintenant_avec_un_truc_long" \
  borgbackup borg extract /backups/repo::backup-20260808-080000 \
  source/data/monfichier.txt --stdout > /tmp/monfichier.txt
```

Restaurer un répertoire complet vers un volume Docker :

```bash
docker exec -e BORG_PASSPHRASE="change_moi_maintenant_avec_un_truc_long" \
  borgbackup borg extract /backups/repo::backup-20260808-080000 \
  source/docker-volumes/nextcloud_data
```

Pour une restauration complète vers un point de montage propre, crée un répertoire temporaire dans le conteneur et extrais-y l'archive entière :

```bash
docker exec -e BORG_PASSPHRASE="change_moi_maintenant_avec_un_truc_long" \
  borgbackup sh -c "mkdir -p /tmp/restore && cd /tmp/restore && borg extract /backups/repo::backup-20260808-080000"
```

BorgBackup préserve les permissions, les attributs étendus et les ACLs lors de l'extraction. C'est un détail crucial quand tu restaures des volumes Docker avec des permissions spécifiques.

## Automatiser avec un cron Dockerisé

Personne ne lance ses backups à la main tous les jours. Le moyen le plus simple d'automatiser BorgBackup dans un environnement Docker est d'ajouter un conteneur cron dédié ou d'utiliser le système cron de l'hôte avec `docker exec`.

Solution recommandée : un conteneur `mazzolino/borgmatic` ou un cron sur l'hôte. Voici l'approche cron native, la plus transparente :

Edite la crontab de l'utilisateur root (nécessaire pour accéder à `/var/lib/docker/volumes`) :

```bash
sudo crontab -e
```

Ajoute cette ligne pour un backup quotidien à 3h du matin :

```bash
0 3 * * * /usr/bin/docker exec -e BORG_PASSPHRASE="change_moi_maintenant_avec_un_truc_long" borgbackup borg create --compression zstd,5 /backups/repo::backup-$(date +\%Y\%m\%d-\%H\%M\%S) /source/data /source/docker-volumes >> /var/log/borgbackup.log 2>&1
```

Puis une ligne pour le nettoyage automatique des vieilles archives, à 4h du matin :

```bash
0 4 * * * /usr/bin/docker exec -e BORG_PASSPHRASE="change_moi_maintenant_avec_un_truc_long" borgbackup borg prune --keep-daily=7 --keep-weekly=4 --keep-monthly=12 /backups/repo >> /var/log/borgbackup-prune.log 2>&1
```

La commande `borg prune` supprime les archives selon une politique de rétention. Ici, on garde :
- les 7 derniers jours
- les 4 dernières semaines
- les 12 derniers mois

C'est une stratégie classique qui équilibre granularité et économie d'espace.

## Sauvegarder vers un serveur distant en SSH

Un backup local est un bon début, mais la règle d'or du 3-2-1 veut qu'une copie soit hors site. BorgBackup supporte nativement SSH pour pousser les archives vers un serveur distant.

Sur ton serveur distant, initialise un dépôt :

```bash
ssh user@backup-server "mkdir -p /backups/borg && docker run --rm -v /backups/borg:/backups/repo -e BORG_PASSPHRASE=ton_passphrase borgbackup/borg:1.4 borg init --encryption=repokey-blake2 /backups/repo"
```

Depuis ton homelab, crée un backup distant en montant la connexion SSH via un volume. Plus simplement, utilise l'image BorgBackup avec la syntaxe SSH intégrée :

```bash
docker exec -e BORG_PASSPHRASE="change_moi_maintenant_avec_un_truc_long" \
  borgbackup borg create --compression zstd,5 \
  ssh://user@backup-server/~/backups/borg::backup-$(date +%Y%m%d-%H%M%S) \
  /source/data /source/docker-volumes
```

Pour que cela fonctionne, le conteneur doit avoir accès à tes clés SSH. Monte ton `~/.ssh` dans le conteneur :

```yaml
volumes:
  - ~/.ssh:/root/.ssh:ro
```

Si tu préfères héberger toi-même un stockage S3-compatible pour diversifier tes destinations, j'ai détaillé le déploiement de [MinIO avec Docker](/minio-docker-stockage-objet-s3/). MinIO n'est pas natively compatible avec BorgBackup (qui préfère SSH ou le système de fichiers), mais c'est une excellente destination pour d'autres outils de ton stack.

## Surveiller l'espace disque et l'intégrité

Avec le temps, même une déduplication efficace finit par consommer de l'espace. Voici les commandes utiles pour garder un œil sur la santé de ton dépôt.

Voir l'espace utilisé par le dépôt :

```bash
docker exec -e BORG_PASSPHRASE="change_moi_maintenant_avec_un_truc_long" \
  borgbackup borg info /backups/repo
```

La sortie affiche `Deduplicated size`, qui est la taille réellement occupée sur disque après déduplication et compression. Compare cette valeur à la taille totale de tes sources : le ratio te donne une idée de l'efficacité.

Voir l'espace consommé par chaque archive individuellement :

```bash
docker exec -e BORG_PASSPHRASE="change_moi_maintenant_avec_un_truc_long" \
  borgbackup borg info /backups/repo::backup-20260808-080000
```

Cette commande affiche la taille "originale" (données brutes), la taille "compressée", et la taille "dédupliquée" pour cette archive spécifique. C'est l'indicateur le plus fiable de l'efficacité de ta stratégie de compression.

## Dépannage : les erreurs courantes

**"Passphrase is wrong"** : vérifie que la variable `BORG_PASSPHRASE` est bien passée à `docker exec`. Un espace ou une quote mal placée suffit à tout casser.

**"Repository path does not exist"** : le chemin du dépôt doit exister avant d'exécuter `borg init`. Crée le répertoire avec `mkdir -p` ou monte un volume existant.

**"No space left on device"** : BorgBackup ne supprime pas automatiquement les vieilles archives. Il faut explicitement lancer `borg prune` ou un script équivalent.

**"Corrupted segment reference"** : exécute `borg check --repair /backups/repo`. Attention, `--repair` peut supprimer des données corrompées irrémédiablement. Garde toujours un backup de ton backup pour les données critiques.

**"Resource temporarily unavailable"** : si tu lances plusieurs backups simultanés sur le même dépôt, BorgBackup verrouille le dépôt. Un seul processus à la fois. Utilise des dépôts séparés pour des parallélisations nécessaires.

## Astuces pour optimiser la vitesse et la compression

1. **Choisir le bon algorithme de compression** : `zstd` est le plus rapide avec un bon ratio. `lz4` est encore plus rapide mais compresse moins. `zlib` est lent mais optimal pour du texte pur.
2. **Exclure les fichiers inutiles** : utilise `--exclude` pour ignorer les caches, les logs et les fichiers temporaires. Exemple : `--exclude '/source/data/*/cache/*'`.
3. **Segmenter les backups** : si tu as 2 To de données, ne les mets pas toutes dans une seule archive. Crée des archives par service (nextcloud, vaultwarden, databases) pour accélérer la restauration ciblée.
4. **SSD pour le dépôt** : les opérations de déduplication sont I/O intensives. Un dépôt sur SSD (ou NVMe) est nettement plus rapide qu'un dépôt sur disque mécanique, surtout pour les backups incrémentaux.
5. **Monter avec `noatime`** : si ton dépôt est sur un système de fichiers dédié, monte-le avec `noatime` pour réduire les écritures inutiles.

## Conclusion

BorgBackup est un outil de sauvegarde qui ne fait pas de cadeaux : pas d'interface web, pas de notifications push, pas de boutons glossy. Mais ce qu'il fait, il le fait mieux que quasiment tout le marché. La déduplication bloc à bloc, le chiffrement AES-256-CTR et la compression Zstandard en font le compagnon idéal d'un homelab Dockerisé sérieux.

Dans mon [guide auto-hébergement complet](/auto-hebergement-guide-complet-2025/), je martèle une évidence : un service sans backup est un service jetable. Avec BorgBackup en Docker, tu transformes ce jetable en pérenne. Déploie-le cette semaine, teste une restauration, et dors tranquille.
