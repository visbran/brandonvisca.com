---
title: "Zoraxy Docker : reverse proxy HTTP/HTTPS en Go (alternative simple à Traefik)"
description: "Zoraxy Docker : déploie un reverse proxy HTTP/HTTPS en Go simple et léger. Alternative à Traefik pour ton homelab avec Docker Compose."
pubDatetime: "2026-07-04T09:00:00.000Z"
modDatetime: "2026-07-04T09:00:00.000Z"
author: Brandon Visca
tags:
  - reseau
  - docker
  - intermediaire
  - zoraxy
  - reverse-proxy
  - homelab
featured: false
draft: false
focusKeyword: zoraxy docker
faqs:
  - question: "Quelle est la différence entre Zoraxy et Traefik ?"
    answer: "Zoraxy est un reverse proxy écrit en Go qui se veut plus simple à configurer que Traefik. Il n'utilise pas de labels Docker ni de découverte de services automatique : tout se passe via une interface web ou un fichier JSON. Traefik reste plus puissant pour les architectures complexes, mais Zoraxy brille par sa simplicité dans un homelab classique."
  - question: "Zoraxy supporte-t-il Let's Encrypt ?"
    answer: "Oui, Zoraxy intègre nativement la génération et le renouvellement automatique de certificats Let's Encrypt. Il gère aussi les certificats auto-signés et l'import de certificats personnalisés sans aucune dépendance externe."
  - question: "Puis-je utiliser Zoraxy sans Docker ?"
    answer: "Absolument. Zoraxy est distribué sous forme de binaire Go autonome. Cependant, Docker (ou Docker Compose) reste la méthode recommandée pour un déploiement propre, reproductible et facilement maintenable dans un homelab."
  - question: "Zoraxy gère-t-il la répartition de charge (load balancing) ?"
    answer: "Oui, Zoraxy propose un load balancing simple en amont avec plusieurs backends. Il supporte aussi le failover basique, ce qui suffit largement pour la majorité des usages domestiques et petites infrastructures."
ogImage: ""
---
> 💡 **TL;DR**
> - Zoraxy est un reverse proxy HTTP/HTTPS écrit en Go, beaucoup plus simple à prendre en main que Traefik
> - Il s'installe en 5 minutes avec Docker Compose et se configure via une interface web claire
> - Parfait pour un homelab où tu veux un reverse proxy simple sans la complexité
> - Gestion automatique des certificats Let's Encrypt, load balancing basique et zéro dépendance

## Pourquoi chercher une alternative à Traefik ?

Traefik est excellent. Je l'utilise depuis des années sur plusieurs infrastructures et je ne cracherai pas dessus. Mais avouons-le : sa courbe d'apprentissage est raide. Entre les providers, les middlewares, les labels Docker, les CRDs Kubernetes et la doc qui change à chaque version majeure, on passe parfois plus de temps à configurer le reverse proxy qu'à déployer l'application derrière.

Dans un homelab, la complexité doit rester proportionnelle au besoin. Tu n'as pas besoin d'un Airbus A380 pour aller chercher ton pain. C'est là qu'intervient **Zoraxy** : un reverse proxy HTTP/HTTPS écrit en Go par les équipes de Tobu Topia, conçu pour être **léger, rapide et simple**. Une installation **zoraxy docker** se résume à un fichier Compose et quelques clics dans une interface web.

Zoraxy ne révolutionne pas le genre. Il fait ce qu'on attend d'un reverse proxy — router du HTTP/HTTPS vers des services internes — sans inventer quarante-deux concepts abstraits. Une interface web, un fichier de conf JSON, et c'est parti.

Si tu cherches un comparatif avec un autre reverse proxy Docker déjà déployé, jette un œil à mon [guide Traefik Docker](/traefik-reverse-proxy-docker/).

## Qu'est-ce que Zoraxy exactement ?

