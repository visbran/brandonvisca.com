---
title: "Technitium Network Suite : serveur DHCP et NTP open source pour ton homelab"
description: "Installe un serveur DHCP et NTP auto-hébergé avec Technitium Network Suite. Guide complet : Docker, configuration DHCP, reservations, synchronisation NTP."
pubDatetime: 2026-04-28 00:00:00+01:00
author: Brandon Visca
tags:
  - homelab
  - reseau
  - auto-hebergement
  - technitium
  - intermediaire
  - guide
featured: false
draft: false
focusKeyword: technitium network suite
faqs:
  - question: "Technitium Network Suite peut-il remplacer le DHCP de pfSense ?"
    answer: "Oui pour un homelab simple. Technitium gère réservations MAC, plages DHCP et options avancées (NTP, suffixe DNS). Pour des VLANs multiples avec règles firewall, pfSense reste plus adapté."
  - question: "Peut-on utiliser Technitium Network Suite en mode bridge Docker ?"
    answer: "Oui, mais en mode bridge le serveur DHCP ne sert que les clients du bridge Docker. Pour couvrir tout le réseau local, utilise le mode host ou un LXC sur Proxmox."
  - question: "Technitium Network Suite est-il compatible Raspberry Pi ?"
    answer: "Oui. L'image Docker supporte linux/arm64 et linux/arm/v7. Le serveur tourne sans problème avec 256 Mo de RAM — compatible Raspberry Pi 3 et 4."
---
## Introduction

Gérer son réseau domestique ou son homelab, c'est aussi gérer les briques fondamentales souvent négligées : le DHCP qui distribue les IPs et le NTP qui synchronise les horloges. Jusqu'à récemment, les options open source étaient limitées : ISC DHCP sur Linux, pfSense pour les réseaux complets, ou pire — le DHCP du routeur fourni par votre FAI avec ses options fermées.

Technitium Network Suite change la donne. Développé par Shripad D. et maintenu activement, c'est une application .NET Core qui tourne sur Windows, Linux, macOS et même en conteneur Docker. Elle combine serveur DHCP, serveur NTP et DNS dynamique dans une interface web moderne — le tout gratuitement et sans licence.

Dans ce guide, je vous montre comment installer Technitium Network Suite en Docker, le configurer pour un réseau domestique avec des reservations DHCP, et synchroniser vos machines avec un serveur NTP local. À la fin, un comparatif avec les alternatives vous aidera à décider si c'est la bonne solution pour votre setup.

---

## Qu'est-ce que Technitium Network Suite ?

Technitium Network Suite est une suite réseau complète écrite en C# (.NET Core). Elle inclut trois services principaux :

| Service | Fonction |
|---|---|
| **DHCP Server** | Distribue les adresses IP aux clients du réseau |
| **NTP Server** | Synchronise l'heure des machines du réseau |
| **DNS Client** | Mise à jour dynamique d'enregistrements DNS |

L'application se distingue par plusieurs points :

- **Interface web intégrée** : plus besoin de configurer via fichiers JSON ou lignes de commande. Tout se fait depuis un dashboard graphique accessible depuis n'importe quel navigateur.
- **Multiplateforme** : Windows, Linux, macOS, Docker.
- **Léger** : l'image Docker ne pèse qu'environ 150 Mo.
- **Activement maintenu** : sorties régulières sur GitHub avec une communauté réactive.
- **Zéro dépendance tierce** : pas de base de données requise (stockage en fichiers JSON), pas de serveur web supplémentaire.

Pour un homelab ou un réseau domestique, c'est une alternative crédible à pfSense pour ceux qui veulent juste un serveur DHCP/NTP sans la complexité d'un firewall UTM complet.

---

## Installation avec Docker Compose

### Prérequis

- Docker et Docker Compose installés sur votre hôte
- Un réseau Docker bridge (ou host) adapté à votre topologie
- Accès root ou utilisateur dans le groupe docker

### Configuration réseau

