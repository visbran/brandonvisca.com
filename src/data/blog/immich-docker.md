---
title: Immich remplace Google Photos ? Guide Docker complet 2026
description: Guide complet pour installer Immich avec Docker Compose et remplacer Google Photos par une solution open-source auto-hébergée.
pubDatetime: "2026-05-15T19:00:00+02:00"
modDatetime: "2026-05-15T19:00:00+02:00"
author: Brandon Visca
tags:
  - auto-hebergement
  - docker
  - multimedia
  - vie-privee
  - intermediaire
  - guide
featured: false
draft: false
focusKeyword: immich docker
faqs:
  - question: "Immich est-il vraiment gratuit ?"
    answer: "Oui, c'est open-source sous licence AGPL-3.0 et 100 % gratuit en self-hosted. Aucune fonctionnalité payante, aucun abonnement."
  - question: "Faut-il un serveur puissant pour faire tourner Immich ?"
    answer: "Pas forcément. Un VPS à 4 Go de RAM ou un NAS modeste suffisent pour commencer. Le machine learning (recherche par contenu) demande un peu plus de ressources."
  - question: "Puis-je importer mes photos depuis Google Photos ?"
    answer: "Oui, via Google Takeout. Immich propose un outil d'upload en vrac qui gère les albums et même les métadonnées EXIF."
  - question: "Quelle est la différence avec Nextcloud Photos ?"
    answer: "Immich est spécialisé uniquement dans les médias. L'interface est fluide, la recherche par contenu (ML) est native, et l'expérience mobile est bien supérieure. Nextcloud reste le couteau-suisse, Immich est le scalpel."
---
> 💡 **TL;DR** : Immich est une alternative open-source à Google Photos qui te permet d'héberger tes photos et vidéos sur ton propre serveur. Guide complet pour l'installer en quelques minutes avec Docker Compose.

## Table des matières

