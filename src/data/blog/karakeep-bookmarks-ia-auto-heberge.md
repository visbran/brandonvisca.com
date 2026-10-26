---
title: "Karakeep Docker : bookmarks avec tagging IA auto-hébergé"
description: "Déploie Karakeep Docker, le gestionnaire de bookmarks open source avec tagging IA automatique : guide complet d'installation et de sécurisation."
pubDatetime: "2026-10-26T11:02:11+01:00"
modDatetime: "2026-10-25T08:00:00.000Z"
author: Brandon
tags:
  - auto-hebergement
  - automation
  - sauvegarde
  - reverse-proxy
  - intermediaire
featured: false
draft: false
focusKeyword: karakeep docker
faqs:
  - question: "Karakeep Docker consomme-t-il beaucoup de ressources ?"
    answer: "Compte environ 2 Go de RAM pour les trois conteneurs (app, Chrome headless, Meilisearch). Sur un petit VPS ou un LXC homelab, ça tient très bien."
  - question: "Faut-il payer OpenAI pour profiter du tagging automatique ?"
    answer: "Non. Une clé OpenAI accélère le tagging, mais Karakeep fonctionne aussi avec Ollama en local, donc sans dépense ni donnée qui sort de ton réseau."
  - question: "Peut-on migrer ses bookmarks depuis Hoarder, Linkding ou le navigateur ?"
    answer: "Oui. Karakeep est l'ex-Hoarder, la doc officielle fournit un guide de migration direct, et l'import Netscape HTML couvre Chrome, Firefox et la plupart des gestionnaires."
---
> 💡 **TL;DR**
> - Karakeep (ex-Hoarder) archive liens, notes, images et PDF, puis les tague automatiquement avec de l'IA, locale ou via OpenAI
> - Stack Docker Compose à 3 conteneurs (app, Chrome headless, Meilisearch) : environ 2 Go de RAM, port 3000, licence AGPL-3.0
> - Extension navigateur, recherche plein texte quasi instantanée, et import direct depuis Hoarder, Chrome ou Pinboard

## Karakeep, le gestionnaire de bookmarks qui lit tes liens à ta place

Tu as un dossier "À lire plus tard" avec 400 onglets jamais rouverts ? Un Pocket qui te fait les gros yeux depuis que Mozilla a changé trois fois son modèle de tarification ? Chez moi, le problème était simple : je sauvegardais des liens, mais je ne les retrouvais jamais parce que je ne les avais pas tagués au moment de les enregistrer. Et taguer à la main, soyons honnêtes, ça ne survit jamais à la troisième semaine.

**Karakeep Docker** règle ce problème précis. C'est un gestionnaire de bookmarks auto-hébergé, développé par Localhost Labs Ltd, qui capture n'importe quoi (lien, note, image, PDF), en garde une copie lisible, puis lance un modèle de langage pour générer les tags et un résumé tout seul. Le projet s'appelait auparavant Hoarder : le rebranding a changé le nom et le dépôt, pas le fonctionnement. La licence est AGPL-3.0, donc totalement libre tant que tu ne revends pas un service encapsulé autour.

Dans ce guide, on installe Karakeep Docker avec la stack officielle, on configure le tagging IA (avec ou sans clé OpenAI), on sécurise l'accès et on prévoit la sauvegarde avant que tu n'y mettes 2000 liens.

## Table des matières

## Karakeep Docker : la stack Compose complète

Karakeep Docker ne tient pas dans un seul conteneur. La stack officielle en embarque trois : l'application web, un Chrome headless pour charger les pages et en faire une capture fidèle, et Meilisearch pour la recherche plein texte. C'est ce qui le distingue d'un Linkding ou d'un Shaarli minimaliste, au prix d'un peu plus de RAM.

Crée un dossier de projet, puis le fichier `docker-compose.yml` :

```yaml
services:
  web:
    image: ghcr.io/karakeep-app/karakeep:${KARAKEEP_VERSION:-release}
    restart: unless-stopped
    volumes:
      - data:/data
    ports:
      - "3000:3000"
    env_file:
      - .env
    environment:
      MEILI_ADDR: http://meilisearch:7700
      BROWSER_WEB_URL: http://chrome:9222
      DATA_DIR: /data
  chrome:
    image: ghcr.io/karakeep-app/karakeep-chrome:release
    restart: unless-stopped
  meilisearch:
    image: getmeili/meilisearch:v1.41.0
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - meilisearch:/meili_data

volumes:
  data:
  meilisearch:
```