Avant de lancer le conteneur, choisissez le mode réseau. Pour un homelab classique sur un serveur Proxmox/LXC, le mode **host** est recommandé car il permet au serveur DHCP d'écouter directement sur le réseau local.

```yaml
version: "3.8"

services:
  technitium:
    image: technitium/network-suite:latest
    container_name: technitium-dhcp-ntp
    hostname: technitium
    network_mode: host
    restart: unless-stopped
    volumes:
      - ./config:/etc/opt/technitium
      - ./logs:/var/log/technitium
    environment:
      - TZ=Europe/Paris
```

Lancez le conteneur :

```bash
docker compose up -d
```

Vérifiez que le conteneur est actif :

```bash
docker logs -f technitium-dhcp-ntp
```

L'interface web sera accessible sur **http://IP-DE-VOTRE-HOST:6080**. Le serveur DHCP écoute sur le port 67/UDP et le serveur NTP sur le port 123/UDP.

> **Note** : Si vous êtes sur un NAS Synology ou un système avec un kernel qui ne supporte pas le mode host (comme Docker Desktop sur macOS), utilisez le mode bridge et configurez les ports exposés :

```yaml
services:
  technitium:
    image: technitium/network-suite:latest
    container_name: technitium-dhcp-ntp
    ports:
      - "6080:6080"   # Interface web
      - "67:67/udp"   # DHCP Server
      - "123:123/udp" # NTP Server
    volumes:
      - ./config:/etc/opt/technitium
      - ./logs:/var/log/technitium
    restart: unless-stopped
```

Dans ce mode bridge, le serveur DHCP ne pourra servir que les clients branchés sur le bridge Docker — ce qui limite son intérêt à un sous-réseau dédié.

---

## Configuration du serveur DHCP

### Accès à l'interface

Ouvrez `http://IP-DE-VOTRE-HOST:6080` dans votre navigateur. Au premier démarrage, aucun mot de passe n'est défini. Laissez les champs vides et cliquez sur **Login** pour accéder au dashboard.

Naviguez vers **DHCP** dans le menu latéral.

### Créer une étendue DHCP

Une étendue définit la plage d'adresses IP que le serveur peut distribuer.

1. Cliquez sur **Scopes** → **Add Scope**
2. Remplissez les champs :

| Champ | Valeur exemple | Description |
|---|---|---|
| **Name** | `Homelab LAN` | Nom de l'étendue |
| **Description** | `Réseau local homelab 192.168.1.0/24` | Description libre |
| **Network** | `192.168.1.0` | Adresse réseau |
| **Subnet Mask** | `255.255.255.0` | Masque CIDR /24 |
| **Start Address** | `192.168.1.100` | Début de la plage DHCP |
| **End Address** | `192.168.1.200` | Fin de la plage DHCP |
| **Gateway** | `192.168.1.1` | Routeur/passerelle par défaut |
| **DNS Servers** | `192.168.1.1, 1.1.1.1` | Serveurs DNS |

3. Cliquez sur **Save**.

Votre étendue est maintenant active. Les clients qui envoient une requête DHCP sur le réseau recevront une adresse entre 192.168.1.100 et 192.168.1.200.

### Ajouter des reservations DHCP

Les reservations assignent une adresse IP fixe à une adresse MAC spécifique. C'est indispensable pour les serveurs, les machines avec des règles firewall fixes, ou tout équipement qui doit toujours obtenir la même IP.

1. Allez dans **DHCP** → **Leases** → **Add Reservation**
2. Remplissez :

| Champ | Valeur exemple |
|---|---|
| **MAC Address** | `B8:27:EB:12:34:56` |
| **Host Name** | `proxmox-node1` |
| **IP Address** | `192.168.1.10` |
| **Description** | `Node Proxmox principal` |

3. **Save**.

La reservation sera toujours servie depuis cette IP, que le client soit allumé ou non. Pour un serveur Proxmox qui héberge vos VMs, c'est particulièrement utile pour toujourspointer vers le bon host dans vos configs Ansible ou dans `/etc/hosts`.

