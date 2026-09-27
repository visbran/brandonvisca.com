---
title: "Plex Docker : serveur média auto-hébergé complet"
description: "Installe Plex Docker en 10 minutes : docker-compose, PLEX_CLAIM, montage des bibliothèques, transcodage matériel et comparatif Jellyfin."
pubDatetime: "2026-09-27T11:02:34+02:00"
modDatetime: "2026-09-26T08:00:00.000Z"
author: Brandon
tags:
  - auto-hebergement
  - docker
  - mediacenter
  - streaming
  - intermediaire
featured: false
draft: false
focusKeyword: plex docker
faqs:
  - question: "Plex Docker consomme combien de RAM en usage normal ?"
    answer: "Au repos, compte 200 à 400 Mo pour le conteneur. Pendant un transcodage logiciel, ça grimpe facilement à 1-2 Go selon la résolution source et cible, d'où l'intérêt du transcodage matériel si ton CPU sature."
  - question: "Je peux migrer ma bibliothèque Plex existante vers le conteneur Docker ?"
    answer: "Oui. Arrête l'ancienne instance, copie le dossier de config (base de données, métadonnées, miniatures) dans le volume /config du conteneur, puis démarre. Les identifiants de compte et les serveurs associés restent liés au token de la base copiée."
  - question: "Faut-il exposer le port 32400 directement sur internet ?"
    answer: "Non, pas en accès direct. Passe par le relais Plex (activé par défaut, NAT traversal automatique) ou par un reverse proxy avec certificat TLS si tu veux ton propre nom de domaine. Exposer le port brut sans rien devant, c'est prendre un risque inutile."
---
> 💡 **TL;DR**
> - Plex Docker se monte avec l'image officielle `plexinc/pms-docker` ou l'image communautaire `linuxserver/plex`, réseau host recommandé, volumes séparés pour la config et les médias
> - Le token `PLEX_CLAIM` (valable 4 minutes, généré sur plex.tv/claim) rattache le conteneur à ton compte dès le premier démarrage
> - Jellyfin reste l'alternative 100 % open source si tu veux éviter le compte cloud obligatoire de Plex, au prix d'un écosystème client moins poli

## Pourquoi monter Plex Docker plutôt qu'une installation native

Plex tourne très bien installé nativement sur un NAS Synology ou une distribution Linux classique. Mais dès que tu gères plus d'un service auto-hébergé, l'installation native devient vite ingérable : dépendances qui traînent, mises à jour qui cassent d'autres paquets, config éparpillée dans `/var/lib`.

Avec Docker, ta bibliothèque Plex tient dans un seul dossier `/config`. Tu sauvegardes ce dossier, tu changes de machine, tu relances le conteneur, et tout est là. Chez moi, c'est ce qui m'a définitivement convaincu de migrer : plus de "pourquoi Plex ne démarre plus après la mise à jour du système", juste `docker compose up -d` et basta.

## Table des matières

## Deux images, deux philosophies

Monter Plex Docker commence par un choix d'image, avant tout `docker run`. Il y en a deux qui comptent vraiment :

- **`plexinc/pms-docker`** : l'image officielle, maintenue directement par Plex Inc. Elle colle aux releases publiées sur le site officiel.
- **`linuxserver/plex`** : l'image de la communauté LinuxServer.io, sous licence GPLv3, avec les variables `PUID`/`PGID` qui simplifient la gestion des permissions face à un NAS ou un montage NFS.

✅ Les deux font le job. Je pars sur l'image LinuxServer.io dans cet article parce que la gestion des UID/GID en fait la référence quand tes médias sont sur un stockage partagé avec d'autres conteneurs (Radarr, Sonarr, ton client torrent).

## Installation de Plex Docker : le docker-compose qui marche

