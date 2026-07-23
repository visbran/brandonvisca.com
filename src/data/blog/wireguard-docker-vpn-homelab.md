---
title: "WireGuard Docker : VPN ultra-simple pour ton homelab"
description: "Guide WireGuard Docker : déploie un VPN simple et sécurisé avec Docker Compose. Comparatif, config pas à pas et astuces homelab."
pubDatetime: "2026-06-23T08:00:00.000Z"
modDatetime: "2026-06-23T08:00:00.000Z"
author: Brandon
tags:
  - wireguard
  - docker
  - securite
  - vpn
  - reseau
  - debutant
featured: false
draft: false
focusKeyword: wireguard docker
faqs:
  - question: "Quelle différence entre WireGuard et OpenVPN ?"
    answer: "WireGuard est plus léger (~4 000 lignes de code contre 400 000+ pour OpenVPN), plus rapide (3 à 4×), et utilise une cryptographie moderne (Curve25519, ChaCha20). Sa configuration tient en 10 lignes contre des centaines pour OpenVPN."
  - question: "WireGuard fonctionne-t-il derrière un routeur NAT ?"
    answer: "Oui, grâce au UDP hole punching et au PersistentKeepalive qui maintient le mapping NAT actif. Il suffit de rediriger le port UDP (51820 par défaut) sur ta box vers ton serveur Docker."
  - question: "Puis-je utiliser WireGuard Docker sur un Raspberry Pi ?"
    answer: "Absolument. WireGuard est intégré au kernel Linux moderne et consomme très peu de ressources. L'image linuxserver/wireguard tourne parfaitement sur un Raspberry Pi 4 avec 1 Go de RAM."
ogImage: ""
---
> 💡 **TL;DR**
> - WireGuard est un VPN moderne, léger et rapide qui remplace avantageusement OpenVPN dans ton homelab
> - Tu le déploies en 3 minutes avec Docker Compose et l'image `linuxserver/wireguard`
> - Un fichier de config de 10 lignes suffit, contre des centaines pour OpenVPN
> - Cryptographie moderne (Curve25519, ChaCha20), performances supérieures, batterie préservée sur mobile
> - Docker Compose complet, tableau comparatif WireGuard vs OpenVPN et checklist sécurité inclus ci-dessous

## Table des matières

## Pourquoi un VPN dans ton homelab ?

Tu as monté ton homelab. Nextcloud, Vaultwarden, Homer, tout tourne sur ton serveur derrière ta box Internet. Sauf que quand tu sors de chez toi, plus rien. Tu veux consulter ton gestionnaire de mots de passe depuis un café, synchroniser tes fichiers depuis le train, ou juste accéder à ton tableau de bord homelab sans ouvrir des ports à tout internet.

La solution classique, c'est d'ouvrir un port sur ta box et d'exposer tes services directement. Mauvaise idée. Tu te retrouves avec des scanners automatiques qui cognent à ta porte toutes les 30 secondes, des bots qui testent des credentials, et une surface d'attaque qui grandit chaque fois que tu ajoutes un service. Si tu as déjà lu mon [guide Fail2Ban Docker](/fail2ban-docker-securite-serveur/), tu sais que les tentatives de brute-force sont incessantes.

Un VPN résout ce problème de façon élégante. Tu crées un tunnel chiffré entre ton appareil (téléphone, laptop, tablette) et ton serveur. Une fois connecté, tu es "virtuellement" chez toi. Tes services restent derrière ton firewall, invisibles du web. Seuls les appareils authentifiés peuvent entrer. C'est la différence entre laisser ta porte d'entrée grande ouverte et avoir un interphone avec badge.

Et quand tu parles de VPN simple, rapide et moderne, tu parles de WireGuard.

## WireGuard, c'est quoi exactement ?

WireGuard est un protocole VPN open-source créé en 2016 par Jason A. Donenfeld. Il a été intégré au kernel Linux en 2020 et est désormais considéré comme l'état de l'art en matière de VPN. Contrairement à OpenVPN ou IPsec, WireGuard repose sur une philosophie radicale : **moins de code, moins de configuration, plus de sécurité**.

