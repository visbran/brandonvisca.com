---
title: "Outline Docker : wiki auto-hébergé"
description: "Déploie Outline Docker : wiki auto-hébergé moderne. Guide complet avec Docker Compose, comparatif Notion et alternatives wiki."
pubDatetime: "2026-06-15T08:00:00.000Z"
modDatetime: "2026-06-15T08:00:00.000Z"
author: Brandon Visca
tags:
  - docker
  - intermediaire
  - auto-hebergement
  - wiki
  - outline
featured: false
draft: false
focusKeyword: outline docker
ogImage: ""
faqs:
  - question: "Outline est-il vraiment open-source ?"
    answer: "Oui, Outline est open-source sous licence BSL (Business Source License). Tu peux l'auto-héberger gratuitement pour un usage interne. Seul le déploiement en SaaS multi-tenant est soumis à licence commerciale."
  - question: "Quelle est la différence entre Outline et Notion ?"
    answer: "Outline ressemble visuellement à Notion mais tourne sur ton serveur. Les données restent chez toi, il n'y a pas d'abonnement mensuel et tu contrôles entièrement l'infrastructure."
  - question: "Outline consomme-t-il beaucoup de ressources ?"
    answer: "Compte 2 Go de RAM minimum pour Outline + PostgreSQL + Redis + MinIO. Un VPS à 4 Go de RAM est confortable pour une petite équipe. C'est plus gourmand que BookStack mais plus léger que Confluence."
  - question: "Puis-je utiliser Outline sans domaine personnalisé ?"
    answer: "Techniquement oui avec une IP locale, mais tu perdras les intégrations OAuth et les prévisualisations de liens. Un sous-domaine avec HTTPS est fortement recommandé."
---
> 💡 **TL;DR**
> - Outline est un wiki auto-hébergé moderne, open-source et visuellement proche de Notion
> - Tu le déploies avec Docker Compose (PostgreSQL + Redis + MinIO + Outline)
> - Interface Markdown avec éditeur WYSIWYG, collections, partages et SSO natif
> - Parfait pour les équipes techniques qui veulent un Notion-like sans cloud
> - Docker Compose complet et comparatif des alternatives ci-dessous

## Table des matières

## Pourquoi un wiki auto-hébergé qui ressemble à Notion ?

Tu utilises Notion pour documenter tes procédures, ton architecture infra et tes runbooks. C'est beau, c'est fluide, et ton équipe adore. Mais derrière cette interface soignée, il y a un petit détail qui gratte : tes données vivent sur des serveurs américains, tu payes un abonnement qui grimpe avec les utilisateurs, et quand Notion fait une mise à jour qui casse ton workflow, tu n'as aucune alternative que d'attendre le hotfix.

Le problème du cloud SaaS pour la documentation interne, c'est que ton savoir métier devient un actif externe. Quand Notion fait faillite, change de politique ou bloque ton compte par erreur (ça arrive), toute ta base de connaissances part avec.

Outline est la réponse technique à ce problème. C'est un wiki moderne développé par la team Outline (anciennement de la team @getoutline sur GitHub), construit avec React et Node.js, qui offre une expérience utilisateur très proche de Notion : éditeur bloc, Markdown caché, collections organisées, partages granulaires. Sauf que tu le contrôles entièrement. Tu l'installes sur ton serveur, tes données restent chez toi, et personne ne te facture à la tête d'utilisateur.

Si tu débutes avec Docker et l'auto-hébergement, commence par mon [guide des services essentiels](/docker-debutant-services-auto-heberger/) pour bien poser les bases. Pour un wiki plus classique orienté équipe, j'ai aussi couvert [BookStack](/bookstack-docker-wiki-equipe/) qui est moins gourmand et plus simple à déployer.

## Qu'est-ce qu'Outline exactement ?

Outline est un wiki et une base de connaissances conçue pour les équipes techniques. Contrairement à MediaWiki ou DokuWiki qui datent des années 2000, Outline adopte une interface moderne type Notion avec une organisation par collections et documents.

Voici ce qu'il propose concrètement :

