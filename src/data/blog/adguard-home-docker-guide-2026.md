---
title: AdGuard Home remplace Pi-hole ? Guide Docker complet 2026
description: Installe AdGuard Home en Docker pour bloquer pubs et trackers sur tout ton réseau. Guide complet 2026, configuration DNS et comparatif Pi-hole.
pubDatetime: 2026-05-08 10:00:00+02:00
author: Brandon Visca
tags:
  - debutant
  - auto-hebergement
  - docker
  - dns
  - securite
  - homelab
featured: false
draft: false
focusKeyword: adguard home docker
faqs:
  - question: "Quelle est la différence entre AdGuard Home et Pi-hole ?"
    answer: "AdGuard Home est plus léger, intègre nativement DNS-over-HTTPS/TLS/QUIC et son interface est plus moderne. Pi-hole reste plus mature sur les listes communautaires et le filtering regex avancé."
  - question: "Puis-je utiliser AdGuard Home comme serveur DHCP ?"
    answer: "Oui, c'est optionnel. AdGuard Home peut remplacer le DHCP de ta box, ce qui facilite l'attribution DNS automatique à tous les appareils. En Docker, il faut utiliser network_mode: host pour le DHCP."
  - question: "Quels ports utiliser pour AdGuard Home en Docker ?"
    answer: "Tu dois exposer au minimum 53/tcp et 53/udp pour le DNS, 3000/tcp pour le setup initial, et 80/tcp (ou 443/tcp pour HTTPS). Le port 67/udp est nécessaire uniquement si tu actives le DHCP."
---
## TL;DR

- AdGuard Home bloque pubs, trackers et sites malveillants au niveau DNS pour **tout ton réseau**.
- Container Docker officiel : `adguard/adguardhome:latest` (moins de 30 Mo, mis à jour avril 2026).
- Il est **plus léger que Pi-hole** et intègre DoH/DoT/DoQ nativement sans bidouiller Unbound.
- Déploiement en 5 min avec un `docker-compose.yml` et deux ports (53 + 3000).
- Change le DNS de ta box pour l'IP de ton serveur, et c'est réglé.

---

## Pourquoi encore un guide DNS ?

T'as déjà vu Nextcloud, Jellyfin, Vaultwarden. Tu t'auto-héberges à fond. Mais tu laisses encore ta Freebox ou ta Livebox pointer vers les DNS d'Orange qui loggent tes requêtes et laissent passer la pub sur chaque appareil de la maison.

**C'est le trou dans la raquette.** Un DNS filtrant, c'est la première brique d'un réseau propre. Pas besoin d'installer un adblocker sur chaque téléphone, tablette et TV. Tu bloques à la source.

AdGuard Home est sorti en 2019, aujourd'hui c'est une alternative crédible — voire supérieure selon les usages — à Pi-hole. Et contrairement à ce que certains croient, il n'est pas "juste un bloqueur russe". Le code est open source, audité, et hébergé sur GitHub sous licence GPL v3.

---

## Qu'est-ce qu'AdGuard Home exactement ?

AdGuard Home est un **serveur DNS récursif local** avec filtrage intégré. Il résout les noms de domaine comme n'importe quel DNS (Google, Cloudflare, ton FAI), mais avant de répondre il consulte des listes de blocage.

Résultat : quand ta TV demande `ads.yahoo.com`, AdGuard répond `0.0.0.0`. La requête de pub meurt dans l'oeuf. Pas de bande passante gaspillée, pas de pixel de tracking chargé.

Au-delà du blocage, il offre :

- **DNS-over-HTTPS (DoH)**, **DNS-over-TLS (DoT)**, **DNS-over-QUIC (DoQ)** natifs.
- Un **tableau de bord web** avec stats temps réel, requêtes bloquées, top clients.
- Un mode **DHCP optionnel** pour gérer toi-même les IPs locales et forcer l'usage de ton DNS.
- Des listes de filtrage compatibles format `hosts`, `adblock` et domaine brut (les mêmes que Pi-hole).

---

## AdGuard Home vs Pi-hole : le comparatif factuel

| Critère | AdGuard Home | Pi-hole v6 |
|---|---|---|
| Taille image Docker | ~27 Mo | ~90 Mo |
| RAM consommée | ~30-50 Mo | ~80-150 Mo |
| Interface web | Moderne, reactive | Fonctionnelle, moins sexy |
| DoH / DoT / DoQ | Natif | Besoin d'Unbound ou cloudflared |
| DHCP intégré | Oui (optionnel) | Oui |
| Filtering regex | Basique | Avancé (Pi-hole FTL) |
| Mise à jour listes | En arrière-plan fluide | Peut ramer avec 5M+ d'entrées |
| Client identification | Par IP / MAC | Par IP / MAC / groupe |

