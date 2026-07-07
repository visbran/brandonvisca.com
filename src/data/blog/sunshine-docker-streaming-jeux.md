---
title: "Sunshine Docker : ton serveur de streaming de jeux maison avec Moonlight"
description: "Déploie Sunshine sous Docker pour streamer tes jeux PC vers n'importe quel écran. Guide complet Moonlight + sunshine docker, réseau et latence."
pubDatetime: "2026-07-05T10:00:00.000Z"
modDatetime: "2026-07-05T10:00:00.000Z"
author: Brandon Visca
tags:
  - intermediaire
  - auto-hebergement
  - docker
  - gaming
  - streaming
  - homelab
featured: false
draft: false
focusKeyword: sunshine docker
faqs:
  - question: "Sunshine fonctionne-t-il avec n'importe quel jeu ?"
    answer: "Oui, Sunshine capture l'écran entier comme OBS. Tout jeu Steam, Epic, GOG ou standalone fonctionne. Les jeux avec anti-cheat kernel-level (certains titres compétitifs) peuvent poser problème, mais la majorité des jeux solo et coop passent sans souci."
  - question: "Quelle latence peut-on espérer avec Moonlight + Sunshine ?"
    answer: "En local (Ethernet ou Wi-Fi 5/6), la latence ajoutée est de 5 à 15 ms. C'est imperceptible pour 99% des jeux. En 4K 60 FPS, compte 10 à 20 ms supplémentaires selon l'encodeur et le réseau."
  - question: "Puis-je streamer en dehors de mon réseau local ?"
    answer: "Oui, mais il te faut un VPN ou un reverse proxy sécurisé. Le plus simple est un tunnel WireGuard vers ton homelab. N'ouvre JAMAIS Sunshine directement sur Internet sans protection."
ogImage: ""
---
> 💡 **TL;DR**
> - Sunshine = serveur de streaming de jeux open-source qui remplace NVIDIA GeForce Experience
> - Moonlight = client léger qui se connecte à Sunshine (Android, iOS, macOS, Linux, Windows, TV)
> - En Docker : un conteneur, quelques volumes, et tu joues sur ta TV depuis ton PC serveur
> - Latence quasi nulle en local, qualité 4K 120 FPS possible selon ton matériel

Tu as un bon PC dans ta chambre ou ton bureau, mais tu veux jouer sur le canapé devant la TV du salon. Ou bien tu as monté une bête de course dans ton placard et tu veux y accéder depuis ton laptop pas très puissant.

Jusqu'à récemment, la seule solution "simple" c'était NVIDIA GeForce Experience avec GameStream. Sauf que NVIDIA a tué GameStream en 2023. Et si t'as pas de carte NVIDIA, t'étais juste dans la merde.

**Sunshine** est arrivé comme alternative open-source, universelle et indépendante du fabricant de GPU. AMD, Intel, NVIDIA : tout le monde est le bienvenu. Et quand tu le mets dans un conteneur Docker, la mise à jour et la gestion deviennent triviales.

Dans ce guide, on installe Sunshine sur ton serveur, on le configure pour encoder en HEVC, on ajoute Moonlight sur tes appareils clients, et on optimise la latence pour que ce soit fluide.

## Table des matières

## Ce dont tu as besoin

Avant de lancer quoi que ce soit, vérifie que ton matériel suit :

- **Un PC/serveur avec GPU** : Intel iGPU (Quick Sync), AMD (VCE) ou NVIDIA (NVENC). Même un iGPU récent suffit pour du 1080p60.
- **Réseau local solide** : Ethernet câblé idéal, Wi-Fi 5 (AC) minimum, Wi-Fi 6 (AX) recommandé.
- **Docker et Docker Compose** installés sur le serveur.
- **Un client Moonlight** sur ton appareil cible (smartphone, tablette, TV Android, PC, macOS, Linux).

Si tu débutes avec Docker, j'ai écrit un guide qui liste [10 services essentiels à auto-héberger avec Docker](/docker-debutant-services-auto-heberger/). Sunshine en fait partie.

## Sunshine, c'est quoi exactement ?

Sunshine est un **serveur de streaming de jeux** open-source. Il capture l'écran de ton PC, l'encode en temps réel et l'envoie à un client via ton réseau local (ou à distance via VPN).

**Analogie simple :** c'est comme si tu avais une GeForce NOW chez toi, sauf que c'est TOI qui contrôles le serveur.

### Pourquoi Sunshine plutôt que Parsec ou Steam Link ?

| Critère | Sunshine | Parsec | Steam Link |
|---|---|---|---|
| **Open source** | ✅ Oui | 🔴 Non | 🔴 Non |
| **Client officiel** | Moonlight (open) | Parsec | Steam Link |
| **Qualité max** | 4K 120 FPS HDR | 4K 60 FPS | 1080p 60 FPS |
| **Encodeurs** | NVENC, QuickSync, VCE, AMF | NVENC, AMF | NVENC, QuickSync |
| **Audio** | 5.1/7.1 surround | Stéréo | Stéréo |
| **Hors réseau local** | VPN nécessaire | Oui (relay cloud) | Oui (Steam relay) |

