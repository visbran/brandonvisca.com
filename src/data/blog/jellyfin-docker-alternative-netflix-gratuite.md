---
title: "Jellyfin avec Docker : Ton Netflix Gratuit en 30 Min (Économise 378€/an)"
pubDatetime: "2025-10-26T20:59:01+01:00"
description: "Installe Jellyfin avec Docker en 20 min. Alternative Netflix auto-hébergée, économise 378€/an. Guide 2025 complet + transcoding 4K."
tags:
  - docker
  - auto-hebergement
  - homelab
  - linux
  - guide
  - intermediaire
---

🎯 TL;DR
---

Tu paies Netflix + Disney+ + Prime Video = **378€/an** pour regarder des films ? Spoiler : tu peux héberger **ton propre Netflix avec Jellyfin** pour 0€ supplémentaire si tu as déjà un serveur (ou 4€/mois sur VPS).

**Ce que tu vas apprendre :**

- Installer Jellyfin avec Docker en 20 minutes chrono
- Organiser ta bibliothèque films/séries automatiquement (metadata, posters, sous-titres)
- Streamer sur TV, mobile, tablette, navigateur
- Transcoding 4K en temps réel (si ton serveur suit)
- Économiser 378€/an minimum en virant tes abonnements streaming
- Inviter famille/amis avec comptes séparés

**Prérequis :**

- Un serveur Linux (VPS, Raspberry Pi 4/5, vieux PC, NAS)
- 2 Go RAM minimum, 4 Go recommandé (8 Go pour transcoding 4K)
- Docker installé
- Espace disque selon ta collection (500 Go = ~200 films HD)
- 30 minutes de ton temps

---

Pourquoi Jellyfin > Netflix (et Plex, et Emby)
---

### Le calcul économique qui fait mal

**Abonnements streaming en 2025 :**

- Netflix Standard : 13,49€/mois = **162€/an**
- Disney+ Premium : 10,99€/mois = **132€/an**
- Prime Video : 6,99€/mois = **84€/an**
- Canal+ : 24,99€/mois = **300€/an** (si fan de sport/séries)

💰 **Total famille moyenne : 378-678€/an**

**Jellyfin auto-hébergé :**

- Serveur (si VPS) : 4-8€/mois = **48-96€/an**
- Électricité (Raspberry Pi) : **~10€/an**
- Contenu : **variable** (achats VOD, Blu-ray d’occasion, bibliothèque municipale…)

💰 **Économie réaliste sur 5 ans : 1 500-3 000€**

Et encore, si tu réutilises ton serveur Nextcloud ou un vieux PC, c’est **quasi gratuit**.

---

### Jellyfin vs Plex vs Emby : Le match

| Critère | Jellyfin | Plex | Emby |
|---|---|---|---|
| **Prix** | 🟢 Gratuit à vie | 🟡 Gratuit (limité) ou 5€/mois | 🟡 Gratuit (limité) ou 5€/mois |
| **Open source** | 🟢 100% | 🔴 Propriétaire | 🟡 Partiellement |
| **Vie privée** | 🟢 Aucune télémétrie | 🔴 Compte Plex obligatoire | 🟡 Compte optionnel |
| **Transcoding** | 🟢 Illimité | 🟡 Limité sans Plex Pass | 🟢 Illimité |
| **Apps mobiles** | 🟢 Gratuites | 🔴 5€ une fois | 🟡 Freemium |
| **Interface** | 🟡 Correcte | 🟢 Excellente | 🟢 Très bonne |
| **Plugins** | 🟢 Large choix | 🟡 Restreints | 🟡 Moyens |
| **Communauté FR** | 🟢 Active | 🟢 Très active | 🟡 Moyenne |

**Verdict :**

- **Tu veux gratuit + privé + sans limites** → **Jellyfin** ✅
- **Tu veux la meilleure interface** → Plex (mais tu paies)
- **Tu veux un mix** → Emby

💡 **Mon avis perso** : Jellyfin fait 95% du job de Plex gratuitement. L’interface est moins léchée mais tu t’y fais en 2 jours. Et surtout, **tes données restent chez toi**.

---

Jellyfin c’est quoi exactement ?
---

