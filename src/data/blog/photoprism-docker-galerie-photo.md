---
title: "PhotoPrism Docker : la galerie photo auto-hébergée qui remplace Google Photos"
description: "Guide PhotoPrism Docker complet. Installe PhotoPrism avec Docker pour une galerie photo auto-hébergée avec reconnaissance IA. Alternative à Google Photos."
pubDatetime: "2026-06-10T08:00:00.000Z"
modDatetime: "2026-06-10T08:00:00.000Z"
author: Brandon Visca
focusKeyword: photoprism docker
tags:
  - auto-hebergement
  - docker
  - photoprism
  - intermediaire
  - guide
featured: false
draft: false
faqs:
  - question: "Quelle RAM est nécessaire pour PhotoPrism Docker ?"
    answer: "PhotoPrism nécessite 2 Go de RAM minimum pour une petite collection. 4 Go sont recommandés pour activer la reconnaissance faciale par IA et indexer plus de 10 000 photos."
  - question: "PhotoPrism ou Immich, lequel choisir ?"
    answer: "PhotoPrism est plus mature et stable depuis 5 ans. Immich est plus moderne mais évolue vite avec des changements fréquents de base de données. Choisis PhotoPrism pour la fiabilité, Immich si tu veux les dernières features."
  - question: "Peut-on importer ses photos Google Photos dans PhotoPrism ?"
    answer: "Oui, exporte tes photos avec Google Takeout, décompresse l'archive, et copie les fichiers dans le dossier originals ou import de PhotoPrism. L'indexation extraira les métadonnées EXIF et GPS."
  - question: "PhotoPrism fonctionne-t-il sur Raspberry Pi ?"
    answer: "Oui, l'image ARM64 est disponible. L'indexation IA sera plus lente que sur x86_64. Prévois un Pi 4 avec 4 Go de RAM minimum et un stockage externe rapide."
---
> 💡 **TL;DR** — PhotoPrism Docker en 4 points :
>
> - **C'est quoi ?** Une galerie photo auto-hébergée avec reconnaissance faciale, classification par IA et import automatique
> - **Pourquoi ?** Google Photos te facture 2 To à 10€/mois, piste tes métadonnées GPS et te bloque si tu dépasses les quotas
> - **Comment ?** Un `docker-compose.yml` avec PhotoPrism + MariaDB = opérationnel en 10 minutes
> - **Coût ?** Zéro euro si tu as déjà un serveur avec Docker

Tu stockes encore tes 15 000 photos sur Google Photos ? Tu reçois ce gentil mail "Vous avez utilisé 95% de votre espace" ? Et quand tu cherches "chat noir" dans ta galerie, Google te sort un algorithme flippant qui te dit exactement où tu étais quand tu l'as pris ?

Bienvenue dans le monde merveilleux du cloud propriétaire. Tu paies pour stocker, tu paies pour chercher, et en prime tu nourris un modèle d'IA avec tes souvenirs de vacances.

Il existe une alternative solide : **PhotoPrism**. C'est une galerie photo open-source, auto-hébergée, avec reconnaissance faciale, classification automatique par IA, et zero tracking. On l'installe avec Docker Compose en 10 minutes, et tes photos restent chez toi. Pour toujours.

Si tu débutes avec Docker, commence par mon [guide Docker pour débutants](/docker-debutant-services-auto-heberger/) pour bien poser les bases. Et si tu cherches déjà à stocker tes fichiers en cloud perso, mon guide [Nextcloud Docker](/nextcloud-docker-installation-complete-2025/) est complémentaire.

## Table des matières

## Pourquoi quitter Google Photos en 2026 ?

Google Photos était génial à ses débuts. Stockage gratuit, recherche par contenu, synchronisation multi-appareil. Puis Google a retiré le stockage gratuit illimité en juin 2021. Depuis, c'est la galère.

### Le calcul qui fait mal

**Google Photos aujourd'hui :**

- 100 Go : 2€/mois = 24€/an
- 2 To : 10€/mois = 120€/an
- 5 To : 25€/mois = 300€/an