**Ce que fait chaque bloc :**

- `web`, L'application elle-même, sur le port 3000. `KARAKEEP_VERSION` te laisse choisir entre `release` (dernière stable) et un numéro fixe, utile si tu veux figer les montées de version sur un homelab de production.
- `chrome`, Le navigateur headless qui charge chaque page bookmarkée pour en extraire le titre, une image de prévisualisation et, si tu actives l'option, un snapshot complet.
- `meilisearch`, Le moteur de recherche qui rend la recherche plein texte quasi instantanée, même avec plusieurs milliers de bookmarks.
- Les volumes `data` et `meilisearch`, Sans eux, tout repart à zéro à la moindre recréation de conteneur.

Si tu gères déjà plusieurs stacks Compose sur ton serveur, c'est le genre de setup Karakeep Docker à 3 services où une interface comme [Dockge](/dockge-docker-gestionnaire-stacks-compose/) t'évite de perdre le fil entre les `.env` de chaque projet.

## Configuration : secrets, clé IA et choix du moteur

Avant de lancer Karakeep Docker, crée le fichier `.env` dans le même dossier :

```bash
DATA_DIR=/data
MEILI_ADDR=http://127.0.0.1:7700
MEILI_MASTER_KEY=change_moi_avec_openssl
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=change_moi_aussi
```

Génère les deux secrets avec `openssl` plutôt que de taper au hasard :

```bash
openssl rand -base64 36
```

Lance une fois pour `NEXTAUTH_SECRET`, une seconde fois pour `MEILI_MASTER_KEY`. Remplace `NEXTAUTH_URL` par l'adresse réelle que tu utiliseras pour accéder à l'instance, sinon l'authentification refuse de coopérer.

⚠️ **Sur le tagging IA** : sans configuration supplémentaire, Karakeep Docker tague à vide. Deux options s'ouvrent ici.

- **Avec OpenAI** : ajoute `OPENAI_API_KEY=sk-...` dans le `.env`. Le tagging devient immédiat et plutôt pertinent, mais chaque bookmark part vers une API tierce et génère un coût, même faible.
- **En local avec Ollama** : si tu fais déjà tourner Ollama sur ton réseau pour d'autres usages, pointe Karakeep vers son endpoint. Rien ne quitte ton infra, le tagging est gratuit, mais la qualité dépend directement du modèle choisi et de la RAM disponible pour le faire tourner correctement.

💡 Mon choix perso : Ollama avec un petit modèle quantifié suffit largement pour du tagging de bookmarks. Pas besoin d'un modèle 70B pour deviner qu'un article sur Caddy mérite le tag "reverse-proxy".

Démarre la stack Karakeep Docker :

```bash
docker compose up -d
docker compose logs -f web
```

Rends-toi sur `http://IP-DU-SERVEUR:3000`, crée ton compte admin, et tu es dedans.

## Premiers pas : extension, bookmarklet et import

Une fois connecté à Karakeep Docker, trois réflexes à prendre tout de suite :

1. **Installe l'extension navigateur** (Chrome, Firefox ou Safari) depuis les paramètres de Karakeep. Un clic sur l'icône sauvegarde la page en cours, pas besoin d'ouvrir l'interface web.
2. **Importe l'historique existant.** Karakeep lit le format Netscape Bookmark HTML, celui qu'exportent Chrome, Firefox et la quasi-totalité des gestionnaires de bookmarks. Si tu viens de Hoarder, la documentation officielle propose un guide de migration dédié, sans repasser par un export-import manuel.
3. **Active l'archive de page complète** si l'espace disque ne te fait pas peur. C'est ce qui te sauve quand un lien bookmarké en 2024 renvoie un 404 en 2026.

Dès les premiers bookmarks ajoutés, le tagging IA se déclenche en tâche de fond. Laisse-lui quelques secondes : le modèle doit charger la page, en extraire le contenu utile, puis générer les tags. Si rien ne se passe, le premier réflexe est de vérifier les logs du conteneur `web`, c'est là que les erreurs de clé API ou d'endpoint Ollama mal configuré apparaissent en clair. Si tu préfères surveiller tes conteneurs sans taper de commandes, [Dozzle](/dozzle-docker-visionneuse-logs-web/) affiche les logs en direct dans une interface web, pratique pour repérer tout de suite un tagging qui boucle en erreur.

