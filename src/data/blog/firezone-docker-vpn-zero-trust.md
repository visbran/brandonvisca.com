---
title: "Firezone Docker : VPN zero-trust basé sur WireGuard"
description: "Guide Firezone Docker : déploie un VPN zero-trust basé sur WireGuard avec Docker Compose. OIDC, policies et split tunneling inclus."
pubDatetime: "2026-07-11T08:00:00.000Z"
modDatetime: "2026-07-11T08:00:00.000Z"
author: Brandon Visca
tags:
  - intermediaire
  - securite
  - vpn
  - wireguard
  - docker
  - zero-trust
featured: false
draft: false
focusKeyword: firezone docker
faqs:
  - question: "Quelle différence entre Firezone et Tailscale ?"
    answer: "Tailscale est un SaaS fermé qui gère le plan de contrôle dans le cloud. Firezone est open-source et auto-hébergé : tu contrôles le control plane, les données d'identité et les policies. WireGuard est le transport dans les deux cas."
  - question: "Firezone peut-il fonctionner sans IDP externe ?"
    answer: "Non. Firezone requiert un fournisseur d'identité compatible OIDC ou SAML (Google Workspace, Okta, Azure AD, Keycloak, etc.). Si tu veux un VPN sans IDP, reste sur un serveur WireGuard Docker classique."
  - question: "Firezone consomme-t-il beaucoup de ressources ?"
    answer: "Non. Le Gateway tourne en Rust (léger, ~50 Mo RAM) et le Control Plane en Elixir. Un VPS avec 1 vCPU et 2 Go de RAM suffit pour une dizaine d'utilisateurs."
  - question: "Puis-je utiliser Firezone derrière un reverse proxy ?"
    answer: "Oui, mais avec précaution. Le port UDP 51820 doit être exposé directement pour le transport WireGuard. Le portail web (TCP 443) peut passer derrière un reverse proxy comme Caddy ou Traefik."
ogImage: "" 
---
> 💡 **TL;DR**
> - Firezone est un VPN zero-trust open-source qui encapsule WireGuard dans une couche d'identité (OIDC/SAML) et de policies
> - Tu le déploies en 15 minutes avec Docker Compose : Gateway Rust + Control Plane Elixir + base PostgreSQL
> - Contrairement à Tailscale, tu gardes le contrôle total de tes données et de tes règles d'accès
> - Split tunneling, NAT traversal et relay fallback inclus nativement

## Table des matières

## Pourquoi Firezone et pas juste WireGuard ?

Tu as déjà lu mon guide [WireGuard Docker](/wireguard-docker-vpn-homelab/) et ton VPN tourne. Tu te connectes depuis ton téléphone, tout roule. Mais à mesure que ton homelab grandit, tu te retrouves face à des questions embarrassantes :

- Comment révoquer l'accès d'un ami qui a quitté le projet sans recréer toutes les clés ?
- Comment empêcher ton téléphone d'envoyer tout le traffic Netflix dans le tunnel ?
- Comment donner accès à un seul service (ex. Nextcloud) sans ouvrir tout le réseau ?
- Qui s'est connecté hier à 3h du matin et depuis quelle IP ?

WireGuard pur est excellent pour le transport chiffré, mais il est volontairement minimaliste. Pas d'authentification centralisée, pas de logs, pas de policies granulaires, pas de revue d'accès en temps réel. C'est un tunnel. Rien de plus.

Firezone conserve WireGuard comme couche de transport (rapide, léger, intégré kernel), mais ajoute par-dessus un **control plane zero-trust** complet : authentification via OIDC, groupes d'utilisateurs, règles d'accès par ressource, split tunneling configurables, et un portail web pour gérer le tout sans toucher à la ligne de commande.

C'est la différence entre ouvrir une porte avec une clé unique partagée entre tout le monde, et installer un système d'interphonie avec badge, logs d'entrée et permissions par étage.

## Qu'est-ce que Firezone exactement ?

Firezone est un projet open-source lancé en 2022 par Jamil Bou Kheir. Il se positionne comme une alternative auto-hébergée aux solutions commerciales zero-trust comme Tailscale, ZeroTier ou les offres ZTNA des éditeurs traditionnels (Zscaler, Palo Alto Prisma Access).

