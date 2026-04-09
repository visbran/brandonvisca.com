---
title: "Nextcloud avec Docker : Ton Cloud Perso en 1h (Adieu Google Drive !)"
pubDatetime: "2025-10-26T20:58:49+01:00"
author: Brandon Visca
description: "Installe Nextcloud avec Docker en 30 min. Alternative Google Drive auto-hébergée, économise 120€/an. Guide 2025 complet + HTTPS gratuit."
tags:
  - docker
  - auto-hebergement
  - homelab
  - linux
  - guide
  - intermediaire
---

🎯 TL;DR

Tu paies 10-20€/mois pour Google Drive, Dropbox ou OneDrive ? Spoiler : tu peux héberger **ton propre cloud avec Nextcloud** pour 3-5€/mois sur un petit VPS.

**Ce que tu vas apprendre :**

- Installer Nextcloud avec Docker en 30 minutes chrono
- Configuration HTTPS automatique (Let’s Encrypt)
- Synchronisation multi-appareils (PC, mobile, tablette)
- Économiser 120-240€/an en virant tes abonnements cloud
- Garder le contrôle total de tes données (hello RGPD 🇫🇷)

**Prérequis :**

- Un serveur Linux (VPS ou machine chez toi)
- 2 Go RAM minimum, 4 Go recommandé
- 20 Go d’espace disque (+ ce que tu veux stocker)
- Un nom de domaine (10€/an suffit)
- 1h de ton temps

- - - - - -

Pourquoi Nextcloud &gt; Google Drive (et les autres)

### Le calcul économique qui fâche

**Google Drive :**

- 100 Go : 2€/mois = **24€/an**
- 200 Go : 3€/mois = **36€/an**
- 2 To : 10€/mois = **120€/an**

**Nextcloud auto-hébergé :**

- VPS 2 Go RAM : 4€/mois = **48€/an**
- Domaine : **10€/an**
- **Total : 58€/an pour stockage illimité** (dans la limite de ton VPS)

💰 **Économie sur 5 ans avec 2 To :** 120€ x 5 – 58€ x 5 = **310€ économisés**

Et encore, si tu as déjà un serveur chez toi (Raspberry Pi, vieux PC…), c’est **gratuit** à part l’électricité.

### Ce que tu gagnes en plus

✅ **Vie privée** : Tes fichiers ne partent pas aux USA  
✅ **Pas de limite** : Tu choisis ta capacité  
✅ **Apps intégrées** : Calendrier, contacts, notes, galerie photos, visio…  
✅ **Partage de fichiers** : Comme WeTransfer mais à toi  
✅ **Conforme RGPD** : Si c’est hébergé en France, tes données restent en France

- - - - - -


