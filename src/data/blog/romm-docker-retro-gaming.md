---
author: Brandon
pubDatetime: "2026-07-12T08:00:00.000Z"
modDatetime: "2026-07-12T08:00:00.000Z"
title: "Romm Docker : gestionnaire de ROMs et rétro-gaming auto-hébergé"
slug: romm-docker-retro-gaming
featured: false
draft: false
tags:
  - debutant
  - auto-hebergement
  - docker
  - retro-gaming
  - emulation
focusKeyword: "romm docker"
description: "Guide Romm Docker : déploie un gestionnaire de ROMs rétro-gaming auto-hébergé. Docker Compose complet, scan auto et intégration émulateurs."
ogImage: ""
faqs:
  - question: "Romm supporte-t-il les jeux multi-disques ?"
    answer: "Oui, Romm regroupe automatiquement les fichiers multi-disques placés dans un sous-dossier commun. Une seule fiche est créée avec un sélecteur de disque."
  - question: "Faut-il un compte IGDB pour utiliser Romm ?"
    answer: "Oui, le scraping des métadonnées nécessite un compte développeur Twitch gratuit pour obtenir un IGDB_CLIENT_ID et IGDB_CLIENT_SECRET. Sans cela, Romm scanne mais n'enrichit pas les jeux."
  - question: "Romm peut-il lancer les jeux directement dans le navigateur ?"
    answer: "Romm intègre EmulatorJS pour certains systèmes 8 et 16 bits. Pour les consoles plus exigeantes, il génère des liens vers des émulateurs locaux comme RetroArch ou DuckStation."
---

> 💡 **TL;DR**
> - Romm est un gestionnaire de ROMs rétro-gaming auto-hébergé, open-source, qui scanne, identifie et organise tes jeux avec métadonnées et pochettes
> - Tu le déploies en 10 minutes avec Docker Compose : conteneur Romm + MariaDB + Redis, stack complète et prête à l'emploi
> - Support de 60+ plateformes (Nintendo, Sega, Sony, Arcade), intégration IGDB/MobyGames pour les métadonnées, et liaison avec émulateurs web
> - Docker Compose complet, structure de dossiers, tips de scan et intégration émulateurs inclus ci-dessous

## Table des matières

## Pourquoi un gestionnaire de ROMs auto-hébergé ?

T'as des Go de ROMs accumulés depuis des années. Des dumps de tes cartouches Game Boy, des ISOs de tes jeux PS1 gravés sur CD-R, des packs MAME téléchargés légalement depuis des archives abandonware, et des homebrews indépendants. Le tout éparpillé sur ton NAS, tes disques durs externes et trois dossiers zippés dont tu as oublié le contenu.

Les émulateurs existent, mais gérer une collection de plusieurs milliers de ROMs reste un cauchemar. Tu lances RetroArch, tu parcours un explorateur de fichiers à dix niveaux de profondeur, tu ne sais plus si c'est la version US ou la version PAL qui fonctionne, et ta bibliothèque ressemble à un garage numérique sans étiquettes.

Tu veux une solution qui :
- scanne tes dossiers de ROMs automatiquement et identifie chaque jeu,
- télécharge les pochettes, descriptions et métadonnées depuis des bases publiques,
- présente tes jeux dans une interface web moderne avec recherche et filtres,
- gère les multi-discs, les versions alternatives et les traductions fan-made,
- reste 100 % sur ton infrastructure, sans abonnement ni télémétrie.

Romm est la réponse. Développé par zurdi15 et la communauté, c'est le chaînon manquant entre ton dossier `ROMS/` et une vraie bibliothèque de jeux rétro gérée par Romm Docker. Si tu cherches à compléter ton homelab média à côté de ton [serveur Komga pour BD et mangas](/komga-docker-bd-manga-auto-heberge/) ou de ton [Navidrome pour la musique](/navidrome-docker-serveur-musique/), Romm est le pendant gaming de ta stack auto-hébergée.

## Qu'est-ce que Romm exactement ?

Romm n'est pas un simple explorateur de fichiers avec des thumbnails. C'est un gestionnaire de bibliothèque de jeux rétro complet, pensé pour les collectionneurs et les amateurs d'émulation.

Voici ce qu'il propose concrètement :

