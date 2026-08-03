---
title: "Syncthing Docker : synchronise tes fichiers sans le cloud"
description: "Syncthing Docker : synchronise tes fichiers entre appareils sans cloud. Tutoriel complet Docker Compose, sécurité et configuration P2P."
pubDatetime: "2026-08-03T08:00:00.000Z"
modDatetime: "2026-08-03T08:00:00.000Z"
author: Brandon Visca
tags:
  - debutant
  - auto-hebergement
  - docker
  - syncthing
  - synchronisation
  - p2p
featured: false
draft: false
focusKeyword: syncthing docker
faqs: []
ogImage: ""
---
> 💡 **TL;DR**
> - Syncthing synchronise tes fichiers en P2P chiffré entre tous tes appareils sans serveur central ni cloud
> - Une image Docker officielle, un volume monté, et tu as une interface web sur le port 8384
> - Alternative open-source à Dropbox et Google Drive, 100 % décentralisée et zero knowledge
>
> - Docker Compose complet + sécurité et configuration multi-device ci-dessous

## Table des matières

## Pourquoi Syncthing Docker plutôt que Dropbox ?

Dropbox, Google Drive, OneDrive : c'est pratique, jusqu'au jour où tes données passent par les serveurs de Microsoft, où un abonnement à 10 €/mois te semble normal, ou où une faille expose tes fichiers personnels à des milliers d'inconnus. Le problème n'est pas la synchronisation : c'est la dépendance à un tiers qui lit, indexe et potentiellement partage tes données.

**Syncthing Docker** résout ça différemment. C'est un outil de synchronisation de fichiers continu, open-source (licence MPL-2.0), développé par le projet `syncthing` sur GitHub avec plus de 67 000 stars. Aucun serveur central : tes appareils communiquent directement en P2P, via le protocole Block Exchange Protocol (BEP). Le trafic est chiffré en TLS 1.3, et aucun mot de passe ou fichier n'est stocké chez un tiers. Même les serveurs de découverte (pour localiser tes appareils) ne voient que les identifiants chiffrés, pas le contenu.

Ce qui fait la différence avec un [Nextcloud auto-hébergé](/nextcloud-docker-installation-complete-2025/) : Syncthing ne demande pas de base de données, pas d'interface lourde, pas de gestion d'utilisateurs. Tu veux juste que ton dossier `Documents` sur ton laptop soit identique à celui de ton serveur NAS ? Syncthing le fait en silence, en continu, avec une empreinte mémoire de ~50 Mo.

## Syncthing vs les alternatives : tableau comparatif

| Outil | P2P / Cloud | Chiffrement | Docker officiel | Sans compte | Ressources |
|-------|-------------|-------------|-----------------|-------------|------------|
| **Syncthing** | P2P direct | TLS 1.3 + chiffrement device | Oui (`syncthing/syncthing`) | Oui | ~50 Mo RAM |
| **Dropbox** | Cloud central | AES-256 (chez Dropbox) | Non | Non | Client lourd |
| **Google Drive** | Cloud central | AES-256 (chez Google) | Non | Non | Client lourd |
| **Nextcloud** | Auto-hébergé | TLS + au repos | Oui (`nextcloud`) | Oui | ~512 Mo+ RAM |
| **Resilio Sync** | P2P hybride | AES-256 | Non (propriétaire) | Non (freemium) | ~100 Mo RAM |
| **rsync + cron** | Manuel | SSH | Non (natif) | Oui | Négligeable |

Mon choix pour un homelab Dockerisé : **Syncthing**. Parce que c'est le seul outil à combiner P2P natif, open-source, image Docker officielle maintenue, et zero configuration réseau complexe. rsync est puissant mais manuel. Nextcloud est génial pour collaborer, mais overkill pour une simple synchro de dossiers.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose installés
- Au moins deux appareils à synchroniser (serveur + laptop, ou deux serveurs)
- Un dossier source existant sur l'hôte, avec les bonnes permissions (PUID/PGID)
- (Optionnel) Un reverse proxy si tu veux exposer l'interface web avec HTTPS

## Syncthing Docker Compose : installation complète

Crée un dossier dédié et le fichier `docker-compose.yml` :