Et ce n'est que le stockage. Tu payes aussi avec tes données : localisation GPS, reconnaissance faciale, analyse EXIF, tout est miné pour l'IA générative.

**PhotoPrism auto-hébergé :**

- VPS 4 Go RAM : 6€/mois = 72€/an
- Disque 2 To : déjà inclus sur ton serveur ou NAS
- **Total : 72€/an pour stockage illimité et zero tracking**

Si tu as déjà un serveur chez toi (Raspberry Pi 4/5, vieux PC, NAS Synology), c'est **quasi gratuit** à part l'électricité.

### Ce que PhotoPrism fait aussi bien que Google

- **Recherche par contenu** : tape "plage", "chat", "voiture rouge" — ça marche
- **Reconnaissance faciale** : regroupe les portraits par personne automatiquement
- **Import automatique** : dossier surveillé, les photos sont indexées dès l'arrivée
- **Albums partagés** : liens publics ou privés avec expiration
- **Carte géographique** : visualise tes photos sur une carte OpenStreetMap
- **RAW et vidéos** : support natif des formats Canon CR3, Nikon NEF, Sony ARW, HEVC
- **Pas de tracking** : zero appel vers Google, zéro analyse externe

### Ce que Google fait mieux (restons honnêtes)

- **Apps mobiles** : Google Photos iOS/Android est plus fluide que l'app web PhotoPrism
- **Stockage infini compressé** : Google propose du "stockage économique" qui compresse les photos. PhotoPrism stocke en qualité originale uniquement
- **Partage familial** : Google gère mieux les albums multi-utilisateurs avec permissions fines

Mais pour la majorité des usages personnels, PhotoPrism couvre 90% des besoins sans vendre ton âme.

## PhotoPrism vs Google Photos vs Immich vs LibrePhotos

| Critère | PhotoPrism | Google Photos | Immich | LibrePhotos |
|---------|-----------|---------------|--------|-------------|
| **Auto-hébergé** | Oui | Non (SaaS) | Oui | Oui |
| **Prix** | Gratuit | 2-25€/mois | Gratuit | Gratuit |
| **Licence** | AGPL v3 | Propriétaire | AGPL v3 | AGPL v3 |
| **Reconnaissance faciale** | Oui (IA locale) | Oui (cloud) | Oui (IA locale) | Oui (IA locale) |
| **Recherche sémantique** | Oui | Oui (puissante) | Oui | Limitée |
| **Import auto** | Oui (dossier surveillé) | Oui (sync) | Oui | Oui |
| **RAW support** | Oui (Darktable/RawTherapee) | Non | Oui | Oui |
| **Vidéos HEVC** | Oui (FFmpeg) | Oui | Oui | Oui |
| **Map/Geo** | OpenStreetMap | Google Maps | OpenStreetMap | OpenStreetMap |
| **App mobile** | Web PWA | Native excellente | Native (beta) | Web PWA |
| **Multi-utilisateur** | Oui | Oui | Oui | Oui |
| **Partage externe** | Liens sécurisés | Liens + albums | Liens | Liens |
| **Ressources RAM** | 2-4 Go | N/A (cloud) | 2-4 Go | 2 Go |
| **Facilité install** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

**Mon choix** : PhotoPrism pour la maturité du projet (5+ ans), la stabilité, et l'interface soignée. Immich est excellent mais encore très en mouvement — l'API et la base de données changent régulièrement. Si tu veux quelque chose qui tourne sans y toucher pendant 6 mois, PhotoPrism est plus sage.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose installés (voir mon [guide Docker débutant](/docker-debutant-services-auto-heberger/))
- **RAM minimum** : 2 Go pour une petite collection (< 10 000 photos). 4 Go recommandé
- **CPU** : x86_64 recommandé. ARM64 fonctionne (Raspberry Pi 4/5) mais l'indexation IA est plus lente
- **Stockage** : SSD recommandé pour la base de données. Les photos peuvent être sur un disque mécanique ou NAS
- Un reverse proxy type Caddy, Nginx Proxy Manager ou Traefik (pour HTTPS)
- Un sous-domaine type `photos.tondomaine.fr` (optionnel mais conseillé)

