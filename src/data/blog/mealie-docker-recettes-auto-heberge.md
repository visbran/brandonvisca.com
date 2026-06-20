---
title: "Mealie Docker : gestionnaire de recettes auto-hébergé"
description: "Mealie Docker : déploie un gestionnaire de recettes auto-hébergé avec Docker Compose. Guide complet, variables d'environnement et comparatif avec Tandoor."
pubDatetime: "2026-06-20T08:00:00.000Z"
modDatetime: "2026-06-20T08:00:00.000Z"
author: Brandon
tags:
  - mealie
  - docker
  - auto-hebergement
  - homelab
  - intermediaire
featured: false
draft: false
focusKeyword: mealie docker
faqs:
  - question: "Mealie est-il gratuit et open-source ?"
    answer: "Oui. Mealie est publié sous licence AGPL-3.0. Le code source est disponible sur GitHub, le projet compte plus de 12 000 stars et est activement maintenu."
  - question: "Mealie ou Tandoor, lequel choisir ?"
    answer: "Mealie est plus simple à déployer, plus léger et bénéficie d'une UX plus moderne. Tandoor est plus complet sur la planification de repas et les listes de courses. Choisis Mealie pour la simplicité, Tandoor si tu veux des fonctionnalités avancées de planification."
  - question: "Peut-on importer des recettes depuis un site web ?"
    answer: "Oui. Mealie scrap automatiquement les recettes depuis la plupart des sites de cuisine. Il suffit de coller l'URL et Mealie extrait les ingrédients, les étapes, les images et les temps de cuisson."
  - question: "Quelle configuration matérielle est nécessaire ?"
    answer: "Pour une utilisation familiale (1 à 20 utilisateurs), SQLite suffit avec 1 cœur CPU, 1 Go de RAM et quelques Go de stockage. Pour des instances plus grosses ou avec NAS, PostgreSQL est recommandé."
ogImage: ""
---
> 💡 **TL;DR**
> - Mealie est un gestionnaire de recettes auto-hébergé open-source sous licence AGPL-3.0
> - Tu l'installes en 10 minutes avec **Mealie Docker**, SQLite intégré et une interface Vue.js
> - Import automatique de recettes depuis n'importe quel site web, planification de repas, listes de courses
> - Alternative plus légère et moderne à Tandoor pour les familles et les petites équipes
> - Docker Compose complet, variables d'environnement détaillées et comparatif des alternatives ci-dessous

## Table des matières

## Pourquoi un gestionnaire de recettes auto-hébergé ?

Tu connais la scène. Tu trouves une recette géniale sur un site de cuisine. Tu la bookmark, elle disparaît dans tes 400 onglets ouverts. Trois semaines plus tard, le site a changé de design, la recette est derrière un paywall, ou pire, le site a fermé. Ta recette est partie avec lui.

Les solutions cloud type Paprika ou les apps mobiles propriétaires ne règlent pas le problème. Tes recettes vivent sur leurs serveurs, formatées dans leurs formats fermés, et si l'app disparaît un jour, tu perds tout. Sans parler du tracking : ces apps savent exactement ce que tu cuisines, quand tu cuisines et combien de personnes tu nourris. Des données parfaites pour te vendre des produits ou alimenter des profils publicitaires.

Mealie est la réponse technique à ce problème. C'est un gestionnaire de recettes auto-hébergé développé en Python (backend API REST) et Vue.js (frontend réactif), sous licence AGPL-3.0. Il scrape automatiquement les recettes depuis des centaines de sites, les stocke dans une base de données locale, et te donne une interface propre pour organiser, planifier et cuisiner. Tes recettes restent chez toi, toujours accessibles, même si Internet coupe.

