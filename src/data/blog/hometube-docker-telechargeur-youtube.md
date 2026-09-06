---
title: "HomeTube Docker : téléchargeur YouTube auto-hébergé avec interface web"
description: "HomeTube Docker : installe un téléchargeur YouTube auto-hébergé avec interface web et intégration Plex/Jellyfin en quelques minutes."
pubDatetime: "2026-08-20T09:00:00.000Z"
modDatetime: "2026-08-20T09:00:00.000Z"
author: Brandon
tags:
  - intermediaire
  - auto-hebergement
  - docker
  - youtube
  - jellyfin
featured: false
draft: false
focusKeyword: hometube docker
faqs:
  - question: "HomeTube est-il légal ?"
    answer: "HomeTube utilise yt-dlp, un outil open-source. La légalité dépend de la juridiction et de l'usage (usage privé vs redistribution). Respecte les conditions d'utilisation des plateformes et les droits d'auteur."
  - question: "Quelle est la différence entre HomeTube et yt-dlp en ligne de commande ?"
    answer: "HomeTube est une interface web Streamlit qui encapsule yt-dlp avec des options avancées (playlist sync, processing vidéo, intégration media server) sans toucher au terminal."
  - question: "HomeTube fonctionne-t-il avec Plex ?"
    answer: "Oui. HomeTube organise les fichiers téléchargés dans une structure de dossiers compatible Plex, Jellyfin et Emby."
  - question: "Peut-on télécharger des playlists entières ?"
    answer: "Oui. HomeTube gère la synchronisation intelligente des playlists avec un suivi résilient. La bibliothèque locale reste synchronisée avec la source."
  - question: "Quels formats vidéo sont supportés ?"
    answer: "HomeTube supporte plus de 1800 plateformes via yt-dlp : YouTube, Reddit, Vimeo, Dailymotion, TikTok, Twitch, Facebook, Instagram, etc."
ogImage: ""
---
> 💡 **TL;DR**
> - HomeTube est une interface web **Streamlit** qui encapsule **yt-dlp** pour télécharger des vidéos en haute qualité.
> - Une image Docker officielle `ghcr.io/egalitarianmonkey/hometube` permet un déploiement **hometube docker** en une minute.
> - Intégration native **Plex**, **Jellyfin** et **Emby** avec une structure de dossiers automatique.

Tu as déjà eu envie de télécharger une playlist YouTube complète, de l'organiser proprement dans ta bibliothèque [Jellyfin](/jellyfin-docker-alternative-netflix-gratuite/) et d'y accéder depuis ton canapé sans passer par trois outils différents ? Bien sûr que oui. Et tu as probablement fini par copier-coller des URLs dans un terminal en espérant que yt-dlp ne crashe pas au milieu du téléchargement.

**HomeTube** résout exactement ce problème. C'est un téléchargeur vidéo universel avec une interface web élégante, conçu pour s'intégrer directement dans ton homelab. Pas de terminal, pas de scripts bash à bidouiller. Tu colles l'URL, tu choisis la qualité, et HomeTube gère le reste : téléchargement, nommage propre, placement dans la bonne arborescence, et même synchronisation de playlists.

## Table des matières

## Qu'est-ce que HomeTube Docker exactement ?

HomeTube est un projet open-source (AGPL-3.0) développé par **EgalitarianMonkey**, avec plus de 1400 stars sur GitHub. Il s'agit d'une couche graphique en **Streamlit** au-dessus de **yt-dlp**, le célèbre fork actif de youtube-dl. Mais ce n'est pas juste un wrapper : HomeTube ajoute une logique d'organisation automatique des fichiers, une gestion résiliente des playlists, et des options de processing vidéo avancées (découpage, sous-titres intégrés, conversion de formats).

L'image Docker officielle est publiée sur le GitHub Container Registry (`ghcr.io/egalitarianmonkey/hometube`) et supporte amd64 ainsi que arm64. Elle embarque Python 3.11+, Streamlit 1.49+ et toutes les dépendances yt-dlp préconfigurées.

