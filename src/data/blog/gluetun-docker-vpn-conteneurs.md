---
title: "Gluetun Docker : faire passer tes conteneurs par un VPN"
description: Gluetun docker route tes conteneurs derriere un VPN avec kill switch integre. Installation WireGuard, Docker Compose et depannage pas a pas.
pubDatetime: "2026-10-10T11:02:11+02:00"
modDatetime: "2026-10-09T08:00:00.000Z"
author: Brandon
tags:
  - reseau
  - docker
  - vpn
  - wireguard
  - guide
  - intermediaire
featured: false
draft: false
focusKeyword: gluetun docker
faqs:
  - question: "Gluetun docker ralentit-il mes téléchargements ?"
    answer: "Un peu, surtout en OpenVPN. En WireGuard la perte est faible, souvent sous 10 % si ton VPN et ton lien internet le permettent."
  - question: "Que se passe-t-il si le VPN tombe en pleine nuit ?"
    answer: "Le kill switch coupe le trafic des conteneurs attachés. Ils restent injoignables jusqu'à ce que gluetun reconnecte, aucune fuite vers ton FAI."
  - question: "Je peux faire passer Sonarr ou qBittorrent par Gluetun ?"
    answer: "Oui, via network_mode: service:gluetun sur le conteneur cible. Ses ports s'exposent alors sur le conteneur gluetun, pas sur le sien."
---
> 💡 **TL;DR**
> - Gluetun docker isole ta connexion VPN dans un seul conteneur : les autres (Sonarr, qBittorrent, Jellyfin) s'y attachent via `network_mode: service:gluetun`
> - Kill switch intégré par règles de pare-feu : si le tunnel tombe, le trafic est coupé, jamais basculé sur ton FAI
> - Compatible WireGuard et OpenVPN, une vingtaine de fournisseurs supportés, image officielle `qmcgaw/gluetun`

## Gluetun docker : le VPN qui protège tes conteneurs, pas toute ta machine

Tu veux que ton client torrent ou ton gestionnaire de séries passe par un VPN, mais pas forcément tout ton homelab. Installer un VPN système sur l'hôte, c'est du tout ou rien : chaque conteneur en profite, ou aucun. Chez moi, je ne veux pas que mon Jellyfin ou mon Nextcloud passent par un tunnel chiffré pour rien, juste parce qu'un conteneur voisin télécharge.

C'est exactement le problème que règle **gluetun**, un conteneur Go développé par qdm12, disponible sur [github.com/qdm12/gluetun](https://github.com/qdm12/gluetun) sous licence MIT. Il fait une seule chose : porter une connexion VPN, OpenVPN ou WireGuard, et laisser d'autres conteneurs partager sa pile réseau. Rien d'autre tourne dedans, pas de service annexe, juste le tunnel et un pare-feu qui verrouille tout le reste.

## Table des matières

## Pourquoi isoler le VPN dans un conteneur gluetun docker

Un VPN au niveau de l'hôte protège tout, y compris ce qui n'en a pas besoin. Il complique aussi le retour en arrière : tu coupes le VPN système, tu perds l'accès internet de ta machine entière le temps de débugger.

Avec gluetun docker, le découpage est net. Un seul conteneur gère le tunnel, et tu décides conteneur par conteneur qui y passe. Ton Jellyfin reste en accès direct, rapide, sans latence ajoutée. Ton qBittorrent ou ton Sonarr, eux, sortent uniquement via le VPN. Si gluetun tombe, ces deux-là perdent le réseau, mais le reste de ton homelab continue de tourner normalement.

Autre avantage, la portabilité. Tu changes de fournisseur VPN, tu modifies deux ou trois variables d'environnement dans le service gluetun, et tous les conteneurs attachés suivent sans qu'on touche à leur configuration.

## Installation : docker-compose avec gluetun docker et WireGuard

L'image officielle est `qmcgaw/gluetun`, aussi publiée sur `ghcr.io/qdm12/gluetun`. Elle a besoin de la capacité `NET_ADMIN` et du périphérique `/dev/net/tun` pour monter le tunnel. Voici une base de configuration avec un fournisseur en WireGuard :

```yaml
services:
  gluetun:
    image: qmcgaw/gluetun
    container_name: gluetun
    cap_add:
      - NET_ADMIN
    devices:
      - /dev/net/tun:/dev/net/tun
    environment:
      - VPN_SERVICE_PROVIDER=mullvad
      - VPN_TYPE=wireguard
      - WIREGUARD_PRIVATE_KEY=ta_cle_privee_wireguard
      - WIREGUARD_ADDRESSES=10.64.xxx.xxx/32
      - SERVER_COUNTRIES=Netherlands
      - FIREWALL_OUTBOUND_SUBNETS=192.168.1.0/24
    ports:
      - "8080:8080"
    restart: unless-stopped
```

La clé privée et l'adresse WireGuard viennent du fichier de configuration que ton fournisseur (Mullvad, Surfshark, ProtonVPN, parmi une vingtaine de providers supportés) te génère sur son tableau de bord. Pas la clé affichée sur la page de gestion des appareils : celle du fichier `.conf` ou `.json` téléchargé, champ `PrivateKey`. `FIREWALL_OUTBOUND_SUBNETS` doit contenir ton sous-réseau LAN en CIDR, sinon tu perds l'accès depuis ton réseau local aux ports publiés par gluetun.

Avec OpenVPN, le principe est identique, seules les variables changent : `VPN_TYPE=openvpn`, `OPENVPN_USER` et `OPENVPN_PASSWORD` à la place de la clé WireGuard.

