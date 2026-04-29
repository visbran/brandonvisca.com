---
title: "Technitium DNS Server : installe ton bloqueur de pubs libre (2026)"
description: Installe Technitium DNS Server en Docker et remplace Pi-hole ou AdGuard Home. Blocage pubs, DNS récursif, DNSSEC — guide complet 2026.
pubDatetime: 2026-04-29 00:00:00+01:00
author: Brandon Visca
tags:
  - reseau
  - auto-hebergement
  - docker
  - dns
  - intermediaire
  - guide
featured: false
draft: false
focusKeyword: technitium dns server
faqs:
  - question: "Technitium DNS Server peut-il remplacer Pi-hole ?"
    answer: "Oui. Technitium DNS Server offre le blocage de publicités via listes DNS, un résolveur récursif natif, DNSSEC, DoH et DoT — dans une seule image Docker. Il fait tout ce que Pi-hole fait, sans dépendance à dnsmasq ni à un résolveur externe."
  - question: "Peut-on utiliser Technitium DNS Server et Technitium Network Suite ensemble ?"
    answer: "Absolument, et c'est même le setup recommandé pour un homelab. Technitium Network Suite gère le DHCP et pousse automatiquement l'IP du DNS Server aux clients via l'option DHCP 6. Les enregistrements DNS sont créés dynamiquement à chaque nouveau bail."
  - question: "Technitium DNS Server fonctionne-t-il sur Raspberry Pi ?"
    answer: "Oui. L'image Docker est disponible pour linux/arm64 et linux/arm/v7, compatible Raspberry Pi 3 et 4. Le serveur tourne correctement avec 256 Mo de RAM allouée — largement suffisant sur un RPi 4."
---
# Technitium DNS Server : installe ton bloqueur de pubs libre (2026)

> 💡 **TL;DR** — Ce qu'il faut retenir :
> - Technitium DNS Server est un serveur DNS récursif open source avec blocage de pubs intégré — alternative directe à Pi-hole et AdGuard Home.
> - L'installation Docker prend 5 minutes : une commande, un port, une interface web sur `:5380`.
> - Il s'intègre nativement avec Technitium Network Suite pour unifier DNS + DHCP sur le même tableau de bord.

## Table des matières

T'as un Pi-hole qui tient par des bouts de ficelle depuis 3 ans, ou un AdGuard Home qui rame sur ton RPi parce qu'il charge 4 millions d'entrées au démarrage ? Technitium DNS Server mérite qu'on s'y attarde sérieusement.

C'est un serveur DNS récursif complet, open source : blocage de pubs intégré, support DoH/DoT, DNSSEC et API REST propre dans une image Docker d'une centaine de mégaoctets. J'ai migré mon homelab dessus il y a quelques semaines, après avoir utilisé Technitium Network Suite pour le DHCP. Voilà le retour honnête.

## Technitium DNS Server vs Pi-hole vs AdGuard Home

Avant d'installer quoi que ce soit, voilà la situation objective. Les trois outils font du blocage DNS, mais leur architecture est très différente.

| Critère | Technitium DNS Server | Pi-hole v6 | AdGuard Home |
|---|---|---|---|
| **DNS récursif natif** | ✅ | ❌ (nécessite Unbound) | ✅ |
| **Blocage de pubs** | ✅ | ✅ | ✅ |
| **DoH / DoT** | ✅ | ❌ (partiel v6) | ✅ |
| **DNSSEC validation** | ✅ | ✅ (via Unbound) | ✅ |
| **Interface web** | Moderne | Correcte | Moderne |
| **ARM (Raspberry Pi)** | ✅ arm64 + armv7 | ✅ | ✅ |
| **RAM minimum** | ~128 Mo | ~200 Mo | ~100 Mo |
| **API REST complète** | ✅ | Limitée | ✅ |
| **Zones DNS locales** | ✅ | ❌ | Limitée |
| **Langage** | C# (.NET) | PHP + Python | Go |

Pi-hole reste excellent si tu veux le maximum de listes et de visibilité communautaire. AdGuard Home est plus léger au démarrage. **Technitium se distingue sur un point clé : il est son propre résolveur récursif**. Pas besoin d'empiler Unbound à côté pour du DNS-over-HTTPS propre.

Autre avantage concret : si t'as déjà [Technitium Network Suite pour ton DHCP et ton NTP](https://brandonvisca.com/technitium-network-suite/), passer au DNS Server devient une évidence. Même stack, même interface web, intégration native entre les deux.