## Installation de PhotoPrism avec Docker Compose

On part sur une stack complète **photoprism docker** : PhotoPrism + MariaDB. SQLite fonctionne pour les petites collections, mais MariaDB est recommandé dès que tu dépasses 5 000 photos.

Crée un dossier dédié :

```bash
mkdir -p ~/photoprism && cd ~/photoprism
```

Crée le fichier `docker-compose.yml` :

```yaml
services:
  photoprism:
    image: photoprism/photoprism:260601
    container_name: photoprism
    restart: unless-stopped
    stop_grace_period: 10s
    security_opt:
      - seccomp:unconfined
      - apparmor:unconfined
    ports:
      - "2342:2342"
    environment:
      PHOTOPRISM_ADMIN_USER: "admin"
      PHOTOPRISM_ADMIN_PASSWORD: "TON_MOT_DE_PASSE_FORT"
      PHOTOPRISM_AUTH_MODE: "password"
      PHOTOPRISM_SITE_URL: "https://photos.tondomaine.fr"
      PHOTOPRISM_SITE_TITLE: "Ma Galerie"
      PHOTOPRISM_SITE_CAPTION: "Photos"
      PHOTOPRISM_SITE_DESCRIPTION: ""
      PHOTOPRISM_SITE_AUTHOR: "Ton Nom"
      PHOTOPRISM_FOLDERS_PATH: "/photoprism/originals"
      PHOTOPRISM_STORAGE_PATH: "/photoprism/storage"
      PHOTOPRISM_ORIGINALS_PATH: "/photoprism/originals"
      PHOTOPRISM_IMPORT_PATH: "/photoprism/import"
      PHOTOPRISM_DATABASE_DRIVER: "mysql"
      PHOTOPRISM_DATABASE_SERVER: "mariadb:3306"
      PHOTOPRISM_DATABASE_NAME: "photoprism"
      PHOTOPRISM_DATABASE_USER: "photoprism"
      PHOTOPRISM_DATABASE_PASSWORD: "MOT_DE_PASSE_MARIADB"
      PHOTOPRISM_FFMPEG_ENCODER: "intel"       # Change par "nvidia" ou "software" si besoin
      PHOTOPRISM_FFMPEG_BITRATE: "32"
      PHOTOPRISM_INIT: "gpu tensorflow"
      PHOTOPRISM_UID: 1000
      PHOTOPRISM_GID: 1000
      PHOTOPRISM_UMASK: "0002"
    working_dir: "/photoprism"
    volumes:
      - "./storage:/photoprism/storage"
      - "/chemin/vers/tes/photos:/photoprism/originals"
      - "./import:/photoprism/import"
      - "/etc/localtime:/etc/localtime:ro"
    devices:
      - "/dev/dri:/dev/dri"                     # Intel QSV / VA-API
      # - "/dev/nvidia0:/dev/nvidia0"           # Décommente pour NVIDIA
      # - "/dev/nvidiactl:/dev/nvidiactl"
      # - "/dev/nvidia-modeset:/dev/nvidia-modeset"
      # - "/dev/nvidia-uvm:/dev/nvidia-uvm"
      # - "/dev/nvidia-uvm-tools:/dev/nvidia-uvm-tools"
    depends_on:
      - mariadb
    networks:
      - photoprism-net

  mariadb:
    image: mariadb:10.11
    container_name: photoprism_mariadb
    restart: unless-stopped
    stop_grace_period: 5s
    security_opt:
      - seccomp:unconfined
      - apparmor:unconfined
    command: >
      mysqld
      --innodb-buffer-pool-size=512M
      --transaction-isolation=READ-COMMITTED
      --character-set-server=utf8mb4
      --collation-server=utf8mb4_unicode_ci
      --max-connections=512
      --innodb-rollback-on-timeout=OFF
      --innodb-lock-wait-timeout=120
    volumes:
      - "./database:/var/lib/mysql"
    environment:
      MARIADB_DATABASE: "photoprism"
      MARIADB_USER: "photoprism"
      MARIADB_PASSWORD: "MOT_DE_PASSE_MARIADB"
      MARIADB_ROOT_PASSWORD: "ROOT_PASSWORD_MARIADB"
    networks:
      - photoprism-net

  ## Optionnel : proxy inverse Caddy pour HTTPS
  # caddy:
  #   image: caddy:2
  #   container_name: photoprism_caddy
  #   restart: unless-stopped
  #   ports:
  #     - "80:80"
  #     - "443:443"
  #   volumes:
  #     - ./Caddyfile:/etc/caddy/Caddyfile
  #     - caddy_data:/data
  #     - caddy_config:/config
  #   networks:
  #     - photoprism-net

networks:
  photoprism-net:
    driver: bridge
```

