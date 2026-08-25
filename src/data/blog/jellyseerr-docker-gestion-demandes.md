---
title: "Jellyseerr Docker : gestion des demandes médias pour Jellyfin/Plex"
description: "Déploie jellyseerr docker pour gérer les demandes médias sur Jellyfin et Plex. Guide complet avec docker-compose fonctionnel et intégration *arr."
pubDatetime: "2026-08-22T06:00:00.000Z"
modDatetime: "2026-08-22T06:00:00.000Z"
author: Brandon Visca
tags:
  - auto-hebergement
  - docker
  - mediacenter
  - debutant
featured: false
draft: false
focusKeyword: jellyseerr docker
faqs:
  - question: "Jellyseerr fonctionne-t-il avec Plex et Jellyfin ?"
    answer: "Oui, Jellyseerr supporte nativement Jellyfin et Plex. Il suffit de connecter ton serveur média dans les paramètres pour synchroniser les bibliothèques et les utilisateurs."
  - question: "Quelle est la différence entre Jellyseerr et Ombi ?"
    answer: "Jellyseerr est le fork officiel d'Overseerr adapté à Jellyfin, avec une interface plus moderne et une meilleure intégration *arr. Ombi est plus ancien et moins actif en développement."
  - question: "Jellyseerr a-t-il besoin d'une base de données externe ?"
    answer: "Non, Jellyseerr utilise une base SQLite interne. Aucun conteneur MariaDB ou PostgreSQL n'est nécessaire, ce qui simplifie le déploiement Docker."
  - question: "Peut-on restreindre les demandes par utilisateur ?"
    answer: "Oui, Jellyseerr propose des quotas de demandes configurables par rôle utilisateur. Tu peux limiter le nombre de films ou séries demandées par semaine ou par mois."
ogImage: ""
---
> 💡 **TL;DR**
> - Jellyseerr = interface web pour que ta famille demande films/séries sur Jellyfin ou Plex
> - Un conteneur Docker, pas de base de données externe, prêt en 5 minutes
> - S'intègre avec Radarr/Sonarr pour automatiser les téléchargements

## Table des matières

## Qu'est-ce que Jellyseerr et pourquoi l'utiliser

Tu as monté ton [Jellyfin comme serveur média](/jellyfin-docker-alternative-netflix-gratuite/), tout roule. Sauf que ta famille et tes amis te bombardent de messages : « Tu peux rajouter la saison 2 de ça ? », « Y a pas tel film ? ».

**Jellyseerr résout ce problème.** C'est une interface web où tes utilisateurs peuvent chercher et demander eux-mêmes du contenu. Tu gardes la main sur ce qui est accepté, et si tu branches [Radarr](/radarr-docker-gestion-films/) et Sonarr, le téléchargement se fait tout seul. Pour un déploiement rapide, la solution jellyseerr docker est idéale : un seul conteneur, pas de base de données externe.

Jellyseerr est le fork d'Overseerr (initialement réservé à Plex) adapté à Jellyfin. Même code, même interface soignée, mais avec un support natif des deux serveurs média.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose
- Un serveur Jellyfin ou Plex déjà configuré
- (Optionnel) Radarr et Sonarr pour l'automatisation
- 1 Go de RAM minimum pour le conteneur

## Jellyseerr Docker : installation avec Docker Compose

Crée un dossier `jellyseerr` et un fichier `docker-compose.yml` :

```yaml
services:
  jellyseerr:
    image: fallenbagel/jellyseerr:latest
    container_name: jellyseerr
    restart: unless-stopped
    ports:
      - "5055:5055"
    volumes:
      - ./config:/app/config
    environment:
      - LOG_LEVEL=info
      - TZ=Europe/Paris
    networks:
      - mediacenter

networks:
  mediacenter:
    external: true
```

Puis lance le conteneur :

```bash
docker compose up -d
```

Accède à l'interface sur `http://IP_DU_SERVEUR:5055` et suis le wizard de configuration.

