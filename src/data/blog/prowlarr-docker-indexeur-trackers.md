---
title: "Prowlarr Docker : indexeur de trackers pour Radarr et Sonarr"
description: "Déploie Prowlarr avec Docker pour centraliser tes indexeurs de trackers et les synchroniser automatiquement avec Radarr et Sonarr."
pubDatetime: "2026-08-28T06:00:00.000Z"
modDatetime: "2026-08-28T06:00:00.000Z"
author: Brandon
tags:
  - docker
  - auto-hebergement
  - intermediaire
  - radarr
  - sonarr
  - prowlarr
featured: false
draft: false
focusKeyword: prowlarr docker
ogImage: ""
---
> 💡 **TL;DR**
> - Prowlarr centralise la gestion de tous tes indexeurs de trackers en un seul point.
> - Grâce à Docker Compose, tu le déploies en 5 minutes et il synchronise tout avec Radarr et Sonarr.
> - Plus besoin d'ajouter manuellement tes trackers dans chaque application : Prowlarr le fait pour toi.

Tu as déployé [Radarr](/radarr-docker-gestion-films/) pour tes films et [Sonarr](/sonarr-docker-gestion-series/) pour tes séries. Tu passes ton temps à ajouter les mêmes indexeurs dans chaque outil, à vérifier si un tracker est encore accessible, à mettre à jour tes clés d'API à la main ? **Prowlarr** est la solution à ce cauchemar administratif. C'est un indexeur de trackers qui centralise la gestion de tes sources et les pousse automatiquement vers toutes tes applications du stack mediacenter.

Dans ce tutoriel, on déploie Prowlarr avec Docker, on configure les indexeurs, on le lie à Radarr et Sonarr, et on automatise la synchro. Rien de superflu, que de la technique qui marche.

## Table des matières

## Qu'est-ce que Prowlarr et pourquoi l'utiliser ?

Prowlarr fait partie de la famille *Arr (Radarr, Sonarr, Lidarr, Readarr, Whisparr) développée par le même groupe. Son rôle est simple mais crucial :

- **Centraliser la gestion de tes indexeurs** : tu ajoutes un tracker une fois dans Prowlarr, et il le pousse vers Radarr, Sonarr, et les autres.
- **Synchronisation automatique** : quand tu ajoutes, modifies ou supprimes un indexeur, Prowlarr met à jour toutes les applications connectées sans intervention manuelle.
- **Support natif de nombreux trackers** : torrents (publics et privés), Usenet (NZB), et même certains trackers spécialisés.
- **Gestion des états de santé** : Prowlarr vérifie régulièrement si tes trackers répondent et t'alerte en cas de problème.
- **Recherche unifiée** : tu peux rechercher un fichier directement depuis Prowlarr pour voir quel tracker le propose, sans passer par chaque app.

Concrètement, au lieu d'ouvrir Radarr pour ajouter un tracker, puis Sonarr pour refaire la même manip, puis Lidarr si tu l'utilises, tu fais tout une seule fois dans Prowlarr. C'est un gain de temps énorme et une réduction drastique des erreurs de configuration.

## Prérequis

Avant de lancer le conteneur, vérifie que tu as :

- Docker et Docker Compose installés sur ton serveur.
- Un réseau Docker commun pour ton stack mediacenter (on utilisera `mediacenter` comme dans les autres guides).
- [Radarr](/radarr-docker-gestion-films/) et/ou [Sonarr](/sonarr-docker-gestion-series/) déjà déployés et fonctionnels.
- Un client de téléchargement (qBittorrent, Transmission, SABnzbd…) configuré.
- Les dossiers partagés pour tes médias et tes téléchargements (`/data/movies`, `/data/tv`, `/data/downloads` par exemple).

## Docker Compose : le déploiement

Crée un dossier dédié pour Prowlarr et place ton `docker-compose.yml` à l'intérieur :

```bash
mkdir -p ~/docker/prowlarr && cd ~/docker/prowlarr
```

Voici la configuration Docker Compose optimale pour Prowlarr :

