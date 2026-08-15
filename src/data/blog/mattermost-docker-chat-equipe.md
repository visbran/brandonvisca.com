---
title: "Mattermost Docker : chat d'équipe auto-hébergé (alternative Slack)"
description: "Guide complet mattermost docker : déploie Mattermost avec Docker. Messagerie d'équipe auto-hébergée, alternative open-source à Slack gratuite."
pubDatetime: "2026-08-15T08:00:00.000Z"
modDatetime: "2026-08-15T08:00:00.000Z"
author: brandon
tags:
  - auto-hebergement
  - docker
  - messagerie
  - equipe
  - intermediaire
featured: false
draft: false
focusKeyword: mattermost docker
---
> 💡 **TL;DR**
>
> - Mattermost est un chat d'équipe open-source que tu déploies en 10 minutes avec Docker.
> - Stack minimale : conteneur Mattermost + PostgreSQL + reverse proxy HTTPS.
> - Tu gardes le contrôle total de tes données, sans dépendre de Slack ou Teams.

Tu en as marre de payer Slack à 8$ par utilisateur et par mois pour un historique de messages qui finit dans un cloud américain ? Tu veux une messagerie d'équipe où **tu** décides où tes données dorment ? Mattermost est la réponse. C'est un logiciel de chat d'équipe open-source, développé en Go et React, qui tourne parfaitement dans un conteneur Docker. Ce guide te montre comment le monter de zéro, le sécuriser avec HTTPS et le rendre utilisable par ton équipe en moins d'une demi-heure.

## Pourquoi Mattermost plutôt que Slack ou Teams ?

Slack, c'est pratique. Microsoft Teams aussi. Le problème, c'est le prix, la souveraineté des données et la dépendance à un tiers. Quand tu cliques sur "Accepter" chez Slack, tu acceptes que tes conversations, fichiers et métadonnées transitent par leurs serveurs. Avec Mattermost, tout reste sur **ta** machine.

Voici ce que tu obtiens gratuitement avec la Team Edition :

- Canaux publics et privés, messages directs, threads
- Partage de fichiers (stockés localement)
- Recherche full-text dans l'historique
- Applications mobiles iOS et Android
- Intégrations via webhooks, slash commands et bots
- Appels vocaux et vidéo via plugin (ou intégration Jitsi)
- SSO via GitLab, Google, Okta (OAuth 2.0/OpenID Connect)
- Pas de limite d'utilisateurs, pas de tarification par siège

La version Enterprise ajoute l'authentification LDAP/AD, la conformité avancée et le support officiel. Pour un homelab ou une petite équipe, la Team Edition suffit largement.

## Prérequis

Avant de commencer, assure-toi d'avoir :

- Un serveur Linux (Debian, Ubuntu, AlmaLinux...) avec Docker et Docker Compose installés
- Un nom de domaine pointant vers ton serveur (ex: `chat.tondomaine.com`)
- Un reverse proxy pour gérer le HTTPS (ce guide utilise [Caddy](/caddy-docker-reverse-proxy-guide/))
- 2 Go de RAM minimum pour le conteneur Mattermost + PostgreSQL

Si Docker Compose est encore flou pour toi, jette un œil au [guide Docker pour débutants](/docker-debutant-services-auto-heberger/) avant de continuer.

## Architecture de la stack

Notre déploiement repose sur trois briques :

1. **PostgreSQL** : base de données principale de Mattermost. MySQL est supporté, mais PostgreSQL est recommandé par les développeurs pour de meilleures performances.
2. **Mattermost Team Edition** : le serveur de messagerie lui-même.
3. **Caddy** : reverse proxy qui gère le HTTPS automatiquement avec Let's Encrypt.

Chaque service vit dans son propre conteneur. Les données persistent dans des volumes Docker. Rien ne touche le système hôte.

## Le docker-compose.yml

Crée un répertoire dédié et un fichier `docker-compose.yml` :

```bash
mkdir -p ~/mattermost-docker
cd ~/mattermost-docker
```

Voici le fichier complet :

