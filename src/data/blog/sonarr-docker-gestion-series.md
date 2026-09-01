---
title: "Sonarr Docker : gestion automatique de séries TV"
description: "Installe Sonarr avec Docker pour automatiser le téléchargement de tes séries. Guide sonarr docker complet avec docker-compose, config et intégration."
pubDatetime: "2026-08-27T06:00:00.000Z"
modDatetime: "2026-08-28T06:00:00.000Z"
author: Brandon Visca
tags:
  - docker
  - auto-hebergement
  - sonarr
  - mediacenter
  - intermediaire
featured: false
draft: false
focusKeyword: sonarr docker
faqs:
  - question: "Sonarr et Radarr, quelle différence ?"
    answer: "Sonarr gère les séries TV (saisons, épisodes, numérotation). Radarr gère les films. Les deux partagent la même logique, le même fonctionnement Docker et les mêmes indexeurs."
  - question: "Sonarr remplace-t-il Plex ou Jellyfin ?"
    answer: "Non. Sonarr gère le téléchargement et l'organisation. Plex/Jellyfin gèrent la lecture. Sonarr prépare les fichiers, ton serveur média les lit."
  - question: "Pourquoi Sonarr ne télécharge pas certains épisodes ?"
    answer: "Vérifie les indexeurs (dispos et testés), le profil de qualité (ex: 1080p Web-DL), le monitoring (épisode marqué Monitored), et les restrictions de release (custom formats bloquants)."
---
> 💡 **TL;DR**
> - Sonarr surveille tes séries et télécharge automatiquement les nouveaux épisodes selon tes critères.
> - Un conteneur Docker Compose simple, 5 minutes de déploiement, zéro conflit avec le système hôte.
> - Branché à qBittorrent/Transmission et Jellyfin/Plex, tu obtiens un pipeline de séries 100% autonome.

## Table des matières

## Qu'est-ce que Sonarr et pourquoi l'utiliser

Tu as déjà mis en place [Radarr pour tes films](/radarr-docker-gestion-films/) et ton serveur média tourne. Sauf que chaque semaine c'est la même galère : vérifier quels épisodes sont sortis, trouver les bons fichiers, les renommer correctement pour que Plex ou Jellyfin les reconnaissent, et surtout ne pas rater le season finale parce que tu as oublié de checker.

**Sonarr est là pour ça.** C'est un gestionnaire de séries TV open-source qui :

