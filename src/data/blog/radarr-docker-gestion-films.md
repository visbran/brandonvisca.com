---
title: "Radarr Docker : gestion automatique de films pour ton mediacenter"
description: "Déploie Radarr avec Docker pour automatiser la gestion de tes films : téléchargement, renommage, qualité et organisation sans lever le petit doigt."
pubDatetime: "2026-08-25T06:00:00.000Z"
modDatetime: "2026-08-28T06:00:00.000Z"
author: Brandon Visca
tags:
  - docker
  - auto-hebergement
  - radarr
  - mediacenter
  - intermediaire
featured: false
draft: false
focusKeyword: radarr docker
faqs: []
---
> 💡 **TL;DR**
> - Radarr surveille automatiquement les sorties films et les télécharge selon tes critères de qualité.
> - Une stack Docker Compose te permet de le déployer en 5 minutes, propre et isolée.
> - Branché à un client de téléchargement et [Jellyfin](https://brandonvisca.com/jellyfin-docker-alternative-netflix-gratuite/), tu obtiens un mediacenter 100% autonome.

Tu as déjà mis en place [Jellyfin sur Docker](https://brandonvisca.com/jellyfin-docker-alternative-netflix-gratuite/) et tu passes tes soirées à chercher manuellement les nouveaux films pour compléter ta bibliothèque ? Arrête tout. **Radarr** est l'outil qu'il te faut. C'est un gestionnaire de films qui surveille les sorties, vérifie la qualité, télécharge et organise tout seul comme un grand.

Dans ce tutoriel, on va déployer **Radarr avec Docker**, le configurer pour qu'il parle à ton client de téléchargement, et l'intégrer à ton écosystème mediacenter. Pas de blabla, que du concret.

## Table des matières

## Qu'est-ce que Radarr et pourquoi l'utiliser ?

Radarr est un gestionnaire de films open-source inspiré de [Sonarr](/sonarr-docker-gestion-series/), son cousin pour les séries. Son job :

- Surveiller les films que tu veux voir ou revoir.
- Découvrir automatiquement quand une nouvelle version est disponible (Web-DL, Blu-Ray 1080p, 4K HDR…).
- Envoyer la demande de téléchargement à ton client préféré (qBittorrent, Transmission, SABnzbd…).
- Renommer et déplacer le fichier dans la bonne arborescence, prêt à être lu par Jellyfin ou Plex.
- Mettre à jour la qualité si une version supérieure sort plus tard.

En gros, tu ajoutes un film une fois, et Radarr fait le reste. C'est comme avoir un bibliothécaire obsessionnel-compulsif qui travaille 24h/24.

## Prérequis

Avant de commencer, assure-toi d'avoir :

- Un serveur avec Docker et Docker Compose installés (si ce n'est pas le cas, reviens vite sur le [guide Docker pour débutants](https://brandonvisca.com/docker-debutant-services-auto-heberger/)).
- Un client de téléchargement déjà fonctionnel (qBittorrent, Transmission, SABnzbd…).
- Un dossier partagé pour tes médias, idéalement structuré comme `/data/movies` et `/data/downloads`.
- Un réseau Docker commun pour tes services mediacenter (on va utiliser `mediacenter`).

## Docker Compose : le déploiement

Crée un dossier dédié pour Radarr et place ton `docker-compose.yml` à l'intérieur :

```bash
mkdir -p ~/docker/radarr
cd ~/docker/radarr
```

Voici la configuration à utiliser :

```yaml
services:
  radarr:
    image: lscr.io/linuxserver/radarr:latest
    container_name: radarr
    restart: unless-stopped
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Paris
    volumes:
      - ./config:/config
      - /data/downloads:/downloads
      - /data/movies:/movies
    ports:
      - "7878:7878"
    networks:
      - mediacenter

networks:
  mediacenter:
    external: true
```

**Explications rapides :**
- `PUID`/`PGID` à adapter selon ton utilisateur (`id $USER` pour les connaître).
- `./config` persiste la base de données et les paramètres.
- `/data/downloads` doit pointer vers le dossier de téléchargement de ton client BitTorrent/Usenet.
- `/data/movies` est ta bibliothèque finale, celle que Jellyfin/Plex scanne.
- Le réseau `mediacenter` partagé permet à Radarr de communiquer avec Jellyfin, Jellyseerr et ton client de téléchargement sans exposer de ports inutiles.

Lance le conteneur :

```bash
docker compose up -d
```

En 30 secondes, Radarr est dispo sur `http://localhost:7878`.

## Configuration de Radarr

### Paramètres généraux

Va dans **Settings > Media Management** et active :
- **Rename Movies** : oui, laisse Radarr renommer proprement tes fichiers.
- **Replace Illegal Characters** : oui.
- **Standard Movie Format** : `{Movie Title} ({Release Year}) {Quality Full}` (tu peux affiner selon tes goûts).
- **Movie Folder Format** : `{Movie Title} ({Release Year})`.

Dans **Settings > Profiles**, vérifie que tu as un profil de qualité qui te correspond. Le profil par défaut "Any" est trop permissif. Crée plutôt un profil "HD-1080p" ou "HD-2160p" selon ton matos.

### Ajouter un indexeur

C'est le moteur de recherche de Radarr. Sans ça, il est aveugle.

Va dans **Settings > Indexers** et clique sur **Add**. Tu peux ajouter :
- Des indexeurs publics (Jackett/Prowlarr fait l'intermédiaire).
- Des indexeurs Newznab pour l'Usenet.
- Un instance **Prowlarr** (recommandé si tu utilises aussi Sonarr, Lidarr…).

**Astuce pro** : Prowlarr centralise tous tes indexeurs et les synchronise avec Radarr. Tu configures une seule fois, et tous tes *arr en profitent.

### Connecter le client de téléchargement

Toujours dans **Settings > Download Clients**, ajoute ton client :

- **qBittorrent** : hôte `qbittorrent`, port `8080`, identifiants de connexion Web UI. Si tu ne l'as pas encore installé, j'ai un guide complet sur [qBittorrent Docker](https://brandonvisca.com/qbittorrent-docker-client-torrent/).
- **Transmission** : hôte `transmission`, port `9091`.
- **SABnzbd** : hôte `sabnzbd`, port `8080`, clé API.

Radarr va envoyer le `.torrent` ou le `.nzb` au client, surveiller le dossier de téléchargement, puis déplacer/renommer le fichier final dans `/data/movies`.

### Ajouter des films

Clique sur **Movies > Add New**. Cherche un titre, sélectionne-le, et Radarr récupère automatiquement :
- Le titre original et traduit.
- L'année de sortie.
- L'affiche et les métadonnées.
- Le statut de sortie (annoncé, en salles, sorti en digital, Blu-Ray…).

Tu peux ajouter des films manuellement, ou laisser une autre application (comme [Jellyseerr](https://brandonvisca.com/jellyseerr-docker-gestion-demandes/)) les pousser automatiquement vers Radarr.

## Intégration avec Jellyseerr et ton mediacenter

Si tu as suivi le tutoriel [Jellyseerr Docker](https://brandonvisca.com/jellyseerr-docker-gestion-demandes/), tu sais déjà que tes utilisateurs peuvent demander des films via une interface web. Quand une demande est approuvée, Jellyseerr la transmet à Radarr. Celui-ci :

1. Cherche parmi tes indexeurs.
2. Envoie le meilleur candidat au client de téléchargement.
3. Attend que le fichier arrive.
4. Le renomme, le déplace, et signale à Jellyseerr que c'est prêt.
5. Jellyseerr notifie l'utilisateur.

Résultat : tu n'as **strictement rien à faire**. Tu es juste là pour valider les demandes et regarder les logs si ça coince.

## Les bons réflexes

### Qualité avant quantité

Radarr peut télécharger plusieurs versions du même film (Web-DL, puis remplacer par le Blu-Ray). Ça consomme de la bande passante et de l'espace disque. Deux options :
- **Upgrade Until** : dans le profil de qualité, dis-lui de s'arrêter à "Bluray-1080p" par exemple.
- **Custom Formats** : crée des règles pour privilégier certaines releases (ex. : x265 pour gagner de la place, ou x264 pour la compatibilité).

### Le monitoring adapté

Quand tu ajoutes un film, tu as trois modes :
- **Monitor Movie** : Radarr surveille et télécharge dès qu'une version sort.
- **Monitor Existing** : il ne télécharge que si la version actuelle est en dessous de ton profil de qualité.
- **Unmonitor** : il garde l'entrée mais ne télécharge rien.

Pour un film sorti depuis 10 ans, "Monitor Existing" est généralement suffisant. Pour un blockbuster à venir, "Monitor Movie" te garantit le téléchargement dès la sortie digitale.

### Backup automatique

Radarr stocke toute sa config dans `/config`. Mais une base SQLite corrompue, c'est vite arrivé. Active le backup interne dans **System > Backup** (cocher "Backup Interval"), ou mieux, ajoute le dossier `config` à ta stratégie de sauvegarde (Restic, BorgBackup, ce que tu veux).

## Dépannage rapide

### Radarr ne trouve pas de release
- Vérifie que tes indexeurs sont bien configurés et accessibles. Pour les gérer et synchroniser automatiquement avec Sonarr depuis un seul point, j'ai testé [Prowlarr Docker](/prowlarr-docker-indexeur-trackers/).
- Regarde les **logs** (System > Logs > Files) pour voir si l'indexeur répond.
- Assure-toi que le film est bien taggé "Monitored".

### Le fichier reste dans le dossier de téléchargement
- Radarr attend que le client signale la fin du téléchargement. Vérifie que "Completed Download Handling" est activé dans **Settings > Download Clients**.
- Problème de permissions ? Le conteneur doit pouvoir lire dans `/downloads` et écrire dans `/movies`.

### Jellyfin ne voit pas le nouveau film
- Radarr a peut-être renommé le dossier après le scan Jellyfin. Dans Jellyfin, lance un scan manuel ou configure le webhook Jellyfin dans Radarr pour forcer le rafraîchissement automatique.

## Conclusion

Radarr transforme ton serveur en véritable cinémathèque autonome. Une fois configuré, il gère les recherches, les téléchargements, le renommage et l'organisation sans que tu aies à intervenir. Couplé à Docker, tu obtiens un service propre, reproductible et facile à sauvegarder.

Intègre-le avec Jellyfin pour la lecture et [Jellyseerr](https://brandonvisca.com/jellyseerr-docker-gestion-demandes/) pour les demandes utilisateurs, et tu auras un mediacenter qui ferait pâlir n'importe quel service de streaming payant. Le seul truc qu'il ne fera pas à ta place, c'est choisir le film du vendredi soir.
