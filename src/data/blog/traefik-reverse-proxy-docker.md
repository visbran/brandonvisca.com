---
title: "Traefik v3 : le reverse proxy Docker qui gère le HTTPS tout seul"
description: "Installe Traefik v3 comme reverse proxy Docker. Labels auto, HTTPS Let's Encrypt, middlewares — guide complet pour ton homelab en 2026."
pubDatetime: 2026-05-05 10:00:00+02:00
modDatetime: 2026-05-05 10:00:00+02:00
author: Brandon Visca
tags:
  - docker
  - securite
  - auto-hebergement
  - intermediaire
featured: false
draft: false
focusKeyword: traefik docker
faqs:
  - question: "Traefik remplace-t-il Nginx ?"
    answer: "Non. Traefik est un reverse proxy et load balancer. Nginx peut aussi faire ça, mais Traefik est spécialisé pour les conteneurs Docker avec découverte automatique."
  - question: "Peut-on utiliser Traefik sans Docker ?"
    answer: "Oui, Traefik supporte Kubernetes, Consul et fichiers statiques. Mais Docker reste le combo le plus populaire en homelab."
  - question: "Let's Encrypt fonctionne-t-il derrière un routeur domestique ?"
    answer: "Oui avec le challenge HTTP, à condition que les ports 80 et 443 soient redirigés vers ton serveur."
  - question: "Comment savoir si un certificat SSL est bien généré ?"
    answer: "Vérifie le fichier acme.json dans ton volume Traefik. Ou regarde dans le dashboard : onglet HTTP > Routers > TLS doit afficher un cadenas vert."
---
> 💡 **TL;DR** — Ce qu'il faut retenir :
> - Traefik découvre tes conteneurs Docker tout seul via leurs labels.
> - Plus besoin d'éditer un fichier de config à chaque nouveau service.
> - HTTPS Let's Encrypt en deux lignes de labels.
> - Dashboard intégré pour voir toutes tes routes et certificats en temps réel.

## Table des matières

## Pourquoi choisir Traefik plutôt que Nginx ?

Nginx, c'est le dinosaure des reverse proxy. Rapide, stable, tout le monde l'utilise. Mais quand tu joues avec Docker au quotidien, ça devient vite pénible.

Tu installes un nouveau conteneur. Tu ouvres ton `nginx.conf`. Tu ajoutes un bloc `server {}`. Tu recharges Nginx. Tu oublies un point-virgule, ça plante. Tu débugges. Tu réessayes.

**Traefik v3** supprime toute cette friction. Il écoute le socket Docker et détecte les conteneurs qui se lancent. Tu ajoutes trois labels dans ton `docker-compose.yml`, et Ta-da : ta route est créée. Zéro reload, zéro fichier de conf à trifouiller.

En plus, il gère les certificats Let's Encrypt tout seul. Tu n'oublies jamais de renouveler un certificat parce que Traefik le fait automatiquement. C'est ça qui fait la différence pour un homelab : la barrière à l'ajout d'un service passe de 15 minutes à 30 secondes.

*(Pas encore à l'aise avec Docker ? Commence par mon guide [Docker pour les débutants](/docker-debutant-services-auto-heberger/), c'est fait exprès.)*