- **Support de 60+ plateformes** : Nintendo (NES, SNES, N64, GB, GBA, DS, 3DS, Switch), Sega (Master System, Mega Drive, Saturn, Dreamcast), Sony (PS1, PS2, PSP), Microsoft (Xbox), Arcade (MAME, Neo-Geo), PC (DOS, ScummVM), et bien d'autres. Romm reconnaît les extensions courantes : `.zip`, `.7z`, `.iso`, `.bin`, `.cue`, `.chd`, `.nds`, `.gba`, `.n64`, etc.
- **Identification automatique** : scan de tes dossiers avec hash matching (CRC, MD5, SHA-1) contre les bases de données IGDB et MobyGames. Romm identifie le jeu exact, y compris la région, la version et le hack.
- **Métadonnées et pochettes** : téléchargement automatique des jaquettes front/back, screenshots, descriptions, dates de sortie, éditeurs, genres, et notes. L'interface présente tes jeux comme une vraie bibliothèque, pas comme une liste de fichiers.
- **Multi-fichiers et multi-discs** : gestion des jeux sur plusieurs disques (Final Fantasy VII, Metal Gear Solid), des versions alternatives (beta, prototype, traduction), et des DLCs.
- **Collections et listes personnalisées** : crée des collections thématiques ("Shmups", "RPGs Japonais", "Jeux de mon enfance") pour organiser des jeux de différentes plateformes.
- **Tags et statuts** : marque les jeux comme "En cours", "Terminé", "Abandonné", "À tester". Filtrage par statut, genre, plateforme ou note.
- **Interface web responsive** : interface Vue.js moderne, adaptée au desktop, tablette et mobile. Recherche instantanée, filtres avancés, vue grille et vue liste.
- **Émulation dans le navigateur** : intégration possible avec des émulateurs web (EmulatorJS, Ruffle) pour jouer directement depuis le navigateur sans installer d'émulateur local.
- **Multi-utilisateurs** : crée des comptes pour tes amis ou ta famille avec des permissions par bibliothèque. L'un voit les jeux Nintendo, l'autre les jeux Arcade.
- **Scan planifié** : surveillance automatique des dossiers pour détecter les nouveaux ajouts et les indexer sans intervention.
- **API REST** : documentation Swagger incluse pour automatiser l'ajout de ROMs, la gestion des collections ou l'intégration avec d'autres outils.

Le projet est open-source sous licence GPL-3.0, maintenu activement sur le repo `zurdi15/romm` avec plus de 4 000 stars sur GitHub. L'image Docker officielle `rommapp/romm` est publiée sur Docker Hub avec support amd64 et arm64. Si tu débutes avec Docker, commence par mon guide sur [les services essentiels à auto-héberger](/docker-debutant-services-auto-heberger/) pour bien structurer ton environnement avant d'ajouter Romm Docker à ta stack.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose installés (Docker Engine 24+ recommandé)
- 1 cœur CPU et 1 Go de RAM minimum (2 Go recommandés pour le scan de grosses collections)
- 2 Go d'espace disque pour l'application, plus l'espace de ta collection de ROMs
- Un nom de domaine ou sous-domaine si tu veux HTTPS en frontal
- Un reverse proxy (Caddy, Traefik ou Nginx Proxy Manager) pour gérer les certificats SSL

Romm est raisonnablement léger. Un Raspberry Pi 4 avec 4 Go de RAM suffit pour indexer plusieurs milliers de ROMs et servir plusieurs utilisateurs. Pour un usage confortable avec de grosses collections et des scans fréquents, un petit VPS de 2 cœurs / 2 Go est amplement suffisant.

## Déploiement Romm Docker avec Docker Compose

Crée un dossier dédié et un fichier `docker-compose.yml` :

```bash
mkdir -p ~/romm && cd ~/romm
```

Voici le Docker Compose complet et prêt à l'emploi :

```yaml
services:
  romm:
    image: rommapp/romm:latest
    container_name: romm
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - DB_HOST=romm-db
      - DB_PORT=3306
      - DB_USER=romm
      - DB_PASSWD=romm_password_change_me
      - DB_NAME=romm
      - REDIS_HOST=romm-redis
      - REDIS_PORT=6379
      - REDIS_PASSWORD=redis_password_change_me
      - ROMM_AUTH_SECRET_KEY=change_me_to_a_random_32_char_string
      - ROMM_AUTH_USERNAME=admin
      - ROMM_AUTH_PASSWORD=admin_password_change_me
      - IGDB_CLIENT_ID=votre_igdb_client_id
      - IGDB_CLIENT_SECRET=votre_igdb_client_secret
      - MOBYGAMES_API_KEY=votre_moby_api_key
    volumes:
      - ./roms:/romm/library
      - ./resources:/romm/resources
      - ./config:/romm/config
      - ./assets:/romm/assets
    depends_on:
      - romm-db
      - romm-redis

  romm-db:
    image: mariadb:10.6
    container_name: romm-db
    restart: unless-stopped
    environment:
      - MYSQL_ROOT_PASSWORD=root_password_change_me
      - MYSQL_DATABASE=romm
      - MYSQL_USER=romm
      - MYSQL_PASSWORD=romm_password_change_me
    volumes:
      - ./db:/var/lib/mysql

  romm-redis:
    image: redis:7-alpine
    container_name: romm-redis
    restart: unless-stopped
    command: redis-server --requirepass redis_password_change_me
```