- [Pourquoi Nextcloud &gt; Google Drive (et les autres)](#pourquoi-nextcloud-google-drive-et-les-autres)
  - [Le calcul économique qui fâche](#le-calcul-economique-qui-fache)
  - [Ce que tu gagnes en plus](#ce-que-tu-gagnes-en-plus)
- [Avant de commencer : Choisir ton setup](#avant-de-commencer-choisir-ton-setup)
  - [Option 1 : VPS Cloud (recommandé pour débuter)](#option-1-vps-cloud-recommande-pour-debuter)
  - [Option 2 : Homelab (gratuit mais plus technique)](#option-2-homelab-gratuit-mais-plus-technique)
- [Installation Nextcloud avec Docker : La méthode propre](#installation-nextcloud-avec-docker-la-methode-propre)
  - [Étape 1 : Préparer le serveur](#etape-1-preparer-le-serveur)
  - [Étape 2 : Créer la structure Docker Compose](#etape-2-creer-la-structure-docker-compose)
  - [Étape 3 : Lancer Nextcloud](#etape-3-lancer-nextcloud)
  - [Étape 4 : Configuration HTTPS avec Nginx Proxy Manager](#etape-4-configuration-https-avec-nginx-proxy-manager)
  - [Étape 5 : Configuration initiale Nextcloud](#etape-5-configuration-initiale-nextcloud)
- [Optimisations post-installation (important !)](#optimisations-post-installation-important)
  - [Activer le cache Redis](#activer-le-cache-redis)
  - [Augmenter la limite d’upload](#augmenter-la-limite-dupload)
  - [Sécuriser avec fail2ban (optionnel mais recommandé)](#securiser-avec-fail-2-ban-optionnel-mais-recommande)
- [Synchronisation multi-appareils](#synchronisation-multi-appareils)
  - [Desktop (Windows/Mac/Linux)](#desktop-windows-mac-linux)
  - [Mobile (Android/iOS)](#mobile-android-i-os)
- [Cas d’usage réels : Qui utilise Nextcloud ?](#cas-dusage-reels-qui-utilise-nextcloud)
  - [Scénario 1 : Famille (4 personnes)](#scenario-1-famille-4-personnes)
  - [Scénario 2 : Freelance / Entrepreneur Solo](#scenario-2-freelance-entrepreneur-solo)
  - [Scénario 3 : Petite asso (15 membres)](#scenario-3-petite-asso-15-membres)
- [Backup &amp; Restauration](#backup-restauration)
  - [Stratégie de backup recommandée](#strategie-de-backup-recommandee)
  - [Restauration depuis backup](#restauration-depuis-backup)
- [Problèmes courants &amp; Solutions](#problemes-courants-solutions)
  - [❌ « Trusted domain error »](#%E2%9D%8C-trusted-domain-error)
  - [❌ Nextcloud lent / Timeouts](#%E2%9D%8C-nextcloud-lent-timeouts)
  - [❌ « 502 Bad Gateway » après restart](#%E2%9D%8C-502-bad-gateway-apres-restart)
  - [❌ Espace disque plein](#%E2%9D%8C-espace-disque-plein)
- [🎯 Nextcloud dans l’écosystème d’indépendance numérique](#%F0%9F%8E%AF-nextcloud-dans-lecosysteme-dindependance-numerique)
- [Pour aller plus loin](#maillage-interne-pour-aller-plus-loin)
- [Conclusion : Reprends le contrôle de tes données](#conclusion-reprends-le-controle-de-tes-donnees)


Avant de commencer : Choisir ton setup

### Option 1 : VPS Cloud (recommandé pour débuter)

**Pour qui ?** Tu débutes, tu veux que ça marche vite, et tu n’as pas de serveur à la maison.

**Recommandation VPS français** :

- **Hetzner Cloud CPX11** : 4,51€/mois HT → 2 vCPU, 2 Go RAM, 40 Go SSD, Allemagne
- **Scaleway DEV1-S** : 0,01€/h → 2 vCPU, 2 Go RAM, 20 Go SSD, Paris
- **OVHcloud VPS Starter** : 3,50€/mois HT → 1 vCPU, 2 Go RAM, 20 Go SSD, France

💡 **Pourquoi un VPS ?**

- Accès depuis n’importe où (pas besoin d’ouvrir ton routeur)
- IP fixe incluse
- Bande passante illimitée
- Backups automatiques disponibles

### Option 2 : Homelab (gratuit mais plus technique)

**Pour qui ?** Tu as déjà un Raspberry Pi 4/5, un vieux PC ou un mini PC chez toi.

**Avantages :**

- Coût quasi nul (électricité ~10€/an pour un Raspberry Pi)
- Stockage vraiment illimité (tu branches un disque externe)
- Contrôle total physique

**Inconvénients :**

- Configuration réseau plus complexe (DynDNS, port forwarding)
- Dépendant de ta connexion internet maison
- Pas d’accès si ton électricité saute

💡 **Mon conseil :** Commence sur VPS, migre sur homelab quand tu seras à l’aise.

- - - - - -

Installation Nextcloud avec Docker : La méthode propre

![Nextcloud Docker](7b962eb7-0c5e-4e5b-a5e6-1bc8861d75d6.png)### Étape 1 : Préparer le serveur

On part sur **Ubuntu 24.04 LTS** (ou 22.04, ça marche aussi).

```bash
# Mise à jour du système
sudo apt update && sudo apt upgrade -y

# Installation des dépendances
sudo apt install -y curl git nano

# Installation Docker (méthode officielle)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Ajouter ton utilisateur au groupe docker
sudo usermod -aG docker $USER
newgrp docker

# Vérification
docker --version
docker compose version
```

sudo apt install docker-compose-plugin

⚠️ **Erreur fréquente** : « Permission denied » → Tu as oublié `newgrp docker` ou tu n’as pas relancé ta session SSH.

- - - - - -

### Étape 2 : Créer la structure Docker Compose

On va créer un setup **Nextcloud + MariaDB + Nginx Proxy Manager** pour gérer facilement HTTPS.

```bash
# Créer le dossier projet
mkdir -p ~/nextcloud && cd ~/nextcloud

# Créer le docker-compose.yml
nano docker-compose.yml
```

services:
  # Base de données MariaDB
  db:
    image: mariadb:11.2
    container_name: nextcloud-db
    restart: unless-stopped
    command: --transaction-isolation=READ-COMMITTED --log-bin=binlog --binlog-format=ROW
    volumes:
      - ./db:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=ChangeMotDePasseSuperSecure123!
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud
      - MYSQL_PASSWORD=NextcloudPassword456!
    networks:
      - nextcloud-network

  # Redis pour améliorer les performances
  redis:
    image: redis:7.2-alpine
    container_name: nextcloud-redis
    restart: unless-stopped
    command: redis-server --requirepass RedisPassword789!
    networks:
      - nextcloud-network

  # Nextcloud
  nextcloud:
    image: nextcloud:28-apache
    container_name: nextcloud-app
    restart: unless-stopped
    ports:
      - "8080:80"
    volumes:
      - ./nextcloud:/var/www/html
      - ./data:/var/www/html/data
    environment:
      - MYSQL_HOST=db
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud
      - MYSQL_PASSWORD=NextcloudPassword456!
      - REDIS_HOST=redis
      - REDIS_HOST_PASSWORD=RedisPassword789!
      - NEXTCLOUD_TRUSTED_DOMAINS=ton-domaine.fr
      - OVERWRITEPROTOCOL=https
      - OVERWRITECLIURL=https://ton-domaine.fr
    depends_on:
      - db
      - redis
    networks:
      - nextcloud-network

  # Cron pour les tâches de maintenance
  cron:
    image: nextcloud:28-apache
    container_name: nextcloud-cron
    restart: unless-stopped
    volumes:
      - ./nextcloud:/var/www/html
      - ./data:/var/www/html/data
    entrypoint: /cron.sh
    depends_on:
      - db
      - redis
      - nextcloud
    networks:
      - nextcloud-network

networks:
  nextcloud-network:
    driver: bridge

volumes:
  db:
  nextcloud:
  data:

💡 **Explications ligne par ligne :**

- `mariadb:11.2` : Base de données performante (+ rapide que PostgreSQL pour Nextcloud)
- `redis` : Cache qui accélère drastiquement l’interface
- `nextcloud:28-apache` : Version 28 avec Apache intégré
- `OVERWRITEPROTOCOL=https` : Force HTTPS même derrière un reverse proxy
- `cron` : Container dédié qui exécute les tâches de maintenance toutes les 5 min

⚠️ **CHANGE LES MOTS DE PASSE !** Remplace tous les `ChangeMotDePasseSuperSecure`, `NextcloudPassword`, `RedisPassword` par TES mots de passe.

- - - - - -

### Étape 3 : Lancer Nextcloud

```bash
# Lancer tous les containers
docker compose up -d

# Vérifier que tout tourne
docker ps
```

# Voir les logs
docker compose logs -f nextcloud

# Erreur classique "Connection refused" = la DB n'est pas prête
# Solution : attends 30 secondes et recharge la page

# Erreur "Permission denied" dans les logs
sudo chown -R www-data:www-data ./nextcloud ./data

- - - - - -

### Étape 4 : Configuration HTTPS avec Nginx Proxy Manager

Pour exposer Nextcloud en HTTPS proprement, on va utiliser **Nginx Proxy Manager** (interface graphique hyper simple).

```bash
# Revenir dans le home
cd ~

# Créer dossier NPM
mkdir nginx-proxy-manager && cd nginx-proxy-manager

# Créer docker-compose.yml
nano docker-compose.yml
```

version: '3.8'

services:
  npm:
    image: 'jc21/nginx-proxy-manager:latest'
    container_name: nginx-proxy-manager
    restart: unless-stopped
    ports:
      - '80:80'    # HTTP
      - '443:443'  # HTTPS
      - '81:81'    # Interface admin
    volumes:
      - ./data:/data
      - ./letsencrypt:/etc/letsencrypt
    networks:
      - proxy-network

networks:
  proxy-network:
    external: true
    name: nextcloud_nextcloud-network

```bash
# Lancer NPM
docker compose up -d

# Créer le network partagé si erreur
docker network create nextcloud_nextcloud-network
docker compose up -d
```

# Headers de sécurité
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Robots-Tag "noindex, nofollow" always;
add_header Referrer-Policy "no-referrer" always;

# Headers pour Nextcloud
proxy_set_header X-Forwarded-Proto $scheme;
proxy_set_header X-Forwarded-Host $host;

# Configuration .well-known pour CalDAV/CardDAV
location = /.well-known/carddav {
    return 301 $scheme://$host/remote.php/dav;
}

location = /.well-known/caldav {
    return 301 $scheme://$host/remote.php/dav;
}

location = /.well-known/webfinger {
    return 301 $scheme://$host/index.php/.well-known/webfinger;
}

location = /.well-known/nodeinfo {
    return 301 $scheme://$host/index.php/.well-known/nodeinfo;
}

# Augmenter les timeouts pour les gros fichiers
client_max_body_size 10G;
client_body_timeout 300s;
fastcgi_buffers 64 4K;

Clique **Save** → Let’s Encrypt va automatiquement générer ton certificat HTTPS !

🎉 **Tu peux maintenant accéder à** `https://cloud.ton-domaine.fr`

- - - - - -

### Étape 5 : Configuration initiale Nextcloud

Ouvre `https://cloud.ton-domaine.fr` → Tu arrives sur l’assistant d’installation.

**Configuration recommandée :**

1. **Compte administrateur :**

- Utilisateur : `admin` (ou ton prénom)
- Mot de passe : **FORT** (générateur aléatoire recommandé)

1. **Stockage &amp; base de données :**

- Dossier des données : `/var/www/html/data` (déjà configuré)
- **Configurer la base de données** : MySQL/MariaDB
- Utilisateur BDD : `nextcloud`
- Mot de passe BDD : `NextcloudPassword456!` (celui du docker-compose)
- Nom BDD : `nextcloud`
- Hôte BDD : `db:3306`

1. **Applications recommandées :**

- ✅ Calendrier
- ✅ Contacts
- ✅ Notes
- ✅ Photos
- ⬜ Talk (visio – gourmand en ressources)

Clique **Terminer l’installation** → Ça prend 1-2 minutes.

- - - - - -

Optimisations post-installation (important !)

### Activer le cache Redis

Par défaut, Nextcloud ne sait pas qu’on a Redis. Il faut l’activer manuellement.

```bash
# Se connecter au container Nextcloud
docker exec -it nextcloud-app bash
# Éditer config.php
nano /var/www/html/config/config.php
```

  'memcache.local' => '\OC\Memcache\APCu',
  'memcache.distributed' => '\OC\Memcache\Redis',
  'memcache.locking' => '\OC\Memcache\Redis',
  'redis' => array(
    'host' => 'redis',
    'port' => 6379,
    'password' => 'RedisPassword789!',
  ),

Sauvegarde (Ctrl+O, Enter, Ctrl+X) et quitte le container (`exit`).

```bash
# Redémarrer Nextcloud
docker restart nextcloud-app
```

# Créer un fichier de config PHP custom
nano ~/nextcloud/nextcloud/uploads.ini

```bash
upload_max_filesize = 10G
post_max_size = 10G
max_execution_time = 3600
max_input_time = 3600
memory_limit = 512M
```

# Modifier le docker-compose pour monter ce fichier
cd ~/nextcloud
nano docker-compose.yml

Dans la section `nextcloud` → `volumes`, ajoute :

```bash
    volumes:
      - ./nextcloud:/var/www/html
      - ./data:/var/www/html/data
      - ./nextcloud/uploads.ini:/usr/local/etc/php/conf.d/uploads.ini
```

# Relancer
docker compose down
docker compose up -d

🎉 **Tu peux maintenant envoyer des fichiers jusqu’à 10 Go !**

- - - - - -

### Sécuriser avec fail2ban (optionnel mais recommandé)

Si ton Nextcloud est accessible publiquement, protège-le contre le bruteforce.

```bash
# Installation fail2ban
sudo apt install fail2ban -y

# Créer un filtre Nextcloud
sudo nano /etc/fail2ban/filter.d/nextcloud.conf
```

[Definition]
failregex = ^{"reqId":".*","level":2,"time":".*","remoteAddr":"<HOST>","user":".*","app":"core","method":".*","url":".*","message":"Login failed:
            ^{"reqId":".*","level":2,"time":".*","remoteAddr":"<HOST>","user":".*","app":"no app in context","method":".*","url":".*","message":"Login failed:
ignoreregex =

```bash
# Créer la jail
sudo nano /etc/fail2ban/jail.d/nextcloud.local
```

[nextcloud]
enabled = true
port = http,https
protocol = tcp
filter = nextcloud
maxretry = 5
bantime = 3600
findtime = 600
logpath = /home/ton-user/nextcloud/data/nextcloud.log

> Remplace `/home/ton-user/nextcloud/data/nextcloud.log` par le chemin réel.

```bash
# Redémarrer fail2ban
sudo systemctl restart fail2ban

# Vérifier le statut
sudo fail2ban-client status nextcloud
```

#!/bin/bash
# Script de backup Nextcloud
# À placer dans ~/backup-nextcloud.sh

BACKUP_DIR="/home/backups/nextcloud"
DATE=$(date +%Y-%m-%d_%H-%M)

# Créer dossier backup
mkdir -p $BACKUP_DIR

# Mettre Nextcloud en mode maintenance
docker exec nextcloud-app php occ maintenance:mode --on

# Backup base de données
docker exec nextcloud-db mysqldump -u nextcloud -pNextcloudPassword456! nextcloud > $BACKUP_DIR/nextcloud-db-$DATE.sql

# Backup fichiers (compression)
tar -czf $BACKUP_DIR/nextcloud-data-$DATE.tar.gz ~/nextcloud/data
tar -czf $BACKUP_DIR/nextcloud-config-$DATE.tar.gz ~/nextcloud/nextcloud/config

# Désactiver mode maintenance
docker exec nextcloud-app php occ maintenance:mode --off

# Garder seulement les 7 derniers backups
find $BACKUP_DIR -type f -mtime +7 -delete

echo "✅ Backup terminé : $DATE"

```bash
# Rendre exécutable
chmod +x ~/backup-nextcloud.sh

# Tester
./backup-nextcloud.sh

# Automatiser avec cron (tous les jours à 2h du matin)
crontab -e
```

0 2 * * * /home/ton-user/backup-nextcloud.sh >> /home/ton-user/backup.log 2>&1

**Méthode 2 : Backup vers cloud externe (paranoia niveau ++)**

```bash
# Installer rclone (sync vers S3, Backblaze, etc.)
curl https://rclone.org/install.sh | sudo bash

# Configurer une destination (exemple : Backblaze B2)
rclone config
# Suis l'assistant interactif

# Modifier le script de backup pour envoyer ailleurs
rclone sync /home/backups/nextcloud remote-b2:nextcloud-backups
```

# 1. Réinstaller Docker + Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 2. Recréer la structure
mkdir -p ~/nextcloud && cd ~/nextcloud

# 3. Copier le docker-compose.yml (tu l'as sauvegardé à part, hein ?)

# 4. Extraire les backups
tar -xzf nextcloud-data-XXXX.tar.gz -C ~/
tar -xzf nextcloud-config-XXXX.tar.gz -C ~/nextcloud/nextcloud/

# 5. Restaurer la base de données
docker compose up -d db  # Lancer juste la DB d'abord
sleep 10
docker exec -i nextcloud-db mysql -u nextcloud -pNextcloudPassword456! nextcloud < nextcloud-db-XXXX.sql

# 6. Lancer Nextcloud
docker compose up -d

# 7. Réparer les permissions si nécessaire
docker exec nextcloud-app chown -R www-data:www-data /var/www/html

🎉 **Tu as récupéré toutes tes données !**

- - - - - -

Problèmes courants &amp; Solutions

### ❌ « Trusted domain error »

**Symptôme :** Message d’erreur « Vous accédez au serveur depuis un domaine non approuvé ».

**Cause :** Nextcloud refuse les connexions depuis un domaine non configuré.

**Solution :**

```bash
docker exec -it nextcloud-app bash
nano /var/www/html/config/config.php
```

'trusted_domains' =>
array (
  0 => 'localhost',
  1 => 'ton-ip-serveur',
  2 => 'cloud.ton-domaine.fr',
),

- - - - - -

### ❌ Nextcloud lent / Timeouts

**Symptôme :** L’interface rame, les uploads échouent après 30 secondes.

**Causes possibles :**

1. Redis pas activé → Voir section « Optimisations »
2. VPS sous-dimensionné (&lt; 2 Go RAM)
3. PHP mal configuré

**Solution PHP :**

```bash
# Éditer la config
nano ~/nextcloud/nextcloud/uploads.ini
```

max_execution_time = 7200
max_input_time = 7200
memory_limit = 1G

```bash
docker compose restart nextcloud
```

# Attends 30-60 secondes (MariaDB est lente à démarrer)

# Si ça persiste, check les logs
docker compose logs -f nextcloud
docker compose logs -f db

Souvent c’est juste que la DB n’était pas prête. Relance :

```bash
docker compose restart nextcloud
```

# Vérifier l'espace
df -h

# Nettoyer les anciennes images Docker
docker system prune -a

# Nettoyer les versions de fichiers Nextcloud (garde 5 versions)
docker exec nextcloud-app php occ versions:cleanup

# Supprimer les fichiers en corbeille
docker exec nextcloud-app php occ trashbin:cleanup --all-users

# Dernière option : augmenter le VPS ou ajouter un volume

- - - - - -

🎯 Nextcloud dans l’écosystème d’indépendance numérique

Félicitations, tu viens de franchir un cap majeur : **remplacer Google Drive, Google Photos ET Google Docs** d’un seul coup. Mais soyons honnêtes, l’indépendance numérique ne s’arrête pas au stockage cloud.

Si tu veux vraiment te libérer des GAFAM, Nextcloud est **le premier pilier d’une stack complète** qui te fera économiser jusqu’à **534€/an** :

- ✅ **Nextcloud** → Remplace Google Drive/Photos/Docs (que tu viens d’installer)
- 🎬 **Jellyfin** → Remplace Netflix/Prime Video (économie : ~240€/an)
- 🔐 **Vaultwarden** → Remplace LastPass/1Password (économie : ~60€/an)

**Résultat ?** Une infrastructure 100% sous ton contrôle, sans abonnement récurrent, et qui peut tourner sur un simple Raspberry Pi 4.

👉 **[Découvre la stack complète d’indépendance numérique (guide pas à pas)](https://brandonvisca.com/independance-numerique-2025-guide-complet/)**

*Note : Si tu suis ce guide, tu auras une vision d’ensemble de l’architecture + les liens entre ces 3 services.*

- - - - - -

Pour aller plus loin

Si tu veux pousser ton setup plus loin, consulte ces guides complémentaires :

🔒 **[Sécuriser ton serveur Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/)** → Firewall, SSH, fail2ban, mises à jour automatiques

🐳 **[Docker pour débutants](https://brandonvisca.com/docker-debutant-services-auto-heberger/)** → Si tu veux mieux comprendre Docker et créer d’autres services

🌐 **[Nginx : Optimiser les headers HTTP](https://brandonvisca.com/securiser-nginx-avec-headers-http/)** → Pour renforcer la sécurité de ton reverse proxy

- - - - - -

Conclusion : Reprends le contrôle de tes données

Tu viens de mettre en place **ton propre cloud perso** en moins d’1h. Nextcloud avec Docker, c’est :

✅ Économique (58€/an vs 120€+ pour les clouds commerciaux)  
✅ Privé (tes données chez toi, pas chez Google/Microsoft)  
✅ Puissant (calendrier, contacts, notes, galerie, visio…)  
✅ Scalable (tu ajoutes de l’espace quand tu veux)

**Prochaines étapes suggérées :**

1. **Configurer les apps** : Calendrier, Contacts, Notes, Deck (kanban)
2. **Installer OnlyOffice** : Éditer des documents Word/Excel directement dans Nextcloud
3. **Activer 2FA** : Paramètres → Sécurité → Authentification à deux facteurs
4. **Partager avec tes proches** : Créer des comptes pour ta famille
5. **Automatiser les backups** : Utilise le script fourni + cron

Et surtout, dis adieu aux 10-20€/mois de Google Drive. 🎉

💬 **Questions, galères, ou réussites ?** Balance tout en commentaire, je réponds à tout le monde !
