---
title: "Pocket-ID Docker SSO : déploiement léger avec OpenID Connect"
description: "Guide pocket-id docker sso complet : déploie Pocket-ID avec Docker Compose pour un SSO léger et rapide via OpenID Connect dans ton homelab."
pubDatetime: "2026-08-04T06:00:00.000Z"
modDatetime: "2026-08-04T06:00:00.000Z"
author: Brandon
tags:
  - sso
  - openid-connect
  - docker
  - securite
  - auto-hebergement
  - intermediaire
featured: false
draft: false
focusKeyword: pocket-id docker sso
faqs:
  - question: "Quelle est la différence entre Pocket-ID et Keycloak ?"
    answer: "Pocket-ID est minimaliste et prêt en 5 minutes. Keycloak est une solution enterprise lourde qui nécessite une configuration avancée et plus de ressources."
  - question: "Pocket-ID est-il gratuit ?"
    answer: "Oui, c'est un projet open-source sous licence MIT, sans limitation d'utilisateurs ni de clients OIDC."
  - question: "Pocket-ID fonctionne-t-il sans Docker ?"
    answer: "Des binaires natifs sont disponibles, mais Docker reste la méthode recommandée pour un déploiement propre, reproductible et isolé."
ogImage: "" 
---
> 💡 **TL;DR**
> - Pocket-ID est un fournisseur d'identité OpenID Connect ultra-léger, parfait pour l'auto-hébergement
> - Il se déploie en 5 minutes avec Docker Compose et consomme moins de 100 Mo de RAM
> - Tu peux centraliser l'authentification de tous tes services homelab sans la complexité de Keycloak

## Table des matières

## Introduction

Gérer une dizaine de services dans ton homelab signifie souvent gérer une dizaine de couples login / mot de passe. C'est fastidieux, peu sécurisé et source d'erreurs. Les solutions enterprise comme Keycloak ou Authelia existent, mais elles demandent une courbe d'apprentissage steile et des ressources serveur conséquentes.

**Pocket-ID** est un fournisseur d'identité OpenID Connect (OIDC) open-source conçu pour être minimaliste, rapide et facile à déployer. Un conteneur, une base de données SQLite, et tu obtiens un portail d'authentification centralisé prêt à connecter tes applications.

Dans ce guide, nous allons déployer Pocket-ID avec Docker Compose, configurer un client OIDC de base et sécuriser l'accès.

## Pourquoi choisir Pocket-ID ?

| Critère | Pocket-ID | Keycloak | Authelia |
|---|---|---|---|
| RAM | ~80 Mo | +1 Go | ~200 Mo |
| Base de données | SQLite intégrée | PostgreSQL obligatoire | Redis + DB |
| Configuration | Interface web intuitive | XML / CLI complexe | Fichiers YAML |
| OIDC natif | Oui | Oui | Oui (via OIDC) |
| TOTP / Passkeys | Oui | Oui | Oui |

Pocket-ID brille par sa **simplicité** : pas de stack à assembler, pas de dizaines de variables d'environnement à comprendre. Tu lances le conteneur, tu crées ton premier utilisateur depuis l'interface, et tu configures tes clients OIDC en quelques clics.

Si tu cherches une solution de sécurité plus lourde pour une infrastructure complexe, j'ai aussi publié un guide sur [WireGuard avec Docker](https://brandonvisca.com/wireguard-docker-vpn-homelab/) pour sécuriser l'accès réseau.

## Prérequis

- Un serveur ou un NAS avec Docker et Docker Compose installés
- Un nom de domaine (ou un sous-domaine) pointant vers ton serveur
- Un reverse proxy (Nginx Proxy Manager, Traefik ou Caddy) pour gérer le HTTPS

Si tu n'as pas encore de reverse proxy en place, mon guide sur [Nginx Proxy Manager](https://brandonvisca.com/nginx-proxy-manager-docker-guide/) t'explique comment monter le tien en quelques minutes.

## Déploiement avec Docker Compose

Crée un répertoire dédié et un fichier `docker-compose.yml` :

```yaml
services:
  pocket-id:
    image: ghcr.io/pocket-id/pocket-id:latest
    container_name: pocket-id
    restart: unless-stopped
    ports:
      - "3000:3000"
    volumes:
      - ./data:/app/backend/data
    environment:
      - APP_ENV=production
      - PUBLIC_APP_URL=https://id.tondomaine.com
      - TRUST_PROXY=true
      - DATABASE_URL=/app/backend/data/pocket-id.db
```

> **Note** : Remplace `id.tondomaine.com` par ton propre sous-domaine. Le port `3000` est interne ; en production, tu passeras par le reverse proxy en HTTPS.

Lance le conteneur :

```bash
docker compose up -d
```

Pocket-ID démarre et crée automatiquement sa base SQLite dans le dossier `./data`.

## Configuration initiale

1. Accède à `https://id.tondomaine.com` (via ton reverse proxy)
2. Crée ton compte administrateur lors du premier démarrage
3. Depuis l'interface d'administration, navigue vers **Clients OIDC**
4. Ajoute un nouveau client avec :
   - **Name** : le nom de ton service (ex. *Dashy*)
   - **Redirect URIs** : l'URL de callback de ton application (ex. `https://dashy.tondomaine.com/oauth2/callback`)
   - **Scopes** : `openid profile email`
5. Note le **Client ID** et le **Client Secret** générés

## Exemple d'intégration : Homer Dashboard

Pour protéger un service comme Homer Dashboard (ou n'importe quel service compatible OIDC), ajoute ces variables dans la configuration SSO de ton application :

- **Issuer URL** : `https://id.tondomaine.com`
- **Client ID** : celui généré précédemment
- **Client Secret** : celui généré précédemment
- **Scopes** : `openid profile email`

Si tu utilises [Cloudflare Tunnel](https://brandonvisca.com/cloudflare-tunnel-docker-homelab/) pour exposer tes services, l'authentification Pocket-ID ajoute une couche SSO en amont de ton tunnel existant.

## Sécurité et bonnes pratiques

- **HTTPS obligatoire** : OIDC repose sur des échanges de tokens. Ne jamais exposer Pocket-ID en HTTP clair.
- **Backups** : copie régulièrement le fichier SQLite (`data/pocket-id.db`) et le dossier `data`.
- **Passkeys / TOTP** : active l'authentification à deux facteurs pour ton compte administrateur depuis les paramètres utilisateur.
- **Mises à jour** : mets à jour régulièrement l'image Docker (`docker compose pull && docker compose up -d`).
- **Réseau** : isole Pocket-ID dans un réseau Docker dédié et n'expose pas le port `3000` publiquement si tu utilises un reverse proxy local.

## Conclusion

Pocket-ID redéfinit ce qu'un SSO auto-hébergé peut être : léger, rapide et fonctionnel sans compromis. En moins de dix minutes, tu centralises l'authentification de ton homelab et tu élimines la fatigue des mots de passe multiples. C'est la solution idéale pour ceux qui veulent du SSO sans la surcharge d'une infrastructure IAM traditionnelle.