## Kill switch : comment gluetun docker coupe le trafic au lieu de fuiter

C'est le vrai argument de gluetun docker face à un simple client VPN lancé dans un conteneur à la main. Le pare-feu interne n'autorise que deux routes de sortie : vers le serveur VPN lui-même, et à travers le tunnel une fois établi. Tout le reste est jeté.

Concrètement, si le tunnel se coupe, pas de bascule silencieuse vers ta connexion FAI. Les conteneurs attachés à gluetun perdent purement et simplement le réseau, jusqu'à la reconnexion. C'est brutal, mais c'est le but : un kill switch qui laisse passer "juste un peu" de trafic en clair n'en est pas un.

Pour vérifier que ça marche vraiment chez toi, ne te contente pas de lire la doc. Entre dans un conteneur attaché et compare l'IP publique avec et sans le VPN actif :

```bash
docker exec -it qbittorrent curl -s ifconfig.me
docker stop gluetun
docker exec -it qbittorrent curl -s --max-time 5 ifconfig.me
```

La première commande doit renvoyer l'IP du serveur VPN. La seconde doit échouer, pas renvoyer ton IP publique réelle. Si elle répond, ton kill switch fuit, et il faut revoir la config réseau avant de faire confiance au conteneur.

## Faire passer un autre conteneur par gluetun docker

C'est là que gluetun docker devient intéressant au quotidien : d'autres conteneurs peuvent partager sa pile réseau sans avoir leur propre configuration VPN. Dans le `docker-compose.yml`, un conteneur comme qBittorrent se déclare avec `network_mode` plutôt qu'avec son propre réseau :

```yaml
services:
  qbittorrent:
    image: lscr.io/linuxserver/qbittorrent
    network_mode: "service:gluetun"
    depends_on:
      - gluetun
    environment:
      - PUID=1000
      - PGID=1000
```

Détail qui piège tout le monde la première fois : les ports du conteneur attaché ne se déclarent plus sur lui, mais sur gluetun. Si qBittorrent écoute sur `8080`, c'est dans le bloc `ports` de gluetun qu'il faut l'ouvrir, pas dans celui de qBittorrent, qui n'a d'ailleurs plus le droit d'en déclarer. Deuxième piège : si tu redémarres ou mets à jour gluetun, tous les conteneurs qui partagent sa pile réseau perdent la connexion et doivent être relancés aussi, Docker ne le fait pas pour toi automatiquement.

## Gluetun docker face aux autres approches réseau

Gluetun docker n'est pas la seule façon de maîtriser le trafic réseau de ton homelab, et il ne joue pas dans la même catégorie que tout le monde.

Si ton besoin, c'est relier tes propres machines entre elles en mesh VPN plutôt que masquer ta sortie vers des services tiers, regarde plutôt [Headscale, le serveur Tailscale auto-hébergé](/headscale-docker-tailscale-self-hosted/). Les deux cas d'usage ne se recouvrent pas : Headscale connecte tes appareils entre eux, gluetun docker fait sortir un conteneur par un fournisseur VPN commercial.

Si ta préoccupation, c'est plutôt exposer un service vers l'extérieur sans ouvrir de port sur ta box, c'est le problème inverse, et [Cloudflare Tunnel](/cloudflare-tunnel-docker-homelab/) répond à ce besoin-là, pas gluetun docker. Les deux outils peuvent cohabiter sans se gêner sur le même hôte.

Pour surveiller que ton kill switch tient dans le temps et détecter une coupure de tunnel avant qu'elle ne passe inaperçue, [SNMPd en conteneur](/snmpd-docker-monitorer-reseau/) te donne une base de supervision réseau simple à brancher sur ton monitoring existant.

## Dépannage : les pièges classiques avec gluetun docker

**Le conteneur attaché ne sort jamais sur internet.** Vérifie d'abord que gluetun lui-même est bien connecté, avec `docker logs gluetun`. Tant que le tunnel n'est pas monté, tout ce qui partage sa pile réseau reste bloqué, c'est voulu.

**Impossible d'atteindre l'interface web depuis ton LAN.** Le port doit être publié sur le service gluetun, et `FIREWALL_OUTBOUND_SUBNETS` doit inclure ton sous-réseau. Sans ça, le pare-feu interne bloque aussi les retours vers ton réseau local, pas seulement vers internet.

**Le port forwarding ne marche pas.** Certains fournisseurs comme Mullvad attribuent un port dynamique qu'il faut déclarer dans `FIREWALL_VPN_INPUT_PORTS`. Sans cette variable, gluetun bloque le trafic entrant même si ton fournisseur l'a bien ouvert côté serveur.

**Tout casse après une mise à jour.** Les conteneurs attachés à gluetun docker ne survivent pas à son redémarrage. Relance-les dans l'ordre : gluetun d'abord, les conteneurs dépendants ensuite, avec un petit délai pour laisser le tunnel se rétablir.

## Conclusion

Gluetun docker fait une chose, et il la fait bien : isoler un tunnel VPN dans un conteneur jetable, avec un kill switch qui ne laisse rien fuiter quand ça tombe. T'évites le VPN système qui englobe toute ta machine, tu gardes un découpage net entre ce qui doit sortir masqué et ce qui n'en a pas besoin.

Le vrai travail, c'est la vérification : teste le kill switch à froid, pas seulement une fois à l'installation. Un tunnel qui tient un mois peut très bien se reconnecter en clair le jour où tu changes de fournisseur ou de version d'image. Mon conseil : automatise le test `curl` du kill switch dans ton monitoring existant, tu n'auras pas à y repenser.