**Ce qui le définit :**

- **WireGuard sous-jacent** : pas de réinvention de la roue, le transport est le meilleur du marché
- **Identity-aware access** : chaque connexion est liée à une identité vérifiée via ton IDP
- **Policy-based routing** : tu décides qui accède à quoi, sur quels ports, depuis quels appareils
- **Split tunneling** : seul le traffic destiné à ton homelab passe par le tunnel, le reste sort par la connexion locale
- **NAT traversal + relay** : STUN/TURN intégrés pour traverser les NAT symétriques sans configuration manuelle
- **Multi-plateforme** : clients natifs Linux, macOS, Windows, iOS, Android

Le projet est sous licence Apache 2.0, hébergé sur GitHub, et financé par un modèle open-core : la version communautaire est complète pour un usage personnel ou PME, tandis que des fonctionnalités avancées (multi-sites, SIEM, audit avancé) sont réservées à l'édition Enterprise.

## Architecture et composants du déploiement Firezone Docker

Pour comprendre où va chaque brique, voici l'architecture simplifiée d'un déploiement Firezone Docker standard :

| Composant | Technologie | Rôle |
|-----------|-------------|------|
| **Gateway** | Rust | Point d'entrée VPN. Gère les tunnels WireGuard, le NAT traversal, le relay fallback. |
| **Control Plane** | Elixir / Phoenix | API REST, websocket temps réel, gestion des policies et des identités. |
| **Web UI** | Phoenix LiveView | Interface d'administration et portail utilisateur. |
| **Base de données** | PostgreSQL | Stockage des utilisateurs, groupes, policies, sessions, logs. |
| **Token/Secrets** | Pas de Redis requis | Les tokens JWT sont signés et vérifiés via clés définies en variables d'environnement. |

Le Gateway est le seul composant exposé sur Internet (UDP pour WireGuard, TCP pour le portail et les API). Le Control Plane et PostgreSQL restent sur le réseau interne Docker.

## Prérequis

Avant de lancer le `docker-compose.yml`, vérifie que tu as :

