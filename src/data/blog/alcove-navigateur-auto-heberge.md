---
title: "Alcove Docker : navigateur web auto-hébergé pour homelab"
description: "Guide Alcove Docker : déploie un navigateur web auto-hébergé pour ton homelab avec Docker Compose. Reverse proxy, sécurité HTTPS et configuration complète."
pubDatetime: "2026-07-16T08:00:00.000Z"
modDatetime: "2026-07-16T08:00:00.000Z"
author: Brandon
tags:
  - debutant
  - auto-hebergement
  - alcove
  - navigateur
  - homelab
featured: false
draft: false
focusKeyword: alcove docker
ogImage: ""
---
> 💡 **TL;DR**
> - **C'est quoi ?** Un navigateur web qui tourne dans un conteneur Docker et s'affiche dans ton navigateur
> - **Pourquoi ?** Accéder à des ressources internes, tester depuis l'extérieur, fournir un accès contrôlé
> - **Comment ?** Un docker-compose.yml, quelques variables d'environnement, et c'est en ligne

## Table des matières

## Qu'est-ce qu'Alcove ?

Alcove est un navigateur web auto-hébergé qui te permet d'ouvrir des onglets de navigation directement depuis une interface web hébergée sur ton propre serveur. Pas besoin d'installer un client lourd : tout passe par le navigateur. Déployer Alcove avec Docker est la méthode la plus rapide pour l'intégrer dans un homelab existant.

Le projet s'appuie sur Chromium embarqué dans un conteneur Docker, avec une couche VNC/noVNC pour afficher l'interface graphique dans ton navigateur. C'est une solution pensée pour les homelabs : légère, rapide à déployer, et totalement sous ton contrôle.

**Stack technique :**
- Chromium comme moteur de rendu
- noVNC pour l'accès web
- Debian comme base d'image Docker
- Accès par port web standard

## Pourquoi utiliser Alcove Docker dans ton homelab

C'est pas juste pour faire joli. Voici les cas concrets où ça sauve la mise :

**Accéder à des ressources internes**
Tu as un NAS, une imprimante réseau ou un outil interne qui n'est pas exposé sur Internet ? Un navigateur hébergé sur ton réseau local peut y accéder directement, sans VPN supplémentaire.

**Tester depuis l'extérieur**
Besoin de vérifier qu'un site répond bien depuis un autre réseau ? Tu ouvres Alcove depuis ton téléphone en 4G, et tu testes en temps réel.

**Isoler ta navigation**
Chaque session est dans un conteneur jetable. Tu veux tester un lien douteux ou consulter un site sans laisser de traces ? Ferme l'onglet, le conteneur repart à zéro.

**Partager un accès contrôlé**
Tu peux donner un accès navigateur à un collègue ou un membre de ta famille sans lui confier tes identifiants VPN.

## Docker Compose : le fichier complet

Crée un dossier dédié :

```bash
mkdir -p ~/docker/alcove && cd ~/docker/alcove
```

Voici le `docker-compose.yml` complet et fonctionnel :

```yaml
services:
  alcove:
    image: lscr.io/linuxserver/chromium:latest
    container_name: alcove
    restart: unless-stopped
    security_opt:
      - seccomp:unconfined
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Paris
      - CHROME_CLI=https://github.com/linuxserver/docker-chromium
    volumes:
      - ./config:/config
    ports:
      - "3000:3000"
      - "3001:3001"
    shm_size: "1gb"
```

Lance le conteneur :

```bash
docker compose up -d
```

En 30 secondes, Alcove est disponible sur `http://ton-serveur:3000`.

**Explications des choix :**

- `seccomp:unconfined` : Chromium a besoin de permissions étendues pour fonctionner correctement dans un conteneur
- `shm_size: "1gb"` : alloue suffisamment de mémoire partagée pour éviter les crashs de Chromium (le défaut 64 Mo est trop juste)
- Ports 3000 (interface web) et 3001 (optionnel, HTTPS interne)
- Le volume `./config` persiste les favoris et la session

## Configuration des variables d'environnement

Les variables clés à adapter :

| Variable | Valeur par défaut | Description |
|---|---|---|
| `PUID` | `1000` | UID de l'utilisateur propriétaire des fichiers |
| `PGID` | `1000` | GID du groupe |
| `TZ` | `Etc/UTC` | Fuseau horaire (ex : Europe/Paris) |
| `CHROME_CLI` | URL vide | Page d'accueil au lancement |

Pour trouver ton PUID/PGID :

```bash
id -u  # PUID
id -g  # PGID
```

Tu peux aussi passer des arguments Chromium personnalisés via la variable `CHROME_CLI` :

```yaml
      - CHROME_CLI=--window-size=1920,1080 --start-maximized
```

Ou ouvrir directement un site interne au démarrage :

```yaml
      - CHROME_CLI=https://192.168.1.1
```

