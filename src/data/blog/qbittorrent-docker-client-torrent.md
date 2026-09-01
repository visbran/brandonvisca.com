---
title: "qBittorrent Docker : client torrent avec interface web auto-hébergé"
description: "qBittorrent Docker : déploie un client torrent auto-hébergé avec interface web et intègre-le à ta stack mediacenter en quelques minutes."
pubDatetime: "2026-08-30T06:00:00.000Z"
modDatetime: "2026-08-30T06:00:00.000Z"
author: Brandon Visca
tags:
  - qbittorrent
  - auto-hebergement
  - docker
  - debutant
  - mediacenter
featured: false
draft: false
focusKeyword: qbittorrent docker
faqs:
  - question: ""
    answer: ""
ogImage: ""
---
> 💡 **TL;DR**
> - qBittorrent en Docker te donne un client torrent complet accessible depuis n'importe quel navigateur.
> - L'image LinuxServer est stable, bien maintenue et s'intègre facilement à ta stack mediacenter.
> - Branché à Radarr, Sonarr et Prowlarr, tu obtiens un pipeline de téléchargement 100% automatisé.

Tu en as marre de laisser ton PC allumé la nuit pour finir un torrent ? Ou pire, tu utilises encore un client desktop qui bouffe tes ressources et dont tu perds le contrôle dès que tu sors de chez toi ? C'est fini. On va déployer **qBittorrent avec Docker**, et tu vas pouvoir gérer tes téléchargements depuis une interface web propre, n'importe où, n'importe quand.

qBittorrent, c'est le client open-source qui a fait oublier µTorrent à toute une génération. Pas de pub, pas de spyware, pas de limite débile. Et en version Docker, il devient un service propre, isolé et intégrable dans ton homelab. Prêt ? C'est parti.

## Pourquoi qBittorrent Docker plutôt qu'un client desktop ?

Bon, déjà, la question elle est vite répondue. Un client desktop, c'est bien pour un usage ponctuel sur ta machine. Mais pour un mediacenter auto-hébergé, c'est une plaie :

- Ton PC doit rester allumé 24/7.
- Tu n'as pas accès à distance facilement.
- Les mises à jour sont manuelles et pénibles.
- Ça pollue ton système avec des dossiers de config partout.

Avec Docker, qBittorrent tourne sur ton serveur, isolé dans son propre container. Tu y accèdes via une interface web. Il redémarre automatiquement si ton serveur reboot. Tu peux le brancher à Radarr, Sonarr et le reste de la famille *arr pour que tout se télécharge tout seul. Bref, c'est propre.

Et puis soyons honnêtes : si tu lis ce blog, c'est que tu es déjà convaincu par Docker. Si ce n'est pas encore le cas, va jeter un œil au [guide Docker Compose complet](/docker-debutant-services-auto-heberger/) pour comprendre pourquoi c'est devenu indispensable.

## Prérequis

Avant de balancer le `docker-compose.yml`, vérifie que tu as bien :

- Un serveur Linux avec Docker et Docker Compose installés.
- Un volume de stockage dédié pour tes téléchargements (idéalement séparé du système).
- Un réseau Docker commun pour tes services mediacenter (on va utiliser `mediacenter`).
- Une connexion internet décente (évidemment).
- La ferme envie d'automatiser tout ça.

Si tu n'as pas encore de réseau `mediacenter`, crée-le :

```bash
docker network create mediacenter
```

## Docker Compose : le déploiement

Crée un dossier pour qBittorrent et place ton fichier de configuration dedans :

```bash
mkdir -p ~/docker/qbittorrent
cd ~/docker/qbittorrent
```

Voici le `docker-compose.yml` que j'utilise en production. Il est simple, efficace, et il marche :

```yaml
services:
  qbittorrent:
    image: lscr.io/linuxserver/qbittorrent:latest
    container_name: qbittorrent
    restart: unless-stopped
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Paris
      - WEBUI_PORT=8080
    volumes:
      - ./config:/config
      - /data/downloads:/downloads
    ports:
      - "8080:8080"
      - "6881:6881"
      - "6881:6881/udp"
    networks:
      - mediacenter

networks:
  mediacenter:
    external: true
```

Quelques explications pour les curieux :

- `PUID` et `PGID` : les IDs utilisateur et groupe de ton utilisateur Linux. Adapte selon ton système (`id $USER` pour les connaître).
- `WEBUI_PORT=8080` : le port de l'interface web. Tu peux le changer si 8080 est déjà pris.
- `/data/downloads` : le dossier où tes torrents seront téléchargés. Adapte le chemin à ton setup.
- `6881` : le port de communication BitTorrent. TCP et UDP sont nécessaires.
- `restart: unless-stopped` : le container redémarre automatiquement sauf si tu l'arrêtes manuellement.

Lance le tout :

```bash
docker compose up -d
```

Attends quelques secondes que le container initialise sa config, puis ouvre ton navigateur sur `http://IP_DU_SERVEUR:8080`.

