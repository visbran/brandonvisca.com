---
title: "Transmission Docker : client torrent ultra-léger avec interface web"
description: "Déploie Transmission avec Docker : client torrent ultra-léger, interface web, et intégration parfaite avec ta stack mediacenter auto-hébergée."
pubDatetime: "2026-09-01T06:00:00.000Z"
modDatetime: "2026-09-01T06:00:00.000Z"
author: Brandon
tags:
  - transmission
  - torrent
  - auto-hebergement
  - docker
  - debutant
featured: false
draft: false
focusKeyword: transmission docker
ogImage: ""
---
> 💡 **TL;DR**
>
> - Transmission en Docker est le client torrent le plus léger du marché : il tourne sur un Raspberry Pi sans broncher
> - Interface web native, zéro bloat : tu gères tes téléchargements depuis n'importe quel navigateur
> - S'intègre à Sonarr, Radarr et la famille *arr pour un pipeline mediacenter 100% automatisé

Tu cherches un client torrent qui ne bouffe pas toute ta RAM, qui démarre en deux secondes, et qui ne te spamme pas de publicités à chaque clic ? Bienvenue dans le monde de Transmission. Créé en 2005 par les équipes derrière macOS, c'est le client BitTorrent qui a fait ses preuves depuis presque vingt ans. Pas de spyware, pas d'interface lourde en Qt qui met trois plombes à s'afficher, pas de fonctionnalités inutiles qui sentent le développeur qui s'ennuie. Juste un moteur de téléchargement propre, mature, et efficace.

Et quand tu le mets dans un conteneur Docker, Transmission devient un service discret qui tourne en arrière-plan sur ton serveur, accessible depuis une interface web minimaliste. Si tu as déjà lu mon guide sur [qBittorrent Docker](/qbittorrent-docker-client-torrent/), tu te demandes sûrement quel client choisir. La réponse est simple : qBittorrent est le couteau suisse avec toutes les options, Transmission est le scalpel qui consomme trois fois moins de mémoire et démarre instantanément. Pour un serveur auto-hébergé où chaque mégabyte compte, le choix se fait vite.

## Table des matières

## Pourquoi choisir Transmission Docker ?

Commençons par le chiffre qui tue. Un conteneur Transmission au repos consomme environ 30 à 50 Mo de RAM. qBittorrent consomme 150 à 250 Mo dans la même situation. Sur un Raspberry Pi 4 avec 4 Go de RAM, cette différence représente le quart de ta mémoire disponible. Sur un VPS low-cost avec 1 Go de RAM, c'est la différence entre un serveur fluide et un serveur qui swap jusqu'à la mort. Transmission est écrit en C, le code est mature et épuré, et le projet est maintenu activement depuis deux décennies. Ce n'est pas un joujou qu'un développeur a abandonné après six mois parce qu'il s'est découvert une passion pour le crochet.

L'interface web de Transmission est l'autre argument massue. Elle est incluse nativement depuis la conception du logiciel. Pas besoin d'activer un plugin caché dans trois sous-menus, pas besoin d'installer une extension tierce. Tu démarres le conteneur, tu ouvres le port 9091, et tu as une interface responsive qui fonctionne sur desktop, tablette et mobile. Elle est minimaliste : une liste de torrents, une barre de progression, des infos de vitesse. Rien de plus. Et c'est exactement ce qu'il faut quand tu veux juste vérifier si ton téléchargement est fini sans attendre quinze secondes qu'une interface lourde se charge.

La philosophie de Transmission mérite aussi qu'on s'y attarde. Dans un monde où chaque logiciel veut devenir une plateforme avec son propre magasin d'applications, Transmission reste fidèle à un seul job : télécharger et partager des fichiers via BitTorrent. Pas de moteur de recherche intégré qui rame, pas de milliers d'options de configuration obscures, pas de gestionnaire de plugins à maintenir. C'est un client torrent. Point final. Si tu veux un outil qui fait une chose et qui la fait bien, tu es au bon endroit.

Et puis il y a le dossier `watch`. Cette petite fonctionnalité souvent négligée est un game changer pour l'automatisation. Tu déposes un fichier `.torrent` dans un dossier spécifique, et Transmission le démarre automatiquement. Quand tu branches ça à Sonarr, Radarr et consorts, tu obtiens un pipeline où les téléchargements se lancent sans aucune intervention manuelle. C'est propre, c'est fiable, et ça ne dépend pas d'une API qui peut changer de version demain.

## Prérequis