- Surveille tes séries préférées et détecte automatiquement les nouveaux épisodes.
- Cherche parmi tes indexeurs la meilleure release selon ton profil de qualité.
- Envoie le téléchargement à ton client BitTorrent ou Usenet.
- Renomme et déplace chaque épisode dans la bonne arborescence (`/series/Nom de la série/Saison 01/`).
- Met à jour la qualité quand une version supérieure sort (passage d'un Web-DL à un Blu-Ray par exemple).
- Gère les saisons, les épisodes spéciaux, et même les anime avec leur propre numérotation.

En gros, tu ajoutes une série une fois, et Sonarr s'occupe du reste. C'est le complément parfait de Radarr dans ton écosystème mediacenter.

## Prérequis

Avant de lancer le conteneur, assure-toi d'avoir :

- Un serveur avec Docker et Docker Compose installés. Si c'est pas encore fait, retourne sur le [guide Docker pour débutants](/docker-debutant-services-auto-heberger/) avant de continuer ton déploiement sonarr docker.
- Un client de téléchargement déjà fonctionnel (qBittorrent, Transmission, SABnzbd…). Sonarr ne télécharge pas directement, il envoie le `.torrent` ou le `.nzb` à ton client.
- Un dossier partagé pour tes médias, structuré de préférence comme `/data/series` et `/data/downloads`.
- Un réseau Docker commun pour tes services mediacenter (on va réutiliser `mediacenter`, comme pour Radarr et Jellyseerr).

## Sonarr Docker : déploiement avec Docker Compose

Crée un dossier dédié pour Sonarr et place ton `docker-compose.yml` à l'intérieur :

```bash
mkdir -p ~/docker/sonarr
cd ~/docker/sonarr
```

Voici la configuration complète :

```yaml
services:
  sonarr:
    image: lscr.io/linuxserver/sonarr:latest
    container_name: sonarr
    restart: unless-stopped
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Paris
    volumes:
      - ./config:/config
      - /data/downloads:/downloads
      - /data/series:/series
    ports:
      - "8989:8989"
    networks:
      - mediacenter

networks:
  mediacenter:
    external: true
```

**Explications rapides :**
- `PUID` et `PGID` : adapte-les selon ton utilisateur (`id $USER` pour les connaître). Sonarr doit pouvoir lire dans `/downloads` et écrire dans `/series`.
- `./config` persiste la base de données SQLite, les paramètres et la liste des séries.
- `/data/downloads` pointe vers le dossier de téléchargement de ton client BitTorrent/Usenet. Sonarr surveille ce dossier pour détecter les fichiers terminés.
- `/data/series` est ta bibliothèque finale. C'est ce dossier que Jellyfin ou Plex scanne pour afficher tes séries.
- Le réseau `mediacenter` partagé permet à Sonarr de communiquer avec qBittorrent, Radarr, [Jellyseerr](/jellyseerr-docker-gestion-demandes/) et Jellyfin sans exposer de ports supplémentaires.

Lance le conteneur :

```bash
docker compose up -d
```

En 30 secondes, Sonarr est dispo sur `http://localhost:8989`.

## Configuration initiale de Sonarr

### Paramètres généraux

Va dans **Settings > Media Management** et configure :
- **Rename Episodes** : active-le. Sonarr renomme chaque épisode au format `Nom de la Série - S01E01 - Titre de l'Épisode [Qualité]`. C'est propre, standard, et Jellyfin/Plex adorent ça.
- **Replace Illegal Characters** : oui, pour éviter les caractères foireux sur certains systèmes de fichiers.
- **Standard Episode Format** : `{Series Title} - S{season:00}E{episode:00} - {Episode Title} [{Quality Full}]`
- **Season Folder Format** : `Season {season:00}`

Dans **Settings > Profiles**, vérifie les profils de qualité existants. Le profil "Any" est trop permissif. Crée plutôt un profil "HD-1080p" ou "HD-720p" selon ton stockage et ta bande passante. Si tu as un écran 4K, tu peux créer un profil "Ultra-HD" avec une préférence pour les releases HDR.

### Ajouter un indexeur

Sans indexeur, Sonarr est aveugle. Il ne sait pas quels fichiers existent.

Va dans **Settings > Indexers** et clique sur **Add**. Les options principales :
- **Indexeurs publics** via Jackett ou Prowlarr (recommandé).
- **Indexeurs Newznab** pour l'Usenet.
- **Prowlarr** : si tu utilises déjà Prowlarr pour Radarr, ajoute Sonarr dedans. Tu configures les indexeurs une fois, et Prowlarr les synchronise avec Sonarr, Radarr, Lidarr, etc. C'est le workflow le plus propre.

Teste chaque indexeur après l'ajout. Un indexeur qui répond en timeout ralentit toutes tes recherches.

### Connecter le client de téléchargement

Dans **Settings > Download Clients**, ajoute ton client :

- **qBittorrent** : hôte `qbittorrent`, port `8080`, identifiants de connexion Web UI. Si tu ne l'as pas encore installé, j'ai un guide complet sur [qBittorrent Docker](https://brandonvisca.com/qbittorrent-docker-client-torrent/).
- **Transmission** : hôte `transmission`, port `9091`.
- **SABnzbd** : hôte `sabnzbd`, port `8080`, clé API.

Sonarr envoie le `.torrent` ou le `.nzb` au client, surveille le dossier de téléchargement, puis déplace et renomme le fichier final dans `/data/series`. Le mécanisme "Completed Download Handling" doit être activé pour que ça se fasse automatiquement.

### Ajouter des séries

Clique sur **Series > Add New**. Cherche le titre, sélectionne-la, et Sonarr récupère automatiquement :
- Le titre original et traduit.
- Le nombre de saisons et d'épisodes.
- Les affiches et métadonnées.
- Le statut de la série (en cours, terminée, annulée…).

Pour chaque série, tu choisis :
- **Le profil de qualité** (Any, HD-1080p, Ultra-HD…).
- **Le monitoring** :
  - **Monitor All** : surveille toutes les saisons, passées et futures.
  - **Monitor Future** : surveille uniquement les saisons à venir (idéal pour une série en cours).
  - **Monitor Existing** : surveille les saisons déjà sorties pour un upgrade de qualité.
  - **Unmonitor** : garde la série dans Sonarr mais ne télécharge rien.

Mon conseil : pour une série en cours de diffusion, mets "Monitor Future". Pour une série terminée que tu veux compléter, mets "Monitor All".

## Intégration avec Radarr, Jellyseerr et ton mediacenter

Sonarr ne vit pas tout seul. Il brille quand il est connecté au reste de ton écosystème.

### Avec Radarr

Radarr gère les films, Sonarr gère les séries. Les deux utilisent le même réseau Docker `mediacenter`, les mêmes indexeurs via Prowlarr, et les mêmes dossiers `/data`. Cohérence totale. Si tu as suivi le tutoriel [Radarr Docker](/radarr-docker-gestion-films/), l'intégration est immédiate. Même logique, mêmes bons réflexes.

### Avec Jellyseerr

Si tu as déployé [Jellyseerr](/jellyseerr-docker-gestion-demandes/), tes utilisateurs peuvent demander des séries via une interface web. Quand tu approuves la demande, Jellyseerr la pousse automatiquement vers Sonarr. Celui-ci :

1. Ajoute la série à sa liste.
2. Cherche parmi les indexeurs.
3. Envoie la meilleure release au client de téléchargement.
4. Renomme et déplace l'épisode dans `/data/series`.
5. Notifie Jellyseerr que l'épisode est disponible.
6. Jellyseerr prévient l'utilisateur.

Tout seul. Tu n'as qu'à approuver.

### Avec Jellyfin ou Plex

Sonarr prépare les fichiers, ton serveur média les lit. Une fois un épisode déplacé dans `/data/series`, Jellyfin ou Plex le détecte lors du prochain scan. Tu peux même configurer un webhook dans Sonarr pour forcer un scan immédiat de la bibliothèque concernée dès qu'un nouveau fichier arrive.

Pour Jellyfin : va dans **Settings > Connect** dans Sonarr, ajoute un webhook Jellyfin avec l'URL `http://jellyfin:8096` et ta clé API. Chaque nouvel épisode déclenche un scan ciblé.

## Conseils et pièges courants

### La numérotation des saisons

Certaines séries ont des saisons spéciales (épisodes de Noël, OAV, anime…) qui ne suivent pas la numérotation standard. Sonarr gère ça via les "Season 00" (épisodes spéciaux). Assure-toi que les métadonnées TMDB/TVDB correspondent bien à ton organisation de fichiers.

### Les anime

Les anime posent souvent problème à cause de la numérotation absolue (épisode 147 au lieu de S05E23). Sonarr a un mode "Anime" qui gère la numérotation absolue via des indexeurs spécialisés. Ajoute des indexeurs dédiés anime et configure le profil de langue sur "Japanese" avec sous-titres si besoin.

### Les doublons de release

Sonarr peut télécharger plusieurs versions du même épisode (Web-DL puis remplacer par Blu-Ray). Pour éviter de saturer ta connexion et ton disque :
- Configure **Upgrade Until** dans le profil de qualité (ex : arrêter à "Bluray-1080p").
- Utilise les **Custom Formats** pour privilégier certains encodeurs ou formats (x265 pour gagner de la place, x264 pour la compatibilité).

### Les permissions

Le problème le plus fréquent : Sonarr écrit dans `/data/series` avec l'utilisateur `PUID/PGID`, mais Jellyfin lit avec un autre UID. Si les permissions ne sont pas alignées, Jellyfin ne voit pas les fichiers. Solution simple : utilise le même `PUID/PGID` pour tous tes conteneurs mediacenter, ou crée un groupe commun avec les bonnes permissions (`chmod 775` sur les dossiers médias).

### Le monitoring excessif

Monitorer 50 séries avec "Monitor All" génère beaucoup de requêtes vers les indexeurs. Certains indexeurs publics limitent le nombre de requêtes par minute. Si tu vois des erreurs "Rate limited" dans les logs, réduis la fréquence de recherche dans **Settings > Indexers > RSS Sync Interval** (par défaut 15 minutes, tu peux passer à 30 ou 60).

### Backup de la config

Sonarr stocke tout dans `/config` : séries suivies, profils de qualité, historique des téléchargements. Une corruption SQLite et tu perds tout. Active le backup automatique dans **System > Backup** (intervalle recommandé : 7 jours). Et surtout, intègre le dossier `config` à ta stratégie de sauvegarde globale (BorgBackup, Restic, ou ce que tu utilises déjà).

## Dépannage rapide

### Sonarr ne trouve pas de release pour un épisode
- Vérifie que l'épisode est bien marqué "Monitored".
- Teste tes indexeurs un par un dans **Settings > Indexers**. Tu peux aussi utiliser [Prowlarr Docker](/prowlarr-docker-indexeur-trackers/) pour centraliser et synchroniser tous tes indexeurs depuis un seul point.
- Regarde les logs (System > Logs) pour voir si l'indexeur répond.
- Vérifie que la date de sortie de l'épisode est bien passée (TMDB peut indiquer une date future par erreur).

### Le fichier reste dans le dossier de téléchargement
- Vérifie que "Completed Download Handling" est activé dans **Settings > Download Clients**.
- Assure-toi que Sonarr peut lire dans `/downloads` et écrire dans `/series` (teste avec un `touch` depuis le conteneur).
- Vérifie que le client signale bien la fin du téléchargement (qBittorrent en "Pause" ne signale pas completion).

### Jellyfin ne voit pas la nouvelle saison
- Sonarr a peut-être créé un nouveau dossier de saison après le dernier scan Jellyfin. Force un scan manuel ou configure le webhook comme expliqué plus haut.
- Vérifie que le format de renommage correspond bien à ce que Jellyfin attend (`Nom - S01E01 - Titre`).

## Conclusion

Sonarr transforme la gestion de tes séries en un processus invisible. Tu ajoutes une série une fois, tu configures ton profil de qualité, et il fait le reste : recherche, téléchargement, renommage, organisation. Couplé à Docker, tu obtiens un service propre, isolé et facile à sauvegarder.

Côté client torrent, Sonarr fonctionne aussi bien avec [Transmission Docker](/transmission-docker-client-torrent/) qu'avec qBittorrent. Transmission est particulièrement pertinent si tu veux minimiser l'empreinte mémoire sur un serveur limité.

Intègre-le avec Radarr pour les films, [Jellyseerr](/jellyseerr-docker-gestion-demandes/) pour les demandes utilisateurs, et Jellyfin pour la lecture, et tu auras un mediacenter qui gère tout seul ta bibliothèque TV. Le seul truc qu'il ne fera pas à ta place, c'est choisir quelle série binge-watcher ce week-end.
