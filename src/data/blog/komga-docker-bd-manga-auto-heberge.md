---
title: "Komga Docker : serveur de BD/manga auto-hébergé"
description: "Guide komga docker : déploie Komga, serveur BD/manga auto-hébergé MIT. Docker Compose, config et comparatif inclus."
pubDatetime: "2026-06-16T08:00:00.000Z"
modDatetime: "2026-06-16T08:00:00.000Z"
author: Brandon
tags:
  - docker
  - auto-hebergement
  - intermediaire
  - komga
  - manga
  - medias
featured: false
draft: false
focusKeyword: "komga docker"
ogImage: ""
faqs:
  - question: "Komga supporte-t-il les mangas japonais en lecture de droite à gauche ?"
    answer: "Oui, Komga propose un mode manga natif qui inverse la direction de lecture (right-to-left) avec défilement continu optimisé pour ce format."
  - question: "Puis-je synchroniser Komga avec ma liseuse Kobo ?"
    answer: "Oui, Komga intègre le Kobo Sync et le KOReader Sync, ce qui permet de télécharger des tomes et synchroniser la progression de lecture directement depuis la liseuse."
  - question: "Komga nécessite-t-il une base de données externe ?"
    answer: "Non, Komga utilise SQLite intégrée. Toutes les données sont stockées dans le volume /config du conteneur Docker, sans dépendance externe."
  - question: "Quelle est la différence entre Komga et Kavita ?"
    answer: "Komga est optimisé pour les comics et mangas (CBZ/CBR) avec mode RTL et Kobo Sync. Kavita est plus polyvalent pour les ebooks longs (EPUB, PDF techniques). Les deux peuvent coexister."
---
> 💡 **TL;DR**
> - Komga est un serveur de BD, manga et comics auto-hébergé, open-source sous licence MIT avec plus de 6 300 stars sur GitHub
> - Il lit CBZ, CBR, PDF et EPUB avec une interface web moderne, collections, séries et métadonnées
> - Déploiement Docker en 5 minutes, ressources ultra-légères (512 Mo RAM), compatible Raspberry Pi
> - Docker Compose complet, comparatif avec Calibre-Web, Kavita et Plex Comics, ainsi que la config OPDS et multi-utilisateurs ci-dessous

## Pourquoi un serveur de BD et manga auto-hébergé ?

T'as des Go de comics, mangas et bandes dessinées stockés sur un NAS, un disque dur externe ou un vieux serveur. Les retrouver demande de parcourir des dossiers imbriqués à dix niveaux de profondeur avec des noms comme `One_Piece_v87_[FR]_VIZ_DIGITAL.cbz`. Quand tu veux reprendre une série au tome 43, tu perds 10 minutes à vérifier quel fichier tu avais ouvert la dernière fois.

Les solutions commerciales existent mais posent problème. Plex a un module comics, mais il est limité, payant via Plex Pass, et tes métadonnées partent chez eux. Les lecteurs locaux type ComicRack ou Calibre Desktop sont puissants mais datés, non multi-utilisateurs, et inaccessibles depuis ton téléphone ou ta tablette.

Tu veux un serveur qui :
- indexe tes archives CBZ/CBR et tes PDFs automatiquement,
- présente tes séries avec couvertures, métadonnées et ordre chronologique,
- te permette de reprendre ta lecture exactement où tu t'étais arrêté,
- soit accessible depuis n'importe quel appareil avec un navigateur,
- supporte les comptes multiples pour partager avec ta famille,
- reste 100 % sur ton infrastructure, sans abonnement ni télémétrie.

Komga est la réponse. Développé en Kotlin avec Spring Boot par un passionné de manga, il est rapide, stable, et conçu spécifiquement pour les collections de bandes dessinées. Si tu cherches à compléter ton homelab média à côté de ton [serveur Kavita pour les ebooks](/kavita-docker-lecteur-ebooks/) ou de ton [Jellyfin pour films et séries](/jellyfin-docker-alternative-netflix-gratuite/), Komga est le chaînon manquant.

## Qu'est-ce que Komga exactement ?

Komga n'est pas un simple explorateur de fichiers. C'est un serveur de lecture complet avec une interface web moderne, pensée pour la consommation de comics et manga.

Voici ce qu'il propose concrètement :

