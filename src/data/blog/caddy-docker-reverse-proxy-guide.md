---
title: "Caddy Docker : le reverse proxy HTTPS automatique en 5 minutes"
description: "Guide caddy docker complet : reverse proxy HTTPS automatique avec Let's Encrypt en Docker, Caddyfile simple et comparatif Nginx. En 5 minutes chrono."
pubDatetime: "2026-06-07T08:00:00.000Z"
modDatetime: "2026-06-07T08:00:00.000Z"
author: Brandon Visca
tags:
  - docker
  - auto-hebergement
  - reverse-proxy
  - https
  - intermediaire
  - guide
featured: false
draft: false
focusKeyword: caddy docker
ogImage: ""
---
**TL;DR : Caddy est un serveur web écrit en Go qui gère automatiquement les certificats HTTPS Let's Encrypt, sans Certbot, sans configuration complexe. Un Caddyfile de 5 lignes suffit à exposer un service Docker avec HTTPS. Voici la méthode.**

## Pourquoi Caddy change la donne

La plupart des gens configurent Nginx + Certbot quand ils veulent du HTTPS. C'est robuste, ça marche, mais c'est lourd. Tu dois gérer le renouvellement des certificats, la syntaxe Nginx est verbeuse, et la moindre erreur de chemin de certificat te laisse en HTTP avec un truc qui pète silencieusement.

