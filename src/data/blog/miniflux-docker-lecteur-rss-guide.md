---
title: "Miniflux Docker : ton lecteur RSS auto-hébergé en 5 min"
description: "Guide complet Miniflux Docker : déploie ton lecteur RSS auto-hébergé avec PostgreSQL en 5 min. Alternative open-source à Feedly."
pubDatetime: "2026-06-05T08:00:00.000Z"
modDatetime: "2026-06-09T00:00:00+01:00"
author: Brandon Visca
tags:
  - docker
  - auto-hebergement
  - homelab
  - debutant
  - guide
  - linux
featured: false
draft: false
focusKeyword: miniflux docker
faqs:
  - question: "Miniflux vs FreshRSS, comment choisir ?"
    answer: "Miniflux est minimaliste, rapide et léger. FreshRSS possède plus de plugins et d'interfaces personnalisables. Choisis Miniflux si tu préfères la simplicité, FreshRSS si tu veux un écosystème extensible."
  - question: "Combien de RAM consomme Miniflux en Docker ?"
    answer: "Miniflux seul consomme environ 30-50 Mo de RAM. Avec PostgreSQL, compte 150-200 Mo au total. C'est ridiculement léger comparé à des solutions web modernes."
  - question: "Les apps RSS iOS fonctionnent-elles avec Miniflux ?"
    answer: "Oui, via l'API Fever. Reeder 5, NetNewsWire et Fiery Feeds se connectent nativement à Miniflux avec l'URL Fever et tes identifiants."
  - question: "Faut-il une base de données pour Miniflux ?"
    answer: "Oui, PostgreSQL est obligatoire (version 13+ recommandée). Miniflux ne fonctionne pas avec SQLite ou MySQL."
  - question: "Comment migrer mes flux depuis Feedly ?"
    answer: "Exporte ton OPML depuis Feedly (Organize > Export OPML), puis importe-le dans Miniflux via Feeds > Import."
---
> 💡 **TL;DR**
> - Lecteur RSS minimaliste et auto-hébergé, sans tracking ni pub, contrairement à Feedly
> - Un `docker-compose.yml` avec Miniflux + PostgreSQL : opérationnel en 5 minutes
> - Zéro euro si tu as déjà un serveur avec Docker

Tu ouvres encore ton navigateur pour vérifier 15 blogs différents ? Tu regrettes Google Reader comme tout le monde ? Et Feedly, entre les pubs intégrées, le tracking de lecture et les algos qui décident ce que tu dois voir... ben ça commence à te gonfler sérieusement.

Bonne nouvelle : **Miniflux** existe. C'est un lecteur RSS open-source, minimaliste, et terriblement efficace. Tu le déploies chez toi en Docker, tu gardes le contrôle total, et zéro tracking.

Dans cet article, on installe Miniflux avec Docker Compose (PostgreSQL inclus), on configure les flux, on synchronise avec les apps iOS via l'API Fever, et on ajoute quelques règles de filtrage pour trier automatiquement.

Si tu débutes en auto-hébergement, n'hésite pas à consulter mon [guide Docker pour débutants](/docker-debutant-services-auto-heberger/) et mon [guide auto-hébergement complet](/auto-hebergement-guide-complet-2025/) pour bien poser les bases.

## Table des matières


## Pourquoi un lecteur RSS auto-hébergé en 2026 ?

Google Reader a fermé en 2013. Depuis, on a eu droit à une succession de remplaçants qui ont soit fermé, soit été rachetés, soit transformés en machines à données personnelles.

Les réseaux sociaux ont essayé de remplacer RSS avec des algorithmes opaques. Résultat : tu rates 80% des publications des sites que tu suis parce qu'une IA te montre des memes de chats que tu n'as jamais demandés.

Le RSS, c'est le web comme il aurait dû rester :

- Tu choisis **exactement** quels sites suivre
- Tu lis **dans l'ordre chronologique**, pas celui d'un algorithme
- Pas de pub intégrée, pas de tracking, pas de "engagement optimization"
- Ton historique de lecture reste chez toi