- **Formats natifs** : CBZ, CBR, PDF et EPUB. Pas de conversion nécessaire, Komga lit directement les archives ZIP/RAR et les fichiers PDF source. Les images à l'intérieur des archives sont affichées à la volée.
- **Organisation par séries et collections** : Komga scanne tes dossiers et détecte automatiquement les séries, tomes, chapitres et one-shots. Tu peux créer des collections thématiques ("Shonen", "Seinen", "BD franco-belge", "Marvel") pour grouper des séries de différents dossiers.
- **Métadonnées et couvertures** : extraction automatique des couvertures depuis les archives, lecture des fichiers `ComicInfo.xml` (format standard), support des métadonnées via l'API REST ou l'interface web.
- **Lecture web responsive** : interface adaptée au desktop, tablette et mobile. Lecture paginée ou en défilement continu, mode manga (de droite à gauche), zoom, rotation, mode nuit et plein écran.
- **Reprise de lecture** : ta position de lecture est sauvegardée par utilisateur. Tu peux reprendre exactement à la page où tu t'étais arrêté depuis n'importe quel appareil.
- **Multi-utilisateurs** : crée des comptes pour chaque membre de ta famille avec des permissions granulaires par bibliothèque. L'un peut accéder aux mangas, l'autre aux comics Marvel uniquement.
- **OPDS** : flux OPDS standard compatible avec les lecteurs externes sur iOS (Chunky, Panels) et Android (Moon Reader, Librera).
- **Kobo Sync et KOReader Sync** : synchronisation de la progression de lecture avec les liseuses Kobo et l'application KOReader, un avantage unique face aux concurrents.
- **API REST** : documentation Swagger incluse, permettant d'automatiser l'ajout de métadonnées, la gestion des bibliothèques ou l'intégration avec d'autres outils.
- **Lecture hors ligne** : téléchargement d'un tome ou d'un chapitre complet depuis l'interface web pour lecture sans connexion.
- **Analyse des archives** : vérification automatique de l'intégrité des fichiers CBZ/CBR, détection des archives corrompues.
- **Import automatique** : scan périodique des dossiers surveillés pour détecter les nouveaux fichiers et les indexer automatiquement.

Le projet est open-source sous licence MIT, maintenu activement sur le repo `gotson/komga`. L'image Docker officielle `gotson/komga` est publiée sur Docker Hub avec support amd64, arm64 et armv7. Si tu débutes avec Docker, commence par mon guide sur [les services essentiels à auto-héberger](/docker-debutant-services-auto-heberger/) pour bien structurer ton environnement avant d'ajouter Komga.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose installés (Docker Engine 24+ recommandé)
- 1 cœur CPU et 512 Mo de RAM minimum (1 Go recommandé pour les grosses collections)
- 1 Go d'espace disque pour l'application, plus l'espace de ta collection
- Un nom de domaine ou sous-domaine si tu veux HTTPS en frontal
- Un reverse proxy (Caddy, Traefik ou Nginx Proxy Manager) pour gérer les certificats SSL

Komga est incroyablement léger. Un Raspberry Pi 4 avec 2 Go de RAM suffit pour servir plusieurs milliers de tomes à plusieurs utilisateurs simultanés. Pour un usage confortable avec de gros PDF, un petit VPS de 1 cœur / 2 Go est amplement suffisant.

## Déploiement Komga avec Docker Compose

Crée un dossier dédié et un fichier `docker-compose.yml` :

```bash
mkdir -p ~/komga && cd ~/komga
```

Voici le Docker Compose complet et prêt à l'emploi :

```yaml
version: "3.8"

services:
  komga:
    image: gotson/komga:latest
    container_name: komga
    restart: unless-stopped
    ports:
      - "25600:25600"
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Paris
      - KOMGA_LIBRARIES_SCAN_CRON=0 0 * * * *
      - KOMGA_LIBRARIES_SCAN_STARTUP=true
      - KOMGA_REMEMBERME_KEY=${KOMGA_REMEMBERME_KEY:-change-me-in-production}
    volumes:
      - ./config:/config
      - /chemin/vers/ta/collection:/data
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:25600/actuator/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

**Points clés de cette configuration :**

- `PUID=1000` et `PGID=1000` : adapte à l'UID/GID de ton utilisateur Linux (`id` pour vérifier)
- `KOMGA_LIBRARIES_SCAN_CRON` : scan automatique des bibliothèques toutes les heures. Syntaxe cron standard. Mets `0 0 */6 * * *` pour un scan toutes les 6 heures si ta collection est très grande.
- `KOMGA_LIBRARIES_SCAN_STARTUP=true` : scan au démarrage du conteneur pour rattraper les fichiers ajoutés pendant l'arrêt
- `/chemin/vers/ta/collection` : remplace par le chemin absolu de ton dossier contenant les BD/mangas. Komga scanne les sous-dossiers récursivement.
- `./config` : dossier local où Komga stocke sa base SQLite, les miniatures et les paramètres
- Le `healthcheck` vérifie que l'API actuator répond, ce qui garantit que l'application est vraiment prête

Lance le conteneur :

```bash
docker compose up -d
```

Accède à l'interface via `http://<ip-du-serveur>:25600`. Au premier démarrage, Komga te demande de créer un compte administrateur.

