---
title: "Paperless-ngx : votre bureau numérique auto-hébergé avec OCR"
description: Guide complet pour installer Paperless-ngx avec Docker Compose. Archivez, numérisez et retrouvez facilement vos documents dans votre bureau numérique.
pubDatetime: 2026-05-31 06:00:00+00:00
author: Brandon Visca
tags:
  - debutant
  - docker
  - auto-hebergement
  - administration-systeme
  - productivite
  - ocr
featured: false
draft: false
ogImage: ""
---
## Pourquoi vos documents méritent mieux qu'un tiroir en plastique

Tu connais le coup. Tous les ans tu reçois :
- ton avis d'imposition,
- ton attestation d'assurance habitation,
- la facture de ton opérateur internet qui augmente mystérieusement,
- et ce contrat de travail que tu as signé en catastrophe.

Tu les mets dans un classeur. Ou pire, dans un tiroir avec les tickets de caisse de 2019. Et quand tu dois retrouver ton dernier relevé de compteur EDF ? C'est la chasse au trésor.

Paperless-ngx, c'est la fin de cette époque. C'est un **bureau numérique auto-hébergé** qui ingère tes PDF et tes scans, leur applique un OCR, les classe automatiquement et te permet de les retrouver en deux secondes avec une simple recherche texte. Le tout chez toi, sans passer par Google Drive ou Dropbox. Parce que tes fiches de paie, c'est pas le business model de Silicon Valley.

Ce guide t'explique comment le faire tourner avec Docker Compose en moins de 20 minutes. Si tu débutes avec Docker, commence peut-être par [mon article sur les services essentiels à auto-héberger](/docker-debutant-services-auto-heberger/) pour comprendre l'écosystème.

## Qu'est-ce que Paperless-ngx exactement ?

Paperless-ngx est un fork communautaire très actif du projet original Paperless. Il est sous licence **GPL-3.0** et maintenu par une équipe de passionnés. Pas de startup derrière, pas d'exit stratégique, juste du code open-source qui fait le job.

Voici ce qu'il fait concrètement :
- **OCR automatique** : il extrait le texte de tes PDF et de tes images (factures, courriers, contrats) pour les rendre indexables. Il supporte le français, l'anglais, l'allemand et plein d'autres langues.
- **Classification intelligente** : il devine le type de document (facture, contrat, etc.) et peut suggérer des tags et des correspondants.
- **Workflow de consommation** : tu déposes un fichier dans un dossier, il disparaît et réapparaît 30 secondes plus tard proprement classé dans l'interface web.
- **Recherche full-text** : tu cherches "EDF janvier 2024" et il te ressort le bon PDF avec le montant surligné.
- **Gestion des droits** : multi-utilisateurs, groupes, permissions granulaires.
- **API REST** : pour brancher des outils comme [n8n](/n8n-docker-workflow-automation/) et automatiser des pipelines.
- **Consommation email** : il peut récupérer automatiquement les pièces jointes d'une adresse email dédiée.
- **Versioning** : il conserve l'original et le PDF OCRisé.

En gros, c'est Evernote pour les gens qui n'ont pas envie de payer un abonnement et qui aiment savoir où dorment leurs données.

## Prérequis matériels et logiciels

L'avantage de Paperless-ngx, c'est qu'il n'est pas gourmand. Un **Raspberry Pi 4 avec 4 Go de RAM** peut tenir la route pour un usage familial. Pour un usage plus soutenu (PME, gros volumes) :
- **2 cœurs CPU** (l'OCR utilise du CPU, c'est inévitable),
- **4 Go de RAM minimum**, 8 Go recommandés,
- **20 Go d'espace disque** pour le système, puis autant que tes documents en prennent.

Sur le plan logiciel, il te faut :
- Docker et Docker Compose installés (voir [mon guide Docker débutant](/docker-debutant-services-auto-heberger/)),
- Un accès SSH à ton serveur (ou ton NAS compatible Docker),
- Un nom de domaine (optionnel mais recommandé, via un reverse proxy comme Traefik ou Nginx Proxy Manager).