## Accès et utilisation

Ouvre `http://ton-serveur:3000` dans ton navigateur.

L'interface noVNC te présente un bureau minimal avec Chromium lancé. Tu navigues comme sur un PC classique : onglets, barre d'adresse, favoris. La différence ? Tout tourne sur ton serveur.

**Astuce :** Si tu utilises un reverse proxy, expose seulement le port 3000. Le port 3001 sert surtout en interne.

Si tu débutes avec Docker, mon guide sur [les services essentiels à auto-héberger avec Docker](/docker-debutant-services-auto-heberger/) t'explique tout depuis l'installation.

## Sécurité : HTTPS et reverse proxy

**Ne laisse jamais Alcove accessible en HTTP brut sur Internet.** Voici comment sécuriser l'accès.

### Avec Traefik

Si tu utilises déjà Traefik, j'ai un guide complet sur [Traefik v3](/traefik-reverse-proxy-docker/). Ajoute ces labels à ton service :

```yaml
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.alcove.rule=Host(`alcove.tondomaine.fr`)"
      - "traefik.http.routers.alcove.entrypoints=websecure"
      - "traefik.http.routers.alcove.tls.certresolver=letsencrypt"
      - "traefik.http.services.alcove.loadbalancer.server.port=3000"
      - "traefik.http.routers.alcove.middlewares=auth@docker"
```

### Avec Caddy

```text
alcove.tondomaine.com {
    reverse_proxy alcove:3000
}
```

### Authentification basique

Ajoute une couche de protection simple avant d'exposer quoi que ce soit. Avec Traefik :

```yaml
      - "traefik.http.middlewares.alcove-auth.basicauth.users=admin:$$apr1$$..."
```

Ou place Alcove derrière ton VPN ([WireGuard Docker](/wireguard-docker-vpn-homelab/)) pour un accès sécurisé sans exposer le service sur Internet.

## Alcove vs les alternatives

Il existe d'autres solutions de navigation distante auto-hébergées :

| Solution | Technologie | Poids | Usage idéal |
|---|---|---|---|
| **Alcove** | Chromium + noVNC | Léger | Navigation quotidienne, ressources internes |
| **Neko** | Chromium/Firefox + WebRTC | Moyen | Streaming, sessions partagées avec audio |
| **SealSkin** | Conteneurs desktop | Lourd | Apps complètes, pas juste un navigateur |
| **linuxserver/webtop** | Bureau complet | Très lourd | Bureau à distance, pas juste un navigateur |

**Mon avis :** Alcove gagne si tu cherches juste un navigateur accessible depuis le web. C'est plus léger qu'une VM ou un bureau complet, et ça consomme moins de RAM qu'une solution WebRTC. Si tu as besoin d'audio/vidéo en temps réel, Neko est meilleur. Pour un tableau de bord qui centralise l'accès à Alcove et tes autres services, j'ai publié un guide sur [Homer Dashboard Docker](/homer-dashboard-docker-homelab/).

## Checklist sécurité

Avant d'exposer Alcove :

- [ ] HTTPS forcé via reverse proxy
- [ ] Authentification basique ou VPN obligatoire
- [ ] PUID/PGID corrects pour les permissions fichiers
- [ ] `shm_size` à 1 Go minimum
- [ ] Container mis à jour régulièrement (`docker compose pull && docker compose up -d`)
- [ ] Backup du dossier `config/` pour les favoris

## FAQ

### Quelle est la différence entre Alcove et un bureau à distance ?

Alcove se limite à un navigateur web dans un conteneur. Un bureau à distance te donne accès à tout le système. C'est plus léger, plus rapide à démarrer, et ça expose moins de surface d'attaque.

### Est-ce que Alcove conserve l'historique de navigation ?

Oui, si tu montes un volume Docker sur `./config`. Sans volume, les données disparaissent à chaque redémarrage du conteneur. Pour une navigation éphémère, ne monte pas de volume persistant.

### Peut-on utiliser Alcove sur un Raspberry Pi ?

L'image `linuxserver/chromium` supporte les architectures ARM64. Sur un Raspberry Pi 4 ou 5 avec 4 Go de RAM minimum, ça fonctionne. Le Pi 3 manque de RAM pour être confortable.

### Alcove est-il sécurisé pour consulter des sites bancaires ?

Non. Même auto-hébergé, ce n'est pas un environnement certifié pour la bureautique sensible. Utilise-le pour tester, accéder à des ressources internes, ou naviguer de façon isolée, jamais pour des données critiques.

## Conclusion

Alcove est un outil simple mais redoutablement utile dans un homelab. Il te donne un navigateur accessible depuis n'importe quel appareil, isolé dans un conteneur, et totalement sous ton contrôle. Pour quelques centaines de méga de RAM, tu gagnes une flexibilité que ni Chrome ni Firefox ne peuvent offrir.
