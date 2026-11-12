---
title: "Immich-go : migrer Google Photos vers Immich sans rien perdre"
description: "Migre tes photos Google Photos vers Immich avec immich-go, l'outil en ligne de commande qui garde albums et métadonnées intacts."
pubDatetime: "2026-11-05T11:01:44+01:00"
modDatetime: "2026-11-04T08:00:00.000Z"
author: Brandon
tags:
  - auto-hebergement
  - multimedia
  - stockage
  - sauvegarde
  - intermediaire
featured: false
draft: false
focusKeyword: immich-go
faqs:
  - question: "Immich-go supprime-t-il mes photos de Google Photos après la migration ?"
    answer: "Non. Immich-go ne touche jamais ton compte Google, il lit uniquement l'archive Takeout que tu as téléchargée en local. Tu gardes Google Photos intact en parallèle jusqu'à ce que tu sois sûr de ta migration."
  - question: "Combien de temps prend l'import de plusieurs dizaines de milliers de photos ?"
    answer: "Ça dépend surtout de la puissance du serveur Immich et de la génération des miniatures côté serveur. Compte plusieurs heures pour une grosse bibliothèque, lance l'import dans un tmux ou screen pour ne pas tout perdre si ta connexion coupe."
  - question: "Que se passe-t-il si l'import est interrompu en cours de route ?"
    answer: "Relance exactement la même commande. Immich-go calcule une somme de contrôle par fichier et ignore tout ce qui est déjà présent sur le serveur, donc aucun risque de doublon ni de repartir de zéro."
---
> 💡 **TL;DR**
> - immich-go est l'outil en ligne de commande qui importe un export Google Takeout dans Immich, albums et métadonnées compris
> - Pas de Docker ni de Node requis : un seul binaire, disponible pour Linux, macOS, Windows et FreeBSD
> - Gratuit et open source (licence AGPL-3.0), avec une détection de doublons par somme de contrôle qui rend les reprises d'import sans risque

## Immich-go : la passerelle entre Google Takeout et Immich

Tu as installé Immich sur ton serveur, tu as goûté à l'auto-hébergement, et maintenant tu te retrouves avec le vrai problème : comment tu sors concrètement tes photos de Google Photos ? Glisser-déposer 40 000 fichiers un par un n'est pas une option, et l'export Takeout de Google ne parle pas nativement le format d'Immich.

C'est exactement le trou que comble **immich-go**. Ce n'est pas une fonctionnalité native d'Immich, c'est un projet tiers distinct, maintenu par la communauté sur GitHub (compte `simulot`), mais c'est devenu l'outil de référence que la documentation officielle d'Immich elle-même recommande pour ce cas précis. Son rôle est simple : il lit tes archives Takeout, retrouve les métadonnées JSON associées à chaque photo, reconstruit les albums, et envoie tout ça vers ton instance Immich via son API.

Ce guide couvre l'export depuis Google, l'installation d'immich-go, la commande de migration, et les pièges qui font perdre une soirée si on ne les voit pas venir.

## Table des matières

## Pourquoi migrer de Google Photos vers Immich

Le calcul économique est connu : au-delà du quota gratuit, Google facture le stockage photo au mois, et la facture grimpe vite dès que tu dépasses quelques dizaines de milliers de clichés en haute résolution. Tu paies pour stocker tes propres souvenirs, et en prime Google analyse tes métadonnées GPS, reconnaît les visages, et classe tout ça pour nourrir ses propres modèles.

Immich fait le travail inverse. Reconnaissance faciale locale, recherche par contenu, carte géographique, tout tourne sur ton matériel. Si tu as déjà remplacé Google Drive par [Paperless-ngx](/paperless-ngx-docker-guide-auto-hebergement/) pour tes documents scannés, Google Photos est souvent la dernière pièce du puzzle qui te retient encore chez Google.