## Sécuriser l'accès et sauvegarder tes données

Karakeep Docker n'embarque pas de TLS natif, donc le port 3000 ne doit jamais traîner directement sur internet. Place-le derrière un reverse proxy :

```caddyfile
bookmarks.tondomaine.com {
    reverse_proxy localhost:3000
}
```

Si tu utilises déjà Traefik ou Nginx Proxy Manager, le principe reste identique : un seul point d'entrée HTTPS, le port 3000 qui reste strictement interne au réseau Docker ou au LAN.

✅ **Checklist avant de bookmarker sérieusement :**

- Reverse proxy HTTPS en place, port 3000 fermé côté pare-feu externe
- `NEXTAUTH_SECRET` et `MEILI_MASTER_KEY` changés, pas laissés à leur valeur d'exemple
- Sauvegarde planifiée du volume `data` (base de données, archives de pages, images) et du volume `meilisearch` si tu ne veux pas réindexer des milliers de bookmarks à la main

Une sauvegarde simple suffit pour démarrer :

```bash
docker compose stop
tar czf karakeep-backup-$(date +%F).tar.gz data meilisearch
docker compose start
```

Arrêter la stack le temps du `tar` évite une base SQLite corrompue en cours d'écriture. Si tu veux une solution planifiée plutôt qu'un script à lancer à la main, un outil de sauvegarde par snapshot fera le travail récurrent pendant que tu passes à autre chose.

## Karakeep face aux alternatives : Linkding, Pocket, Raindrop

Karakeep n'est pas le seul gestionnaire de bookmarks auto-hébergé, et il ne cherche pas à l'être pour tous les usages.

- **Linkding** : plus léger, SQLite seul, pas de tagging IA ni de Chrome headless. Si tu veux juste ranger des liens avec des tags manuels et une empreinte minimale, c'est le choix le plus économe en ressources.
- **Pocket (Mozilla)** : apps mobiles soignées, mais tes données de lecture nourrissent un algorithme de recommandations que tu n'as pas demandé. Zéro contrôle sur l'infra.
- **Raindrop.io** : interface très travaillée côté SaaS, plan gratuit limité en fonctionnalités avancées, et encore une fois tes données hébergées ailleurs que chez toi.

Le vrai argument de Karakeep Docker, c'est le tagging automatique couplé à l'auto-hébergement. Aucune des alternatives citées ne propose les deux en même temps sans payer un abonnement ou sans confier ses liens à un tiers. Si ton usage est simplement de ranger des URL avec deux ou trois tags manuels, Linkding reste plus sobre. Si tu veux que l'outil comprenne le contenu de ce que tu sauvegardes, Karakeep justifie ses conteneurs en plus.

Dans une stack de veille personnelle, Karakeep Docker s'intègre bien à côté d'un lecteur RSS comme [FreshRSS](/freshrss-docker-lecteur-rss/) : les flux remontent les articles, Karakeep garde ceux que tu veux relire plus tard avec un tag qui tient debout. Et si l'archivage te plaît pour les bookmarks, la même logique de capture et de recherche plein texte s'applique à tes documents administratifs avec [Paperless-ngx](/paperless-ngx-docker-guide-auto-hebergement/), un autre outil qui transforme du contenu brut en quelque chose de retrouvable.

## Conclusion

Karakeep Docker coûte un peu plus de ressources qu'un simple gestionnaire de bookmarks, mais c'est précisément le prix du tagging automatique et de la recherche plein texte qui fonctionnent vraiment. Trois conteneurs, un `.env` avec deux secrets à générer, un reverse proxy devant, et tu as un outil qui range tes liens à ta place au lieu de te culpabiliser avec un dossier "à lire plus tard" qui ne redescend jamais.

Si tu pars de zéro, commence en local avec Ollama pour le tagging avant d'envisager une clé OpenAI, tu verras vite si la qualité te suffit. Et quoi que tu choisisses, ne saute pas l'étape sauvegarde : un volume Docker sans copie externe, c'est un historique de bookmarks qui ne pèse rien jusqu'au jour où le disque lâche.