Dans mon [guide des services essentiels à auto-héberger avec Docker](/docker-debutant-services-auto-heberger/), je recommande de commencer par les outils de productivité du quotidien. **Mealie Docker** rentre pile dans cette catégorie : il remplace un usage quotidien (chercher des recettes, les organiser, les retrouver) par une solution que tu contrôles totalement. Après Vaultwarden pour les mots de passe et Memos pour les notes, Mealie est souvent le troisième service que je déploie sur un nouvel homelab.

## Qu'est-ce que Mealie exactement ?

Mealie est né d'un constat simple : les gestionnaires de recettes existants sont soit trop basiques (des dossiers de bookmarks), soit trop complexes (des apps lourdes avec synchronisation cloud obligatoire). **Mealie Docker** vise le juste milieu : une interface web élégante, une API REST complète, et un scraper intelligent qui comprend la structure des recettes sur le web.

Voici ce qu'il propose concrètement :

- **Import automatique par URL** : tu colles l'adresse d'une recette, Mealie va chercher les ingrédients, les étapes, les temps de préparation/cuisson, les portions, les images et les tags. Ça marche avec la plupart des sites de cuisine francophones et anglophones.
- **Éditeur de recettes intégré** : pour tes recettes familiales ou celles que tu inventes, un éditeur WYSIWYG te permet de tout saisir manuellement avec mise en forme.
- **Planification de repas** : un calendrier hebdomadaire où tu glisses-déposes tes recettes. Mealie génère automatiquement la liste des courses à partir des repas planifiés.
- **Listes de courses** : générées automatiquement depuis le calendrier de repas ou manuellement. Tu coches les articles au fur et à mesure de tes achats.
- **Gestion des stocks** : suivi des ingrédients disponibles dans ta cuisine. Utile pour éviter d'acheter du paprika alors que tu en as déjà trois pots.
- **Multi-utilisateur** : plusieurs comptes utilisateurs avec rôles (admin, utilisateur). Chaque famille peut avoir son propre espace.
- **Partage public/privé** : certaines recettes peuvent être partagées via une URL publique sans nécessiter de compte. Pratique pour envoyer une recette à un ami.
- **Conversion des unités** : Mealie convertit automatiquement les unités (cuillères à soupe en grammes, Farenheit en Celsius, etc.).
- **Nutrition** : estimation automatique des valeurs nutritionnelles basée sur les ingrédients.
- **Tags et catégories** : organisation flexible par tags personnalisés, catégories et outils de cuisine.
- **Recherche avancée** : recherche par ingrédient, catégorie, tag ou texte libre. Avec PostgreSQL, la recherche floue (fuzzy search) est disponible.
- **API REST complète** : pour automatiser l'import, la planification ou la synchronisation avec d'autres outils.
- **Thème clair/sombre** : interface moderne adaptative.

L'image officielle `ghcr.io/mealie-recipes/mealie:v3.19.2` (version stable au moment de la rédaction) est maintenue activement et supporte amd64 ainsi qu'arm64. L'équipe Mealie recommande de toujours spécifier un tag de version explicite plutôt que `latest`, afin de contrôler les mises à jour et lire les notes de release.

Si tu cherches un outil de notes rapide pour noter tes idées de recettes en cours de développement, j'ai aussi couvert [Memos avec Docker](/memos-docker-notes-auto-heberge/), un bloc-notes auto-hébergé ultra-léger et minimaliste.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose installés (Docker Engine 24+ recommandé)
- 1 cœur CPU et 1 Go de RAM minimum (2 Go recommandés pour être confortable)
- Quelques Go d'espace disque pour la base de données et les images de recettes
- Un nom de domaine ou sous-domaine pointant vers ton serveur si tu veux HTTPS
- Un reverse proxy (Caddy, Traefik ou Nginx Proxy Manager) pour gérer les certificats SSL

Mealie est raisonnablement léger. Pour une utilisation familiale avec SQLite, un VPS modeste ou même un Raspberry Pi 4 suffisent amplement. L'équipe recommande de fixer une limite mémoire explicite de 1000 Mo car Python peut pré-allouer plus de RAM que nécessaire sur des machines bien pourvues.

