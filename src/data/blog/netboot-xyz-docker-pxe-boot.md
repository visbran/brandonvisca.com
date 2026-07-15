---
title: "Netboot Docker avec Netboot.xyz : boot PXE pour installer n'importe quel OS"
description: "Netboot docker avec Netboot.xyz : boot PXE pour installer Linux, Windows ou BSD via le réseau. Guide Docker Compose complet et testé."
pubDatetime: "2026-07-06T08:00:00.000Z"
modDatetime: "2026-07-06T08:00:00.000Z"
author: Brandon
tags:
  - debutant
  - linux-sysadmin
  - docker
  - netboot
  - pxe
featured: false
draft: false
focusKeyword: netboot docker
ogImage: ""
---

> 💡 **TL;DR**
>
> - **Netboot.xyz** te permet de booter n'importe quel OS directement depuis le réseau, sans clé USB ni ISO à graver.
> - Tu lances un simple conteneur Docker avec un serveur TFTP/HTTP intégré.
> - Ça marche pour Ubuntu, Debian, Fedora, Arch, Windows, FreeBSD et des dizaines d'autres.
> - Idéal pour provisionner des serveurs, des VMs ou des labos rapidement.

## Table des matières

## Qu'est-ce que Netboot.xyz ?

[Netboot.xyz](https://netboot.xyz) est un projet open-source qui fournit un environnement de boot réseau (PXE/iPXE) tout prêt. Au lieu de graver une ISO sur une clé USB, tu configures tes machines pour démarrer sur le réseau. Elles contactent le serveur Netboot.xyz, affichent un menu web et te proposent d'installer l'OS de ton choix.

Les use cases principaux :

- **Provisionner un parc de serveurs** sans intervention physique.
- **Tester des distros Linux** sans télécharger d'ISO.
- **Réinstaller un serveur à distance** quand tu n'as pas de KVM/IPMI.
- **Labo homelab** : tu bootes tes VMs Proxmox directement en PXE. Si tu cherches à optimiser ton infra Proxmox, jette un œil au [guide des conteneurs LXC sous Proxmox](/proxmox-lxc-containers-guide/).

Le tout tourne dans un conteneur Docker légér, ce qui le rend ultra simple à déployer.

## Prérequis

Avant de commencer, assure-toi d'avoir :

- Une machine avec **Docker et Docker Compose** installés. Si ce n'est pas encore le cas, suis le [guide Docker débutant](/docker-debutant-services-auto-heberger/) pour mettre en place ta stack rapidement.
- Un **accès réseau** entre le serveur Docker et les machines clientes.
- Un serveur **DHCP** qui peut pointer vers ton serveur TFTP (c'est souvent ta box, pfSense, OPNsense ou un serveur DHCP interne).
- Les ports 80 (HTTP), 69 (TFTP) et 3000 (interface web) disponibles sur le serveur.

## Installation Docker

Crée un dossier pour Netboot.xyz et un fichier `docker-compose.yml` :

```bash
mkdir -p ~/netbootxyz && cd ~/netbootxyz
```

```yaml
version: "3.8"

services:
  netbootxyz:
    image: ghcr.io/netbootxyz/netbootxyz:latest
    container_name: netbootxyz
    environment:
      - TZ=Europe/Paris
      - MENU_VERSION=1.9.9
    volumes:
      - ./config:/config
      - ./assets:/assets
    ports:
      - "80:80"
      - "69:69/udp"
      - "3000:3000"
    restart: unless-stopped
    cap_add:
      - NET_ADMIN
    networks:
      - netboot

networks:
  netboot:
    driver: bridge
```

> ⚠️ **Pourquoi `NET_ADMIN` ?** Le conteneur a besoin de manipuler les interfaces réseau pour répondre aux requêtes PXE broadcast.

Lance le conteneur :

```bash
docker compose up -d
```

Vérifie qu'il est bien up :

```bash
docker compose ps
```

## Configuration

### Volumes persistants

Le conteneur expose deux volumes importants :

- `/config` : contient les menus personnalisés, les fichiers de configuration iPXE et les logs.
- `/assets` : stocke les images ISO et kernels que tu choisis de mettre en cache locale.

Tu peux éditer les menus directement dans `./config/menus/` si tu veux ajouter tes propres entrées ou masquer celles qui ne t'intéressent pas.

### Variables d'environnement clés

| Variable | Description | Défaut |
|---|---|---|
| `TZ` | Fuseau horaire | `UTC` |
| `MENU_VERSION` | Version du menu netboot.xyz | `latest` |
| `NGINX_PORT` | Port HTTP interne | `80` |
| `WEB_APP_PORT` | Port de l'interface web | `3000` |

Tu peux surcharger l'URL de base si tu héberges toi-même les assets :

```yaml
environment:
  - NGINX_HOST=http://ton-ip-local
```

## Comment ça marche : le boot PXE / iPXE expliqué simplement

Le **PXE** (Preboot eXecution Environment) est un standard qui permet à une machine de démarrer depuis le réseau au lieu d'un disque local. Voici le déroulement simplifié :

1. Ta machine client envoie une requête DHCP au démarrage.
2. Le serveur DHCP répond avec une **IP** et l'adresse du **serveur TFTP** où trouver le bootloader.
3. La machine télécharge le bootloader **iPXE** via TFTP.
4. iPXE charge un menu depuis le serveur HTTP de Netboot.xyz.
5. Tu choisis l'OS à installer. iPXE télécharge le kernel et l'initrd nécessaires.
6. L'installation commence, comme si tu avais booté depuis une ISO locale.

C'est transparent, rapide et ça évite de jongler avec des clés USB.

## Installer un OS depuis le menu web

### Étape 1 : configurer le DHCP

Ta machine cliente doit savoir où chercher le serveur TFTP. Tu as deux options :

**Option A, DHCP existant (box/pfSense/OPNsense)** :
Dans les options DHCP, renseigne :
- **Next Server** (IP du serveur Netboot.xyz)
- **Boot Filename** : `netboot.xyz.kpxe` (BIOS) ou `netboot.xyz.efi` (UEFI)

**Option B, Docker avec DHCP intégré** :
Si tu n'as pas accès au DHCP de ton routeur, tu peux ajouter un conteneur `dhcpd` dans le même `docker-compose.yml` sur le même réseau bridge. C'est plus avancé mais totalement faisable.

### Étape 2 : booter la machine cliente

Sur ta machine cliente :

1. Entre dans le BIOS/UEFI.
2. Active le **Boot from Network** (PXE Boot / Network Boot).
3. Mets le **Network Boot** en première priorité.
4. Redémarre.

Tu devrais voir apparaître le menu Netboot.xyz avec une liste d'OS.

### Étape 3 : choisir et installer

Navigue dans le menu avec les flèches du clavier. Tu trouveras des catégories comme :

- **Linux**
  - Ubuntu
  - Debian
  - Fedora
  - Arch Linux
  - Alpine
- **BSD**
  - FreeBSD
  - OpenBSD
- **Windows**
  - Windows PE / Installers (via chainload)
- **Utilities**
  - GParted
  - Clonezilla
  - MemTest86

Sélectionne ton OS, le kernel se télécharge et l'installation démarre. Pour certaines distros, tu peux même choisir entre une install graphique ou netinstall.

## Tips et astuces

### Personnaliser les menus

Les fichiers de menu sont en format iPXE (fichiers `.ipxe`) dans `/config/menus/`. Tu peux ajouter tes propres entrées pour pointer vers des ISO internes ou des serveurs PXE existants.

Exemple d'entrée personnalisée pour une ISO locale :

```ipxe
:custom_iso
kernel ${live_endpoint}/assets/custom-debian.iso
initrd ${live_endpoint}/assets/custom-initrd.gz
boot
```

### Cache local des assets

Par défaut, Netboot.xyz télécharge les kernels à la volée depuis Internet. Si tu as une connexion lente ou si tu veux accélérer les boots, précharge les assets courants dans `./assets/`.

### Boot PXE et VLAN

Si ton réseau client est sur un VLAN différent, assure-toi que le serveur Docker a une interface tagged sur ce VLAN, ou que ton routeur fait du **DHCP relay** (IP Helper) vers le serveur Netboot.xyz.

### Vérifier que TFTP répond bien

Depuis une autre machine du réseau, teste le serveur TFTP :

```bash
tftp ton-serveur-netboot -c get netboot.xyz.kpxe
```

Si le fichier se télécharge, le service TFTP fonctionne.

### Sécuriser l'accès

L'interface web de Netboot.xyz (port 3000) n'a pas d'authentification par défaut. Si elle est exposée sur un réseau partagé, borne l'accès avec un reverse proxy comme [Caddy](/caddy-docker-reverse-proxy-guide/) ou un firewall interne.

### Troubleshooting rapide

| Symptôme | Cause probable | Solution |
|---|---|---|
| Pas de menu PXE | DHCP mal configuré | Vérifie Next Server et Boot Filename |
| TFTP timeout | Port 69 bloqué | Ouvre UDP/69 sur le firewall |
| Menu web inaccessible | Port 3000 fermé | Vérifie `docker compose ps` |
| Kernel introuvable | URL distante indisponible | Précharge l'asset en local |

## Conclusion

Netboot.xyz sous Docker transforme n'importe quel serveur en point de boot universel. Plus besoin de clés USB, plus besoin de graver des ISO. Tu configures une fois, et tu installes ce que tu veux, quand tu veux, directement depuis le réseau. C'est l'outil parfait pour un homelab efficace et un provisionnement sans friction. Si tu veux aller plus loin avec Proxmox, j'ai aussi publié un guide sur les [Proxmox VE Helper Scripts](/proxmox-ve-helper-scripts-community/) qui te permettent d'installer des conteneurs LXC préconfigurés en un clic.
