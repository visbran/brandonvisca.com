---
title: "DuckDNS Docker : DDNS gratuit pour ton IP dynamique"
description: "DuckDNS Docker : garde ton nom de domaine à jour avec ton IP dynamique gratuitement. Guide pas à pas avec Docker Compose, variables et astuces homelab."
pubDatetime: "2026-07-29T08:00:00.000Z"
modDatetime: "2026-07-29T08:00:00.000Z"
author: brandon
tags:
  - debutant
  - reseau
  - docker
  - duckdns
  - auto-hebergement
featured: false
draft: false
focusKeyword: duckdns docker
faqs:
  - question: "DuckDNS est-il vraiment gratuit ?"
    answer: "Oui, DuckDNS est totalement gratuit. Aucun abonnement, aucune limite de requêtes, aucune publicité. C'est un service maintenu par deux développeurs avec un modèle de dons volontaires."
  - question: "Puis-je utiliser DuckDNS avec un reverse proxy comme Nginx Proxy Manager ?"
    answer: "Absolument. DuckDNS te donne un sous-domaine public pointant vers ton IP. Tu peux ensuite configurer Nginx Proxy Manager ou Traefik pour router les requêtes vers tes services internes avec SSL Let's Encrypt."
  - question: "Quelle différence entre DuckDNS et Cloudflare Tunnel ?"
    answer: "DuckDNS met à jour un enregistrement DNS vers ton IP publique. Il faut donc ouvrir des ports sur ta box et avoir une IP publique réelle. Cloudflare Tunnel crée un tunnel sortant sans IP publique ni ouverture de ports."
  - question: "DuckDNS fonctionne-t-il derrière un CGNAT ?"
    answer: "Non. DuckDNS résout le problème de l'IP dynamique, pas celui du CGNAT. Si ton FAI te met derrière un CGNAT, ton IP n'est pas publique. Dans ce cas, privilégie Cloudflare Tunnel ou un VPN comme Tailscale."
ogImage: ""
---
> 💡 **TL;DR**
> - DuckDNS met à jour automatiquement ton nom de domaine quand ton FAI change ton IP publique
> - Gratuit, sans pub, sans limitation, juste un token et une requête HTTP toutes les 5 minutes
> - Docker Compose officiel disponible, config en 2 variables d'environnement
> - Complément parfait d'un reverse proxy comme [Nginx Proxy Manager](/nginx-proxy-manager-docker-guide/) pour exposer tes services

## Table des matières

## Pourquoi ton IP dynamique te pourrit la vie

Tout auto-hébergeur connaît la galère. Tu montes un serveur homelab, tu configures tes services, tout tourne nickel en local sur `192.168.1.42`. Tu veux accéder à ton Nextcloud, ton Vaultwarden ou ton dashboard depuis l'extérieur. Tu notes l'IP publique affichée sur ta box, tu tapes l'adresse dans ton navigateur… et ça marche. Génial.

Deux jours plus tard, ta box redémarre suite à une mise à jour nocturne du FAI. Ton IP publique a changé. Ton bookmark est mort. Tu dois aller sur `monip.org`, noter la nouvelle IP, mettre à jour tes configs, tes scripts, tes apps mobiles. C'est insupportable.

La solution s'appelle DNS dynamique (DDNS). Un service qui surveille ton IP publique et met à jour automatiquement l'enregistrement DNS de ton nom de domaine quand elle change. [Cloudflare Tunnel](/cloudflare-tunnel-docker-homelab/) résout ça sans IP publique, mais si tu en as une (même dynamique), DuckDNS est la solution gratuite la plus simple qui existe.

## DuckDNS Docker : c'est quoi exactement

DuckDNS est un service DDNS (Dynamic DNS) gratuit créé en 2014 par deux développeurs. Aucune interface chargée de pubs, aucun plan premium qui te bloque. Tu crées un sous-domaine du type `tonnom.duckdns.org`, tu récupères un token, et un petit script envoie ton IP actuelle à leurs serveurs régulièrerement.

Ce qui fait la différence :

- **Gratuit et illimité** : pas de quota de requêtes, pas de limite de sous-domaines
- **Open source** : les clients sont sur GitHub, tu peux auditer le code
- **Simple** : une requête HTTP GET suffit pour mettre à jour l'IP
- **API directe** : pas besoin de client propriétaire, n'importe quel `curl` fonctionne

L'image Docker officielle de LinuxServer encapsule tout ça proprement. Un conteneur léger qui tourne en fond et met à jour ton IP automatiquement. Le combo DuckDNS Docker te libère de la gestion manuelle de ton IP publique.

## Prérequis

- Un serveur Docker (NAS, VPS, Raspberry Pi, vieux PC… peu importe)
- Une IP publique réelle (vérifie que ton FAI ne te met pas en CGNAT)
- Un compte DuckDNS (création gratuite en 30 secondes sur duckdns.org)
- Ton token DuckDNS et le sous-domaine choisi

Pour vérifier si tu es en CGNAT, regarde l'IP WAN affichée sur ta box et compare-la avec `curl ifconfig.me`. Si les deux sont différentes, tu es derrière un CGNAT. Dans ce cas, DuckDNS ne suffira pas. Reporte-toi au guide [Cloudflare Tunnel](/cloudflare-tunnel-docker-homelab/) à la place.

## Mise en place avec Docker Compose

Tu crées un dossier pour ton conteneur DuckDNS et tu places un `docker-compose.yml` dedans :

```yaml
services:
  duckdns:
    image: lscr.io/linuxserver/duckdns:latest
    container_name: duckdns
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Paris
      - SUBDOMAINS=tonnom
      - TOKEN=votre-token-duckdns
      - LOG_FILE=false
    volumes:
      - ./config:/config
    restart: unless-stopped
```