## Configuration initiale

Après le premier lancement, voici les étapes essentielles :

1. **Crée ton compte admin** via l'assistant web affiché au premier accès
2. **Ajoute une bibliothèque** : `Administration` → `Libraries` → `Add library`. Choisis le dossier `/data` (ou un sous-dossier), nomme ta bibliothèque (ex: "Mangas"), puis sauvegarde.
3. **Lance le scan** : Komga scanne automatiquement les fichiers. Selon la taille de la collection, cela peut prendre de quelques secondes à plusieurs minutes.
4. **Vérifie les séries détectées** : Komga lit les métadonnées des fichiers `ComicInfo.xml` s'ils sont présents dans les archives. Sans ce fichier, il déduit le titre et le numéro de tome depuis le nom du fichier.

### Améliorer les métadonnées avec ComicInfo.xml

Pour des résultats optimaux, place un fichier `ComicInfo.xml` à la racine de chaque archive CBZ/CBR. Voici un exemple minimal :

```xml
<?xml version="1.0"?>
<ComicInfo>
  <Series>One Piece</Series>
  <Number>87</Number>
  <Title>Le Royaume de Wano</Title>
  <Summary>Luffy et ses alliés...</Summary>
  <Year>2021</Year>
  <Month>4</Month>
  <Writer>Eiichiro Oda</Writer>
  <Publisher>Glénat</Publisher>
  <Genre>Shonen</Genre>
  <PageCount>192</PageCount>
</ComicInfo>
```

Des outils comme Komga Companion, Mylar3 ou ComicTagger peuvent générer automatiquement ces fichiers depuis des bases comme ComicVine.

## Reverse proxy et HTTPS

Komga n'a pas besoin de configuration spéciale derrière un reverse proxy. Voici un exemple avec Caddy :

```
komga.exemple.com {
    reverse_proxy localhost:25600
}
```

Avec Traefik et labels Docker Compose :

```yaml
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.komga.rule=Host(\`komga.exemple.com\`)"
      - "traefik.http.routers.komga.tls=true"
      - "traefik.http.routers.komga.tls.certresolver=letsencrypt"
      - "traefik.http.services.komga.loadbalancer.server.port=25600"
```

Avec Nginx Proxy Manager, crée simplement un proxy host pointant vers `http://komga:25600` (si sur le même réseau Docker) ou `http://<ip>:25600`.

## Sauvegarde

Komga stocke toutes ses données dans le volume `/config`. Pour sauvegarder, il suffit de copier ce dossier :

```bash
tar czvf komga-backup-$(date +%Y%m%d).tar.gz ~/komga/config
```

Et pour restaurer :

```bash
tar xzvf komga-backup-20260115.tar.gz -C ~/
```

Les fichiers média (`/data`) restent inchangés : pas besoin de les sauvegarder avec Komga si tu les as déjà dans ta stratégie de backup globale. Si tu veux une solution de backup complète pour tes conteneurs, j'ai détaillé [Duplicati avec Docker](/duplicati-docker-sauvegarde/) dans un guide dédié.

## Komga vs les alternatives : le tableau comparatif

| Critère | Komga | Calibre-Web | Kavita | Plex Comics |
|---------|-------|-------------|--------|-------------|
| **Licence** | MIT | GPL-3.0 | GPL-3.0 | Propriétaire |
| **Formats** | CBZ, CBR, PDF, EPUB | EPUB, PDF, CBZ (limité) | EPUB, PDF, CBZ, CBR, images | CBZ, CBR, PDF |
| **Interface** | Moderne, manga-first | Datée, fonctionnelle | Moderne, ebook-first | Intégrée à Plex |
| **Mode manga** | RTL natif, défilement continu | Non | RTL via paramètre | Non |
| **Collections** | Oui, personnalisables | Oui (tags/lists) | Oui (collections) | Limité |
| **Multi-utilisateurs** | Oui, par bibliothèque | Oui, basique | Oui, avancé | Oui, Plex Pass |
| **OPDS** | Oui | Oui | Oui | Non |
| **Kobo Sync** | Oui | Non | Non | Non |
| **KOReader Sync** | Oui | Non | Non | Non |
| **Ressources RAM** | 512 Mo | 256 Mo | 512 Mo | 1 Go+ |
| **Base de données** | SQLite intégrée | SQLite (via Calibre) | SQLite intégrée | Propriétaire |
| **Prix** | Gratuit | Gratuit | Gratuit | Plex Pass obligatoire |
| **Télémétrie** | Aucune | Aucune | Aucune | Oui (Plex) |