- **Éditeur bloc Markdown** : tu écris en Markdown mais avec une interface visuelle. Les blocs sont manipulables, les images glissables, les tableaux éditables en direct.
- **Organisation par collections** : tu crées des collections ("Infrastructure", "Procédures", "Onboarding") et tu ranges tes documents dedans avec un système de navigation à gauche.
- **Permissions granulaires** : par collection, par document, par utilisateur. Tu peux rendre public un document tout en gardant le reste privé.
- **SSO natif** : Google Workspace, Slack, Azure AD, OIDC, SAML2. Pas besoin de plugin tiers.
- **Recherche full-text** : rapide, avec surlignage des résultats. L'indexation se fait via PostgreSQL.
- **Historique des révisions** : chaque modification est tracée, comparable et annulable.
- **Templates de documents** : pour standardiser les runbooks, les post-mortem et les specs techniques.
- **Export Markdown/HTML** : pour archiver ou migrer vers un autre système.
- **API REST** : pour automatiser la création de documents depuis tes pipelines CI/CD.
- **Intégrations** : webhooks, Slack, Zapier-like via l'API.

La licence est BSL (Business Source License) : l'auto-hébergement est gratuit et open-source. Seul le déploiement commercial en SaaS multi-tenant est soumis à licence payante. Pour ton homelab ou ton équipe, c'est 100% gratuit.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose (Docker Engine 24+ recommandé)
- **2 Go de RAM minimum** (4 Go recommandés pour être confortable)
- 10 Go d'espace disque pour le système et les uploads
- Un nom de domaine ou sous-domaine pointant vers ton serveur
- Un reverse proxy ([Caddy](/caddy-docker-reverse-proxy-guide/), Traefik ou Nginx Proxy Manager) pour gérer les certificats SSL

Outline est plus gourmand que BookStack parce qu'il embarque un backend Node.js, PostgreSQL, Redis et un stockage d'objets (MinIO ou S3). Un Raspberry Pi 4 ne suffira pas. Prévois un VPS de 2 coeurs / 4 Go ou un petit serveur dédié.

## Déploiement Outline Docker avec Docker Compose

Crée un dossier dédié et un fichier docker-compose.yml :

```bash
mkdir -p ~/outline && cd ~/outline
```

Voici le Docker Compose complet, prêt à l'emploi :

```yaml
version: "3.8"

services:
  outline:
    image: outlinewiki/outline:latest
    container_name: outline
    env_file: .env
    ports:
      - "3000:3000"
    volumes:
      - ./data:/var/lib/outline/data
    depends_on:
      - postgres
      - redis
      - minio
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    container_name: outline_postgres
    env_file: .env
    volumes:
      - ./postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: outline_redis
    volumes:
      - ./redis_data:/data
    restart: unless-stopped

  minio:
    image: minio/minio:latest
    container_name: outline_minio
    env_file: .env
    command: server /data --console-address ":9001"
    volumes:
      - ./minio_data:/data
    ports:
      - "9000:9000"
      - "9001:9001"
    restart: unless-stopped
```

Crée ensuite le fichier .env à côté du docker-compose.yml :

```bash
# --- Base de données ---
POSTGRES_USER=outline
POSTGRES_PASSWORD=change-me-postgres-password
POSTGRES_DB=outline

# --- Redis ---
REDIS_URL=redis://redis:6379

# --- Outline ---
DATABASE_URL=postgres://outline:change-me-postgres-password@postgres:5432/outline
DATABASE_URL_TEST=postgres://outline:change-me-postgres-password@postgres:5432/outline-test
SECRET_KEY=change-me-secret-key-32-chars-min
UTILS_SECRET=change-me-utils-secret-32-chars-min
URL=https://wiki.tondomaine.com
PORT=3000

# Stockage fichier (MinIO)
AWS_ACCESS_KEY_ID=outline
AWS_SECRET_ACCESS_KEY=change-me-minio-password
AWS_REGION=eu-west-1
AWS_S3_UPLOAD_BUCKET_URL=http://minio:9000
AWS_S3_UPLOAD_BUCKET_NAME=outline-uploads
AWS_S3_UPLOAD_MAX_SIZE=26214400
AWS_S3_FORCE_PATH_STYLE=true
AWS_S3_ACL=private

# SMTP (optionnel mais recommandé)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=ton-email@gmail.com
SMTP_PASSWORD=ton-app-password
SMTP_FROM_EMAIL=noreply@tondomaine.com
SMTP_REPLY_EMAIL=noreply@tondomaine.com
SMTP_TLS=true

# Authentification (OIDC / Google / Slack)
# Si tu utilises Google OAuth :
GOOGLE_CLIENT_ID=ton-google-client-id
GOOGLE_CLIENT_SECRET=ton-google-client-secret
```

**Génère deux clés secrètes longues** avant de lancer :

```bash
openssl rand -hex 32
# Exécute deux fois et colle les valeurs dans SECRET_KEY et UTILS_SECRET
```

