---
title: "Audiobookshelf Docker : serveur de livres audio et podcasts auto-hébergé"
description: "Audiobookshelf Docker : déploie ton serveur de livres audio et podcasts avec Compose, les bons volumes et une mise à jour sans perte de données."
pubDatetime: "2026-10-07T11:02:11+02:00"
modDatetime: "2026-10-06T08:00:00.000Z"
author: Brandon
tags:
  - auto-hebergement
  - mediacenter
  - multimedia
  - intermediaire
featured: false
draft: false
focusKeyword: audiobookshelf docker
faqs:
  - question: "Ça consomme combien de RAM et de CPU ?"
    answer: "La doc officielle ne donne aucun chiffre, donc je ne t'en invente pas. Lance docker stats pendant une écoute et une analyse de bibliothèque : tu auras la vraie valeur pour ta machine."
  - question: "Puis-je mettre le dossier /config sur un partage NFS ou SMB ?"
    answer: "La doc officielle le déconseille, car la base est en SQLite et les écritures sur réseau peuvent la corrompre. Garde /config sur un disque local et laisse seulement les médias sur le partage réseau."
  - question: "Vais-je perdre ma bibliothèque en mettant à jour le conteneur ?"
    answer: "Non, tant que tu gardes les volumes. Les utilisateurs et réglages sont dans /config, les métadonnées dans /metadata. Un docker compose pull suivi de down et up ne touche qu'à l'image."
---
> 💡 **TL;DR**
> - Audiobookshelf est un serveur auto-hébergé pour livres audio et podcasts, avec interface web et applis mobiles
> - Le déploiement tient dans un fichier Compose : l'image `ghcr.io/advplyr/audiobookshelf` et quatre volumes (`/config`, `/metadata`, `/audiobooks`, `/podcasts`)
> - La mise à jour se fait en trois commandes, et tant que les volumes sont en place, rien ne se perd

Tes livres audio traînent sur un disque USB, tes podcasts dans une appli qui les range à sa façon, et ta progression ne suit jamais d'un appareil à l'autre. Un petit serveur chez toi règle tout ça. Avec Audiobookshelf Docker, tu déploies en quelques minutes une bibliothèque qui t'appartient, sans dépendre d'un abonnement.

## Table des matières

## Ce qu'Audiobookshelf fait (et ce qu'il ne fait pas)

Audiobookshelf est un projet open source, développé par advplyr et publié sur GitHub. Il gère deux familles de contenus : les livres audio, rangés en bibliothèques, et les podcasts, avec leurs abonnements. Il garde la trace de ta progression par livre et par épisode, et propose des applis mobiles pour écouter hors ligne.

Il ne télécharge pas les livres à ta place et ce n'est pas un gestionnaire de fichiers. Tu déposes tes fichiers dans un dossier, il les indexe, il récupère les pochettes et les métadonnées, et il te sert le flux. Cette séparation des rôles est justement ce qui le rend simple à maintenir.

Pour la partie conteneurs, audiobookshelf docker est le chemin le plus propre. L'image officielle est publiée sur le registre GitHub, et tout le paramétrage passe par quatre volumes et un port. Pas besoin d'installer Node ni une base de données à côté. Avec un audiobookshelf docker bien monté, l'hôte ne porte que tes médias et tes dossiers de données, le logiciel reste dans l'image.

## Audiobookshelf Docker : le fichier Compose

L'image à utiliser est `ghcr.io/advplyr/audiobookshelf`. À l'intérieur du conteneur, l'application écoute sur le port 80. La doc officielle publie l'exemple sur le port 13378 de l'hôte, je garde la même convention. Voilà le fichier de départ, à adapter à tes chemins :

```yaml
services:
  audiobookshelf:
    image: ghcr.io/advplyr/audiobookshelf:latest
    container_name: audiobookshelf
    ports:
      - 13378:80
    volumes:
      - /srv/audiobookshelf/config:/config
      - /srv/audiobookshelf/metadata:/metadata
      - /srv/audiobookshelf/audiobooks:/audiobooks
      - /srv/audiobookshelf/podcasts:/podcasts
    environment:
      - TZ=Europe/Paris
    restart: unless-stopped
```

Crée les dossiers, puis lance le conteneur depuis le répertoire qui contient le fichier :

```bash
mkdir -p /srv/audiobookshelf/{config,metadata,audiobooks,podcasts}
docker compose up -d
```

Ouvre ensuite `http://IP_DE_TA_MACHINE:13378` dans ton navigateur. Le premier passage te demande de créer le compte administrateur. C'est tout pour le démarrage.

Pour l'écoute hors de chez toi, évite d'ouvrir le port 13378 directement sur ta box. Un VPN vers ton réseau ou un reverse proxy avec authentification reste la voie propre, et les applis mobiles fonctionnent très bien derrière l'un ou l'autre.

Si tu préfères une commande unique sans Compose, la doc propose aussi un `docker run` avec les mêmes quatre `-v` et le `-e TZ=...`. Le résultat est identique, mais le fichier Compose se versionne et se relance plus facilement.

## Les volumes : ce qui va où

Dans un audiobookshelf docker, les quatre volumes ne jouent pas le même rôle, et c'est là que la plupart des installations se trompent :

- `/config` contient la base SQLite (utilisateurs, bibliothèques, réglages) et les scripts de migration. C'est le cœur du service.
- `/metadata` regroupe les métadonnées, les images de couverture, le cache, les logs et les sauvegardes que l'application génère elle-même.
- `/audiobooks` et `/podcasts` sont les points d'entrée vers tes médias. Tu remplaces les chemins de gauche par tes vrais dossiers, et ceux de droite ne changent jamais.