```yaml
services:
  syncthing:
    image: syncthing/syncthing:latest
    container_name: syncthing
    hostname: mon-serveur-syncthing
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Paris
    volumes:
      - ./config:/var/syncthing/config
      - /path/to/your/data:/var/syncthing/data
    ports:
      - "8384:8384"
      - "22000:22000/tcp"
      - "22000:22000/udp"
      - "21027:21027/udp"
    restart: unless-stopped
    networks:
      - syncthing-net

networks:
  syncthing-net:
    driver: bridge
```

Quelques explications :

- `PUID` / `PGID` : adapte à l'utilisateur propriétaire de tes données (`id $USER` pour connaître les valeurs). Syncthing doit pouvoir lire et écrire dans le volume de données.
- `/var/syncthing/config` : contient la base de données interne, les certificats device et la configuration XML. À sauvegarder régulièrement, j'en parle dans mon guide [Duplicati Docker](/duplicati-docker-sauvegarde/).
- `/var/syncthing/data` : monte le dossier que tu veux synchroniser. Tu peux ajouter autant de volumes que nécessaire.
- Port `8384` : interface web de gestion
- Port `22000` : protocole de synchro BEP (TCP + UDP)
- Port `21027` : discovery local UDP (pour trouver les appareils sur le même réseau)

Démarre le conteneur :

```bash
cd /opt/syncthing
docker compose up -d
```

L'interface web est accessible sur `http://serveur:8384`. Au premier démarrage, Syncthing génère un certificat auto-signé et un identifiant device unique (format `XXXXXXX-XXXXXXX-XXXXXXX-XXXXXXX-XXXXXXX-XXXXXXX-XXXXXXX-XXXXXXX`).

## Configuration Syncthing Docker : synchro multi-device

### 1. Relier deux appareils

Sur chaque appareil (serveur Docker + laptop, téléphone, etc.), ouvre Syncthing :

- **Action → Afficher l'ID** : copie l'identifiant device à 56 caractères
- Sur l'autre appareil, clique sur **Ajouter un appareil distant**, colle l'ID
- Donne un nom explicite (`laptop-brandon`, `nas-omv`, `pixel-8`)
- Coche **Introducteur** si cet appareil doit partager ses autres connexions
- Sauvegarde

L'autre appareil recevra une demande de connexion. Accepte-la. Les deux devices échangent alors leurs certificats TLS et établissent une connexion chiffrée. Même si tu passes par les relay servers publics (en cas de NAT strict), le contenu reste illisible.

### 2. Partager un dossier

Une fois les appareils connectés :

- Clique sur **Ajouter un dossier**
- **Chemin du dossier** : `/var/syncthing/data/mon-dossier` (dans le conteneur) ou adapte selon tes volumes
- **ID du dossier** : laisse l'UUID par défaut ou donne un nom simple (`documents`, `photos-2026`)
- Onglet **Partage** : coche les appareils distants autorisés à recevoir ce dossier
- Onglet **Versionnement** (optionnel) : active la version simple ou staggered pour garder des copies avant écrasement
- Sauvegarde

L'autre appareil recevra une notification de partage. Accepte-le, choisis le chemin local de réception, et la synchronisation démarre automatiquement. Syncthing ne transfère que les blocs modifiés (déduplication au niveau block), ce qui rend les mises à jour ultra-rapides même sur des fichiers de plusieurs gigaoctets.

### 3. Configuration avancée utile

| Paramètre | Valeur recommandée | Pourquoi |
|-----------|-------------------|----------|
| **Écouteur d'adresses** | `default` | Écoute sur 0.0.0.0:22000, IPv4 + IPv6 |
| **Serveur de relais** | `default` | Active les relay publics en secours (données chiffrées) |
| **Découverte globale** | Activée | Permet de trouver tes appareils même sans IP fixe |
| **Découverte locale** | Activée | Découverte rapide sur le LAN (broadcast UDP) |
| **Limite bande passante** | `0` (illimité) ou personnalise | Évite de saturer ta connexion |
| **Rescan interval** | 3600s (1h) | Syncthing utilise l'os fs watcher, le rescan est rarement utile |

Si tu débutes avec Docker et que ce vocabulaire te semble dense, mon [guide des 10 services essentiels](/docker-debutant-services-auto-heberger/) reprend les bases de Docker Compose et des volumes avec des explications plus progressives.

