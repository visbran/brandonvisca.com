---
title: "Cloudflare Tunnel Docker : accède à ton homelab sans IP publique"
description: "Guide complet cloudflare tunnel docker : expose ton homelab sur Internet sans IP fixe ni ouverture de ports. Docker compose fonctionnel inclus."
pubDatetime: "2026-07-23T08:00:00.000Z"
modDatetime: "2026-07-23T08:00:00.000Z"
author: Brandon Visca
tags:
  - intermediaire
  - reseau
  - docker
  - cloudflare
  - tunnel
  - homelab
featured: false
draft: false
focusKeyword: cloudflare tunnel docker
ogImage: ""
---
> 💡 **TL;DR**
>
> - Cloudflare Tunnel (cloudflared) crée un tunnel sortant HTTPS entre ton serveur et le réseau Cloudflare, aucun port entrant à ouvrir.
> - Tu obtiens un domaine public, un certificat SSL auto, et une protection DDoS native.
> - Pas d'IP publique fixe requise. Ça marche derrière un CGNAT, un 4G, ou la box de ton FAI de base.
> - Ce guide cloudflare tunnel docker te donne le `docker-compose.yml` complet, la config d'ingress, et les pièges à éviter.

## Table des matières

## Le problème de l'IP publique

Tout auto-hébergeur a un jour vécu ce moment de gloire : tu viens de monter ton serveur Docker, tu as déployé Nextcloud, Vaultwarden, ou ton dashboard Homer. Tu ouvres fièrement un navigateur sur `192.168.1.42:8080`, et ça marche. Parfait.

Puis tu essaies d'y accéder depuis le café du coin. Et là, c'est le drame.

Ton FAI t'a filé une IP dynamique. Ou pire : une IP derrière un CGNAT (la fameuse "IP partagée" qui te met dans le même réseau local que 15 000 autres abonnés). Tu peux ouvrir des ports sur ta Freebox tant que tu veux, personne n'arrivera à ton serveur.

Les solutions classiques ?

- **Ouverture de ports + DDNS** (ex: [DuckDNS Docker](/duckdns-docker-ddns-gratuit/)) : ça marche quand ton FAI n'est pas en CGNAT. C'est fragile, dangereux, et ton IP finit sur Shodan avant d'avoir fini ton café.
- **VPN comme [WireGuard](/wireguard-docker-vpn-homelab/) ou [Tailscale](/tailscale-vpn-mesh-homelab/)** : excellent pour l'accès distant sécurisé, mais ça ne résout pas le problème de partage public. Ton VPN, c'est pour toi. Pas pour exposer un service à des utilisateurs externes.
- **Reverse proxy avec IP publique fixe** : c'est le Graal, mais ça coûte cher et ça expose ton infrastructure.

Cloudflare Tunnel est la solution intermédiaire qui tue le game : tu exposes tes services sur Internet, sans IP publique, sans ouvrir de ports, et avec la protection réseau de Cloudflare en prime.

## Cloudflare Tunnel, c'est quoi exactement ?

Cloudflare Tunnel (anciennement Argo Tunnel, outil cloudflared) est un service gratuit qui crée un tunnel sortant (outbound) entre ton serveur et le réseau de Cloudflare. Concrètement :

1. Tu installes un petit agent (`cloudflared`) sur ton serveur.
2. Cet agent ouvre une connexion HTTPS persistante vers les serveurs de Cloudflare.
3. Quand quelqu'un visite ton domaine, Cloudflare route le trafic vers ton serveur via ce tunnel.
4. Ton serveur n'a jamais besoin d'accepter de connexion entrante.

Le trafic est chiffré de bout en bout. Cloudflare gère le certificat SSL. Tu as accès à des règles de sécurité (Zero Trust), à la protection DDoS, et à un cache CDN si tu veux accélérer tes assets statiques.

Le tout est **gratuit** pour un usage personnel. Pas de quota ridicule. Pas de carte de crédit pour tester. Tu as juste besoin d'un domaine (qui peut être un sous-domaine gratuit sur un domaine que tu possèdes déjà, ou un domaine acheté chez ton registrar préféré).

## Comment ça marche (schéma mental)

Avant le tunnel, ton architecture ressemble à ça :

```text
Internet → Routeur (NAT/PAT) → Serveur (ports ouverts)
```

Problème : si tu n'as pas d'IP publique, la flèche de gauche n'atteint jamais ton routeur.

Avec Cloudflare Tunnel, ça devient :

```text
Internet → Cloudflare (CDN + SSL + WAF) → Tunnel sortant → cloudflared → Docker → Ton service
```

Le truc magique : c'est ton serveur qui initie la connexion vers Cloudflare. Donc le firewall de ta box, le CGNAT de ton FAI, le NAT strict de ton employeur, tout ça devient transparent. Tant que ton serveur peut sortir sur le port 443 (HTTPS), le tunnel fonctionne.

## Prérequis

- Un domaine chez Cloudflare (ou transféré chez eux, ou avec les NS pointant vers Cloudflare)
- Un serveur avec Docker et Docker Compose
- Un accès sortant HTTPS (port 443), ce que tout FAI permet, même bridé
- 5 minutes pour lire ce guide