### Miniflux vs FreshRSS vs Feedly

| Critère | Miniflux | FreshRSS | Feedly |
|---------|----------|----------|--------|
| **Auto-hébergé** | Oui | Oui | Non (SaaS) |
| **Prix** | Gratuit | Gratuit | 7$/mois (Pro) |
| **Interface** | Minimaliste, rapide | Riche, thèmes | Moderne, trackée |
| **Plugins** | Non (philosophie) | Oui (extensible) | Non (fermé) |
| **API** | REST + Fever | REST + Fever + GReader | API payante |
| **Ressources RAM** | ~50 Mo | ~100 Mo | N/A (cloud) |
| **Filtrage** | Règles intégrées | Plugins tiers | Limité (payant) |
| **Apps mobiles** | Via API Fever | Via API | Officielles (trackées) |
| **Open source** | Oui (GPLv3) | Oui (AGPL) | Non |

Mon choix : **Miniflux** pour la simplicité radicale. Si tu préfères personnaliser à fond et installer des plugins, j'ai publié un guide complet sur [FreshRSS avec Docker](/freshrss-docker-lecteur-rss/). Feedly, c'est pratique mais tu es le produit.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose installés (voir mon [guide Docker débutant](/docker-debutant-services-auto-heberger/))
- Un reverse proxy type Nginx Proxy Manager ou Traefik (pour HTTPS, recommandé)
- Un nom de domaine ou sous-domaine (optionnel mais vivement conseillé)
- Un gestionnaire de mots de passe pour stocker le mot de passe admin PostgreSQL

Miniflux est si léger qu'il tourne parfaitement sur un Raspberry Pi 4 avec 4 Go de RAM. Sur un mini-PC Intel N100, tu oublieras même qu'il est là.

## Installation avec Docker Compose

On déploie Miniflux avec PostgreSQL dans une stack simple. Crée un dossier dédié :

```bash
mkdir -p ~/docker/miniflux
cd ~/docker/miniflux
```

### Le docker-compose.yml complet

```yaml
version: "3.8"

services:
  miniflux-db:
    image: postgres:16-alpine
    container_name: miniflux-db
    environment:
      POSTGRES_USER: miniflux
      POSTGRES_PASSWORD: change_moi_maintenant_super_secret
      POSTGRES_DB: miniflux
    volumes:
      - ./db:/var/lib/postgresql/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "miniflux"]
      interval: 10s
      timeout: 5s
      retries: 5

  miniflux:
    image: miniflux/miniflux:2.2.4
    container_name: miniflux
    ports:
      - "8080:8080"
    environment:
      DATABASE_URL: postgres://miniflux:change_moi_maintenant_super_secret@miniflux-db:5432/miniflux?sslmode=disable
      RUN_MIGRATIONS: "1"
      CREATE_ADMIN: "1"
      ADMIN_USERNAME: admin
      ADMIN_PASSWORD: change_moi_aussi_maintenant
      BASE_URL: https://miniflux.tondomaine.com
      POLLING_FREQUENCY: "15"
      BATCH_SIZE: "100"
      WORKER_POOL_SIZE: "5"
      # API Fever pour les apps mobiles
      FEVER_TOKEN: un_token_aleatoire_de_32_chars
    depends_on:
      miniflux-db:
        condition: service_healthy
    restart: unless-stopped
```

Quelques explications importantes :

