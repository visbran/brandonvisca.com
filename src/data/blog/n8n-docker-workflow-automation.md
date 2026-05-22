---
title: "n8n Docker : remplace Zapier par du self-hosted"
description: "Installe n8n en Docker pour automatiser ton homelab. Workflows visuels, 800+ intégrations, zéro coût — alternative open-source à Zapier."
pubDatetime: 2026-05-22 12:00:00+02:00
modDatetime: 2026-05-22 12:00:00+02:00
author: Brandon Visca
tags:
  - docker
  - n8n
  - workflow-automation
  - intermediaire
  - auto-hebergement
  - homelab
featured: false
draft: false
focusKeyword: n8n docker
faqs:
  - question: "n8n est-il vraiment gratuit ?"
    answer: "Le coeur de n8n est gratuit et open-source sous licence Sustainable Use License. Tu peux l'héberger toi-même sans limite de tâches. Certaines fonctionnalités avancées (LDAP, SSO, audit logs) sont payantes via la licence Enterprise."
  - question: "Quelle est la différence entre n8n et Zapier ?"
    answer: "Zapier est SaaS : tes données passent chez eux, tu payes au nombre de tâches. n8n est auto-hébergé : tes workflows restent sur ton serveur, c'est gratuit et sans limite de tâches en mode self-hosted."
  - question: "Combien de RAM faut-il pour faire tourner n8n en Docker ?"
    answer: "Minimum 2 Go de RAM pour n8n seul. Avec PostgreSQL en plus, prévois 3-4 Go. Sur un Raspberry Pi 4 avec 4 Go ça passe, mais c'est serré. Un mini-PC ou un NAS x86 avec 8 Go est idéal."
  - question: "Puis-je utiliser n8n sans Docker ?"
    answer: "Oui, via npm global (`npm install n8n -g`) ou en téléchargeant le binaire. Mais Docker reste le plus propre pour un homelab : isolation, backup des volumes, rollback facile."
---
> 💡 **TL;DR** — Ce qu'il faut retenir :
> - n8n est un outil d'automatisation visuel auto-hébergé, alternative à Zapier et Make.
> - 800+ intégrations natives, licence Sustainable Use License (fair-code).
> - Stack Docker simple : PostgreSQL + n8n + volumes persistants.
> - 3 workflows homelab prêts à l'emploi : monitoring, DNS, archivage.
> - Sécurise avec HTTPS + auth basique, ne laisse pas ton instance en HTTP ouvert.

## Pourquoi payer quand tu peux self-hoster ?

Zapier facture 150 €/mois pour 10 000 tâches. Make grimpe à 200 €/mois pour du volume un peu sérieux. Et à chaque exécution, **tes données partent chez eux**.

n8n ? C'est **0 €**. Tu l'installes sur ton NAS, ton mini-PC ou ton VPS. Tes workflows restent chez toi. Pas de plafond de tâches. Pas de vendor lock-in. Si ton serveur est allumé, tes automatisations tournent.

L'outil est passé en licence **Sustainable Use License** (fair-code) : le code est lisible, modifiable, et gratuit pour la plupart des usages. Seules les fonctionnalités Enterprise (SSO, audit logs) sont payantes. Pour un homelab, tu n'en as pas besoin.

## C'est quoi n8n exactement ?

n8n est un éditeur de workflows visuels. Tu drag & drop des **nodes** (déclencheurs et actions), tu les relies, et ça tourne.

- **800+ intégrations** natives : Telegram, Discord, Nextcloud, GitHub, RSS, HTTP, SSH, Docker, Google Sheets, Notion…
- **Webhooks** entrants et sortants pour connecter n'importe quel service.
- **Expressions** en JavaScript pour transformer les données entre chaque node.
- **Execution log** complet : chaque run est tracé, debuggable.

L'interface ressemble à un Zapier en plus technique — et c'est exactement ce qu'on veut.

## Prérequis : ce qu'il te faut avant de commencer

Tu dois déjà avoir ça en place :

- **Docker et Docker Compose** installés. Si ce n'est pas le cas, voir [/docker-debutant-services-auto-heberger/](/docker-debutant-services-auto-heberger/).
- **2 Go de RAM minimum** pour n8n seul, 4 Go recommandés avec PostgreSQL.
- **Un reverse proxy** (Traefik, Nginx Proxy Manager, Caddy) pour exposer n8n en HTTPS. Pas question de laisser ça en HTTP sur le port 5678 ouvert. Si tu utilises Traefik, on a déjà un guide : [/traefik-reverse-proxy-docker/](/traefik-reverse-proxy-docker/).
- **Un nom de domaine** (ou sous-domaine) pointé vers ton serveur.
- **~5 Go d'espace disque** pour les volumes Docker.

## Docker Compose : le stack complet

On va monter **PostgreSQL** pour la persistence + **n8n** pour l'app. SQLite est possible, mais PostgreSQL évite la corruption en cas de crash.

