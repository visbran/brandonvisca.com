---
title: "Dawarich Docker : remplace Google Timeline auto-hébergé"
description: "Dawarich Docker : ton alternative auto-hébergée à Google Timeline pour visualiser et importer tout ton historique de localisation."
pubDatetime: "2026-11-01T11:02:11+01:00"
modDatetime: "2026-10-31T08:00:00.000Z"
author: Brandon
tags:
  - auto-hebergement
  - base-de-donnees
  - reverse-proxy
  - tailscale
  - intermediaire
featured: false
draft: false
focusKeyword: dawarich docker
faqs:
  - question: "Dawarich Docker consomme combien de RAM sur mon serveur ?"
    answer: "La documentation recommande au moins 2 Go de RAM pour l'instance. Le compose officiel plafonne le conteneur applicatif à 4 Go par défaut, ajustable via APP_MEMORY_LIMIT selon la taille de ton historique."
  - question: "Que se passe-t-il si je perds l'accès à mon instance Dawarich ?"
    answer: "Tes données vivent dans le volume PostgreSQL et peuvent être exportées en GeoJSON ou GPX depuis l'interface. Sauvegarde ce volume régulièrement, c'est ta seule copie de ton historique de localisation."
  - question: "Dawarich peut-il suivre ma position en temps réel comme Google Maps ?"
    answer: "Oui, via OwnTracks ou Overland configurés en mode HTTP, ou via les apps mobiles officielles de Dawarich qui envoient ta position régulièrement à ton instance self-hosted."
---
> 💡 **TL;DR**
> - Dawarich est une alternative auto-hébergée à Google Timeline : import de ton historique Google, visualisation sur carte, statistiques de trajets
> - Installation en Docker Compose avec trois conteneurs (app, PostgreSQL/PostGIS, Redis), accessible sur le port 3000
> - Suivi en temps réel possible via OwnTracks, Overland ou les apps mobiles officielles, et export de tes données en GeoJSON/GPX à tout moment

## Google a ton historique complet depuis des années. Et si tu le reprenais ?

Google Timeline sait où tu étais mardi à 14h. Il sait combien de temps tu as passé chez le médecin, quel trajet tu prends pour aller au boulot, et depuis quand tu fréquentes ce nouveau resto. Toutes ces données dorment sur des serveurs qui ne t'appartiennent pas, et Google peut en changer les règles du jour au lendemain. C'est déjà arrivé avec la migration forcée du Timeline vers le stockage local du téléphone en 2024.

**Dawarich Docker règle ce problème.** Tu récupères ton export Google, tu l'importes dans ton propre conteneur Docker, et tu as exactement la même carte, les mêmes statistiques, sauf que tout tourne chez toi. Mon setup chez moi tourne depuis plusieurs mois sans accroc, et c'est devenu mon point de référence quand je veux savoir où j'étais tel jour sans passer par un compte Google.

## Table des matières

## Qu'est-ce que Dawarich et pourquoi remplacer Google Timeline

Dawarich Docker est un projet open source maintenu par le développeur Freika, publié sous licence AGPL-3.0 sur GitHub, où il dépasse les 10 000 étoiles. Le projet se présente lui-même comme l'alternative auto-hébergée à Google Timeline, et c'est exactement ce qu'il fait : il affiche ton historique de localisation sur une carte interactive, calcule des statistiques de trajets, et te laisse explorer tes déplacements par jour, mois ou année.

Ce qui distingue Dawarich Docker d'un simple visualiseur de carte :