Zoraxy est un reverse proxy et un outil de gestion de réseau écrit en Go. Son créateur l'a pensé comme un remplaçant léger de Nginx Proxy Manager et de Traefik, avec une emphase sur la simplicité d'utilisation. Pour ceux qui cherchent une solution **zoraxy docker** rapide à mettre en place, il frappe directement dans le mille.

**Ce qu'il fait bien :**
- Reverse proxy HTTP/HTTPS avec gestion des virtual hosts
- Certificats SSL/TLS auto-signés, importés ou Let's Encrypt natif
- Load balancing basique avec failover
- Redirection HTTP vers HTTPS automatique
- Rate limiting intégré
- Authentification basique HTTP native
- WebSocket supporté nativement
- Interface d'administration web moderne

**Ce qu'il ne fait pas (encore) :**
- Pas de découverte de services Docker automatique (pas de labels magiques)
- Pas d'intégration Kubernetes native
- Pas de middlewares aussi riches que ceux de Traefik

Pour un homelab classique, une dizaine de conteneurs sur un seul nœud, ces limitations sont largement acceptables. Si tu as une architecture micro-services multi-nœuds avec Consul et Vault, reste sur Traefik ou Caddy.

## Prérequis

Avant de déployer Zoraxy, assure-toi d'avoir :

- Docker et Docker Compose installés (ou `docker compose` en plugin V2)
- Un domaine pointant vers ton serveur (obligatoire pour Let's Encrypt)
- Les ports 80 et 443 ouverts et redirigés vers ton hôte Docker
- Un sous-réseau Docker dédié (optionnel mais propre)

Si tu n'as pas encore de domaine configuré pour ton homelab, tu peux utiliser des certificats auto-signés pour tester, mais ton navigateur hurlera à chaque connexion. Pour un setup propre, un vrai domaine avec des vrais certificats vaut largement le coup.

## Installation de Zoraxy Docker avec Docker Compose

Zoraxy n'est pas encore sur Docker Hub officiel (le projet évolue vite), mais l'image communautaire `tobu1337/zoraxy` est fiable et bien maintenue. Voici un `docker-compose.yml` minimal et fonctionnel pour déployer **zoraxy docker** sur ton serveur :

```yaml
version: "3.8"

services:
  zoraxy:
    image: tobu1337/zoraxy:latest
    container_name: zoraxy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
      - "5487:5487"
    volumes:
      - ./zoraxy-data:/opt/zoraxy/data
      - ./zoraxy-certs:/opt/zoraxy/certs
      - /var/run/docker.sock:/var/run/docker.sock:ro
    environment:
      - ZORAXY_PORT=5487
      - ZORAXY_ADMIN_USER=admin
      - ZORAXY_ADMIN_PASS=change_me_maintenant
    networks:
      - proxy

networks:
  proxy:
    driver: bridge
```

**Points importants :**
- Le port `5487` est l'interface d'administration web. Ne l'expose **jamais** sur Internet sans protection (VPN, IP whitelist ou authentification forte)
- Le volume `zoraxy-data` conserve la configuration JSON et la base de règles
- Le volume `zoraxy-certs` stocke les certificats SSL générés ou importés
- Le montage du socket Docker en read-only permet à Zoraxy de lister les conteneurs si tu actives les fonctionnalités de découverte limitée

Démarre le conteneur :

```bash
cd /chemin/vers/zoraxy
docker compose up -d
```

Attends 10-15 secondes que le service initialise, puis connecte-toi à `http://<ip-du-serveur>:5487` avec les identifiants définis dans les variables d'environnement.

## Configuration de base

L'interface web de Zoraxy est immédiate. Pas de JSON à éditer à la main (même si c'est possible), pas de reload à envoyer en ligne de commande. C'est précisément ce qui fait la force d'un setup **zoraxy docker** : tout se fait via l'UI.

### 1. Créer ton premier proxy rule

Dans le menu **Proxy Rules**, clique sur **Add Rule** :