## Le docker-compose.yml complet

Voici une stack complète et fonctionnelle. Elle inclut Paperless-ngx, une base PostgreSQL pour la métadonnée, et Redis pour le cache et les files d'attente de traitement. C'est la configuration recommandée par les développeurs.

```yaml
version: "3.8"

services:
  broker:
    image: docker.io/library/redis:7
    container_name: paperless-redis
    restart: unless-stopped
    volumes:
      - ./redisdata:/data

  db:
    image: docker.io/library/postgres:16
    container_name: paperless-db
    restart: unless-stopped
    volumes:
      - ./pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: paperless
      POSTGRES_USER: paperless
      POSTGRES_PASSWORD: changez-moi-svp

  webserver:
    image: ghcr.io/paperless-ngx/paperless-ngx:2.20
    container_name: paperless
    restart: unless-stopped
    depends_on:
      - db
      - broker
    ports:
      - "8000:8000"
    volumes:
      - ./data:/usr/src/paperless/data
      - ./media:/usr/src/paperless/media
      - ./export:/usr/src/paperless/export
      - ./consume:/usr/src/paperless/consume
    environment:
      PAPERLESS_REDIS: redis://broker:6379
      PAPERLESS_DBHOST: db
      PAPERLESS_DBUSER: paperless
      PAPERLESS_DBPASS: changez-moi-svp
      PAPERLESS_DBNAME: paperless
      PAPERLESS_SECRET_KEY: changez-moi-aussi-par-une-cle-aleatoire-de-plus-de-50-caracteres
      PAPERLESS_OCR_LANGUAGE: fra
      PAPERLESS_TIME_ZONE: Europe/Paris
      PAPERLESS_ADMIN_USER: admin
      PAPERLESS_ADMIN_PASSWORD: admin-temporaire-a-changer
      PAPERLESS_ADMIN_MAIL: admin@localhost
      USERMAP_UID: 1000
      USERMAP_GID: 1000
```

Quelques explications s'imposent :
- `ghcr.io/paperless-ngx/paperless-ngx:2.20` piste la branche 2.20.x stable. Tu peux aussi utiliser `latest`, mais je préfère pinner pour éviter les surprises.
- `PAPERLESS_OCR_LANGUAGE: fra` active l'OCR en français. Si tu traites des documents bilingues, mets `fra+eng`.
- Le dossier `./consume` est magique : tout fichier déposé dedans est ingéré automatiquement.
- `USERMAP_UID/GID` aligne les permissions avec ton utilisateur Linux (vérifie avec `id` sur ton serveur).

**Important** : remplace absolument les mots de passe et la `SECRET_KEY`. Génère une clé aléatoire avec `openssl rand -hex 32` par exemple.

Besoin de lire des documents Office (.docx, .xlsx) ? Tu peux ajouter les services Gotenberg et Tika. C'est un peu plus lourd, mais ça transforme Paperless en couteau suisse. La documentation officielle a des exemples complets si tu en as besoin.

## Déploiement étape par étape

1. Crée le dossier de travail :
```bash
mkdir -p ~/docker/paperless && cd ~/docker/paperless
```

2. Colle le `docker-compose.yml` ci-dessus dans un fichier (avec `nano docker-compose.yml` ou `vim`), modifie les mots de passe et sauvegarde.

3. Crée les dossiers nécessaires :
```bash
mkdir -p data media export consume redisdata pgdata
```

4. Lances la stack :
```bash
docker compose up -d
```

5. Patientes 30 à 60 secondes le temps que la base de données s'initialise et que Paperless migre son schéma.

6. Vérifie les logs :
```bash
docker compose logs -f webserver
```
Quand tu vois `Listening at: http://0.0.0.0:8000`, c'est bon.

7. Ouvres `http://IP_DE_TON_SERVEUR:8000` dans ton navigateur et connecte-toi avec l'admin créé automatiquement (`admin` / `admin-temporaire-a-changer`).

8. **Change immédiatement ce mot de passe** dans Paramètres > Comptes. Ce n'est pas une option.

## Créer un utilisateur proprement