La contrainte, c'est que Google ne propose aucune API de synchronisation directe vers un service tiers. Le seul chemin officiel, c'est l'export Takeout, un gros paquet d'archives zip qu'il faut ensuite réinjecter manuellement. C'est précisément ce que fait immich-go, sans te demander de trier un seul fichier à la main.

## Exporter tes photos avec Google Takeout

Rends-toi sur `takeout.google.com` avec le compte Google concerné. Clique sur "Tout désélectionner", puis coche uniquement **Google Photos**. Tenter d'exporter tout ton compte Google d'un coup multiplie la taille de l'archive et le temps de préparation pour rien.

Choisis le format `.zip` plutôt que `.tgz` : c'est le format qu'immich-go lit nativement, alors que les archives `.tgz` doivent d'abord être décompressées à la main avant de pouvoir être traitées. Google te laisse aussi choisir la taille maximale de chaque morceau d'archive. Peu importe la valeur retenue, l'essentiel est de garder toutes les archives générées dans le même dossier au moment de l'import : immich-go reconstruit la bibliothèque complète à partir de l'ensemble des morceaux, et une archive manquante se traduit directement par des photos absentes à l'arrivée.

Google prévient par mail quand l'archive est prête, en général après quelques heures pour une bibliothèque de taille moyenne, et parfois plus d'une journée pour plusieurs dizaines de milliers de photos. Télécharge tous les morceaux avant de lancer quoi que ce soit, les liens de téléchargement de Google expirent après quelques jours.

## Installer immich-go

Pas de conteneur à builder, pas de dépendance Node ou Python à gérer : immich-go se distribue sous forme d'un binaire précompilé, téléchargeable depuis la page Releases du projet sur GitHub, avec des builds pour Linux, macOS, Windows et FreeBSD. Si tu pilotes déjà la stack Immich via [Dockge](/dockge-docker-gestionnaire-stacks-compose/), sache qu'immich-go n'a pas sa place dans ce `docker-compose.yml` : il tourne directement en ligne de commande sur la machine depuis laquelle tu lances l'import, qu'il s'agisse de ton poste ou du serveur lui-même.

Récupère l'archive correspondant à ton système, puis installe le binaire dans ton PATH :

```bash
tar -xzf immich-go_*.tar.gz
chmod +x immich-go
sudo mv immich-go /usr/local/bin/
```

Vérifie que l'installation a fonctionné et liste les commandes disponibles :

```bash
immich-go --help
```

⚠️ Le projet se présente lui-même comme une version jeune, pas encore testée à grande échelle sur tous les cas d'usage. Ça ne veut pas dire qu'il est instable au quotidien, mais ça justifie de garder une copie de tes archives Takeout tant que tu n'as pas vérifié l'import de bout en bout dans Immich.

## Migrer vers Immich avec immich-go

Avant de lancer quoi que ce soit, génère une clé API dans Immich : connecte-toi à l'interface web, va dans les paramètres de ton compte, section clés API, et crée-en une nouvelle dédiée à cette migration. Garde-la de côté, tu ne la reverras plus en clair une fois la fenêtre fermée.

La commande de base ressemble à ça :

```bash
immich-go upload from-google-photos \
  --server=http://IP_DU_SERVEUR:2283 \
  --api-key=TA_CLE_API \
  /chemin/vers/takeout-*.zip
```

Le dernier argument peut pointer vers un dossier entier contenant toutes les archives, immich-go les détecte automatiquement et les traite comme un seul export cohérent. Pendant l'import, l'outil retrouve pour chaque photo son fichier JSON de métadonnées associé (date de prise de vue, position GPS, titre) et reconstitue les albums tels qu'ils existaient dans Google Photos.

Pour une grosse bibliothèque, lance la commande dans une session `tmux` ou `screen` plutôt que dans un terminal classique. Si ta connexion SSH coupe en plein import de dizaines de milliers de fichiers, tu ne veux pas avoir à tout relancer depuis le début. Si certains fichiers parasites viennent polluer l'export (miniatures, fichiers système cachés dans l'archive), la commande propose un flag `--ban-file` pour les exclure explicitement par motif de nom.