Le projet est disponible sur [GitHub (TechnitiumSoftware/DnsServer)](https://github.com/TechnitiumSoftware/DnsServer) et activement maintenu — v13.x au moment de cet article.

## Installation avec Docker Compose

### Prérequis

- Docker et Docker Compose installés sur ton hôte
- Port 53/UDP libre (voir note ci-dessous)
- Port 5380/TCP libre pour l'interface web

> ⚠️ **Attention** : Sur la plupart des distributions Linux modernes (Ubuntu 20.04+, Debian 12, Fedora…), le port 53 est déjà utilisé par `systemd-resolved`. Vérifie avant de lancer :
>
> ```bash
> sudo ss -tulpn | grep ':53'
> ```
>
> Si `systemd-resolved` occupe le port, désactive-le proprement :
>
> ```bash
> sudo systemctl disable --now systemd-resolved
> sudo rm /etc/resolv.conf
> echo "nameserver 1.1.1.1" | sudo tee /etc/resolv.conf
> ```
>
> Une fois Technitium lancé, tu mets à jour `/etc/resolv.conf` pour pointer vers `127.0.0.1`.

### docker-compose.yml — mode host (recommandé)

```yaml
version: "3.8"

services:
  technitium-dns:
    image: technitium/dns-server:latest
    container_name: technitium-dns
    hostname: dns-server
    network_mode: host
    restart: unless-stopped
    volumes:
      - ./config:/etc/dns
    environment:
      - DNS_SERVER_DOMAIN=dns.homelab.local
      - TZ=Europe/Paris
```

Le mode `host` est requis pour que le conteneur écoute directement sur l'interface réseau de l'hôte — indispensable pour répondre aux requêtes DNS du réseau local sur le port 53/UDP.

Lance le conteneur :

```bash
docker compose up -d
docker logs -f technitium-dns
```

L'interface web est accessible sur **http://IP-DE-TON-HÔTE:5380**. Au premier démarrage, définis un mot de passe administrateur — il n'y en a pas par défaut.

### docker-compose.yml — mode bridge (NAS, Docker Desktop)

Si le mode host n'est pas disponible sur ton environnement (NAS Synology, macOS avec Docker Desktop) :

```yaml
version: "3.8"

services:
  technitium-dns:
    image: technitium/dns-server:latest
    container_name: technitium-dns
    ports:
      - "5380:5380"    # Interface web
      - "53:53/udp"    # DNS UDP
      - "53:53/tcp"    # DNS TCP
      - "853:853/tcp"  # DNS-over-TLS
      - "443:443/tcp"  # DNS-over-HTTPS
    volumes:
      - ./config:/etc/dns
    restart: unless-stopped
    environment:
      - DNS_SERVER_DOMAIN=dns.homelab.local
      - TZ=Europe/Paris
```

> 💡 **Astuce** : La variable `DNS_SERVER_DOMAIN` définit le nom du serveur dans les réponses SOA et les logs. J'utilise `dns.homelab.local` pour identifier clairement le serveur dans mes dashboards de monitoring.

## Blocage de publicités avec les listes DNS

C'est la feature principale pour la plupart des homelabs. Technitium gère les listes au format `hosts`, `adblock` et domaine brut, les mêmes formats que Pi-hole ou AdGuard.

### Ajouter les listes de blocage

Dans l'interface web, va dans **Blocklist** → **Add Blocklist** et ajoute tes sources. Voilà ma sélection pour un usage quotidien :

| Liste | URL | Format |
|---|---|---|
| StevenBlack Hosts | `https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts` | Hosts |
| OISD Basic | `https://basic.oisd.nl/domainswild` | Domain |
| HaGeZi Pro | `https://raw.githubusercontent.com/hagezi/dns-blocklists/main/domains/pro.txt` | Domain |
| uBlock Origin Filters | `https://ublockorigin.github.io/uAssets/filters/filters.txt` | Adblock |

Clique sur **Update All** pour forcer la mise à jour immédiate. Technitium applique les listes en mémoire, sans redémarrage du conteneur.

> ✅ **Bonne pratique** : Commence avec une seule liste (StevenBlack ou OISD Basic) et navigue normalement pendant 24h avant d'en ajouter d'autres. Certaines listes agressives (HaGeZi Pro++) cassent des services légitimes — vérifie d'abord que ton quotidien numérique n'est pas impacté.

### Vérifier que le blocage fonctionne

Depuis une machine cliente pointant sur ton DNS :

```bash
# Doit retourner 0.0.0.0 ou NXDOMAIN
dig ads.google.com @192.168.1.X

# Doit retourner l'IP réelle
dig google.com @192.168.1.X
```

Les requêtes en temps réel sont visibles dans **Logs** → **Query Logs**. Tu vois chaque requête avec le statut (Allowed, Blocked, Cached) et le domaine source.

### Whitelist ponctuelle

Un domaine bloqué à tort ? Dans **Blocklist** → **Allow List**, ajoute le domaine. La whitelist est prioritaire sur toutes les listes de blocage — pas besoin de modifier les listes elles-mêmes.

## DNS récursif, DNSSEC et modes de résolution

C'est là que Technitium se distingue vraiment de Pi-hole. Il gère trois modes de résolution configurables à la volée.

### Mode récursif (recommandé homelab)

Dans **Settings** → **Recursion**, sélectionne **Allow Recursion** et définis la plage autorisée sur ton réseau local (`192.168.0.0/16` par exemple).

En mode récursif, Technitium contacte directement les serveurs racines DNS (`.`, `.com`, `.fr`…) sans intermédiaire. Aucun FAI ni tiers impliqué dans la résolution.

```text
Requête client → Technitium DNS → Serveurs racines → TLD → DNS authoritative → Réponse
```

Active aussi **DNSSEC Validation** dans **Settings** → **DNSSEC** pour valider les signatures cryptographiques des réponses. Ça protège contre le cache poisoning et les attaques man-in-the-middle sur les résolutions DNS.

### Mode Forwarding avec chiffrement (DoH/DoT)

Si tu préfères forwarder les requêtes vers un resolver externe chiffré, va dans **Settings** → **Forwarders** :

| Serveur | Protocole | Adresse |
|---|---|---|
| Cloudflare | DoH | `https://cloudflare-dns.com/dns-query` |
| Quad9 | DoT | `tls://dns.quad9.net` |
| NextDNS | DoH | `https://dns.nextdns.io/TON-ID` |

> ⚠️ **Attention** : Le mode Forwarding est plus simple à mettre en place mais dépend d'un tiers. Pour un homelab privé, le mode récursif direct est plus souverain. Le Forwarding a du sens si tu veux utiliser les filtres premium de NextDNS en complément du blocage local.

### Zones DNS locales

Technitium peut faire autorité sur ta zone interne (`homelab.local`). Dans **Zones** → **Add Zone** :

- **Type** : Primary Zone
- **Name** : `homelab.local`

Tu ajoutes ensuite tes enregistrements A manuellement, ou tu laisses Technitium Network Suite créer les enregistrements dynamiques via le DHCP. Les deux produits se complètent parfaitement ici.

## Intégration avec Technitium Network Suite

Si tu utilises déjà [Technitium Network Suite](https://brandonvisca.com/technitium-network-suite/) pour ton DHCP, l'intégration DNS est native et automatique.

Dans **Network Suite → DHCP → Scopes → Edit ton étendue** :

- **DNS Servers** : l'IP de ton hôte Technitium DNS Server
- **Domain Name** (option DHCP 15) : `homelab.local`

Les clients DHCP reçoivent automatiquement l'IP du DNS Server à chaque bail. Quand une machine obtient un bail, Network Suite crée un enregistrement `A` dans ta zone `homelab.local`. Résolution DNS par nom d'hôte transparente sur tout ton réseau, sans configuration supplémentaire.

Mon setup actuel sur un Mini PC Proxmox :

```text
┌──────────────────────────────────────────────────┐
│  LXC Proxmox (192.168.1.2)                       │
│  ┌─────────────────┐  ┌────────────────────────┐ │
│  │ Technitium NS   │  │ Technitium DNS Server  │ │
│  │ DHCP .100-.200  │  │ DNS récursif + blocage │ │
│  │ NTP stratum 3   │  │ Zone homelab.local     │ │
│  │ Port :6080      │  │ Port :53 + :5380       │ │
│  └─────────────────┘  └────────────────────────┘ │
│  ┌──────────────────────────────────────────────┐ │
│  │  Tous les clients → bail DHCP → DNS .2       │ │
│  └──────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

Le résultat : toute machine qui obtient un bail DHCP est immédiatement résolvable par nom sur le réseau (`proxmox-node.homelab.local`, `nas.homelab.local`…). Plus besoin de gérer `/etc/hosts` ou un DNS split-horizon complexe.

Si tu veux aller plus loin sur la gestion des enregistrements DNS et le nettoyage des entrées obsolètes, le guide sur le [DNS Scavenging sous Windows Server](https://brandonvisca.com/dns-scavenging-windows-server-guide-complet/) couvre le même principe côté Active Directory.

## Conclusion

Technitium DNS Server est une des meilleures options pour auto-héberger son DNS en 2026. Il est propre, activement maintenu, et il fait du DNS récursif natif sans jongler avec Unbound. Si t'es déjà sur la stack Technitium pour le DHCP, c'est un no-brainer — t'es à 5 minutes d'un DNS complet unifié.

La migration depuis Pi-hole est quasi-transparente : importe tes listes, désactive l'ancien serveur, pointe ton DHCP sur la nouvelle IP. Pas de mauvaise surprise.

Et si tu veux synchroniser tes blocages DNS sur plusieurs instances (un DNS par VLAN, par exemple), jette un œil à [Nebula-Sync pour Pi-hole v6](https://brandonvisca.com/nebula-sync-pihole-v6-installation-docker-guide/) — le concept de synchronisation de listes est transposable.

## Pour aller plus loin

- [Technitium Network Suite : serveur DHCP et NTP pour ton homelab](/technitium-network-suite/)
- [Nebula-Sync : synchronise tes Pi-hole v6 automatiquement](/nebula-sync-pihole-v6-installation-docker-guide/)
- [DNS Scavenging Windows Server : le guide complet](/dns-scavenging-windows-server-guide-complet/)