Avant de lancer le conteneur, trois trucs à avoir sous la main : **Docker et Docker Compose** installés sur ton hôte (Linux de préférence, Plex Docker tourne aussi sur Synology/QNAP via leur interface Docker), **un compte Plex.tv** gratuit et obligatoire pour l'appairage initial (contrairement à Jellyfin, tu ne peux pas faire tourner Plex sans passer par leur infra pour le "claim" du serveur), et **une arborescence de médias propre**, séparée en dossiers par type (`/movies`, `/tv`) pour que Plex scanne correctement les métadonnées.

⚠️ Si tes fichiers médias sont sur un NAS distant, monte le partage réseau (NFS ou SMB) sur l'hôte Docker *avant* de démarrer le conteneur, pas depuis l'intérieur du conteneur. Ça t'évite des soucis de permissions à répétition.

Récupère ton token sur `plex.tv/claim` (valable 4 minutes, donc prépare ton fichier avant d'y aller) et lance ton `docker-compose.yml` :

```yaml
services:
  plex:
    image: lscr.io/linuxserver/plex:latest
    container_name: plex
    network_mode: host
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Paris
      - VERSION=docker
      - PLEX_CLAIM=claim-xxxxxxxxxxxxxxxxxxxx
    volumes:
      - /chemin/vers/plex/config:/config
      - /chemin/vers/films:/movies
      - /chemin/vers/series:/tv
    restart: unless-stopped
```

Puis :

```bash
docker compose up -d
```

Le mode `network_mode: host` n'est pas un caprice : Plex utilise la découverte réseau (GDM) pour se faire trouver par tes clients locaux, et ça marche nettement mieux sans NAT Docker au milieu. Si tu es en bridge pour une raison précise (plusieurs interfaces réseau, isolation stricte), ouvre au minimum le port `32400/tcp` et attends-toi à devoir configurer le relais manuellement.

Une fois le conteneur up, l'interface web est sur `http://<ip-de-ton-hote>:32400/web`. Connecte-toi avec ton compte Plex, et le serveur "claimé" apparaît directement rattaché.

## Configurer tes bibliothèques

Dans l'interface web, `Réglages > Gérer > Bibliothèques > Ajouter une bibliothèque`. Choisis le type (Films, Séries), pointe vers `/movies` ou `/tv` (les chemins *dans* le conteneur, pas ceux de l'hôte), et laisse Plex scanner.

Le scan initial peut prendre un moment selon le volume de fichiers : Plex va chercher les métadonnées (affiches, synopsis, casting) sur ses agents en ligne. Pour que ça matche bien, respecte une convention de nommage standard :

```
/movies/Nom du film (2026)/Nom du film (2026).mkv
/tv/Nom de la série/Season 01/Nom de la série - S01E01.mkv
```

💡 Un nommage bancal, c'est la cause numéro un des mauvais matchs de métadonnées. Si Plex associe ton film à la mauvaise fiche, corrige le nom du fichier plutôt que de bidouiller manuellement la correspondance à chaque scan.

## Transcodage : le vrai enjeu de perf

C'est là que Plex Docker se joue vraiment. Le transcodage à la volée (quand un client demande une résolution ou un codec que sa bande passante ou son appareil ne supporte pas) est gourmand en CPU si tu restes en logiciel.

Pour activer le transcodage matériel (Intel Quick Sync, par exemple), il faut :

1. Que ton hôte ait un GPU Intel avec Quick Sync activé (`/dev/dri` accessible).
2. Ajouter le device au compose :

```yaml
    devices:
      - /dev/dri:/dev/dri
```

3. Activer "Accélération matérielle de transcodage" dans `Réglages > Transcodeur`, et avoir un Plex Pass actif (fonctionnalité réservée aux abonnés payants).

✅ Sans Quick Sync ni Plex Pass, privilégie le "Direct Play" : configure tes clients pour lire les fichiers dans leur format natif sans transcoder. Ça évite de mettre ton CPU à genoux, au prix de fichiers parfois plus lourds à streamer en 4K sur une connexion limitée.