Le code fait environ 4 000 lignes. OpenVPN en fait plus de 400 000 avec OpenSSL. Moins de code signifie moins de bugs, moins de vulnérabilités, et une auditabilité réaliste. WireGuard utilise des primitives cryptographiques modernes et éprouvées : Curve25519 pour l'échange de clés, ChaCha20 pour le chiffrement, Poly1305 pour l'authentification, et BLAKE2s pour le hachage. Pas de choix d'algorithme à la configuration, pas de cipher suites obsolètes à désactiver.

Côté réseau, WireGuard est un VPN de couche 3 (IP) plutôt que couche 2 ou couche applicative. Chaque pair (peer) possède une clé publique qui l'identifie. Pas de certificats X.509, pas d'infrastructure PKI, pas de handshake TLS compliqué. Tu génères une paire de clés, tu échanges les clés publiques entre serveur et client, et c'est prêt.

Pour l'auto-hébergement, WireGuard est particulièrement pertinent parce qu'il consomme peu de ressources. Sur un Raspberry Pi ou un VPS low-cost, il tourne sans accroc. La batterie de ton téléphone en profite aussi : la latence de handshake réduite et l'absence de keepalive agressif font que WireGuard est plus sobre que OpenVPN sur mobile.

Dans la pratique, pour un homelab Dockerisé, tu vas déployer WireGuard via un conteneur qui gère le serveur et génère les configurations clients automatiquement. Pas besoin d'installer un serveur Debian complet avec `wg-quick` et des scripts shell. Un fichier `docker-compose.yml` bien conçu suffit pour ton setup **wireguard docker**.

## WireGuard Docker vs OpenVPN : le comparatif technique

| Critère | WireGuard | OpenVPN |
|---------|-----------|---------|
| Taille du code | ~4 000 lignes (kernel) | ~400 000+ lignes (avec OpenSSL) |
| Cryptographie | Curve25519, ChaCha20, Poly1305 | Configurable (souvent AES-256-CBC/GCM) |
| Performance | 3-4× plus rapide | Bonne, mais surcharge protocolaire |
| Latence handshake | Quasi instantané | TLS handshake multi-RTT |
| Configuration | Clé publique/privée, 10 lignes | Certificats X.509, fichiers de 200+ lignes |
| Mobilité (roaming) | Gérée nativement | Reconnexion lente au changement de réseau |
| Consommation batterie | Faible (mobile) | Élevée (keepalive fréquents) |
| Auditabilité | Possible et réalisée | Quasi impossible à cause de la taille |
| Support NAT/firewall | UDP hole punching intégré | TCP/UDP, plus complexe à travers NAT |
| Maturité | Stable, intégré kernel Linux | Très mature, très éprouvé |
| Complexité déploiement | Très faible | Moyenne à élevée |

**Verdict** : pour un homelab personnel, WireGuard est le choix par défaut. OpenVPN reste pertinent dans des contextes d'entreprise où la conformité FIPS ou l'intégration avec des PKI existantes est obligatoire. Pour toi et tes appareils, WireGuard est plus rapide à déployer, plus rapide à l'exécution, et plus simple à auditer.

> **Tu veux aller plus loin ?** Si tu cherches un VPN zero-trust avec authentification SSO et politiques d'accès granulaires basées sur WireGuard, j'ai publié un guide complet sur [Firezone Docker](/firezone-docker-vpn-zero-trust/).

## Prérequis

Avant de lancer ton conteneur WireGuard, vérifie ces quelques points :

- Un serveur Docker fonctionnel (si ce n'est pas encore fait, mon [guide Docker Compose pour débutants](/docker-debutant-services-auto-heberger/) t'explique comment monter ta stack)
- Un port UDP ouvert sur ta box/routeur, redirigé vers ton serveur (par défaut 51820/UDP)
- Les modules kernel WireGuard présents (inclus dans les kernels Linux modernes, vérifier avec `modprobe wireguard`)
- Un nom de domaine (optionnel mais recommandé pour éviter de taper une IP dynamique)
- Docker et Docker Compose installés sur le serveur
- Un minimum de 512 Mo de RAM et quelques Mo d'espace disque