- **Root Domain** : `subdomain.tondomaine.com`
- **Target URL** : `http://<ip-conteneur>:<port>` ou `http://nom-conteneur:port` si sur le même réseau Docker
- **Protocol** : HTTP (Zoraxy gère la terminaison SSL en amont)
- **Enable HTTPS** : coche si tu veux forcer HTTPS avec redirection automatique

### 2. Gérer les certificats SSL

Va dans **Certificates**. Tu as trois options :

**Auto-signed** : Zoraxy génère un certificat auto-signé en un clic. Utile pour du lab interne, inutilisable en production.

**ACME / Let's Encrypt** : Renseigne ton email, choisis le challenge HTTP-01 (le plus simple quand le port 80 est accessible) et clique **Obtain**. Le renouvellement est automatique.

**Upload** : Importe ton propre certificat + clé privée au format PEM.

### 3. Activer la redirection HTTP vers HTTPS

Dans **Global Settings**, active l'option **Force HTTPS**. Désormais, toute requête HTTP sera redirigée vers HTTPS automatiquement. C'est une option basique mais essentielle qu'on oublie trop souvent.

## Exemple concret : proxifier Plex, Home Assistant et Vaultwarden

Prenons un scénario réel. Tu as trois services dans ton homelab et tu veux leur attribuer des sous-domaines propres :

```yaml
# docker-compose.yml des services
version: "3.8"

services:
  plex:
    image: linuxserver/plex:latest
    container_name: plex
    restart: unless-stopped
    environment:
      - PUID=1000
      - PGID=1000
    volumes:
      - ./plex-config:/config
      - /mnt/media:/media
    networks:
      - proxy

  homeassistant:
    image: ghcr.io/home-assistant/home-assistant:stable
    container_name: homeassistant
    restart: unless-stopped
    volumes:
      - ./ha-config:/config
    networks:
      - proxy

  vaultwarden:
    image: vaultwarden/server:latest
    container_name: vaultwarden
    restart: unless-stopped
    volumes:
      - ./vw-data:/data
    networks:
      - proxy

networks:
  proxy:
    external: true
```

Dans Zoraxy, tu crées trois règles :

| Root Domain | Target URL |
|-------------|------------|
| `plex.tondomaine.com` | `http://plex:32400` |
| `ha.tondomaine.com` | `http://homeassistant:8123` |
| `pass.tondomaine.com` | `http://vaultwarden:80` |

Tu demandes un certificat Let's Encrypt pour `*.tondomaine.com` (wildcard avec challenge DNS si ton registrar est supporté) ou trois certificats distincts. Zoraxy les déploie, les associe aux règles, et tu peux oublier la partie réseau.

Si tu cherches une solution de gestionnaire de mots de passe auto-hébergée, j'ai aussi un [guide complet Vaultwarden Docker](/vaultwarden-docker-gestionnaire-mots-de-passe/) qui détaille la sécurisation du conteneur.

## Load balancing et failover

Zoraxy permet de définir plusieurs backends pour une même règle. C'est rudimentaire, pas d'algorithmes avancés comme least-connection, mais pour un homelab, un simple round-robin ou un failover actif/passif suffit.

Dans l'interface, édite une règle existante et ajoute des **Upstream Servers** :

```text
Primary: http://app-1:8080
Secondary: http://app-2:8080
Failover: http://app-backup:8080
```

Si le primaire ne répond plus, Zoraxy bascule automatiquement sur le secondaire. Pas besoin de Keepalived, de HAProxy ni d'une usine à gaz. Ça fait le job sans prétention.

## Mise à jour de Zoraxy

Comme pour tout conteneur Docker, la mise à jour se résume à deux lignes :

```bash
cd /chemin/vers/zoraxy
docker compose pull
docker compose up -d
```

Zoraxy conserve sa configuration dans le volume monté, donc le redémarrage est transparent. Avant chaque mise à jour, je te recommande de sauvegarder le dossier `zoraxy-data` :

```bash
tar czvf zoraxy-backup-$(date +%F).tar.gz zoraxy-data/
```

## Zoraxy vs Traefik vs Caddy : le match