Sur Plex Docker, le dossier `/config` contient toute ta base de données, tes métadonnées téléchargées et tes miniatures. C'est lui qu'il faut sauvegarder, pas tes fichiers médias qui sont remplaçables. J'ai déjà écrit sur [Duplicati Docker pour la sauvegarde chiffrée auto-hébergée](/duplicati-docker-sauvegarde/) si tu veux automatiser cette partie plutôt que de faire des copies manuelles à la main.

⚠️ Arrête le conteneur avant de copier le dossier `/config` à froid. Une copie à chaud sur une base SQLite active peut te donner un fichier corrompu.

## Plex vs Jellyfin : le vrai comparatif

La question revient à chaque fois qu'on parle serveur média auto-hébergé. Voici les différences qui comptent, sans les paragraphes marketing :

| Critère | Plex | Jellyfin |
|---|---|---|
| Licence | Propriétaire, gratuit avec option payante | 100 % open source (GPLv2) |
| Compte cloud requis | Oui, obligatoire | Non |
| Transcodage matériel | Réservé au Plex Pass | Gratuit, inclus |
| Apps clients | Très polies (TV, mobile, web) | Correctes mais moins abouties |
| Découverte de contenu | Bandes-annonces, recommandations | Minimaliste |
| Communauté / plugins | Écosystème fermé | Plugins communautaires ouverts |

Si ta priorité c'est le confort d'usage pour toute la famille (interface léchée, apps qui marchent sans bidouille sur toutes les télés), Plex garde l'avantage. Si ta priorité c'est l'indépendance totale, zéro compte tiers, zéro dépendance à un serveur cloud pour l'appairage, Jellyfin est objectivement plus cohérent avec l'esprit auto-hébergement.

Chez moi, les deux tournent en parallèle sur des bibliothèques différentes. Plex pour le salon familial, Jellyfin pour mes propres tests. Pas de dogme, juste l'outil qui correspond à l'usage.

## Dépannage courant sur Plex Docker

**Le serveur n'apparaît pas dans l'interface plex.tv après le claim.** Vérifie que le token n'a pas expiré (4 minutes de validité) et que le conteneur a bien accès à internet en sortie. Regarde les logs avec `docker logs plex`.

**Les métadonnées ne se téléchargent pas.** Le conteneur doit pouvoir atteindre les agents Plex en ligne. Si tu es derrière un DNS filtrant type Pi-hole avec des listes agressives, whitelist les domaines Plex.

**Transcodage qui rame malgré Quick Sync activé.** Vérifie que `/dev/dri` est bien monté (`docker exec plex ls /dev/dri` doit lister `renderD128`) et que l'utilisateur du conteneur (PUID) a les droits sur ce device côté hôte, généralement via le groupe `render` ou `video`.

**Bibliothèque qui ne scanne pas les nouveaux fichiers.** Le scan automatique a un délai par défaut. Force un scan manuel depuis les trois points à côté de la bibliothèque, ou active la surveillance temps réel (inotify) dans les réglages avancés de la bibliothèque.

## Conclusion

Plex Docker, c'est la voie la plus propre pour héberger ton serveur média sans polluer ton système hôte. Le compose ci-dessus suffit pour un usage standard, et l'ajout du transcodage matériel ne prend que quelques lignes de plus si ton CPU commence à souffrir.

La vraie question c'est de savoir si tu es prêt à dépendre du compte cloud Plex pour l'appairage, ou si tu préfères l'indépendance totale de Jellyfin. Les deux se déploient de la même façon en Docker, donc rien ne t'empêche de tester les deux avant de trancher.

Une fois Plex up, pense à l'écosystème autour : [un client torrent ultra-léger](/transmission-docker-client-torrent/) pour alimenter tes bibliothèques, [Duplicati](/duplicati-docker-sauvegarde/) pour la sauvegarde de la config, et [Changedetection pour surveiller les sorties](/changedetection-docker-surveillance-web/) si tu veux être alerté sans dépendre d'un plugin tiers.