## Première connexion et sécurisation

Par défaut, l'interface web de qBittorrent utilise des identifiants basiques :

- **Utilisateur** : `admin`
- **Mot de passe** : un mot de passe temporaire généré automatiquement

Pour récupérer ce mot de passe temporaire, consulte les logs du container :

```bash
docker logs qbittorrent | grep password
```

Tu vas voir une ligne du genre :

```
The WebUI admin password has not been changed from the default. Your temporary password is: abc123def456
```

Connecte-toi avec ces identifiants, puis va immédiatement dans **Outils > Options > Interface Web** pour changer le mot de passe. Ne laisse jamais le mot de passe par défaut, sauf si tu aimes qu'un bot ukrainien utilise ta connexion pour miner du Monero.

Tant que tu es dans les options, désactive l'authentification locale si tu accèdes via un reverse proxy (on y vient), et active l'HTTPS si tu exposes qBittorrent sur internet. Même si dans l'idéal, tu ne devrais jamais exposer ton client torrent directement sur le web sans protection.

## La config qui change tout

qBittorrent marche out of the box, mais quelques réglages bien placés te feront gagner du temps et de la bande passante.

### Emplacement des téléchargements

Dans **Outils > Options > Téléchargements**, configure le dossier de téléchargement par défaut :

```
/downloads/complete
```

Et active l'option "Conserver les fichiers non récupérés en haut" pour que Radarr et Sonarr trouvent plus facilement leurs petits.

### Limites de bande passante

Si tu ne veux pas que tes streams Jellyfin saccadent parce qu'un torrent de 80 Go part en plein milieu, limite la vitesse de téléchargement et d'envoi dans **Outils > Options > Vitesse**. Perso, je mets un plafond à 80% de ma bande passante totale.

### Sonde de port

Dans **Outils > Options > Connexion**, vérifie que le port d'écoute correspond bien à celui exposé dans Docker (`6881` dans notre exemple). Active l'UPnP si ton routeur le supporte, ou configure une règle NAT manuelle pour rediriger le port 6881 vers ton serveur.

### Torrents RSS

Si tu suis des releases régulièrement, configure un flux RSS dans **Outils > Options > Lecteur RSS**. Pratique pour suivre les sorties de tes séries préférées sans passer par Prowlarr. Mais bon, entre nous, Prowlarr fait ça mieux.

## Le Web UI en détail

L'interface web de qBittorrent est franchement bien foutue. Elle reprend quasiment toutes les fonctionnalités du client desktop : ajout de torrents via magnet ou fichier `.torrent`, gestion des priorités, limitation de vitesse par torrent, tags, catégories, et même un petit graphique de vitesse en temps réel.

Ce que j'apprécie particulièrement : la gestion des catégories. Tu peux créer des catégories comme `radarr`, `tv-sonarr`, `manual`, `linux-isos` (wink wink), et chaque torrent se retrouve automatiquement dans le bon dossier. C'est indispensable quand tu as plusieurs applications qui écrivent dans le même volume de téléchargements.

Autre fonctionnalité sympa : le moteur de recherche intégré. Si tu configures des plugins de recherche (Plugins > Rechercher des plugins), tu peux chercher directement dans l'interface web sans passer par un site de tracker. Pratique quand tu veux tester rapidement si un fichier existe quelque part.

Et puis il y a la vue "Contenu" qui te montre les fichiers individuels d'un torrent. Utile quand tu télécharges une saison complète mais que tu ne veux récupérer que deux épisodes. Tu décoches le reste, et hop, pas de gâchis d'espace disque.

## Sécurité : ne joue pas au cow-boy

Un client torrent exposé sur internet, c'est une cible. Voici les règles de base :

1. **Ne jamais exposer le port 8080 directement sur internet.** Utilise un reverse proxy (Traefik, Caddy, Nginx Proxy Manager) avec authentification.
2. **Changer le mot de passe admin immédiatement.** On en a déjà parlé, mais c'est important.
3. **Utiliser un VPN si nécessaire.** L'image LinuxServer supporte WireGuard et OpenVPN via des variables d'environnement spécifiques si tu veux router tout le trafic du container.
4. **Restreindre l'accès par IP.** Dans les options de l'interface web, tu peux whitelist certaines IP.
5. **Activer les mises à jour automatiques.** L'image `latest` se met à jour via Watchtower ou un cron Docker.

Pour le VPN, LinuxServer propose des images dérivées comme `qbittorrentvpn` qui intègrent directement le tunnel. Mais si tu as déjà un VPN sur ton serveur (via un container WireGuard ou Tailscale), pas besoin de compliquer.

## Intégration avec la stack *arr

Là où qBittorrent devient vraiment intéressant, c'est quand tu le branches à ton écosystème mediacenter. Si tu as suivi mes précédents guides, tu as déjà probablement entendu parler de la famille *arr.

### Brancher Radarr

