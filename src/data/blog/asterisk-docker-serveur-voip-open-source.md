---
title: "Asterisk Docker : serveur VoIP open-source complet"
description: "Asterisk Docker : build de l'image, trunk SIP, gestion du NAT et du RTP, sécurité contre le toll fraud pour un PBX VoIP auto-hébergé complet."
pubDatetime: "2026-10-20T11:02:11+02:00"
modDatetime: "2026-10-19T08:00:00.000Z"
author: Brandon
tags:
  - auto-hebergement
  - hardening
  - reverse-proxy
  - monitoring
  - avance
featured: false
draft: false
focusKeyword: asterisk docker
faqs:
  - question: "Faut-il un matériel VoIP spécifique pour faire tourner Asterisk dans Docker ?"
    answer: "Non. Un softphone (Zoiper, Linphone) ou un téléphone SIP classique suffit. Le matériel analogique (cartes FXO/FXS) reste la seule exception, et il demande un passthrough compliqué en conteneur."
  - question: "Comment gérer le NAT quand Asterisk tourne derrière un routeur domestique ?"
    answer: "En réglant external_media_address et external_signaling_address dans pjsip.conf, en ouvrant la plage RTP en UDP sur le routeur, et en évitant le mode bridge Docker pour ce service."
  - question: "Quelle est la différence entre Asterisk et FreePBX ?"
    answer: "Asterisk est le moteur, en ligne de commande et fichiers texte. FreePBX est une interface web qui pilote ce même moteur. Tu peux très bien rester sur Asterisk nu si tu es à l'aise avec la configuration."
---
> 💡 **TL;DR**
> - Asterisk est un PBX open-source complet (SIP, IAX, WebRTC, IVR), maintenu par Sangoma sous licence GPLv2
> - Pas d'image Asterisk Docker officielle : tu construis la tienne depuis les sources ou tu pars d'une image communautaire entretenue
> - Le vrai piège n'est pas l'installation mais le NAT et le flux RTP, à régler avant de brancher ton premier trunk SIP

## Asterisk Docker : le PBX open-source qui tient dans un conteneur

Asterisk, c'est le grand-père de la téléphonie open-source. Le projet existe depuis la fin des années 90, et il tourne encore aujourd'hui derrière une bonne partie des centraux téléphoniques du monde libre, des petites boîtes qui veulent sortir de leur contrat opérateur jusqu'aux call centers qui comptent leurs appels par milliers. Chez moi, c'est le genre de projet homelab qui a l'air intimidant au premier abord et qui, une fois le déclic NAT/RTP fait, devient presque banal à maintenir.

Lancer Asterisk dans Docker change la donne par rapport à une install sur bare metal : tu isoles tes dépendances, tu versionnes ta config, tu détruis et recrées le conteneur sans toucher à l'hôte. La contrepartie, c'est que la VoIP n'aime pas la virtualisation réseau légère, et c'est précisément le sujet qui fait dérailler la plupart des tutos Asterisk Docker trouvés en ligne. On va le traiter correctement.

## Table des matières

## Installer Asterisk avec Docker

Première chose à savoir : il n'existe pas d'image Asterisk Docker officielle estampillée Sangoma. Contrairement à beaucoup d'outils de ce blog, le projet ne publie pas de `Dockerfile` maintenu sur son propre dépôt. Tu as deux routes possibles pour monter ton propre Asterisk Docker.

**Construire ta propre image depuis les sources.** C'est la méthode que je recommande si tu veux maîtriser exactement ce qui tourne. Un `Dockerfile` minimal sur base Debian ressemble à ça :

```dockerfile
FROM debian:12-slim
ARG ASTERISK_BRANCH=20

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential wget subversion libxml2-dev libsqlite3-dev \
    libssl-dev libedit-dev uuid-dev pkg-config ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src
RUN wget -q https://downloads.asterisk.org/pub/telephony/asterisk/asterisk-${ASTERISK_BRANCH}-current.tar.gz \
    && tar xzf asterisk-${ASTERISK_BRANCH}-current.tar.gz \
    && cd asterisk-${ASTERISK_BRANCH}* \
    && contrib/scripts/install_prereq install \
    && ./configure \
    && make menuselect.makeopts \
    && make -j"$(nproc)" \
    && make install \
    && make samples \
    && make config

EXPOSE 5060/udp 5061/tcp 10000-20000/udp
CMD ["asterisk", "-f", "-vvv"]
```