1. [Immich, c'est quoi concrètement](#immich-cest-quoi-concrètement)
2. [Pourquoi quitter Google Photos](#pourquoi-quitter-google-photos)
3. [Prérequis](#prérequis)
4. [Installation avec Docker Compose](#installation-avec-docker-compose)
5. [Premier démarrage et configuration](#premier-démarrage-et-configuration)
6. [Importer tes photos existantes](#importer-tes-photos-existantes)
7. [Les applications mobiles](#les-applications-mobiles)
8. [Astuces pour aller plus loin](#astuces-pour-aller-plus-loin)
9. [Le mot de la fin](#le-mot-de-la-fin)

## Immich, c'est quoi concrètement

Immich est une application web et mobile qui fait exactement ce que Google Photos fait — mais sur ton propre serveur. Pas de cloud américain, pas de collecte de données, pas de tarification qui change tous les six mois.

Le projet est porté par une communauté très active. Avec plus de 100 000 étoiles sur GitHub et des releases régulières (la v2.7.5 vient de sortir en avril 2026), il est devenu le standard de facto dans le monde de l'auto-hébergement multimédia.

Ce que tu peux faire avec Immich :

- **Sauvegarder automatiquement** les photos et vidéos de ton téléphone
- **Rechercher** par contenu ("chat", "plage", "voiture") grâce au machine learning
- **Partager** des albums avec ta famille, même si eux n'ont pas Immich
- **Gérer la géolocalisation** et les métadonnées EXIF
- **Créer des albums partagés**, des favoris et des archives

⚠️ **Point d'attention** : le projet porte encore le badge "early access" sur son site officiel. Cela signifie que le développeur te recommande d'avoir une stratégie de sauvegarde à côté. Dans la pratique, le projet est très stable, mais cette prudence est de mise.

## Pourquoi quitter Google Photos

Google Photos a changé son modèle économique en 2022. La synchronisation gratuite illimitée avec compression a disparu. Aujourd'hui, chaque photo compte dans ton quota Google de 15 Go (partagé avec Gmail et Drive).

Et même si tu payes pour le stockage, il reste une question fondamentale : tes souvenirs intimes sont stockés sur des serveurs dont tu ne contrôles pas les politiques. Google a le droit d'utiliser tes images pour affiner sa modèle de reconnaissance faciale, d'analyse de contenu et même de publicité ciblée.

Avec Immich :

- **Tes photos restent chez toi.** Sur ton NAS, ton VPS ou ton serveur dédié.
- **Tu décides quand tout ça disparaît.** Pas de coupure de service surprise.
- **Pas de compression forcée.** Tu peux stocker les fichiers originaux sans altération.
- **Pas de dépendance à un écosystème fermé.** Ton contenu est dans un format standard, pas verrouillé dans une app.

## Prérequis

Pour suivre ce guide, tu auras besoin de :

- Un serveur sous Linux (Debian/Ubuntu recommandé) avec Docker et Docker Compose installés
- Au moins 4 Go de RAM disponibles (8 Go recommandés si tu actives le machine learning)
- Environ 20 Go d'espace disque pour le système + la taille de ta bibliothèque photo
- Un nom de domaine (facultatif mais recommandé) et un reverse proxy comme Traefik ou Nginx

Si Docker Compose n'est pas encore installé sur ton serveur, voici la commande rapide :

```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

🔍 **Astuce** : si tu cherches un guide complet pour Docker, j'ai publié une [introduction à Docker pour débutants](/docker-debutant-services-auto-heberger/).

## Installation avec Docker Compose

Immich ne s'installe pas en un seul container. Le compose officiel prévoit plusieurs services :

- `immich-server` : le moteur principal qui sert l'interface web et l'API
- `immich-machine-learning` : le module qui repère les objets, les visages et les contenus dans tes photos
- `redis` : le cache entre le serveur et la base de données
- `postgres` : la base de données relationnelle qui stocke les métadonnées

Voici le fichier `docker-compose.yml` officiel et à jour :

```yaml
name: immich

services:
  immich-server:
    container_name: immich-server
    image: ghcr.io/immich-app/immich-server:release
    command: ['start.sh', 'immich']
    volumes:
      - ${UPLOAD_LOCATION}:/usr/src/app/upload
      - /etc/localtime:/etc/localtime:ro
    ports:
      - '2283:2283'
    environment:
      REDIS_HOSTNAME: immich-redis
      DB_DATABASE_NAME: ${DB_DATABASE_NAME}
      DB_USERNAME: ${DB_USERNAME}
      DB_PASSWORD: ${DB_PASSWORD}
    depends_on:
      - immich-redis
      - immich-database
    restart: always
    healthcheck:
      disable: false

  immich-machine-learning:
    container_name: immich-machine-learning
    image: ghcr.io/immich-app/immich-machine-learning:release
    volumes:
      - model-cache:/cache
    environment:
      REDIS_HOSTNAME: immich-redis
      DB_DATABASE_NAME: ${DB_DATABASE_NAME}
      DB_USERNAME: ${DB_USERNAME}
      DB_PASSWORD: ${DB_PASSWORD}
    restart: always
    healthcheck:
      disable: false

  immich-redis:
    container_name: immich-redis
    image: docker.io/redis:6.2-alpine@sha256:148bb5411c44abd... # vérifier le hash sur le repo
    healthcheck:
      test: redis-cli ping || exit 1
    restart: always

  immich-database:
    container_name: immich-database
    image: docker.io/tensorchord/pgvecto-rs:pg14-v0.2.0@sha256:739cdd6... # vérifier le hash
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_USER: ${DB_USERNAME}
      POSTGRES_DB: ${DB_DATABASE_NAME}
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: pg_isready --dbname='$${POSTGRES_DB}' --username='$${POSTGRES_USER}' || exit 1; Chksum='$$(pg_walfile_name_offset('$${PGDATA}'))'
      interval: 5m
      start_interval: 30s
      start_period: 5m
    command:
      - postgres
      - -c
      - shared_preload_libraries=vectors.so
      - -c
      - 'search_path="$$user", public, vectors'
      - -c
      - logging_collector=on
      - -c
      - max_wal_size=2GB
      - -c
      - shared_buffers=512MB
      - -c
      - wal_compression=on
    restart: always

volumes:
  model-cache:
  pgdata:
```

> ⚠️ **Attention** : les hashes SHA256 dans le compose officiel changent à chaque release. Va toujours chercher la version officielle sur le repo GitHub : `https://github.com/immich-app/immich/releases/latest`

Crée ensuite ton fichier `.env` avec les variables suivantes :

```bash
UPLOAD_LOCATION=./library
DB_DATABASE_NAME=immich
DB_USERNAME=postgres
DB_PASSWORD=remplace_par_un_mot_de_passe_fort
```

Lance l'installation :

```bash
docker network create immich
docker-compose up -d
```

Cela prend environ 30 secondes. Le service sera accessible sur le port `2283`.

## Premier démarrage et configuration

Ouvre ton navigateur et rends-toi sur `http://IP_DU_SERVEUR:2283`. Tu arrives sur un wizard de configuration en trois étapes :

1. **Crée un compte administrateur.** C'est le premier utilisateur, il devient automatiquement admin.
2. **Laisse les paramètres par défaut** pour le stockage et les modèles ML.
3. **Active la recherche par contenu.** C'est ce qui démarque le plus Immich des autres solutions.

Dès la connexion, tu peux explorer l'interface. Elle ressemble furieusement à Google Photos : une timeline, une vue par album, une carte géographique et une page de recherche.

Si tu utilises un reverse proxy (fortement recommandé), ajoute cette configuration Traefik dans ton `docker-compose.yml` :

```yaml
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.immich.rule=Host(\`photos.ton-domaine.fr\`)"
      - "traefik.http.routers.immich.entrypoints=websecure"
      - "traefik.http.routers.immich.tls.certresolver=letsencrypt"
      - "traefik.http.services.immich.loadbalancer.server.port=2283"
```

Tu veux un guide complet sur Traefik ? J'ai testé et publié [un comparatif entre Traefik et Nginx](/traefik-reverse-proxy-docker/) pour l'auto-hébergement.

## Importer tes photos existantes

Immich propose deux méthodes pour importer ton historique :

### Depuis Google Photos (Takeout)

1. Va sur [Google Takeout](https://takeout.google.com/) et demande l'export de tes données Google Photos.
2. Décompresse l'archive sur ton serveur.
3. Utilise le CLI d'Immich pour l'import en masse :

```bash
docker exec -it immich-server immich upload /usr/src/app/upload/takeout/
```

### Depuis un dossier local

Pour un simple glisser-déposer, tu peux utiliser l'interface web ou le client CLI. Sur le serveur, place tes fichiers dans le volume de upload et lance :

```bash
docker exec -it immich-server immich upload /usr/src/app/upload/mes-photos/
```

Le processus peut être long. Immich va indexer chaque fichier, extraire les métadonnées EXIF, reconnaître les visages et générer des vignettes.

## Les applications mobiles

C'est ici que le projet devient vraiment intéressant. Immich propose des applications iOS et Android gratuites.

- **iOS** : disponible sur le App Store, recherche "Immich"
- **Android** : disponible sur le Google Play Store ou en APK direct

Une fois connectée, l'application te propose un **auto-upload** en arrière-plan. Tes photos sont immédiatement envoyées vers ton serveur dès que tu es en Wi-Fi. Tu peux même choisir de garder les originaux sur le téléphone ou de libérer de l'espace en supprimant les fichiers locaux après upload.

L'interface mobile est fluide, rapide, et gère même la lecture de vidéos transcodées automatiquement si ton serveur est un peu léger.

## Astuces pour aller plus loin

- **Machine learning facultatif** : si ton serveur manque de RAM, tu peux désactiver le service `immich-machine-learning`. Tu perdras la recherche par contenu et la reconnaissance faciale, mais pas la synchronisation.
- **Sauvegarde de la base de données** : avec un simple `pg_dump` ou en montant le volume `pgdata` dans une stratégie de backup type Restic ou Kopia.
- **Stockage externe** : le volume `UPLOAD_LOCATION` peut pointer vers un montage NFS, un disque externe ou même un bucket S3.
- **Multi-utilisateur** : depuis l'interface admin, tu peux créer des accès pour ta famille. Chacun a son propre espace, mais les albums peuvent être partagés.

💡 **Mon réglage perso** : j'ai monté un volume NFS depuis mon NAS Proxmox vers le container et j'utilise [Watchtower](/watchtower-mise-a-jour-docker-auto/) pour garder Immich à jour automatiquement. Zéro intervention, toujours la dernière version.

## Le mot de la fin

Immich est une des alternatives les plus abouties à Google Photos dans l'écosystème open-source. La synchronisation mobile est fiable, l'interface est moderne, et le machine learning ajoute une vraie valeur pour indexer ses souvenirs.

Son seul défaut ? Il ne fait que des photos. Si tu cherches une suite complète — documents, agenda, contacts, fichiers — Nextcloud reste incontournable. Mais pour une bibliothèque photo dédiée, auto-hébergée et respectueuse, Immich est la solution à adopter en 2026.

Si tu passés à l'auto-hébergement récemment, tu peux aussi lire mon [guide complet pour quitter Google](/quitter-google-auto-hebergement/). Il détaille chaque étape pour reprendre le contrôle de ton indépendance numérique.