Conseil : si tu utilises un VPS cloud, vérifie que ton hébergeur autorise le trafic UDP entrant. Certains free tiers ou environnements restrictifs bloquent les ports UDP non standards.

## Docker Compose complet pour ton VPN WireGuard

Voici le fichier `docker-compose.yml` prêt à l'emploi. Il utilise l'image `linuxserver/wireguard`, maintenue activement, avec la génération automatique des configurations clients. C'est le cœur de ton déploiement **wireguard docker**.

```yaml
version: "3.8"

services:
  wireguard:
    image: lscr.io/linuxserver/wireguard:latest
    container_name: wireguard
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Paris
      - SERVERURL=vpn.tondomaine.com # ou ton IP publique
      - SERVERPORT=51820
      - PEERS=phone,laptop,tablette # noms des clients
      - PEERDNS=1.1.1.1,9.9.9.9 # DNS Cloudflare + Quad9
      - INTERNAL_SUBNET=10.13.13.0
      - ALLOWEDIPS=0.0.0.0/0 # tunnel tout le trafic
      - PERSISTENTKEEPALIVE=25
      - LOG_CONFS=true # génère les QR codes et fichiers de conf
    volumes:
      - ./wireguard/config:/config
      - /lib/modules:/lib/modules:ro
    ports:
      - "51820:51820/udp"
    sysctls:
      - net.ipv4.conf.all.src_valid_mark=1
    restart: unless-stopped
```

**Points importants :**

- `cap_add: NET_ADMIN` est obligatoire pour que le conteneur puisse créer l'interface réseau tunnel.
- `SYS_MODULE` et le volume `/lib/modules` permettent au conteneur d'accéder aux modules kernel WireGuard.
- `SERVERURL` doit être ton IP publique ou un nom de domaine pointant vers ton serveur.
- `PEERS` définit le nombre et les noms des clients. Change les noms ou ajoute-en autant que tu veux.
- `ALLOWEDIPS=0.0.0.0/0` route tout le trafic internet via le VPN. Si tu veux seulement accéder au réseau local, remplace par `10.13.13.0/24,192.168.1.0/24` (adapte selon ton LAN).
- `PERSISTENTKEEPALIVE=25` envoie un paquet toutes les 25 secondes pour maintenir le tunnel ouvert derrière un NAT strict.

Lance la stack :

```bash
cd /chemin/vers/wireguard
docker compose up -d
```

Le premier démarrage génère les clés du serveur et les configurations pour chaque peer. Les fichiers `.conf` et les QR codes sont disponibles dans `./wireguard/config/`.

Si tu débutes avec Docker Compose, ce fichier s'intègre parfaitement dans une stack plus large. Tu peux l'ajouter à ton `docker-compose.yml` principal ou le garder isolé. Pour organiser proprement tes services, jette un œil à mon [guide Docker Compose pour débutants](/docker-debutant-services-auto-heberger/).

## Configuration pas à pas

### Étape 1 : Créer le dossier et le fichier Compose

```bash
mkdir -p ~/docker/wireguard
cd ~/docker/wireguard
```

Copie le `docker-compose.yml` ci-dessus dans ce dossier.

### Étape 2 : Adapter les variables

Modifie au minimum :
- `SERVERURL` : ton nom de domaine ou IP publique
- `TZ` : ton fuseau horaire (`Europe/Paris`, `Europe/Brussels`, etc.)
- `PEERS` : les noms des appareils que tu veux connecter
- `PEERDNS` : les DNS que tu veux utiliser (Cloudflare `1.1.1.1` et Quad9 `9.9.9.9` sont des choix sains)

### Étape 3 : Ouvrir le port sur ta box

Redirige le port UDP 51820 de ta box/routeur vers l'IP locale de ton serveur Docker. La procédure varie selon les modèles (Freebox, Livebox, Bbox, etc.), mais elle se trouve généralement dans les paramètres "Redirection de ports" ou "NAT/PAT".