```yaml
version: "3.8"

services:
  postgres:
    image: postgres:16-alpine
    container_name: mattermost-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: mmuser
      POSTGRES_PASSWORD: mmuser-password-change-me
      POSTGRES_DB: mattermost
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U mmuser -d mattermost"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - mattermost-net

  mattermost:
    image: mattermost/mattermost-team-edition:10.1
    container_name: mattermost-app
    restart: unless-stopped
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      MM_SQLSETTINGS_DRIVERNAME: postgres
      MM_SQLSETTINGS_DATASOURCE: postgres://mmuser:mmuser-password-change-me@mattermost-postgres:5432/mattermost?sslmode=disable&connect_timeout=10
      MM_SERVICESETTINGS_SITEURL: https://chat.tondomaine.com
      MM_SERVICESETTINGS_LISTENADDRESS: :8065
      MM_FILESETTINGS_DIRECTORY: /mattermost/data/
      MM_LOGSETTINGS_FILELOCATION: /mattermost/logs/
    volumes:
      - mattermost_data:/mattermost/data
      - mattermost_logs:/mattermost/logs
      - mattermost_config:/mattermost/config
      - mattermost_plugins:/mattermost/plugins
      - mattermost_client_plugins:/mattermost/client/plugins
    networks:
      - mattermost-net
    ports:
      - "127.0.0.1:8065:8065"

  caddy:
    image: caddy:2-alpine
    container_name: mattermost-caddy
    restart: unless-stopped
    depends_on:
      - mattermost
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
      - caddy_config:/config
    networks:
      - mattermost-net

volumes:
  postgres_data:
  mattermost_data:
  mattermost_logs:
  mattermost_config:
  mattermost_plugins:
  mattermost_client_plugins:
  caddy_data:
  caddy_config:

networks:
  mattermost-net:
    driver: bridge
```

Quelques points importants :

- **Ne mets jamais le port 8065 en écoute publique** (`0.0.0.0:8065`). On le lie à `127.0.0.1:8065` pour que seul Caddy puisse y accéder via le réseau interne Docker.
- Remplace `chat.tondomaine.com` par ton vrai nom de domaine.
- Change le mot de passe PostgreSQL. Évite les caractères spéciaux dans l'URL de connexion qui posent problème avec certaines versions.
- On utilise PostgreSQL 16, la version actuellement recommandée. Si tu veux en savoir plus sur la configuration Docker de PostgreSQL, consulte le guide [PostgreSQL Docker](/postgresql-docker-base-de-donnees/).

## Configuration du Caddyfile

Dans le même répertoire, crée le fichier `Caddyfile` :

```caddyfile
chat.tondomaine.com {
    reverse_proxy mattermost:8065
    encode gzip zstd
}
```

Caddy va automatiquement générer et renouveler le certificat SSL via Let's Encrypt. Si tu préfères utiliser Traefik ou Nginx Proxy Manager, l'adaptation est simple, il suffit de rediriger le trafic vers le port 8065 du conteneur Mattermost.

## Premier lancement

Lance la stack :

```bash
docker compose up -d
```

Attends 30 secondes que PostgreSQL initialise la base et que Mattermost démarre. Puis ouvre ton navigateur sur `https://chat.tondomaine.com`.

Tu vas tomber sur l'écran de configuration initiale. Crée ton compte administrateur, choisis un nom d'équipe et configure les paramètres de base. Ce compte sera le **System Admin**, garde-le précieusement.

## Configuration post-installation recommandée

Une fois connecté, va dans **System Console** (menu hamburger en haut à gauche > System Console) et applique ces réglages :

### Sécurité

- **Connection Security** : active "TLS" si tu passes par un reverse proxy (Caddy gère ça en amont, donc laisse "None" côté Mattermost).
- **Session Lengths** : raccourcis la durée des sessions web à 30 jours et mobile à 30 jours pour limiter les risques.
- **Password Requirements** : impose au moins 10 caractères, une majuscule, un chiffre et un symbole.

### Fichiers et stockage

- **File Storage** : vérifie que "Local File System" est sélectionné et que le chemin est `/mattermost/data/`. C'est ton volume Docker qui stockera les pièces jointes.
- **Maximum File Size** : par défaut 100 Mo. Augmente si ton équipe partage des vidéos ou des maquettes lourdes.

### Notifications et intégrations

- **Email Notifications** : configure un SMTP (SendGrid, Mailgun, ou ton propre serveur) pour que les utilisateurs reçoivent les mentions par mail.
- **Webhooks** : dans **Integrations > Incoming/Outgoing Webhooks**, tu peux créer des hooks pour relier Mattermost à GitLab, GitHub, Jenkins, etc.

## Les applications mobiles

Mattermost fournit des applications officielles gratuites sur l'App Store et Google Play. Par défaut, elles se connectent aux serveurs cloud Mattermost. Pour ton instance auto-hébergée :

1. Installe l'app Mattermost
2. Au premier lancement, tape l'URL de ton serveur : `https://chat.tondomaine.com`
3. Connecte-toi avec tes identifiants

Pas besoin de Google Firebase Cloud Messaging (FCM) ou d'Apple Push Notification Service (APNS) pour la base. Les notifications push fonctionnent en mode local, mais elles seront moins instantanées. Pour des notifications push fiables, Mattermost propose un serveur de notification push qu'il faut configurer séparément, ou utiliser le service push gratuit de Mattermost (les données de notification transitent alors par leurs serveurs, sans le contenu des messages).

## Sauvegarde de ton instance

Tes données vivent dans deux endroits : la base PostgreSQL et les volumes Mattermost. Pour sauvegarder complètement ton serveur, il te faut les deux.