Crée un dossier `n8n` et ce `docker-compose.yml` :

```yaml
services:
  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: n8n
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U n8n -d n8n"]
      interval: 5s
      timeout: 5s
      retries: 5

  n8n:
    image: n8nio/n8n:latest
    restart: unless-stopped
    environment:
      DB_TYPE: postgresdb
      DB_POSTGRESDB_HOST: postgres
      DB_POSTGRESDB_PORT: 5432
      DB_POSTGRESDB_DATABASE: n8n
      DB_POSTGRESDB_USER: n8n
      DB_POSTGRESDB_PASSWORD: ${POSTGRES_PASSWORD}
      N8N_BASIC_AUTH_ACTIVE: "true"
      N8N_BASIC_AUTH_USER: ${N8N_USER}
      N8N_BASIC_AUTH_PASSWORD: ${N8N_PASSWORD}
      WEBHOOK_URL: ${WEBHOOK_URL}
      GENERIC_TIMEZONE: Europe/Paris
    ports:
      - "127.0.0.1:5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  postgres_data:
  n8n_data:
```

Et le fichier `.env` à côté :

```bash
POSTGRES_PASSWORD=ton_mot_de_passe_fort_ici
N8N_USER=admin
N8N_PASSWORD=un_autre_mot_de_passe_fort
WEBHOOK_URL=https://n8n.tondomaine.com
```

**Explications des variables critiques :**

- `WEBHOOK_URL` : l'URL publique de ton instance. Sans ça, les webhooks entrants génèrent des URL en `localhost` et ne fonctionnent pas.
- `N8N_BASIC_AUTH_ACTIVE` : active l'authentification basique sur l'interface web. Ce n'est pas du SSO, mais ça bloque les scanners de bots.
- `GENERIC_TIMEZONE` : obligatoire pour que les triggers planifiés (type cron) soient à l'heure de Paris.
- `127.0.0.1:5678` : n8n n'écoute que sur localhost. C'est **ton reverse proxy** qui fait le lien HTTPS vers le monde extérieur.

Lance le stack :

```bash
docker compose up -d
```

Attends ~30 secondes que PostgreSQL passe le healthcheck, puis accède à `https://n8n.tondomaine.com`. Authentifie-toi avec les credentials du `.env`.

## 3 workflows pratiques pour ton homelab

Voici trois automatisations concrètes que tu peux monter en 10 minutes chacune.

### A. Uptime Kuma down → notification Telegram

Tu utilises déjà [Uptime Kuma](/uptime-kuma-2-0-monitoring-auto-heberge/) pour surveiller tes services. Relions-le à Telegram pour être alerté en temps réel.

**Dans n8n :**

1. Crée un workflow, ajoute un node **Webhook** (type `Catch`).
2. Copie l'URL du webhook générée (`https://n8n.tondomaine.com/webhook/...`).
3. Dans Uptime Kuma, va dans les paramètres de monitoring → **Notifications** → ajoute un type **Webhook**.
4. Colle l'URL n8n, méthode `POST`.