Avant de balancer le `docker-compose.yml`, assure-toi d'avoir les bases en place :

- Un serveur Linux avec Docker et Docker Compose installés. Si ce n'est pas encore fait, retourne sur le [guide Docker pour débutants](/docker-debutant-services-auto-heberger/) avant de continuer.
- Un volume de stockage dédié pour tes téléchargements. Idéalement séparé du système, sur un disque externe ou un volume monté.
- Un réseau Docker commun pour tes services mediacenter. On va utiliser le réseau `mediacenter`, comme pour les autres services de la stack.
- Une connexion internet fonctionnelle et un port disponible sur ta box pour le trafic BitTorrent.

Si tu n'as pas encore créé le réseau `mediacenter`, c'est le moment :

```bash
docker network create mediacenter
```

Ce réseau permet à tous tes conteneurs mediacenter de communiquer entre eux sans exposer de ports supplémentaires à l'extérieur. Transmission pourra parler à Sonarr, Radarr et Jellyfin directement par leur nom de conteneur, comme s'ils étaient sur le même switch local.

## Docker Compose : le déploiement

Crée un dossier dédié pour Transmission et place ton fichier de configuration à l'intérieur :

```bash
mkdir -p ~/docker/transmission
cd ~/docker/transmission
```

Voici le `docker-compose.yml` que j'utilise en production depuis des mois. Il est simple, efficace, et il fonctionne du premier coup :

```yaml
services:
  transmission:
    image: lscr.io/linuxserver/transmission:latest
    container_name: transmission
    restart: unless-stopped
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Paris
      - USER=admin
      - PASS=motdepasse_ultra_secure
    volumes:
      - ./config:/config
      - /data/downloads:/downloads
      - /data/downloads/watch:/watch
    ports:
      - "9091:9091"
      - "51413:51413"
      - "51413:51413/udp"
    networks:
      - mediacenter

networks:
  mediacenter:
    external: true
```

Quelques explications pour ceux qui aiment comprendre ce qu'ils font :

- `PUID` et `PGID` : identifiants de ton utilisateur Linux sur le système hôte. Exécute `id $USER` pour connaître les tiens. Transmission doit pouvoir lire et écrire dans le dossier de téléchargement.
- `USER` et `PASS` : identifiants de l'interface web. Change ce mot de passe, évidemment. Si tu ne configures rien, Transmission démarre sans authentification, ce qui est une mauvaise idée si ton serveur est exposé.
- `./config` : persiste la configuration du client, la liste des torrents, et les paramètres de l'interface web.
- `/data/downloads` : dossier où tes fichiers téléchargés seront stockés. Adapte ce chemin à ton infrastructure de stockage.
- `/data/downloads/watch` : dossier magique. Tu y déposes un fichier `.torrent`, Transmission le récupère automatiquement en quelques secondes. C'est particulièrement utile pour l'intégration avec les outils *arr.
- `9091` : port de l'interface web. Tu peux le changer si ce port est déjà occupé sur ton serveur.
- `51413` : port de communication BitTorrent. TCP et UDP sont nécessaires pour échanger avec les peers et le tracker.
- `restart: unless-stopped` : si ton serveur redémarre, Transmission redémarre automatiquement avec lui.

Lance le tout avec une seule commande :

```bash
docker compose up -d
```

En dix secondes chrono, ton conteneur est opérationnel. Tu peux vérifier qu'il est bien démarré avec :

```bash
docker compose ps
```

Puis ouvre ton navigateur sur `http://IP_DU_SERVEUR:9091`.

## Interface web et première configuration

L'interface web de Transmission est un modèle d'économie. Une barre d'outils en haut, une liste de torrents au milieu, un panneau d'informations en bas. C'est tout. Pas d'onglets qui s'empilent, pas de menus contextuels à dix niveaux, pas de publicités qui clignotent.

Pour ajouter un torrent, tu as trois options :

1. **Le bouton "Ajouter"** en haut à gauche pour uploader un fichier `.torrent` depuis ton ordinateur.
2. **Un lien magnet** que tu colles directement dans le champ prévu.
3. **Le dossier `watch`** que tu as monté. Tu déposes un fichier `.torrent` dedans via SSH, SFTP, ou un script, et Transmission le démarre automatiquement en quelques secondes.

Va dans les préférences via l'icône d'engrenage en bas à gauche et configure ces points essentiels :