```yaml
services:
  prowlarr:
    image: lscr.io/linuxserver/prowlarr:latest
    container_name: prowlarr
    restart: unless-stopped
    networks:
      - mediacenter
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Paris
    volumes:
      - ./config:/config
    ports:
      - "9696:9696"

networks:
  mediacenter:
    external: true
```

**Points importants :**

- **PUID / PGID** : adapte `1000` à l'UID et GID de ton utilisateur (`id $USER`). C'est essentiel pour que Prowlarr puisse lire et écrire dans les volumes sans problème de permissions.
- **Réseau externe** : on utilise le réseau `mediacenter` déjà créé pour Radarr, Sonarr, qBittorrent, Jellyfin, etc. Cela permet à Prowlarr de communiquer avec les autres services par leur nom de conteneur.
- **Pas de binding de dossiers médias** : contrairement à Radarr ou Sonarr, Prowlarr n'a pas besoin d'accéder aux fichiers. Il gère uniquement les indexeurs et communique via les API.

Pour créer le réseau si ce n'est pas déjà fait :

```bash
docker network create mediacenter
```

Lance le stack :

```bash
docker compose up -d
```

Prowlarr est maintenant accessible sur `http://<IP_SERVEUR>:9696`.

## Configuration initiale

### Premier accès

Ouvre `http://<IP_SERVEUR>:9696` dans ton navigateur. Prowlarr ne demande pas de mot de passe par défaut, alors **sécurise immédiatement l'accès** :

1. Va dans **Settings** → **General**.
2. Active **Authentication** sur `Forms (Login page)`.
3. Définis un **Username** et un **Password** solides.
4. Enregistre avec **Save Changes**.

### Configuration du proxy inverse (optionnel mais recommandé)

Si tu utilises déjà Traefik ou Caddy pour tes autres services, ajoute Prowlarr avec un sous-domaine propre (`prowlarr.tondomaine.com`). Cela te permet d'accéder à Prowlarr depuis l'extérieur de manière sécurisée et d'intégrer [Jellyseerr](/jellyseerr-docker-gestion-demandes/) ou d'autres outils qui communiquent via HTTPS.

Exemple avec Traefik (labels à ajouter au service) :

```yaml
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.prowlarr.rule=Host(`prowlarr.tondomaine.com`)"
      - "traefik.http.routers.prowlarr.entrypoints=https"
      - "traefik.http.routers.prowlarr.tls.certresolver=letsencrypt"
      - "traefik.http.services.prowlarr.loadbalancer.server.port=9696"
```

## Ajout des indexeurs

C'est le cœur du système. Va dans **Indexers** → **Add Indexer**.

Prowlarr propose une liste impressionnante de trackers. Tu peux filtrer par protocole (Torrent ou Usenet), langue, catégorie, et statut (public/privé).

### Indexeurs publics

Pour les trackers publics (1337x, YTS, ThePirateBay, etc.), la configuration est généralement simple :

1. Sélectionne le tracker dans la liste.
2. Prowlarr remplit automatiquement l'URL de base.
3. Ajoute un **Name** personnalisé si tu veux (ex: `1337x - Films`).
4. Règle le **Sync Profile** sur `Standard` pour commencer.
5. Clique sur **Test** pour vérifier que Prowlarr arrive à joindre le tracker.
6. Si le test réussit, clique sur **Save**.

### Indexeurs privés

Pour les trackers privés, la configuration est plus stricte :

1. Sélectionne ton tracker privé dans la liste.
2. Renseigne tes identifiants selon ce que demande le tracker :
   - **Cookie** (copié depuis ton navigateur)
   - **Username / Password**
   - **API Key** ou **Passkey**
3. Configure le nombre de **Download Slots** si le tracker l'impose.
4. Certains trackers privés nécessitent de cocher "Use Full Season RSS" pour les séries.
5. **Test** impérativement avant de sauvegarder.

**Conseil** : ne surcharge pas Prowlarr avec 50 indexeurs. 5 à 10 trackers bien choisis (mix publics/privés selon tes besoins) suffisent largement et réduisent le temps de recherche.

