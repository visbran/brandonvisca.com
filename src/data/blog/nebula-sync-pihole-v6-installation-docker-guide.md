---
title: "Nebula-Sync : synchronise tes Pi-hole v6 automatiquement (remplace Gravity Sync)"
description: "Découvrez Nebula-Sync, l'outil gratuit qui remplace Gravity Sync pour synchroniser plusieurs Pi-hole v6. Installation Docker + config complète."
pubDatetime: "2025-10-23T20:55:40+02:00"
modDatetime: 2026-04-16 00:00:00+01:00
author: Brandon Visca
tags:
  - nebula-sync
  - pihole
  - dns
  - docker
  - homelab
  - intermediaire
featured: false
draft: false
focusKeyword: Nebula-Sync
---
> 💡 **TL;DR** — Nebula-Sync est le successeur de Gravity Sync compatible Pi-hole v6. Il synchronise automatiquement tes Pi-hole (listes noires, config DNS, groupes) via Docker ou binaire Go. Un docker-compose de 10 lignes suffit pour démarrer.

Spoiler : c'est le successeur non-officiel de Gravity Sync, et il est compatible avec Pi-hole v6.

## Table des matières

## Pourquoi synchroniser plusieurs Pi-hole ?

![481](bounce-tv-confused-say-what-baffled-uvtau2ekhrsgifowfb.gif)

Tu te dis peut-être : « Pourquoi avoir plusieurs Pi-hole ? » Bonne question. Et si tu découvres Pi-hole pour la première fois, commence par [mon guide auto-hébergement complet](/auto-hebergement-guide-complet-2025/) avant de revenir ici.

**Haute disponibilité** : Si ton unique Pi-hole plante, tous tes appareils se retrouvent sans résolution DNS. Pas cool quand tu veux juste regarder Netflix un dimanche soir.

**Redondance géographique** : Un Pi-hole dans ton homelab principal, un autre sur un VPS distant ou chez un pote. Si ton internet coupe, le deuxième prend le relais.

**Load balancing** : Répartir la charge entre plusieurs serveurs DNS, surtout si tu as 50 devices IoT qui spamment des requêtes DNS toute la journée.

Le problème ? Maintenir la même config sur 2, 3, voire 10 Pi-hole, c'est l'enfer. Tu ajoutes une liste noire sur l'un, tu dois la recopier sur les autres. Avec Nebula-Sync, tu configures **un seul Pi-hole primaire**, et tous les autres répliques se synchronisent automatiquement.

## Nebula-Sync vs Gravity Sync : le match

![537](seinfeld-fight-george-costanza-6hfudkwlwcabc.gif)

Si tu connais **Gravity Sync**, tu sais qu'il était LA solution pour synchroniser des Pi-hole. Problème : Gravity Sync n'est plus maintenu activement et n'est **pas compatible avec Pi-hole v6**.

Nebula-Sync reprend le concept, mais en mieux :

- Compatible Pi-hole v6.x (et uniquement v6, d'ailleurs)
- Écrit en Go (léger, rapide, un seul binaire)
- Support Docker natif
- Synchronisation complète (Teleporter) ou sélective
- Webhooks pour monitoring
- Cron intégré pour automatisation

Bref, si tu upgraes vers Pi-hole v6, Nebula-Sync est ton nouveau meilleur ami.

## Installation : toutes les options

Nebula-Sync peut tourner en standalone (binaire Go) ou via Docker. Si tu débutes avec Docker, [ce guide te mettra à niveau en 20 minutes](/docker-debutant-services-auto-heberger/) avant de revenir ici.

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

Si tu as Go d'installé, tu peux aussi compiler directement :

```bash
go install github.com/lovelaze/nebula-sync@latest
```

Vérifie que ça fonctionne :

```bash
nebula-sync --version
```

### Option 2 : Installation via Docker Compose (recommandée)

Crée un fichier `docker-compose.yml` :

```yaml
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
```

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

Vérifie que le conteneur tourne :

```bash
docker logs -f nebula-sync
```

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

## Configuration de Pi-hole côté serveur

Avant que Nebula-Sync puisse se connecter à tes Pi-hole, il faut configurer l'API sur chaque instance : primaire et répliques.

### Étape 1 : Activer l'API

Ouvre le fichier de config Pi-hole :

```bash
sudo nano /etc/pihole/pihole.toml
```

Trouve la section `[webserver.api]` et assure-toi que l'API est activée (elle l'est par défaut sur Pi-hole v6).