Si tu débutes avec Docker et que les concepts de volumes, réseaux et reverse proxy te semblent flous, commence par mon article sur [les services essentiels à auto-héberger avec Docker](/docker-debutant-services-auto-heberger/). Les bases y sont expliquées clairement, et Mealie est un excellent second service pour mettre en pratique.

## Déploiement Mealie Docker avec SQLite

Pour une utilisation familiale de 1 à 20 utilisateurs, SQLite est le choix parfait. Zero configuration, zero dépendance externe, et des performances excellentes pour cette échelle.

Crée un dossier dédié et un fichier `docker-compose.yml` :

```bash
mkdir -p ~/mealie && cd ~/mealie
```

Voici le Docker Compose complet et prêt à l'emploi pour installer **mealie docker** :

```yaml
services:
  mealie:
    image: ghcr.io/mealie-recipes/mealie:v3.19.2
    container_name: mealie
    restart: always
    ports:
      - "9925:9000"
    deploy:
      resources:
        limits:
          memory: 1000M
    volumes:
      - mealie-data:/app/data/
    environment:
      ALLOW_SIGNUP: "false"
      PUID: 1000
      PGID: 1000
      TZ: Europe/Paris
      BASE_URL: https://recettes.tondomaine.com
      TOKEN_TIME: 48
      API_PORT: 9000
      LOG_LEVEL: info

volumes:
  mealie-data:
```

### Explication des variables d'environnement

| Variable | Valeur | Description |
|----------|--------|-------------|
| `ALLOW_SIGNUP` | `"false""` | Désactive l'inscription publique. Tu crées les comptes toi-même. Depuis la version 1.4.0, cette valeur est `false` par défaut pour des raisons de sécurité. |
| `PUID` | `1000` | ID utilisateur Linux pour les permissions sur les fichiers du volume. Doit correspondre à l'utilisateur qui lance Docker. |
| `PGID` | `1000` | ID groupe Linux pour les permissions sur les fichiers du volume. |
| `TZ` | `Europe/Paris` | Fuseau horaire pour les dates et heures des recettes, planifications et logs. |
| `BASE_URL` | `https://recettes.tondomaine.com` | URL publique de ton instance. Utilisée pour les liens dans les notifications et pour l'authentification OIDC si tu l'actives. |
| `TOKEN_TIME` | `48` | Durée de validité des tokens d'authentification en heures. Maximum 9600 heures (400 jours). |
| `API_PORT` | `9000` | Port interne de l'API. Ne change pas cette valeur si tu utilises Docker. Le port exposé sur l'hôte se règle dans `ports`. |
| `LOG_LEVEL` | `info` | Niveau de verbosité des logs : `critical`, `error`, `warning`, `info` ou `debug`. |

Lance le conteneur :

```bash
docker compose up -d
```

Attends une dizaine de secondes que le service démarre, puis accède à `http://IP-du-serveur:9925`. Le premier utilisateur qui s'inscrit devient automatiquement administrateur.

## Déploiement avec PostgreSQL (optionnel)

Si tu prévois de nombreux utilisateurs concurrents, ou si tu stockes les données sur un NAS (Network Attached Storage), PostgreSQL est recommandé. SQLite n'est pas conçu pour fonctionner sur du stockage réseau et peut provoquer des corruptions de données.

