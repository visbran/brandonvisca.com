---
title: "FreshRSS Docker : ton lecteur RSS auto-hébergé (alternative légère à Google Reader)"
description: "Guide complet pour installer FreshRSS avec Docker Compose. Lecteur RSS auto-hébergé et open-source. Comparatif freshrss docker, Miniflux et Feedly."
pubDatetime: "2026-06-18T08:00:00.000Z"
modDatetime: "2026-06-18T08:00:00.000Z"
author: Brandon Visca
tags:
  - auto-hebergement
  - docker
  - freshrss
  - intermediaire
  - rss
  - guide
featured: false
draft: false
focusKeyword: freshrss docker
faqs:
  - question: "FreshRSS ou Miniflux : lequel choisir ?"
    answer: "FreshRSS est plus complet avec une interface web riche, des catégories, des filtres avancés et des plugins. Miniflux est minimaliste, ultra-léger et privilégie la lecture sans distraction. Choisis FreshRSS si tu veux une expérience proche de Google Reader avec des fonctionnalités avancées."
  - question: "FreshRSS peut-il remplacer Feedly ?"
    answer: "Oui, FreshRSS est une excellente alternative auto-hébergée à Feedly. Il offre la synchronisation multi-appareils via l'API Fever et Google Reader, l'import/export OPML, et des applications mobiles compatibles."
  - question: "Quelles sont les ressources minimales pour FreshRSS sous Docker ?"
    answer: "FreshRSS est très léger : environ 50 Mo de RAM et moins de 500 Mo d'espace disque pour l'installation de base. Une Raspberry Pi 3B+ suffit pour une utilisation personnelle."
ogImage: "" 
---
> 💡 **TL;DR**
> - FreshRSS est un lecteur RSS open-source, auto-hébergé et ultra-léger qui tourne parfaitement sous Docker. Il offre une interface web riche, des filtres avancés, des plugins et une API compatible avec les applis mobiles.
> - En 5 minutes, tu peux remplacer Feedly par une solution que tu contrôles entièrement, même sur une Raspberry Pi.
> - Comparatif inclus : FreshRSS vs Miniflux vs Feedly, avec Docker Compose complet et fonctionnel.

## Table des matières

## Pourquoi encore utiliser RSS en 2026 ?

Avec l'explosion des algorithmes, des fils d'actualité bruités et des réseaux sociaux en déclin, le RSS fait un retour en force chez les geeks et les professionnels de l'information. C'est le seul moyen de centraliser tes sources favorites, blogs, sites d'actu, newsletters, chaînes YouTube, releases GitHub, sans intermédiaire qui décide ce que tu dois lire.

Google Reader a disparu en 2013, mais l'écosystème RSS n'a jamais été aussi vivant. Feedly domine le marché des solutions SaaS, mais payantes et verrouillées. Côté auto-hébergement, deux noms reviennent constamment : Miniflux et FreshRSS. Si tu cherches une solution minimaliste, j'ai déjà testé [Miniflux avec Docker](/miniflux-docker-lecteur-rss-guide/). Aujourd'hui, on s'attaque à FreshRSS, l'alternative plus complète et proche de l'expérience Google Reader.

## Qu'est-ce que FreshRSS ?

FreshRSS est un agrégateur RSS libre et gratuit, développé en PHP par la communauté française. Lancé en 2013, il est régulièrement mis à jour et bénéficie d'une communauté active. Contrairement à une simple liste de flux, FreshRSS propose une véritable interface de gestion d'articles avec :

- Un système de catégories et de tags personnalisés
- Des filtres de lecture avancés (par mot-clé, auteur, URL)
- Une gestion des favoris et articles partagés
- Un mode multi-utilisateur avec gestion des droits
- Un système de plugins extensible
- Une API compatible Fever et Google Reader pour les applis mobiles
- Un support natif de l'authentification via formulaire, HTTP ou OpenID Connect

Son architecture PHP/MySQL ou PostgreSQL le rend compatible avec la plupart des hébergements classiques, mais c'est sous Docker qu'il devient vraiment intéressant pour un déploiement propre et reproductible.

## FreshRSS, Miniflux ou Feedly : le comparatif

Choisir un lecteur RSS dépend de ton usage. Voici un tableau comparatif objectif entre les trois solutions les plus citées.