### Paramètres des indexeurs

Dans **Settings** → **Indexers**, tu peux régler :

- **Minimum Seeders** : ignore les torrents avec moins de seeders (ex: 1 ou 2).
- **Retention** : pour l'Usenet, le nombre de jours pendant lesquels l'article est disponible.
- **Query Limit** et **Grab Limit** : évite de surcharger les trackers, surtout les privés qui ont des quotas.
- **RSS Sync Interval** : fréquence de rafraîchissement des flux RSS. Par défaut 15 minutes, tu peux descendre à 10 sur les trackers publics.

## Synchronisation avec Radarr et Sonarr

Là où Prowlarr devient vraiment puissant, c'est dans la synchro avec tes applications. Va dans **Settings** → **Apps**.

### Ajouter Radarr

1. Clique sur **Add Application**.
2. Sélectionne **Radarr**.
3. Remplis les champs :
   - **Name** : `Radarr`
   - **Prowlarr Server** : l'URL de ton instance Prowlarr (ex: `http://prowlarr:9696` si même réseau Docker, ou `https://prowlarr.tondomaine.com` si via reverse proxy)
   - **Radarr Server** : l'URL de Radarr (`http://radarr:7878` ou `https://radarr.tondomaine.com`)
   - **API Key** : la clé API de Radarr (disponible dans Radarr → Settings → General)
   - **Sync Profile** : `Standard`
   - **Sync Categories** : coche `Movies`
4. Clique sur **Test**. Si c'est vert, clique sur **Save**.

Prowlarr va immédiatement pousser tous les indexeurs configurés vers Radarr. Tu peux le vérifier en ouvrant Radarr → Settings → Indexers : tes trackers apparaissent comme par magie.

### Ajouter Sonarr

La procédure est identique :

1. **Add Application** → **Sonarr**.
2. **Sonarr Server** : `http://sonarr:8989`
3. **API Key** : depuis Sonarr → Settings → General.
4. **Sync Categories** : coche `TV`.
5. **Test** puis **Save**.

Tu peux aussi connecter Lidarr (musique), Readarr (livres), Whisparr ou d'autres applications compatibles si tu les utilises.

### Gérer la synchro

Dans **Settings** → **Apps**, tu vois l'état de chaque connexion. Le bouton **Sync App Indexers** force une synchronisation immédiate. C'est utile quand tu ajoutes un nouvel indexeur et que tu veux le propager tout de suite.