Si tu préfères ne pas laisser l'utilisateur admin par défaut, supprime-le après avoir créé le tien. Ou utilises la commande officielle pour créer un superuser :

```bash
docker compose exec -T webserver python manage.py createsuperuser
```

Tape ton nom d'utilisateur, ton email et ton mot de passe quand il le demande. C'est plus propre que les variables d'environnement.

## Le workflow quotidien : consommer sans réfléchir

Là où Paperless-ngx devient addictif, c'est dans son **workflow de consommation**. Tu as trois méthodes pour nourrir la bête :

**1. Le dossier consume (le plus simple)**
Tu branches ton scanner en réseau ou tu copies un PDF dans `~/docker/paperless/consume/`. Paperless le détecte, l'OCRise, extrait les dates et les montants, et le classe. 30 secondes plus tard, il est dans l'interface.

**2. L'upload manuel**
Glisser-déposer directement dans l'interface web. Pratique pour un document unique.

**3. L'email (le plus automatique)**
Tu configures une adresse email dédiée (style `paperless@tondomaine.com`). Paperless se connecte en IMAP toutes les 10 minutes, récupère les pièces jointes et les ingère. Parfait pour les factures envoyées par mail.

## Les fonctionnalités qui font vraiment la différence

### Les Tags et les Correspondants
Tu peux créer des règles qui appliquent automatiquement un tag "Facture" dès que le document contient le mot "TVA". Ou associer un correspondant "EDF" à tout document venant de `edf.fr`. C'est comme des filtres Gmail, mais pour ton classeur.

### Les Vues personnalisées
Tu prépares ta déclaration d'impôts ? Crée une vue qui affiche uniquement les documents tagués "Impôts" datant de l'année N-1. Fini de scroller dans 400 PDF.

### Les Workflows avancés
Dans les dernières versions, tu peux créer des règles conditionnelles : "Si le document contient 'rappel' et vient de 'ameli.fr', alors assigne le tag 'Santé' et le correspondant 'CPAM'". C'est ce qui transforme Paperless d'un simple stockage en un vrai classeur intelligent.

### L'API REST
Tout est contrôlable via API. Tu veux automatiser l'envoi de documents depuis [Nextcloud](/nextcloud-docker-installation-complete-2025/) ? Possible. Brancher un webhook [n8n](/n8n-docker-workflow-automation/) pour archiver les factures reçues par email ? Facile. L'API est documentée directement dans l'interface, onglet "API".

## Intégrations : connecter Paperless au reste de ton écosystème

Paperless-ngx n'est pas une île. Il s'intègre naturellement dans un homelab :
- Avec **[Nextcloud](/nextcloud-docker-installation-complete-2025/)** : synchronise un dossier Nextcloud avec le dossier `consume` de Paperless via un lien symbolique ou un montage bind. Les documents uploadés sur Nextcloud sont automatiquement OCRisés.
- Avec **[Vaultwarden](/vaultwarden-docker-gestionnaire-mots-de-passe/)** : stocke ton mot de passe admin Paperless dans ton gestionnaire de mots de passe. Évidence, mais on ne le répète jamais assez.
- Avec **Traefik ou Nginx Proxy Manager** : expose Paperless en HTTPS avec un certificat Let's Encrypt. Ne laisse jamais une interface d'admin accessible en HTTP clair sur internet.
- Avec **[Immich](/immich-docker/)** : Paperless gère les documents, Immich les photos. Gardes les deux séparés : les PDF dans Paperless, les souvenirs dans Immich.

## Sauvegardes : ne perds pas trois ans de paperasse

Une stack Docker, c'est cool. Mais si ton disque meurt, c'est la catastrophe. Voici ma stratégie de backup en trois couches :

1. **Volumes Docker** : le dossier `~/docker/paperless` contient `data`, `media`, `pgdata` et `redisdata`. Backup ce dossier entier avec `rsync`, `restic` ou `kopia` vers un NAS ou un stockage cloud chiffré.