**Partir d'une image communautaire entretenue.** Plusieurs mainteneurs publient des images à jour, basées sur Alpine ou Debian, avec un suivi régulier des versions. Vérifie juste la date du dernier build avant de t'y fier : le volume de projets abandonnés sur ce créneau est élevé.

Une fois l'image construite, le `docker-compose.yml` est le cœur du setup Asterisk Docker :

```yaml
services:
  asterisk:
    build: .
    container_name: asterisk
    restart: unless-stopped
    network_mode: host
    volumes:
      - ./config:/etc/asterisk
      - ./sounds:/var/lib/asterisk/sounds/custom
      - ./spool:/var/spool/asterisk
```

Remarque le `network_mode: host`. On y revient juste après, mais c'est la clé de voûte qui évite 90 % des galères signalées sur les forums.

Pour piloter ce service sans taper des commandes `docker compose` à chaque modif, j'ai basculé toute ma gestion de stacks sur [Dockge](/dockge-docker-gestionnaire-stacks-compose/) : interface web, édition du compose en direct, redéploiement en un clic. Ça change vraiment la vie sur un service aussi sensible aux redémarrages qu'un PBX.

## Configurer les trunks SIP et les extensions

Asterisk moderne pousse vers `pjsip.conf` plutôt que le vieux `chan_sip`, qui est officiellement retiré des branches récentes. Voici une extension locale minimale :

```ini
[6001]
type=endpoint
context=internal
disallow=all
allow=ulaw,alaw,opus
auth=auth6001
aors=6001

[auth6001]
type=auth
auth_type=userpass
username=6001
password=change-moi-vraiment

[6001]
type=aor
max_contacts=1
```

Et un trunk SIP générique vers un opérateur VoIP (adapte les identifiants à ton propre contrat) :

```ini
[trunk-operateur]
type=registration
outbound_auth=trunk-auth
client_uri=sip:ton_identifiant@sip.ton-operateur.exemple
server_uri=sip:sip.ton-operateur.exemple

[trunk-auth]
type=auth
auth_type=userpass
username=ton_identifiant
password=ton_mot_de_passe
```

Le dialplan dans `extensions.conf` relie les deux mondes, et c'est la pièce qui fait d'un Asterisk Docker un vrai PBX plutôt qu'une coquille vide. Un exemple simple qui route les appels sortants vers le trunk et les entrants vers une extension :

```ini
[internal]
exten => _X.,1,Dial(PJSIP/${EXTEN}@trunk-operateur)
exten => 6001,1,Dial(PJSIP/6001,20)
 same => n,Voicemail(6001@default)
```

⚠️ Ne laisse jamais un contexte `default` ou `internal` accepter des appels anonymes sans authentification. C'est la porte d'entrée numéro un du toll fraud, le sujet de la prochaine section.

## NAT et RTP : la vraie difficulté du VoIP en conteneur