### Étape 2 : Générer un mot de passe d'application

Dans l'interface web Pi-hole v6, va dans **Settings → API → App Password** et génère un mot de passe dédié. C'est ce mot de passe que tu utiliseras dans `PRIMARY` et `REPLICAS`.

### Étape 3 : Activer webserver.api.app_sudo sur les répliques

Cette étape est critique pour les Pi-hole répliques. Sans ça, Nebula-Sync ne pourra pas exécuter `pihole -g` après le sync.

#### Méthode 1 : via l'interface web

Dans **Settings → API**, active l'option **Allow sudo**.

#### Méthode 2 : via CLI

```bash
sudo nano /etc/pihole/pihole.toml
```

Trouve la section `[webserver.api]` et modifie :

```toml
[webserver.api]
app_sudo = true  # Change de false à true
```

Puis redémarre Pi-hole FTL :

```bash
sudo systemctl restart pihole-FTL
```

**Répète ça sur chaque réplique.** Oublie cette étape, et Nebula-Sync va se plaindre d'erreurs d'authentification.

> ⚠️ **Attention** — `webserver.api.app_sudo = true` donne à Nebula-Sync les droits d'exécuter des commandes en tant que root via l'API Pi-hole. Limite l'accès réseau au conteneur Nebula-Sync uniquement : n'expose jamais le port API Pi-hole sur l'extérieur.

## Configuration avancée : sync sélectif

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

## Lancer Nebula-Sync en homelab

### Méthode 1 : Binaire + Systemd

Crée un service systemd `/etc/systemd/system/nebula-sync.service` :

```ini
[Unit]
Description=Nebula Sync - Pi-hole Synchronization
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/nebula-sync run --env-file /etc/nebula-sync/.env
User=root

[Install]
WantedBy=multi-user.target
```

**Créer un timer systemd** (pour exécution périodique) :

```ini
[Unit]
Description=Nebula Sync Timer
Requires=nebula-sync.service

[Timer]
OnBootSec=5min
OnUnitActiveSec=30min

[Install]
WantedBy=timers.target
```

Active et démarre le tout :

```bash
systemctl daemon-reload
systemctl enable nebula-sync.timer
systemctl enable nebula-sync.service
systemctl start nebula-sync.timer

# Vérifier
systemctl status nebula-sync.timer
systemctl list-timers
```

### Méthode 2 : Docker Compose (recommandée)

Avec le `docker-compose.yml` donné plus haut, lance simplement :

```bash
docker-compose up -d
```

Vérifie que le conteneur tourne :

```bash
docker ps | grep nebula-sync
```

Check les logs en temps réel :

```bash
docker logs -f nebula-sync
```

## Monitoring avec webhooks

Nebula-Sync supporte les webhooks pour t'alerter en cas de succès ou d'échec de sync.

### Exemple 1 : Healthchecks.io

```bash
WEBHOOK_SYNC_SUCCESS_URL=https://hc-ping.com/ton-uuid-ici
WEBHOOK_SYNC_FAILURE_URL=https://hc-ping.com/ton-uuid-ici/fail
```

À chaque sync réussi, Healthchecks.io recevra un ping. Si un sync rate, tu recevras une alerte.

### Exemple 2 : ntfy.sh (notification push)

```bash
WEBHOOK_SYNC_FAILURE_URL=https://ntfy.sh/monpiholebackup
WEBHOOK_SYNC_FAILURE_BODY=Sync Pi-hole a échoué !
```

### Exemple 3 : Webhook custom avec JSON

```bash
WEBHOOK_SYNC_FAILURE_URL=https://ton-serveur.com/api/alert
WEBHOOK_SYNC_FAILURE_METHOD=POST
WEBHOOK_SYNC_FAILURE_BODY={"service":"nebula-sync","status":"failed"}
WEBHOOK_SYNC_FAILURE_HEADERS=Content-Type:application/json
```

Bref, tu peux brancher n'importe quel système de monitoring.

## Erreurs fréquentes et comment les résoudre

### « Failed to initialize service: permission denied »

