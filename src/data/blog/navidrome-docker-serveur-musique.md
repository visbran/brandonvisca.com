---
title: "Navidrome Docker : ton Spotify auto-hébergé en 5 min"
description: "Guide Navidrome Docker : déploie un serveur musique auto-hébergé et open-source. Docker Compose complet + comparatif avec Jellyfin et Plex."
pubDatetime: "2026-06-19T08:00:00.000Z"
author: Brandon Visca
tags:
  - docker
  - auto-hebergement
  - intermediaire
  - musique
  - streaming
featured: false
draft: false
focusKeyword: navidrome docker
ogImage: "" 
---
> 💡 **TL;DR**
> - Navidrome est un serveur de musique auto-hébergé, open-source et ultra-léger qui lit MP3, FLAC, OGG et AAC
> - Tu le déploies en 5 minutes avec Docker Compose, interface web moderne et apps mobiles compatibles (Subsonic API)
> - Alternative open-source à Spotify, Plexamp et Jellyfin pour la musique uniquement, sans abonnement ni tracking
> - Docker Compose complet, tableau comparatif et astuces de config inclus ci-dessous

## Pourquoi un serveur de musique auto-hébergé ?

T'as des Go de MP3 et FLAC accumulés depuis des années. Des albums achetés sur Bandcamp, des rips de tes vieux CDs, des mixes SoundCloud téléchargés légalement, et des fichiers lossless que tu refuses de compresser parce que "on entend la différence sur un bon casque". Le tout éparpillé sur ton NAS, ton laptop, ton téléphone et trois applications différentes qui ne se parlent pas.

Spotify ? C'est pratique, mais tu paies 11€/mois pour streamer ta propre musique quand tu es hors ligne, et l'interface est de plus en plus encombrée de podcasts, d'audiobooks et de suggestions algorithmiques que tu n'as pas demandées. Apple Music c'est pareil, avec en prime l'écosystème fermé. Quant à YouTube Music, c'est l'expérience publicitaire maximale si tu ne paies pas.

Tu veux une solution qui :
- lit ta bibliothèque locale sans conversion ni upload,
- est accessible depuis n'importe quel appareil avec un navigateur ou une app,
- garde tes playlists, tes favoris et ta position de lecture synchronisés,
- supporte le streaming avec transcodage à la volée pour économiser la bande passante,
- reste 100 % sur ton infrastructure, sans abonnement ni télémétrie.

Navidrome est la réponse. Développé en Go par un passionné de musique, c'est un serveur audio ultra-léger, rapide, et conçu spécifiquement pour les collections musicales. Si tu cherches à compléter ton homelab média à côté de ton [serveur Jellyfin pour films et séries](/jellyfin-docker-alternative-netflix-gratuite/) ou ton [lecteur Kavita pour ebooks](/kavita-docker-lecteur-ebooks/), Navidrome est le chaînon manquant pour la musique.

## Qu'est-ce que Navidrome exactement ?

Navidrome n'est pas un simple indexeur de fichiers MP3. C'est un serveur de streaming musical complet avec une interface web moderne, pensée pour la consommation de musique en continu.

Voici ce qu'il propose concrètement :

- **Formats natifs multiples** : MP3, FLAC, OGG Vorbis, AAC, ALAC, WMA, WAV, Opus. Pas de conversion nécessaire, Navidrome sert directement le fichier source ou le transcode à la volée selon la bande passante disponible.
- **Interface web responsive** : interface adaptée au desktop, tablette et mobile. Lecture en continu, gestion des playlists, files d'attente, mode aléatoire et répétition.
- **Gestion des bibliothèques** : tu organises ta musique par dossiers et Navidrome scanne automatiquement pour détecter les nouveaux albums, extraire les métadonnées ID3 et récupérer les pochettes via MusicBrainz ou Last.fm.
- **Métadonnées et pochettes** : extraction automatique des tags ID3, pochettes d'album, paroles, biographies d'artistes et informations sur les albums depuis des bases de données publiques.
- **Lecture multi-appareils** : ta position de lecture, tes playlists et tes favoris suivent ton compte utilisateur. Tu reprends exactement où tu t'étais arrêté depuis n'importe quel appareil.
- **API Subsonic compatible** : Navidrome implémente l'API Subsonic, ce qui le rend compatible avec des dizaines d'apps mobiles : DSub, Ultrasonic, Substreamer, play:Sub, iSub et même Sonos via des bridges.
- **Comptes utilisateurs multiples** : crée des comptes pour ta famille ou tes amis avec des permissions sur certaines bibliothèques seulement.
- **Transcodage à la volée** : conversion automatique FLAC → MP3 ou OGG pour économiser la bande passante mobile, configurable par utilisateur.
- **Recherche rapide** : indexation interne pour retrouver un artiste, un album ou un titre en quelques millisecondes.
- **Scrobbling Last.fm** : envoi automatique de tes écoutes vers Last.fm pour les stats et les recommandations.
- **Smart playlists** : playlists dynamiques basées sur des critères (joué récemment, jamais joué, favoris, etc.).
- **Partage** : liens publics pour partager un album ou une playlist avec des amis sans leur donner accès à toute ta bibliothèque.