⚠️ **Remplace les valeurs avant de lancer :**

- `TON_MOT_DE_PASSE_FORT` : mot de passe admin PhotoPrism
- `MOT_DE_PASSE_MARIADB` : mot de passe base de données (identique aux deux endroits)
- `ROOT_PASSWORD_MARIADB` : mot de passe root MariaDB
- `/chemin/vers/tes/photos` : le chemin absolu vers ton dossier photos existant
- `photos.tondomaine.fr` : ton sous-domaine

Lance la stack :

```bash
docker compose up -d
```

Attends 30 secondes que MariaDB démarre, puis accède à `http://IP_DU_SERVEUR:2342`. Connecte-toi avec `admin` et ton mot de passe.

## Configuration initiale

### Premier indexage

Quand tu te connectes pour la première fois, PhotoPrism te demande d'indexer tes photos. Clique sur "Library" puis "Start" dans la section Index. Selon le nombre de photos, ça prend entre 5 minutes et 2 heures.

PhotoPrism va :

- Extraire les métadonnées EXIF (date, GPS, appareil photo)
- Générer des vignettes (thumbnails)
- Lancer la reconnaissance faciale
- Classer automatiquement par catégories (nature, architecture, personnes, animaux...)

### Paramètres essentiels à modifier

Dans "Settings" :

- **Library** : active "Auto Import" si tu veux que le dossier `/import` soit surveillé
- **Advanced** : ajuste la qualité des JPEG générés (par défaut 85%, tu peux monter à 95%)
- **Services** : configure un compte OpenStreetMap pour la carte (optionnel)
- **Account** : change le mot de passe admin et active l'authentification à deux facteurs

### Performance et indexation IA

La première indexation est gourmande. Si tu as un Intel récent avec iGPU, l'accélération matérielle QSV accélère énormément la génération des vignettes et la reconnaissance faciale.

Si tu vois des erreurs `tensorflow` dans les logs, vérifie que le dossier `storage` a les bonnes permissions :

```bash
docker compose exec photoprism chmod -R 755 /photoprism/storage
```

## Organisation des photos et workflows

### Originals vs Import

PhotoPrism gère deux modes :

1. **Originals** (`/photoprism/originals`) : tes photos existantes, PhotoPrism les lit sans les toucher. C'est le mode recommandé si tu as déjà une arborescence organisée.
2. **Import** (`/photoprism/import`) : dossier temporaire où tu jettes les photos depuis ton téléphone. PhotoPrism les déplace automatiquement dans `originals` en les renommant et triant par date.

Mon workflow perso :

- Je monte mon NAS dans `originals` (read-only si je veux être sûr)
- Je configure une sync SFTP/Syncthing vers le dossier `import` depuis mon téléphone
- PhotoPrism importe et range tout seul

### Albums, favoris et labels

Une fois indexé, tu peux :

- Créer des **albums** manuels (vacances, famille, projet)
- Marquer des photos en **favoris** (étoile)
- Filtrer par **labels IA** (chat, plage, forêt...)
- Visualiser sur la **carte** si les photos ont des données GPS
- Rechercher par **visage** dans l'onglet People

La recherche texte fonctionne en anglais par défaut. Tape "beach" plutôt que "plage" pour de meilleurs résultats.

## Sauvegarde de ta galerie