### Les fonctionnalités clés

- **Téléchargement best-quality** : stratégie automatique pour récupérer la meilleure qualité disponible (vidéo + audio fusionnées en MKV ou MP4).
- **Blocage natif des publicités et sponsors** : grâce à l'intégration yt-dlp, les segments sponsorisés sont automatiquement exclus.
- **Organisation media-server ready** : les fichiers sont nommés et classés selon une structure compatible Plex, Jellyfin ou Emby.
- **Playlist sync intelligente** : suivi résilient des playlists. Si une vidéo est supprimée de la source, HomeTube le sait. Si tu ajoutes des vidéos, il les télécharge automatiquement.
- **Auth par cookies** : indispensable pour les contenus restreints ou les erreurs de signature YouTube.
- **Processing avancé** : découpe de clips, intégration de sous-titres, conversion de formats personnalisés.
- **Arguments yt-dlp custom** : proxy, limite de taille, filtres de format, tout est configurable.
- **1800+ plateformes supportées** : YouTube, Reddit, Vimeo, Dailymotion, TikTok, Twitch, Facebook, Instagram, etc.

## Prérequis

Avant de lancer le conteneur, assure-toi d'avoir :

- Un serveur avec **Docker** et **Docker Compose** installés. Si tu débutes, suis d'abord mon guide [Docker pour débutants](/docker-debutant-services-auto-heberger/).
- Un dossier dédié pour les téléchargements (idéalement sur un volume avec suffisamment d'espace, les vidéos 4K grossissent vite).
- Optionnel : un conteneur [Jellyfin](/jellyfin-docker-alternative-netflix-gratuite/) ou Plex déjà configuré pour pointer vers la même bibliothèque.

## Installation de HomeTube Docker avec Compose

Crée un dossier dédié et un fichier `docker-compose.yml` :

```bash
mkdir -p ~/hometube && cd ~/hometube
nano docker-compose.yml
```

Voici une configuration complète et prête pour la production :

```yaml
services:
  hometube:
    image: ghcr.io/egalitarianmonkey/hometube:latest
    container_name: hometube
    restart: unless-stopped
    ports:
      - "8501:8501"
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Paris
    volumes:
      - ./config:/app/config
      - ./downloads:/app/downloads
      - ./cookies:/app/cookies:ro
    networks:
      - hometube-net

networks:
  hometube-net:
    driver: bridge
```

### Explications des volumes

- `./config:/app/config` : persiste la configuration HomeTube, l'historique des téléchargements et la base de suivi des playlists. **Ne jamais supprimer ce dossier** si tu veux garder la synchronisation playlist intacte.
- `./downloads:/app/downloads` : dossier de sortie des vidéos téléchargées. C'est ici que tu dois monter ton stockage media (NAS, disque externe, ou sous-volume Jellyfin).
- `./cookies:/app/cookies:ro` : monte un fichier `cookies.txt` en lecture seule. Essentiel pour les contenus YouTube restreints ou les erreurs 403 récentes. Génère-le avec une extension de navigateur comme **Get cookies.txt LOCALLY**.

Lance le stack :

```bash
docker compose up -d
```

L'interface web est accessible sur `http://<IP-serveur>:8501`.

### Générer le fichier cookies.txt

Depuis les changements de 2024-2025 sur YouTube, les téléchargements anonymes sont de plus en plus limités. HomeTube recommande vivement d'utiliser un fichier `cookies.txt` authentifié. Voici la méthode la plus simple :

1. Installe l'extension **Get cookies.txt LOCALLY** dans Chrome ou Firefox.
2. Connecte-toi à YouTube avec ton compte Google.
3. Clique sur l'extension, choisis "Export as Netscape", et sauvegarde le fichier sous `./cookies/cookies.txt` dans ton dossier HomeTube.
4. Redémarre le conteneur pour qu'il prenne en compte le fichier : `docker compose restart`.

Ce fichier contient tes tokens de session. Garde-le secret et ne le versionne jamais dans Git. Un `chmod 600 ./cookies/cookies.txt` sur l'hôte est une bonne pratique.

### Vérifier les permissions

HomeTube tourne par défaut avec l'UID 1000. Si ton dossier de téléchargements appartient à un autre utilisateur, les écritures échoueront silencieusement. Pour corriger :

```bash
ls -ld ~/hometube/downloads
# Si le propriétaire n'est pas ton utilisateur :
sudo chown -R $(id -u):$(id -g) ~/hometube/downloads
```

Ou adapte les variables `PUID` et `PGID` dans le `docker-compose.yml` pour correspondre à l'utilisateur propriétaire de ton stockage media.

## Intégration avec Jellyfin ou Plex

Le vrai intérêt de HomeTube réside dans son organisation automatique. Pour que Jellyfin ou Plex détectent immédiatement les nouveaux fichiers, il faut harmoniser les volumes.

### Exemple avec Jellyfin

Supposons que ton conteneur [Jellyfin](/jellyfin-docker-alternative-netflix-gratuite/) monte déjà `/media/videos` pour les films et séries. Tu peux faire pointer HomeTube vers le même sous-dossier :

```yaml
volumes:
  - /media/videos/youtube:/app/downloads
```

HomeTube télécharge alors directement dans `/media/videos/youtube/`, et Jellyfin scannera automatiquement ce dossier selon la fréquence de scan configurée dans ton bibliothèque.

### Astuce : utiliser une bibliothèque "YouTube" dédiée

Dans Jellyfin, crée une bibliothèque de type **Films** ou **Émissions de TV** pointant vers `/media/videos/youtube`. Configure le scan automatique toutes les 15 minutes ou déclenche-le manuellement après une session de téléchargement.

### Nommage des fichiers

HomeTube nomme les fichiers avec un format explicite : `Titre de la vidéo [ID].mkv`. C'est lisible, unique, et compatible avec les scanners media server. Si tu actives l'option de processing avancé, tu peux même forcer l'extension MP4 et l'intégration des sous-titres pour une compatibilité maximale avec les clients Jellyfin.

## Configuration web UI

L'interface Streamlit est minimaliste mais complète. Voici les réglages importants à vérifier lors du premier lancement :

1. **Dossier de téléchargement** : vérifie qu'il pointe bien vers `/app/downloads` (ou ton montage perso).
2. **Qualité vidéo** : laisse "Best Quality" par défaut. Si tu veux réduire la taille, choisis une limite de résolution (1080p max par exemple).
3. **Format de sortie** : MKV est le défaut. Passe en MP4 si tes clients Jellyfin ont des soucis avec les conteneurs MKV.
4. **Sous-titres** : active l'embed des sous-titres pour les vidéos étrangères. C'est propre et évite les fichiers `.srt` qui polluent le dossier.
5. **Cookies** : indique le chemin `/app/cookies/cookies.txt` si tu as monté le volume. Sans ça, YouTube bloquera rapidement les téléchargements massifs.
6. **Arguments yt-dlp custom** : ici tu peux ajouter des flags comme `--proxy`, `--max-filesize 2G`, ou `--no-playlist` selon tes besoins.

## HomeTube vs yt-dlp en ligne de commande

Pourquoi ne pas simplement utiliser `yt-dlp` directement ? C'est une question légitime, surtout si tu es à l'aise en terminal.

| Critère | yt-dlp CLI | HomeTube Docker |
|---|---|---|
| Interface | Terminal | Web (Streamlit) |
| Organisation fichiers | Manuelle (scripts) | Automatique (media-server ready) |
| Playlist sync | Possible avec cron + scripts | Natif avec suivi résilient |
| Processing vidéo | ffmpeg manuel | Intégré (cut, subtitles, convert) |
| Accessibilité réseau | Local uniquement | Accessible depuis tout appareil sur le réseau |
| Cookies | Fichier `--cookies-from-browser` | Interface de configuration web |

Mon avis : si tu télécharges occasionnellement une vidéo, yt-dlp CLI est suffisant. Si tu gères une bibliothèque, des playlists de chaînes, et que tu veux que ta famille puisse aussi ajouter des vidéos depuis son téléphone, HomeTube est le bon compromis. C'est le même moteur (yt-dlp) mais avec une couche d'organisation qui fait gagner des heures.

## Astuces avancées

### Automatiser les mises à jour

L'image `latest` de HomeTube est régulièrement mise à jour pour suivre les évolutions yt-dlp et corriger les changements de YouTube. Pour ne pas avoir à vérifier manuellement, configure [Watchtower](/watchtower-mise-a-jour-docker-auto/) :

```yaml
  watchtower:
    image: containrrr/watchtower
    container_name: watchtower
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - WATCHTOWER_POLL_INTERVAL=86400
      - WATCHTOWER_INCLUDE_STOPPED=true
```

Watchtower vérifie une fois par jour et redémarre HomeTube avec la dernière image si une nouvelle version est disponible.

### Reverse proxy avec Traefik

Si tu exposes HomeTube sur Internet (ou sur ton réseau local avec un nom de domaine interne), passe par un reverse proxy. Voici les labels Traefik à ajouter au service HomeTube :

```yaml
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.hometube.rule=Host(`hometube.monlab.local`)"
      - "traefik.http.routers.hometube.entrypoints=websecure"
      - "traefik.http.routers.hometube.tls.certresolver=letsencrypt"
      - "traefik.http.services.hometube.loadbalancer.server.port=8501"
```

N'oublie pas de retirer le binding direct du port `8501` sur l'hôte dans ce cas, Traefik gère tout.

### Sécuriser avec authentification

L'interface Streamlit de HomeTube ne propose pas nativement d'authentification. Si tu l'exposes sur Internet, place-la derrière un [reverse proxy avec authentification](/traefik-reverse-proxy-docker/) (Traefik + Forward Auth, ou Nginx + Authelia) pour éviter que n'importe qui puisse télécharger des vidéos sur ton serveur.

### Surveillance des téléchargements

HomeTube logue ses activités dans le dossier config. Pour monitorer la santé du conteneur et l'espace disque restant sur ton volume de téléchargements, un outil comme [Beszel](/beszel-monitoring-docker/) ou Netdata est pertinent. Le disque plein est l'ennemi numéro un des téléchargeurs auto-hébergés.

## Dépannage rapide

| Problème | Cause probable | Solution |
|---|---|---|
| Erreur 403 sur YouTube | Signature expirée / blocage IP | Importe un fichier cookies.txt à jour |
| Téléchargement très lent | Throttling YouTube | Utilise `--throttled-rate` dans les args custom yt-dlp |
| Fichier MKV illisible sur client | Codec incompatible | Force la conversion MP4 dans les options avancées |
| Playlist ne se synchronise pas | Dossier config supprimé | Ne jamais supprimer `./config`, il contient la DB de sync |
| Container redémarre en boucle | Permission sur le dossier downloads | Vérifie que PUID/PGID correspondent à l'utilisateur propriétaire du volume |

## Conclusion

HomeTube n'est pas révolutionnaire dans son moteur, c'est du yt-dlp, et yt-dlp reste le meilleur outil de téléchargement vidéo du monde open-source. Mais HomeTube est révolutionnaire dans son **usage** : il transforme un outil de power-user en un service familial, accessible depuis un navigateur, parfaitement intégré à ton homelab media.

Si tu as déjà [Jellyfin](/jellyfin-docker-alternative-netflix-gratuite/) ou Plex, et que tu cherches un moyen élégant d'y injecter du contenu web organisé, HomeTube mérite sa place dans ton `docker-compose.yml`. Une image, deux volumes, et ton canapé devient une fenêtre sur tout le web vidéo.