**Verdict :**

- **Tu lis principalement manga et comics en CBZ/CBR** → **Komga** ✅ C'est le meilleur lecteur web pour cette cible, avec le mode RTL et le défilement continu.
- **Tu veux aussi gérer des ebooks EPUB et PDF techniques** → **Kavita** ✅ Plus polyvalent pour les formats longs, liseuse ebook et la documentation. Les deux peuvent coexister sur le même serveur sans problème.
- **Tu as déjà une base Calibre et tu veux un accès web simple** → **Calibre-Web** ✅ Migration transparente, mais l'expérience lecture est inférieure.
- **Tu es déjà dans l'écosystème Plex et tu veux tout centralisé** → **Plex Comics** ⚠️ Payant, limité, mais pratique si tu refuses d'héberger un second service.

**Mon usage perso** : Komga pour les mangas et comics, Kavita côte à côte pour les romans et documentation technique EPUB. Les deux tournent sur le même VPS de 2 Go de RAM sans aucune tension.

## Astuces et configuration avancée

### Organiser tes dossiers pour Komga

Komga détecte les séries via l'arborescence. Voici la structure recommandée :

```
/data
├── Mangas
│   ├── One Piece
│   │   ├── One Piece - Tome 01.cbz
│   │   ├── One Piece - Tome 02.cbz
│   │   └── ...
│   ├── Naruto
│   │   └── ...
├── Comics
│   ├── Marvel
│   │   ├── Amazing Spider-Man
│   │   │   └── ...
│   └── DC
│       └── ...
└── BD
    ├── Astérix
    │   └── ...
    └── Tintin
        └── ...
```

Chaque sous-dossier de dernier niveau est une série. Komga groupe automatiquement les fichiers par nom de dossier parent.

### Variables d'environnement utiles

| Variable | Valeur par défaut | Description |
|----------|-------------------|-------------|
| `KOMGA_LIBRARIES_SCAN_CRON` | `-` | Expression cron pour le scan automatique (`0 0 */6 * * *` = toutes les 6h) |
| `KOMGA_LIBRARIES_SCAN_STARTUP` | `false` | Scan au démarrage du conteneur |
| `KOMGA_REMEMBERME_KEY` | - | Clé secrète pour la persistance des sessions (obligatoire en prod) |
| `KOMGA_TASKCONSISTENCY_SCAN_ONBOOT` | `false` | Vérification d'intégrité au boot |
| `SERVER_PORT` | `25600` | Port interne du serveur |

### Mise à jour

Mettre à jour Komga est aussi simple que changer l'image :

```bash
cd ~/komga
docker compose pull
docker compose up -d
```

La base SQLite est automatiquement migrée si nécessaire.

### Accès depuis mobile

L'interface web de Komga est parfaitement utilisable sur mobile, mais pour une expérience native, utilise le flux OPDS avec Panels (iOS) ou Moon Reader (Android). Pour les liseuses Kobo, le Kobo Sync intégré permet de télécharger et synchroniser la progression directement depuis l'appareil.

### Sécurité basique

- Change le mot de passe admin par défaut immédiatement
- Utilise HTTPS via ton reverse proxy, jamais en HTTP sur internet
- Mets une authentification forte si exposé au web (fail2ban, Authelia, ou authentification Cloudflare)
- Restreins les bibliothèques sensibles par utilisateur dans `Administration` → `Users`
- Si tu cherches à durcir la sécurité de ton serveur, mes commandes de [hardening Linux](/hardening-linux-10-commandes/) restent pertinentes

## Conclusion

Komga est le serveur de BD et manga auto-hébergé que la communauté attendait depuis des années. Léger, rapide, conçu par un utilisateur de manga pour des utilisateurs de manga, il gère parfaitement les collections en CBZ/CBR avec une interface moderne et un support OPDS / Kobo Sync que personne d'autre ne propose gratuitement. À côté de ton [Jellyfin pour les films](/jellyfin-docker-alternative-netflix-gratuite/) et de ton [Kavita pour les ebooks](/kavita-docker-lecteur-ebooks/), il complète l'écosystème média de ton homelab sans friction.

Le déploiement Docker prend moins de 10 minutes. Mets tes archives dans un dossier, monte le volume, lance le conteneur, et commence à lire. Aucun SaaS, aucun abonnement, aucune télémétrie. Tes mangas restent chez toi, accessibles depuis n'importe où.
