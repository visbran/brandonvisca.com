---
title: "Tsdproxy Docker : reverse proxy automatique Tailscale pour conteneurs"
description: Tsdproxy Docker expose tes conteneurs via Tailscale sans config manuelle. Reverse proxy auto avec labels Docker. Guide complet.
pubDatetime: "2026-07-09T08:00:00.000Z"
modDatetime: "2026-07-09T08:00:00.000Z"
author: Brandon Visca
tags:
  - intermediaire
  - reseau
  - docker
  - tailscale
  - auto-hebergement
featured: false
draft: false
focusKeyword: tsdproxy docker
faqs:
  - question: "Tsdproxy nécessite-t-il un domaine public ?"
    answer: "Non. Tsdproxy utilise le réseau mesh Tailscale. Chaque service reçoit un nom de machine visible uniquement sur ton tailnet. Pas besoin d'acheter un nom de domaine ni d'ouvrir les ports 80/443 sur ta box."
  - question: "Quelle est la différence entre Tsdproxy et Traefik + Tailscale ?"
    answer: "Tsdproxy détecte automatiquement les conteneurs Docker et crée les entrées Tailscale serve sans aucune configuration manuelle. Traefik nécessite des labels Docker et un Caddyfile ou des fichiers de conf pour gérer les routes. Tsdproxy est l'outil idéal si tu veux zero-config."
  - question: "Tsdproxy fonctionne-t-il avec plusieurs nœuds ?"
    answer: "Oui, dans la mesure où chaque nœud exécute son instance Tsdproxy et que les conteneurs partagent le réseau Tailscale. Cependant, Tsdproxy est conçu pour un déploiement mono-nœud simple. Pour du multi-nœud complexe, Traefik reste pertinent."
  - question: "Puis-je utiliser Tsdproxy sans Docker ?"
    answer: "Non. Tsdproxy est conçu spécifiquement pour Docker. Il écoute les événements du socket Docker et génère les configs Tailscale serve à la volée. Sans Docker, il n'a rien à surveiller."
ogImage: ""
---
> 💡 **TL;DR**
> - Tsdproxy expose automatiquement tes conteneurs Docker sur ton réseau Tailscale sans écrire un seul fichier de conf
> - Un label `tsdproxy.enable=true` suffit pour créer une entrée DNS dans ton tailnet
> - Plus besoin de configurer `tailscale serve` manuellement pour chaque service
> - Zéro port ouvert sur Internet, zéro domaine public, zéro Certbot

## Table des matières

## Pourquoi Tsdproxy Docker change tout pour Tailscale

Tailscale est déjà une merveille. Tu as un réseau mesh sécurisé entre tes appareils, tu n'ouvres aucun port sur ta box, et tout communique comme si tu étais sur le même LAN. Mais quand tu veux exposer un service Docker (un dashboard, un wiki, un serveur de musique) à ton tailnet sans le rendre public sur Internet, tu arrives à la case manuelle.

La méthode classique, c'est de taper `tailscale serve --bg --set-path=/ monservice 8080` pour chaque conteneur. Si tu en as cinq, c'est cinq commandes. Si tu en rajoutes un sixième dans deux semaines, tu as oublié la syntaxe et tu retournes sur la doc. Si tu supprimes un conteneur, tu dois nettoyer les routes à la main. C'est pénible.

**Tsdproxy docker** résout ce problème en automatisant l'intégration entre Docker et Tailscale. Il écoute les événements Docker (création, suppression de conteneurs) et met à jour les routes Tailscale serve automatiquement. Tu ajoutes un label dans ton `docker-compose.yml`, tu lances le conteneur, et paf : ton service est accessible sur `http://mon-service.ton-tailnet.ts.net` depuis n'importe quel appareil connecté à Tailscale.

C'est particulièrement utile si tu as déjà adopté [WireGuard pour ton VPN](/wireguard-docker-vpn-homelab/) et que tu cherches une couche de publication de services encore plus simple pour ton homelab interne. Pas de certificats SSL à gérer, pas de DNS public à configurer, pas de reverse proxy à maintenir. Si tu débutes avec Docker, mon [guide pour les débutants](/docker-debutant-services-auto-heberger/) t'explique comment monter ta stack avant d'ajouter Tsdproxy.

## Tsdproxy Docker, c'est quoi exactement ?

Tsdproxy est un reverse proxy automatique écrit en Go par almeidap (dépôt GitHub `almeidap/tsdproxy`). Son fonctionnement est simple : il tourne dans un conteneur tsdproxy docker avec accès au socket Docker et à la CLI Tailscale. Quand il détecte un conteneur avec le label `tsdproxy.enable=true`, il crée automatiquement une règle `tailscale serve` qui expose le port interne du conteneur sur le tailnet.