Le projet est open-source sous licence GPL-3.0, maintenu activement sur le repo `navidrome/navidrome` avec plus de 12 000 stars sur GitHub. L'image Docker officielle `deluan/navidrome` est publiée sur Docker Hub avec support amd64, arm64 et armv7. Si tu débutes avec Docker, commence par mon guide sur [les services essentiels à auto-héberger](/docker-debutant-services-auto-heberger/) pour bien poser les bases avant d'ajouter Navidrome à ta stack.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose installés (Docker Engine 24+ recommandé)
- 1 cœur CPU et 256 Mo de RAM minimum (512 Mo recommandé pour le transcodage)
- 1 Go d'espace disque pour l'application, puis selon ta collection musicale
- Un nom de domaine ou sous-domaine si tu veux HTTPS en frontal
- Un reverse proxy (Caddy, Traefik ou Nginx Proxy Manager) pour gérer les certificats SSL

Navidrome est incroyablement léger. Un Raspberry Pi 3 avec 1 Go de RAM suffit pour servir une bibliothèque de plusieurs milliers d'albums à plusieurs utilisateurs simultanés. Pour un usage confortable avec transcodage FLAC, un petit VPS de 1 cœur / 1 Go est amplement suffisant. C'est l'un des serveurs média les plus économes en ressources que j'ai testé.

## Déploiement Navidrome avec Docker Compose

Crée un dossier dédié et un fichier `docker-compose.yml` :

```bash
mkdir -p ~/navidrome && cd ~/navidrome
```

Voici le Docker Compose complet et prêt à l'emploi :

```yaml
services:
  navidrome:
    image: deluan/navidrome:latest
    container_name: navidrome
    restart: unless-stopped
    user: "1000:1000"
    environment:
      - ND_SCANSCHEDULE=1h
      - ND_LOGLEVEL=info
      - ND_SESSIONTIMEOUT=24h
      - ND_BASEURL=/
      - ND_ENABLETRANSCODINGCONFIG=true
      - ND_TRANSCODINGCACHESIZE=100MB
    ports:
      - "4533:4533"
    volumes:
      - ./data:/data
      - /path/to/your/music:/music:ro
```

Explications des variables d'environnement :

- `ND_SCANSCHEDULE=1h` : scan automatique de la bibliothèque toutes les heures pour détecter les nouveaux albums
- `ND_LOGLEVEL=info` : niveau de log, passe à `debug` si tu cherches un problème
- `ND_SESSIONTIMEOUT=24h` : durée de session avant déconnexion automatique
- `ND_ENABLETRANSCODINGCONFIG=true` : active la configuration du transcodage depuis l'interface web
- `ND_TRANSCODINGCACHESIZE=100MB` : taille du cache de transcodage

**Points importants :**

- Remplace `/path/to/your/music` par le chemin réel de ta collection musicale sur le serveur hôte
- Le volume `/music` est monté en lecture seule (`:ro`) pour éviter toute modification accidentelle
- Le dossier `./data` stocke la base de données SQLite, les caches et les pochettes téléchargées
- Le port par défaut est `4533`, à adapter si tu as déjà un service dessus

### Le fichier .env recommandé

Pour séparer les secrets et les configs, crée un fichier `.env` à côté du `docker-compose.yml` :

```bash
# .env
PUID=1000
PGID=1000
MUSIC_PATH=/mnt/music
DATA_PATH=./data
PORT=4533
```

Et adapte le `docker-compose.yml` :

```yaml
services:
  navidrome:
    image: deluan/navidrome:latest
    container_name: navidrome
    restart: unless-stopped
    user: "${PUID}:${PGID}"
    environment:
      - ND_SCANSCHEDULE=1h
      - ND_LOGLEVEL=info
      - ND_SESSIONTIMEOUT=24h
      - ND_ENABLETRANSCODINGCONFIG=true
      - ND_TRANSCODINGCACHESIZE=100MB
    ports:
      - "${PORT}:4533"
    volumes:
      - ${DATA_PATH}:/data
      - ${MUSIC_PATH}:/music:ro
```

### Lancement