**Verdict :**
- Tu veux du **4K 120 FPS HDR** sur ta TV → **Sunshine**
- Tu veux jouer avec des potes en co-op à distance → Parsec (plus simple)
- Tu veux juste streamer Steam rapidement → Steam Link (plus limité)

## Architecture et ports pour sunshine docker

Sunshine écoute sur plusieurs ports :

- **47989/tcp** : interface web d'administration
- **47984/tcp** : WebSocket pour la configuration
- **47998/udp** et **47999/udp** : streaming vidéo et audio
- **48000/udp** : contrôle (inputs clavier/souris/manette)
- **48010/udp** : RTP (temps réel)

En Docker, tu dois mapper TOUS ces ports. En mode `host` c'est plus simple, mais en mode bridge (port mapping explicite) c'est plus propre et sécurisé.

## Installation sunshine docker avec Docker Compose

Crée un dossier dédié :

```bash
mkdir -p ~/docker/sunshine && cd ~/docker/sunshine
```

Crée le fichier `docker-compose.yml` :

```yaml
version: "3.8"

services:
  sunshine:
    image: lizardbyte/sunshine:latest
    container_name: sunshine
    restart: unless-stopped
    # Mode host recommandé pour Sunshine (besoin d'accès au GPU et au réseau)
    network_mode: host
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Paris
    volumes:
      - ./config:/config/sunshine
      - /dev/shm:/dev/shm  # Mémoire partagée pour le capture d'écran
    devices:
      # Intel iGPU (Quick Sync)
      - /dev/dri:/dev/dri
      # Si NVIDIA : ajouter les runtime devices
    # Décommenter pour NVIDIA (nécessite le toolkit NVIDIA Docker)
    # runtime: nvidia
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: 1
    #           capabilities: [gpu]
```

Lance le conteneur :

```bash
docker compose up -d
```

Rends-toi sur `http://<IP-DU-SERVEUR>:47989` pour la configuration initiale.

> ⚠️ **Important :** le mode `network_mode: host` signifie que Sunshine utilise la pile réseau de l'hôte. C'est nécessaire pour que la découverte mDNS fonctionne et que les ports UDP soient correctement gérés. Si tu préfères le mode bridge, prépare-toi à mapper manuellement tous les ports UDP listés ci-dessus.

## Configuration initiale de Sunshine

### 1. Créer un compte administrateur

À la première connexion, Sunshine te demande de créer un utilisateur. Choisis un mot de passe fort, c'est l'accès à ton serveur de jeux.

### 2. Configurer l'encodeur

Va dans **Configuration > Audio/Video** :

| Réglage | Valeur recommandée |
|---|---|
| **Encoder** | Auto-détecté (QuickSync pour Intel, NVENC pour NVIDIA, AMF pour AMD) |
| **Résolution** | Native (ou 1920x1080 si le client est faible) |
| **FPS** | 60 ou 120 selon l'écran client |
| **Bitrate** | 20 Mbps pour 1080p60, 50 Mbps pour 4K60 |
| **Codec** | HEVC (H.265) si ton client le supporte, sinon H.264 |

L'encodeur matériel est crucial. Sans lui, le CPU encode en software et la latence explose.

### 3. Ajouter des applications

Dans **Applications**, ajoute les jeux ou launchers que tu veux streamer :

```
Name: Steam
Command: steam.exe  (ou /usr/bin/steam sur Linux)
Image path: (optionnel, logo Steam)
```

Tu peux aussi ajouter le bureau entier : laisse le champ Command vide.

### 4. Activer l'accès distant (optionnel, avec VPN)

Si tu veux jouer depuis l'extérieur, NE fais PAS confiance à l'UPnP. Utilise un VPN. J'ai détaillé la méthode dans mon guide sur [WireGuard Docker pour sécuriser l'accès à ton homelab](/wireguard-docker-vpn-homelab/). Une fois connecté en VPN, ton client Moonlight voit Sunshine comme s'il était en local.

## Installer Moonlight sur tes appareils

Moonlight est le client officiel de Sunshine. Il est disponible partout :

