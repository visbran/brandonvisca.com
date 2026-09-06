---
title: "Kavita Docker : ton lecteur ebooks auto-hébergé (alternative à Calibre)"
description: "Installe Kavita avec Docker : le serveur de ebooks auto-hébergé qui lit EPUB, PDF, CBZ et manga. Guide complet avec Docker Compose, config et astuces."
pubDatetime: "2026-06-14T06:00:00.000Z"
author: Brandon
tags:
  - auto-hebergement
  - docker
  - kavita
  - ebooks
  - intermediaire
featured: false
draft: false
ogImage: ""
---
> 💡 **TL;DR**
> - Kavita est un serveur de lecture ebooks auto-hébergé qui gère EPUB, PDF, CBZ/CBR, images et manga
> - Tu le déploies en 5 minutes avec Docker Compose, interface web moderne et responsive
> - Alternative open-source (GPL-3.0) à Calibre-Web, plus rapide et plus agréable à utiliser
> - Docker Compose complet, tableau comparatif et astuces de config inclus ci-dessous

## Table des matières

## Pourquoi un serveur d'ebooks auto-hébergé ?

T'as une bibliothèque numérique qui ressemble à un champ de bataille. Des EPUB achetés sur diverses plateformes, des PDF de documentation technique, des mangas en CBZ téléchargés légalement (ou pas), et des scans de vieux magazines. Le tout éparpillé sur ton NAS, ton laptop, ton téléphone et trois applications différentes qui ne se parlent pas.

Calibre Desktop ? C'est un outil puissant, mais l'interface ressemble à Windows 95 et la synchronisation entre appareils relève du parcours du combattant. Calibre-Web est mieux, mais il reste visuellement daté et certaines opérations demandent encore de passer par le backend Calibre. Quant aux solutions commerciales comme Kindle Cloud, elles te lient à un écosystème fermé où tes livres ne t'appartiennent pas vraiment.

Tu as besoin d'un serveur de lecture qui :
- lit tous tes formats sans conversion préalable,
- est accessible depuis n'importe quel appareil avec un navigateur,
- garde ta position de lecture et tes favoris synchronisés,
- te laisse gérer tes collections sans dépendre d'un service tiers,
- est joli et fluide, parce que passer du temps dans une UI moche ça use le moral.

Kavita répond à tous ces besoins. C'est un projet open-source développé en C# avec .NET, sous licence GPL-3.0, avec plus de 10 900 stars sur GitHub. L'image Docker officielle `jvmilazz0/kavita` est maintenue activement et supporte amd64, arm64 et armv7. Si tu cherches à compléter ton homelab avec un service média dédié aux ebooks, Kavita s'intègre parfaitement à côté de ton [Jellyfin pour les films](/jellyfin-docker-alternative-netflix-gratuite/) ou ta [galerie PhotoPrism](/photoprism-docker-galerie-photo/).

## Qu'est-ce que Kavita exactement ?

Kavita n'est pas un simple indexeur de fichiers. C'est un serveur de lecture complet avec une interface web moderne, pensée pour la consommation de contenus longs.

Voici ce qu'il propose concrètement :

- **Formats natifs multiples** : EPUB, PDF, CBZ, CBR, images (PNG, JPG, WebP), archives ZIP/RAR contenant des images. Pas de conversion nécessaire, Kavita lit directement le fichier source.
- **Lecture web responsive** : interface adaptée au desktop, tablette et mobile. Lecture en mode continu ou paginée, zoom, rotation, mode nuit.
- **Gestion des bibliothèques** : tu organises tes ebooks par collections (Roman, Tech, Manga, Documentation) et Kavita scanne automatiquement les dossiers pour détecter les nouveaux fichiers.
- **Métadonnées et couvertures** : extraction automatique des couvertures, titres, auteurs, séries et numéros de tome depuis les fichiers EPUB et les archives CBZ.
- **Lecture multi-appareils** : ta position de lecture, tes favoris et tes listes de lecture suivent ton compte utilisateur.
- **Lecture hors ligne** : tu peux télécharger un chapitre ou un livre complet pour le lire sans connexion.
- **Comptes utilisateurs multiples** : crée des comptes pour ta famille ou tes amis avec des permissions sur certaines bibliothèques seulement.
- **Mode manga** : lecture de droite à gauche pour les mangas japonais, avec défilement continu optimisé.
- **API REST** : pour automatiser, intégrer ou synchroniser avec d'autres outils.
- **Recherche rapide** : indexation interne pour retrouver un titre ou un auteur en quelques millisecondes.
- **OPDS** : flux OPDS compatible avec les lecteurs externes comme Moon Reader ou KyBook.