- Un serveur Docker fonctionnel (mon [guide Docker Compose pour débutants](/docker-debutant-services-auto-heberger/) t'aide si besoin)
- Un nom de domaine pointant vers ton serveur (obligatoire pour le HTTPS et l'OIDC)
- Un fournisseur d'identité compatible OIDC : Google Workspace, Azure AD, Okta, ou Keycloak auto-hébergé
- Les ports `80/tcp`, `443/tcp` et `51820/udp` ouverts sur ton pare-feu et redirigés vers le serveur
- Docker Compose v2+ et `docker` en rootless ou avec permissions appropriées

Pour le pare-feu, si tu cherches une solution simple, [Fail2Ban Docker](/fail2ban-docker-securite-serveur/) complète bien la stack.

## Le Docker Compose Firezone Docker complet

Crée un dossier dédié et place ton `docker-compose.yml` dedans :

```yaml
version: "3.8"

services:
  postgres:
    image: postgres:16-alpine
    container_name: firezone-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: firezone
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: firezone
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - firezone

  firezone:
    image: ghcr.io/firezone/firezone:latest
    container_name: firezone
    restart: unless-stopped
    depends_on:
      - postgres
    cap_add:
      - NET_ADMIN
    sysctls:
      - net.ipv4.ip_forward=1
      - net.ipv6.conf.all.forwarding=1
    ports:
      - "80:80"
      - "443:443"
      - "51820:51820/udp"
    environment:
      EXTERNAL_URL: https://vpn.tondomaine.fr
      DATABASE_HOST: postgres
      DATABASE_NAME: firezone
      DATABASE_USER: firezone
      DATABASE_PASSWORD: ${DB_PASSWORD}
      ADMIN_EMAIL: admin@tondomaine.fr
      DEFAULT_CLIENT_EXPIRATION_DAYS: 30
      WEBSOCKET_URL: wss://vpn.tondomaine.fr
      SECRET_KEY_BASE: ${SECRET_KEY_BASE}
      LIVE_VIEW_SIGNING_SALT: ${LIVE_VIEW_SIGNING_SALT}
      COOKIE_SIGNING_SALT: ${COOKIE_SIGNING_SALT}
      COOKIE_ENCRYPTION_SALT: ${COOKIE_ENCRYPTION_SALT}
      TELEMETRY_ENABLED: "false"
    volumes:
      - firezone_data:/var/firezone
    networks:
      - firezone

volumes:
  postgres_data:
  firezone_data:

networks:
  firezone:
    driver: bridge
```

**Quelques précisions :**

- `EXTERNAL_URL` doit correspondre exactement au domaine que tu as pointé vers ton serveur
- Le port `51820/udp` est **obligatoire** pour le transport WireGuard. Ne le cache pas derrière un reverse proxy
- Les ports 80/443 servent le portail web et l'API. Tu peux les mettre derrière [Caddy Docker](/caddy-docker-reverse-proxy-guide/) ou Traefik si tu préfères
- `NET_ADMIN` est nécessaire pour que Firezone configure les interfaces réseau et les règles iptables du conteneur

## Configuration étape par étape

### 1. Générer les secrets

Firezone a besoin de quatre secrets forts. Génère-les avec OpenSSL :

```bash
export SECRET_KEY_BASE=$(openssl rand -base64 48)
export LIVE_VIEW_SIGNING_SALT=$(openssl rand -base64 24)
export COOKIE_SIGNING_SALT=$(openssl rand -base64 24)
export COOKIE_ENCRYPTION_SALT=$(openssl rand -base64 24)
export DB_PASSWORD=$(openssl rand -base64 32)

# Crée le fichier .env
cat > .env <<EOF
DB_PASSWORD=$DB_PASSWORD
SECRET_KEY_BASE=$SECRET_KEY_BASE
LIVE_VIEW_SIGNING_SALT=$LIVE_VIEW_SIGNING_SALT
COOKIE_SIGNING_SALT=$COOKIE_SIGNING_SALT
COOKIE_ENCRYPTION_SALT=$COOKIE_ENCRYPTION_SALT
EOF
```

### 2. Lancer la base de données

```bash
docker compose up -d postgres
sleep 10
docker compose exec postgres psql -U firezone -d firezone -c "\dt" 2>/dev/null || echo "Attendre 5s et relancer"
```

Attends que PostgreSQL soit prêt avant de lancer Firezone.

### 3. Lancer Firezone

```bash
docker compose up -d firezone
```

Le premier démarrage crée les tables et un compte admin local (sans OIDC). Tu peux te connecter avec `ADMIN_EMAIL` et un mot de passe généré dans les logs :

```bash
docker compose logs firezone | grep "password"
```

**Note** : le compte admin local est temporaire. Dès que l'OIDC est configuré, il est préférable de désactiver l'authentification locale ou d'en restreindre l'usage.

## Intégration OIDC (exemple Google Workspace)

L'authentification OIDC est le cœur du zero-trust. Voici la marche à suivre avec Google Workspace (adaptable à Keycloak, Azure AD, Okta, etc.) :

**Dans Google Cloud Console :**
1. Crée un projet ou sélectionne-en un existant
2. Va dans "APIs & Services" → "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
3. Type : "Web application"
4. URI de redirection autorisée : `https://vpn.tondomaine.fr/auth/oidc/google/callback`
5. Récupère le **Client ID** et le **Client Secret**

**Dans Firezone (Web UI) :**
1. Connecte-toi en admin
2. Va dans "Settings" → "Identity Providers"
3. Ajoute un fournisseur OIDC
4. Remplis :
   - **Name** : Google
   - **Client ID** : ton ID Google
   - **Client Secret** : ton secret Google
   - **Discovery URL** : `https://accounts.google.com/.well-known/openid-configuration`
   - **Redirect URI** : laisse la valeur pré-remplie
5. Sauvegarde

Après cette étape, tes utilisateurs se connecteront avec leur compte Google Workspace. Firezone récupère automatiquement l'email et le nom, et crée un compte Firezone à la volée.

**Avec Keycloak auto-hébergé :**
Si tu préfères garder le contrôle total, déploie Keycloak dans un autre conteneur Docker et configure Firezone avec l'URL de découverte de ton realm (`https://keycloak.tondomaine.fr/realms/homelab/.well-known/openid-configuration`). C'est la solution la plus souveraine.

## Déploiement et vérification

Une fois l'OIDC configuré, crée ton premier **Site** (représente ton réseau ou ton homelab), puis un **Gateway** (le point d'entrée VPN). Firezone te fournit un token de provisionnement à passer au conteneur Gateway si tu sépares les rôles.

Dans le Docker Compose ci-dessus, tout est fusionné. Le container `firezone` joue les rôles de Control Plane, Web UI et Gateway. Pour un homelab personnel, c'est suffisant.

**Vérification post-déploiement :**

```bash
# Vérifier que le conteneur tourne
docker compose ps

# Vérifier que WireGuard écoute sur UDP 51820
ss -ulnp | grep 51820

# Vérifier les logs en temps réel
docker compose logs -f firezone
```

Si tout est vert, tu dois pouvoir accéder au portail à `https://vpn.tondomaine.fr` et te connecter via OIDC.

## Configuration des clients

Firezone fournit des applications natives pour toutes les plateformes. Tu les télécharges sur [firezone.dev/download](https://www.firezone.dev/download).

**Le workflow utilisateur est le suivant :**

1. L'utilisateur ouvre le client Firezone
2. Il entre l'URL du portail : `https://vpn.tondomaine.fr`
3. Il est redirigé vers l'IDP pour authentification
4. Après validation OIDC, le client reçoit une configuration WireGuard (clés, endpoints, allowed IPs)
5. Le tunnel s'établit automatiquement

**Android / iOS :**
L'app mobile gère le roaming réseau (4G vers WiFi) de façon transparente, comme Tailscale. Le split tunneling est configurable depuis le portail web : tu définis les `Allowed IPs` par groupe d'utilisateurs.

**Linux headless :**
Pour un serveur sans interface graphique, Firezone fournit un client CLI. Tu le provisionnes avec un token de service et il monte le tunnel au boot via systemd.

## Split tunneling et policies

C'est ici que Firezone devient intéressant par rapport à un WireGuard classique.

Dans le portail web, tu crées des **Policies** qui lient des **Users** ou **Groups** à des **Resources** (IPs, sous-réseaux, ports). Exemples concrets :

| Règle | Utilisateur | Accès |
|-------|-------------|-------|
| Admins réseau | Groupe `ops` | `10.0.0.0/8`, tous les ports |
| Nextcloud only | Groupe `famille` | `10.0.1.50:443` uniquement |
| Monitoring | Groupe `dev` | `10.0.1.20:3000` (Grafana) |
| Accès VPN interdit | Groupe `invites` | Aucun (suspendu) |

Le **split tunneling** se configure au niveau des ressources. Si tu définis une ressource comme `10.0.0.0/24`, seul le traffic vers ce réseau passe par le tunnel. Le traffic vers `8.8.8.8` ou Netflix sort par la connexion locale de l'utilisateur. Résultat : pas de latence inutile, pas de géoblocage activé par erreur.

## NAT traversal et relay fallback

Firezone intègre un mécanisme de NAT traversal basé sur STUN pour établir des connexions peer-to-peer quand c'est possible. Quand les deux pairs sont derrière un NAT symétrique ou un CGNAT (Free, SFR en mobile), le STUN échoue. Firezone bascule alors automatiquement sur un **relay TURN** hébergé sur ton propre serveur (le Gateway fait office de relay).

Contrairement à Tailscale qui utilise les serveurs DERP de Tailscale Inc., le relay Firezone est **ton serveur**. Le traffic chiffré WireGuard transite par ton infrastructure, jamais par un tiers. C'est un avantage considérable pour la confidentialité, même si ça augmente légèrement la latence dans les cas de relay forcé.

## Comparaison : Firezone vs Tailscale vs ZeroTier

| Critère | Firezone | Tailscale | ZeroTier |
|---------|----------|-----------|----------|
| Modèle | Open-source auto-hébergé | SaaS fermé | SaaS fermé (control plane) |
| Code source | Apache 2.0 (GitHub) | Partiellement open (client) | Propriétaire (client open) |
| Transport | WireGuard | WireGuard | Protocole propriétaire |
| Control plane | Ton serveur | Serveurs Tailscale | Planètes ZeroTier |
| IDP requis | Oui (OIDC/SAML) | Oui (OIDC ou intégré) | Non (compte ZeroTier) |
| Split tunneling | Oui, policies granulaires | Oui (ACL) | Oui (rules) |
| Relay | Auto (ton serveur) | DERP cloud | Roots cloud |
| SSO gratuit | Oui | Oui (jusqu'à 3 users) | Non (payant avancé) |
| Complexité déploiement | Moyenne (Docker) | Faible (installer l'app) | Faible |
| Souveraineté données | Totale | Partielle | Faible |

**Verdict** : si tu veux un VPN zero-trust sans dépendre d'un SaaS américain et que tu acceptes de gérer un conteneur Docker, Firezone est la meilleure option open-source actuelle. Si tu veux zero-config et que tu fais confiance à Tailscale Inc., Tailscale reste plus simple. ZeroTier est un tiers inutile aujourd'hui, son protocole propriétaire n'apporte plus rien par rapport à WireGuard.

## Sécurité et bonnes pratiques

Un VPN zero-trust ce n'est pas juste du chiffrement, c'est une posture. Quelques règles à respecter :

- **Rotate les secrets** : regénère `SECRET_KEY_BASE` et les salts tous les 6 mois
- **Restreindre l'accès admin** : utilise un groupe IDP dédié pour les admins Firezone
- **Monitorer les connexions** : Firezone logue les sessions. Exporte-les vers [Beszel](/beszel-monitoring-docker/) ou ton syslog pour conservation
- **MFA obligatoire** : configure l'MFA sur ton IDP (Google Workspace, Azure AD, Keycloak). Firezone hérite de la politique MFA de l'IDP
- **Backup PostgreSQL** : la base contient les clés publiques et les policies. Un dump régulier via `pg_dump` est indispensable
- **Mises à jour** : abonne-toi aux releases GitHub de Firezone et relance `docker compose pull && docker compose up -d` mensuellement

## Dépannage

**Le client ne parvient pas à établir le tunnel**
- Vérifie que le port UDP 51820 est bien redirigé vers le serveur et non bloqué par le pare-feu
- Vérifie que `EXTERNAL_URL` correspond bien au domaine DNS résolu publiquement
- Teste depuis l'extérieur avec `nc -u -v vpn.tondomaine.fr 51820`

**L'authentification OIDC échoue**
- Vérifie l'URI de redirection exacte dans la config de ton IDP (trailing slash sensible)
- Vérifie que le domaine est bien en HTTPS (Let's Encrypt valide ou certificat auto-signé)
- Consulte les logs : `docker compose logs firezone | grep -i oidc`

**Performance dégradées (latence élevée)**
- Vérifie si le traffic passe par le relay (indicateur dans le client). Si oui, c'est un NAT symétrique. Normal, mais plus lent
- Place ton serveur dans un datacenter avec un IPv4 public dédié pour minimiser les relais

## Conclusion

Firezone apporte à WireGuard ce qui lui manquait pour devenir une solution zero-trust complète : gestion des identités, policies d'accès, split tunneling et un portail web utilisable par des humains normaux. Le tout en open-source et auto-hébergé.

Contrairement à Tailscale où le plan de contrôle vit dans un cloud tiers, Firezone te garde maître de ton infrastructure. Pour un sysadmin qui gère déjà Docker et un nom de domaine, le déploiement est une formalité de 15 minutes. Le gain en souveraineté et en granularité d'accès est immédiat.

Si tu cherches un accès distant sécurisé pour ton homelab sans vendre ton âme à un SaaS, Firezone Docker est aujourd'hui le meilleur compromis entre simplicité de WireGuard et richesse fonctionnelle du zero-trust. Déploie-le, configure ton OIDC, et dors enfin tranquille en sachant que tes services ne sont accessibles qu'aux bonnes personnes, aux bons moments, et depuis les bons appareils.