**Pourquoi `mediacenter` en réseau externe ?** Si tu suis les bonnes pratiques de [Docker pour débutants](/docker-debutant-services-auto-heberger/), tu partages un réseau Docker entre Jellyseerr, Jellyfin, Radarr et Sonarr. Ça évite d'exposer des ports inutilement et de jouer avec les IPs.

## Configuration : connecter Jellyseerr à ton écosystème

### Étape 1 : Serveur média

Dans les paramètres « Jellyfin » ou « Plex », renseigne l'URL interne de ton serveur. Si tu utilises le réseau Docker `mediacenter`, c'est simplement `http://jellyfin:8096` ou `http://plex:32400`.

### Étape 2 : Utilisateurs

Jellyseerr importe automatiquement les comptes utilisateurs de ton serveur média. Tu peux attribuer des permissions par profil : admin, power user, ou simple utilisateur.

### Étape 3 : Services *arr (optionnel mais recommandé)

Dans les paramètres, ajoute :
- **Radarr** pour les films : URL `http://radarr:7878` et ta clé API
- **Sonarr** pour les séries : URL `http://sonarr:8989` et ta clé API

Une fois connecté, quand un utilisateur fait une demande et que tu l'approuves, Radarr ou Sonarr la récupère automatiquement. Jellyseerr surveille ensuite l'état du téléchargement et notifie l'utilisateur quand le contenu est disponible.

### Étape 4 : Notifications

Jellyseerr supporte Discord, Telegram, Slack, et webhook générique. Configure un canal Discord pour que tes utilisateurs reçoivent un message quand leur demande est acceptée ou disponible.

## Gestion des demandes au quotidien

L'interface admin te permet de :
- Approuver ou refuser les demandes individuellement
- Activer l'approbation automatique pour les utilisateurs de confiance
- Limiter les demandes par quota (ex. : 3 films par semaine)
- Voir l'état des téléchargements en cours directement dans Jellyseerr

Le moteur de recherche utilise TMDB et affiche trailers, casting, et notes. Tes utilisateurs n'ont aucune raison de demander « le film avec le gars là » sans préciser le titre.

## Jellyseerr vs Ombi : lequel choisir

| Fonctionnalité | Jellyseerr | Ombi |
| --- | --- | --- |
| Interface | Moderne, réactive | Plus datée |
| Jellyfin natif | Oui | Partiel |
| Intégration *arr | Radarr, Sonarr, Lidarr, Readarr | Radarr, Sonarr, Lidarr |
| Développement | Actif (fork Overseerr) | Ralenti |
| Base de données | SQLite intégrée | SQLite ou externe |

**Verdict :** Jellyseerr est plus agréable à utiliser et mieux maintenu. À moins que tu aies une configuration Ombi très complexe, la migration vaut le coup.

## Sécurité et bonnes pratiques

- Expose pas le port 5055 directement sur Internet. Passe par un reverse proxy (Caddy, Traefik, Nginx Proxy Manager) avec HTTPS.
- Active l'authentification locale dans Jellyseerr même si tes utilisateurs viennent de Jellyfin.
- Place Jellyseerr derrière un VPN ou un tunnel (Cloudflare Tunnel, Tailscale) si tu n'as pas besoin d'accès public.

## TL;DR du docker-compose à copier-coller

```yaml
services:
  jellyseerr:
    image: fallenbagel/jellyseerr:latest
    container_name: jellyseerr
    restart: unless-stopped
    ports:
      - "5055:5055"
    volumes:
      - ./config:/app/config
    environment:
      - LOG_LEVEL=info
      - TZ=Europe/Paris
    networks:
      - mediacenter

networks:
  mediacenter:
    external: true
```

Jellyseerr transforme le chaos des demandes en un système propre et automatisé. Tes utilisateurs sont autonomes, tu gardes le contrôle, et tu passes moins de temps à gérer des listes de films sur Messenger.