Tu n'as PAS besoin :
- d'une IP publique fixe
- d'ouvrir des ports sur ton routeur
- d'un reverse proxy externe
- de configurer du NAT ou du port forwarding

## Étape 1 : Créer un tunnel dans le dashboard Cloudflare

1. Connecte-toi sur [dash.cloudflare.com](https://dash.cloudflare.com).
2. Sélectionne ton domaine.
3. Dans le menu de gauche, va sur **Zero Trust** > **Networks** > **Tunnels**.
4. Clique sur **Create a tunnel**.
5. Choisis **Cloudflared**.
6. Donne un nom à ton tunnel, par exemple `homelab-tunnel`.
7. Garde le token affiché à l'écran. Tu en auras besoin pour le `docker-compose.yml`.

Ce token est l'équivalent de la clé privée de ton tunnel. Ne le partage pas. Ne le commit pas sur GitHub. On va le passer via une variable d'environnement.

## Étape 2 : Récupérer le token

Cloudflare te donne une commande de connexion qui ressemble à ça :

```bash
cloudflared tunnel run --token eyJhIjoi...
```

Le token commence par `eyJh`. C'est un JWT encodé en base64. Copie-le en entier.

> **Note importante** : Cloudflare affiche parfois un token "quick tunnel" temporaire. Ce n'est pas le même. Le token du tunnel permanent est plus long et ne contient pas de `trycloudflare`.

## Étape 3 : docker-compose.yml

Crée un dossier dédié et un fichier `docker-compose.yml` :

```yaml
services:
  cloudflared:
    image: cloudflare/cloudflared:2026.7.2
    container_name: cloudflared
    restart: unless-stopped
    command: tunnel run
    environment:
      - TUNNEL_TOKEN=${TUNNEL_TOKEN}
    networks:
      - homelab
    # Pas besoin de ports exposés. Le tunnel sort par le réseau interne.

networks:
  homelab:
    external: true
```

Puis crée un fichier `.env` à côté :

```bash
TUNNEL_TOKEN=eyJhIjoidG9uLXRva2VuLWRlLXR1bm5lbC1pY2ki...
```

Lance le conteneur :

```bash
docker compose up -d
```

Vérifie les logs :

```bash
docker logs -f cloudflared
```

Tu devrais voir un message du genre :

```text
INF Connection registered connIndex=0 location=FRA
INF Connected to FRA
```

Si tu vois ça, ton tunnel est vivant. Il discute déjà avec Cloudflare. Maintenant, il faut lui dire quoi exposer.

## Étape 4 : Configurer les ingress (les services à exposer)

Tu peux configurer les ingress de deux façons : via le dashboard Cloudflare (plus simple pour commencer) ou via un fichier de config YAML local. Je te montre les deux.

### Méthode A : Dashboard Cloudflare (recommandée pour débuter)

1. Dans le dashboard, retourne sur **Zero Trust** > **Networks** > **Tunnels**.
2. Clique sur ton tunnel `homelab-tunnel`.
3. Dans l'onglet **Public Hostname**, clique sur **Add a public hostname**.
4. Remplis :
   - **Subdomain** : `nextcloud` (ou ce que tu veux)
   - **Domain** : ton-domaine.com
   - **Path** : laisse vide
   - **Type** : HTTP
   - **URL** : `nextcloud:80` (nom du service Docker + port interne)
5. Clique sur **Save hostname**.

Attends 30 secondes, puis va sur `https://nextcloud.ton-domaine.com`. Ça marche.

Tu peux ajouter autant de hostnames que tu veux :
- `vaultwarden.ton-domaine.com` → `vaultwarden:80`
- `dashboard.ton-domaine.com` → `dashy:8080`
- `adguard.ton-domaine.com` → `adguard:3000`

Le service cible est résolu via le réseau Docker interne (`homelab`). C'est pour ça qu'on a mis tout le monde sur le même réseau externe.

### Méthode B : Fichier config.yml local (plus propre en production)

Crée un fichier `config.yml` :

```yaml
tunnel: <TUNNEL_ID>
credentials-file: /etc/cloudflared/credentials.json

ingress:
  - hostname: nextcloud.ton-domaine.com
    service: http://nextcloud:80
  - hostname: vaultwarden.ton-domaine.com
    service: http://vaultwarden:80
  - hostname: code.ton-domaine.com
    service: http://code-server:8080
  - hostname: adguard.ton-domaine.com
    service: http://adguard:3000
  - service: http_status:404
```

Et adapte ton `docker-compose.yml` :

```yaml
services:
  cloudflared:
    image: cloudflare/cloudflared:2026.7.2
    container_name: cloudflared
    restart: unless-stopped
    command: tunnel --config /etc/cloudflared/config.yml run
    volumes:
      - ./config.yml:/etc/cloudflared/config.yml:ro
      - ./credentials.json:/etc/cloudflared/credentials.json:ro
    networks:
      - homelab

networks:
  homelab:
    external: true
```

La dernière ligne `service: http_status:404` est un catch-all. Si quelqu'un tape un sous-domaine non configuré, il obtient une 404. C'est une sécurité basique.

> **Astuce réseau** : le DNS interne de Docker résolve les noms de service automatiquement. Tant que tous tes conteneurs sont sur le même réseau `homelab`, `nextcloud` est résolu en IP interne sans intervention de ta part. Si tu utilises [AdGuard Home](/adguard-home-docker-guide-2026/) comme DNS local, vérifie que les requêtes internes ne sont pas forwardées vers un DNS externe, sinon Docker ne pourra pas résoudre les noms de service.

## Sécurité : zero trust et politiques d'accès

Exposer un service sur Internet, même via Cloudflare, c'est bien. Le laisser ouvert à tout le monde, c'est moins bien.

Cloudflare te permet d'ajouter des règles d'accès sans écrire une ligne de code :

### Application Access (Zero Trust)

Dans le dashboard, va sur **Zero Trust** > **Access** > **Applications**.

Clique sur **Add an application**.

- **Application name** : Nextcloud (ou autre)
- **Session duration** : 24h (temps avant re-authentification)
- **Identity providers** : One-time PIN (code envoyé par email), GitHub, Google, au choix
- **Policies** : ajoute une règle du genre "email contient @ton-domaine.com"

Maintenant, quand quelqu'un visite `nextcloud.ton-domaine.com`, Cloudflare affiche une page d'authentification avant de laisser passer le trafic. Même si le service sous-jacent n'a aucune authentification, il est protégé par Cloudflare.

C'est particulièrement utile pour des dashboards d'administration, des outils internes, ou des services que tu ne veux pas laisser publics.

### Rate limiting et WAF

Cloudflare inclut un pare-feu d'application web (WAF) gratuit. Il bloque automatiquement les requêtes suspectes :
- Injection SQL
- XSS
- Scan de vulnérabilités
- Bots malveillants

Le rate limiting (limitation de requêtes) est aussi disponible en gratuit, avec un plafond généreux. Pour un homelab personnel, tu n'as aucune raison de le désactiver.

## Comparatif rapide avec les alternatives

| Solution | IP publique requise | Ouverture de ports | Exposition publique | Facilité |
|---|---|---|---|---|
| Ouverture de ports + DDNS | Oui (sauf CGNAT) | Oui | Oui | Moyen |
| [WireGuard](/wireguard-docker-vpn-homelab/) | Non | Non | Non (VPN) | Moyen |
| Tailscale | Non | Non | Non (VPN) | Facile |
| [Firezone](/firezone-docker-vpn-zero-trust/) | Non | Non | Non (VPN ZT) | Moyen |
| Cloudflare Tunnel | Non | Non | Oui | Facile |
| Reverse proxy cloud (VPS) | Oui (le VPS) | Oui | Oui | Complexe |

Cloudflare Tunnel n'est pas un VPN. C'est un outil d'exposition publique. Si tu veux accéder à ton réseau interne en tant que client (bureau à distance, partage de fichiers NAS, etc.), un VPN comme WireGuard ou Tailscale reste la bonne solution. Mais si tu veux héberger un service web accessible depuis n'importe où, le tunnel est le plus simple et le plus sécurisé.

## Dépannage

### "Connection refused" ou erreur 502

Vérifie que le service cible est bien joignable depuis le réseau Docker interne :

```bash
docker exec -it cloudflared sh
wget -qO- http://nextcloud:80
```

Si ça ne marche pas, ton service n'est pas sur le même réseau Docker, ou il n'écoute pas sur le bon port.

### Tunnel "degraded" ou déconnexions fréquentes

Cloudflared tente de se connecter à plusieurs datacenters Cloudflare. Si ton FAI bride le trafic sortant, le tunnel peut devenir instable. Vérifie que le port 443 TCP est bien ouvert en sortie :

```bash
nc -zv cloudflare.com 443
```

### Domaine non résolu

Attends que la propagation DNS se fasse. Même avec Cloudflare, ça peut prendre quelques minutes. Vérifie aussi que le sous-domaine est bien configuré dans le dashboard et que le tunnel est enregistré comme actif.

### Besoin de monitoring

Si tu veux surveiller la santé de ton tunnel et de tes services Docker en général, un outil comme [Beszel](/beszel-monitoring-docker/) ou [Zabbix](/zabbix-docker-monitoring-infrastructure/) peut t'alerter quand le conteneur `cloudflared` redémarre ou consomme trop de ressources.

## Conclusion

Cloudflare Tunnel est l'outil cloudflare tunnel docker que tout auto-hébergeur devrait connaître. Il résout un vrai problème, accéder à ton homelab sans IP publique, avec une simplicité déconcertante. Un conteneur Docker, un token, quelques clics dans un dashboard, et tes services sont sur Internet avec un certificat SSL valide et une protection réseau intégrée.

Le meilleur dans tout ça ? C'est gratuit, sans quota abusif, et ça fonctionne partout. Que tu sois chez un FAI en fibre ou en 4G rural avec un CGNAT de mort, ton tunnel passe.

Arrête de te battre avec le port forwarding et les IP dynamiques. Déploie cloudflared, pointe ton domaine, et retourne coder quelque chose d'utile à la place.