**Vitesse et bande passante :**
- Limite de téléchargement : adapte selon ta connexion. Si tu as de la fibre symétrique, tu peux laisser libre. Si tu es en ADSL, limite à 80% de ta bande passante pour garder un internet utilisable.
- Limite d'envoi : idem. L'upload consomme de la bande passante montante et augmente la latence de ta connexion.
- Ratio de partage : configure un arrêt automatique à un ratio de 2.0. C'est la courtoisie BitTorrent de base : tu reprends ce que tu as pris, et tu rends le double.

**Peers et réseau :**
- Limite globale de peers : 200 suffisent largement pour un usage domestique.
- Peers par torrent : 50 est une valeur équilibrée.
- Port d'écoute : vérifie qu'il est bien sur 51413, celui que tu as exposé dans le `docker-compose.yml`.
- Activer le DHT et le LPD : oui, pour trouver plus de sources sans dépendre uniquement du tracker.

**Fichiers :**
- Vérifie que le dossier de téléchargement par défaut pointe bien vers `/downloads` dans le conteneur. C'est le chemin interne, pas le chemin de ton hôte.

Le dossier `/watch` est ton allié pour l'automatisation. Quand tu branches Transmission à [Sonarr](/sonarr-docker-gestion-series/), celui-ci dépose les fichiers `.torrent` directement dans ce dossier. Transmission les consomme, télécharge les épisodes, et Sonarr récupère les fichiers terminés pour les renommer et les classer. Tu n'as jamais à toucher un fichier `.torrent` de ta vie.

## Intégration avec Sonarr et la famille *arr

Transmission brille particulièrement quand tu le branches à ton écosystème mediacenter. Si tu as déjà déployé [Sonarr pour gérer tes séries](/sonarr-docker-gestion-series/), la connexion est d'une simplicité déconcertante.

Dans Sonarr, va dans **Settings > Download Clients > Ajouter (+) > Transmission**.

Remplis les champs comme suit :