## Sécurité et bonnes pratiques

### Interface web et mot de passe

Par défaut, l'interface web de Syncthing écoute sur `127.0.0.1:8384`. Quand tu l'exposes via Docker sur `0.0.0.0:8384`, elle devient accessible depuis n'importe quelle IP du réseau. Définit immédiatement un mot de passe GUI :

- **Actions → Paramètres → Interface GUI**
- **Nom d'utilisateur GUI** : `admin`
- **Mot de passe GUI** : un mot de passe fort (généré par ton gestionnaire)
- Coche **Use HTTPS for GUI** pour forcer TLS sur l'interface

### Reverse proxy avec Traefik (optionnel)

Si tu veux un accès externe sécurisé, ne fais pas de port-forwarding direct sur le 8384. Passe par un reverse proxy avec authentification. J'ai détaillé le déploiement de [Traefik v3](/traefik-reverse-proxy-docker/) : labels auto-discovery, HTTPS Let's Encrypt, et middlewares basiques en quelques lignes.

Exemple de labels Traefik pour Syncthing :

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.syncthing.rule=Host(`sync.tondomaine.fr`)"
  - "traefik.http.routers.syncthing.tls.certresolver=letsencrypt"
  - "traefik.http.services.syncthing.loadbalancer.server.port=8384"
```

### Sauvegarde de la config

Le dossier `./config` contient le fichier `config.xml` et les certificats device. Sans eux, tu perds l'identité de ton appareil et toutes les relations de confiance établies avec les autres nodes. Backupe ce dossier comme n'importe quel volume Docker critique.

### Pare-feu

Ouvre uniquement les ports nécessaires :

```bash
sudo ufw allow 8384/tcp   # Interface web (si pas de reverse proxy)
sudo ufw allow 22000/tcp  # BEP protocol
sudo ufw allow 22000/udp  # BEP protocol (QUIC)
sudo ufw allow 21027/udp  # Discovery local
```

Si tu utilises un reverse proxy, le port 8384 n'a pas besoin d'être exposé publiquement : Traefik communique en interne Docker.

## Monitoring et résolution de problèmes

### Vérifier l'état de la synchro

L'interface web affiche l'état de chaque dossier et appareil :

- **Synchronisé à 100 %** : vert, tout est à jour
- **Synchronisation (xx %)** : orange, transfert en cours
- **Hors tension** : gris, appareil injoignable (vérifie le pare-feu ou la connexion)
- **Désynchronisé** : rouge, conflit de version ou erreur réseau

### Logs utiles

```bash
docker logs -f syncthing --tail 100
```

Les lignes importantes à surveiller :

- `Detected 0 NAT devices` : normal derrière un routeur, les relays prendront le relais
- `Connected to device XXXXXXX...` : connexion P2P établie
- `Folder "documents" is syncing (42 %)` : progression du transfert
- `File name is invalid on Windows` : conflit de nommage (caractères interdits), à corriger manuellement

### Conflits de fichiers

Quand un fichier est modifié sur deux appareils simultanément, Syncthing crée une version conflictuelle :

```text
mon-document.sync-conflict-20260803-143000-laptop.txt
```

Garde la bonne version, supprime le conflit. Active le versionnement (simple ou staggered) pour éviter la perte de données.

## Conclusion

Syncthing est l'outil de synchronisation que j'installe systématiquement sur chaque serveur et laptop de mon homelab. Il remplace Dropbox sans effort cognitif, sans abonnement, et sans céder tes données à une multinationale. Avec Docker, le déploiement prend moins de dix minutes : une image officielle, un volume monté, et tes fichiers voyagent chiffrés entre tes appareils 24h/24. Si tu prends le contrôle de ton cloud avec [Nextcloud](/nextcloud-docker-installation-complete-2025/) et que tu sauvegardes tes volumes avec [Duplicati](/duplicati-docker-sauvegarde/), Syncthing complète parfaitement la chaîne en assurant la synchro temps réel entre tous tes endpoints. Décentraliser tes données, ce n'est pas un caprice idéologique : c'est une stratégie opérationnelle qui marche, aujourd'hui, maintenant.