Retour dans n8n, ajoute un node **Telegram** (action `Send Message`) :
- Connecte ton bot Telegram (crée-le via [@BotFather](https://t.me/BotFather) si besoin).
- Chat ID : ton ID personnel ou celui d'un groupe.
- Message : `🔴 {{ $json.msg }} est DOWN — {{ $json.time }}`

Active le workflow. Dès qu'un service tombe, tu reçois le message sur Telegram.

### B. Détection changement Pi-hole → push ntfy

Tu veux être notifié quand une nouvelle liste de blocage est chargée sur Pi-hole (ou AdGuard).

**Dans n8n :**

1. Node **Schedule Trigger** → toutes les 6 heures.
2. Node **HTTP Request** → `GET http://pi-hole-ip/admin/api.php?summaryRaw` (adapte selon ton setup Pi-hole).
3. Node **Compare Datasets** ou **If** → compare la valeur `gravity_last_updated` avec un valeur stockée dans une **Static Data** ou un fichier.
4. Si différent → node **HTTP Request** vers ton serveur **ntfy** (ou directement le node ntfy s'il existe dans ta version) :
   - URL : `https://ntfy.tondomaine.com/homelab`
   - Body : `🛡️ Pi-hole : nouvelle liste de blocage chargée`

C'est basique, mais ça te dispense de vérifier l'interface Pi-hole tous les jours.

### C. Fichier Nextcloud uploadé → traitement Paperless-ngx

Tu stockes tes documents dans [Nextcloud](/nextcloud-docker-installation-complete-2025/) et tu veux les archiver automatiquement dans Paperless-ngx pour l'OCR.

**Dans n8n :**

1. Node **Nextcloud Trigger** → écoute le dossier `/Documents/à-traiter/`.
2. Node **Nextcloud** (Download File) → récupère le fichier uploadé.
3. Node **HTTP Request** → `POST https://paperless.tondomaine.com/api/documents/post_document/` avec :
   - Header `Authorization: Token <ton_api_token_paperless>`
   - Body type : `Form-Data`
   - Fichier binaire issu du node précédent
4. Node **Nextcloud** (Delete File) → supprime le fichier du dossier temporaire.

Résultat : tu poses un PDF dans Nextcloud, il disparaît et réapparaît 30 secondes plus tard dans Paperless avec l'OCR fait.

## Sécurise ton instance

n8n a accès à tes services internes. Ne l'expose pas n'importe comment.

**HTTPS obligatoire**
Via Traefik, Nginx Proxy Manager, ou Caddy. Pas de HTTP en clair, même en local.

**Authentification basique**
Les variables `N8N_BASIC_AUTH_USER` et `N8N_BASIC_AUTH_PASSWORD` du `.env` activent un login sur l'interface. Ce n'est pas du SSO, mais ça évite que le premier script Python qui scanne le port 5678 tombe sur ton dashboard.

**IP whitelist sur l'admin**
Si tu as une IP fixe, ajoute un middleware Traefik pour n'autoriser l'accès à `/` que depuis ton réseau, et laisser `/webhook/` ouvert pour les services externes.

**Backup des volumes**

```bash
docker run --rm -v n8n_data:/data -v $(pwd):/backup alpine tar czf /backup/n8n-backup-$(date +%F).tar.gz -C /data .
```

Stocke ce fichier sur un NAS ou un bucket S3. La base PostgreSQL se backup en même temps avec `pg_dump`.

**Rate limiting**
Via Traefik middleware `RateLimit` ou Nginx Proxy Manager. Évite les abus sur les webhooks publics.

## Zapier vs n8n vs Make : le tableau qui fâche

| Critère | Zapier | Make | n8n self-hosted |
|---|---|---|---|
| **Coût mensuel** | 150 €+ | 200 €+ | **0 €** |
| **Tâches / mois** | 10 000 (plan Pro) | 40 000 (plan Team) | **Illimité** |
| **Intégrations** | 7 000+ | 1 800+ | **800+** |
| **Code custom** | Limité (Python) | Limité | **JS complet** |
| **Où tournent les données** | Cloud US/EU | Cloud EU | **Ton serveur** |
| **Open-source** | ❌ Non | ❌ Non | ✅ Fair-code |
| **Complexité** | Facile | Moyenne | Technique |
| **Idéal pour** | PME sans IT | Agences marketing | **Homelab, tech, privacy** |

Zapier reste le plus simple si tu veux cliquer et oublier. Make est plus puissant sur les transformations visuelles. Mais si tu veux **contrôler tes données** et ne pas payer 150 €/mois pour synchroniser deux feuilles Google, n8n écrase la concurrence.

## Pro tips pour aller plus loin

**Execution order**
Par défaut, n8n exécute les nodes un par un. Si tu as un workflow avec 50 images à traiter, ça prend 50× le temps. Active **Execute Once** sur les nodes déclencheurs et utilise le mode **Run once for each item** pour paralléliser.

**Variables d'environnement**
Stocke les tokens API, clés SSH et mots de passe dans le fichier `.env`, jamais en dur dans les workflows. n8n expose ces variables via `$env.VAR_NAME` dans les expressions.

**Webhooks locaux**
Si deux services tournent sur le même réseau Docker, utilise leurs noms de service comme URL au lieu de passer par l'extérieur. Exemple : `http://netdata:19999` au lieu de `https://netdata.tondomaine.com`. Ça évite la latence et les problèmes de certificat.

**SQLite en dev, PostgreSQL en prod**
Pour tester un workflow rapidement, tu peux lancer n8n sans base de données (`DB_TYPE` non défini, il utilisera SQLite). Mais pour la prod, PostgreSQL est obligatoire.

**Mises à jour**

```bash
docker compose pull && docker compose up -d
```

n8n sort une version par semaine environ. Le tag `latest` suit la branche stable. Relis les [release notes](https://github.com/n8n-io/n8n/releases) avant de mettre à jour — les breaking changes sont signalés.

**Monitoring de n8n lui-même**
Ajoute un healthcheck Docker dans le `docker-compose.yml` :

```yaml
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://127.0.0.1:5678/healthz"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Et surveille-le avec [Uptime Kuma](/uptime-kuma-2-0-monitoring-auto-heberge/) ou [Netdata](/netdata-docker/). Un workflow qui ne se déclenche plus parce que n8n est down, c'est pire que pas de workflow du tout.

**Docker en rootless**
n8n tourne en interne avec l'user `node` (UID 1000). Assure-toi que les volumes ont les bonnes permissions, ou monte-le avec `user: "1000:1000"` dans le compose.

---

Tu as maintenant un n8n fonctionnel, sécurisé, et trois workflows pour automatiser ton homelab sans sortir la carte bleue. Le temps que tu passes à monter ces workflows, tu le récupères en moins de deux mois comparé à un abonnement Zapier. Et surtout, **tes données ne quittent jamais ton serveur**.