Le tout tourne dans un seul conteneur Docker léger, sans base de données externe nécessaire (Kavita utilise SQLite par défaut). Si tu débutes avec Docker, commence par mon guide sur [les services essentiels à auto-héberger](/docker-debutant-services-auto-heberger/) pour bien poser les bases avant d'ajouter Kavita à ta stack.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose installés (Docker Engine 24+ recommandé)
- 1 cœur CPU et 512 Mo de RAM minimum (1 Go recommandé pour les grosses bibliothèques)
- 1 Go d'espace disque pour l'application, puis selon ta collection d'ebooks
- Un nom de domaine ou sous-domaine si tu veux HTTPS en frontal
- Un reverse proxy (Caddy, Traefik ou Nginx Proxy Manager) pour gérer les certificats SSL

Kavita est extrêmement léger. Un Raspberry Pi 4 avec 2 Go de RAM suffit pour servir une bibliothèque de plusieurs milliers de titres à plusieurs utilisateurs simultanés. Pour un usage confortable avec de gros PDF, un petit VPS de 1 cœur / 2 Go est largement suffisant.

## Déploiement Kavita avec Docker Compose

Crée un dossier dédié et un fichier `docker-compose.yml` :

```bash
mkdir -p ~/kavita && cd ~/kavita
```

Voici le Docker Compose complet et prêt à l'emploi :

```yaml
version: "3.8"

services:
  kavita:
    image: jvmilazz0/kavita:latest
    container_name: kavita
    environment:
      - TZ=Europe/Paris
    volumes:
      - ./kavita-data:/kavita/config
      - /chemin/vers/ta/bibliotheque:/books:ro
    ports:
      - "5000:5000"
    restart: unless-stopped
```

**Explications ligne par ligne :**

- `image: jvmilazz0/kavita:latest` : l'image officielle, mise à jour régulièrement avec les nouvelles versions stables.
- `container_name: kavita` : pour identifier facilement le conteneur dans `docker ps`.
- `environment: TZ=Europe/Paris` : fuseau horaire pour les logs et les tâches planifiées.
- `volumes` : deux montages obligatoires. Le premier (`./kavita-data:/kavita/config`) persiste la base de données SQLite, les caches et les paramètres. Le second (`/chemin/vers/ta/bibliotheque:/books:ro`) monte ta bibliothèque d'ebooks en lecture seule. **Adapte `/chemin/vers/ta/bibliotheque` à ton système.**
- `ports: "5000:5000"` : expose Kavita sur le port 5000 de ton serveur.
- `restart: unless-stopped` : redémarrage automatique sauf arrêt manuel.

**Lancement :**

```bash
docker compose up -d
```

Attends 10-20 secondes que le conteneur initialise sa base de données, puis ouvre `http://IP_DE_TON_SERVEUR:5000` dans ton navigateur.

## Configuration initiale

La première fois que tu te connectes, Kavita te demande de créer un compte administrateur. Renseigne un email, un mot de passe solide, et valide.

Une fois dans le dashboard, voici les étapes essentielles :

**1. Créer une bibliothèque**

Va dans Settings > Libraries > Add Library. Choisis un type :
- **Book** : pour les EPUB, PDF et ebooks standards
- **Comic** : pour les CBZ, CBR, archives d'images
- **Manga** : comme Comic mais avec lecture de droite à gauche par défaut

Dans le champ folder, indique `/books` (ou le sous-dossier correspondant si tu as monté plusieurs répertoires).

**2. Lancer le premier scan**

Kavita scanne automatiquement les fichiers et extrait les métadonnées. Selon la taille de ta bibliothèque, ça peut prendre de quelques secondes à plusieurs minutes. Les couvertures apparaissent au fur et à mesure.