- **Imports multiples** : Google Maps Timeline (anciens et nouveaux formats d'export), OwnTracks, Strava, Immich, fichiers GPX et GeoJSON, voire les métadonnées EXIF de tes photos
- **Exports** : GeoJSON et GPX, donc tes données ne sont jamais enfermées dans Dawarich
- **Visualisations** : carte de chaleur, points individuels, lignes de trajet, et un mode « Fog of War » qui dévoile progressivement les zones que tu as visitées, un peu comme un jeu de stratégie
- **Partage familial** : tu peux suivre la position de plusieurs membres d'un même foyer sur la même instance
- **Intégrations** : connexion directe à Immich ou Photoprism pour croiser tes photos avec tes déplacements

Le projet propose aussi une offre cloud payante pour qui ne veut pas s'embêter avec l'auto-hébergement, mais la version self-hosted reste complète et gratuite. C'est celle-là qui nous intéresse ici.

Si tu es déjà dans une démarche de reprendre la main sur tes données personnelles, Dawarich Docker s'inscrit dans la même logique que [Paperless-ngx](/paperless-ngx-docker-guide-auto-hebergement/) pour tes documents ou [FreshRSS](/freshrss-docker-lecteur-rss/) pour tes flux d'actualité : un service de plus qui sort de l'écosystème des géants du web pour vivre sur ton infra.

## Prérequis avant d'installer Dawarich Docker

Avant de te lancer, vérifie que tu as :

- Docker 20.10 ou plus récent, et Docker Compose 1.29 ou plus récent
- Un serveur AMD64 ou ARM64 (Raspberry Pi 4/5 compatible)
- Au moins 2 Go de RAM disponibles pour l'instance, la documentation officielle insiste sur ce minimum
- Un accès SSH ou terminal sur la machine qui hébergera le conteneur
- Ton export Google Timeline si tu veux migrer ton historique (on y revient plus bas)

⚠️ Dawarich Docker stocke des données de géolocalisation précises. Ne l'expose jamais sur Internet sans authentification, et réfléchis à qui aura accès à cette instance avant même de la monter.

## Dawarich Docker : installation avec Docker Compose

La méthode officielle repose sur trois conteneurs : l'application Rails, une base PostgreSQL avec l'extension PostGIS pour les données géographiques, et Redis pour les files de tâches en arrière-plan. Depuis la version 1.17.0 du projet, Sidekiq tourne intégré dans le conteneur applicatif, donc tu n'as plus besoin d'un quatrième service séparé juste pour ça.

Crée un dossier dédié et récupère le fichier de référence :

```bash
mkdir -p ~/docker/dawarich && cd ~/docker/dawarich
```

Fichier `compose.yml` minimal basé sur la configuration officielle :

```yaml
services:
  dawarich_redis:
    image: redis:8-alpine
    container_name: dawarich_redis
    command: redis-server --save 900 1 --save 300 10 --appendonly no
    volumes:
      - dawarich_shared:/data
    restart: always

  dawarich_db:
    image: postgis/postgis:17-3.5-alpine
    container_name: dawarich_db
    shm_size: 1G
    volumes:
      - dawarich_db_data:/var/lib/postgresql/data
      - dawarich_shared:/var/shared
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: change_moi
      POSTGRES_DB: dawarich_production
    restart: always

  dawarich_app:
    image: freikin/dawarich:latest
    container_name: dawarich_app
    ports:
      - "3000:3000"
    volumes:
      - dawarich_public:/var/app/public
      - dawarich_watched:/var/app/tmp/imports/watched
      - dawarich_storage:/var/app/storage
    environment:
      RAILS_ENV: production
      REDIS_URL: redis://dawarich_redis:6379
      DATABASE_HOST: dawarich_db
      DATABASE_USERNAME: postgres
      DATABASE_PASSWORD: change_moi
      DATABASE_NAME: dawarich_production
      APPLICATION_HOSTS: localhost,ton-domaine.tld
      SECRET_KEY_BASE: genere_une_vraie_cle_ici
      TIME_ZONE: Europe/Paris
    depends_on:
      - dawarich_db
      - dawarich_redis
    restart: unless-stopped

volumes:
  dawarich_db_data:
  dawarich_shared:
  dawarich_public:
  dawarich_watched:
  dawarich_storage:
```

**Deux points qui font la différence entre une install qui marche et une install qui fuit :**

- `POSTGRES_PASSWORD` et `SECRET_KEY_BASE` sont fixés à des valeurs de démo dans la configuration par défaut du projet. Change-les avant le premier `docker compose up`, pas après.
- `APPLICATION_HOSTS` doit lister tous les noms de domaine ou IP par lesquels tu accèdes à l'instance, séparés par des virgules, sinon Rails rejette les requêtes avec une erreur « Blocked host ».

Lance le tout :

```bash
docker compose up -d
```

Le premier démarrage prend une minute ou deux, le temps que la base s'initialise et que les migrations tournent. Ouvre ensuite `http://IP_DU_SERVEUR:3000`, crée ton premier compte administrateur, et tu es dans l'interface.

Pour gérer ce stack au quotidien sans retaper des commandes `docker compose` à chaque mise à jour, j'utilise [Dockge](/dockge-docker-gestionnaire-stacks-compose/), qui affiche l'état des conteneurs et permet de relancer le stack d'un clic depuis une interface web.

## Importer ton historique Google Timeline dans Dawarich

C'est la partie qui donne tout son sens à l'outil. Google te laisse exporter ton historique complet depuis [Google Takeout](https://takeout.google.com) en demandant les données « Location History (Timeline) ». Tu reçois un e-mail avec un fichier zip, généralement dans l'heure qui suit.

Une fois le zip décompressé, Dawarich Docker reconnaît automatiquement plusieurs formats :

- `Records.json` : le format récent utilisé par les exports Takeout actuels
- `Location History.json` : l'ancien format, encore présent si tu as un historique ancien
- Les fichiers « Semantic Location History » : un export par mois, utile si tu veux importer progressivement

Pour lancer l'import, va dans **Paramètres → Imports**, choisis la source correspondant à ton fichier, sélectionne-le (tu peux en sélectionner plusieurs à la fois) et clique sur **Create import**. Dawarich Docker traite le fichier en arrière-plan, via les files Redis dont on a parlé plus haut.

💡 Si ton export Google pèse plusieurs centaines de mégaoctets, l'import depuis l'interface web peut timeout. Dans ce cas, copie le fichier directement dans le conteneur avec `docker cp` puis lance la tâche en ligne de commande à l'intérieur du conteneur. Tu peux suivre la progression de l'import depuis la page Sidekiq intégrée à l'instance.

Une fois l'import terminé, ta carte se remplit. Chaque point devient un marqueur, chaque trajet une ligne, et les statistiques (distance totale, pays visités, villes traversées) se calculent automatiquement. C'est à ce moment précis que l'intérêt de l'outil devient concret : des années d'historique Google, d'un coup, chez toi.

## Suivi en temps réel : OwnTracks, Overland et les apps mobiles

Importer le passé c'est bien, mais Dawarich Docker sert aussi à continuer d'enregistrer ta position au jour le jour, sans dépendre de Google.

Ta clé API se trouve dans la section **Compte** de l'interface, et la documentation de l'API vit à l'adresse `/api-docs` de ton instance.

**Avec Overland** (app iOS) : configure l'endpoint de réception vers :

```
http://ton-instance:3000/api/v1/overland/batches?api_key=TA_CLE_API
```

**Avec OwnTracks** (iOS/Android) : passe l'app en mode HTTP, désactive l'option qui envoie le payload en JSON brut (Dawarich attend les données en paramètres de requête, pas dans le corps), et pointe vers le même type d'URL avec ta clé en paramètre.

**Avec les apps officielles Dawarich** (iOS et Android) : tu n'as qu'à saisir l'URL de ton instance et ta clé API, ou scanner le QR code généré dans les paramètres de ton compte. C'est le chemin le plus simple si tu démarres de zéro.

⚠️ Comme la clé API transite dans l'URL, elle peut se retrouver dans les logs d'accès de ton reverse proxy. Si tu surveilles tes logs, pense à les filtrer ou à restreindre leur rétention pour ce endpoint précis.

## Sécuriser et exposer Dawarich sans tout donner à Internet

Par nature, Dawarich Docker concentre des données ultra-sensibles : l'historique complet de tes déplacements. Deux approches raisonnables pour y accéder depuis l'extérieur de chez toi.

**La première, exposer via un reverse proxy** avec HTTPS et un nom de domaine. Nginx Proxy Manager ou Caddy font le travail, à condition d'ajouter le domaine choisi dans `APPLICATION_HOSTS` et de ne jamais laisser le port 3000 ouvert directement sur Internet.

**La seconde, plus simple et plus sûre pour ce type de données, passer par Tailscale.** Tu installes le client sur ton serveur et sur ton téléphone, tu rejoins le même tailnet, et ton instance Dawarich devient accessible uniquement depuis tes propres appareils, sans jamais toucher à un port public ni à un certificat. Pour des données aussi personnelles qu'un historique de localisation, je recommande clairement cette option plutôt qu'une exposition publique, même protégée par mot de passe.

Dans les deux cas, change le mot de passe administrateur par défaut dès la création du compte, et active l'authentification à deux facteurs si tu comptes exposer l'instance, même via un VPN.

## Dépannage : les pièges classiques

**L'interface reste inaccessible après le démarrage**
Vérifie les logs du conteneur applicatif avant de conclure à un bug. Si tu gères plusieurs conteneurs sur ton homelab, [Dozzle](/dozzle-docker-visionneuse-logs-web/) te donne une vue en temps réel sur tous tes logs Docker sans taper une seule commande `docker logs`.

**Erreur « Blocked host » dans le navigateur**
`APPLICATION_HOSTS` ne contient pas le nom ou l'IP que tu utilises pour accéder à l'instance. Ajoute-le à la liste séparée par des virgules et redémarre le conteneur applicatif.

**L'import Google Timeline reste bloqué**
Les très gros fichiers `Records.json` timeout depuis l'interface web. Passe par la commande en ligne intégrée au conteneur plutôt que par l'upload web pour les exports de plusieurs années.

**Les points n'apparaissent pas sur la carte après un envoi OwnTracks**
Vérifie que l'option « JSON payload » est bien désactivée côté app. Dawarich attend les coordonnées en paramètres de requête HTTP, pas dans un corps JSON.

**Tu veux garder une copie de tes trajets ailleurs que dans Dawarich Docker**
Exporte régulièrement en GeoJSON ou GPX depuis l'interface, et range ces fichiers quelque part où tu peux les consulter facilement. [Filestash](/filestash-docker-navigateur-fichiers-web/) fait un bon visualiseur pour naviguer dans ces exports si tu les stockes sur un partage réseau.

## Conclusion

Dawarich Docker coche une case précise : récupérer un historique de localisation que Google construit depuis des années, et continuer à l'alimenter sans dépendre d'un compte externe. L'installation tient en trois conteneurs, l'import de ton export Google se fait depuis une interface simple, et le suivi en temps réel passe par des protocoles ouverts comme OwnTracks plutôt que par une app propriétaire.

La seule vraie exigence, c'est de traiter ces données avec le sérieux qu'elles méritent : mots de passe changés, accès restreint par VPN plutôt qu'exposition publique, et exports réguliers pour ne jamais dépendre d'une seule copie. Une fois ça posé, tu as ta propre carte, chez toi, sans que personne d'autre n'ait à la regarder.
