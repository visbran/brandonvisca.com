---
title: "PairDrop Docker : AirDrop multiplateforme via le navigateur"
description: "PairDrop Docker : héberge ton propre AirDrop multiplateforme dans le navigateur, sans compte ni appli, avec Docker Compose et reverse proxy."
pubDatetime: "2026-09-21T11:02:11+02:00"
modDatetime: "2026-09-20T08:00:00.000Z"
author: Brandon
tags:
  - auto-hebergement
  - docker
  - guide
  - intermediaire
featured: false
draft: false
focusKeyword: pairdrop docker
faqs:
  - question: "PairDrop fonctionne-t-il sans connexion internet ?"
    answer: "Oui, sur le même réseau local PairDrop passe en pair à pair via WebRTC sans jamais toucher internet, tant que les appareils partagent le même LAN ou Wi-Fi."
  - question: "Faut-il un compte ou une application à installer pour utiliser PairDrop ?"
    answer: "Non, PairDrop n'exige ni compte ni inscription : tu ouvres l'URL dans ton navigateur, les appareils se voient automatiquement et tu glisses un fichier pour l'envoyer."
  - question: "PairDrop conserve-t-il une copie des fichiers transférés sur le serveur ?"
    answer: "Non, les fichiers transitent en direct entre les navigateurs via WebRTC, le serveur ne sert qu'à la signalisation et ne stocke jamais aucun fichier envoyé."
---
> 💡 **TL;DR**
> - PairDrop Docker recrée AirDrop dans un navigateur, entre Windows, Linux, Android et iPhone, sans compte ni appli
> - Un conteneur, aucun volume, un port à exposer : l'install PairDrop Docker tient dans un docker-compose.yml de dix lignes
> - Reste en local si tu ne fais rien de plus, mais un reverse proxy en HTTPS et un serveur TURN débloquent les transferts entre réseaux différents

## Table des matières

## Pourquoi PairDrop plutôt qu'une clé USB ou Snapdrop

Tu as un iPhone, un PC sous Windows, un vieux laptop Linux et un Android qui traîne sur le bureau. Envoyer une photo de l'un à l'autre, c'est soit AirDrop (qui ne parle qu'à d'autres appareils Apple), soit un mail à toi-même, soit une clé USB qu'il faut retrouver au fond d'un tiroir.

PairDrop règle ce problème. C'est un fork de Snapdrop, maintenu par schlagmichdoch sur GitHub, qui reprend l'idée de base (transférer des fichiers en pair à pair via le navigateur, sans backend qui stocke quoi que ce soit) et l'améliore franchement : appairage persistant par code à six chiffres ou QR-code, renommage des appareils pour s'y retrouver, téléchargement automatique côté récepteur, intégration au menu contextuel sur Windows, Linux, iOS et Android, et une interface qui a été reprise de zéro.

Le projet est sous licence GPL-3.0, largement utilisé (plus de 11 000 étoiles sur GitHub) et reçoit des mises à jour régulières. Ce n'est pas un side-project abandonné après trois commits : c'est un vrai outil qui a pris la suite de Snapdrop.

La bonne nouvelle, c'est que PairDrop Docker tourne aussi bien sur un Raspberry Pi que sur ton NAS ou ton serveur de homelab. Tu l'héberges une fois, et toute la maison (ou toute la boîte) l'utilise sans rien installer.

## PairDrop Docker : installation avec Docker Compose

Deux images officielles existent : celle maintenue par LinuxServer.io, à récupérer sur son registre dédié (nom complet dans le compose ci-dessous), et celle publiée directement par le projet sur le registre GitHub (`ghcr.io/schlagmichdoch/pairdrop`). Les deux fonctionnent, l'image LinuxServer.io est la plus documentée et celle que le guide officiel met en avant en premier.

Crée un dossier dédié :

```bash
mkdir -p ~/pairdrop && cd ~/pairdrop
```

Et le fichier `docker-compose.yml` :

```yaml
services:
  pairdrop:
    image: lscr.io/linuxserver/pairdrop:latest
    container_name: pairdrop
    restart: unless-stopped
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Paris
      - WS_FALLBACK=false
      - RATE_LIMIT=false
      - RTC_CONFIG=false
      - DEBUG_MODE=false
    ports:
      - "127.0.0.1:3000:3000"
```

Ce qu'il faut retenir sur ce compose :