**Mon avis** : si tu veux du DoH natif sans empiler trois conteneurs, AdGuard Home gagne. Si tu veux du filtering regex très fin et une communauté reddit immense, Pi-hole reste le roi. Pour un homelab débutant/intermédiaire, AdGuard est le meilleur rapport simplicité/puissance en 2026.

---

## Prérequis

- Un serveur avec Docker et Docker Compose installés (peu importe l'OS).
- Un accès réseau stable, IP fixe recommandée pour le serveur.
- Les ports 53/tcp et 53/udp **disponibles** sur l'hôte (conflit possible avec systemd-resolved sur Ubuntu — on verra la résolution plus bas).
- Docker Hub accessible pour pull `adguard/adguardhome:latest`.

> **Astuce** : AdGuard Home tourne parfaitement sur un Raspberry Pi 4, un LXC Proxmox ou une VM cheap chez Hetzner. J'ai testé sur un LXC Debian 12 avec 512 Mo de RAM : il ne gère même pas d'utiliser 10 % des ressources.

---

## Installation Docker

### Structure des dossiers

Crée l'arborescence :

```bash
mkdir -p ~/docker/adguardhome/{work,conf}
cd ~/docker/adguardhome
```

- `work/` → données de travail et stats.
- `conf/` → fichier de configuration `AdGuardHome.yaml`.

### Le docker-compose.yml

```yaml
services:
  adguardhome:
    image: adguard/adguardhome:latest
    container_name: adguardhome
    restart: unless-stopped
    ports:
      - "53:53/tcp"
      - "53:53/udp"
      - "80:80/tcp"
      - "443:443/tcp"
      - "3000:3000/tcp"
      # Décommente les lignes ci-dessous UNIQUEMENT si tu actives le DHCP
      # - "67:67/udp"
      # - "68:68/udp"
    volumes:
      - ./work:/opt/adguardhome/work
      - ./conf:/opt/adguardhome/conf
    cap_add:
      - NET_BIND_SERVICE
    # Pour le DHCP, décommente aussi :
    # network_mode: host
```

Pourquoi `NET_BIND_SERVICE` ? Pour que le processus à l'intérieur du conteneur puisse binder le port 53 sans tourner en root.

> **Attention sur Ubuntu/Debian** : `systemd-resolved` écoute déjà sur le port 53 local. Avant de lancer le conteneur, corrige ça :
>
> ```bash
> sudo systemctl stop systemd-resolved
> sudo systemctl disable systemd-resolved
> # Modifie /etc/resolv.conf pour pointer vers 1.1.1.1 ou 127.0.0.1
> ```

### Lancement

```bash
docker compose up -d
```

Vérifie que le conteneur tourne :

```bash
docker ps --filter name=adguardhome
```

---

## Configuration initiale

Ouvre ton navigateur sur :

```
http://<IP_DU_SERVEUR>:3000
```

Un wizard de setup démarre :

1. **Admin Web Interface** : choisis le port 80 (ou 8080 si 80 est pris) et définis un login/mot de passe fort.
2. **DNS Server** : laisse le port 53 par défaut. Tu peux ajouter des upstreams DNS sécurisés dès maintenant. Voici ma recommandation :
   - `https://dns.cloudflare.com/dns-query` (DoH Cloudflare)
   - `https://dns.quad9.net/dns-query` (DoH Quad9, + malware blocking)
3. **Filters** : AdGuard propose par défaut la liste "AdGuard DNS filter". C'est un excellent départ. Tu peux en ajouter d'autres comme :
   - StevenBlack hosts
   - OISD Blocklist Basic
   - Phishing Army
4. **Fin du wizard** : il génère le fichier `AdGuardHome.yaml` dans ton volume `./conf`.

> **Sécurité** : change immédiatement le port d'admin en HTTPS (DoH) ou mets-le derrière un reverse proxy type Traefik si tu exposes en externe. Ne laisse pas le dashboard en HTTP clair sur Internet.

---

## Intégration réseau

### Méthode 1 : changer le DNS du routeur (recommandé)

Connecte-toi à l'interface d'admin de ta box (Freebox, Livebox, etc.) et change les DNS primaires et secondaires pour l'IP locale de ton serveur AdGuard Home.

Avantage : zéro config sur chaque appareil. Inconvénient : si ton serveur tombe, plus Internet. Prévois un DNS secondaire de secours (ex: `1.1.1.1`) ou un keepalived/VRRP si tu veux du HA.

### Méthode 2 : DHCP intégré d'AdGuard (optionnel)

Si ta box ne laisse pas changer les DNS, tu peux désactiver le DHCP de la box et activer celui d'AdGuard Home. C'est lourd mais ça marche à tous les coups.

Dans l'interface AdGuard : **Settings → DHCP settings**.

Définis la plage d'IPs, la passerelle (IP de la box), et le DNS (IP du serveur AdGuard lui-même). N'oublie pas de désactiver le DHCP de la box avant.

> **Docker oblige** : pour que le DHCP fonctionne, le conteneur DOIT être en `network_mode: host`. Sinon les requêtes broadcast DHCP ne sortiront pas correctement.

---

## Dashboard et stats

L'interface d'AdGuard Home est vraiment soignée. En un coup d'oeil tu vois :

- Nombre de requêtes DNS traitées (on parle vite de milliers par heure sur un réseau domestique avec objets connectés).
- Taux de blocage (généralement entre 15 % et 40 % selon tes listes).
- Top clients : c'est souvent la TV Samsung ou l'enceinte Alexa qui mène le classement des requètes suspicieuses.
- Requêtes bloquées en temps réel (utile pour déboguer un site qui charge mal).

Tu peux créer des **profils clients** (par IP ou MAC) pour appliquer des listes de blocage différentes selon les appareils. Pratique pour alléger le filtering sur le PC de travail tout en bloquant tout sur la tablette des gamins.

---

## Mise à jour

AdGuard Home publie régulièrement des mises à jour. Procédure simple :

```bash
cd ~/docker/adguardhome
docker compose pull
docker compose up -d
```

Le fichier de config persiste dans `./conf`, tu ne perds aucun réglage. Les stats et logs restent dans `./work`.

---

## FAQ

### Puis-je utiliser AdGuard Home comme serveur DHCP ?

Oui, c'est optionnel. AdGuard Home peut remplacer le DHCP de ta box, ce qui facilite l'attribution DNS automatique à tous les appareils. En Docker, il faut utiliser `network_mode: host` pour que le DHCP fonctionne.

### Quels ports utiliser pour AdGuard Home en Docker ?

Tu dois exposer au minimum `53/tcp` et `53/udp` pour le DNS, `3000/tcp` pour le setup initial, et `80/tcp` (ou `443/tcp` pour HTTPS). Le port `67/udp` est nécessaire uniquement si tu actives le DHCP.

### Quelle est la différence entre AdGuard Home et Pi-hole ?

AdGuard Home est plus léger, intègre nativement DNS-over-HTTPS/TLS/QUIC et son interface est plus moderne. Pi-hole reste plus mature sur les listes communautaires et le filtering regex avancé.

### Mon internet coupe quand le conteneur s'arrête. Normal ?

Totalement. Si ta box pointe vers AdGuard comme DNS unique et que le conteneur est down, plus de résolution de noms. Configure un DNS secondaire de secours sur ta box, ou monte une solution HA (keepalived, deux instances AdGuard).

### Dois-je ouvrir le port 3000 en permanence ?

Non. Le port 3000 sert uniquement pour le wizard initial. Une fois configuré, tu peux le retirer du `docker-compose.yml` et du firewall. Le dashboard tourne ensuite sur le port 80 (ou 443 si HTTPS).

---

## Conclusion

AdGuard Home n'est pas "le nouveau Pi-hole qui tue l'ancien". C'est un outil différent, plus moderne sur l'intégration DNS chiffré et plus léger en ressources. Pour un auto-hébergeur qui veut un DNS filtrant propre sans monter une usine à gaz avec Unbound + cloudflared + Pi-hole, c'est le choix malin.

Le container `adguard/adguardhome:latest` fait moins de 30 Mo, démarre en quelques secondes, et une fois ton routeur configuré, **tout ton réseau est nettoyé** : pub, trackers, malware, et même les requêtes teslascopes de tes objets connectés.

Fais-le tourner ce week-end. Ton bandwidth te remerciera, et ta TV Samsung arrêtera d'appeler ses serveurs toutes les 30 secondes.

---

## Articles connexes

- [Guide complet pour débuter l'auto-hébergement avec Docker](/docker-debutant-services-auto-heberger/)
- [Nextcloud en Docker : installation complète 2025](/nextcloud-docker-installation-complete-2025/)
- [Jellyfin en Docker : alternative Netflix gratuite](/jellyfin-docker-alternative-netflix-gratuite/)
- [Uptime Kuma 2.0 : monitoring auto-hébergé](/uptime-kuma-2-0-monitoring-auto-heberge/)
- [Auto-hébergement : le guide complet 2025](/auto-hebergement-guide-complet-2025/)
- [Technitium DNS Server : l'alternative au-delà de Pi-hole et AdGuard](/technitium-dns-server/)
