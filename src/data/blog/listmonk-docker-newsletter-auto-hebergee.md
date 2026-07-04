---
title: "Listmonk Docker : newsletters auto-hébergées (alternative Mailchimp)"
description: "Déploie Listmonk sous Docker : guide listmonk docker complet pour créer une newsletter auto-hébergée et se passer de Mailchimp."
pubDatetime: "2026-07-03T08:00:00.000Z"
modDatetime: "2026-07-04T14:00:00.000Z"
author: Brandon
tags:
  - auto-hebergement
  - docker
  - intermediaire
  - newsletter
  - listmonk
featured: false
draft: false
focusKeyword: listmonk docker
faqs:
  - question: "Quelle est la différence entre Listmonk et Mailchimp ?"
    answer: "Listmonk est open-source et auto-hébergé : aucune limite d'abonnés, tes données restent chez toi, et tu ne paies que ton VPS. Mailchimp est un SaaS propriétaire avec des tarifs qui grimpent rapidement selon le nombre de contacts."
  - question: "Faut-il un serveur SMTP dédié pour utiliser Listmonk ?"
    answer: "Non. Listmonk gère les listes et les campagnes, mais il a besoin d'un relais SMTP pour envoyer les emails. Tu peux utiliser un service externe (Mailgun, Brevo, AWS SES) ou ton propre serveur mail si tu l'as auto-hébergé."
  - question: "Listmonk peut-il gérer des milliers d'abonnés ?"
    answer: "Oui. Listmonk est codé en Go et conçu pour la performance. Des instances en production gèrent des centaines de milliers de contacts sans problème, pourvu que PostgreSQL dispose de suffisamment de ressources."
---
> 💡 **TL;DR**
> - **Listmonk** est un outil de newsletter open-source en Go et Vue.js : gratuit, rapide, sans limite d'abonnés
> - Tu le déploies en 10 minutes avec **Docker Compose** (Listmonk + PostgreSQL), prêt à recevoir tes contacts
> - Interface complète : listes, campagnes, templates HTML/Markdown, double opt-in, API REST, webhooks
> - Pour l'envoi SMTP, tu branches ton relais (Mailgun, SendGrid, ou ton propre serveur mail) et tu gardes le contrôle total de tes données

## Table des matières

## Pourquoi se passer de Mailchimp en 2026 ?

Mailchimp, c'est pratique. Tu crées un compte, tu upload tes contacts, tu envoies des emails. Le problème ? Le prix grimpe vite. Dès que tu dépasses 500 abonnés, tu passes à un plan payant. À 5 000 abonnés, tu paies déjà plusieurs dizaines d'euros par mois. Et si tu as 50 000 contacts, la facture devient indécente.

Mais ce n'est pas qu'une question de coût. Quand tu utilises un service externe, **tes données ne sont pas chez toi**. Tes listes d'abonnés, leurs comportements d'ouverture, leurs clics, tout transite par les serveurs d'une boîte américaine. Le RGPD t'oblige à informer tes abonnés de cette sous-traitance, à signer un DPA (Data Processing Agreement) et à t'assurer que les données ne quittent pas l'Europe sans garanties.

Avec un outil auto-hébergé comme Listmonk, le problème disparaît. Tes contacts restent sur ton serveur. Tes logs d'envoi restent chez toi. Tu n'as pas de limite artificielle. Et tu peux envoyer autant d'emails que ton serveur SMTP (ou ton relais) peut digérer.

En 2026, l'auto-hébergement n'est plus réservé aux barbus. Un VPS chez Hetzner ou OVH coûte 5 €/mois. Docker tourne partout. Et des outils comme Listmonk prouvent que tu peux remplacer des SaaS propriétaires par des solutions open-source sans compromis.

Si tu débutes avec Docker, mon [guide des services essentiels à auto-héberger](/docker-debutant-services-auto-heberger/) te donne les bases avant d'attaquer celui-ci.

## Qu'est-ce que Listmonk ?

Listmonk est une plateforme de newsletter et de mailing list développée en Go (backend) et Vue.js (frontend). Le projet est open-source sous licence AGPL-3.0, avec un dépôt actif sur GitHub (`knadh/listmonk`). L'application est conçue pour être légère, rapide et sans dépendances lourdes.