**Crée le bucket MinIO** avant le premier lancement :

```bash
docker compose up -d minio
sleep 5
docker exec outline_minio mc alias set local http://localhost:9000 outline change-me-minio-password
docker exec outline_minio mc mb local/outline-uploads
docker exec outline_minio mc anonymous set none local/outline-uploads
```

Lance ensuite tout le stack :

```bash
docker compose up -d
```

Attends 30 secondes que PostgreSQL initialise la base, puis accède à https://wiki.tondomaine.com. Si tu n'as pas encore configuré le reverse proxy, utilise http://IP-du-serveur:3000 temporairement.

### Premier utilisateur

Outline ne crée pas d'utilisateur admin par défaut. Tu dois passer par la ligne de commande pour créer le premier compte :

```bash
docker exec -it outline yarn sequelize db:migrate
docker exec -it outline yarn sequelize db:seed:all
```

Si la seed ne crée pas d'utilisateur, tu peux forcer la création via l'API interne ou utiliser une authentification OIDC/Google pour te connecter la première fois.

### Avec un reverse proxy Caddy

Si tu utilises [Caddy avec Docker](/caddy-docker-reverse-proxy-guide/), ajoute ce bloc dans ton Caddyfile :

```caddy
wiki.tondomaine.com {
    reverse_proxy outline:3000
}
```

Caddy gère automatiquement les certificats Let's Encrypt. Pas de Certbot, pas de renouvellement manuel.

### Avec Nginx Proxy Manager

Dans l'interface web de [Nginx Proxy Manager](/nginx-proxy-manager-docker-guide/) :
1. Ajoute un proxy host : wiki.tondomaine.com
2. Forward hostname : outline
3. Forward port : 3000
4. Active "Block Common Exploits" et "Request a new SSL Certificate"
5. Force SSL et HSTS

## Configuration initiale et premiers pas

Une fois connecté, configure ces éléments avant d'inviter ton équipe.

**1. Créer une collection**
Dans la barre latérale gauche, clique sur "New collection". Donne-lui un nom (ex: "Infrastructure") et une couleur. Définis les permissions : private, view-only, ou editable pour l'équipe.

**2. Créer le premier document**
Clique sur "New document" dans la collection. L'éditeur s'ouvre. Tu peux écrire directement en Markdown ou utiliser les commandes / pour insérer des blocs (tableau, code, image, embed).

**3. Configurer l'authentification SSO**
Dans Paramètres > Authentication, active Google OAuth, Slack ou un provider OIDC générique. C'est le moyen le plus propre de gérer les accès. Si tu n'as pas d'annuaire, Outline gère aussi les invitations par email.

**4. Définir les templates**
Dans Paramètres > Templates, crée des modèles pour tes documents récurrents :
- Template "Runbook incident" : contexte, étapes, rollback, post-mortem
- Template "Spec technique" : objectif, contraintes, solution, tests
- Template "Onboarding" : accès, outils, contacts, premières tâches

**5. Configurer les notifications**
Active les notifications Slack ou email pour les commentaires et les modifications importantes. Cela évite que les mises à jour passent inaperçues.

## Outline vs les alternatives : tableau comparatif

| Critère | Outline | Notion | BookStack | Wiki.js | Confluence |
|---------|---------|--------|-----------|---------|------------|
| **Licence** | BSL (open-source) | Propriétaire | MIT | AGPL-3.0 | Propriétaire |
| **Auto-hébergé** | Oui | Non | Oui | Oui | Server payant |
| **Coût** | Gratuit | 8-15€/user/mois | Gratuit | Gratuit | 5-27€/user/mois |
| **Interface** | Bloc Markdown, moderne | Bloc, très design | WYSIWYG classique | Markdown + WYSIWYG | Lourd, daté |
| **SSO** | Google, Slack, OIDC, SAML | Google, SAML (payant) | LDAP, SAML2, OIDC | LDAP, OAuth, SAML | Atlassian natif |
| **Recherche** | Full-text PostgreSQL | Excellente (IA) | Full-text MariaDB | Elasticsearch | Power Search |
| **Ressources RAM** | ~2 Go (stack complet) | N/A (cloud) | ~256 Mo | ~512 Mo | 2 Go+ |
| **Export** | Markdown, HTML | PDF, Markdown (payant) | PDF, ePub, HTML | Markdown, PDF | PDF, Word |
| **API** | REST complète | REST limitée | REST | GraphQL + REST | REST (cloud limité) |
| **App mobile** | Responsive web | Native iOS/Android | Responsive web | Responsive web | Application native |
| **Facilité** | Bonne | Excellente | Très intuitive | Technique | Courbe d'apprentissage |