**3. Paramétrer le scan automatique**

Dans Settings > Libraries > Edit (ta bibliothèque), active l'option "Watch Folder" si tu veux que Kavita détecte les nouveaux fichiers en temps réel. Sinon, un scan périodique toutes les 24 heures est configuré par défaut.

**4. Créer des utilisateurs (optionnel)**

Dans Account > Users, tu peux créer des comptes avec des accès restreints à certaines bibliothèques. Pratique si tu partages ton serveur avec ta famille et que tu veux séparer les mangas des PDF techniques.

## Scanner et organiser ta bibliothèque

L'organisation de tes fichiers influence directement la qualité du scan. Kavita est assez intelligent, mais quelques conventions aident énormément :

- **Pour les ebooks** : `Auteur/Titre.epub` ou `Série/Tome 01 - Titre.epub`
- **Pour les mangas/comics** : `Série/Chapitre 001/` ou `Série/Tome 01.cbz`
- **Les archives CBZ/CBR** : Kavita lit directement les archives sans les extraire. Assure-toi que les images sont nommées dans l'ordre (001.jpg, 002.jpg, etc.).

Kavita reconnaît les séries et numéros de tome dans les noms de fichiers. Si tu utilises un outil comme ComicTagger ou Mylar pour renseigner les métadonnées ComicInfo.xml dans tes CBZ, Kavita les exploite nativement.

Pour les EPUB, les métadonnées internes (titre, auteur, série, langue) sont lues directement. Pas besoin de renommer parfaitement si l'EPUB est bien fait.

Si tu cherches aussi une solution pour gérer tes fichiers sur le même serveur, j'ai un guide sur [File Browser Docker](/filebrowser-docker-gestionnaire-fichiers/) qui te permettra d'organiser et transférer tes ebooks facilement avant de les scanner avec Kavita.

## Tableau comparatif : Kavita vs Calibre-Web vs Komga

Tu hésites entre plusieurs solutions ? Voici le match réel :

| Critère | Kavita | Calibre-Web | Komga |
|---------|--------|-------------|-------|
| **Licence** | GPL-3.0 | GPL-3.0 | AGPL-3.0 |
| **Formats ebooks** | EPUB, PDF, CBZ, CBR, images | EPUB, PDF, CBZ, CBR, TXT | CBZ, CBR, PDF, EPUB (limité) |
| **Interface** | Moderne, responsive, fluide | Fonctionnelle mais datée | Moderne, orientée comics/manga |
| **Lecture web** | Native, mode nuit, pagination | Native mais basique | Excellente, mode manga optimisé |
| **Base de données** | SQLite intégrée (simple) | Nécessite Calibre Desktop | SQLite intégrée |
| **OPDS** | ✅ Oui | ✅ Oui | ✅ Oui |
| **Multi-utilisateurs** | ✅ Oui, permissions granulaires | ✅ Oui | ✅ Oui |
| **Position de lecture** | ✅ Oui, cross-device | ✅ Oui | ✅ Oui |
| **Lecture hors ligne** | ✅ Téléchargement | ❌ Non | ❌ Non |
| **Extraction métadonnées** | Automatique (couvertures, séries) | Dépend de Calibre Desktop | Automatique (Komga exploite ComicInfo.xml) |
| **Ressources** | Très légère | Légère mais nécessite Calibre | Légère |
| **Manga mode** | ✅ Lecture droite-gauche | ❌ Basique | ✅ Exemplaire |

**Verdict :**

- **Tu veux un serveur ebooks généraliste (romans, tech, manga)** → **Kavita** ✅
- **Tu as déjà une base Calibre Desktop massive et tu veux juste un accès web** → Calibre-Web
- **Tu lis exclusivement des mangas/comics et tu veux la meilleure expérience manga** → [Komga](/komga-docker-bd-manga-auto-heberge/)

Mon avis perso : Kavita fait 90% du job des deux autres réunis, avec une interface bien plus agréable et aucune dépendance externe. Pour un homelab, c'est le choix le plus simple et le plus propre.

## Astuces et bonnes pratiques

**Renommer proprement avant d'importer**