| Critère | Zoraxy | Traefik | Caddy |
|---------|--------|---------|-------|
| Courbe d'apprentissage | Très douce | Raide | Douce |
| Découverte auto Docker | Limitée | Excellente | Via module |
| Let's Encrypt natif | Oui | Oui | Oui (intégré) |
| Fichier de conf | JSON + UI | YAML/Labels | Caddyfile |
| WebSocket | Natif | Natif | Natif |
| Middlewares | Basiques | Très riches | Corrects |
| Load balancing | Simple | Avancé | Simple |
| Empreinte mémoire | ~20 Mo | ~50-80 Mo | ~30 Mo |

Mon avis : si tu débutes dans l'auto-hébergement et que tu veux juste pointer des sous-domaines vers des conteneurs sans lire 200 pages de doc, **Zoraxy est un excellent choix**. Une stack **zoraxy docker** est plus légère que [Caddy](/caddy-docker-reverse-proxy-guide/) et infiniment plus accessible que Traefik pour un usage domestique.

Traefik reste le roi des environnements Cloud Native complexes. Caddy est le champion de la configuration déclarative élégante. Zoraxy occupe une niche simple : **le reverse proxy qui se configure en cliquant**.

## Sécuriser l'interface d'administration

C'est le point le plus critique. Le port 5487 est la clef de ton royaume. Si quelqu'un y accède, il peut rediriger n'importe quel domaine vers n'importe quoi.

**Mes recommandations :**
- **Ne jamais exposer 5487 sur Internet**. Utilise un VPN comme [WireGuard](/wireguard-docker-vpn-homelab/) ou un tunnel SSH pour y accéder
- Changer le mot de passe par défaut immédiatement (évidence, mais on sait jamais)
- Limiter l'accès par IP si tu es en réseau local fixe
- Activer l'authentification basique sur l'interface si Zoraxy le propose dans ta version

Dans un contexte professionnel, Zoraxy n'est probablement pas assez durci. Pour un homelab derrière une box domestique avec un accès VPN, le risque reste maîtrisé si tu suis ces règles.

## Dépannage rapide

### Zoraxy ne démarre pas
Vérifie que les ports 80, 443 et 5487 ne sont pas déjà occupés par un autre service (Apache, Nginx, Traefik...). Utilise `ss -tlnp | grep -E '(:80|:443|:5487)'` pour identifier le coupable.

### Certificat Let's Encrypt en échec
Le challenge HTTP-01 nécessite que le port 80 soit accessible depuis Internet et que le domaine resolve bien vers ton IP. Vérifie aussi que Cloudflare n'est pas en mode proxy strict (qui masque l'IP originale) sans configuration DNS spécifique.

### 502 Bad Gateway
Le backend est injoignable. Vérifie que le conteneur cible est bien sur le même réseau Docker `proxy` et que son port interne est correct. Zoraxy n'est pas en mode host par défaut : il résout les noms via le DNS interne Docker.

### Erreur "permission denied" sur le socket Docker
Assure-toi que le montage du socket est bien en `:ro` (read-only) et que l'utilisateur à l'intérieur du conteneur a les droits suffisants. En dernier recours, monte-le sans `:ro`, même si c'est moins propre.

## Conclusion

Zoraxy n'est pas l'outil le plus hype de l'écosystème homelab. Il ne figure pas dans toutes les vidéos YouTube ni dans tous les repo GitHub étoilés. Pourtant, il résout un vrai problème : celui de la complexité excessive des reverse proxies modernes pour des besoins simples.

En quelques minutes, tu peux router du HTTPS propre vers tes conteneurs, gérer des certificats Let's Encrypt et loadbalancer deux instances sans écrire une seule ligne de YAML abstruse. Pour un homelab personnel ou une petite infrastructure où la simplicité prime, Zoraxy est une alternative légitime à Traefik et à Nginx Proxy Manager.

**Adopte Zoraxy si tu veux un reverse proxy qui se configure comme un routeur domestique : des cases à cocher, des champs à remplir, et ça marche.**