Mon verdict pour un homelab ou une équipe technique :

- **Outline** : le meilleur compromis entre modernité et souveraineté. Si tu veux un Notion-like sans cloud, c'est le choix par défaut. Le déploiement est plus lourd que BookStack mais l'expérience utilisateur le vaut.
- **Notion** : si tu n'as pas le temps de gérer un serveur et que le budget n'est pas un problème. Mais tu restes dépendant d'un service externe.
- **BookStack** : pour des équipes moins techniques ou un usage purement procédural. Plus léger, plus rapide à déployer, mais moins moderne visuellement.
- **Wiki.js** : excellent pour les équipes de dev qui aiment le Markdown brut et veulent du multilingue avancé. Moins intuitif pour les profils non-techniques.
- **Confluence** : si tu es déjà dans l'écosystème Atlassian et que tu as le budget. Sinon, c'est overpriced et lent.

## Sécuriser l'accès et les données

Un wiki contient souvent des informations sensibles. Voici les mesures de base à appliquer.

**HTTPS partout**
Ne laisse jamais Outline en HTTP. Ton reverse proxy doit forcer le HTTPS, activer HSTS et bloquer les versions obsolètes de TLS. Caddy le fait nativement.

**Sauvegardes automatisées**
Le volume ./postgres_data contient la base de données. Le volume ./data contient les uploads et la configuration. Sauvegarde-les avec Duplicati ou un script cron rsync.

```bash
#!/bin/bash
# backup-outline.sh
DATE=$(date +%Y%m%d_%H%M%S)
tar czf "/backup/outline_app_$DATE.tar.gz" ~/outline/data ~/outline/minio_data
docker exec outline_postgres pg_dump -U outline outline > "/backup/outline_db_$DATE.sql"
```

**Mises à jour**
Outline publie des mises à jour régulières sur Docker Hub. Mets à jour une fois par semaine :

```bash
cd ~/outline
docker compose pull
docker compose up -d
```

**Fail2ban**
Si tu exposes Outline sur Internet, protège-toi contre les attaques par force brute sur la page de connexion. [Fail2ban avec Docker](/fail2ban-docker-securite-serveur/) peut surveiller les logs du reverse proxy et bannir les IP abusives.

**Authentification double facteur**
Si tu utilises un provider OIDC compatible TOTP (comme Authelia), active le 2FA pour tous les comptes admin. Outline se fie au provider d'identité pour cela.

## Intégrations et astuces avancées

**Brancher un S3 externe**
Si tu veux externaliser le stockage des fichiers, remplace MinIO par un bucket AWS S3, Scaleway ou Wasabi. Modifie simplement les variables AWS_S3_* dans le .env et supprime le service MinIO du docker-compose.yml.

**Notifications Slack**
Via l'API REST d'Outline et un webhook Slack, tu peux notifier ton channel technique à chaque création ou modification de document critique. C'est un simple script Python lancé en tâche cron ou via [n8n](/n8n-docker-workflow-automation/).

**Personnalisation CSS**
Outline permet d'injecter du CSS personnalisé via les paramètres d'administration. Tu peux harmoniser les couleurs avec ta charte graphique ou ajuster la typographie.

**Import depuis Notion**
Si tu migres depuis Notion, exporte tes pages au format Markdown (Notion le supporte nativement). Outline importe le Markdown brut. Tu devras recréer manuellement la structure des collections.

**Lien avec ta gestion documentaire**
Pour les documents scannés et la gestion documentaire lourde, [Paperless-ngx](/paperless-ngx-docker-guide-auto-hebergement/) complète Outline sur les documents administratifs. Mon workflow : Paperless stocke et OCRise les factures, Outline documente les procédures techniques.

## FAQ

**Puis-je utiliser Outline sans MinIO ?**
Oui, mais tu perdras la gestion des pièces jointes et des images. Tu peux aussi utiliser un bucket S3 externe à la place de MinIO.

**Outline gère-t-il plusieurs langues ?**
L'interface est traduite en plusieurs langues dont le français. La documentation que tu écris reste dans la langue de ton choix.

**Est-ce que je peux héberger Outline derrière un sous-chemin ?**
Non, Outline nécessite un domaine racine (ex: wiki.tondomaine.com) et ne supporte pas les sous-chemins (tondomaine.com/wiki). Prévois un sous-domaine dédié.
