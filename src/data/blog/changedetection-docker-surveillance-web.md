---
title: "Changedetection Docker : guide complet pour surveiller n'importe quel site web (alternative Distill.io)"
description: "Guide changedetection docker : installe Changedetection.io et surveille n'importe quel site web avec alertes prix et disponibilité."
focusKeyword: "changedetection docker"
pubDatetime: "2026-07-08T08:00:00.000Z"
modDatetime: "2026-07-08T08:00:00.000Z"
author: Brandon
tags:
  - intermediaire
  - auto-hebergement
  - docker
  - surveillance
  - monitoring
featured: false
draft: false
ogImage: ""
---
> 💡 **TL;DR**
> - Changedetection.io est un outil open-source qui surveille n'importe quelle page web et t'envoie une alerte dès qu'un élément change
> - Tu l'héberges toi-même en 5 minutes avec Docker Compose, sans dépendre d'un service cloud payant comme Distill.io
> - Parfait pour les alertes prix, la surveillance de disponibilité produit, le monitoring de pages concurrentes ou de documentation

## Table des matières

## Pourquoi surveiller des pages web ?

T'as déjà rafraîchi dix fois par jour la page d'un site d'e-commerce en attendant une baisse de prix ? Ou attendu une réouverture des inscriptions à une formation sans savoir quand ça tombe ? Ou voulu suivre une modification discrète sur un site concurrent sans passer ta vie à comparer des captures d'écran ?

C'est exactement le job de Changedetection.io. C'est un outil de surveillance de changements web, open-source, auto-hébergé, et qui tourne dans un simple conteneur Docker. Tu lui donnes une URL, il la scanne régulièrement, compare le contenu, et t'envoie une alerte par email, Discord, Telegram, Slack, ou n'importe quel webhook dès qu'un changement est détecté.

La différence avec Distill.io ou Visualping ? Tu contrôles tout. Tes données restent chez toi, tu ne payes pas un abonnement cloud, et tu peux surveiller autant de pages que tu veux sans limite artificielle.

Si tu cherches aussi à monitorer l'état de tes services et la santé de tes serveurs, j'ai déjà couvert [Beszel pour Docker](/beszel-monitoring-docker/). Changedetection.io complète parfaitement cette stack en surveillant l'extérieur : les sites web, les prix, les annonces.

## Prérequis

Avant de lancer quoi que ce soit, assure-toi d'avoir :

- Un serveur avec Docker et Docker Compose installés
- Un accès SSH ou local à ta machine
- (Optionnel) Un nom de domaine ou sous-domaine si tu veux exposer l'interface derrière un reverse proxy
- (Optionnel) Un reverse proxy comme Traefik ou Caddy déjà en place

Si tu débutes avec Docker et que tu veux voir les bases, j'ai un guide sur [les services essentiels à auto-héberger](/docker-debutant-services-auto-heberger/). C'est le bon point de départ avant d'empiler des outils.

## Installation via Docker Compose

Crée un dossier dédié pour Changedetection.io :

```bash
mkdir -p ~/docker/changedetection && cd ~/docker/changedetection
```

Voici le fichier `docker-compose.yml` complet et fonctionnel :

```yaml
version: "3.8"

services:
  changedetection:
    image: ghcr.io/dgtlmoon/changedetection.io:latest
    container_name: changedetection
    restart: unless-stopped
    ports:
      - "5000:5000"
    volumes:
      - changedetection-data:/datastore
    environment:
      - PLAYWRIGHT_DRIVER_URL=ws://playwright-chrome:3000

  playwright-chrome:
    image: dgtlmoon/changedetection.io-playwright-chrome:latest
    container_name: changedetection-chrome
    restart: unless-stopped
    environment:
      - SCREEN_WIDTH=1920
      - SCREEN_HEIGHT=1080
      - SCREEN_DEPTH=24

volumes:
  changedetection-data:
```

Ce Docker Compose lance deux conteneurs :

1. **changedetection** : l'application principale qui expose le dashboard web sur le port 5000
2. **playwright-chrome** : un navigateur headless Chrome qui permet de rendre les sites JavaScript avant analyse (indispensable pour les Single Page Applications)

Lance le tout avec :

```bash
docker compose up -d
```

Attends environ 30 secondes pour que les images se téléchargent et que les conteneurs démarrent. Puis ouvre ton navigateur à l'adresse `http://IP_DE_TON_SERVEUR:5000`.

La première fois, tu n'as pas besoin de login. L'interface est directement accessible. Tu peux ajouter un mot de passe dans les paramètres si tu exposes Changedetection.io sur Internet.

## Configuration : ajouter ton premier site à surveiller

L'interface de Changedetection.io est minimaliste et efficace. Voici comment configurer une surveillance en 3 clics.

### 1. Ajouter une URL

Clique sur le bouton **Watch** en haut à droite. Rentre l'URL de la page à surveiller. Donne-lui un titre clair, genre "Prix MacBook Pro Amazon".

### 2. Définir la fréquence de vérification

Par défaut, Changedetection.io vérifie toutes les minutes. C'est un peu agressif pour la plupart des usages. Règle plutôt sur **15 minutes** pour un prix, **1 heure** pour un blog, ou **1 jour** pour une page qui bouge rarement.

### 3. Choisir le mode de détection

Changedetection.io propose plusieurs modes de récupération du contenu :

- **Plain HTTP requests** : rapide, léger, idéal pour les sites statiques en HTML pur
- **Playwright Chromium** : rend le JavaScript avant analyse. Indispensable pour les sites modernes qui chargent leur contenu dynamiquement (Amazon, React, Vue, etc.)