- `miniflux-db` : PostgreSQL 16 en version Alpine (ultra-légère). Healthcheck pour attendre que la base soit prête avant de lancer Miniflux.
- `DATABASE_URL` : chaîne de connexion PostgreSQL. Assure-toi que le mot de passe correspond exactement à celui du conteneur postgres.
- `RUN_MIGRATIONS: "1"` : applique automatiquement les migrations de base de données au démarrage.
- `CREATE_ADMIN: "1"` : crée un compte admin au premier lancement. Après, tu peux le retirer ou le garder (pas de risque, il ne recrée pas si l'utilisateur existe).
- `BASE_URL` : URL publique de ton instance. Adapte avec ton domaine ou IP.
- `POLLING_FREQUENCY: "15"` : intervalle de rafraîchissement des flux en minutes. Par défaut 60, j'aime bien 15 pour un flux actif.
- `FEVER_TOKEN` : clé API pour connecter les apps mobiles (Reeder, NetNewsWire...).

**Change impérativement** les mots de passe `POSTGRES_PASSWORD` et `ADMIN_PASSWORD`.

Lance la stack :

```bash
docker compose up -d
```

Vérifie que tout tourne :

```bash
docker compose ps
# miniflux-db : healthy
# miniflux    : running
```

Accède à l'interface : `http://<ip-serveur>:8080` ou directement ton domaine si tu as configuré le reverse proxy.

## Configuration initiale

### Premier accès

Connecte-toi avec les identifiants définis dans le docker-compose :

- **Username :** `admin`
- **Password :** celui que tu as mis dans `ADMIN_PASSWORD`

Change immédiatement le mot de passe admin dans Settings > Users.

### Créer un utilisateur normal

Ne navigue pas en admin au quotidien. Va dans Users > Create User et crée tes comptes personnels. Les comptes utilisateurs ont les mêmes droits sur les flux mais pas sur la configuration système.

### Importer tes flux

Si tu viens d'un autre lecteur :

1. Exporte un fichier OPML depuis ton ancien lecteur (Feedly : Organize > Export OPML)
2. Dans Miniflux : Feeds > Import > choisis ton fichier OPML
3. Tous tes flux sont importés avec leurs catégories

### Quelques sources pour démarrer

Si tu pars de zéro, voici quelques sites francophones tech avec des flux RSS de qualité :

- Korben.info
- Next INpact
- Le Journal du hacker (liens)
- Putain de Code
- TechCrunch France
- Presse-citron

Tu peux aussi ajouter des chaînes Youtube qui proposent des flux (les "communities" RSS de certaines plateformes).

## Fonctionnalités clés de Miniflux

### Lecture sans distraction

C'est le cœur de Miniflux. Quand tu cliques sur un article, Miniflux affiche :

- Le titre et l'auteur
- Le contenu extrait (ou intégral si le flux est complet)
- Les liens cliquables
- Zéro pub, zéro pop-up, zéro sidebar encombrante

Le mode "Reader" est intégré : il extrait automatiquement le contenu complet même si le flux ne le fournit que partiellement.

### Marquage et gestion des articles

- **Read/unread** : marque les articles comme lus ou non lus
- **Star** : articles à garder, comme des favoris
- **Archive** : les articles lus disparaissent de la vue par défaut mais restent accessibles
- **Catégories** : organise tes flux par thème (Tech, News, Dev, etc.)

Le raccourci clavier `m` marque comme lu, `s` met en favori. La navigation entièrement clavier est supportée (essaie `?` pour voir la liste).

### Règles de filtrage (highlight)

C'est là que Miniflux devient intelligent. Tu peux créer des règles qui agissent automatiquement sur les articles entrants :

Va dans Feeds > Integrations > Create Filter :

**Exemple 1 : Ignorer les articles qui contiennent "Bitcoin"**

- Rule title : "No crypto spam"
- If title matches : `Bitcoin|cryptocurrency|crypto`
- Action : Mark as Read

**Exemple 2 : Marquer prioritairement les articles Docker**

- If title matches : `Docker|Kubernetes|container`
- Action : Star

**Exemple 3 : Supprimer les articles courts (micro-actus)**

- If content length is less than `200`
- Action : Mark as Read

Les règles sont exécutées dans l'ordre et s'appliquent à tous les flux ou seulement à ceux que tu sélectionnes.

### API REST native

Miniflux expose une API REST complète (documentée sur `/docs` de ton instance). Tu peux :

- Créer des scripts d'import/export
- Déclencher des actions à distance
- Intégrer dans un dashboard (Home Assistant, etc.)
- Automatiser la gestion des flux

L'API utilise une clé d'authentification que tu trouves dans Settings > API Keys.

### Fever API : compatibilité apps iOS/Android

Le protocole Fever est supporté nativement. Ça signifie que presque toutes les apps RSS du marché se connectent à ton Miniflux.

**Apps compatibles testées :**

- Reeder 5 (iOS/macOS), la référence
- NetNewsWire (iOS/macOS), open source, gratuit
- Fiery Feeds (iOS)
- Readrops (Android), open source

**Configuration Reeder 5 :**

1. Ajouter un compte > Fever
2. URL : `https://miniflux.tondomaine.com/fever/`
3. Username : ton username Miniflux
4. Password : le `FEVER_TOKEN` de ton docker-compose
5. Valider, sync instantanée

## Tips avancés

### Catégories intelligentes

Trie tes flux par catégorie (Tech, News, Science, Veille...). Pour chaque catégorie, tu peux configurer l'ordre d'affichage (chronologique ou par priorité).

Astuce : crée une catégorie "Must Read" pour les flux les plus importants, et consulte-la en premier.

### Bookmarklet

Miniflux fournit un bookmarklet pour s'abonner rapidement à un site. Va dans Settings > Bookmarks, glisse le bookmarklet dans ta barre de favoris du navigateur.

Quand tu es sur un site avec un flux, clique sur le bookmarklet, l'abonnement s'ouvre directement dans Miniflux.

### PWA (Progressive Web App)

Miniflux est une PWA nativement. Depuis Chrome ou Safari sur mobile :

- "Ajouter à l'écran d'accueil"
- L'app s'ouvre sans barre d'adresse
- Notifications push (si activées dans les settings)

Sur iOS, c'est presque aussi fluide qu'une app native à part la sync en arrière-plan.

### Dark mode

Activable dans Settings > Theme. Le thème sombre est parfaitement calibré pour la lecture longue.

## Maintenance et mises à jour

Mettre à jour Miniflux est trivial avec Docker :

```bash
cd ~/docker/miniflux
docker compose pull
# La commande pull va télécharger les nouvelles images
docker compose up -d
# Les conteneurs redémarrent avec les nouvelles versions
```

Miniflux gère les migrations automatiquement (`RUN_MIGRATIONS: "1"`), donc zéro manipulation SQL manuelle.

### Sauvegardes

La base de données PostgreSQL contient tous tes flux, articles lus, favoris et règles de filtrage. Sauvegarde-la régulièrement.

Option simple : copie le dossier `./db/` monté en volume et stocke-le ailleurs (NAS, cloud chiffré). Pour les backups automatiques, j'utilise Duplicati sur mon homelab, j'ai écrit un [guide complet à ce sujet](/duplicati-docker-sauvegarde/) que je te recommande chaudement.

Option pro : pg_dump via un cron hebdomadaire :

```bash
0 3 * * 0 docker exec miniflux-db pg_dump -U miniflux miniflux > /backup/miniflux-$(date +\%Y\%m\%d).sql
```

Garde aussi une copie de ton `docker-compose.yml` et ton `FEVER_TOKEN` dans ton gestionnaire de mots de passe.

## Conclusion

Miniflux c'est le retour du RSS comme on l'aimait : simple, rapide, et contrôlé. Pas d'algorithme opaque, pas de réseau social qui décide ce que tu dois lire, pas de pub intégrée.

Tu installes ça sur ton serveur en 5 minutes, tu branches Reeder sur ton iPhone, et tu retrouves enfin le plaisir de lire les actualités dans l'ordre, sans filtre, sans stress.

Le RSS n'est pas mort. Il a juste attendu que tu lui construises une maison. Installe ta stack, branche Reeder, et reprends la main sur ta veille.

## Pour aller plus loin

- [Documentation officielle de Miniflux](https://miniflux.app/docs/), configuration, variables d'environnement et API REST
- [Linkding : gestionnaire de bookmarks auto-hébergé](/linkding-docker-bookmarks/), le complément parfait pour archiver ce que tu lis
- [Duplicati en Docker : sauvegarder ta base PostgreSQL](/duplicati-docker-sauvegarde/), pour ne jamais perdre tes flux et tes favoris