```yaml
services:
  mealie:
    image: ghcr.io/mealie-recipes/mealie:v3.19.2
    container_name: mealie
    restart: always
    ports:
      - "9925:9000"
    deploy:
      resources:
        limits:
          memory: 1000M
    volumes:
      - mealie-data:/app/data/
    environment:
      ALLOW_SIGNUP: "false"
      PUID: 1000
      PGID: 1000
      TZ: Europe/Paris
      BASE_URL: https://recettes.tondomaine.com
      DB_ENGINE: postgres
      POSTGRES_USER: mealie
      POSTGRES_PASSWORD: super_secret_password_a_changer
      POSTGRES_SERVER: postgres
      POSTGRES_PORT: 5432
      POSTGRES_DB: mealie
    depends_on:
      postgres:
        condition: service_healthy

  postgres:
    container_name: postgres_mealie
    image: postgres:17
    restart: always
    volumes:
      - mealie-pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: super_secret_password_a_changer
      POSTGRES_USER: mealie
      PGUSER: mealie
      POSTGRES_DB: mealie
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 30s
      timeout: 20s
      retries: 3

volumes:
  mealie-data:
  mealie-pgdata:
```

Variables spécifiques à PostgreSQL :

| Variable | Description |
|----------|-------------|
| `DB_ENGINE` | `"postgres""` pour activer PostgreSQL au lieu de SQLite |
| `POSTGRES_USER` | Nom d'utilisateur PostgreSQL |
| `POSTGRES_PASSWORD` | Mot de passe PostgreSQL (à changer impérativement) |
| `POSTGRES_SERVER` | Nom d'hôte du conteneur PostgreSQL (ici `postgres`) |
| `POSTGRES_PORT` | Port PostgreSQL (5432 par défaut) |
| `POSTGRES_DB` | Nom de la base de données |

## Configuration initiale et premiers pas

**1. Créer le compte administrateur**
Le premier utilisateur inscrit obtient automatiquement les droits admin. Choisis un mot de passe fort et un email valide. Active le 2FA (TOTP) dans les paramètres de sécurité si ton instance est exposée sur Internet.

**2. Importer ta première recette**
Clique sur "Créer une recette", choisis "Importer depuis une URL", et colle l'adresse d'un site de cuisine. Mealie va scraper automatiquement les ingrédients, les étapes, les images et les métadonnées. Teste avec plusieurs sites pour vérifier la compatibilité. La plupart des sites utilisant du schema.org Recipe sont supportés nativement.

**3. Créer une recette manuelle**
Pour les recettes familiales transmises de génération en génération, utilise l'éditeur intégré. Tu peux ajouter des images, formater les étapes, indiquer les temps et les portions. Les recettes manuelles sont souvent plus jolies car tu contrôles totalement la mise en page.

**4. Organiser avec des tags**
Crée une structure de tags cohérente dès le début. Voici ce que j'utilise :
- `rapide` : moins de 30 minutes
- `vegetarien`, `vegan`, `sans-gluten` : régimes alimentaires
- `hiver`, `ete`, `aperitif` : saisons et occasions
- `batch` : recettes pour préparer en grande quantité et congeler

**5. Tester le calendrier de repas**
Glisse une recette sur un jour du calendrier hebdomadaire. Mealie calcule automatiquement la liste de courses nécessaire. C'est l'une des fonctionnalités les plus appréciées des familles qui planifient leurs repas à l'avance.

**6. Configurer les thèmes (optionnel)**
Mealie permet de personnaliser les couleurs via des variables d'environnement. Tu peux changer les couleurs primaires, secondaires, d'accent, et les couleurs de messages d'erreur/succès pour les modes clair et sombre.

## Mealie vs Tandoor vs les alternatives