```bash
docker compose up -d
```

Navidrome démarre en quelques secondes. Accède à l'interface via `http://<ip-serveur>:4533` et crée le compte administrateur au premier démarrage.

### Organisation des fichiers musicaux

Navidrome lit ta bibliothèque telle qu'elle est organisée sur le disque. Une structure claire aide l'extraction des métadonnées :

```
/music/
├── Artistes/
│   ├── Pink Floyd/
│   │   ├── The Dark Side of the Moon/
│   │   │   ├── 01 - Speak to Me.mp3
│   │   │   ├── 02 - Breathe.mp3
│   │   │   └── cover.jpg
│   │   └── The Wall/
│   └── Daft Punk/
│       ├── Discovery/
│       └── Random Access Memories/
└── Compilations/
    └── Best of 2025/
```

Les tags ID3 sont prioritaires sur la structure des dossiers. Si tes fichiers sont bien tagués, Navidrome les classe correctement même si les dossiers sont un peu chaotiques.

## Configuration initiale

Au premier démarrage, Navidrome te demande de créer un compte admin. Une fois connecté :

1. **Scan de la bibliothèque** : va dans Settings > Library et clique sur "Scan Now" ou attends le scan automatique (`ND_SCANSCHEDULE=1h`)
2. **Création d'utilisateurs** : Settings > Users pour ajouter des comptes famille/amis
3. **Configuration du transcodage** : Settings > Transcoding pour activer la conversion à la volée (MP3 192k par défaut, configurable)
4. **Scrobbling Last.fm** : Settings > Personal pour connecter ton compte Last.fm
5. **Dossier playlists** : Navidrome détecte automatiquement les fichiers `.m3u` et `.m3u8` dans ta bibliothèque

Le scan initial peut prendre du temps selon la taille de ta collection. Pour 10 000 titres, compte 5 à 10 minutes. Les scans suivants sont incrémentaux et quasi instantanés.

## Navidrome vs Jellyfin vs Plex : le match pour la musique

Tous les trois gèrent la musique, mais leur approche diffère. Voici le comparatif brut pour t'aider à choisir.

| Critère | Navidrome | Jellyfin | Plex |
|---------|-----------|----------|------|
| **Prix** | Gratuit, open-source (GPL-3.0) | Gratuit, open-source | Gratuit (limité) ou Plex Pass 5€/mois |
| **Ressources** | ~50 Mo RAM | ~300 Mo RAM | ~500 Mo+ RAM |
| **Interface musique** | Dédiée, optimisée audio | Généraliste (films + musique) | Généraliste, lourde |
| **Apps mobiles** | DSub, Ultrasonic, Substreamer (gratuites) | App Jellyfin (gratuite) | Plexamp (Plex Pass requis) |
| **Transcodage** | À la volée, configurable | Oui, plus gourmand | Oui, limité sans Plex Pass |
| **API Subsonic** | Native, complète | Non | Non |
| **Scrobbling Last.fm** | Natif | Plugin | Plugin, limité sans Pass |
| **Smart playlists** | Oui, basées sur critères | Non | Oui, avec Plex Pass |
| **Paroles** | Oui, via API | Non | Oui, avec Plex Pass |
| **Multi-utilisateurs** | Oui, permissions par bibliothèque | Oui, avancé | Oui, limité sans Pass |
| **Partage public** | Oui, liens directs | Non | Oui, limité |
| **Installation Docker** | 1 conteneur, 5 min | 1 conteneur, 10 min | 1 conteneur, compte obligatoire |
| **Vie privée** | Zero télémétrie | Zero télémétrie | Télémétrie, compte Plex obligatoire |

**Verdict :**

- **Tu veux un serveur musique dédié, léger, avec apps mobiles gratuites** → **Navidrome** ✅
- **Tu veux un serveur média unique pour films, séries ET musique** → **Jellyfin** ✅
- **Tu veux la meilleure app mobile (Plexamp) et tu paies** → Plex (mais tu perds en vie privée)

**Mon avis perso** : Navidrome fait 100 % du job pour la musique, avec une empreinte mémoire ridicule comparée à Jellyfin et Plex. Si tu as déjà Jellyfin pour la vidéo, ajouter Navidrome pour la musique coûte quasi zéro en ressources et te donne une expérience audio bien supérieure. C'est la combinaison que je recommande.

## Astuces et optimisations

### Configurer le transcodage FLAC → MP3 pour le mobile

Par défaut, Navidrome sert les fichiers en qualité originale. Sur mobile en 4G, c'est du gâchis de bande passante. Configure un profil de transcodage dans Settings > Transcoding :

