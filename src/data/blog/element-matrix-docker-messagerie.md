---
title: "Element + Matrix Docker : héberge ta messagerie décentralisée"
description: Héberge ta propre messagerie Matrix avec Element et Docker. Guide complet pour un serveur Synapse décentralisé, sécurisé et fédéré.
pubDatetime: "2026-08-18T06:00:00.000Z"
modDatetime: "2026-08-18T06:00:00.000Z"
author: Brandon Visca
tags:
  - intermediaire
  - auto-hebergement
  - messagerie
  - matrix
  - docker
  - decentralise
featured: false
draft: false
focusKeyword: element matrix docker
ogImage: ""
---
> 💡 **TL;DR**
>
> - Matrix est un protocole de messagerie décentralisé et fédéré. Element est le client web le plus populaire.
> - Synapse est le homeserver de référence. On le déploie avec Element et PostgreSQL en quelques minutes via Docker Compose.
> - Tu obtiens un serveur de chat auto-hébergé, chiffré de bout en bout, fédéré avec le réseau Matrix mondial.

## Pourquoi Matrix et pas WhatsApp, Signal ou Slack ?

WhatsApp appartient à Meta. Signal est mieux, mais tu dépends toujours de leurs serveurs. Slack ? C'est fermé, payant, et tes données dorment chez Salesforce. Matrix, c'est différent. C'est un **protocole** ouvert, pas un produit. Tu installes un **homeserver** chez toi (Synapse), tu choisis ton client (Element, Cinny, FluffyChat), et tu communiques avec n'importe qui sur le réseau Matrix mondial. Ou personne, si tu préfères rester en interne.

Ce qui change la donne :

- **Décentralisation** : chacun héberge son serveur. Pas de point unique de défaillance.
- **Fédération** : ton serveur parle aux autres. Un utilisateur `@alice:mondomaine.fr` peut discuter avec `@bob:matrix.org` sans compte chez l'autre.
- **Chiffrement E2E** : activé par défaut dans les salons privés. Même ton admin ne peut pas lire les messages.
- **Open-source** : le code est public, audité, extensible.
- **Pas de forçage** : pas de numéro de téléphone obligatoire, pas de "nous avons mis à jour nos CGU".

Si tu veux une messagerie d'équipe plus classique sans fédération, [Mattermost](/mattermost-docker-chat-equipe/) ou [Rocket.Chat](/rocket-chat-docker-messagerie-auto-hebergee/) sont de très bonnes alternatives auto-hébergées. Mais si la décentralisation te parle, Matrix est le seul choix sérieux.

## Architecture du déploiement

On va monter trois services conteneurisés :

1. **Synapse** : le homeserver Matrix. C'est le cœur du système. Il gère les comptes, les salons, les messages, la fédération.
2. **PostgreSQL** : base de données de Synapse. SQLite est possible pour tester, mais tu veux du PostgreSQL en production.
3. **Element Web** : l'interface web. C'est le client que tes utilisateurs ouvrent dans leur navigateur.

Tu peux ajouter un reverse proxy (Caddy, [Traefik](/traefik-reverse-proxy-docker/), Nginx Proxy Manager) pour le HTTPS. Pour un accès distant sécurisé, un tunnel [WireGuard](/wireguard-docker-vpn-homelab/) ou un VPN est recommandé.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose
- Un nom de domaine (ou sous-domaine) pointant vers ton serveur : `matrix.tondomaine.fr`
- 2 Go de RAM minimum (4 Go recommandés pour Synapse + PostgreSQL)
- 20 Go d'espace disque SSD

## Génération de la configuration Synapse

Synapse a besoin d'un fichier de configuration généré avant le premier démarrage. Crée un dossier dédié :

```bash
mkdir -p ~/matrix-docker
cd ~/matrix-docker
```

Génère la config avec l'image officielle :

```bash
docker run -it --rm \
  -v "$(pwd)/synapse-data:/data" \
  -e SYNAPSE_SERVER_NAME=matrix.tondomaine.fr \
  -e SYNAPSE_REPORT_STATS=no \
  matrixdotorg/synapse:latest generate
```

Remplace `matrix.tondomaine.fr` par ton vrai domaine. Cette commande crée `homeserver.yaml` et un certificat auto-signé dans `./synapse-data/`.

