---
title: "Pi-hole v6 Docker : bloqueur de pubs pour tout ton réseau"
description: "Déploie Pi-hole v6 en Docker pour bloquer les pubs et trackers sur tout ton réseau : configuration DNS, DHCP et migration depuis la v5."
pubDatetime: "2026-11-11T11:01:06+01:00"
modDatetime: "2026-11-10T08:00:00.000Z"
author: Brandon
tags:
  - reseau
  - docker
  - dns
  - intermediaire
featured: false
draft: false
focusKeyword: pi-hole v6
faqs:
  - question: "Pi-hole v6 en Docker consomme combien de ressources ?"
    answer: "Très peu : prévois quelques dizaines de mégaoctets de RAM et une fraction de cœur CPU au repos, largement moins qu'une VM dédiée ou qu'un routeur du commerce."
  - question: "Que se passe-t-il si mon conteneur Pi-hole tombe, plus personne n'a de DNS ?"
    answer: "C'est le vrai risque d'un DNS centralisé sur un seul conteneur. Garde un résolveur de secours côté DHCP, ou déploie une deuxième instance Pi-hole v6 synchronisée avec Nebula-Sync pour ne jamais te retrouver sans résolution."
  - question: "Je viens de la v5, mes listes de blocage et mes réglages vont-ils survivre à la migration vers Pi-hole v6 ?"
    answer: "Oui, la base gravity et l'historique sont conservés lors de la mise à jour. Vérifie seulement tes variables d'environnement : les anciennes clés v5 sont ignorées par le conteneur v6, qui attend désormais les clés FTLCONF_*."
---
> 💡 **TL;DR**
> - Pi-hole v6 bloque pubs, trackers et télémétrie au niveau DNS, pour tous les appareils du réseau, sans extension à installer sur chacun
> - La v6 change l'interface d'admin, le format de config (TOML) et les variables d'environnement Docker, qui passent toutes en `FTLCONF_*`
> - Un seul conteneur suffit pour démarrer, mais un vrai réseau mérite un résolveur récursif en amont et une deuxième instance synchronisée

## Pi-hole v6 Docker : le bloqueur de pubs qui protège tout ton réseau

Installer un bloqueur de pubs sur chaque navigateur, chaque téléphone, chaque appareil qui traîne chez toi, c'est un combat perdu d'avance. Ta smart TV n'a pas d'extension. Ton frigo connecté non plus. Et ton ado qui passe par le 4G du voisin dès que tu as le dos tourné, encore moins.

La vraie question c'est : pourquoi bloquer la pub 50 fois, une par appareil, quand tu peux le faire une fois, au niveau du réseau ? C'est exactement ce que fait Pi-hole v6. Il s'installe comme résolveur DNS pour tout ton LAN et refuse de répondre aux domaines connus pour servir de la pub ou du tracking. Le reste du trafic continue normalement, sans rien à configurer côté client.

Chez moi, c'est la première brique que je pose sur un nouveau réseau, avant même le reverse proxy. Et depuis la v6, sortie en 2026, le projet a pris un vrai coup de jeune : interface repensée, configuration centralisée, conteneur Docker beaucoup plus simple à maintenir qu'avant.

## Table des matières

## Pi-hole v6 : ce qui change par rapport à la v5

Pi-hole v6 n'est pas une mise à jour cosmétique. C'est une réécriture du cœur du projet, FTL, qui embarque maintenant son propre serveur web à la place de l'ancienne interface PHP servie par lighttpd. Concrètement, pour toi qui déploies en Docker, ça change plusieurs habitudes :

- **Un seul fichier de configuration** au format TOML (`/etc/pihole/pihole.toml`), qui remplace la pile de fichiers dnsmasq éparpillés dans `/etc/dnsmasq.d/`
- **Des variables d'environnement renommées** : toutes les anciennes clés `WEBPASSWORD`, `DNSMASQ_LISTENING` et compagnie disparaissent au profit de clés `FTLCONF_<section>_<option>`, qui collent directement aux chemins du nouveau fichier TOML
- **Un mot de passe d'API** à la place du mot de passe web classique, défini via `FTLCONF_webserver_api_password`
- **Un port 443 actif par défaut**, avec un certificat auto-signé généré par FTL, pour chiffrer l'accès à l'interface
- **Un Teleporter revu**, toujours là pour exporter/importer ta config en un clic, mais dans un format d'archive différent de la v5