Caddy, lui, intègre nativement ACME (le protocole de Let's Encrypt). Il demande le certificat, le renouvelle, et le sert. Tout seul. Sans cron externe, sans volume de certificats à monter à la main. C'est dans son ADN depuis le début.

**Ce que Caddy fait mieux que Nginx pur :**
- Configuration HTTPS entièrement automatique (obtention + renouvellement Let's Encrypt)
- Syntaxe lisible et concise (Caddyfile vs bloc `server` Nginx de 20 lignes)
- HTTP/2 et HTTP/3 activés par défaut
- Pas de dépendance externe (Certbot, cron, scripts de renouvellement)
- Réécriture de headers et reverse proxy en quelques mots

Le seul point où Nginx reste devant : les très grosses charges (C10K problem) et les cas d'usage avancés avec des modules tiers spécifiques.

## Caddy vs Nginx Proxy Manager vs Nginx pur

| Critère | Caddy Docker | Nginx Proxy Manager | Nginx pur + Certbot |
|---------|--------------|--------------------|---------------------|
| Configuration HTTPS | Automatique, zero-config | Via interface web (clic) | Manuelle + Certbot + cron |
| Syntaxe | Caddyfile simple (5 lignes) | Aucune (UI) | Nginx conf verbeuse (20+ lignes) |
| Interface graphique | Non | Oui | Non |
| Renouvellement certificats | Auto (intégré) | Auto (intégré) | Certbot + cron manuel |
| Performance | Très bonne | Bonne (Nginx derrière) | Excellente |
| Docker Compose labels | Possible (caddy-docker-proxy) | Oui (intégré) | Non |
| Idéal pour | Ceux qui aiment le terminal et la simplicité | Débutants, UI graphique | Sysadmins, gros trafic |

Pour ma part, si tu veux une interface graphique pour gérer tes reverse proxies, j'ai aussi testé [Nginx Proxy Manager](/nginx-proxy-manager-docker-guide/) et c'est plutôt sympa pour les débutants. Mais si tu préfères rester dans le terminal avec une config propre et minimale, Caddy est clairement au-dessus.

## Architecture du setup

On va monter Caddy dans Docker avec un volume pour persister les certificats (éviter de les re-demander à chaque restart) et un volume pour le Caddyfile. Ensuite on expose un service — ici Uptime Kuma en exemple — derrière Caddy. Le tout sur un serveur avec un nom de domaine pointant dessus.

**Prérequis :**
- Un serveur (VPS, Raspberry Pi, whatever) avec Docker et Docker Compose
- Un nom de domaine pointant vers l'IP du serveur (A record)
- Les ports 80 et 443 ouverts sur le pare-feu

Pour sécuriser le serveur qui héberge Caddy, n'oublie pas de mettre en place [Fail2Ban](/fail2ban-docker-securite-serveur/) et un pare-feu restrictif.

## Le Docker Compose

```yaml
version: "3.9"

services:
  caddy:
    image: caddy:2-alpine
    container_name: caddy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
      - caddy_config:/config
    networks:
      - proxy

  uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: uptime-kuma
    restart: unless-stopped
    volumes:
      - uptime-kuma-data:/app/data
    networks:
      - proxy
    # Pas de ports exposés directement, Caddy gère l'accès

volumes:
  caddy_data:
  caddy_config:
  uptime-kuma-data:

networks:
  proxy:
    driver: bridge
```

**Points importants :**
- Le port 80 est obligatoire pour le challenge HTTP-01 de Let's Encrypt
- Le port 443 est ton HTTPS
- `caddy_data` persiste les certificets et l'état ACME
- Le service interne (Uptime Kuma) n'expose aucun port directement, il passe par le réseau Docker `proxy`

Si tu cherches d'autres services à auto-héberger derrière ton reverse proxy, tu peux jeter un œil à [Gitea](/gitea-serveur-git-docker-auto-hebergement/) pour ton propre Git, ou [n8n](/n8n-docker-workflow-automation/) pour automatiser des workflows sans dépendre de Zapier.

## Le Caddyfile

Crée un fichier `Caddyfile` à côté de ton `docker-compose.yml` :

```caddyfile
kuma.monserveur.fr {
    reverse_proxy uptime-kuma:3001
}
```

Remplace `kuma.monserveur.fr` par ton domaine. C'est tout. Pas de directive SSL, pas de mention de certificat. Caddy détecte qu'il s'agit d'un domaine public, fait le challenge Let's Encrypt, obtient le certificat et sert du HTTPS.

Si tu veux rediriger le www vers le non-www (ou l'inverse) :

```caddyfile
kuma.monserveur.fr {
    reverse_proxy uptime-kuma:3001
}

www.kuma.monserveur.fr {
    redir https://kuma.monserveur.fr{uri}
}
```

**Headers de sécurité recommandés :**

```caddyfile
kuma.monserveur.fr {
    reverse_proxy uptime-kuma:3001 {
        header_up Host {host}
        header_up X-Real-IP {remote}
        header_up X-Forwarded-For {remote}
        header_up X-Forwarded-Proto {scheme}
    }
    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        Referrer-Policy "strict-origin-when-cross-origin"
    }
}
```

Caddy injecte déjà automatiquement les headers `X-Forwarded-Proto` dans la plupart des cas, mais être explicite ne coûte rien.

## Reverse proxy multi-sites avec un seul Caddy

Ton Caddyfile peut gérer autant de domaines que tu veux. Si tu auto-héberges plusieurs services (Gitea, n8n, Uptime Kuma, etc.), tu configures tout dans un seul fichier :

```caddyfile
gitea.monserveur.fr {
    reverse_proxy gitea:3000
}

n8n.monserveur.fr {
    reverse_proxy n8n:5678
}

kuma.monserveur.fr {
    reverse_proxy uptime-kuma:3001
}
```

Caddy demande un certificat distinct pour chaque sous-domaine. Pas besoin de déclarer quoi que ce soit : il détecte automatiquement les blocs de domaine et les enregistre auprès de Let's Encrypt en une seule passe au démarrage.

**Challenges ACME : comment ça marche sous le capot**

Quand Caddy démarre, il prépare chaque certificat en deux étapes :
1. HTTP-01 : Let's Encrypt envoie une requête sur ton domaine au port 80. Caddy répond avec un token spécifique.
2. Validation et délivrance du certificat, stockage dans `/data/caddy/certificates/`.

Tout ça est automatisé. Caddy écrit un fichier JSON dans son data dir pour suivre l'état ACME, et il vérifie régulièrement l'expiration. À 2/3 de la durée du certificat (soit environ 60 jours), Caddy relance silencieusement la procédure.

Si tu préfères le challenge DNS-01 (nécessaire pour les wildcards type `*.monserveur.fr`), Caddy supporte de nombreux providers via plugins DNS. Mais cela requiert de recompiler Caddy avec le plugin adapté, ou d'utiliser l'image personnalisée `caddy:builder` pour compiler une version avec les modules nécessaires.

## Compression et cache pour accélérer le frontal

Caddy intègre nativement `encode gzip` et `encode zstd`. Tu peux les activer en une ligne :

```caddyfile
kuma.monserveur.fr {
    encode gzip zstd
    reverse_proxy uptime-kuma:3001
}
```

Le navigateur demande la compression dans ses headers (`Accept-Encoding`), et Caddy compresse la réponse au vol. Pas besoin d'activer un module externe ou de recompiler quoi que ce soit.

Pour le cache, Caddy ne fait pas de cache de contenu statique par défaut contrairement à Nginx. Si tu sers des assets lourds (images, CSS, JS), tu peux soit utiliser un CDN Cloudflare (couche externe), soit ajouter un Varnish devant Caddy. Pour un usage classique d'auto-hébergement de services Docker, la compression gzip suffit amplement.

## Hardéner Caddy : bonnes pratiques

Même si Caddy fait le job tout seul, quelques ajustements sécuritaires valent le coup :

**1. Limiter les méthodes HTTP**
```caddyfile
kuma.monserveur.fr {
    @not_allowed method OPTIONS PATCH DELETE
    respond @not_allowed 405
    reverse_proxy uptime-kuma:3001
}
```

**2. Bloquer les IP suspects (fail2ban)**
Caddy logue au format JSON dans son stdout. Tu peux router les logs vers un fichier avec un volume monté, puis faire lire ce fichier à Fail2Ban pour bannir les scanners. J'utilise personnellement [Fail2Ban en Docker](/fail2ban-docker-securite-serveur/) qui lit les logs Caddy et ban les tentatives massives de scanning de chemins communs (`/wp-admin/`, `/.env`, etc.).

**3. Rate limiting avec Caddy**
Tu peux limiter le nombre de requêtes par IP avec le module `http.rate_limit` (nécessite un plugin ou une version compilée). Pour un setup simple, rester sur un firewall `ufw` ou `nftables` côté hôte est suffisant.

**4. Logs structurés**
Active les logs JSON pour une ingestion plus facile par un outil comme Loki ou un simple parsing :
```caddyfile
{
    log {
        output file /var/log/caddy/access.log
        format json
    }
}
```

Et monte le volume `/var/log/caddy` dans ton Docker Compose.

## Exposer un service déjà existant avec un réseau Docker externe

Imaginons que Uptime Kuma est déjà déployé sur un réseau Docker existant. Tu peux simplement relier Caddy à ce réseau externe au lieu de tout redéployer dans un seul `docker-compose.yml`.

**Docker Compose de Caddy (réseau externe) :**
```yaml
services:
  caddy:
    image: caddy:2-alpine
    networks:
      - uptime-kuma_network
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
    ports:
      - "80:80"
      - "443:443"

volumes:
  caddy_data:

networks:
  uptime-kuma_network:
    external: true
```

Le Caddyfile reste identique. Caddy résout le nom `uptime-kuma` via le DNS interne Docker du réseau partagé. C'est l'approche que j'utilise quand des services tournent déjà depuis longtemps et que je veux juste ajouter un reverse proxy sans tout casser.

## FAQ rapide

**Est-ce que Caddy fonctionne derrière un CDN comme Cloudflare ?**
Oui. Active le mode Full (Strict) dans Cloudflare et laisse Caddy gérer Let's Encrypt. Caddy obtiendra un certificat pour ton domaine, Cloudflare fera confiance à ce certificat, et l'accès direct au serveur sera aussi en HTTPS. Si tu mets le mode "Flexible", Cloudflare seul fait le HTTPS, ce qui cache des problèmes.

**Peut-on utiliser Caddy sans Docker ?**
Évidemment. Le binaire officiel fonctionne sur Linux, Windows, macOS. Mais dans un contexte d'auto-hébergement de services Docker, le conteneur est plus pratique : isolation, reproductibilité, update atomique.

**Caddy vs Traefik ?**
Traefik est très populaire dans l'écosystème Docker grâce à son auto-discovery via labels. Il fait aussi du HTTPS automatique (Let's Encrypt). Points de différence : Caddy a une syntaxe de config plus lisible (Caddyfile vs YAML/TOML Traefik), Traefik est plus flexible sur les providers de cloud. Pour un auto-hébergeur solo, Caddy est plus simple. Pour un cluster Kubernetes ou Swarm, Traefik a l'avantage.

**Les certificats sont-ils gratuits ?**
Oui. Let's Encrypt est 100% gratuit. Caddy le gère pour toi. Pas d'abonnement, pas de limite de sites raisonnable pour un usage perso.

## Lancer le tout

```bash
docker compose up -d
```

Attends 10-20 secondes, puis :

```bash
docker compose logs caddy | tail -20
```

Tu dois voir une ligne du type :
`autoserv obtained certificate | kuma.monserveur.fr`

Puis teste en HTTPS :
```bash
curl -I https://kuma.monserveur.fr
```

Tu dois avoir un `HTTP/2 200` avec `strict-transport-security` dans les headers. Le certificat est valide, auto-généré, et il se renouvellera tout seul.

## Docker labels : l'approche zero-config avec caddy-docker-proxy

Il existe une approche encore plus lazy : `lucaslorentz/caddy-docker-proxy`. Caddy découvre automatiquement les services via les labels Docker. Plus besoin de Caddyfile statique.

**Docker Compose adapté :**

```caddyfile
services:
  caddy:
    image: lucaslorentz/caddy-docker-proxy:2-alpine
    container_name: caddy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - caddy_data:/data
      - caddy_config:/config
    networks:
      - proxy

  uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: uptime-kuma
    restart: unless-stopped
    volumes:
      - uptime-kuma-data:/app/data
    networks:
      - proxy
    labels:
      caddy: kuma.monserveur.fr
      caddy.reverse_proxy: "{{upstreams 3001}}"
```

Avantages : ajoute un service, ajoute des labels, c'est en ligne. Inconvénient : Caddy a besoin d'accéder au socket Docker, ce qui pose une question de sécurité sur un serveur multi-tenant.

Pour un usage perso sur un serveur dédié, c'est très pratique. Pour de la prod en équipe, je préfère le Caddyfile versionné en Git.

## Débuguer quand ça coince

**Erreur : pas de certificat, boucle sur le challenge**
- Ton port 80 est-il bien ouvert et routé vers Caddy ? Let's Encrypt doit atteindre Caddy sur le port 80
- Le domaine pointe-t-il bien sur l'IP du serveur ? `nslookup ton.domaine` pour vérifier

**Erreur : rate limit Let's Encrypt**
- Let's Encrypt limite à 5 certificats par domaine par semaine. Ne teste pas en boucle avec de vrais domaines. Utilise le staging ACME pour tester :
```caddyfile
{
    acme_ca https://acme-staging-v02.api.letsencrypt.org/directory
}
```

**Le certificat n'est pas renouvelé**
- Caddy renouvelle automatiquement à 2/3 de la durée de vie. Vérifie les logs : `docker compose logs caddy | grep -i renew`
- Si Caddy redémarre trop souvent (crashloop), le renouvellement peut être bloqué

**Erreur : reverse_proxy retourne 502 Bad Gateway**
- Le service interne est-il bien sur le même réseau Docker que Caddy ?
- Le port cible dans `reverse_proxy` est-il le bon ? (ex: Uptime Kuma écoute sur le 3001)
- Le service interne est-il UP ? `docker compose ps`

## Conclusion

Caddy dans Docker, c'est le combo qui fait oublier les nuits à se battre avec Certbot. Un Caddyfile de 3 lignes, un `docker compose up -d`, et ton service est en HTTPS avec un certificat valide. Le renouvellement est silencieux, la config reste lisible, et tu peux même automatiser via les labels Docker si tu es dans une logique d'infrastructure as code.

Si tu veux une interface graphique, je te renvoie vers [Nginx Proxy Manager](/nginx-proxy-manager-docker-guide/). Si tu veux du pur fichier de config minimaliste et maintenable, Caddy est probablement le meilleur choix du moment pour un auto-hébergement Docker.