### Étape 4 : Lancer le conteneur

```bash
docker compose up -d
docker logs -f wireguard
```

Les premiers logs montrent la génération des clés et des configs. Attends la fin du setup avant de passer à l'étape suivante.

### Étape 5 : Vérifier le serveur

```bash
docker exec -it wireguard wg show
```

Tu dois voir l'interface `wg0` avec la clé publique du serveur et la liste des peers configurés (sans handshake pour l'instant, c'est normal).

## Générer les clients

Les configurations clients sont générées automatiquement au premier démarrage. Tu les trouves dans le volume monté :

```bash
ls ~/docker/wireguard/config/peer_*/
```

Chaque dossier `peer_NOM` contient :
- `peer_NOM.conf` : fichier de configuration WireGuard
- `peer_NOM.png` : QR code scannable avec l'app mobile WireGuard

### Sur mobile (iOS/Android)

1. Installe l'application WireGuard depuis l'App Store ou Google Play
2. Appuie sur le `+` en bas à droite
3. Choisis "Créer depuis le QR code"
4. Scanne le PNG affiché sur ton écran (ou transfère-le sur ton téléphone)
5. Active le tunnel

### Sur ordinateur (Windows/macOS/Linux)

1. Installe le client WireGuard officiel
2. Importe le fichier `.conf`
3. Active le tunnel

### Pour ajouter un nouveau client

Tu peux modifier la variable `PEERS` en ajoutant un nouveau nom, puis relancer :

```bash
docker compose down
# édite le docker-compose.yml pour ajouter le nouveau peer
docker compose up -d
```

Le conteneur génère automatiquement la nouvelle configuration sans toucher aux peers existants.

## Sécuriser ton tunnel VPN

Un VPN mal configuré est un risque. Voici la checklist des points à valider :

- [ ] **Changer le port par défaut** : 51820 est connu des scanners. Si tu veux réduire le bruit, utilise un port non standard (> 50000) et adapte la redirection.
- [ ] **Restreindre ALLOWEDIPS** : si tu n'as pas besoin de router tout ton trafic internet par le VPN, limite aux IPs de ton homelab. Ça réduit la charge et évite de surconsommer la bande passante.
- [ ] **Mettre à jour l'image régulièrement** : `docker compose pull && docker compose up -d` pour récupérer les patches kernel et les mises à jour de l'image.
- [ ] **Activer l'authentification à deux facteurs** sur tous les services accessibles via le VPN. Le VPN sécurise l'accès réseau, pas l'application elle-même.
- [ ] **Surveiller les connexions** : utilise un outil de monitoring pour t'assurer que ton serveur WireGuard reste accessible. [Uptime Kuma](/uptime-kuma-2-0-monitoring-auto-heberge/) peut monitorer un port UDP ou un healthcheck HTTP si tu exposes un service derrière. Pour une supervision plus poussée de ton infrastructure complète (CPU, RAM, conteneurs, alerting Telegram), tu peux aussi déployer [Zabbix avec Docker](/zabbix-docker-monitoring-infrastructure/).
- [ ] **Limiter les peers** : chaque peer est un vecteur d'attaque potentiel. Supprime les configs des appareils que tu n'utilises plus.
- [ ] **Bloquer les IPs malveillantes** : couple WireGuard avec un firewall (UFW, iptables) et un outil comme [Fail2Ban](/fail2ban-docker-securite-serveur/) pour bloquer les scanners sur tes autres services.
- [ ] **Utiliser des DNS filtrants** : `PEERDNS=1.1.1.1` est bien, mais tu peux aussi utiliser ton propre [AdGuard Home](/adguard-home-docker-guide-2026/) pour bloquer les trackers et pubs au niveau DNS.
- [ ] **Ne pas exposer le port de gestion Docker** : le port 2375/2376 ne doit jamais être accessible depuis l'extérieur. Le VPN ne rend pas cette exposition acceptable.

### Rotation des clés

WireGuard n'a pas de mécanisme automatique de rotation de clés. Il est recommandé de régénérer les paires de clés tous les 6 à 12 mois. Pour cela :

