---
title: "Kopia Docker : sauvegardes chiffrées et dédupliquées avec interface web"
description: Déploie Kopia Docker pour des sauvegardes chiffrées et dédupliquées, avec interface web KopiaUI, politiques de rétention automatiques.
pubDatetime: "2026-11-12T11:00:44+01:00"
modDatetime: "2026-11-11T08:00:00.000Z"
author: Brandon
tags:
  - securite
  - sauvegarde
  - stockage
  - intermediaire
featured: false
draft: false
focusKeyword: kopia docker
faqs:
  - question: "Que se passe-t-il si je perds le mot de passe de mon dépôt Kopia ?"
    answer: "Rien ne peut le récupérer. Le chiffrement est fait côté client avec AES256_GCM, sans porte dérobée : sans mot de passe, le dépôt entier est illisible pour toujours."
  - question: "Quelle est la différence entre Kopia et Restic ?"
    answer: "Les deux chiffrent en AES-256-GCM et dédupliquent par blocs, mais Kopia ajoute une interface web native (KopiaUI) et un mode serveur, alors que Restic reste purement CLI."
  - question: "Kopia docker consomme-t-il beaucoup de RAM pendant un snapshot ?"
    answer: "Le découpage en blocs et le calcul de hash sont gourmands en CPU sur de gros volumes, mais la RAM reste raisonnable, quelques centaines de Mo suffisent dans la majorité des cas."
---
> 💡 **TL;DR**
> - Kopia docker chiffre tes sauvegardes côté client en AES256_GCM et déduplique par blocs, avec une interface web KopiaUI incluse
> - L'image officielle `kopia/kopia` tourne en mode serveur sur le port 51515, repository local, NAS, S3, B2 ou Azure
> - Licence Apache 2.0, gratuit, dernière version stable 0.23.x, policies de rétention et planification intégrées

## Kopia Docker : la sauvegarde chiffrée qui ne te demande pas de choisir entre CLI et interface web

Tu gères déjà quelques conteneurs critiques chez toi et tu te poses la question que tout le monde se pose trop tard : qu'est-ce qui se passe si le disque lâche demain. Si t'as déjà creusé le sujet, tu es tombé sur rsync, Duplicati, BorgBackup, Restic, et maintenant Kopia. Chez moi, c'est Kopia qui a fini par gagner sa place, pour une raison simple : il fait tout ce que fait Restic côté chiffrement et déduplication, mais il ajoute une vraie interface web sans sacrifier le mode CLI pur pour les scripts. Deux usages, un seul outil.

On va voir comment déployer Kopia docker proprement, créer ton premier dépôt chiffré, configurer les politiques de rétention, et comparer honnêtement avec les alternatives que tu as peut-être déjà en tête.

## Table des matières

## Qu'est-ce que Kopia et pourquoi l'utiliser en Docker

Kopia est un outil de sauvegarde multiplateforme maintenu sur GitHub sous `kopia/kopia`, sous licence Apache 2.0. Gratuit, open source, et activement développé : la dernière version stable au moment où j'écris ces lignes est la 0.23.x. Deux interfaces cohabitent : un binaire CLI pur pour scripter tes backups en cron, et KopiaUI, une interface graphique (et un mode serveur web) pour ceux qui préfèrent cliquer plutôt que taper des commandes.

Techniquement, Kopia repose sur trois piliers :

- **Déduplication par blocs** : les fichiers sont découpés en morceaux de taille variable (content-defined chunking), et seuls les blocs réellement nouveaux sont stockés. Un fichier de 20 Go modifié de 50 Mo ne coûte que 50 Mo de stockage supplémentaire.
- **Chiffrement côté client en AES256_GCM** : le chiffrement et l'authentification se font avant l'envoi vers le stockage distant. La clé dérive de ton mot de passe de dépôt via scrypt. Le stockage distant ne voit jamais tes données en clair, même s'il s'agit d'un bucket S3 que tu ne contrôles pas entièrement.
- **Compression intégrée**, configurable par politique, avec exclusion possible de certaines extensions déjà compressées (vidéos, archives).

Côté backends supportés, Kopia est particulièrement flexible : stockage local ou NAS, Amazon S3 (et compatibles S3), Azure Blob Storage, Google Cloud Storage, Backblaze B2, WebDAV, SFTP, Rclone pour les services tiers (support expérimental), et même ton propre Kopia Repository Server pour centraliser plusieurs machines. Si ton homelab tourne déjà avec [Suricata docker](/suricata-docker-ids-ips-reseau/) pour surveiller le réseau, Kopia s'intègre dans la même logique de sécurité : chiffrer à la source plutôt que de faire confiance au transport.