Si tu arrives d'une v5, bonne nouvelle : la base gravity (tes listes de blocage, ton historique de requêtes) survit à la mise à jour. Mauvaise nouvelle : si tu avais bricolé des variables d'environnement v5 dans ton `docker-compose.yml`, elles sont silencieusement ignorées. Pi-hole v6 démarre quand même, juste pas avec les réglages que tu croyais avoir.

## Installer Pi-hole v6 avec Docker Compose

Avant de lancer quoi que ce soit, vérifie que le port 53 est libre sur ton hôte. Sur beaucoup de distributions, `systemd-resolved` l'occupe déjà en local. Si c'est ton cas, désactive son stub listener avant de continuer, sinon le conteneur refusera de démarrer.

Voici un `docker-compose.yml` minimal pour Pi-hole v6, repris de la documentation officielle :

```yaml
services:
  pihole:
    container_name: pihole
    image: pihole/pihole:latest
    ports:
      - "53:53/tcp"
      - "53:53/udp"
      - "80:80/tcp"
      - "443:443/tcp"
      #- "67:67/udp"    # DHCP, seulement si Pi-hole gère le DHCP
      #- "123:123/udp"  # NTP, seulement si Pi-hole fait aussi serveur de temps
    environment:
      TZ: "Europe/Paris"
      FTLCONF_webserver_api_password: "change-moi"
      FTLCONF_dns_listeningMode: "ALL"
    volumes:
      - "./etc-pihole:/etc/pihole"
    cap_add:
      - NET_ADMIN   # utile seulement si Pi-hole sert aussi le DHCP
      - SYS_TIME    # idem pour le NTP
    restart: unless-stopped
```

Quelques points qui méritent une explication :

- `FTLCONF_dns_listeningMode: "ALL"` est nécessaire tant que tu restes en réseau Docker `bridge` par défaut. Sans ça, FTL n'écoute que sur l'interface locale et ignore les requêtes venues du reste de ton LAN, ce qui rend tout le reste de cette page inutile.
- Le volume `./etc-pihole:/etc/pihole` est le seul vraiment indispensable. C'est là que vivent ta base gravity, ton fichier `pihole.toml` et tes certificats auto-signés. Perds-le et tu repars de zéro.
- `cap_add` ne sert que si tu veux que Pi-hole gère en plus le DHCP (`NET_ADMIN`) ou se comporte comme client NTP pour régler l'heure de l'hôte (`SYS_TIME`). Si tu as déjà un serveur de temps dédié à côté, comme [Chrony Docker](/chrony-docker-serveur-ntp-homelab/), laisse ces lignes commentées : pas besoin d'empiler les responsabilités sur le même conteneur.

Lance `docker compose up -d`, laisse le conteneur démarrer, puis va chercher le mot de passe admin si tu n'en as pas défini un toi-même : il est généré aléatoirement au premier démarrage et affiché une seule fois dans les logs du conteneur. Rends-toi ensuite sur `https://<ip-de-ton-hote>/admin` pour mettre les mains sur l'interface.

⚠️ **Le certificat est auto-signé.** Ton navigateur va hurler au premier accès. C'est normal, c'est FTL qui le génère lui-même pour chiffrer la connexion locale, pas une alerte de sécurité à prendre au sérieux sur un réseau que tu contrôles.

## Configurer le DNS sur tout ton réseau

Un Pi-hole v6 qui tourne tout seul sur son conteneur ne sert à rien si personne ne l'interroge. Deux façons de brancher le reste de ton réseau dessus.

La première, la plus simple : va dans les réglages DHCP de ta box ou de ton routeur, et remplace le DNS poussé aux clients par l'IP de ton hôte Docker. Chaque appareil qui obtient une adresse continue de passer par le DHCP habituel, mais reçoit désormais Pi-hole comme résolveur. Zéro changement côté clients, et tu gardes ton routeur comme serveur DHCP.

La deuxième, plus radicale : laisser Pi-hole v6 lui-même distribuer les baux DHCP. Ça implique de désactiver le DHCP du routeur, d'ajouter la capacité `NET_ADMIN` vue plus haut, et bien souvent de passer le conteneur en `network_mode: host`, parce que le trafic DHCP broadcast se comporte mal derrière un bridge Docker classique. C'est plus de contrôle (attribution de noms d'hôtes visibles dans l'interface, réservations statiques), mais aussi un point de panne de plus si tu rates la bascule.