Dans notre Docker Compose, Playwright est déjà branché. Sélectionne donc **Playwright Chromium** dès que tu veux surveiller un site moderne.

### 4. Filtrer la zone qui t'intéresse (optionnel mais puissant)

Tu ne veux probablement pas qu'une alerte saute parce que le pied de page ou la bannière pub a changé. Changedetection.io te permet de cibler une zone précise avec :

- **CSS Selector** : par exemple `#priceblock_dealprice` pour ne capturer que le prix sur Amazon
- **XPath** : une autre syntaxe pour cibler un élément HTML précis
- **JSON Path** : si tu surveilles une API REST qui retourne du JSON
- **Text filtering** : ne garder que les lignes contenant un mot-clé précis

Pour trouver le bon sélecteur CSS, utilise l'inspecteur de ton navigateur (clic droit sur l'élément → Inspecter → clic droit sur la balise HTML → Copy → Copy selector).

### 5. Configurer les notifications

Va dans **Settings** puis **Notifications**. Changedetection.io supporte une cinquantaine de canaux :

- Email (SMTP)
- Discord, Slack, Telegram, Matrix
- Webhook générique (parfait pour brancher n8n, Uptime Kuma, ou Home Assistant)
- Apprise (une bibliothèque Python qui supporte encore plus de services)

Pour Discord par exemple, tu crée un webhook dans ton serveur, tu copies l'URL, et tu la colles dans le champ correspondant de Changedetection.io. C'est immédiat.

## Cas d'usage concrets

Voici comment utiliser Changedetection.io dans la vraie vie, avec des exemples que tu peux copier-coller.

### Alerte prix

Tu veux savoir quand le prix d'un produit baisse. Tu crées une surveillance sur la fiche produit avec un filtre CSS sur le bloc prix. Dès que le tarif change, tu reçois une notification. Pas besoin d'extension navigateur opaque qui lit tes données de navigation.

### Surveillance de disponibilité

Tu attends un produit en rupture de stock, une place de concert, une ouverture de précommande. Tu surveilles le texte "Rupture de stock" ou "Indisponible". Dès que ce texte disparaît et est remplacé par "Ajouter au panier", tu reçois une alerte instantanée.

### Monitoring de page concurrente

Tu veux savoir quand un concurrent met à jour ses tarifs, change sa page d'accueil, ou publie un nouveau communiqué. Tu surveilles sa page principale ou sa page tarifs avec une fréquence quotidienne. Tu sais exactement quand il bouge, sans passer ton temps à visiter son site.

### Suivi de documentation et releases

Tu attends une mise à jour d'un outil open-source, une nouvelle version d'un firmware, ou une modification dans une doc technique. Tu pointes Changedetection.io sur la page de release GitHub ou la section changelog. Tu es prévenu avant tout le monde.

Tu peux centraliser toutes ces surveillances dans un tableau de bord unique avec [Homer Dashboard](/homer-dashboard-docker-homelab/). C'est le combo parfait : Homer pour voir tes services d'un coup d'oeil, et Changedetection.io pour surveiller le web à ta place.

## Dépannage : quand ça ne marche pas comme prévu

### Le site retourne une erreur 403 ou un captcha

Certains sites (Amazon, Fnac, etc.) détectent les robots et bloquent les requêtes automatiques. Changedetection.io peut contourner ça en utilisant Playwright Chromium avec des options avancées, mais ce n'est pas magique. Solutions :

- Utilise le mode **Playwright Chromium** au lieu du mode HTTP simple
- Augmente le délai entre les requêtes (minimum 5 minutes)
- Utilise un proxy rotatif si tu surveilles massivement (hors scope de ce guide)
- Privilégie les APIs publiques quand elles existent

### Le contenu détecté ne change pas alors que la page a bougé

Vérifie ton filtre CSS ou XPath. Si le sélecteur est trop précis et qu'une classe CSS a changé côté site, Changedetection.io ne verra rien. Utilise le bouton **Preview** pour voir exactement quel contenu est extrait avant de valider.

### Les notifications n'arrivent pas

Dans **Settings → Notifications**, utilise le bouton **Send test notification** pour vérifier que ton canal est bien configuré. C'est la première étape. Si le test passe mais pas les alertes réelles, vérifie que la surveillance est bien activée (toggle vert).

### Le conteneur Playwright Chrome consomme beaucoup de RAM

Chrome headless peut monter à 1 Go de RAM selon les pages rendues. Si tu n'as que 2 Go sur ton serveur, surveille principalement des sites statiques en mode HTTP simple, et n'utilise Playwright que pour les sites JS indispensables. Ou monte la RAM de ton VPS.

### L'interface est lente à charger

Changedetection.io stocke tout dans une base SQLite locale. Avec plusieurs centaines de surveillances, ça peut ramer. Limite-toi à quelques dizaines de pages surveillées, ou migre vers une base de données externe si tu veux scaler (voir la doc officielle pour PostgreSQL).

## Conclusion

Changedetection.io est l'un de ces outils que tu installes une fois et que tu finis par utiliser tous les jours sans y penser. Il fait exactement ce qu'il promet : surveiller le web à ta place, te prévenir au bon moment, et te laisser le contrôle total sur tes données.

En auto-hébergement, il remplit un créneau que peu d'outils open-source couvrent aussi bien. Distill.io et Visualping sont pratiques, mais ils sont cloud, payants et limités. Avec Docker et quelques lignes de YAML, tu construis une solution équivalente, gratuite et illimitée sur ton propre serveur.

Configure ta première surveillance aujourd'hui. Dans une semaine, tu te demanderas comment tu faisais avant.