Si tu veux automatiser la gestion de tes films, j'ai déjà publié un guide sur [Radarr avec Docker](/radarr-docker-gestion-films/). Dans Radarr, va dans **Paramètres > Téléchargement > Clients de téléchargement** et ajoute qBittorrent :

- Hôte : `qbittorrent`
- Port : `8080`
- Nom d'utilisateur : `admin` (ou celui que tu as configuré)
- Mot de passe : ton mot de passe
- Catégorie : `radarr` (ça sépare les téléchargements dans un sous-dossier)

Radarr va automatiquement envoyer les torrents à qBittorrent et surveiller leur progression.

### Brancher Sonarr

Même principe pour les séries. J'ai couvert ça en détail dans le guide [Sonarr avec Docker](/sonarr-docker-gestion-series/). Configure Sonarr pour utiliser qBittorrent comme client de téléchargement avec la catégorie `tv-sonarr`.

### Brancher Prowlarr

Prowlarr, c'est l'indexeur qui fait le lien entre tes trackers et les applications *arr. Si tu ne connais pas encore, je t'invite à lire le guide sur [Prowlarr avec Docker](/prowlarr-docker-indexeur-trackers/). Une fois configuré, Prowlarr synchronise automatiquement tes indexeurs avec Radarr et Sonarr. qBittorrent n'a qu'à bien se tenir.

### Brancher Jellyseerr

Et si tu veux que tes amis ou ta famille puissent demander des films sans te spammer sur WhatsApp, [Jellyseerr avec Docker](/jellyseerr-docker-gestion-demandes/) est la solution. Jellyseerr envoie les demandes à Radarr/Sonarr, qui passent à Prowlarr, qui trouve le torrent, qui part chez qBittorrent. Tout seul. Comme par magie.

## Monitoring et dépannage

### qBittorrent ne démarre pas

Vérifie les logs :

```bash
docker logs qbittorrent --tail 50
```

Cause fréquente : un conflit de port. Si `8080` est déjà utilisé, change `WEBUI_PORT` et le mapping de ports dans le `docker-compose.yml`.

### Le Web UI est inaccessible

Assure-toi que le container est bien démarré :

```bash
docker ps | grep qbittorrent
```

Vérifie aussi que le pare-feu de ton serveur laisse passer le port 8080 :

```bash
sudo ufw allow 8080/tcp
```

### Les torrents ne téléchargent pas

- Vérifie ton port dans **Outils > Options > Connexion**.
- Teste si le port est bien ouvert avec un outil comme [canyouseeme.org](https://canyouseeme.org).
- Vérifie que le tracker est accessible (certains bloquent les IP de datacenters).
- Assure-toi que le dossier `/downloads` a les bonnes permissions (`chown -R 1000:1000 /data/downloads`).

### Lenteur de l'interface web

L'interface web de qBittorrent peut ramer avec beaucoup de torrents. Limite le nombre de torrents actifs dans les options, ou augmente les ressources CPU/RAM allouées au container.

### Mots de passe perdus

Si tu as oublié ton mot de passe admin, tu peux le réinitialiser en supprimant le fichier de configuration Web UI :

```bash
docker stop qbittorrent
rm ~/docker/qbittorrent/config/qBittorrent/qBittorrent.conf
docker start qbittorrent
```

Le mot de passe temporaire sera régénéré dans les logs.

## Optimisations avancées

### Changer le port de l'interface web

Si tu préfères un port moins évident que 8080 (ce que je recommande), modifie ton `docker-compose.yml` :

```yaml
ports:
  - "4747:8080"
```

Et garde `WEBUI_PORT=8080` (le port interne du container ne change pas, seul le mapping externe change).

### Persistance des stats et ratio

Le dossier `./config` persiste toutes les stats, les ratios, les tags et les règles RSS. Ne le supprime pas sauf si tu veux tout recommencer à zéro.

### Sauvegarde

Pour sauvegarder ta config qBittorrent :

```bash
tar czvf qbittorrent-backup-$(date +%Y%m%d).tar.gz ~/docker/qbittorrent/config
```

Restauration :

```bash
tar xzvf qbittorrent-backup-YYYYMMDD.tar.gz -C ~/docker/qbittorrent/
```

## Conclusion

qBittorrent en Docker, c'est le client torrent que tout homelab qui se respecte devrait avoir. Propre, rapide, accessible de n'importe où et parfaitement intégrable à ta stack mediacenter. Une fois que tu as goûté au téléchargement automatisé avec Radarr, Sonarr et Prowlarr, tu ne pourras plus jamais revenir en arrière.

Si tu cherches une alternative plus légère qui consomme trois fois moins de RAM, j'ai aussi testé [Transmission avec Docker](/transmission-docker-client-torrent/) — c'est le scalpel face au couteau suisse qBittorrent.

Si tu suis le [guide Docker Compose](/docker-debutant-services-auto-heberger/) pour structurer ton projet, tu auras un homelab robuste et maintenable. Le téléchargement automatisé n'est plus un fantasme de sysadmin : c'est ta réalité quotidienne. Et ça, ça n'a pas de prix.