**En une phrase :** Un serveur multimédia qui transforme ta collection de films/séries en **Netflix personnel**.

**Ce que ça fait :**  
✅ Récupère automatiquement les **posters, synopsis, notes** (via TMDB/TVDB)  
✅ Organise ta bibliothèque par **films, séries, musique, photos**  
✅ **Transcode à la volée** (ton film 4K devient 720p si ton mobile est en 4G)  
✅ **Sous-titres automatiques** (recherche et téléchargement intégrés)  
✅ **Comptes utilisateurs** séparés (Papa voit pas les dessins animés des enfants)  
✅ **Reprise lecture** multi-appareils (tu commences sur TV, tu finis sur tablette)  
✅ **Apps dédiées** Android TV, Fire TV, Roku, iOS, Android, Web…

**Ce que ça fait PAS :**  
❌ Télécharger du contenu à ta place (c’est pas son job)  
❌ Gérer les DRM (pas de Netflix/Prime rippé)  
❌ Remplacer ta box TV (c’est complémentaire)

---
## Table des matières


- [Pourquoi Jellyfin > Netflix (et Plex, et Emby)](#pourquoi-jellyfin-netflix-et-plex-et-emby)
  - [Le calcul économique qui fait mal](#le-calcul-economique-qui-fait-mal)
  - [Jellyfin vs Plex vs Emby : Le match](#jellyfin-vs-plex-vs-emby-le-match)
- [Jellyfin c’est quoi exactement ?](#jellyfin-cest-quoi-exactement)
- [Avant de commencer : Choisir ton matériel](#avant-de-commencer-choisir-ton-materiel)
  - [Option 1 : VPS Cloud (le plus simple)](#option-1-vps-cloud-le-plus-simple)
  - [Option 2 : Homelab (le plus économique)](#option-2-homelab-le-plus-economique)
  - [Option 3 : Combo VPS + Stockage externe (hybride)](#option-3-combo-vps-stockage-externe-hybride)
- [Installation Jellyfin avec Docker : La méthode qui marche](#installation-jellyfin-avec-docker-la-methode-qui-marche)
  - [Étape 1 : Préparer le serveur](#etape-1-preparer-le-serveur)
  - [Étape 2 : Créer la structure](#etape-2-creer-la-structure)
  - [Étape 3 : Docker Compose optimisé](#etape-3-docker-compose-optimise)
  - [Étape 4 : Activer le transcoding Intel Quick Sync (si mini PC Intel)](#etape-4-activer-le-transcoding-intel-quick-sync-si-mini-pc-intel)
  - [Étape 5 : Lancer Jellyfin](#etape-5-lancer-jellyfin)
  - [Étape 6 : Configuration initiale Jellyfin](#etape-6-configuration-initiale-jellyfin)
- [Organiser ta bibliothèque : Le naming qui change tout](#organiser-ta-bibliotheque-le-naming-qui-change-tout)
  - [Structure de dossiers recommandée](#structure-de-dossiers-recommandee)
  - [Scanner la bibliothèque](#scanner-la-bibliotheque)
- [Configuration HTTPS avec Nginx Proxy Manager](#configuration-https-avec-nginx-proxy-manager)
- [Apps mobiles & clients](#apps-mobiles-clients)
  - [📱 Mobile (Android & iOS)](#%F0%9F%93%B1-mobile-android-i-os)
  - [📺 TV (Android TV, Fire TV, Apple TV)](#%F0%9F%93%BA-tv-android-tv-fire-tv-apple-tv)
  - [💻 Desktop (Windows, Mac, Linux)](#%F0%9F%92%BB-desktop-windows-mac-linux)
- [Optimisations avancées](#optimisations-avancees)
  - [Activer le transcoding matériel](#activer-le-transcoding-materiel)
  - [Sous-titres automatiques](#sous-titres-automatiques)
  - [Intro Skip (sauter les génériques)](#intro-skip-sauter-les-generiques)
- [Cas d’usage réels](#cas-dusage-reels)
  - [Scénario 1 : Famille (4 personnes)](#scenario-1-famille-4-personnes)
  - [Scénario 2 : Cinéphile hardcore](#scenario-2-cinephile-hardcore)
  - [Scénario 3 : Collocation / Famille élargie](#scenario-3-collocation-famille-elargie)
- [Problèmes courants & Solutions](#problemes-courants-solutions)
  - [❌ « Playback Error » / Erreur de lecture](#%E2%9D%8C-playback-error-erreur-de-lecture)
  - [❌ Transcoding ultra-lent (buffering constant)](#%E2%9D%8C-transcoding-ultra-lent-buffering-constant)
  - [❌ Metadata en anglais au lieu de français](#%E2%9D%8C-metadata-en-anglais-au-lieu-de-francais)
  - [❌ Jellyfin inaccessible depuis l’extérieur](#%E2%9D%8C-jellyfin-inaccessible-depuis-lexterieur)
- [🧩 Jellyfin : La pièce maîtresse de ton indépendance numérique](#maillage-interne-stack-homelab-complete)
- [Légalité & Éthique : Ce qu’il faut savoir](#legalite-ethique-ce-quil-faut-savoir)
  - [✅ Usages légaux en France](#%E2%9C%85-usages-legaux-en-france)
  - [💡 Sources de contenu légales](#%F0%9F%92%A1-sources-de-contenu-legales)
- [Conclusion : Ton Netflix à toi, pour toujours](#conclusion-ton-netflix-a-toi-pour-toujours)


Avant de commencer : Choisir ton matériel
---

### Option 1 : VPS Cloud (le plus simple)

**Pour qui ?** Tu veux streamer depuis l’extérieur, pas de serveur à la maison.

**⚠️ ATTENTION : Légalité du streaming depuis VPS**

Juridiquement en France :

- ✅ Streamer **tes propres Blu-ray/DVD** = légal (copie privée)
- ✅ Héberger sur VPS français = légal
- ❌ Partager avec 50 personnes = zone grise (contrefaçon)

**Conseil légal :** Utilise Jellyfin pour **ton usage personnel/familial** uniquement.

**VPS recommandés pour Jellyfin :**

| VPS | Prix/mois | Specs | Transcoding |
|---|---|---|---|
| Hetzner CPX21 | 8,21€ HT | 3 vCPU, 4 Go RAM | 1080p OK, 4K difficile |
| Scaleway DEV1-M | 0,02€/h | 3 vCPU, 4 Go RAM | 1080p OK |
| OVH VPS Value | 6€ HT | 2 vCPU, 4 Go RAM | 720p-1080p OK |

💡 **Astuce transcoding :** Le transcoding 4K nécessite un CPU costaud OU un GPU (pas dispo sur VPS classiques). Solution : **active Direct Play** = le client lit directement sans transcoder.

---

### Option 2 : Homelab (le plus économique)

**Pour qui ?** Tu as un serveur chez toi (Raspberry Pi, vieux PC, mini PC, NAS).

**Matériel testé et approuvé :**

**🔴 Raspberry Pi 4/5 (8 Go RAM)** – 80€

- ✅ Consommation : 5W (10€/an électricité)
- ✅ Silencieux, compact
- ⚠️ Transcoding limité (720p max, 1080p possible avec Raspberry Pi 5)
- 💡 **Idéal pour Direct Play** (pas de transcoding)

**🟢 Mini PC x86 (Intel N100)** – 150-200€

- ✅ Transcoding matériel Intel Quick Sync (4K OK)
- ✅ Consommation : 10-15W (20€/an)
- ✅ 16 Go RAM possible
- 💡 **Le meilleur rapport qualité/prix 2025**

**🟡 Vieux PC reconverti** – 0€

- ✅ Gratuit (tu l’as déjà)
- ❌ Consommation élevée (50-150W = 100-300€/an)
- ✅ Transcoding OK si CPU récent (i5 8ème gen+)
- 💡 **Solution transitoire avant mini PC**

**🔵 NAS Synology/QNAP** – 300-800€

- ✅ Tout-en-un (stockage + apps)
- ✅ Transcoding matériel (selon modèle)
- ❌ Cher à l’achat
- 💡 **Si tu as déjà un NAS, c’est parfait**

**Ma recommandation 2025 :** **Mini PC Intel N100** (Beelink, GMKtec, Acemagic) = sweet spot performance/prix/conso.

---

### Option 3 : Combo VPS + Stockage externe (hybride)

**Pour qui ?** Tu veux l’accessibilité du VPS mais le stockage pas cher.

**Setup :**

- **VPS léger** (2 Go RAM) pour Jellyfin : 4€/mois
- **Stockage cloud** (Backblaze B2, Wasabi, Hetzner Storage Box) : 5€/To/mois
- **Total : 9€/mois** pour To illimité accessible partout

💡 **Astuce avancée :** Monte le stockage cloud avec `rclone` en cache local. Tu gagnes en vitesse sans exploser le VPS.

---

Installation Jellyfin avec Docker : La méthode qui marche
---

### Étape 1 : Préparer le serveur

On repart sur **Ubuntu 24.04 LTS** (ou 22.04, Debian 12, Raspbian…).

```bash
# Mise à jour système
sudo apt update && sudo apt upgrade -y

# Installer Docker si pas déjà fait
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# Vérifier
docker --version
```

# Créer les dossiers
mkdir -p ~/jellyfin/{config,cache,media/{movies,series,music}}
cd ~/jellyfin

# Vérifier la structure
tree -L 2

Tu devrais voir :

```bash
jellyfin/
├── config/     # Configuration Jellyfin
├── cache/      # Cache transcoding
└── media/
    ├── movies/ # Tes films ici
    ├── series/ # Tes séries ici
    └── music/  # Ta musique ici
```

nano docker-compose.yml

Colle ce fichier **testé en amont** :

```bash
services:
  jellyfin:
    image: jellyfin/jellyfin:latest
    container_name: jellyfin
    restart: unless-stopped

    # Ports
    ports:
      - "8096:8096"   # Interface web
      - "8920:8920"   # HTTPS (optionnel)
      - "7359:7359/udp" # Auto-discovery
      - "1900:1900/udp" # DLNA

    # Volumes
    volumes:
      - ./config:/config
      - ./cache:/cache
      - ./media:/media:ro  # :ro = read-only (sécurité)
      # Si tu as un disque externe monté ailleurs :
      # - /mnt/films:/media/movies:ro
      # - /mnt/series:/media/series:ro

    # Variables d'environnement
    environment:
      - PUID=1000  # ID utilisateur (vérifie avec 'id -u')
      - PGID=1000  # ID groupe (vérifie avec 'id -g')
      - TZ=Europe/Paris
      - JELLYFIN_PublishedServerUrl=https://jellyfin.ton-domaine.fr  # Change si domaine

    # Transcoding matériel (optionnel)
    # Décommente selon ton matériel :

    # Intel Quick Sync (mini PC Intel)
    # devices:
    #   - /dev/dri:/dev/dri

    # NVIDIA GPU (si GPU NVIDIA)
    # runtime: nvidia
    # environment:
    #   - NVIDIA_VISIBLE_DEVICES=all

    # AMD GPU (si GPU AMD)
    # devices:
    #   - /dev/dri:/dev/dri

    networks:
      - jellyfin-network

networks:
  jellyfin-network:
    driver: bridge
```

  id
  # uid=1000(brandon) gid=1000(brandon) groups=...

- `/media:ro` : Read-only = Jellyfin peut **lire** mais pas **modifier/supprimer** tes films (sécurité)
- `TZ=Europe/Paris` : Fuseau horaire français (sinon les heures de visionnage sont fausses)
- **Transcoding matériel** : Décommente la section selon ton matériel pour accélérer le transcoding x10

---

### Étape 4 : Activer le transcoding Intel Quick Sync (si mini PC Intel)

Si tu as un mini PC Intel N100/i3/i5/i7, tu peux utiliser **Quick Sync** = transcoding 4K ultra-rapide.

```bash
# Vérifier que /dev/dri existe
ls -la /dev/dri
# Tu dois voir renderD128 et card0

# Donner accès à Jellyfin
sudo usermod -aG render $USER
sudo usermod -aG video $USER

# Décommenter dans docker-compose.yml :
nano docker-compose.yml
```

devices:
  - /dev/dri:/dev/dri

---

### Étape 5 : Lancer Jellyfin

```bash
# Démarrer
docker compose up -d

# Vérifier que ça tourne
docker ps

# Voir les logs
docker compose logs -f jellyfin
```

/media/movies/
├── Inception (2010)/
│   └── Inception (2010).mkv
├── The Matrix (1999)/
│   └── The Matrix (1999).mkv
├── Interstellar (2014)/
│   └── Interstellar (2014) - 1080p.mkv
└── Le Fabuleux Destin d'Amélie Poulain (2001)/
    └── Le Fabuleux Destin d'Amélie Poulain (2001).mkv

**Règles :**

- ✅ **Dossier par film** : `Nom du Film (Année)/`
- ✅ **Nom de fichier** : `Nom du Film (Année).extension`
- ✅ **Année obligatoire** : sinon Jellyfin confond les remakes
- ⚠️ Évite les caractères spéciaux : `é` OK, mais `? : * < >` → remplace par `-`

---

**📺 Séries (structure optimale) :**

```bash
/media/series/
├── Breaking Bad/
│   ├── Season 01/
│   │   ├── Breaking Bad - S01E01 - Pilot.mkv
│   │   ├── Breaking Bad - S01E02.mkv
│   │   └── Breaking Bad - S01E03.mkv
│   ├── Season 02/
│   │   ├── Breaking Bad - S02E01.mkv
│   │   └── ...
│   └── Season 05/
│       └── ...
└── Stranger Things/
    ├── Season 01/
    │   ├── Stranger Things - S01E01.mkv
    │   └── ...
    └── Season 04/
        └── ...
```

# Augmenter les timeouts pour le streaming
proxy_connect_timeout 600;
proxy_send_timeout 600;
proxy_read_timeout 600;
send_timeout 600;

# Pas de buffer pour le streaming en temps réel
proxy_buffering off;

# Headers
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_set_header X-Forwarded-Host $host;

5. **Save** → Attends 30s → Teste `https://jellyfin.ton-domaine.fr`

🎉 **Ton Jellyfin est accessible en HTTPS !**

---

Apps mobiles & clients
---

### 📱 Mobile (Android & iOS)

**Jellyfin officiel** (recommandé) :

- Android : [Play Store](https://play.google.com/store/apps/details?id=org.jellyfin.mobile)
- iOS : [App Store](https://apps.apple.com/fr/app/jellyfin-mobile/id1480192618)

**Alternatives tierces (parfois meilleures) :**

- **Findroid** (Android) : Interface moderne, meilleure que l’officielle
- **Swiftfin** (iOS) : Plus fluide que l’app officielle
- **Infuse** (iOS, payante 10€/an) : La Rolls du streaming, gère tout

**Configuration :**

1. Lance l’app → **Connexion manuelle**
2. URL : `https://jellyfin.ton-domaine.fr`
3. Identifiants : ton compte Jellyfin
4. ✅ **Activer le téléchargement hors ligne** si tu veux regarder dans le train

---

### 📺 TV (Android TV, Fire TV, Apple TV)

**Android TV / Google TV / Fire TV :**

- Jellyfin officiel dispo sur Play Store TV
- Installe depuis le store de ta box

**Apple TV :**

- Swiftfin (gratuite, excellente)

**Roku :**

- Jellyfin officiel dispo sur Roku Store

**Smart TV Samsung/LG :**

- Pas d’app native 😢
- Solution : **Chromecast** ou **Mini PC Android TV** (30€)

---

### 💻 Desktop (Windows, Mac, Linux)

**Option 1 : Navigateur** (recommandé)

- Ouvre `https://jellyfin.ton-domaine.fr`
- Ça marche parfaitement en web, pas besoin d’app

**Option 2 : Jellyfin Media Player** (si tu veux une vraie app)

- Télécharge : https://github.com/jellyfin/jellyfin-media-player/releases
- Interface type Netflix, mode plein écran

---

Optimisations avancées
---

### Activer le transcoding matériel

Si tu as un mini PC Intel avec Quick Sync :

1. **Dashboard** → **Paramètres** → **Lecture**
2. **Transcoding** :

- Chemin FFmpeg : `/usr/lib/jellyfin-ffmpeg/ffmpeg` (auto)
- ✅ **Activer l’accélération matérielle** : `Intel QuickSync (QSV)`
- ✅ Activer le décodage matériel pour : **H264, HEVC, VP9, AV1**
- ✅ Activer l’encodage matériel pour : **H264, HEVC**

1. **Threads de transcoding** : `0` (auto)
2. **Sauvegarder**

✅ **Test :** Lance un film 4K sur mobile en 4G → Il doit transcoder en 720p instantanément.

---

### Sous-titres automatiques

**Plugin OpenSubtitles :**

1. **Dashboard** → **Plugins** → **Catalogue**
2. Installe : **Open Subtitles**
3. **Redémarre Jellyfin** (obligatoire)
4. **Plugins** → **Open Subtitles** → Configure :

- Crée un compte gratuit sur https://opensubtitles.org
- Entre tes identifiants
- Langue préférée : `Français`

1. **Utilisation :** Clique sur un film → **⚙️ Sous-titres** → **Rechercher** → Jellyfin télécharge les .srt automatiquement

---

### Intro Skip (sauter les génériques)

**Plugin Intro Skipper :**

1. **Plugins** → **Catalogue** → Installe **Intro Skipper**
2. **Redémarre**
3. **Plugins** → **Intro Skipper** :

- ✅ Détection automatique des génériques
- ✅ Bouton « Skip Intro » dans le player

🎉 **Comme Netflix : tu peux sauter les génériques en un clic !**

---

Cas d’usage réels
---

### Scénario 1 : Famille (4 personnes)

**Setup :**

- Mini PC Intel N100 (189€) + disque dur 4 To (90€)
- Total investissement : **279€**
- Électricité : **20€/an**

**Collection :**

- 150 films HD (1,5 To)
- 30 séries (1 To)
- Musique (200 Go)

**Économie :**

- Avant : Netflix + Disney+ + Prime = **378€/an**
- Après : 20€/an électricité
- 💰 **Gain : 358€/an → Amorti en 9 mois**
- 💰 **Gain sur 5 ans : 1 511€**

**Usage :**

- Papa : Films d’action (compte séparé)
- Maman : Séries françaises
- Enfants : Dessins animés (contrôle parental activé)
- Mamie : Regarder depuis son iPad à distance

---

### Scénario 2 : Cinéphile hardcore

**Setup :**

- Vieux PC reconverti (i5-8400, gratuit)
- 2x disques durs 8 To (360€)
- Total : **360€**
- Électricité : **~100€/an**

**Collection :**

- 800 films HD/4K (10 To)
- Documentaires, classiques, films cultes
- Archives personnelles

**Économie :**

- Avant : Achats VOD ~30€/mois = **360€/an**
- Après : 100€/an électricité + 0€ VOD (achète Blu-ray d’occasion 3€)
- 💰 **Gain : 260€/an**

**Usage :**

- Bibliothèque personnelle accessible à vie
- Qualité Blu-ray préservée (pas de compression streaming)
- Pas de censure/disparition de contenu (coucou Netflix qui vire des films)

---

### Scénario 3 : Collocation / Famille élargie

**Setup :**

- VPS 8 Go RAM (15€/mois) + Hetzner Storage Box 5 To (15€/mois)
- Total : **30€/mois = 360€/an**

**Utilisateurs :**

- 8 comptes (4 colocataires + 4 membres famille à distance)

**Économie :**

- Avant : 8 x Netflix Standard = **8 x 162€ = 1 296€/an**
- Après : 360€/an partagé entre 8 = **45€/personne/an**
- 💰 **Économie collective : 936€/an**
- 💰 **Par personne : 117€/an économisés**

---

Problèmes courants & Solutions
---

### ❌ « Playback Error » / Erreur de lecture

**Causes possibles :**

1. **Format non supporté par le client**  
  → Solution : Active le transcoding dans les paramètres Jellyfin
2. **Bande passante insuffisante**  
  → Solution : Réduis la qualité (Dashboard → Lecture → Bitrate max : 8 Mbps)
3. **Transcoding qui plante (CPU trop faible)**  
  → Solution : Active Direct Play (pas de transcoding) :

   Paramètres utilisateur → Lecture → Qualité : Maximum

---

### ❌ Transcoding ultra-lent (buffering constant)

**Symptôme :** Le film lag toutes les 10 secondes.

**Solution :**

```bash
# Vérifier la charge CPU pendant le transcoding
docker exec jellyfin htop

# Si CPU à 100% constamment :
# → Ton serveur est trop faible pour transcoder
```

   sudo ufw allow 80
   sudo ufw allow 443

3. **Vérifie le DNS** : `jellyfin.ton-domaine.fr` pointe bien vers ton IP publique ?

---

🧩 Jellyfin : La pièce maîtresse de ton indépendance numérique
---

Bravo, tu as maintenant ton propre Netflix. Mais imagine un instant :

- **Jellyfin** pour tes films/séries (✅ fait)
- **Nextcloud** pour tes fichiers/photos/documents
- **Vaultwarden** pour tes mots de passe

Tu te retrouves avec **une stack d’indépendance numérique complète** qui te coûte 0€/mois en abonnements. Le seul coût ? L’électricité de ton serveur (environ 5€/mois pour un mini-PC).

**Calcul rapide :**

- Netflix Standard : 13,99€/mois
- Google One (200 Go) : 2,99€/mois
- 1Password : 4,99€/mois

= **261,84€/an** que tu peux économiser.

Et ce n’est que le début. Si tu combines ces 3 services, tu montes à **534€/an d’économies** tout en reprenant le contrôle de tes données.

👉 **[Consulte le guide complet d’indépendance numérique 2025](https://brandonvisca.com/independance-numerique-2025-guide-complet/)** pour voir comment tout interconnecter proprement.

*Bonus : Le guide inclut une roadmap progressive pour ne pas te noyer dans la technique.*

---

Légalité & Éthique : Ce qu’il faut savoir
---

### ✅ Usages légaux en France

**Tu as le DROIT de :**

- Ripper tes propres DVD/Blu-ray pour copie privée (Article L122-5 CPI)
- Héberger ta collection personnelle sur Jellyfin
- Partager avec ta famille proche (même foyer)
- Regarder depuis l’extérieur (en vacances, au travail)

**Tu n’as PAS le droit de :**

- ❌ Télécharger des films piratés (torrent sans droit = contrefaçon)
- ❌ Partager avec 50 personnes (= diffusion publique, Article L335-2 CPI)
- ❌ Contourner les DRM (Netflix/Prime/Disney+ rippé = illégal)

### 💡 Sources de contenu légales

**Où trouver du contenu pour Jellyfin :**

1. **Médiathèque municipale** : Emprunte des DVD/Blu-ray gratuitement, rippe-les
2. **Blu-ray d’occasion** : Leboncoin, Vinted, Cash Converters (3-5€/film)
3. **VOD sans DRM** : Arte Boutique, Vimeo On Demand (téléchargement MP4)
4. **Archives personnelles** : Vidéos de vacances, films de famille
5. **Creative Commons** : Archive.org, films tombés dans domaine public

**Outil de rip légal : MakeMKV**

- Gratuit pour DVD (Windows/Mac/Linux)
- 60€ pour Blu-ray (licence à vie)
- Télécharge : https://www.makemkv.com/

---

Conclusion : Ton Netflix à toi, pour toujours
---

Tu viens de monter **ton propre service de streaming** en 30 minutes. Jellyfin avec Docker, c’est :

✅ **Économique** : 358€/an économisés minimum  
✅ **Indépendant** : Plus d’abonnements qui augmentent tous les ans  
✅ **Privé** : Tes habitudes de visionnage ne partent pas chez Netflix  
✅ **Complet** : Films, séries, musique, photos, tout en un  
✅ **Durable** : Ta collection t’appartient à vie

**Prochaines étapes suggérées :**

1. **Organise ta bibliothèque** : Renomme tes fichiers proprement (Filebot aide beaucoup)
2. **Invite ta famille** : Créer des comptes utilisateurs (Dashboard → Utilisateurs)
3. **Automatise les backups** : Sauvegarde `/config` et ta liste de films
4. **Explore les plugins** : Intro Skipper, OpenSubtitles, Trakt…
5. **Monte ta stack complète** : Jellyfin + Nextcloud + Vaultwarden = indépendance totale

Et surtout, profite de **378€/an** dans ta poche au lieu de les filer à Netflix. 🎉

💬 **Questions, problèmes, ou succès ?** Balance tout en commentaire !