2. **Export natif Paperless** : utilise la commande d'export pour générer une archive propre :
```bash
docker compose exec -T webserver python manage.py document_exporter /usr/src/paperless/export
```
Le dossier `export` contiendra alors tous tes documents avec leurs métadonnées au format JSON. Tu peux les réimporter dans une autre instance Paperless sans effort.

3. **Base de données** : si tu sauvegardes le dossier `pgdata`, tu as tout. Sinon, un `pg_dump` classique fonctionne aussi.

Et pour l'amour du pingouin, teste ta restauration au moins une fois par an. Un backup non testé, c'est un backup qui n'existe pas.

## Dépannage rapide : quand ça coince

Ton OCR ne fonctionne pas ? Vérifie que `PAPERLESS_OCR_LANGUAGE` correspond bien à la langue de tes documents. Si tu mets `fra` et que tu envoies un scan en allemand, Tesseract va te sortir du charabia. Pour le multilingue, utilise `fra+eng`.

Le consumer ne détecte pas tes fichiers ? Vérifie que le dossier `consume` a les bonnes permissions (`chmod 755 consume`) et que l'utilisateur Docker peut y lire (`USERMAP_UID` doit correspondre à ton UID sur l'hôte).

Les PDF restent verrouillés en modification ? Si tu uploades un PDF avec mot de passe, Paperless ne peut pas l'OCRiser. Déverrouille-le avant import.

Lenteur excessive sur les gros volumes ? Augmente la RAM allouée à Docker et vérifie que Redis est bien up. Sans Redis, Paperless refait le calcul de l'index à chaque requête, c'est la mort.

## Sécurité et bonnes pratiques

Paperless-ngx sert à stocker des documents sensibles. C'est un trésor pour un attaquant. Quelques règles d'hygiène à respecter :

- **Chiffre tes volumes** : active le chiffrement au repos sur l'hôte (LUKS, chiffrement de dossier, ou au minimum un NAS avec chiffrement matériel).
- **HTTPS obligatoire** : si Paperless est exposé sur internet, passe par un reverse proxy avec un certificat Let's Encrypt. Jamais d'HTTP en clair pour des documents personnels.
- **Mots de passe solides** : l'utilisateur admin doit avoir un mot de passe complexe, stocké dans [Vaultwarden](/vaultwarden-docker-gestionnaire-mots-de-passe/). Et active l'authentification à deux facteurs sur tous les comptes utilisateurs.
- **Restreins l'accès réseau** : si tu n'as pas besoin d'accéder à Paperless depuis l'extérieur, laisse-le en local uniquement (via un VPN comme WireGuard ou Tailscale). Moins de surface d'attaque, zéro inquiétude.
- **Mets à jour régulièrement** : les versions 2.20.x apportent des correctifs de sécurité. Un `docker compose pull && docker compose up -d` par mois suffit.
- **Journalise les accès** : garde un œil sur les logs (`docker compose logs webserver`). Si tu vois des tentatives de connexion massives, quelqu'un sonde ton instance. Bloque son IP au niveau du pare-feu.

Le principe est simple : tes factures et relevés bancaires ne méritent pas moins de soin que ton [gestionnaire de mots de passe](/vaultwarden-docker-gestionnaire-mots-de-passe/) ou ton [cloud personnel](/nextcloud-docker-installation-complete-2025/).

## À qui s'adresse Paperless-ngx ?

- **Au particulier** qui veut dématérialiser ses papiers administratifs sans donner ses données à un tiers.
- **Au travailleur indépendant** qui doit archiver ses factures et justificatifs pendant 10 ans.
- **À la famille** qui veut centraliser contrats d'assurance, bulletins de salaire et certificats de scolarité.
- **Au curieux tech** qui veut tester un OCR auto-hébergé avant de recommander ça à son boss.

Ce n'est pas un outil pour les entreprises de 500 salariés (il existe des solutions plus robustes et payantes pour ça). Mais pour tout le reste, c'est un monstre d'efficacité.

Penses-y la prochaine fois que tu ouvriras un tiroir en disant "il est où ce putain de contrat ?". La réponse sera dans Paperless, trouvée en 0,3 seconde.