Le moteur tourne dans un binaire unique. La base de données est PostgreSQL. L'interface web est embarquée. Pas besoin d'Apache, de Nginx complexe, ou de cache Redis externe pour démarrer.

**Ce que Listmonk fait nativement :**
- Gestion de **listes** et de **campagnes** illimitées
- **Double opt-in** avec confirmation par email
- Templates en **Markdown** ou **HTML** pur
- Statistiques d'ouverture et de clic (pixel de tracking)
- **API REST** complète pour automatiser tout
- **Webhooks** pour brancher des services externes
- Import/export CSV de contacts
- Gestion des **bounces** et des **unsubscribe** automatiques
- Multi-utilisateurs avec rôles

Ce que Listmonk ne fait pas : il n'envoie pas les emails tout seul. Il génère le contenu, gère les listes, et transmet à un serveur SMTP. C'est à toi de fournir le relais. C'est une séparation de responsabilités saine.

## Prérequis

Avant de commencer, il te faut :
- Un serveur avec **Docker** et **Docker Compose** installés (si ce n'est pas le cas, voir mon [guide Docker pour débutants](/docker-debutant-services-auto-heberger/))
- Un **nom de domaine** pointant vers ton serveur (facultatif mais recommandé pour HTTPS)
- Un **reverse proxy** (Traefik, Nginx Proxy Manager, Caddy) configuré pour exposer tes services en HTTPS
- Un **compte SMTP** ou un serveur mail configuré pour l'envoi réel des emails

Listmonk consomme peu de ressources. Sur un VPS avec 1 vCPU et 2 Go de RAM, il tourne sans problème à côté d'autres conteneurs. PostgreSQL est le plus gourmand de la stack, mais il reste très raisonnable pour des milliers de contacts.

## Architecture et stack

La stack est minimaliste :
- **listmonk** : l'application web (port 9000 par défaut)
- **postgres** : la base de données relationnelle pour stocker les contacts, campagnes et logs

On ajoute un **volume** persistant pour la base de données et un autre pour les uploads (images, templates). Listmonk expose un port HTTP simple. C'est le reverse proxy qui s'occupe du HTTPS et du nom de domaine.

Pas de Redis, pas de RabbitMQ, pas de cluster Elasticsearch. Juste deux conteneurs qui parlent entre eux.

## Le docker-compose.yml complet

Crée un dossier pour le projet :

```bash
mkdir -p ~/docker/listmonk && cd ~/docker/listmonk
```

Crée le fichier `docker-compose.yml` :

```yaml
version: "3.8"

services:
  db:
    image: postgres:16-alpine
    container_name: listmonk_db
    restart: unless-stopped
    environment:
      POSTGRES_USER: listmonk
      POSTGRES_PASSWORD: change_me_strong_password
      POSTGRES_DB: listmonk
    volumes:
      - listmonk_db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U listmonk -d listmonk"]
      interval: 10s
      timeout: 5s
      retries: 5

  app:
    image: listmonk/listmonk:latest
    container_name: listmonk_app
    restart: unless-stopped
    command: [sh, -c, "./listmonk --install --idempotent --yes && ./listmonk --upgrade --yes && ./listmonk"]
    ports:
      - "127.0.0.1:9000:9000"
    environment:
      TZ: Europe/Paris
    volumes:
      - listmonk_uploads:/listmonk/uploads
      - ./config.toml:/listmonk/config.toml:ro
    depends_on:
      db:
        condition: service_healthy

volumes:
  listmonk_db_data:
  listmonk_uploads:
```

**Note sur le port** : on bind `127.0.0.1:9000` pour que Listmonk ne soit accessible que localement. Le reverse proxy (Traefik, Caddy, etc.) redirige le trafic externe vers ce port. C'est une bonne pratique de sécurité.

**Note sur la commande** : au premier démarrage, `--install --idempotent` crée les tables PostgreSQL si la base est vide, et `--upgrade` applique les migrations après une mise à jour d'image. Sans cette étape, Listmonk refuse de démarrer sur une base vierge.

Le conteneur Listmonk attend un fichier `config.toml`. Crée-le :

```bash
nano config.toml
```

```toml
[app]
address = "0.0.0.0:9000"

# Database
[db]
host = "db"
port = 5432
user = "listmonk"
password = "change_me_strong_password"
database = "listmonk"
ssl_mode = "disable"
max_open = 25
max_idle = 25
max_lifetime = "300s"
```

Pas de section SMTP dans ce fichier : Listmonk stocke cette configuration en base de données et tu la définis via l'interface web, ce qui évite d'écrire des mots de passe en clair dans un fichier versionné.

**Change le mot de passe PostgreSQL** avant de lancer. Ne laisse pas `change_me_strong_password` en production. Un mot de passe de 32 caractères aléatoires est le minimum.

## Déploiement étape par étape

Lance la stack :

```bash
docker compose up -d
```

Attends que PostgreSQL soit prêt (le healthcheck valide ça automatiquement). Puis ouvre ton navigateur sur `http://ton-ip:9000` (ou via ton reverse proxy si déjà configuré).

Au premier démarrage, Listmonk t'invite à **créer le compte administrateur** (email, identifiant, mot de passe). Une fois connecté, tu peux passer l'interface en français dans les réglages.

Crée ton compte admin et tu arrives sur le tableau de bord.

**Première chose à faire** : créer une liste.

Va dans **Lists** > **Create list**. Donne un nom (ex: "Ma liste principale"), une description, et active l'option **Double opt-in** si tu veux que les nouveaux contacts confirment leur inscription. C'est obligatoire si tu respectes le RGPD.

Ensuite, importe tes contacts via **Subscribers** > **Import**. Listmonk accepte le CSV avec les colonnes `email`, `name`, `status`. Le statut `confirmed` signifie que le contact a déjà opt-in. `unconfirmed` envoie un email de confirmation automatique.

## Configurer l'envoi d'emails (SMTP)

Listmonk sans SMTP, c'est comme une voiture sans moteur. Tu as besoin d'un relais pour délivrer tes emails.

Trois options :
1. **Un relais externe** : Mailgun, SendGrid, AWS SES, Brevo (ex-Sendinblue). Payant selon le volume, mais simple à configurer.
2. **Ton propre serveur SMTP** : si tu as déjà un Postfix ou un serveur mail auto-hébergé, tu peux l'utiliser. C'est le top niveau pour le contrôle.
3. **Un SMTP de ton hébergeur** : certains VPS incluent un relais mail. Vérifie les limitations (souvent 200-500 emails/jour).

Dans l'interface Listmonk, va dans **Settings** > **SMTP**. Ajoute un nouveau provider :
- **Host** : smtp.mailgun.org (ou ton serveur)
- **Port** : 587 (STARTTLS) ou 465 (SSL/TLS)
- **Username** : ton identifiant SMTP
- **Password** : ton mot de passe ou clé API
- **Auth protocol** : PLAIN ou LOGIN
- **TLS** : Enable TLS
- **From address** : l'adresse d'expédition (ex: newsletter@tondomaine.com)
- **Max connections** : 10
- **Max message rate** : selon ton relais (ex: 50/min pour un petit serveur)

Teste la connexion avec le bouton **Test**. Listmonk envoie un email à ton adresse admin. Si tu le reçois, c'est gagné.

**Conseil pro** : configure les enregistrements SPF et DKIM pour ton domaine. Sans ça, tes emails finissent dans les spams. Ton fournisseur SMTP te donne les DNS records à ajouter. Si tu envoies depuis ton propre serveur, DMARC est indispensable.

Pour le monitoring de l'envoi, j'ai déjà parlé d'outils comme [Vanderplaanki pour sauvegarder tes emails](/vanderplanki-sauvegarde-emails-gratuit-multiplateforme/) si tu veux archiver les campagnes envoyées côté client.

## Créer ta première campagne

Une fois la liste et le SMTP prêts, crée une campagne.

Va dans **Campaigns** > **Create**. Tu as deux choix de format :

**Markdown** : simple, rapide, compatible texte. Listmonk convertit automatiquement en HTML pour les clients mail. Parfait pour les newsletters textuelles.

**HTML** : tu écris le code toi-même (ou tu colles un template). Utile pour les emails design avec images, boutons, colonnes.

Remplis :
- **Name** : le nom interne de la campagne
- **Subject** : l'objet de l'email
- **Lists** : les listes cibles
- **Content** : ton template

Avant d'envoyer à tout le monde, utilise **Preview** pour voir le rendu. Puis clique sur **Send test** pour t'envoyer un email à toi-même. Vérifie le rendu sur desktop et mobile.

Quand tout est bon, clique sur **Start**. Listmonk envoie les emails progressivement selon le rate limit que tu as configuré dans le SMTP. Tu peux suivre la progression en temps réel : combien envoyés, combien ouverts, combien cliqués.

**Tip** : programme tes campagnes avec l'option **Schedule**. Utile pour envoyer à 9h du matin alors que tu rédiges à 2h du matin.

## Sécuriser l'instance

Un outil de newsletter auto-hébergé contient des données personnelles. Il faut le protéger sérieusement.

**HTTPS obligatoire** : expose Listmonk uniquement via ton reverse proxy en HTTPS. Ne laisse jamais le port 9000 ouvert sur Internet en HTTP clair.

**Authentification** : le compte admin est la clé du royaume. Utilise un mot de passe fort (20+ caractères, gestionnaire de mots de passe). Active la 2FA si ton reverse proxy la supporte (Authelia, Authentik).

**Rate limiting** : limite le nombre d'inscriptions par IP pour éviter le spam de formulaires. Listmonk ne le fait pas nativement, mais ton reverse proxy peut ajouter un rate limit sur les endpoints publics.

**Backups** : sauvegarde ton volume PostgreSQL quotidiennement. Un simple `pg_dump` dans un cron suffit :

```bash
docker exec listmonk_db pg_dump -U listmonk listmonk > /backup/listmonk-$(date +%F).sql
```

Conserve plusieurs jours d'historique. Si tu perds ta base de contacts, c'est irréparable.

**Mises à jour** : Listmonk publie des mises à jour régulières. Pour mettre à jour :

```bash
cd ~/docker/listmonk
docker compose pull
docker compose up -d
```

La base se met à jour automatiquement. Lisez toujours les release notes avant, surtout si tu utilises des API ou des webhooks.

## Comparatif : Listmonk vs Mailchimp vs alternatives

| Critère | Listmonk (self-hosted) | Mailchimp | Brevo (ex-Sendinblue) |
|---|---|---|---|
| **Prix** | Gratuit (coût VPS uniquement) | Payant dès 500 abonnés | Gratuit jusqu'à 300 emails/jour |
| **Limites** | Aucune (limite = ton SMTP) | Limites strictes selon le plan | Limites selon le plan |
| **RGPD** | Total contrôle | Sous-traitance externe | Sous-traitance externe |
| **Code source** | Open-source (AGPL) | Propriétaire | Propriétaire |
| **API** | REST complète | REST complète | REST complète |
| **Templates** | Markdown + HTML | Éditeur visuel drag & drop | Éditeur visuel |
| **Multi-listes** | Oui | Oui | Oui |
| **Auto-hébergement** | Oui | Non | Non |
| **Complexité** | Docker requis | Zéro | Zéro |

Listmonk gagne sur le contrôle et le coût. Il perd sur la simplicité initiale (il faut Docker) et sur l'éditeur visuel avancé. Si tu préfères une solution tout-en-un et que tu n'as pas de contrainte budgétaire, Mailchimp reste une option. Mais si tu lis cet article, c'est que tu cherches à t'affranchir des SaaS.

Dans ma stack d'auto-hébergement, Listmonk s'accompagne d'outils comme [Actual Budget pour la gestion financière](/actual-budget-docker-gestion-budget/) et Vaultwarden pour les mots de passe. Le principe est toujours le même : tes données chez toi, tes règles.

## Conclusion

Envoyer des newsletters ne devrait pas coûter une fortune ni exiger de confier tes contacts à un tiers américain. Listmonk prouve qu'un outil open-source, léger et bien conçu peut remplacer Mailchimp pour la majorité des usages.

Avec Docker, le déploiement prend moins de temps que la création d'un compte sur un SaaS propriétaire. Tu contrôles tes données, tes listes, tes templates, et ton volume d'envoi. La seule chose dont tu as besoin en plus, c'est un relais SMTP. Et ça, tu peux même l'auto-héberger si tu es motivé.

Listmonk n'est pas une alternative de niche. C'est une solution de production utilisée par des milliers de projets. Monte ton instance ce week-end. Ton portefeuille et tes abonnés te remercieront.