- **Android TV / Google TV** : Play Store (meilleure expérience TV)
- **iOS / Apple TV** : App Store
- **Windows / macOS / Linux** : [moonlight-stream.org](https://moonlight-stream.org)
- **Raspberry Pi** : paquet disponible pour Linux ARM
- **Chromebook** : app Android ou PWA

### Appairage

1. Ouvre Moonlight sur ton appareil client.
2. Il devrait découvrir automatiquement ton serveur Sunshine via mDNS (si tu es sur le même réseau local).
3. Sinon, ajoute manuellement l'IP du serveur.
4. Sunshine affiche un code PIN à 4 chiffres sur l'écran du serveur. Saisis-le dans Moonlight.
5. C'est appairé. Tu ne referas cette opération qu'une seule fois.

## Optimiser la latence

Le streaming de jeux vit ou meurt selon la latence. Voici les réglages qui comptent vraiment :

### Réseau

- **Ethernet câblé** : toujours privilégié pour le serveur. Un cable Cat5e suffit.
- **Wi-Fi** : Wi-Fi 5 (AC) minimum, Wi-Fi 6 (AX) ou 6E recommandé. Évite le Wi-Fi 2.4 GHz, la latence est trop élevée.
- **QoS** : configure ta box ou ton routeur pour prioriser les flux UDP des ports 47998-48010.

### Encodeur

- **NVENC** (NVIDIA) : le plus rapide, latence ~5 ms d'encodage.
- **Quick Sync** (Intel) : excellent aussi, ~5-8 ms.
- **AMF** (AMD) : correct sur les cartes récentes, un peu plus de latence.
- **Software** (CPU) : évite. 30-50 ms de latence, injouable pour les jeux rapides.

### Réglages Moonlight

Dans les paramètres du client Moonlight :

- **Bitrate** : auto ou fixe selon ton réseau. En local, 50 Mbps c'est large.
- **Mode d'affichage** : Plein écran exclusif si possible (réduit la latence d'affichage).
- **Désactiver le V-Sync** dans Moonlight si tu veux minimiser la latence (au prix du tearing).
- **Frame pacing** : laisse activé pour éviter les micro-saccades.

### Serveur

- **Désactive le HDR** si ton écran client ne le supporte pas. Le tonemapping ajoute de la latence.
- **Réduis la résolution** du serveur à la résolution native du client. Pas la peine d'encoder en 4K pour un écran 1080p.
- **Ferme les applications inutiles** sur le serveur. Chrome avec 40 onglets bouffe du GPU.

## Docker sur un NAS ou serveur sans écran

Si tu veux faire tourner Sunshine sur un NAS ou un serveur headless (sans écran physique), il faut simuler un écran virtuel.

### Méthode 1 : Dummy HDMI plug

Branche un faux écran HDMI (5€ sur Amazon) sur le serveur. L'OS détecte un écran et Sunshine peut capturer.

### Méthode 2 : Écran virtuel (Linux)

Sur Linux, installe `dummy-dkms` ou `evdi` pour créer un écran virtuel :

```bash
sudo apt install xserver-xorg-video-dummy
```

Puis configure `/etc/X11/xorg.conf.d/dummy.conf` avec une résolution fixe.

### Méthode 3 : Parsec VDD (Windows)

Sur Windows, installe le driver d'affichage virtuel de Parsec. C'est gratuit et ça marche avec Sunshine.

## Comparaison avec un homelab média

Si tu as déjà un serveur média avec [Jellyfin](/jellyfin-docker-alternative-netflix-gratuite/), Sunshine s'intègre parfaitement dans la même stack. Tu peux même utiliser le même serveur physique : Jellyfin pour les films, Sunshine pour les jeux. Assure-toi juste que ton GPU a assez de mémoire vidéo pour les deux tâches (4 Go VRAM minimum pour être tranquille).

Pour centraliser tous tes services dans un beau tableau de bord, j'ai aussi un guide sur [Homer Dashboard](/homer-dashboard-docker-homelab/). Tu pourras ajouter un lien vers ton Sunshine et voir en un coup d'œil si le conteneur est up.

## Dépannage courant

### Moonlight ne trouve pas le serveur

- Vérifie que Sunshine tourne : `docker ps | grep sunshine`
- Vérifie le firewall : les ports UDP 47998-48010 doivent être ouverts
- Essaie d'ajouter manuellement l'IP du serveur dans Moonlight
- Sur certaines box, le multicast/mDNS est bloqué : l'ajout manuel contourne le problème

### Latence trop élevée

- Vérifie que l'encodeur matériel est bien activé dans Sunshine (pas "Software")
- Baisse le bitrate dans Moonlight
- Passe en 1080p60 plutôt que 4K60
- Utilise Ethernet au lieu du Wi-Fi

### Écran noir dans Moonlight

- Le serveur n'a pas d'écran actif. Utilise un dummy HDMI ou un écran virtuel.
- Le jeu se lance sur un autre écran virtuel. Force la résolution dans les options du jeu.
- Le GPU n'est pas accessible depuis Docker. Vérifie que `/dev/dri` est monté et que les permissions sont correctes.

### Manette non reconnue

- Sunshine transmet les inputs via USB virtuel. Dans la config Sunshine, va dans **Configuration > Input** et active "Gamepad".
- Certaines manettes Xbox nécessitent le pilote xpad. Installe-le sur l'hôte Docker.
- Sur Linux, ajoute ton utilisateur au groupe `input`.

## Conclusion

Sunshine + Moonlight, c'est la solution la plus propre pour streamer tes jeux depuis ton PC vers n'importe quel écran. Pas de dépendance à NVIDIA, pas d'abonnement cloud, pas de latence infernale. Juste toi, ton réseau local, et un conteneur Docker qui tourne discrètement.

Pour quelques euros de dummy HDMI et une heure de config, tu te retrouves avec un cloud gaming maison qui écrase GeForce NOW sur la latence et la qualité d'image.

Maintenant, branche ta manette et va camper les mid.