|| Critère | Mealie | Tandoor | Paprika | Nextcloud Cookbook |
||---------|--------|---------|---------|-------------------|
|| **Licence** | AGPL-3.0 | MIT-like (avec restrictions) | Propriétaire | AGPL-3.0 |
|| **Auto-hébergé** | Oui | Oui | Non (sync cloud) | Oui (via app Nextcloud) |
|| **Gratuit** | Totalement | Totalement | Payant (app + sync) | Totalement |
|| **Interface** | Moderne, Vue.js | Fonctionnelle, Django | Native iOS/Android | Intégrée Nextcloud |
|| **Import URL** | Excellent, scrape intelligent | Bon, parfois moins fiable | Excellent (payant) | Bon |
|| **Planification repas** | Oui, calendrier hebdo | Oui, très complet | Oui | Non |
|| **Liste de courses** | Oui, auto-générée | Oui, très avancée | Oui | Non |
|| **Gestion des stocks** | Basique | Avancée | Non | Non |
|| **Multi-utilisateur** | Oui, avec rôles | Oui | Non (compte individuel) | Oui (via Nextcloud) |
|| **API REST** | Complète | Complète | Non | Oui (WebDAV) |
|| **Recherche floue** | Oui (avec PostgreSQL) | Non | Non | Non |
|| **Ressources RAM** | ~1000 Mo (limite recommandée) | ~1500 Mo | N/A (cloud) | Variable (Nextcloud lourd) |
|| **Base de données** | SQLite ou PostgreSQL | PostgreSQL | Cloud propriétaire | MySQL/PostgreSQL (Nextcloud) |
|| **App mobile** | Web responsive (PWA) | Web responsive | Native iOS/Android | Nextcloud Files |
|| **Facilité de déploiement** | Très simple (Docker) | Simple (Docker) | N/A (app store) | Complexe (Nextcloud complet) |

Mon verdict pour un homelab ou une utilisation familiale :

- **Mealie** : le meilleur compromis entre simplicité de déploiement, interface moderne et fonctionnalités complètes. L'import par URL est fiable, la planification de repas est intuitive, et la consommation de ressources est raisonnable. C'est mon choix par défaut pour un usage familial.
- **Tandoor** : si tu as besoin d'une gestion avancée des stocks, de planifications complexes sur plusieurs semaines, ou de listes de courses très détaillées. Tandoor est plus complet mais l'interface est moins moderne et le déploiement demande un peu plus d'attention.
- **Paprika** : si tu veux une app native iOS/Android avec synchronisation cloud et que tu t'en fiches de l'auto-hébergement. C'est payant mais très bien fait. Tes recettes ne sont pas chez toi.
- **Nextcloud Cookbook** : si tu as déjà Nextcloud et que tu veux tout centraliser. L'app est correcte mais beaucoup moins riche que Mealie ou Tandoor. Lourd à déployer juste pour des recettes.

Pour sécuriser ton serveur et protéger tes services exposés, j'ai aussi publié un guide sur [AdGuard Home avec Docker](/adguard-home-docker-guide-2026/) qui te permet de bloquer les trackers et les publicités à l'échelle de tout ton réseau.

## Sécuriser l'accès et les données

**HTTPS partout**
Ne laisse jamais Mealie en HTTP si tu l'exposes sur Internet. Ton reverse proxy doit forcer le HTTPS, activer HSTS et bloquer les versions obsolètes de TLS. Caddy gère ça nativement avec une ligne.

**Sauvegardes automatisées**
Le volume `mealie-data` contient la base de données (SQLite ou pas) et les images des recettes. C'est le seul dossier à sauvegarder :

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar czf "/backup/mealie_$DATE.tar.gz" /var/lib/docker/volumes/mealie_mealie-data/_data
```

Si tu utilises PostgreSQL, sauvegarde aussi le volume `mealie-pgdata`. Pour une solution de sauvegarde complète et chiffrée vers le cloud ou un NAS, [Duplicati avec Docker](/duplicati-docker-sauvegarde/) est un excellent choix.

**Mises à jour**
L'équipe Mealie publie régulièrement des versions. Mets à jour une fois par mois en lisant les notes de release sur GitHub :

```bash
cd ~/mealie
docker compose pull
docker compose up -d
```

**Authentification double facteur**
Mealie supporte le TOTP (Google Authenticator, Authy, Bitwarden Authenticator, etc.). Active-le dans les paramètres de sécurité.

**Restreindre les inscriptions**
Garde `ALLOW_SIGNUP: "false""` et crée les comptes utilisateurs manuellement depuis le panneau d'administration.