| Critère | FreshRSS | Miniflux | Feedly |
|---|---|---|---|
| Hébergement | Auto-hébergé | Auto-hébergé | SaaS (cloud) |
| Licence | AGPL-3.0 | Apache 2.0 | Propriétaire |
| Interface | Riche, catégories, panneaux | Minimaliste, texte brut | Moderne, riche |
| Ressources | ~50 Mo RAM | ~30 Mo RAM | N/A (cloud) |
| Multi-utilisateur | Oui | Non (sauf version payante cloud) | Oui (plans payants) |
| Filtres avancés | Oui | Basiques | Oui (payant) |
| Plugins | Oui (communauté) | Non | Non |
| API mobile | Fever + Google Reader | Google Reader + Fever | API propriétaire |
| Import OPML | Oui | Oui | Oui |
| Prix | Gratuit | Gratuit | Gratuit limité, puis 6 €/mois |
| Self-hosted facile | Oui (Docker) | Oui (Docker) | Non |

**Verdict** : Feedly est pratique si tu n'as aucune envie de gérer un serveur. Miniflux est parfait si tu veux du minimalisme radical. FreshRSS est le choix le plus équilibré : interface complète, légèreté, extensibilité, et zéro coût récurrent. Pour une stack complète de services auto-hébergés, j'ai listé mes indispensables dans ce [guide Docker pour débutants](/docker-debutant-services-auto-heberger/).

## Prérequis pour installer FreshRSS avec Docker

Avant de lancer le Docker Compose, assure-toi d'avoir :

- Docker et Docker Compose installés sur ton serveur
- Un accès SSH ou local à ta machine
- (Optionnel) Un nom de domaine ou sous-domaine dédié
- (Optionnel) Un reverse proxy déjà en place

FreshRSS fonctionne sur n'importe quel système supportant Docker : Ubuntu, Debian, Raspberry Pi OS, Synology DSM, etc. Aucune dépendance exotique n'est nécessaire.

## Installation de FreshRSS avec Docker Compose

Voici une configuration complète et fonctionnelle que j'utilise en production. Elle sépare FreshRSS et sa base de données MariaDB, avec des volumes nommés pour la persistance des données.

```yaml
version: "3.8"

services:
  freshrss:
    image: freshrss/freshrss:1.25.0
    container_name: freshrss
    restart: unless-stopped
    ports:
      - "8080:80"
    environment:
      - CRON_MIN=*/20
      - TZ=Europe/Paris
    volumes:
      - freshrss_data:/var/www/FreshRSS/data
      - freshrss_extensions:/var/www/FreshRSS/extensions
    depends_on:
      - freshrss-db

  freshrss-db:
    image: mariadb:11
    container_name: freshrss-db
    restart: unless-stopped
    environment:
      - MYSQL_ROOT_PASSWORD=ton_mot_de_passe_root_fort
      - MYSQL_DATABASE=freshrss
      - MYSQL_USER=freshrss
      - MYSQL_PASSWORD=ton_mot_de_passe_freshrss_fort
    volumes:
      - freshrss_db:/var/lib/mysql

volumes:
  freshrss_data:
  freshrss_extensions:
  freshrss_db:
```

**Points importants sur cette configuration :**

- L'image officielle `freshrss/freshrss` est maintenue par l'équipe du projet et publiée sur Docker Hub
- `CRON_MIN=*/20` lance la mise à jour des flux toutes les 20 minutes automatiquement
- MariaDB est préférable à SQLite dès que tu dépasses quelques dizaines de flux
- Les volumes nommés garantissent la persistance des données même si tu recrées les conteneurs
- Change absolument les mots de passe par défaut avant le premier lancement

Pour lancer la stack :

```bash
cd /opt/freshrss
docker compose up -d
```

Attends quelques secondes que MariaDB initialise sa base, puis accède à `http://ip-de-ton-serveur:8080` pour l'installation web.

## Configuration initiale de FreshRSS

Lors du premier accès, un assistant d'installation te guide en 4 étapes :