```
Nom : MP3 192k
Format : mp3
Bitrate : 192
Commande : ffmpeg -i %s -map 0:0 -b:a %b -v 0 -f mp3 -
```

Active ce profil dans ton compte utilisateur mobile. Le FLAC reste stocké tel quel sur le serveur, mais est transcodé à la volée pour le streaming.

### Activer le scrobbling Last.fm

Dans Settings > Personal, connecte ton compte Last.fm. Tes écoutes sont envoyées automatiquement, ce qui alimente tes stats et tes recommandations sans que Navidrome ne sache quoi que ce soit de tes habitudes.

### Utiliser une app mobile Subsonic

L'interface web de Navidrome est correcte, mais les apps mobiles dédiées sont plus fluides. Mes préférences :

- **Android** : Ultrasonic (gratuit, open-source) ou DSub
- **iOS** : play:Sub (payant une fois, ~3€) ou Substreamer (gratuit)
- **Desktop** : l'interface web suffit, ou Sublime Music (Linux)

Toutes ces apps se connectent via l'URL de ton serveur + tes identifiants Navidrome. L'API Subsonic est standardisée, donc n'importe quelle app compatible fonctionne.

### Sauvegarder la base de données

La base SQLite de Navidrome est dans `./data/navidrome.db`. Sauvegarde-la régulièrement :

```bash
# Backup quotidien via cron
cp ~/navidrome/data/navidrome.db ~/backups/navidrome-$(date +%Y%m%d).db
```

Les pochettes et métadonnées sont recréables depuis les tags ID3, mais les playlists et la position de lecture sont dans cette base. Ne la perds pas.

### Scanner manuellement après un gros ajout

Si tu viens de copier 50 albums et que tu ne veux pas attendre le scan automatique :

```bash
docker exec navidrome curl -X POST http://localhost:4533/api/scan
```

Ou via l'interface web : Settings > Library > Scan Now.

### Sécuriser avec un reverse proxy

N'expose jamais Navidrome directement sur Internet. Utilise Caddy, Traefik ou Nginx Proxy Manager pour gérer HTTPS. Exemple avec Caddy :

```
music.tondomaine.com {
    reverse_proxy localhost:4533
}
```

Caddy génère automatiquement le certificat Let's Encrypt. Si tu cherches un guide complet sur Caddy avec Docker, j'ai déjà couvert le sujet sur le blog.

## Problèmes courants et solutions

**La bibliothèque reste vide après le scan**
Vérifie que le chemin `/music` dans le conteneur pointe bien vers tes fichiers. Exécute `docker exec -it navidrome ls /music` pour confirmer. Vérifie aussi les permissions : l'utilisateur `1000:1000` doit pouvoir lire le dossier.

**Les pochettes ne s'affichent pas**
Navidrome récupère les pochettes depuis MusicBrainz et Last.fm. Si un album n'a pas de pochette, vérifie que tes tags ID3 contiennent un champ `Album Artist` correct. Tu peux aussi placer un fichier `cover.jpg` ou `folder.jpg` dans le dossier de l'album.

**Le transcodage ne fonctionne pas**
Navidrome utilise FFmpeg pour le transcodage. Vérifie que l'image Docker inclut FFmpeg (la version `latest` l'inclut nativement). Si tu utilises une image custom, monte le binaire FFmpeg dans le conteneur.

**Les apps mobiles ne se connectent pas**
Vérifie que l'URL du serveur est accessible depuis le réseau de ton téléphone. Si tu es en HTTPS, assure-toi que le certificat est valide (pas de self-signed sur mobile, c'est galère). Le format d'URL est `https://music.tondomaine.com` avec login/mot de passe Navidrome.

## Conclusion

Navidrome est l'un des services les plus impressionnants que j'ai ajoutés à mon homelab cette année. En 5 minutes de Docker Compose, tu obtiens un serveur musical complet, compatible avec des dizaines d'apps mobiles, qui consomme moins de 50 Mo de RAM et ne demande aucun compte tiers.

Pour la musique, il bat Jellyfin et Plex sur la légèreté, la simplicité et la découvrabilité via l'API Subsonic. Si tu cherches à compléter ta stack média auto-hébergée, c'est le choix évident.

Déploie-le, scanne ta bibliothèque, télécharge Ultrasonic ou DSub sur ton téléphone, et redécouvre ta collection musicale sans algorithme ni publicité. C'est une liberation. Si tu préfères les jeux vidéo rétro à la musique, j'ai aussi publié un guide sur [Romm Docker](/romm-docker-retro-gaming/), un gestionnaire de ROMs auto-hébergé qui organise tes jeux avec pochettes et métadonnées.