Une fois le DNS branché, direction l'onglet **Group Management > Adlists** de l'interface. Pi-hole v6 arrive avec une liste de blocage par défaut, mais rien ne t'empêche d'en ajouter d'autres, orientées trackers, malware ou pub mobile. Le bouton **Update Gravity** télécharge et compile toutes les listes actives en une seule base utilisée par FTL. Pense aussi aux listes blanches : certains sites cassent visuellement si tu bloques trop large, et un domaine remis en liste blanche vaut mieux qu'un Pi-hole qu'on désactive par flemme.

## Aller plus loin : résolution récursive et synchronisation

Pi-hole v6 n'est pas un résolveur DNS au sens strict. Par défaut, il relaie simplement les requêtes non bloquées vers des DNS publics configurés dans ses réglages, exactement comme le ferait n'importe quel routeur. Si tu veux pousser la souveraineté réseau plus loin et arrêter de dépendre d'un tiers pour la résolution elle-même, associe Pi-hole v6 à [Unbound Docker DNS récursif auto-hébergé et performant](/unbound-docker-dns-recursif/). Le principe reste simple : Pi-hole filtre, Unbound résout en interrogeant lui-même les serveurs racine. Tu gagnes en plus la validation DNSSEC au passage.

Le deuxième chantier, c'est la résilience. Un seul Pi-hole v6, c'est un seul point de panne pour tout ton DNS. Dès que tu as deux appareils capables d'héberger un conteneur, l'option la plus propre est de faire tourner une deuxième instance Pi-hole v6 et de les garder synchronisées automatiquement avec [Nebula-Sync : synchronise tes Pi-hole v6 automatiquement (remplace Gravity Sync)](/nebula-sync-pihole-v6-installation-docker-guide/). Tes listes de blocage, tes réglages et tes groupes restent identiques sur les deux nœuds, sans script maison à entretenir.

✅ **Backup avant toute montée de version majeure.** Passe par le Teleporter (onglet Settings) pour exporter ta config avant une mise à jour d'image. Ça prend dix secondes et ça t'évite de tout reconfigurer à la main si quelque chose tourne mal.

## Pièges classiques et dépannage

Quelques galères qui reviennent souvent avec Pi-hole v6 en Docker, et leur sortie :

- **Le conteneur refuse de démarrer, port 53 déjà utilisé.** `systemd-resolved` écoute en local sur la plupart des distributions Linux récentes. Désactive son stub listener (`DNSStubListener=no` dans sa config, puis redémarre le service) avant de relancer le conteneur.
- **L'interface répond mais le blocage ne fait rien.** Vérifie que tes appareils interrogent vraiment Pi-hole : un client qui a mis en cache une ancienne réponse DNS, ou qui a un DNS secondaire public configuré en dur, continuera de passer à côté du filtre. Un `dig` depuis la machine concernée confirme en deux secondes qui répond réellement.
- **Les anciennes variables d'environnement n'ont plus aucun effet.** C'est le piège classique de la migration v5 vers v6 : `WEBPASSWORD` et consorts ne font plus rien, remplacées par les clés `FTLCONF_*`. Pi-hole démarre sans broncher, avec des valeurs par défaut que tu n'avais pas prévues.
- **Le DHCP ne distribue rien une fois activé dans Pi-hole.** Signe quasi certain que le conteneur tourne encore derrière un bridge Docker standard. Repasse en `network_mode: host`, ou accepte de garder le DHCP sur ton routeur et de ne confier que la résolution DNS à Pi-hole.

Une fois tout ça stabilisé, pense à la supervision de la brique elle-même : [SNMPd Docker : monitorer ton réseau simplement](/snmpd-docker-monitorer-reseau/) te permet de garder un œil sur la charge et la dispo du conteneur, histoire de ne pas découvrir une panne de Pi-hole v6 seulement quand plus personne n'arrive à charger la moindre page.

## Conclusion

Pi-hole v6 reste exactement ce qu'il a toujours été : la brique la plus rentable d'un homelab, un bloqueur de pubs réseau qui protège tous tes appareils d'un coup, sans extension, sans config côté client. La v6 ajoute une interface plus propre et une configuration plus cohérente, au prix d'une petite friction si tu migres depuis une v5 avec des variables d'environnement qui datent.

Pars sur l'installation Docker Compose du jour, branche-le sur ton DHCP, laisse Gravity tourner une fois, et donne-lui quelques jours avant de juger. C'est après une semaine d'usage normal, pas après dix minutes de test, que tu mesures vraiment ce que Pi-hole v6 retire de ton trafic réseau.