- `PUID`/`PGID` : les identifiants utilisateur et groupe sous lesquels tourne le conteneur, comme sur toutes les images LinuxServer.io. Récupère les tiens avec `id $USER`.
- Le port est publié uniquement sur `127.0.0.1`. Volontaire : PairDrop Docker n'a aucune raison de traîner en clair sur ton réseau ou sur internet tant qu'un reverse proxy n'est pas devant.
- Aucun volume n'est nécessaire. PairDrop ne stocke aucun fichier transféré, il n'y a rien à persister côté serveur.

Lance le conteneur :

```bash
cd ~/pairdrop
docker compose up -d
```

Ouvre `http://127.0.0.1:3000` (ou l'IP du serveur si tu retires la restriction locale pour un test rapide sur ton LAN). Les autres appareils connectés au même réseau apparaissent automatiquement dans l'interface. Tu glisses un fichier sur l'icône de l'appareil cible, l'autre côté accepte, le transfert part directement en pair à pair.

## Configuration : websocket fallback, rate limit et STUN/TURN

L'install par défaut de PairDrop Docker fonctionne très bien en local, mais quatre variables d'environnement changent son comportement :

| Variable | Rôle | Défaut |
|----------|------|--------|
| `WS_FALLBACK` | Bascule sur WebSocket quand le pair à pair WebRTC échoue (utile derrière un VPN) | `false` |
| `RATE_LIMIT` | Limite chaque client à 1000 requêtes par 5 minutes | `false` |
| `RTC_CONFIG` | Chemin vers un fichier de configuration STUN/TURN personnalisé | `false` |
| `DEBUG_MODE` | Journalise les adresses IP des pairs pour diagnostiquer une connexion qui ne s'établit pas | `false` |

Sur un homelab classique, sans VPN entre les appareils, les valeurs par défaut suffisent. Si une partie de ta famille se connecte via Tailscale ou WireGuard, passe `WS_FALLBACK=true` : le WebRTC direct peut échouer à travers ces tunnels, et le fallback WebSocket rattrape le coup au prix d'un transfert un peu plus lent, relayé par le serveur au lieu d'être vraiment pair à pair.

## Exposer PairDrop Docker derrière un reverse proxy en HTTPS

Voilà le point que beaucoup ratent : PairDrop a besoin d'être servi en HTTPS pour que certaines fonctions marchent correctement sur la plupart des navigateurs, notamment le copier-coller de texte, l'installation en PWA et l'appairage persistant. En HTTP simple, tu perds une partie du confort.

Config Caddy minimale à ajouter dans ton `Caddyfile` :

```caddy
drop.tondomaine.com {
    reverse_proxy pairdrop:3000 {
        header_up X-Forwarded-For {remote_host}
    }
}
```

⚠️ Ce header `X-Forwarded-For` n'est pas cosmétique. PairDrop l'utilise pour déterminer si deux appareils sont sur le même réseau local. Sans lui transmis correctement par le proxy, tous les clients qui passent par ta box se voient comme s'ils étaient tous sur le même LAN, même deux visiteurs qui n'ont rien à voir l'un avec l'autre.

Assure-toi que le conteneur PairDrop et Caddy partagent le même réseau Docker :

```yaml
networks:
  caddy:
    external: true
```

```yaml
services:
  pairdrop:
    # ... reste identique
    networks:
      - caddy
```

Si tu exposes PairDrop Docker plus largement qu'à ta famille, une couche d'authentification devant le reverse proxy n'est pas du luxe. Mon guide sur [Authelia Docker](/authelia-docker-authentification-2fa-homelab/) explique comment poser une double authentification centralisée devant n'importe quel service web, PairDrop y compris.

## Envoyer des fichiers hors réseau local : le serveur TURN

Tant que l'expéditeur et le destinataire sont sur le même réseau (même Wi-Fi, même LAN, ou même VPN mesh), WebRTC établit une connexion directe et le fichier ne transite jamais par ton serveur. Mais dès que les deux appareils sont sur des réseaux différents (ton téléphone en 4G, ton PC derrière une box différente), WebRTC a besoin d'un serveur TURN pour relayer la connexion.

Le dépôt officiel fournit un `docker-compose-coturn.yml` qui ajoute un service Coturn à côté de PairDrop, avec ses propres certificats TLS, un fichier de paramètres Diffie-Hellman et une plage de ports UDP/TCP dédiée (3478, 5349, et 10000-20000). C'est le prix à payer pour des transferts qui sortent du réseau local : un service supplémentaire à maintenir, avec ses propres certificats à renouveler.

Si tu ne veux pas gérer Coturn toi-même, des TURN publics comme OpenRelay existent en solution de secours, à renseigner via la variable `RTC_CONFIG`. Pour un usage familial ou une petite équipe qui reste la plupart du temps sur le même réseau, ça reste souvent plus simple de laisser PairDrop Docker fonctionner en pair à pair pur et de garder Coturn pour plus tard si le besoin se confirme.

## Cas d'usage concrets

### Remplacer AirDrop dans une famille mixte Apple/Android/Windows

Chez moi, il y a un iPhone, deux Android et un PC sous Windows. AirDrop natif ne parle qu'aux appareils Apple entre eux. PairDrop Docker, lui, s'en fiche complètement de la marque : tout le monde ouvre la même URL depuis son navigateur, tout le monde se voit, tout le monde s'envoie des photos de vacances sans passer par un groupe WhatsApp qui compresse tout.

### Transférer un fichier volumineux sans passer par le cloud

Un ISO Linux de 4 Go, une sauvegarde de config, une vidéo en 4K : plutôt que de les uploader sur un service tiers pour les retélécharger ensuite, PairDrop les envoie en direct entre deux machines sur le même réseau. Zéro upload externe, zéro limite de taille imposée par un service cloud.

### Dépanner un poste sans installer d'agent

Tu interviens sur un PC qui n'a ni Nextcloud ni client de synchro installé. Tu ouvres PairDrop Docker sur ton serveur depuis les deux navigateurs, tu glisses le fichier dont tu as besoin, et c'est réglé en trente secondes sans rien poser sur la machine du client. Si tu cherches plutôt un outil dédié au partage d'images avec génération de lien direct plutôt qu'un transfert éphémère entre deux appareils, j'ai aussi détaillé [Droppy sous Docker](/droppy-partage-images-auto-heberge/), plus adapté quand tu veux garder une copie accessible après coup.

## Dépannage rapide

**Les appareils ne se voient pas entre eux**

Vérifie d'abord qu'ils sont réellement sur le même réseau logique. Si PairDrop Docker tourne derrière un reverse proxy, c'est presque toujours le header `X-Forwarded-For` mal transmis qui est en cause : sans lui, le serveur ne peut pas distinguer les réseaux des clients.

**Le transfert démarre puis reste bloqué**

Passe `DEBUG_MODE=true` le temps du diagnostic, relance le conteneur et regarde les logs :

```bash
docker compose logs -f pairdrop
```

Les adresses IP des pairs apparaissent dans les logs, ce qui permet de vérifier si les deux appareils sont bien vus comme étant sur le même réseau par PairDrop. Repasse `DEBUG_MODE=false` une fois le souci identifié, ces logs n'ont rien à faire à traîner en permanence.

**Rien ne se charge, page blanche derrière le reverse proxy**

Vérifie que le certificat TLS est valide et que le proxy pointe bien vers le port interne 3000 du conteneur. Un souci de certificat expiré casse silencieusement certaines fonctions du navigateur (PWA, presse-papier) même si la page semble s'afficher normalement.

## Sauvegardes et mises à jour

Il n'y a rien à sauvegarder côté PairDrop lui-même : pas de base de données, pas de volume, pas de fichier utilisateur stocké sur le serveur puisque tout transite en direct entre navigateurs. Le seul fichier qui mérite d'être versionné, c'est ton `docker-compose.yml`.

Si en revanche tu comptes garder une copie des fichiers reçus après un transfert important, pense à sauvegarder le dossier de destination sur la machine qui les a reçus. Mon guide sur [Duplicati Docker](/duplicati-docker-sauvegarde/) couvre une stratégie de sauvegarde chiffrée simple à mettre en place à côté de ta stack.

Pour la mise à jour, rien d'original :

```bash
cd ~/pairdrop
docker compose pull
docker compose up -d
```

## Conclusion

PairDrop Docker fait une chose et la fait bien : transférer un fichier d'un appareil à un autre sans compte, sans appli, sans upload intermédiaire. Pas de base de données à sauvegarder, pas de volume à gérer, un conteneur qui démarre en quelques secondes.

Si tu t'arrêtes au réseau local, l'installation par défaut suffit largement. Si tu veux l'ouvrir plus largement, un reverse proxy en HTTPS avec le bon header et, éventuellement, un serveur TURN pour les transferts entre réseaux différents complètent le tableau. C'est exactement le genre d'outil discret qui remplace un mail à soi-même ou une clé USB perdue, sans jamais te demander de créer un compte.