### Options DHCP avancées

Technitium permet de configurer des options DHCP standard (RFC 2132). Quelques options utiles pour un homelab :

| Option | Code | Valeur | Usage |
|---|---|---|---|
| **NTP Servers** | 42 | `192.168.1.1` | Clients utilisant ce serveur NTP |
| **Domain Name** | 15 | `homelab.local` | Suffixe DNS pour les clients |
| **Lease Time** | 51 | `86400` (1 jour) | Durée du bail en secondes |
| **Refresh** | 58 | `43200` (12h) | Quand le client doit redemander son bail |

Pour ajouter une option, allez dans **Scopes** → Modifier votre étendue → **DHCP Options** → **Add Option**.

---

## Serveur NTP synchronisé

### Principe

Le protocole NTP (Network Time Protocol) synchronise l'horloge des machines sur votre réseau avec une source de temps fiable. Dans un homelab, c'est souvent négligé — et pourtant, les horloges désynchronisées causent des problèmes subtils : certificats TLS invalides, logs incohérents entre services, Kerberos qui échoue, etc.

Technitium inclut un serveur NTP qui peut :

- Synchroniser son horloge avec des sources externes (pool NTP public)
- Servir de source de temps aux machines locales

### Configuration

1. Allez dans **NTP** dans le menu
2. Activez le serveur NTP s'il ne l'est pas
3. Configurez les **Peers** (sources de temps externes) :

| Peer | Type | Adresse |
|---|---|---|
| 0.pool.ntp.org | Pool | `0.fr.pool.ntp.org` |
| 1.pool.ntp.org | Pool | `1.fr.pool.ntp.org` |
| 2.pool.ntp.org | Pool | `2.fr.pool.ntp.org` |

4. Cliquez sur **Save** et patientez quelques minutes pour la première synchronisation.

Vérifiez le statut dans le dashboard NTP — vous verrez l'offset entre l'horloge locale et les sources synchronisées.

### Configurer les clients Linux

Sur Ubuntu/Debian, le client NTP par défaut est `systemd-timesyncd`. Modifiez `/etc/systemd/timesyncd.conf` :

```ini
[Time]
NTP=192.168.1.1
FallbackNTP=0.fr.pool.ntp.org 1.fr.pool.ntp.org
```

Puis :

```bash
sudo timedatectl set-ntp true
timedatectl status
```

### Configurer les clients Windows

Sur Windows, ouvrez PowerShell en administrateur :

```powershell
w32tm /config /syncfromflags:manual /manualpeerlist:"192.168.1.1,0.fr.pool.ntp.org,1.fr.pool.ntp.org"
w32tm /config /update
w32tm /resync
```

Windows utilisera maintenant votre serveur NTP local en priorité.

---

## Interface web et monitoring

### Dashboard

Le dashboard Technitium donne une vue d'ensemble immédiate :

- **DHCP** : nombre de baux actifs, historique des dernières requêtes
- **NTP** : statut de la synchronisation, stratum actuel, peers connectés
- **System** : CPU, mémoire, uptime du conteneur

### Logs et debugging

En cas de problème, les logs sont disponibles directement dans l'interface (**Logs** dans le menu). Pour un debugging plus fin, redirigez les logs du conteneur vers un fichier :

```yaml
volumes:
  - ./logs:/var/log/technitium
```

```bash
tail -f logs/dhcp.log
tail -f logs/ntp.log
```

---

## Cas d'usage concret : homelab Proxmox

Voici mon setup concret. Mon homelab tourne sur un Mini PC avec Proxmox. J'ai configuré Technitium Network Suite sur un conteneur LXD (donc en mode host) pour qu'il serve mon réseau 192.168.1.0/24.