Remplace `tonnom` par le sous-domaine choisi sur DuckDNS et `votre-token-duckdns` par ton token personnel (visible sur la page d'accueil une fois connecté).

Lance le conteneur :

```bash
docker compose up -d
```

Et c'est tout. Le conteneur envoie immédiatement ton IP à DuckDNS, puis vérifie toutes les 5 minutes si elle a changé.

## Explication du docker-compose.yml

Pendant que le conteneur démarre, détaillons les variables importantes :

| Variable | Description |
|---|---|
| `SUBDOMAINS` | Ton sous-domaine DuckDNS (sans le `.duckdns.org`) |
| `TOKEN` | Ton token d'authentification DuckDNS |
| `LOG_FILE` | `true` pour écrire un log dans `/config/duckdns.log` |
| `TZ` | Fuseau horaire pour les timestamps de log |

Le volume `/config` est optionnel si tu désactives les logs. Par contre, il devient utile si tu actives `LOG_FILE=true` pour déboguer. Le conteneur tourne avec les droits de l'utilisateur 1000:1000, ce qui évite de tourner en root inutilement.

Si tu gères plusieurs sous-domaines (par exemple `home.duckdns.org` et `lab.duckdns.org`), sépare-les par des virgules dans `SUBDOMAINS` :

```yaml
- SUBDOMAINS=home,lab
```

Un seul conteneur suffit pour mettre à jour plusieurs sous-domaines avec le même token.

## Vérification et test

Attends quelques secondes après le démarrage, puis vérifie que ton DNS pointe bien vers ton IP :

```bash
nslookup tonnom.duckdns.org
```

L'adresse retournée doit correspondre à ton IP publique. Si ce n'est pas le cas, consulte les logs du conteneur :

```bash
docker logs duckdns
```

Les messages types indiquent `OK` quand la mise à jour réussit. Si tu vois une erreur `KO`, vérifie que ton token est correct et que le sous-domaine existe bien sur ton compte DuckDNS.

Une fois le DNS résolu correctement, tu peux ouvrir le port 80 ou 443 de ta box vers ton serveur et accéder à tes services via `https://tonnom.duckdns.org`. Pour automatiser les certificats SSL et le routing, installe [Nginx Proxy Manager](/nginx-proxy-manager-docker-guide/). Tu auras un vrai nom de domaine fonctionnel avec HTTPS en quelques clics.

## Intégration avec un reverse proxy

DuckDNS seul donne un nom de domaine qui pointe vers ton IP. Mais il ne gère pas les ports, ni les certificats SSL, ni le routage vers différents services. C'est là qu'un reverse proxy entre en jeu.

Avec [Nginx Proxy Manager](/nginx-proxy-manager-docker-guide/), tu configures un host proxy pour `tonnom.duckdns.org` qui pointe vers ton conteneur interne (par exemple `http://nextcloud:80`). NPM gère automatiquement le certificat Let's Encrypt pour ton domaine DuckDNS. Résultat : tu tapes `https://tonnom.duckdns.org` et tu arrives sur ton Nextcloud, sans warning de certificat, sans port bizarre dans l'URL.

Si tu préfères un resolver DNS local performant pour ton réseau interne, jette aussi un œil à [Unbound Docker](/unbound-docker-dns-recursif/). Il n'a rien à voir avec le DDNS public, mais c'est un excellent complément pour accélérer les requêtes DNS dans ton homelab.

## DuckDNS vs les alternatives

| Critère | DuckDNS | Cloudflare Tunnel | No-IP (gratuit) |
|---|---|---|---|
| **Prix** | Gratuit | Gratuit | Gratuit (renouvellement mensuel obligatoire) |
| **IP publique requise** | Oui | Non | Oui |
| **Ouverture de ports** | Oui | Non | Oui |
| **Certificat SSL** | Via reverse proxy | Natif (Cloudflare) | Via reverse proxy |
| **CGNAT compatible** | Non | Oui | Non |
| **Complexité** | Très simple | Simple | Simple |

DuckDNS brille par sa simplicité extrême. Si tu as une IP publique et que tu veux juste un nom de domaine stable sans te prendre la tête, c'est le choix le plus rapide. Si tu es en CGNAT ou que tu refuses d'ouvrir des ports, [Cloudflare Tunnel](/cloudflare-tunnel-docker-homelab/) est ta seule issue viable.

## Sécurité : ouvrir des ports, c'est sérieux

DuckDNS implique d'ouvrir des ports sur ta box internet. C'est pratique, mais ça expose ton serveur au monde entier. Quelques règles d'or :

- Ouvre uniquement les ports nécessaires (80 et 443 pour un reverse proxy, un seul port pour un VPN)
- Ne jamais exposer le port 22 (SSH) directement sur Internet
- Utilise un pare-feu comme UFW sur ton serveur
- Pense à [CrowdSec Docker](/crowdsec-docker-securite-collaborative/) pour une protection collaborative contre les attaques brute-force

Si tu veux un accès distant sans exposer quoique ce soit, préfère un VPN comme [WireGuard](/wireguard-docker-vpn-homelab/) ou Tailscale. DuckDNS, c'est pour exposer des services publics, pas pour administrer ton serveur à distance.

## Conclusion

DuckDNS Docker est l'outil DDNS le plus honnête que je connaisse. Gratuit, sans chichis, il fait exactement ce qu'il promet : maintenir ton nom de domaine à jour avec ton IP dynamique. Déployé en Docker Compose, il disparaît dans le décor et ne te demande plus jamais d'intervention. Associe-le à un reverse proxy et un pare-feu, et tu as une infrastructure d'accès distant propre pour zéro euro.