- **Nom** : Transmission
- **Hôte** : `transmission` (c'est le nom du conteneur sur le réseau Docker `mediacenter`)
- **Port** : `9091`
- **URL Base** : laisse vide
- **Nom d'utilisateur** : `admin` (ou ce que tu as configuré dans le `docker-compose.yml`)
- **Mot de passe** : ton mot de passe
- **Catégorie** : `sonarr` (facultatif mais recommandé, cela crée un sous-dossier pour trier les téléchargements)

Teste la connexion. Si tout est vert, Sonarr peut maintenant envoyer des torrents directement à Transmission. Le processus est le suivant :

1. Sonarr détecte qu'un nouvel épisode est sorti.
2. Il choisit la meilleure release selon ton profil de qualité.
3. Il envoie le `.torrent` à Transmission via l'API.
4. Transmission télécharge le fichier.
5. Quand le téléchargement est terminé, Sonarr détecte le fichier, le renomme proprement, et le déplace dans ta bibliothèque `/data/series`.

Tu n'as plus rien à faire. Tu ajoutes une série dans Sonarr une fois, et chaque nouvel épisode apparaît automatiquement dans Jellyfin ou Plex quelques minutes après sa sortie.

Le même principe fonctionne avec Radarr pour les films, Lidarr pour la musique, et Readarr pour les livres. Tous ces outils parlent le même dialecte que Transmission via son API JSON-RPC stable et bien documentée. C'est la magie du self-hosting quand les outils sont choisis pour s'assembler comme des Lego.

## Sécuriser ses téléchargements avec un VPN

Je ne vais pas faire le donneur de leçons, mais télécharger sur internet sans protection, c'est comme sortir en sous-vêtements par moins dix degrés. Tu peux le faire, mais il va t'arriver des bricoles.

Transmission ne gère pas le VPN nativement, et c'est une bonne chose. Un client torrent n'a pas à s'occuper de chiffrement réseau, c'est le boulot d'un VPN dédié. La méthode propre consiste à faire tourner Transmission derrière un conteneur VPN, ou à configurer un VPN au niveau du réseau de ton serveur.

Si tu cherches une solution simple et éprouvée, déploie un [VPN WireGuard](/wireguard-docker-vpn-homelab/) sur ton serveur. Tu crées un tunnel sécurisé, et tu configures Transmission pour n'écouter que sur l'interface du tunnel. C'est propre, ça n'impacte pas les autres services, et ça évite les solutions "tout-en-un" qui cachent un client BitTorrent modifié derrière une interface jolie mais opaque.

Pour les utilisateurs avancés, il existe aussi Gluetun, un conteneur qui encapsule tout le trafic d'un autre conteneur via OpenVPN ou WireGuard. Tu fais tourner Transmission dans le même namespace réseau que Gluetun, et bim, tout le trafic BitTorrent passe par le VPN automatiquement. Mais ça sort du scope débutant. Maîtrise d'abord le déploiement de base, puis tu pourras complexifier.

## Astuces et optimisation

Transmission est déjà léger de base, mais tu peux encore optimiser quelques paramètres pour qu'il tourne comme un coussin sur ton serveur.

**Change le port par défaut.** Le port 51413 est saturé par des millions d'utilisateurs et souvent bridé par les FAI. Configure plutôt un port entre 49160 et 65535. Les trackers et le DHT répondent mieux, et tu auras plus de peers connectés.

**Active la liste de blocage.** Va dans Preferences > Privacy > Enable blocklist. Colle une URL comme `https://github.com/Naunter/BT_BlockLists/raw/master/bt_blocklists.gz`. Cela filtre les IPs connues pour être nuisibles ou malveillantes. Ce n'est pas un bouclier absolu, mais ça élimine une partie du bruit.

**Surveille ton disque.** Transmission consomme peu de RAM, mais les torrents peuvent saturer un disque dur mécanique si tu télécharges trop vite. Un SSD pour le cache et les fichiers temporaires, couplé à un HDD pour le stockage final, reste le combo gagnant pour un mediacenter. Si tu n'as qu'un seul disque, limite le nombre de torrents actifs simultanés à 5 ou 10.

**Utilise le RPC pour scripter.** L'API JSON-RPC de Transmission est d'une simplicité biblique. Avec `curl` et dix lignes de bash, tu peux ajouter des torrents automatiquement, vérifier la vitesse globale, ou purger les téléchargements terminés. C'est plus léger qu'une librairie Python obscure qui nécessite quinze dépendances.

**Sauvegarde ton dossier config.** Le dossier `./config` que tu as monté contient la liste de tous tes torrents, leurs ratios, et tes paramètres. Fais-en une copie régulière. Si ton serveur crashe, restaurer ce dossier suffit pour retrouver Transmission exactement comme avant.

## Dépannage rapide

**Transmission ne démarre pas et affiche une erreur de port.**
Si le port 9091 est déjà pris sur ton serveur, change le mapping dans le `docker-compose.yml` : remplace `"9091:9091"` par `"9092:9091"`. L'interface web sera alors accessible sur le port 9092.

**L'interface web est inaccessible depuis l'extérieur.**
Vérifie que le conteneur est bien démarré avec `docker compose ps`, et que ton firewall autorise le port 9091. Si tu es derrière un reverse proxy comme Traefik, vérifie que la route est correctement configurée.

**Les torrents ne se connectent à aucun peer.**
Deux causes probables. Première, le port 51413 n'est pas redirigé sur ta box internet. Deuxième, ton FAI bloque le protocole BitTorrent. Certains opérateurs, notamment sur les réseaux mobiles ou les connexions partagées, brident activement le trafic P2P. Un VPN résout ce problème.

**Sonarr ne parvient pas à communiquer avec Transmission.**
Assure-toi que les deux conteneurs sont bien sur le même réseau Docker `mediacenter`. Dans Sonarr, l'hôte doit être `transmission` (le nom du conteneur), pas l'IP locale de ton serveur. Docker résout les noms de conteneur automatiquement sur un réseau personnalisé.

**Les téléchargements sont lents malgré une bonne connexion.**
Vérifie le nombre de peers connectés, la limite de vitesse configurée, et le port d'écoute. Un port mal redirigé ou bloqué par le firewall réduit drastiquement les performances. Essaye aussi un autre torrent pour écarter un problème de tracker.

## Conclusion

Transmission en Docker, c'est le choix malin quand tu veux un client torrent qui fait son job sans se plaindre. Pas de frills, pas de bloat, pas d'interface qui fait ramer ton navigateur : juste un moteur de téléchargement efficace qui s'intègre parfaitement à ton écosystème auto-hébergé. Sur un serveur limité en ressources, un Raspberry Pi, ou un VPS low-cost, c'est souvent le meilleur choix face à des alternatives plus complètes mais nettement plus lourdes.

Déploie-le, configure-le une fois, branche-le à Sonarr, et oublie-le. C'est exactement ce qu'on attend d'un bon outil d'infrastructure : il fonctionne, il est invisible, et il ne te réveille pas la nuit.