**Cause :** Le conteneur Docker (qui tourne sous l'utilisateur `1001` par défaut) n'a pas les droits de lecture sur tes fichiers secrets.

**Solution :**

```bash
sudo chown 1001:1001 /path/to/secrets/*
sudo chmod 400 /path/to/secrets/*
```

Ou dans ton docker-compose, force l'UID :

```yaml
user: "1000:1000"  # Ton propre UID
```

### « Authentication error » sur les répliques

**Cause :** Tu n'as pas activé `webserver.api.app_sudo` sur tes Pi-hole répliques.

**Solution :** Retourne dans la section « Configuration de Pi-hole côté serveur » et active cette option.

### Le sync ne se déclenche pas automatiquement

**Cause :** Le cron n'est pas bien configuré.

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

## Cas d'usage : mon setup perso

Chez moi, j'ai trois Pi-hole : un sur mon homelab principal, un sur un VPS OVH, et un troisième sur mon VPN Tailscale (adresse en `100.64.x.x`). C'est le même setup que j'utilise pour tous mes services auto-hébergés. Tu peux voir l'approche globale dans [mon guide indépendance numérique](/independance-numerique-2025-guide-complet/). Voilà mon docker-compose de prod :

```yaml
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
```

Résultat : je modifie les listes noires sur mon Pi-hole principal, et dans les 2 heures max, tous mes autres Pi-hole sont à jour. Si un sync plante, je reçois une notif push sur mon téléphone.

## Bonnes pratiques

> 💡 **Astuce** — Avant d'activer Nebula-Sync, exporte ta config Pi-hole via **Settings → Teleporter → Export** sur chaque instance. Si quelque chose tourne mal lors du premier sync, tu peux restaurer en 30 secondes.

**Fais une sauvegarde Teleporter avant** : C'est le filet de sécurité numéro 1.

**Teste avec `FULL_SYNC=true` d'abord** : Commence avec une synchro complète pour voir si tout fonctionne. Tu optimiseras avec le sync sélectif plus tard.

**Surveille les logs les premiers jours** :

```bash
docker logs -f nebula-sync
```

**Utilise des mots de passe d'application distincts** : Ne réutilise pas ton mot de passe admin Pi-hole. Génère un app password dédié pour Nebula-Sync depuis l'interface web.

**Planifie des syncs en heures creuses** : `CRON=0 3 * * *` (3h du matin) pour éviter de surcharger ton DNS pendant les heures d'utilisation.

## Alternatives et comparaison

### Nebula-Sync vs Gravity Sync

| Critère | Nebula-Sync | Gravity Sync |
|---|---|---|
| Compatible Pi-hole v6 | Oui | Non |
| Maintenance active | Oui (2024+) | Abandonnée |
| Installation | Docker ou binaire Go | Script bash |
| Sync sélectif | Oui | Partiel |
| Webhooks | Oui | Non |
| Dépendances | Aucune (Go) | SSH, rsync |

**Verdict** : Gravity Sync est mort pour Pi-hole v6. Nebula-Sync est le seul choix viable aujourd'hui.

### Nebula-Sync vs scripts maison

Tu pourrais écrire un script cron qui fait un `pihole -t` + `rsync` entre tes instances. Ça marche, mais tu réinventes la roue : pas de gestion des erreurs, pas de webhooks, et la moindre mise à jour Pi-hole peut tout casser. Nebula-Sync gère tout ça proprement avec l'API officielle.

## Conclusion

Si tu as plusieurs Pi-hole v6 et que tu veux arrêter de les synchroniser à la main, Nebula-Sync est la solution. Un conteneur Docker, quelques variables d'environnement, et c'est plié. Gravity Sync est mort, longue vie à Nebula-Sync.

La prochaine étape logique : combine Nebula-Sync avec une config Pi-hole solide. Listes de blocage optimisées, DNS-over-HTTPS, surveillance des requêtes. Ton homelab DNS ne sera plus jamais un point de défaillance unique.

Et si tu parts de zéro ou envisages une migration, [Technitium DNS Server](/technitium-dns-server/) propose blocage de pubs + DNS récursif natif + DNSSEC dans un seul conteneur — sans dépendance à dnsmasq ni à Unbound.

## Pour aller plus loin

- [Docker pour débutants : les services à auto-héberger absolument](/docker-debutant-services-auto-heberger/)
- [Nextcloud avec Docker : ton cloud perso en 1h](/nextcloud-docker-installation-complete-2025/)
- [Auto-hébergement : le guide complet pour débutants](/auto-hebergement-guide-complet-2025/)