## Vérifier l'import et gérer les doublons

Une fois l'import terminé, immich-go affiche un résumé : nombre de fichiers traités, nombre importés, nombre ignorés. Compare ce total au nombre de photos et vidéos indiqué par Google dans ton espace de stockage avant l'export. Un écart important signale souvent une archive manquante ou corrompue plutôt qu'un vrai problème côté Immich.

La détection de doublons repose sur une somme de contrôle calculée sur chaque fichier, pas sur le nom. Deux photos identiques présentes dans plusieurs albums Google Photos ne sont envoyées qu'une seule fois vers Immich, tout en conservant leur appartenance à chaque album d'origine. C'est aussi ce qui rend la reprise d'un import interrompu totalement sûre : relancer la même commande ne crée aucun doublon, immich-go reconnaît ce qui est déjà présent et saute directement à la suite.

✅ Une fois l'import validé, ouvre Immich sur mobile et vérifie que la génération des miniatures et la reconnaissance faciale ont bien tourné sur un échantillon de photos avant de considérer la migration terminée.

## Dépannage courant

**Connexion refusée ou clé API rejetée** : vérifie que l'URL du `--server` inclut bien le protocole (`http://` ou `https://`) et le port exact de ton instance Immich. Une clé API révoquée ou expirée donne la même erreur générique, régénère-la si le doute persiste.

**Import anormalement lent** : le goulot d'étranglement vient presque toujours du serveur Immich qui génère les miniatures et lance la reconnaissance faciale en tâche de fond, pas du transfert réseau lui-même. Si tu as [Dozzle](/dozzle-docker-visionneuse-logs-web/) branché sur ton serveur, c'est le moment de surveiller en direct les logs du conteneur Immich pour voir s'il étouffe sous la charge ou s'il tourne normalement.

**Des photos manquent à l'arrivée sans message d'erreur clair** : vérifie d'abord qu'aucune archive Takeout n'a été oubliée dans le dossier source, c'est la cause numéro un. Ensuite, regarde si certains fichiers n'avaient pas de JSON de métadonnées correspondant dans l'export d'origine, Google en génère parfois des incomplets sur de très grosses bibliothèques.

**La commande reste bloquée sans rien afficher** : laisse-la tourner un peu plus longtemps avant de l'interrompre. Sur une bibliothèque de plusieurs dizaines de milliers de fichiers, le calcul des sommes de contrôle avant l'envoi peut prendre du temps sans retour visuel immédiat.

💡 À lire aussi : [Proxmox Backup Server : sauvegardes dédupliquées de tes VM et LXC](/proxmox-backup-server-sauvegarde-vm-lxc/), dans la même veine que cet article.

💡 À lire aussi : [Kopia Docker : sauvegardes chiffrées et dédupliquées avec interface web](/kopia-docker-sauvegarde-chiffree/), dans la même veine que cet article.

## Conclusion

Immich-go ne fait qu'une chose, mais il la fait bien : transformer un export Takeout illisible en une bibliothèque Immich propre, albums et métadonnées intacts. Pas de tri manuel, pas de perte de qualité, pas de dépendance à un service cloud intermédiaire. Juste un binaire, une clé API, et de la patience pendant que tout remonte.

Une fois tes photos rapatriées, la suite logique pour continuer à reprendre la main sur tes données personnelles passe souvent par les mêmes réflexes que pour [Calibre-web](/calibre-web-docker-bibliotheque-ebooks/) ou les autres services que tu auto-héberges déjà : vérifier régulièrement que les sauvegardes couvrent bien la bibliothèque, pas seulement la base de données. Garde tes archives Takeout originales de côté quelques semaines après la migration, le temps de confirmer que tout est bien arrivé sur Immich.