Déploie la stack :

```bash
docker compose up -d
```

Attends 30 secondes que MariaDB initialise la base, puis accède à `http://<ip-serveur>:8080`.

## Explication de la configuration

**Base de données MariaDB** : Romm stocke les métadonnées, les utilisateurs, les collections et les statuts dans MariaDB. Le volume `./db` persiste les données entre les redémarrages. N'utilise pas SQLite en production : les requêtes de recherche sur des milliers de jeux sont bien plus rapides avec un moteur relationnel.

**Redis** : utilisé pour le cache des requêtes API vers IGDB/MobyGames et pour la file d'attente de scan. Redis évite de taper les APIs externes à chaque chargement de page.

**Volumes** :
- `./roms` : tes ROMs organisées par plateforme. C'est le seul volume que tu remplis avec tes jeux.
- `./resources` : fichiers téléchargés (pochettes, screenshots, manuels) par le scraper.
- `./config` : configuration de Romm, règles de scan, identifiants d'API.
- `./assets` : logos de plateformes et autres ressources graphiques.

**Variables d'environnement critiques** :
- `ROMM_AUTH_SECRET_KEY` : clé JWT pour signer les sessions. Change-la pour une chaîne aléatoire de 32 caractères minimum.
- `ROMM_AUTH_USERNAME` et `ROMM_AUTH_PASSWORD` : identifiants du compte administrateur.
- `IGDB_CLIENT_ID` et `IGDB_CLIENT_SECRET` : obligatoires pour le scraping des métadonnées. Tu les obtiens gratuitement sur [Twitch Developer Portal](https://dev.twitch.tv/console).
- `MOBYGAMES_API_KEY` : alternative à IGDB pour certaines plateformes obscures. Gratuit sur [mobygames.com](https://www.mobygames.com/).

## Structure des dossiers de ROMs

Romm attend une structure de dossiers logique. Voici l'organisation recommandée :

```text
~/romm/roms/
├── gba/
│   ├── Pokemon - Version Emeraude (France).gba
│   └── Advance Wars (USA).gba
├── snes/
│   ├── Super Mario World (USA).sfc
│   └── Chrono Trigger (Japan).sfc
├── psx/
│   ├── Final Fantasy VII (USA)/
│   │   ├── Final Fantasy VII (USA) (Disc 1).bin
│   │   ├── Final Fantasy VII (USA) (Disc 1).cue
│   │   ├── Final Fantasy VII (USA) (Disc 2).bin
│   │   └── Final Fantasy VII (USA) (Disc 2).cue
├── mame/
│   └── 1942.zip
└── nds/
    └── The Legend of Zelda - Phantom Hourglass (Europe).nds
```

Le nom du dossier parent (`gba`, `snes`, `psx`) correspond à l'identifiant de plateforme reconnu par Romm. Consulte la [documentation officielle](https://github.com/zurdi15/romm/wiki/Supported-Platforms) pour la liste complète des slugs de plateformes. Garde les noms de fichiers propres : Romm utilise le nom de fichier pour l'identification si le hash matching échoue.

## Premier scan et scraping des métadonnées

Une fois l'interface web accessible :

1. Connecte-toi avec les identifiants admin définis dans le Docker Compose.
2. Va dans **Library > Scan** et sélectionne les plateformes à scanner.
3. Romm analyse les fichiers, calcule les hashes et interroge IGDB/MobyGames.
4. Les jeux identifiés apparaissent avec leur pochette, description et note.
5. Pour les jeux non reconnus, utilise l'édition manuelle pour associer le bon titre.

Le premier scan d'une collection de plusieurs milliers de ROMs peut prendre une heure ou plus. Romm traite les fichiers en arrière-plan, tu peux naviguer dans l'interface pendant le scan. Active le scan planifié dans les paramètres pour que Romm surveille automatiquement les nouveaux ajouts toutes les heures.

## Intégration avec les émulateurs

Romm ne remplace pas ton émulateur. Il l'accompagne. Voici comment les connecter :

**Emulation web intégrée** : Romm peut lancer des émulateurs JavaScript directement dans le navigateur via EmulatorJS pour les consoles 8 et 16 bits (NES, SNES, GB, GBA, Mega Drive). Configure le plugin dans les paramètres et les jeux se lancent en un clic depuis la fiche du jeu. Attention, la performance dépend de ton navigateur et de la complexité du jeu.

**Lancement externe** : pour les consoles plus exigeantes (PS1, PS2, N64, Dreamcast), Romm génère des liens de lancement vers des émulateurs locaux via des URI handlers. Configure RetroArch, DuckStation ou PCSX2 sur ta machine pour ouvrir les ROMs depuis l'URL. C'est la méthode la plus fiable pour une expérience fluide.

**EmuDeck / Steam Deck** : si tu utilises un Steam Deck avec EmuDeck, copie ta structure de dossiers Romm dans le dossier `roms` de EmuDeck. Les deux outils partagent la même hiérarchie par plateforme. Romm sert de bibliothèque de référence et EmuDeck gère le lancement.

**Sauvegardes et states** : Romm ne gère pas directement les sauvegardes in-game. Pour ça, synchronise le dossier des saves de ton émulateur avec Syncthing ou monte-le dans le conteneur. Si tu veux une solution de synchronisation de fichiers auto-hébergée, j'ai aussi publié un guide sur [Outline, un wiki auto-hébergé](/outline-docker-wiki-auto-heberge/) qui peut servir de base de connaissances pour documenter ta config émulation.

## Astuces et bonnes pratiques

**Nommage des fichiers** : Romm identifie mieux les jeux si le nom de fichier suit le format `Titre (Région).ext`. Évite les abréviations obscures et les tags inutiles dans le nom de fichier. Garde les infos techniques (revision, version) dans des tags de fichier si possible.

**Compression** : les ROMs en `.zip` ou `.7z` sont supportées mais ralentissent le scan. Pour les petites consoles (8 et 16 bits), garde les fichiers décompressés si tu as la place. Pour les ISOs PS1/PS2, le format `.chd` (Compressed Hunks of Data) est le meilleur compromis taille/performance.

**Multi-discs** : place tous les fichiers d'un jeu multi-discs dans un sous-dossier portant le nom du jeu. Romm les regroupe automatiquement sous une seule fiche avec un sélecteur de disque.

**Sauvegardes** : sauvegarde régulièrement le volume `./db` pour ne pas perdre tes métadonnées et ta progression de scan. Le dossier `./resources` contient les images téléchargées et peut être régénéré, mais le recréer prend du temps.

**Sécurité** : expose Romm derrière un reverse proxy avec HTTPS. Le module d'authentification intégré est basique ; pour une sécurité renforcée, place Romm derrière Authelia/Authentik ou utilise un tunnel WireGuard/Tailscale. J'ai détaillé les options dans mon guide [WireGuard Docker](/wireguard-docker-vpn-homelab/). Ne laisse jamais Romm ouvert sur Internet sans HTTPS.

**Ressources** : si tu héberges aussi un serveur de streaming de jeux avec [Sunshine Docker](/sunshine-docker-streaming-jeux/), Romm complète parfaitement l'expérience en te donnant une bibliothèque organisée de tes jeux PC rétro avant de les lancer en streaming.

## Tableau comparatif avec les alternatives

| Fonctionnalité | Romm | RetroArch (dossiers) | LaunchBox | Playnite |
|---|---|---|---|---|
| Auto-hébergé | Oui | Non | Non | Non |
| Interface web | Oui | Non | Non | Non |
| Multi-utilisateurs | Oui | Non | Non | Non |
| Scraping IGDB | Natif | Via scripts | Payant | Plugin |
| Support 60+ plateformes | Oui | Oui | Oui | Oui |
| Émulation navigateur | Oui | Non | Non | Non |
| Open-source | GPL-3.0 | GPL-3.0 | Propriétaire | MIT |
| Docker natif | Oui | Non | Non | Non |

Romm est la seule solution véritablement auto-hébergée, multi-utilisateurs et accessible depuis un navigateur. LaunchBox et Playnite sont excellents sur desktop mais inaccessibles depuis un téléphone ou une tablette. Romm transforme ta collection de ROMs en bibliothèque de jeux universelle, consultable depuis n'importe quel appareil.

## Conclusion

Romm transforme ton dossier de ROMs en une vraie bibliothèque de jeux rétro. Avec son interface web moderne, son scraping automatique et son support de 60+ plateformes, c'est l'outil qu'il manquait aux collectionneurs d'émulation. Le déploiement Docker est simple, la consommation de ressources raisonnable, et l'intégration avec les émulateurs existants est fluide. Déploie-le sur ton homelab et redécouvre tes jeux d'enfance avec une organisation digne d'une vraie ludothèque.

> **À savoir :** Les ROMs de jeux commerciaux que tu ne possèdes pas physiquement relèvent généralement du piratage. Romm est un outil de gestion de bibliothèque : utilise-le avec des dumps de tes propres cartouches, des homebrews libres et des jeux abandonware distribués légalement.