**Ce qu'il fait bien :**
- Découverte automatique des conteneurs via Docker labels
- Création et suppression dynamique des routes Tailscale serve
- Nommage automatique basé sur le nom du conteneur ou un label personnalisé
- Aucune exposition sur Internet, tout reste dans le tailnet
- Zéro fichier de configuration statique à maintenir

**Ce qu'il ne fait pas :**
- Pas de gestion de certificats HTTPS personnalisés (Tailscale gère TLS natif)
- Pas de load balancing avancé (un conteneur = une route)
- Pas de découverte Kubernetes (c'est Docker pur)

## Prérequis

Avant de déployer Tsdproxy, assure-toi d'avoir :

- Docker et Docker Compose installés sur ton serveur
- Un compte Tailscale et le client installé sur le serveur hôte
- Le serveur déjà autorisé dans ton tailnet (`tailscale up` effectué)
- Les conteneurs Docker que tu veux exposer sur un réseau Docker commun

Si tu utilises Tailscale en mode `--accept-dns=true` (par défaut), les noms de machine seront résolus automatiquement dans ton tailnet. Pas besoin de toucher à un DNS externe.

## Le Docker Compose

Voici le fichier `docker-compose.yml` minimal pour déployer Tsdproxy. Il doit tourner sur le même hôte que les conteneurs que tu veux exposer, avec accès au socket Docker et au daemon Tailscale.

```yaml
services:
  tsdproxy:
    image: ghcr.io/almeidap/tsdproxy:latest
    container_name: tsdproxy
    restart: unless-stopped
    environment:
      - TSD_API_KEY=tskey-api-XXXXXXXXXXXXXXXXXXXX
      - TSD_EPHEMERAL=false
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /var/lib/tailscale:/var/lib/tailscale
    networks:
      - proxy

networks:
  proxy:
    external: true
```

**Points importants :**
- `TSD_API_KEY` : génère une clé API depuis la console Tailscale (Settings > Keys > Auth Keys > Generate). Choisis une clé réutilisable ou éphémère selon tes besoins.
- `/var/run/docker.sock` : obligatoire pour que Tsdproxy détecte les conteneurs. Monté en read-only pour limiter les risques.
- `/var/lib/tailscale` : permet à Tsdproxy d'interagir avec le daemon Tailscale existant sur l'hôte.
- Le réseau `proxy` doit être externe et partagé avec les services que tu veux exposer.

Crée le réseau avant de lancer :

```bash
docker network create proxy
```

Lance Tsdproxy :

```bash
docker compose up -d
```

## Configurer les labels Docker

Voici la partie magique. Pour exposer un conteneur sur ton tailnet, tu n'as besoin que de deux labels dans son `docker-compose.yml` :

```yaml
services:
  uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: uptime-kuma
    restart: unless-stopped
    volumes:
      - uptime-kuma-data:/app/data
    networks:
      - proxy
    labels:
      - "tsdproxy.enable=true"
      - "tsdproxy.port=3001"
```

Résultat : Uptime Kuma est accessible à `http://uptime-kuma.ton-tailnet.ts.net` depuis n'importe quel appareil connecté à Tailscale. Aucune commande manuelle, aucun fichier de config.

Tu peux aussi personnaliser le nom de la machine avec `tsdproxy.name` :

```yaml
    labels:
      - "tsdproxy.enable=true"
      - "tsdproxy.port=8080"
      - "tsdproxy.name=mon-dashboard"
```

L'URL deviendra alors `http://mon-dashboard.ton-tailnet.ts.net`.

Un autre exemple avec [Jellyfin](/jellyfin-docker-alternative-netflix-gratuite/) :

```yaml
  jellyfin:
    image: jellyfin/jellyfin:latest
    container_name: jellyfin
    restart: unless-stopped
    volumes:
      - jellyfin-config:/config
      - /mnt/media:/media:ro
    networks:
      - proxy
    labels:
      - "tsdproxy.enable=true"
      - "tsdproxy.port=8096"
```

Si tu utilises [Caddy](/caddy-docker-reverse-proxy-guide/) ou [Traefik](/traefik-reverse-proxy-docker/) sur ton serveur, Tsdproxy ne les remplace pas. Il les complète en offrant un accès direct via Tailscale pour les services que tu ne veux pas exposer sur Internet.

## Fonctionnement sous le capot

Tsdproxy repose sur trois briques simples :

1. **Docker Events** : il écoute le socket Docker pour les événements `start`, `stop` et `die`.
2. **Tailscale API** : pour chaque conteneur labellisé, il appelle l'API Tailscale pour créer un serveur web accessible sur le tailnet.
3. **Nommage DNS** : le nom de la machine est automatiquement enregistré dans le DNS interne Tailscale.

Quand tu fais `docker compose up -d` avec un nouveau label `tsdproxy.enable`, Tsdproxy détecte l'événement en quelques secondes et crée la route. Quand tu fais `docker compose down`, la route disparaît automatiquement. Pas de routes fantômes, pas de nettoyage manuel.

Tailscale gère nativement le HTTPS pour les noms de machine. Quand tu accèdes à `https://uptime-kuma.ton-tailnet.ts.net`, Tailscale fournit un certificat Let's Encrypt valide pour ton tailnet. Tu n'as pas besoin de gérer des certificats toi-même.

## Comparatif : Tsdproxy vs Traefik + Tailscale vs Caddy

| Critère | Tsdproxy | Traefik + Tailscale | Caddy + Tailscale |
|---------|----------|---------------------|-------------------|
| Configuration | Zéro (labels Docker) | Labels + fichiers YAML/TOML | Caddyfile |
| Découverte auto | Oui (Docker events) | Oui (providers Docker) | Non (Caddyfile statique) |
| HTTPS | Géré par Tailscale natif | Let's Encrypt + Tailscale | Let's Encrypt natif |
| Exposition Internet | Non (tailnet uniquement) | Possible (optionnel) | Possible (optionnel) |
| Domaine requis | Non (Tailscale DNS) | Oui (si public) | Oui (si public) |
| Idéal pour | Homelab tailnet pur | Architecture hybride publique/privée | Simplicité HTTPS publique |

Mon avis : si tous tes services sont destinés à rester dans ton tailnet sans jamais toucher Internet public, Tsdproxy est la solution la plus simple. Si tu veux certains services publics et d'autres privés, garde [Traefik](/traefik-reverse-proxy-docker/) pour le public et ajoute Tsdproxy pour le privé.

## Sécurité et bonnes pratiques

Même si tout reste dans ton tailnet, quelques règles à respecter :

- **Ne mets pas `tsdproxy.enable=true` sur un conteneur que tu ne veux pas exposer.** C'est la règle numéro un. Tsdproxy rend le service visible pour tous les appareils de ton tailnet.
- **Utilise les ACL Tailscale** pour restreindre l'accès. Dans la console Tailscale, tu peux définir des règles comme `accept: src:group:famille; dst:tag:serveurs` pour limiter qui voit quoi.
- **Génère une clé API dédiée** plutôt que de réutiliser ta clé d'authentification perso. Révoque-la en cas de doute.
- **Garde Tailscale à jour** sur l'hôte. Les mises à jour du daemon corrigent des vulnérabilités réseau.

## Dépannage rapide

### Le conteneur n'apparaît pas sur le tailnet
Vérifie que Tsdproxy est bien lancé et qu'il a accès au socket Docker : `docker logs tsdproxy`. Tu dois voir des lignes du type `Detected container: uptime-kuma`.

### Erreur "invalid API key"
La clé API Tailscale a expiré ou n'a pas les bons droits. Régénère une clé depuis la console avec les permissions "Device" et "Tailnet settings".

### Le nom DNS ne résout pas
Vérifie que le client Tailscale sur ton appareil client a bien `Accept DNS` activé. Sur mobile, c'est dans les paramètres de l'app. Sur Linux, vérifie `--accept-dns=true`.

### Conflit de noms de machine
Si deux conteneurs ont le même nom, Tailscale refuse d'enregistrer le second. Utilise `tsdproxy.name` pour forcer un nom unique.

## Conclusion

Tsdproxy est ce qu'il manquait à l'écosystème Tailscale + Docker. Il transforme l'exposition de services internes d'une corvée manuelle en une découverte automatique fluide. Tu ajoutes deux labels dans un `docker-compose.yml`, tu lances ton conteneur, et il est immédiatement accessible depuis ton téléphone, ton laptop ou ta tablette via le tunnel sécurisé Tailscale.

Pour un homelab où la simplicité prime, c'est probablement le meilleur combo actuel. Pas de reverse proxy à configurer, pas de port à ouvrir sur ta box, pas de Certbot à maintenir. Juste du Docker, du Tailscale, et Tsdproxy qui fait le lien.

Si tu veux d'autres outils pour sécuriser ton homelab, jette un œil à mon [guide WireGuard Docker](/wireguard-docker-vpn-homelab/) pour un VPN de couche inférieure, ou à mes guides pour [Caddy](/caddy-docker-reverse-proxy-guide/) et [Traefik](/traefik-reverse-proxy-docker/) si tu as besoin d'une exposition publique. Bon auto-hébergement !