## Installation de Kopia docker avec Docker Compose

L'image officielle `kopia/kopia` existe en `amd64`, `arm64` et `arm`, avec un tag `latest` pour la dernière stable et `unstable` pour les builds nocturnes. Voici un `docker-compose.yml` adapté du modèle officiel, en mode serveur avec interface web activée :

```yaml
services:
  kopia:
    image: kopia/kopia:latest
    container_name: kopia
    hostname: kopia-backup
    restart: unless-stopped
    ports:
      - "51515:51515"
    command:
      - server
      - start
      - --disable-csrf-token-checks
      - --insecure
      - --address=0.0.0.0:51515
      - --server-username=admin
      - --server-password=CHANGE_MOI
    environment:
      KOPIA_PASSWORD: "MOT_DE_PASSE_DU_DEPOT"
      USER: "kopia"
    volumes:
      - ./config:/app/config
      - ./cache:/app/cache
      - ./logs:/app/logs
      - /chemin/vers/tes/donnees:/data:ro
      - ./repository:/repository
      - /tmp/kopia:/tmp:shared
```

Trois mots de passe à distinguer, et c'est là qu'on se plante souvent au premier essai :

- `KOPIA_PASSWORD` chiffre le dépôt lui-même. Perds-le et le dépôt est définitivement illisible, pas de récupération possible.
- `--server-username` / `--server-password` protègent uniquement l'accès à l'interface web, pas tes données.
- Si tu pousses vers un stockage distant (S3, B2, SFTP), ajoute les credentials correspondants en variables d'environnement, jamais en dur dans le compose versionné.

⚠️ L'option `--insecure` désactive TLS sur l'interface web. Si tu exposes le port 51515 au-delà de ton LAN, mets un reverse proxy devant avec un certificat valide. Si tu as déjà [Certimate docker](/certimate-docker-renouvellement-ssl/) pour renouveler tes certificats SSL, c'est l'occasion de le brancher ici.

Monte le stack :

```bash
docker compose up -d
```

L'interface web répond sur `http://ton-serveur:51515`. Le volume `/data` est monté en lecture seule, c'est une bonne pratique : Kopia n'a aucune raison d'écrire dans ce que tu sauvegardes.

## Créer ton premier dépôt chiffré et lancer un snapshot

Si tu préfères le CLI pur (scripts, cron, pas de serveur web), exécute les commandes directement dans le conteneur ou sur l'hôte avec le binaire natif. Créer un dépôt sur un stockage local :

```bash
kopia repository create filesystem --path /repository
```

Kopia te demande un mot de passe, c'est celui qui chiffre tout. Pour se reconnecter à un dépôt existant depuis une autre machine ou après un redémarrage :

```bash
kopia repository connect filesystem --path /repository
```

Lancer un premier snapshot d'un dossier :

```bash
kopia snapshot create /data
```

Lister les snapshots pour ce même dossier :

```bash
kopia snapshot list /data
```

✅ Première règle d'or : teste une restauration avant de faire confiance au système. Un backup qu'on n'a jamais restauré n'est pas un backup, c'est un espoir.

## Politiques de rétention et planification automatique

C'est la partie que beaucoup laissent aux valeurs par défaut, et c'est une erreur : sans politique explicite, tu peux accumuler des snapshots indéfiniment ou au contraire en perdre trop vite. La commande `policy set` accepte plusieurs options de rétention cumulables :

```bash
kopia policy set --keep-latest 10 --keep-daily 14 --keep-weekly 8 --keep-monthly 12 /data
```

- `--keep-latest` : nombre de snapshots les plus récents à garder peu importe la date
- `--keep-daily`, `--keep-weekly`, `--keep-monthly`, `--keep-annual` : rétention par granularité de temps
- `--keep-hourly` : utile si tu snapshotes plusieurs fois par jour une base de données critique

Pour la planification, Kopia peut déclencher les snapshots lui-même, sans passer par un cron externe :

```bash
kopia policy set --snapshot-interval 6h /data
```

Ou avec une syntaxe crontab si tu veux des horaires précis :

```bash
kopia policy set --snapshot-time-crontab "0 2 * * *" /data
```

Vérifie toujours ce qui est réellement appliqué, Kopia hérite des politiques globales si tu n'en définis pas de spécifique :