```bash
docker compose down
rm -rf ~/docker/wireguard/config/peer_*
docker compose up -d
```

Puis réimporte les nouveaux fichiers `.conf` sur tes appareils. C'est un peu fastidieux mais cela garantit que d'anciennes clés compromises ne restent pas actives indéfiniment.

## Dépannage courant

### Le tunnel ne s'établit pas (handshake échoue)

1. Vérifie que le port UDP est bien redirigé sur ta box et non bloqué par un firewall
2. Confirme que `SERVERURL` correspond bien à ton IP publique ou ton domaine
3. Vérifie que les clés publiques sont bien échangées (`docker exec wireguard wg show` doit lister les peers)
4. Assure-toi que le client utilise bien le port UDP correspondant
5. Teste depuis un autre réseau (4G) pour écarter un problème de firewall local

### Pas d'accès Internet quand le tunnel est actif

1. Vérifie le paramètre `ALLOWEDIPS`. `0.0.0.0/0` route tout le trafic. Si tu veux seulement accéder au LAN, remplace par `10.13.13.0/24,192.168.1.0/24`.
2. Vérifie l'IP forwarding sur le serveur hôte :
   ```bash
   sudo sysctl net.ipv4.ip_forward
   ```
   Si c'est `0`, active-le :
   ```bash
   echo 'net.ipv4.ip_forward=1' | sudo tee /etc/sysctl.d/99-wireguard.conf
   sudo sysctl --system
   ```
3. Vérifie que le conteneur a bien les capabilities `NET_ADMIN` et `SYS_MODULE`

### Le client mobile se déconnecte constamment

Augmente `PERSISTENTKEEPALIVE` (par exemple à `25`) ou baisse-le selon ta consommation de batterie. Si tu es derrière un NAT strict (opérateur mobile), ce keepalive est essentiel pour maintenir le mapping NAT actif.

### "Unable to access interface: Operation not permitted"

Le conteneur n'a pas les capabilities nécessaires. Vérifie que `cap_add` contient bien `NET_ADMIN` et `SYS_MODULE`, et que Docker est exécuté sur un kernel avec les modules WireGuard chargés (`lsmod | grep wireguard`).

### Les DNS ne répondent pas

Vérifie que `PEERDNS` est correctement défini. Si tu utilises un DNS local (comme AdGuard Home ou Pi-hole), assure-toi que son IP est accessible depuis le sous-réseau WireGuard (`10.13.13.0/24`).

## Conclusion

WireGuard est ce que le VPN aurait dû être depuis le début : simple, rapide, sécurisé et sans bullshit. En le containerisant avec Docker, tu ajoutes un élément essentiel à la sécurité de ton homelab sans multiplier la complexité. Plus besoin d'OpenVPN avec ses certificats, ses fichiers de configuration kilométriques et sa consommation énergétique sur mobile.

Avec le `docker-compose.yml` ci-dessus, tu as un serveur WireGuard fonctionnel en quelques minutes. Chaque nouveau client est une ligne dans `PEERS` et un QR code à scanner. C'est la simplicité même pour déployer un **tunnel vpn docker** sécurisé.

Une fois ton VPN en place, tu peux commencer à exposer tes services de manière plus intelligente. Si tu n'as pas d'IP publique fixe et que tu veux exposer certains services sur Internet sans ouvrir de ports, [Cloudflare Tunnel Docker](/cloudflare-tunnel-docker-homelab/) est la solution la plus simple. Si tu utilises Tailscale et que tu veux une exposition automatique de tes conteneurs Docker sans config manuelle, [Tsdproxy Docker](/tsdproxy-docker-tailscale-proxy/) est fait pour ça. Si tu préfères un reverse proxy public avec HTTPS automatique, [Caddy Docker](/caddy-docker-reverse-proxy-guide/) gère les certificats Let's Encrypt. Et n'oublie pas de monitorer l'accessibilité de ton tunnel avec [Uptime Kuma](/uptime-kuma-2-0-monitoring-auto-heberge/). Bon tunneling.