Tu dois éditer `synapse-data/homeserver.yaml` pour quelques ajustements essentiels :

```yaml
# Autoriser l'inscription (à désactiver après création des comptes)
enable_registration: true

# Limiter les inscriptions si besoin
registration_requires_token: false

# URL publique du serveur
public_baseurl: https://matrix.tondomaine.fr/

# Activer le chiffrement E2E par défaut dans les nouveaux salons
default_room_version: "10"

# Logs
log_config: "/data/matrix.tondomaine.fr.log.config"

# Base de données PostgreSQL (on la configure via Docker Compose)
```

Tu peux aussi limiter les inscriptions à des jetons si tu ne veux pas que n'importe qui crée un compte.

## Le docker-compose.yml

Voici le fichier complet. Il embarque Synapse, PostgreSQL et Element Web :

```yaml
version: "3.8"

services:
  synapse:
    image: matrixdotorg/synapse:latest
    container_name: synapse
    restart: unless-stopped
    volumes:
      - ./synapse-data:/data
    environment:
      - SYNAPSE_SERVER_NAME=matrix.tondomaine.fr
      - SYNAPSE_REPORT_STATS=no
    ports:
      - "8008:8008"
    depends_on:
      - postgres

  postgres:
    image: postgres:16-alpine
    container_name: matrix-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: synapse
      POSTGRES_PASSWORD: supermotdepasseachanger
      POSTGRES_DB: synapse
    volumes:
      - postgres-data:/var/lib/postgresql/data

  element-web:
    image: vectorim/element-web:latest
    container_name: element-web
    restart: unless-stopped
    volumes:
      - ./element-config.json:/app/config.json:ro
    ports:
      - "8080:80"
    depends_on:
      - synapse

volumes:
  postgres-data:
```

**Points importants :**

- `supermotdepasseachanger` : change ce mot de passe. Maintenant.
- Le port `8008` expose l'API Matrix de Synapse.
- Element Web écoute sur `8080`. En production, tu le mets derrière un reverse proxy HTTPS.

## Configuration d'Element Web

Crée un fichier `element-config.json` à côté de ton `docker-compose.yml` :

```json
{
  "default_server_config": {
    "m.homeserver": {
      "base_url": "https://matrix.tondomaine.fr",
      "server_name": "matrix.tondomaine.fr"
    }
  },
  "disable_custom_urls": false,
  "disable_guests": true,
  "brand": "Element",
  "integrations_ui_url": "https://scalar.vector.im/",
  "integrations_rest_url": "https://scalar.vector.im/api"
}
```

Ce fichier dit à Element : "connecte-toi par défaut à ce homeserver". Sans ça, tes utilisateurs devraient taper l'URL à la main.

## Connexion de Synapse à PostgreSQL

Édite `synapse-data/homeserver.yaml` et remplace la section `database` par :

```yaml
database:
  name: psycopg2
  args:
    user: synapse
    password: supermotdepasseachanger
    database: synapse
    host: postgres
    port: 5432
    cp_min: 5
    cp_max: 10
```

Assure-toi que le mot de passe correspond à celui du `docker-compose.yml`.

## Lancement

Lance la stack :

```bash
docker compose up -d
```

Attends 10-15 secondes que PostgreSQL démarre, puis vérifie les logs :

```bash
docker logs -f synapse
```

Tu dois voir Synapse se connecter à PostgreSQL et écouter sur le port `8008`.

## Création du premier compte administrateur

Synapse ne crée pas d'admin par défaut. Tu dois le faire manuellement :

```bash
docker exec -it synapse register_new_matrix_user \
  http://localhost:8008 \
  -c /data/homeserver.yaml \
  -u admin \
  -p tonmotdepasse \
  -a
```

L'option `-a` donne les droits admin. Sans ça, c'est un utilisateur standard.

## Reverse proxy et HTTPS

En production, tu dois exposer Synapse et Element en HTTPS. Voici les labels pour Traefik (dans le `docker-compose.yml`) :