```bash
kopia policy show /data
```

💡 Astuce : définis une politique globale raisonnable une fois (`kopia policy set --global ...`) puis surcharge seulement les dossiers qui ont des besoins différents. C'est plus simple à maintenir que de répéter la même politique sur chaque source.

## Restauration, vérification et dépannage

Restaurer un snapshot complet :

```bash
kopia snapshot restore <snapshot-id> /chemin/de/restauration
```

L'ID du snapshot s'obtient avec `kopia snapshot list`. Si tu ne veux récupérer qu'un seul fichier, Kopia permet aussi de monter un snapshot comme un système de fichiers en lecture seule, pratique pour aller piocher un seul document sans tout restaurer.

Les erreurs les plus fréquentes que je croise sur Kopia docker :

- **« repository is not connected »** : le conteneur a redémarré et le fichier `repository.config` dans `/app/config` n'a pas survécu. Vérifie que ce volume est bien persisté, pas dans un tmpfs.
- **Snapshots qui traînent en « incomplete »** : souvent un montage `/tmp` qui n'est pas en mode `shared`, ou un volume source qui a disparu en cours de snapshot. Vérifie les logs dans `/app/logs`.
- **Interface web injoignable** : `--address=0.0.0.0:51515` doit matcher le port publié dans le compose. Si tu as changé le port côté hôte sans changer `--address`, ça ne répond pas.
- **Dépôt distant lent sur S3 ou B2** : augmente la taille du cache local (`/app/cache`), Kopia s'appuie beaucoup sur lui pour éviter de retélécharger des métadonnées à chaque opération.

Pour un audit plus large de ta posture sécurité avant de considérer ton homelab comme protégé, [Lynis docker](/lynis-docker-audit-securite-linux/) complète bien ce genre de mise en place, il vérifie la config système autour de tes conteneurs, pas seulement les sauvegardes.

## Kopia vs Restic vs BorgBackup vs Duplicati : le comparatif

| Outil | Déduplication | Chiffrement | Interface | Image Docker | Niveau requis |
|---|---|---|---|---|---|
| **Kopia** | Par blocs, content-defined | AES256_GCM | CLI + Web (KopiaUI) | `kopia/kopia` | Intermédiaire |
| **Restic** | Par blocs | AES-256-GCM | CLI uniquement | `restic/restic` | Avancé |
| **BorgBackup** | Bloc à bloc, locale | AES-256-CTR | CLI uniquement | `borgbackup/borg` | Intermédiaire |
| **Duplicati** | Par blocs, variable | AES-256 | Web UI complète | `duplicati/duplicati` | Débutant |

Mon avis après avoir fait tourner les quatre en parallèle un moment : si tu veux une interface web sans renoncer au scripting CLI, Kopia docker gagne, c'est le seul qui couvre vraiment les deux usages sans compromis. [Restic docker](/restic-docker-sauvegarde-moderne/) reste imbattable en pur CLI si tu scriptes tout et que l'interface web ne t'intéresse pas. [BorgBackup docker](/borgbackup-docker-sauvegarde/) a l'écosystème le plus mature côté déduplication historique. [Duplicati docker](/duplicati-docker-sauvegarde/) reste le plus accessible pour un premier homelab, quitte à perdre un peu en performance sur de gros volumes.

La vraie question c'est : tu veux scripter en cron sans jamais ouvrir de navigateur, ou tu veux pouvoir vérifier l'état de tes backups d'un coup d'œil sans taper une seule commande. Kopia est le seul des quatre qui ne t'oblige pas à trancher.

## Conclusion

Kopia docker coche les cases qui comptent pour un homelab sérieux : chiffrement côté client sans option à activer séparément, déduplication qui tient réellement tes volumes de stockage à distance raisonnable, et une interface web qu'on n'a pas besoin de bricoler soi-même. Le fait qu'il reste piloté par des policies déclaratives plutôt que des scripts maison en fait aussi un outil qui vieillit bien quand tu ajoutes des machines à sauvegarder.

Mon conseil avant de te lancer : commence petit, un seul dossier, un dépôt local, teste une restauration complète. Une fois que tu as confiance dans le cycle complet, ajoute un stockage distant (S3, B2, ou ton NAS en SFTP) et des politiques de rétention adaptées à chaque source. Bon, on va pas se mentir, la partie la plus facile à négliger c'est de vérifier que la restauration marche vraiment. Fais-le quand même.