Le signal SIP (qui négocie l'appel) et le flux RTP (qui transporte la voix) sont deux choses distinctes, et c'est cette distinction qui piège tout le monde. SIP passe bien à travers un NAT classique. RTP, lui, utilise une large plage de ports UDP dynamiques, et c'est exactement le genre de trafic que Docker en mode `bridge` gère mal : chaque flux demanderait un mapping de port dédié, ce qui n'est tout simplement pas prévu par le protocole.

La solution la plus fiable reste `network_mode: host` dans le compose, vu plus haut. Le conteneur partage directement la pile réseau de l'hôte, Asterisk voit les vraies interfaces, et tu n'as qu'une seule couche de NAT à gérer : celle de ton routeur, pas celle de Docker en plus. C'est le réglage réseau qui fait tenir un Asterisk Docker en production, pas un détail secondaire.

Dans `pjsip.conf`, section transport, indique explicitement tes adresses publique et privée :

```ini
[transport-udp]
type=transport
protocol=udp
bind=0.0.0.0:5060
external_media_address=203.0.113.10
external_signaling_address=203.0.113.10
local_net=192.168.1.0/24
```

Et dans `rtp.conf`, borne la plage de ports RTP à quelque chose de raisonnable (10000-10200 suffit largement pour un usage personnel) et ouvre cette même plage en UDP sur ton routeur :

```ini
[general]
rtpstart=10000
rtpend=10200
```

💡 Si ton FAI te fournit une IP publique dynamique ou si tu es derrière un double NAT (CGNAT), un tunnel comme Tailscale ou WireGuard entre ton PBX et tes softphones distants t'évite complètement le casse-tête RTP/NAT public. C'est souvent plus simple qu'une ouverture de ports agressive.

## Sécuriser ton PBX contre le toll fraud

Un Asterisk Docker mal protégé exposé sur internet se fait scanner en quelques heures. Le but des attaquants n'est pas de t'espionner, c'est de revendre tes minutes d'appels vers des numéros surtaxés à l'étranger. La facture peut tomber en quelques jours si personne ne surveille.

✅ Checklist minimale avant d'ouvrir le port 5060 vers l'extérieur :

- Mots de passe SIP longs et aléatoires, jamais de défaut genre `1234`
- `allowguest=no` partout où ça s'applique, aucun contexte anonyme
- `fail2ban` avec un jail Asterisk qui bannit après quelques tentatives échouées (le pattern de log est bien documenté dans la communauté fail2ban)
- Restriction des destinations internationales et des numéros surtaxés dans le dialplan sortant
- Si possible, un tunnel VPN plutôt qu'une exposition SIP directe pour les postes distants

Côté réseau, un reverse proxy TLS devant l'interface web d'administration (si tu en ajoutes une par la suite, type FreePBX) te protège des scans automatisés qui ciblent les panneaux d'admin exposés en clair. Le SIP lui-même profite aussi du chiffrement : `pjsip.conf` supporte `transport=tls` et le média peut passer en SRTP, mais ça complique sensiblement le NAT traversal vu plus haut, donc réserve ça aux déploiements qui en ont vraiment besoin.

## Monitoring, logs et sauvegarde

Superviser un Asterisk Docker en production ne demande pas d'outils compliqués. Asterisk expose déjà une CLI interactive très complète : `asterisk -rvvv` depuis le conteneur te donne une console live avec tous les événements SIP et dialplan en temps réel. Pratique pour déboguer un appel qui ne passe pas, moins pratique pour une surveillance continue.

Pour ça, je passe par [Dozzle](/dozzle-docker-visionneuse-logs-web/), qui agrège les logs du conteneur Asterisk dans une interface web sans rien configurer de plus. Les erreurs d'authentification SIP répétées, les tentatives de brute force, les enregistrements de trunk qui échouent, tout remonte lisiblement.

Les enregistrements d'appels (si tu actives `MixMonitor` dans le dialplan) et les exports CDR s'accumulent vite en fichiers. J'utilise [Filestash](/filestash-docker-navigateur-fichiers-web/) pour parcourir ces dossiers de voicemail et d'enregistrements depuis un navigateur, sans monter de partage réseau sur chaque poste. Et pour archiver proprement les factures d'opérateur VoIP ou les exports CDR mensuels en PDF, je les fais atterrir dans [Paperless-ngx](/paperless-ngx-docker-guide-auto-hebergement/), qui les indexe et les retrouve par simple recherche plein texte des mois plus tard.

Côté sauvegarde, le réflexe habituel Docker s'applique : seuls `./config`, `./sounds` et `./spool` comptent vraiment, le reste se reconstruit depuis le `Dockerfile`. Une archive régulière de ces trois dossiers suffit à restaurer un PBX complet sur une autre machine.

## Conclusion

Asterisk Docker demande un peu plus de rigueur qu'un simple `docker run` sur une appli web classique, mais rien d'insurmontable une fois que le trio installation, NAT/RTP et sécurité est posé dans cet ordre. Si tu veux une interface web complète par-dessus ce moteur, FreePBX reste la référence, construite directement sur Asterisk et maintenue par la même entreprise. Rien ne t'empêche cependant de rester sur la configuration texte si tu es à l'aise avec `pjsip.conf` et `extensions.conf`, c'est même plus simple à versionner dans un dépôt git.

Le gain réel, une fois le PBX stable : plus de contrat opérateur imposé, un routage d'appels entièrement sous ton contrôle, et un Asterisk Docker qui tient sur un conteneur parmi les autres de ton homelab.