PhotoPrism ne sauvegarde pas tes photos — il les affiche. Si ton disque crashe, tes photos disparaissent. **Tu dois avoir une stratégie de backup.**

Mon setup recommandé :

- **Photos originales** : backup avec rclone vers un cloud chiffré (Backblaze B2, Wasabi) ou un second NAS
- **Base de données** : dump automatique avec `mysqldump` ou [Duplicati](/duplicati-docker-sauvegarde/)
- **Storage PhotoPrism** : backup du dossier `./storage` (cache, index, thumbnails)

Si tu utilises déjà Duplicati, j'ai un guide complet pour le [déployer en Docker](/duplicati-docker-sauvegarde/). Ajoute simplement trois sources à ta tâche de backup :

1. Le dossier de tes photos originales
2. Le dossier `database/` de MariaDB (ou un dump SQL quotidien)
3. Le dossier `storage/` de PhotoPrism

## Sécurisation de l'accès

PhotoPrism expose une interface web. Ne la laisse jamais ouverte sur Internet sans HTTPS et sans authentification.

### Checklist sécurité

- [ ] **HTTPS forcé** : utilise Caddy, Nginx Proxy Manager ou Traefik avec Let's Encrypt
- [ ] **Mot de passe fort** : minimum 16 caractères, pas dans le docker-compose en clair si possible (utilise un fichier `.env`)
- [ ] **Authentification 2FA** : active dans Settings > Account
- [ ] **Fail2Ban** : protège le port 2342 des bruteforce. Voir mon guide [hardening Linux](/hardening-linux-10-commandes/)
- [ ] **VPN/Tailscale** : si tu n'as pas besoin d'accès depuis n'importe où, restreins via VPN
- [ ] **Firewall** : ouvre uniquement le port 443 (HTTPS), pas le 2342 en direct

Pour isoler PhotoPrism dans un `.env` :

```bash
# .env
PHOTOPRISM_ADMIN_PASSWORD="super_mot_de_passe_secure_1234"
```

Puis remplace les valeurs en dur dans le `docker-compose.yml` par `${PHOTOPRISM_ADMIN_PASSWORD}`.

## Dépannage courant

### L'indexation bloque ou est très lente

Vérifie les ressources RAM. PhotoPrism avec TensorFlow pour la reconnaissance faciale consomme 1.5-2.5 Go de RAM. Si tu as moins, désactive l'IA dans Settings > Advanced > Disable TensorFlow.

### Les photos n'apparaissent pas après import

PhotoPrism indexe par défaut uniquement les formats supportés. Vérifie que tes fichiers ne sont pas dans un sous-dossier ignoré (nom commençant par `.` ou `@`). Force un nouvel indexage avec "Complete Rescan" dans Library.

### Erreur de connexion à MariaDB

Les logs disent "connection refused" ? MariaDB met 20-30 secondes à démarrer la première fois. Attends un peu et relance PhotoPrism :

```bash
docker compose restart photoprism
```

### Les thumbnails ne se génèrent pas

Vérifie l'espace disque dans `./storage`. PhotoPrism génère plusieurs tailles de thumbnails (XS à XL). Pour 10 000 photos, prévois 5-10 Go de cache thumbnails.

## Conclusion

PhotoPrism n'est pas Google Photos. L'app mobile n'est pas aussi fluide, le partage familial est moins poussé, et tu dois gérer toi-même le serveur et les backups.

Mais pour tout le reste ? C'est une bête. Reconnaissance faciale locale, recherche sémantique, cartographie GPS, support RAW, zero tracking, zero abonnement. Tes photos restent tes photos.

Si tu as déjà un serveur Docker qui tourne pour [Nextcloud](/nextcloud-docker-installation-complete-2025/) ou [Miniflux](/miniflux-docker-lecteur-rss-guide/), ajouter PhotoPrism prend 10 minutes. Le coût marginal est quasi nul, et le gain en indépendance numérique est énorme.

Installe-le, indexe tes photos, et redécouvre des souvenirs que tu avais oubliés. Sans algorithme qui décide ce que tu dois voir.