Règle à retenir : les quatre dossiers doivent être séparés et ne jamais s'imbriquer. Un `/srv/audiobookshelf/config` qui contient aussi tes audiobooks rendra la suite pénible. Et `/config` reste sur un disque local, pour la raison donnée plus haut sur SQLite.

## Premier démarrage et bibliothèques

Une fois connecté à ton audiobookshelf docker, crée une bibliothèque par type de contenu. Une bibliothèque « livres audio » pointe sur `/audiobooks`, une bibliothèque « podcasts » sur `/podcasts`. Chaque bibliothèque se gère séparément, ce qui évite de mélanger un roman lu en dix heures avec un épisode de vingt minutes.

Pour les livres, une arborescence `Auteur/Titre` fonctionne bien. Les séries se rangent en sous-dossier de l'auteur. Ça n'a rien de magique, mais ça rend l'indexation prévisible et ça t'évite de corriger les métadonnées à la main pendant des semaines.

Pour les podcasts, tu ajoutes l'URL du flux RSS directement dans l'interface, comme tu le ferais dans un [lecteur RSS](/freshrss-docker-lecteur-rss/). Audiobookshelf télécharge ensuite les épisodes dans `/podcasts`.

## Mise à jour et sauvegarde

Les données vivent dans les volumes, donc le conteneur est jetable. Mettre à jour ton audiobookshelf docker se fait en trois commandes. Tu ne reconstruis rien : tu récupères l'image publiée, puis tu relances le service avec les mêmes volumes. À lancer dans le dossier du fichier Compose :

```bash
docker compose pull
docker compose down
docker compose up --detach
```

Trois tags sont disponibles. `:latest` correspond à la dernière version stable, `:edge` est reconstruit à chaque commit et sert aux tests, et `:X.Y.Z` épingle une version précise. Pour un serveur qui doit rester stable, je te conseille de figer la version et de la monter à la main après lecture des notes de release sur GitHub.

Côté sauvegarde, la doc officielle ne décrit pas de procédure dédiée. L'application écrit ses propres sauvegardes dans `/metadata`, mais je te conseille aussi une copie du dossier `/config` prise pendant que le conteneur est arrêté, pour éviter de copier une base SQLite en pleine écriture :

```bash
docker compose down
tar czf abs-config-$(date +%F).tgz -C /srv/audiobookshelf config
docker compose up --detach
```

Ces trois lignes ne coûtent rien et te sauvent le jour où tu casses un réglage en pensant bien faire.

## Dépannage : les pièges classiques

Ton audiobookshelf docker tourne mais la page ne répond pas. Vérifie le sens du mapping : c'est `13378:80`, port de l'hôte à gauche, port du conteneur à droite. L'inversion est l'erreur la plus courante.

Les livres n'apparaissent pas dans la bibliothèque. Le chemin à renseigner dans l'interface est celui du conteneur, `/audiobooks`, pas ton chemin hôte. Vérifie ce que voit le conteneur avec `docker exec audiobookshelf ls /audiobooks`. Si le dossier est vide, le problème vient du volume, pas de l'application.

Les fichiers sont là mais illisibles. Le conteneur doit pouvoir lire tes dossiers médias. Un `ls -l` sur l'hôte te dit vite si les droits bloquent. Un `chown` ciblé règle le cas, pas besoin de passer tout le dossier en 777.

Les épisodes de podcast ne se téléchargent pas. Le conteneur doit pouvoir écrire dans `/podcasts`. Sans droit d'écriture sur le dossier hôte, le téléchargement reste bloqué sans message évident, donc vérifie les droits avant de chercher ailleurs.

Les dates de lecture sont décalées. C'est la variable `TZ` qui manque ou qui est fausse. Mets ton fuseau réel dans le fichier Compose et relance.

Pour suivre les logs en direct sans te connecter en SSH, [Dozzle](/dozzle-docker-visionneuse-logs-web/) fait le travail depuis le navigateur. Si tu préfères cliquer plutôt que taper des commandes, [Portainer](/portainer-docker-interface-web-conteneurs/) gère le conteneur, les volumes et les redémarrages depuis une interface web.

## Audiobookshelf ou Plex pour les livres audio ?

Plex est pensé autour de la vidéo et de la musique. Tu peux détourner une bibliothèque musicale pour y ranger des livres, mais tu te bats ensuite avec les métadonnées et la reprise de lecture. Audiobookshelf part du problème inverse : tout son modèle tourne autour des livres audio et des podcasts, avec la progression comme fonctionnalité centrale.

Si tu as déjà Plex pour tes films, garde-le et installe Audiobookshelf à côté. Les deux serveurs n'ont aucune raison de se marcher dessus, et chacun fait ce pour quoi il a été conçu.

## Conclusion

Un audiobookshelf docker piloté par un fichier Compose, quatre dossiers bien séparés et une mise à jour en trois commandes suffisent pour avoir ta bibliothèque audio chez toi. Le reste, c'est de l'organisation : une arborescence propre, un fuseau horaire correct et une copie de `/config` de temps en temps.

Si tu construis déjà un homelab, Audiobookshelf s'intègre sans friction avec le reste de ta pile Docker. Lance-le, écoute un premier livre, et reviens me dire si tu t'en passes encore.