1. **Langue** : sélectionne Français
2. **Vérifications** : PHP et extensions doivent être toutes vertes (elles le sont dans l'image Docker)
3. **Base de données** : choisis MySQL / MariaDB et renseigne :
   - Hôte : `freshrss-db`
   - Base : `freshrss`
   - Utilisateur : `freshrss`
   - Mot de passe : celui défini dans le compose
4. **Administrateur** : crée ton compte avec un mot de passe fort

Une fois connecté, va dans **Gestion** > **Abonnements** pour importer ton fichier OPML (exporté depuis Feedly ou ton ancien lecteur). FreshRSS récupère instantanément tous tes flux.

## Fonctionnalités avancées à ne pas ignorer

FreshRSS cache des options très puissantes sous son interface sobre :

**Filtres et règles de lecture**
Dans **Configuration** > **Filtres**, tu peux créer des règles automatiques pour marquer comme lu, favoriser ou notifier selon des critères (titre contient "Python", URL contient "github.com", etc.). C'est idéal pour trier le bruit des newsletters ou des releases.

**Partage personnalisé**
Tu peux ajouter des services de partage (Wallabag, Shaarli, Webhooks) pour envoyer un article en un clic vers ton système de bookmarking ou de sauvegarde.

**Thèmes et personnalisation**
Plusieurs thèmes sont disponibles nativement, et la communauté en propose d'autres. Le thème **Dark** est particulièrement réussi pour la lecture nocturne.

**Plugins**
Le répertoire officiel comporte des extensions pour ajouter un lecteur JSON de fever, intégrer Telegram, ou synchroniser avec Pocket. Les plugins se déposent simplement dans le dossier `extensions/`.

**Mode anonyme et multi-utilisateur**
Tu peux créer plusieurs profils utilisateurs avec des droits différenciés. C'est parfait pour partager un serveur entre colocataires ou collègues sans mélanger les flux.

## Sécuriser FreshRSS derrière un reverse proxy

Exposer FreshRSS directement sur le port 8080 n'est pas recommandé en production. Pour héberger FreshRSS derrière un reverse proxy sécurisé, j'utilise [Caddy avec Docker](/caddy-docker-reverse-proxy-guide/). Voici le bloc Caddy correspondant à ajouter dans ton `Caddyfile` :

```text
freshrss.tondomaine.com {
    reverse_proxy freshrss:80
}
```

Caddy gère automatiquement le HTTPS via Let's Encrypt. Si tu utilises Traefik, ajoute simplement les labels appropriés à ton service `freshrss` dans le Docker Compose.

## Applications mobiles compatibles avec FreshRSS

L'un des grands avantages de FreshRSS est son API double : Fever et Google Reader. Cela lui donne une compatibilité quasi universelle avec les lecteurs mobiles :

- **Fiery Feeds** (iOS) : natif, rapide, supporte l'API Fever
- **Unread** (iOS) : design élégant, synchronisation Fever
- **Read You** (Android) : open-source, interface Material You, support Google Reader API
- **NetNewsWire** (iOS/macOS) : gratuit, léger, supporte l'API Google Reader

Pour activer l'API, va dans **Administration** > **Authentification** > **Autoriser l'accès par API**. Génère un mot de passe d'application et configure ton client mobile avec l'URL de ton instance FreshRSS.

## Sauvegarde et migration

FreshRSS rend la sauvegarde très simple grâce à sa structure de données claire. Pour sauvegarder l'intégralité de ton instance :

```bash
# Base de données
docker exec freshrss-db mariadb-dump -u root -pTON_MDP_ROOT freshrss > freshrss_backup.sql

# Données et extensions
docker cp freshrss:/var/www/FreshRSS/data ./freshrss_data_backup
docker cp freshrss:/var/www/FreshRSS/extensions ./freshrss_extensions_backup
```

Pour restaurer, inverse simplement ces opérations. Tu peux aussi configurer un conteneur [Duplicati](/duplicati-docker-sauvegarde/) pour automatiser ces backups vers un stockage distant.

## Conclusion : FreshRSS, l'agrégateur RSS qui a tout bon

FreshRSS est sans doute le meilleur compromis entre légèreté, richesse fonctionnelle et facilité de déploiement dans le monde des lecteurs RSS auto-hébergés. Son interface familière rappelle les meilleures heures de Google Reader, tandis que son support Docker et son API mobile en font une solution moderne et pratique au quotidien.

Que tu sois sur un VPS cloud à 5 €/mois ou une Raspberry Pi dans ton salon, FreshRSS s'intègre naturellement dans une stack d'auto-hébergement. Il remplace avantageusement Feedly pour les utilisateurs soucieux de leur souveraineté numérique, tout en offrant plus de fonctionnalités que Miniflux pour ceux qui veulent une interface riche et des filtres avancés.

Déploie-le, importe tes flux, connecte ton appli mobile, et retrouve enfin un fil d'actualité qui t'appartient.