Même si Kavita lit les métadonnées internes, un nommage cohérent améliore la détection des séries. Utilise un outil comme Calibre (desktop) pour retoucher les métadonnées EPUB, ou ComicTagger pour les CBZ, avant de les balancer dans Kavita.

**Séparer les types de contenu**

Crée des bibliothèques distinctes : une pour les ebooks, une pour les mangas, une pour les PDF techniques. Ça évite d'avoir "Le Guide Docker" à côté de "One Piece Tome 94" dans la même grille.

**Activer la compression des images**

Dans Settings > Media, Kavita propose de compresser les images à la volée pour accélérer le chargement. À activer si tu accèdes depuis l'extérieur ou si ta connexion montante est faible.

**Utiliser un reverse proxy pour HTTPS**

N'expose jamais Kavita en HTTP sur Internet. Utilise Caddy, Traefik ou Nginx Proxy Manager pour obtenir un certificat Let's Encrypt. Si tu utilises Caddy, j'ai un [guide complet sur la configuration](/caddy-docker-reverse-proxy-guide/) qui te montrera comment sécuriser ton homelab en quelques minutes.

**Sauvegarder régulièrement**

Le dossier `./kavita-data` contient tout : base de données, utilisateurs, caches, paramètres. Sauvegarde ce dossier avec [Duplicati](/duplicati-docker-sauvegarde/) ou rsync. La bibliothèque d'ebooks elle-même est en lecture seule, donc pas besoin de la sauvegarder depuis Kavita si tu l'as déjà ailleurs.

**Mise à jour**

Pour mettre à jour Kavita :

```bash
cd ~/kavita
docker compose pull
docker compose up -d
```

Kavita gère automatiquement les migrations de base de données au démarrage. Tu ne perds jamais tes données en mettant à jour.

## Reverse proxy et HTTPS

Pour un accès sécurisé avec un nom de domaine, ajoute ce bloc à ton Caddyfile (si tu utilises Caddy) :

```
ebooks.tondomaine.com {
    reverse_proxy localhost:5000
}
```

Ou avec Traefik, ajoute ces labels au service Kavita dans ton Docker Compose :

```yaml
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.kavita.rule=Host(`ebooks.tondomaine.com`)"
      - "traefik.http.routers.kavita.entrypoints=websecure"
      - "traefik.http.routers.kavita.tls.certresolver=letsencrypt"
```

Si tu n'as pas encore de reverse proxy en place, Caddy est de loin la solution la plus simple pour un homelab. Un fichier Caddyfile de 5 lignes et tu as du HTTPS auto-renouvelé sans toucher à Certbot.

## Sauvegarde et mise à jour

**Sauvegarde** : le seul dossier critique est `./kavita-data`. Tu peux le copier avant chaque mise à jour :

```bash
cp -r ~/kavita/kavita-data ~/backups/kavita-data-$(date +%Y%m%d)
```

Ou mieux, automatise avec un cron qui envoie ça vers un serveur distant ou un stockage cloud.

**Mise à jour** : Kavita publie des mises à jour régulières avec des corrections de bugs et des améliorations de performances. La procédure est toujours la même :

```bash
cd ~/kavita
docker compose pull && docker compose up -d
```

Puis vérifie les logs pour t'assurer que la migration s'est bien passée :

```bash
docker logs --tail 50 kavita
```

## Conclusion

Kavita est l'un de ces outils qui rendent l'auto-hébergement si satisfaisant. En une dizaine de minutes, tu passes d'une collection d'ebooks éparpillée et mal organisée à un serveur de lecture propre, rapide et accessible de partout. L'interface est moderne, la lecture est fluide, et la gestion multi-utilisateurs te permet de partager ta bibliothèque sans compromis.

Si tu as déjà un homelab avec Jellyfin pour les films, PhotoPrism pour les photos et peut-être [BookStack pour ta documentation](/bookstack-docker-wiki-equipe/), Kavita complète parfaitement cet écosystème. C'est le dernier maillon qui manquait à ton infrastructure média personnelle.

Et n'oublie pas : tes ebooks restent sur ton serveur. Pas de dépendance à un cloud, pas de DRM qui te bloquent l'accès, pas d'interface encombrée par de la publicité. Juste toi, tes livres, et un serveur qui fait son boulot.