**Dump PostgreSQL** :

```bash
docker exec mattermost-postgres pg_dump -U mmuser -d mattermost > mattermost-backup-$(date +%F).sql
```

**Volumes Mattermost** :

```bash
tar czvf mattermost-volumes-$(date +%F).tar.gz /var/lib/docker/volumes/mattermost-docker_mattermost_data/ /var/lib/docker/volumes/mattermost-docker_mattermost_config/
```

Automatise ça avec un cron quotidien qui pousse les archives vers un stockage distant (S3, rsync, BorgBackup...). Si tu cherches une solution de sauvegarde Docker complète, [BorgBackup Docker](/borgbackup-docker-sauvegarde/) est un excellent complément à cette stack.

## Mise à jour de Mattermost

Mattermost sort une nouvelle version tous les mois environ. Pour mettre à jour :

```bash
cd ~/mattermost-docker
docker compose pull mattermost
docker compose up -d mattermost
```

Le conteneur redémarre avec la nouvelle image. Les migrations de base de données se font automatiquement au démarrage. Fais toujours un backup avant une mise à jour majeure (changement de version majeure, ex: 9.x → 10.x).

## Comparaison avec les alternatives open-source

Mattermost n'est pas le seul chat d'équipe auto-hébergé. Voici comment il se compare :

| Logiciel | Protocole | Points forts | Points faibles |
|---|---|---|---|
| **Mattermost** | Propriétaire (API REST/WebSocket) | UX proche Slack, facile à déployer, apps mobiles natives | Pas de fédération entre serveurs |
| **Element (Matrix)** | Matrix (fédéré) | Fédération, chiffrement E2E, écosystème large | Plus complexe à administrer, UX moins polishée |
| **Rocket.Chat** | Propriétaire | Très configurable, large communauté | Consomme plus de RAM, UI moins réactive |
| **Zulip** | Propriétaire | Organisation par sujets (threads), idéal pour les devs | UX spécifique, courbe d'apprentissage |

Si tu veux une expérience la plus proche possible de Slack sans fédération, Mattermost est le choix le plus sûr. Si la fédération et le chiffrement de bout en bout sont des impératifs, oriente-toi vers Element/Matrix.

## Sécurité avancée

### Restreindre l'inscription

Par défaut, n'importe qui avec l'URL peut s'inscrire. Va dans **System Console > Authentication > Signup** et désactive "Enable Open Server". Après ça, seul un administrateur peut inviter des utilisateurs.

### Authentification à deux facteurs (2FA)

Active le TOTP dans **System Console > Authentication > MFA**. Chaque utilisateur devra scanner un QR code avec une app comme Aegis ou Google Authenticator.

### Rate limiting

Dans **System Console > Rate Limiting**, configure des limites pour éviter le brute-force sur l'API et les endpoints de connexion.

### Fail2Ban (optionnel)

Si tu veux aller plus loin, configure Fail2Ban pour bannir les IPs qui tentent trop de connexions échouées sur l'interface web de Mattermost.

## Monitoring

Mattermost expose des métriques Prometheus sur le port 8067 (à activer dans la config). Tu peux les scraper avec Prometheus et les visualiser dans Grafana. Ça te permet de surveiller :

- Le nombre de messages par seconde
- Les connexions WebSocket actives
- Les temps de réponse de l'API
- Les erreurs de la base de données

Si tu as déjà une stack [Grafana Prometheus Docker](/grafana-prometheus-docker-monitoring-pro/), ajoute simplement le endpoint Mattermost à ta configuration Prometheus.

## Dépannage rapide

**Mattermost ne démarre pas** : vérifie que PostgreSQL est bien "healthy" (`docker compose ps`) et que le mot de passe dans `MM_SQLSETTINGS_DATASOURCE` correspond à celui de PostgreSQL.

**Erreur "Site URL must be set"** : assure-toi que `MM_SERVICESETTINGS_SITEURL` contient bien `https://` avec ton domaine.

**Les uploads de fichiers échouent** : vérifie les permissions du volume `mattermost_data`. Le conteneur tourne avec l'UID 2000 par défaut.

**Les apps mobiles ne se connectent pas** : ton certificat SSL doit être valide (pas de self-signed). Caddy gère ça, mais vérifie que le DNS pointe bien vers ton serveur.

## Conclusion

Déployer Mattermost avec Docker, c'est récupérer la maîtrise totale de la messagerie de ton équipe. Pas de factures surprises, pas de clauses de confidentialité opaques, pas de limitation arbitraire sur l'historique. En une quinzaine de minutes, tu montes un Slack-like open-source sur ton propre serveur, avec PostgreSQL pour la base, Caddy pour le HTTPS et Docker pour orchestrer le tout. C'est exactement ce que l'auto-hébergement devrait être : simple, fiable et sous ton contrôle.