```yaml
  synapse:
    # ... config existante ...
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.synapse.rule=Host(`matrix.tondomaine.fr`)"
      - "traefik.http.routers.synapse.entrypoints=websecure"
      - "traefik.http.routers.synapse.tls.certresolver=letsencrypt"
      - "traefik.http.services.synapse.loadbalancer.server.port=8008"

  element-web:
    # ... config existante ...
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.element.rule=Host(`chat.tondomaine.fr`)"
      - "traefik.http.routers.element.entrypoints=websecure"
      - "traefik.http.routers.element.tls.certresolver=letsencrypt"
      - "traefik.http.services.element.loadbalancer.server.port=80"
```

Si tu préfères Nginx Proxy Manager ou Caddy, adapte les blocs `server` ou les labels en conséquence. L'essentiel est que les requêtes vers `/_matrix` atteignent bien Synapse.

## Fédération : parler au monde extérieur

Par défaut, ton homeserver est isolé. Pour rejoindre le réseau Matrix mondial, tu dois :

1. Exposer le port `8448` (ou utiliser le port `443` avec un fichier `.well-known`)
2. Configurer un fichier `.well-known/matrix/server` sur ton domaine principal

Si ton domaine est `tondomaine.fr` et ton homeserver `matrix.tondomaine.fr`, crée ce fichier accessible à `https://tondomaine.fr/.well-known/matrix/server` :

```json
{
  "m.server": "matrix.tondomaine.fr:443"
}
```

Ou si tu utilises le port 8448 dédié :

```json
{
  "m.server": "matrix.tondomaine.fr:8448"
}
```

Synapse détecte automatiquement ce fichier et configure la fédération. Tu peux vérifier que tout fonctionne avec le [federation tester](https://federationtester.matrix.org/) officiel.

## Chiffrement de bout en bout

Dans Element, chaque salon privé peut être chiffré E2E. Le chiffrement est géré côté client : Synapse ne voit que des messages chiffrés. Pour activer le chiffrement dans un salon :

1. Crée un salon (ou entre dans un salon privé existant)
2. Clique sur les paramètres du salon → Sécurité et confidentialité
3. Active "Chiffrement de bout en bout"

La première fois, Element génère des clés sur ton appareil. Sauvegarde ta clé de récupération (Security Key) dans un gestionnaire de mots de passe. Sans elle, tu perdras l'historique chiffré si tu changes de navigateur.

## Sauvegarde et monitoring

Synapse stocke tout dans PostgreSQL. Une sauvegarde classique du volume `postgres-data` suffit :

```bash
docker exec -t matrix-postgres pg_dump -U synapse synapse > backup_synapse.sql
```

Pour la sécurité, je recommande d'ajouter un pare-feu applicatif comme [CrowdSec](/crowdsec-docker-securite-collaborative/) devant ton reverse proxy. Synapse expose des endpoints publics pour la fédération, et tu ne veux pas qu'un bot brute-force les tokens d'accès.

Surveille aussi l'espace disque : les médias partagés (images, fichiers) s'accumulent dans `synapse-data/media_store`. Synapse a une commande de purge intégrée :

```bash
docker exec synapse synapse_auto_compressor -c /data/homeserver.yaml
```

## Évolution et alternatives

Matrix n'est pas qu'un chat. Le protocole supporte les appels vidéo via Element Call, les widgets intégrés, les ponts vers Discord/Slack/Telegram (via [mautrix](https://docs.mau.fi/)), et même les espaces (groupes de salons). Si tu veux aller plus loin, explore :

- **Synapse-Admin** : interface web pour gérer les utilisateurs, salons et médias
- **Maubot** : framework de bots Python pour Matrix
- **Element X** : client mobile réécrit en Rust, plus rapide
- **Conduit** : homeserver alternatif en Rust, beaucoup plus léger que Synapse

## Conclusion

Héberger son homeserver Matrix avec Element et Docker, c'est reprendre le contrôle de sa messagerie. Pas de tiers de confiance, pas de facture mensuelle, pas de surprise dans les conditions d'utilisation. Tu installes Synapse, tu connectes Element, et tu discutes avec le monde entier, ou personne. La décentralisation n'est pas une mode. C'est une assurance contre la fermeture, la censure et la surveillance de masse. Matrix est le seul protocole de messagerie qui te donne vraiment ce choix. Utilise-le.