**Important** : les modifications faites directement dans Radarr ou Sonarr (ajout/suppression d'un indexeur) ne sont pas remontées vers Prowlarr. Prowlarr est le maître. Si tu veux ajouter un tracker, fais-le dans Prowlarr et laisse-le synchroniser.

## Intégration avec Jellyseerr et Jellyfin

Si tu utilises [Jellyseerr](/jellyseerr-docker-gestion-demandes/) pour gérer les demandes de tes utilisateurs, le workflow devient encore plus fluide :

1. Un utilisateur demande un film sur Jellyseerr.
2. Jellyseerr envoie la demande à Radarr.
3. Radarr demande à Prowlarr de chercher sur les trackers configurés.
4. Prowlarr retourne les résultats à Radarr.
5. Radarr envoie le téléchargement au client BitTorrent/Usenet.
6. Le fichier arrive, Radarr le renomme et le déplace.
7. [Jellyfin](/jellyfin-docker-alternative-netflix-gratuite/) scanne le dossier et le film apparaît dans la bibliothèque.

Le tout est entièrement automatisé. Toi, tu dors. Le stack travaille.

## Configuration avancée

### Gestion des tags et des restrictions

Dans **Settings** → **Restrictions**, tu peux définir des règles globales :

- **Must Contain** : mots obligatoires dans les releases (ex: `FRENSCHDUB` si tu veux du doublage français).
- **Must Not Contain** : mots à exclure (ex: `CAM`, `TS`, `HDTS` pour éviter les versions caméra).
- **Preferred Words** : privilégie certaines sources (ex: `BluRay` > `Web-DL`).

Ces restrictions s'appliquent à la recherche dans Prowlarr, mais attention : c'est Radarr et Sonarr qui ont le dernier mot sur les critères de qualité et de profils.

### Notifications

Prowlarr peut t'alerter en cas de problème. Va dans **Settings** → **Notifications** et configure par exemple :

- **Discord** : webhook pour recevoir les alertes dans un canal dédié.
- **Telegram** : bot pour les notifications mobiles.
- **Email** : si tu préfères le classique SMTP.

### Sauvegarde

Le dossier `./config` contient toute la configuration de Prowlarr. Sauvegarde-le régulièrement avec le reste de ton stack. Si tu utilises Beszel, Netdata ou un autre outil de monitoring, vérifie que le dossier est inclus dans ta stratégie de backup.

## FAQ

### Prowlarr ne synchronise pas mes indexeurs vers Radarr, pourquoi ?

Vérifie d'abord l'URL et la clé API de Radarr dans Prowlarr (Settings → Apps). Assure-toi que les deux conteneurs sont sur le même réseau Docker (`mediacenter`). Teste la connexion avec le bouton **Test** : si tu as une erreur de timeout, c'est probablement un problème de réseau ou de firewall.

### Prowlarr affiche "Unable to connect to indexer", que faire ?

Ce message indique que le tracker ne répond pas ou a changé d'adresse. Vérifie :
- Si c'est un tracker public, l'URL de base est peut-être bloquée par ton FAI. Utilise un DNS non filtrant comme [AdGuard Home](/adguard-home-docker-guide-2026/) ou configure un VPN sur ton routeur.
- Si c'est un tracker privé, ton compte est peut-être banni ou la méthode d'authentification a changé.
- Vérifie aussi que le tracker n'est pas en maintenance en consultant leur page officielle ou un forum.

### Est-ce que Prowlarr remplace Jackett ?

Oui et non. Prowlarr est le successeur "officiel" dans l'écosystème *Arr et offre une intégration native bien plus propre que Jackett. Cependant, Jackett supporte encore plus de trackers que Prowlarr. Si un tracker très spécifique n'est pas dans Prowlarr, tu peux utiliser Jackett comme intermédiaire et l'ajouter comme indexer custom dans Prowlarr. Mais dans 95% des cas, Prowlarr suffit amplement.

### Puis-je utiliser Prowlarr sans Radarr/Sonarr ?

Techniquement oui, Prowlarr a une fonction de recherche manuelle qui te permet de trouver des releases directement. Cependant, son véritable intérêt réside dans la synchronisation automatique avec les applications *Arr. Sans cela, tu perds l'essentiel de sa valeur.

### Prowlarr consomme-t-il beaucoup de ressources ?

Non. Prowlarr est très léger. En usage normal, il consomme moins de 200 Mo de RAM et une fraction de CPU. Les pics surviennent uniquement pendant les synchros massives ou quand tu lances une recherche manuelle sur plusieurs trackers simultanément.

## Conclusion

Prowlarr est le ciment qui relie toutes les briques de ton mediacenter. En centralisant la gestion de tes indexeurs et en synchronisant automatiquement avec Radarr, Sonarr et le reste de l'écosystème, il t'évite des heures de configuration répétitive et réduit les erreurs humaines.

Déployé en quelques minutes avec Docker Compose, il s'intègre parfaitement à ton stack existant. Si tu as déjà mis en place Radarr et Sonarr, ajouter Prowlarr n'est pas une option, c'est une évidence.

Maintenant, ton mediacenter est complet : [Jellyfin](/jellyfin-docker-alternative-netflix-gratuite/) pour la lecture, Radarr pour les films, Sonarr pour les séries, [Jellyseerr](/jellyseerr-docker-gestion-demandes/) pour les demandes, et Prowlarr pour orchestrer les trackers. Tu n'as plus qu'à choisir ce que tu veux regarder ce soir.