Pour creuser chaque paramètre, la [documentation officielle de Traefik](https://doc.traefik.io/traefik/) reste la source la plus complète.

## Architecture d'un reverse proxy en homelab

Avant de configurer quoi que ce soit, il faut comprendre où Traefik s'insère dans ton bazar.

Voici le cheminement classique d'une requête vers ton homelab :

1. DNS : `cloud.tondomaine.fr` pointe vers l'IP de ton serveur
2. Le routeur (ou ton box) redirige les ports 80 et 443 vers le serveur
3. Traefik reçoit la requête, lit l'hôte demandé et choisit la route
4. Il vérifie si le certificat HTTPS existe, et le génère si besoin
5. Il applique les middlewares (règles de redirection, authentification, compression)
6. Il balance la requête vers le conteneur Docker concerné

Tout ce chemin est invisible pour toi. Tu ne fais qu'ajouter des labels. Traefik fait le reste.

## File de Docker Compose

Crée un répertoire `traefik` et un `docker-compose.yml` :

```yaml
services:
  traefik:
    image: traefik:v3.1
    container_name: traefik
    restart: unless-stopped
    command:
      - "--api.dashboard=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.tlschallenge=true"
      - "--certificatesresolvers.letsencrypt.acme.email=contact@tondomaine.fr"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./letsencrypt:/letsencrypt
    networks:
      - proxy
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.traefik.rule=Host(`traefik.tondomaine.fr`)"
      - "traefik.http.routers.traefik.entrypoints=websecure"
      - "traefik.http.routers.traefik.tls.certresolver=letsencrypt"
      - "traefik.http.services.traefik.loadbalancer.server.port=8080"
      - "traefik.http.routers.traefik.middlewares=auth@docker"
      - "traefik.http.middlewares.auth.basicauth.users=admin:$apr1$H6uskkkW$ZIG9gpCfZ3y6/9hGztC0P0"

networks:
  proxy:
    external: true
```

### Les paramètres à comprendre

- `providers.docker.exposedbydefault=false` : Traefik ignore tous les conteneurs par défaut. Seuls ceux avec `traefik.enable=true` sont routés. C'est une sécurité essentielle : tu ne peux pas exposer un conteneur par erreur.
- `entrypoints.web` et `entrypoints.websecure` : les points d'entrée HTTP (80) et HTTPS (443). Traefik écoute sur ces ports et distribue les requêtes.
- `certificatesresolvers.letsencrypt` : le résolveur ACME. Il demande un certificat valide auprès de Let's Encrypt. TLS-ALPN-01 est utilisé ici, et ça marche sans problème si les ports 80/443 sont ouverts.
- Le label `traefik.http.routers.traefik.rule=Host(...)` : l'expression qui déclenche cette route. Si l'en-tête Host de la requête correspond, la route est activée.

Le réseau `proxy` est défini comme externe. Cela signifie que tu dois le créer toi-même, et que tous tes autres conteneurs vont s'y rattacher. C'est la magie : même réseau = découverte automatique.

Crée le réseau avant de lancer :

```bash
docker network create proxy
```

Lance Traefik :

```bash
docker compose up -d
```

Attends 30 secondes pour que le certificat se génère, puis accède au dashboard : `https://traefik.tondomaine.fr`.

> ⚠️ **Note de sécurité** : le hash du mot de passe dans l'exemple est à remplacer. Utilise `htpasswd -nb admin tonmotdepasse` pour générer le tien. Ne laisse jamais le dashboard sans protection.

## Le fichier acme.json : ton coffre-fort de certificats

Le volume `./letsencrypt:/letsencrypt` est crucial. Il stocke le fichier `acme.json` qui contient toutes les données de tes certificats Let's Encrypt.

Règles immuables :

- Ne le supprime jamais si tu veux éviter le rate-limit de Let's Encrypt
- Ne versionne pas ce fichier dans Git, il contient tes clés privées
- Mets-le dans un volume Docker persistent pour qu'il survive à un `docker compose down`

Tu vérifies son contenu avec :

```bash
cat letsencrypt/acme.json | jq
```

(si `jq` n'est pas installé, un simple `ls -la letsencrypt/` suffit pour confirmer sa présence)

## Router un nouveau conteneur : la méthode des labels

Voici la partie qui fait de Traefik un outil indispensable.

Quand tu lances un service, tu ne touches plus au fichier de Traefik. Tu ajoutes des labels directement dans le `docker-compose.yml` du service.

### Exemple avec Nextcloud

On va router vers mon guide existant d'installation Nextcloud, cette fois via Traefik :

```yaml
services:
  nextcloud:
    image: nextcloud:latest
    container_name: nextcloud
    restart: unless-stopped
    volumes:
      - nextcloud_data:/var/www/html
    networks:
      - proxy
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.nextcloud.rule=Host(`cloud.tondomaine.fr`)"
      - "traefik.http.routers.nextcloud.entrypoints=websecure"
      - "traefik.http.routers.nextcloud.tls.certresolver=letsencrypt"
      - "traefik.http.services.nextcloud.loadbalancer.server.port=80"

volumes:
  nextcloud_data:

networks:
  proxy:
    external: true
```

`docker compose up -d` et Nextcloud est accessible sur `https://cloud.tondomaine.fr` avec un certificat valide. Aucune autre action requise.

Même mécanisme pour [Vaultwarden](/vaultwarden-docker-gestionnaire-mots-de-passe/) :

```yaml
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.vaultwarden.rule=Host(`pass.tondomaine.fr`)"
      - "traefik.http.routers.vaultwarden.entrypoints=websecure"
      - "traefik.http.routers.vaultwarden.tls.certresolver=letsencrypt"
      - "traefik.http.services.vaultwarden.loadbalancer.server.port=80"
```

Tu peux même utiliser des sous-domaines dynamiques ou des wildcard si tu configures le challenge DNS. Ce n'est pas du niveau intermédiaire, mais sache que Traefik est aussi puissant que scalable.

## Les entrypoints et la redirection HTTP → HTTPS

Par défaut, ton site est accessible sur `http://cloud.tondomaine.fr` et `https://cloud.tondomaine.fr`. C'est une faille de sécurité.

On ajoute deux lignes dans le fichier `docker-compose.yml` de Traefik pour forcer la redirection automatique :

```yaml
      - "--entrypoints.web.http.redirections.entrypoint.to=websecure"
      - "--entrypoints.web.http.redirections.entrypoint.scheme=https"
```

Relance Traefik :

```bash
docker compose up -d --force-recreate
```

Maintenant, toute requête HTTP est automatiquement transformée en HTTPS. Google et tes visiteurs apprécieront.

## Les middlewares : la couche de traitement des requêtes

Les middlewares modifient les requêtes et réponses en transit entre Internet et ton conteneur.

### Compression Gzip

Ajoute un middleware global de compression :

```yaml
      - "traefik.http.middlewares.gzip.compress=true"
```

Puis applique-le à chaque route :

```yaml
      - "traefik.http.routers.nextcloud.middlewares=gzip"
```

Ça réduit le poids des pages de 30 à 50 %, surtout pour les interfaces web lourdes comme Nextcloud ou des dashboards.

### Authentification basique (basic auth)

Pour protéger un service interne sans mettre en place un SSO complet, le basic auth fait l'affaire. On en a parlé dans le fichier Traefik principal pour protéger le dashboard.

Syntaxe :

```yaml
      - "traefik.http.middlewares.auth.basicauth.users=admin:$$apr1$$H6uskkkW$$ZIG9gpCfZ3y6/9hGztC0P0"
```

N'oublie pas de doubler les `$` dans les fichiers Docker Compose (dépendances de variables d'environnement).

### Réécriture d'en-têtes

Certaines applis (Nextcloud en tête) ont besoin que le proxy informe qu'on passe par HTTPS. Cela évite des boucles de redirection. Ajoute un middleware de réécriture d'en-têtes :

```yaml
      - "traefik.http.middlewares.nextcloud-headers.headers.customrequestheaders.X-Forwarded-Proto=https"
      - "traefik.http.middlewares.nextcloud-headers.headers.stsSeconds=31536000"
      - "traefik.http.routers.nextcloud.middlewares=nextcloud-headers"
```

STS (Strict Transport Security) force le navigateur à n'utiliser que HTTPS pendant un an. C'est un plus pour le référencement et la confiance utilisateur.

## Le dashboard : ton observatoire

Le dashboard de Traefik est un outil de debugging inestimable. Onglet par onglet :

- **HTTP Routers** : les règles de routage actives. Tu vois le Host, l'entrypoint, le middleware, et si un certificat TLS est attaché.
- **HTTP Services** : les conteneurs détectés avec leur IP interne et leur port.
- **Middlewares** : les règles appliquées. Si une règle ne fonctionne pas, c'est visible ici.
- **TLS Certificates** : liste des certificats Let's Encrypt en place, dates d'expiration, état.

Si un service ne s'affiche pas, les causes classiques sont :

1. Le label `traefik.enable=true` est absent
2. Le conteneur n'est pas sur le réseau `proxy`
3. Le port interne spécifié dans le label ne correspond pas au port écouté par l'appli
4. Un autre conteneur déclare déjà le même `Host(...)`

## Monitoring : logs et tracing simple

Pour les premières semaines d'utilisation, activer les logs de debug est une bonne idée. Ajoute :

```yaml
      - "--log.level=INFO"
      - "--accesslog=true"
```

Les logs d'accès affichent chaque requête passant par Traefik avec le code de retour et la durée de traitement. Si un service est lent, c'est ici que tu le vois.

### Types de middlewares courants

| Middleware | Fonction | Utilisation |
|---|---|---|
| `compress` | Compression Gzip | Appliquer sur toutes les routes web |
| `basicauth` | Authentification simple | Dashboard, outils admin |
| `ratelimit` | Limiter les requêtes | API exposées en public |
| `stripprefix` | Retirer un préfixe d'URL | API avec version dans l'URL |
| `headers` | Ajouter / modifier des en-têtes | Sécurité HTTPS, CORS |

### Logs utiles en cas de problème

Quand un service ne répond pas, voici les commandes à connaître :

```bash
# Voir les logs de Traefik en temps réel
docker logs -f traefik --tail 50

# Vérifier que le conteneur est bien sur le réseau proxy
docker network inspect proxy

# Lister les routes détectées par Traefik
curl http://localhost:8080/api/http/routers
```

Les erreurs les plus fréquentes se résument à trois causes :

1. Le label `traefik.enable=true` est oublié
2. Le conteneur cible écoute sur un port différent de celui déclaré dans `loadbalancer.server.port`
3. Le fichier `acme.json` a les mauvaises permissions et Traefik ne peut pas y écrire

Pour éviter le point 3, fixe les permissions au premier lancement :

```bash
touch letsencrypt/acme.json
chmod 600 letsencrypt/acme.json
```

### Sécuriser un service interne sans l'exposer

Supposons que tu aies un service de monitoring comme [Uptime Kuma](/uptime-kuma-2-0-monitoring-auto-heberge/) que tu veux consulter sans qu'il soit indexable sur le web.

Solution : aucun label sur le conteneur. Il reste sur le réseau Docker interne, accessible uniquement via VPN ou depuis d'autres conteneurs. Traefik ne le voit jamais.

Alternative : utilise `traefik.enable=true` mais ajoute une règle IP whitelist :

```yaml
      - "traefik.http.middlewares.local-only.ipwhitelist.sourcerange=192.168.1.0/24"
```

Ton conteneur est exposé, mais seul ton réseau local peut y accéder. C'est la meilleure approche si tu veux garder une simplicité sans sacrifier la sécurité.

## Exemple complet : stack homelab avec Traefik

Pour terminer, voici un fichier de composition typique de mon propre homelab. Il montre comment tu peux avoir Traefik, un service web et une base de données sur le même réseau, avec uniquement le service web exposé :

```yaml
services:
  traefik:
    image: traefik:v3.1
    container_name: traefik
    restart: unless-stopped
    command:
      - "--api.dashboard=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--entrypoints.web.http.redirections.entrypoint.to=websecure"
      - "--entrypoints.web.http.redirections.entrypoint.scheme=https"
      - "--certificatesresolvers.letsencrypt.acme.tlschallenge=true"
      - "--certificatesresolvers.letsencrypt.acme.email=contact@tondomaine.fr"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
      - "--log.level=INFO"
      - "--accesslog=true"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./letsencrypt:/letsencrypt
    networks:
      - proxy
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.traefik.rule=Host(`traefik.tondomaine.fr`)"
      - "traefik.http.routers.traefik.entrypoints=websecure"
      - "traefik.http.routers.traefik.tls.certresolver=letsencrypt"
      - "traefik.http.services.traefik.loadbalancer.server.port=8080"
      - "traefik.http.routers.traefik.middlewares=traefik-auth"
      - "traefik.http.middlewares.traefik-auth.basicauth.users=admin:$apr1$H6uskkkW$ZIG9gpCfZ3y6/9hGztC0P0"

  uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: uptime-kuma
    restart: unless-stopped
    volumes:
      - uptime-kuma-data:/app/data
    networks:
      - proxy
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.uptime.rule=Host(`status.tondomaine.fr`)"
      - "traefik.http.routers.uptime.entrypoints=websecure"
      - "traefik.http.routers.uptime.tls.certresolver=letsencrypt"
      - "traefik.http.services.uptime.loadbalancer.server.port=3001"
      - "traefik.http.routers.uptime.middlewares=gzip"
      - "traefik.http.middlewares.gzip.compress=true"

volumes:
  uptime-kuma-data:

networks:
  proxy:
    external: true
```

Tu remarques que la base de données n'est même pas dans ce fichier. Elle vit dans un autre compose, sur le même réseau `proxy`, sans aucun label Traefik. Elle est complètement invisible depuis Internet. C'est cette séparation qui fait la force d'une architecture conteneurisée bien pensée.

## Conclusion

Avec Traefik v3, ton homelab change de dimension. Ajouter un service ne prend plus que quelques labels. La sécurité HTTPS est automatique. Le dashboard offre une visibilité totale.

Et si tu veux continuer à construire ton infrastructure Docker, jette un œil à mes guides pour [Nextcloud](/nextcloud-docker-installation-complete-2025/), [Vaultwarden](/vaultwarden-docker-gestionnaire-mots-de-passe/), ou pour automatiser les mises à jour avec [Watchtower](/watchtower-mise-a-jour-docker-auto/). Bon auto-hébergement !

## Articles connexes

- [Yopass vs PrivateBin vs Password Pusher : lequel choisir ? (2025)](/yopass-vs-privatebin-vs-password-pusher/)
- [Immich Docker remplace Google Photos ? Guide complet 2026](/immich-docker/)
- [Jellyfin avec Docker : Ton Netflix Gratuit en 30 Min (Économise 378€/an)](/jellyfin-docker-alternative-netflix-gratuite/)
- [Nextcloud avec Docker : Ton Cloud Perso en 1h (Adieu Google Drive !)](/nextcloud-docker-installation-complete-2025/)