**Authentification externe (optionnel)**
Mealie supporte LDAP et OpenID Connect (OIDC) depuis la version 1.4.0. Si tu as déjà un serveur d'authentification centralisé (Authelia, Keycloak, Authentik), tu peux y brancher Mealie pour une authentification unique (SSO).

## Intégrations et astuces avancées

**Utiliser la recherche floue avec PostgreSQL**
Si tu déploies avec PostgreSQL, la recherche floue est activée automatiquement. Elle te permet de trouver une recette même si tu ne te souviens plus exactement du nom. "ratatouille" trouvera "ratatouille provençale" et "ratatouille au four".

**Exporter les recettes**
Mealie peut exporter tes recettes au format JSON standardisé. C'est utile pour migrer vers un autre outil ou pour archiver tes recettes en dehors de Mealie. Le format est basé sur schema.org Recipe, donc compatible avec la plupart des outils du marché.

**Partage public avec URL courte**
Chaque recette peut être rendue publique avec une URL partageable. L'ami qui reçoit le lien voit la recette complète sans besoin de compte. Parfait pour partager ta recette de brownies avec le monde entier.

**Utiliser comme PWA sur mobile**
L'interface web de Mealie est responsive et fonctionne très bien sur mobile. Ajoute-la à l'écran d'accueil de ton téléphone pour une expérience proche d'une app native. Pas besoin d'app store, pas de tracking SDK.

**Intégration avec l'API REST**
L'API REST de Mealie est documentée et accessible directement depuis l'interface. Tu peux automatiser l'import de recettes depuis tes scripts, synchroniser la planification de repas avec d'autres calendriers, ou générer des listes de courses depuis des routines domotiques.

**Personnalisation des couleurs**
Via les variables d'environnement, tu peux changer toute la palette de couleurs de Mealie. Utile pour adapter l'interface à tes goûts ou à la charte graphique de ton homelab.

**Gestionnaire de fichiers en complément**
Pour stocker les photos de tes plats finis, les scans de vieilles recettes manuscrites ou les PDF de magazines de cuisine, [File Browser avec Docker](/filebrowser-docker-gestionnaire-fichiers/) s'intègre parfaitement à côté de Mealie. Tu stockes les fichiers dans File Browser et tu références les liens dans tes notes de recettes.

## FAQ

**Mealie est-il traduit en français ?**
Oui, l'interface est entièrement traduite en français et dans de nombreuses autres langues. La langue se change dans les paramètres utilisateur.

**Puis-je importer des recettes depuis Paprika, ChefTap ou d'autres apps ?**
Mealie supporte l'import de fichiers JSON au format schema.org Recipe. Si ton app actuelle exporte dans ce format, la migration est directe. Sinon, des scripts de conversion existent dans la communauté.

**Les recettes importées restent-elles si le site source disparaît ?**
Oui, une fois importée dans Mealie, la recette est entièrement stockée dans ta base de données locale avec ses images. Le site source peut fermer, tu gardes ta recette.

**Puis-je héberger Mealie sur un Raspberry Pi ?**
Oui, l'image supporte ARM64. Un Raspberry Pi 4 avec 2 Go de RAM suffit pour une utilisation familiale avec SQLite. Prévois un stockage externe rapide si tu stockes beaucoup d'images haute résolution.

**Mealie gère-t-il les allergies alimentaires ?**
Tu peux taguer les recettes avec des tags comme `sans-gluten`, `sans-arachide` ou `sans-lactose`. Mealie ne fait pas d'analyse automatique des allergènes, mais la recherche par tag te permet de filtrer rapidement.

**Puis-je scanner des recettes manuscrites ?**
Pas directement dans Mealie. Mais tu peux scanner tes recettes manuscrites avec ton téléphone, les stocker dans [File Browser avec Docker](/filebrowser-docker-gestionnaire-fichiers/), et créer une recette dans Mealie avec un lien vers le scan.
