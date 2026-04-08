---
title: "Nebula-Sync : synchroniser plusieurs Pi-hole v6 gratuitement (le remplaçant de Gravity Sync)"
pubDatetime: "2025-10-23T20:55:40+02:00"
description: "Découvrez Nebula-Sync, l''outil gratuit qui remplace Gravity Sync pour synchroniser plusieurs Pi-hole v6. Installation Docker + config complète."
tags:
  - docker
  - homelab
  - reseau
  - linux
  - guide
  - intermediaire
---

Spoiler : c’est le successeur non-officiel de Gravity Sync, et il est compatible avec Pi-hole v6.


- [Nebula-Sync vs Gravity Sync : le match](#nebula-sync-vs-gravity-sync-le-match)
- [Installation : toutes les options](#installation-toutes-les-options)
  - [Option 1 : Installation via binaire (sans Docker)](#option-1-installation-via-binaire-sans-docker)
  - [Option 2 : Installation via Docker Compose (recommandée)](#option-2-installation-via-docker-compose-recommandee)
  - [Option 3 : Docker run (pour les minimalistes)](#option-3-docker-run-pour-les-minimalistes)
- [Configuration de Pi-hole côté serveur](#configuration-de-pi-hole-cote-serveur)
  - [Étape 1 : Activer l’API](#etape-1-activer-l-api)
  - [Étape 2 : Générer un mot de passe d’application](#etape-2-generer-un-mot-de-passe-dapplication)
  - [Étape 3 : Activer webserver.api.app\_sudo sur les répliques](#etape-3-activer-webserver-api-app-sudo-sur-les-repliques)
      - [Méthode 1 : via l’interface web](#methode-1-via-linterface-web)
      - [Méthode 2 : via CLI](#methode-2-via-cli)
- [Configuration avancée : sync sélectif](#configuration-avancee-sync-selectif)
- [Lancer Nebula-Sync en homelab](#lancer-nebula-sync-en-production)
  - [Méthode 1 : Binaire + Systemd](#methode-1-binaire-systemd)
  - [Méthode 2 : Docker Compose (recommandée)](#methode-2-docker-compose-recommandee)
- [Monitoring avec webhooks](#monitoring-avec-webhooks)
  - [Exemple 1 : Healthchecks.io](#exemple-1-healthchecks-io)
  - [Exemple 2 : ntfy.sh (notification push)](#exemple-2-ntfy-sh-notification-push)
  - [Exemple 3 : Webhook custom avec JSON](#exemple-3-webhook-custom-avec-json)
- [Erreurs fréquentes et comment les résoudre](#erreurs-frequentes-et-comment-les-resoudre)
  - [« Failed to initialize service: permission denied »](#failed-to-initialize-service-permission-denied)
  - [« Authentication error » sur les répliques](#authentication-error-sur-les-repliques)
  - [Le sync ne se déclenche pas automatiquement](#le-sync-ne-se-declenche-pas-automatiquement)
  - [Les listes de blocage ne se synchronisent pas](#les-listes-de-blocage-ne-se-synchronisent-pas)
- [Cas d’usage : mon setup perso](#cas-dusage-mon-setup-perso)
- [Bonnes pratiques](#bonnes-pratiques)
- [Alternatives et comparaison](#alternatives-et-comparaison)
  - [Nebula-Sync vs Gravity Sync](#nebula-sync-vs-gravity-sync)
  - [Nebula-Sync vs scripts maison](#nebula-sync-vs-scripts-maison)
- [Pour aller plus loin](#pour-aller-plus-loin)
- [Conclusion : Nebula-Sync, le chaînon manquant de ton homelab](#conclusion-nebula-sync-le-chainon-manquant-de-ton-homelab)


Pourquoi synchroniser plusieurs Pi-hole ?

![](bounce-tv-confused-say-what-baffled-uvtau2ekhrsgifowfb.gif)Tu te dis peut-être : « Pourquoi avoir plusieurs Pi-hole ? » Bonne question.

**Haute disponibilité** : Si ton unique Pi-hole plante, tous tes appareils se retrouvent sans résolution DNS. Pas cool quand tu veux juste regarder Netflix un dimanche soir.

**Redondance géographique** : Un Pi-hole dans ton homelab principal, un autre sur un VPS distant ou chez un pote. Si ton internet coupe, le deuxième prend le relais.

**Load balancing** : Répartir la charge entre plusieurs serveurs DNS, surtout si tu as 50 devices IoT qui spamment des requêtes DNS toute la journée.

Le problème ? Maintenir la même config sur 2, 3, voire 10 Pi-hole, c’est l’enfer. Tu ajoutes une liste noire sur l’un, tu dois la recopier sur les autres. Avec Nebula-Sync, tu configures **un seul Pi-hole primaire**, et tous les autres répliques se synchronisent automatiquement.

Nebula-Sync vs Gravity Sync : le match

![](seinfeld-fight-george-costanza-6hfudkwlwcabc.gif)Si tu connais **Gravity Sync**, tu sais qu’il était LA solution pour synchroniser des Pi-hole. Problème : Gravity Sync n’est plus maintenu activement et n’est **pas compatible avec Pi-hole v6**.

Nebula-Sync reprend le concept, mais en mieux :

- Compatible Pi-hole v6.x (et uniquement v6, d’ailleurs)
- Écrit en Go (léger, rapide, un seul binaire)
- Support Docker natif
- Synchronisation complète (Teleporter) ou sélective
- Webhooks pour monitoring
- Cron intégré pour automatisation

Bref, si tu upgraes vers Pi-hole v6, Nebula-Sync est ton nouveau meilleur ami.

Installation : toutes les options

Nebula-Sync peut tourner en standalone (binaire Go) ou via Docker. Voyons les deux méthodes.

### Option 1 : Installation via binaire (sans Docker)

Télécharge la dernière version depuis les [releases GitHub](https://github.com/lovelaze/nebula-sync/releases/latest) :

```bash
# Télécharge le binaire
wget https://github.com/lovelaze/nebula-sync/releases/latest/download/nebula-sync-linux-amd64 -O nebula-sync

# Rends-le exécutable
chmod +x nebula-sync

# Déplace-le dans /usr/local/bin pour l'utiliser partout
sudo mv nebula-sync /usr/local/bin/

```

go install github.com/lovelaze/nebula-sync@latest


Vérifie que ça fonctionne :

```bash
nebula-sync --version

```

services:
  nebula-sync:
    image: ghcr.io/lovelaze/nebula-sync:latest
    container_name: nebula-sync
    environment:
      - PRIMARY=http://192.168.1.10|VotreSuperMotDePasse
      - REPLICAS=http://192.168.1.11|password1,http://192.168.1.12|password2
      - FULL_SYNC=true
      - RUN_GRAVITY=true
      - CRON=0 * * * *
      - TZ=Europe/Paris
    restart: unless-stopped


**Explications :**

- `PRIMARY` : URL + mot de passe de ton Pi-hole principal
- `REPLICAS` : Liste des Pi-hole à synchroniser (séparés par des virgules)
- `FULL_SYNC=true` : Synchronisation complète via Teleporter (recommandé)
- `RUN_GRAVITY=true` : Lance `pihole -g` après chaque sync
- `CRON=0 * * * *` : Sync toutes les heures
- `TZ=Europe/Paris` : Timezone pour les logs

Lance le conteneur :

```bash
docker-compose up -d

```

docker logs -f nebula-sync


### Option 3 : Docker run (pour les minimalistes)

Si tu veux juste tester rapidement sans docker-compose :

```bash
docker run --rm \
  --name nebula-sync \
  -e PRIMARY="http://192.168.1.10|password" \
  -e REPLICAS="http://192.168.1.11|password" \
  -e FULL_SYNC=true \
  -e RUN_GRAVITY=true \
  ghcr.io/lovelaze/nebula-sync:latest

```

sudo nano /etc/pihole/pihole.toml


Trouve la section `[webserver.api]` et modifie :

```bash
[webserver.api]
app_sudo = true  # Change de false à true

```

sudo systemctl restart pihole-FTL


**Répète ça sur chaque réplique.** Oublie cette étape, et Nebula-Sync va se plaindre d’erreurs d’authentification.

Configuration avancée : sync sélectif

Si tu ne veux pas tout synchroniser (par exemple, tu veux garder des listes DHCP différentes sur chaque Pi-hole), tu peux désactiver `FULL_SYNC` et choisir précisément ce que tu synchronises.

Exemple de fichier `.env` pour un sync ultra-personnalisé :

```bash
PRIMARY=http://192.168.1.10|password
REPLICAS=http://192.168.1.11|password,http://192.168.1.12|password
FULL_SYNC=false

# Sync uniquement les paramètres DNS
SYNC_CONFIG_DNS=true

# Sync les listes de blocage
SYNC_GRAVITY_AD_LIST=true
SYNC_GRAVITY_AD_LIST_BY_GROUP=true

# Sync les domaines autorisés/bloqués
SYNC_GRAVITY_DOMAIN_LIST=true
SYNC_GRAVITY_DOMAIN_LIST_BY_GROUP=true

# Ne synchronise PAS les clients ni le DHCP
SYNC_GRAVITY_CLIENT=false
SYNC_CONFIG_DHCP=false

RUN_GRAVITY=true
CRON=0 2 * * *  # Sync tous les jours à 2h du mat
TZ=Europe/Paris

```

[Unit]
Description=Nebula Sync - Pi-hole Synchronization
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/nebula-sync run --env-file /etc/nebula-sync/.env
User=root

[Install]
WantedBy=multi-user.target

**Créer un timer systemd** (pour exécution périodique) :

```bash
[Unit]
Description=Nebula Sync Timer
Requires=nebula-sync.service

[Timer]
OnBootSec=5min
OnUnitActiveSec=30min

[Install]
WantedBy=timers.target
```

systemctl daemon-reload
systemctl enable nebula-sync.timer
systemctl enable nebula-sync.service
systemctl start nebula-sync.timer

# Vérifier
systemctl status nebula-sync.timer
systemctl list-timers

### Méthode 2 : Docker Compose (recommandée)

Avec le `docker-compose.yml` donné plus haut, lance simplement :

```bash
docker-compose up -d

```

docker ps | grep nebula-sync


Check les logs en temps réel :

```bash
docker logs -f nebula-sync

```

WEBHOOK_SYNC_SUCCESS_URL=https://hc-ping.com/ton-uuid-ici
WEBHOOK_SYNC_FAILURE_URL=https://hc-ping.com/ton-uuid-ici/fail


À chaque sync réussi, Healthchecks.io recevra un ping. Si un sync rate, tu recevras une alerte.

### Exemple 2 : ntfy.sh (notification push)

```bash
WEBHOOK_SYNC_FAILURE_URL=https://ntfy.sh/monpiholebackup
WEBHOOK_SYNC_FAILURE_BODY=Sync Pi-hole a échoué !

```

WEBHOOK_SYNC_FAILURE_URL=https://ton-serveur.com/api/alert
WEBHOOK_SYNC_FAILURE_METHOD=POST
WEBHOOK_SYNC_FAILURE_BODY={"service":"nebula-sync","status":"failed"}
WEBHOOK_SYNC_FAILURE_HEADERS=Content-Type:application/json


Bref, tu peux brancher n’importe quel système de monitoring.

Erreurs fréquentes et comment les résoudre

### « Failed to initialize service: permission denied »

**Cause :** Le conteneur Docker (qui tourne sous l’utilisateur `1001` par défaut) n’a pas les droits de lecture sur tes fichiers secrets.

**Solution :**

```bash
sudo chown 1001:1001 /path/to/secrets/*
sudo chmod 400 /path/to/secrets/*

```

user: "1000:1000"  # Ton propre UID


### « Authentication error » sur les répliques

**Cause :** Tu n’as pas activé `webserver.api.app_sudo` sur tes Pi-hole répliques.

**Solution :** Retourne dans la section « Configuration de Pi-hole côté serveur » et active cette option.

### Le sync ne se déclenche pas automatiquement

**Cause :** Le cron n’est pas bien configuré.

**Solution :** Vérifie que la variable `CRON` est bien définie. Format : `minute heure jour mois jour_de_semaine`.

Exemples :

- `0 * * * *` = Toutes les heures
- `*/30 * * * *` = Toutes les 30 minutes
- `0 2 * * *` = Tous les jours à 2h du matin

### Les listes de blocage ne se synchronisent pas

**Cause :** Si `FULL_SYNC=false`, tu dois activer manuellement les options de sync.

**Solution :** Ajoute :

```bash
SYNC_GRAVITY_AD_LIST=true
SYNC_GRAVITY_AD_LIST_BY_GROUP=true

```

services:
  nebula-sync:
    image: ghcr.io/lovelaze/nebula-sync:latest
    container_name: nebula-sync
    environment:
      - PRIMARY=http://192.168.1.10|MotDePassePrimaire
      - REPLICAS=http://192.168.1.11|password1,http://100.64.0.5|password2
      - FULL_SYNC=true
      - RUN_GRAVITY=true
      - CRON=0 */2 * * *  # Sync toutes les 2 heures
      - TZ=Europe/Paris
      - WEBHOOK_SYNC_FAILURE_URL=https://ntfy.sh/monpiholebackup
    restart: unless-stopped


Résultat : je modifie les listes noires sur mon Pi-hole principal, et dans les 2 heures max, tous mes autres Pi-hole sont à jour. Si un sync plante, je reçois une notif push.

Bonnes pratiques

**Fais une sauvegarde Teleporter avant** : Avant d’activer Nebula-Sync pour la première fois, exporte ta config via Teleporter sur tous tes Pi-hole. Au cas où.

**Teste avec `FULL_SYNC=true` d’abord** : Commence avec une synchro complète pour voir si tout fonctionne. Tu optimiseras avec le sync sélectif plus tard.

**Surveille les logs les premiers jours** :

```bash
docker logs -f nebula-sync

```