```
┌─────────────────────────────────────────────┐
│  Mini PC Proxmox                            │
│  ┌──────────────┐  ┌──────────────────────┐ │
│  │ LXD: Technitium │  │  VM: Nextcloud, Vaultwarden │ │
│  │  DHCP : .100-.200│  │  VM: Jellyfin       │ │
│  │  NTP : stratum 3│  │  VM: Pi-hole        │ │
│  └──────────────┘  └──────────────────────┘ │
│  ┌──────────────────────────────────────────┐│
│  │ Bridge vmbr0 (mode host) — IP .1        ││
│  └──────────────────────────────────────────┘│
└─────────────────────────────────────────────┘
```

Réservations actives :

| Machine | MAC | IP reservée |
|---|---|---|
| Proxmox Node | `B8:27:EB:12:34:56` | `.10` |
| NAS Synology | `00:11:32:AB:CD:EF` | `.11` |
| Switch manageé | `00:1A:2B:3C:4D:5E` | `.12` |
| Borne WiFi AP | `F0:9F:C2:A1:B2:C3` | `.13` |

Le serveur NTP local同步 mes 4 machines Linux et 2 VMs Windows. Le stratum 3 suffit pour un homelab — mes logs sont maintenant alignés et je peux corréler un événement sur plusieurs systèmes sans dédouble.

---

## Comparatif : Technitium vs Alternatives

| Critère | Technitium Network Suite | pfSense/OPNsense | ISC DHCP | Windows Server DHCP |
|---|---|---|---|---|
| **Coût** | Gratuit, open source | Gratuit (CE) | Gratuit | Licence Windows Server |
| **Interface** | Web moderne | Web complète | CLI / config file | MMC graphique |
| **Setup DHCP** | 10 min Docker | 30 min (full install) | 1h+ config | 20 min |
| **NTP intégré** | ✅ | ✅ | ❌ | ✅ |
| **DNS dynamique** | ✅ | ✅ (unbound) | ❌ | ❌ |
| **Reservations MAC** | ✅ | ✅ | ✅ | ✅ |
| **Multi-étendue** | ✅ | ✅ | ✅ | ✅ |
| **API REST** | ✅ | ✅ | ❌ | ✅ |
| **Ressources** | ~150 Mo / <512 Mo RAM | 1 Go+ / 2 Go+ RAM | ~50 Mo | Dépend de Windows |
| **Idéal pour** | Homelab, VM unique | Firewall complet | Serveur Linux dédié | Environnement Windows |

**Mon avis** : Pour un homelab sur un seul serveur (Proxmox, un NUC, un NAS), Technitium est le meilleur compromis entre simplicité et fonctionnalités. Si vous avez déjà un routeur pfSense, autant utiliser son DHCP intégré. Mais si vous voulez une solution légère, dédiée, et graphiquement accessible sans overhead, Technitium gagne.

---

## Conclusion et next steps

Technitium Network Suite comble un vide dans l'écosystème self-hosted : celui du DHCP et NTP sans enterprise. En 15 minutes chrono, vous avez un serveur DHCP avec reservations et un serveur NTP synchronisé — le tout dans un conteneur Docker qui consomme moins de ressources qu'un onglet de navigateur.

Si vous avez suivi ce guide, vous avez maintenant un serveur DHCP fiable pour votre homelab. Pour aller plus loin, voici deux articles connexes qui traitent de l'infrastructure réseau autour de Technitium :

- [Nebula-Sync : synchronise tes Pi-hole v6 automatiquement](https://brandonvisca.com/nebula-sync-pihole-v6-installation-docker-guide/) — après avoir maîtrisé vos IPs avec Technitium, synchronisez vos blocage DNS sur plusieurs Pi-hole
- [Uptime Kuma 2.0 : le monitoring auto-hébergé](https://brandonvisca.com/uptime-kuma-2-0-monitoring-auto-heberge/) — surveillez la disponibilité de vos services DHCP et NTP depuis un dashboard unique
- [Sécurité de votre serveur Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/) — durcissez votre hôte Docker après installation de nouveaux services réseau

MDEOF