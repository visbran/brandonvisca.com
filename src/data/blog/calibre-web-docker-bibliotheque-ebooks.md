---
title: "Calibre Web Docker : bibliothèque ebooks auto-hébergée"
description: "Déploie calibre web docker pour lire tes ebooks partout : configuration complète, flux OPDS et sync Kobo, en 10 minutes chrono."
pubDatetime: "2026-10-03T11:02:12+02:00"
modDatetime: "2026-10-02T08:00:00.000Z"
author: Brandon
tags:
  - auto-hebergement
  - stockage
  - multimedia
  - intermediaire
featured: false
draft: false
focusKeyword: calibre web docker
faqs:
  - question: "Calibre-Web remplace-t-il Calibre sur le PC ?"
    answer: "Non. Calibre reste l'outil d'import et d'édition de métadonnées sur ton poste. Calibre-Web lit la bibliothèque générée par Calibre et l'expose en web, en lecture, OPDS et sync Kobo."
  - question: "La conversion de formats fonctionne direct dans le conteneur linuxserver ?"
    answer: "Non, pas par défaut. Il faut ajouter le DOCKER_MODS universal-calibre, qui installe les binaires Calibre dans le conteneur. Sans ça, Calibre-Web lit mais ne convertit rien."
  - question: "Calibre-Web consomme combien de RAM sur un petit serveur ?"
    answer: "Très peu au repos, de l'ordre de 100 à 150 Mo. Ça grimpe pendant une conversion de format ou une génération de miniatures de couvertures, mais ça redescend aussitôt."
---
> 💡 **TL;DR**
> - Calibre-Web expose ta bibliothèque Calibre en interface web : lecture navigateur, flux OPDS, sync Kobo.
> - Une image Docker officielle linuxserver, deux volumes (config, books), et ta bibliothèque est en ligne en 10 minutes.
> - La conversion de formats demande un module en plus (DOCKER_MODS universal-calibre), sinon Calibre-Web se contente de lire ce qui existe déjà.

## Pourquoi auto-héberger sa bibliothèque ebooks

Tu as une collection d'ebooks qui traîne sur ton PC, dans Calibre, et tu voudrais la lire depuis ta liseuse, ta tablette ou ton téléphone sans faire des allers-retours en USB. Les solutions du marché imposent un compte, un cloud, parfois un DRM. Et Calibre lui-même, aussi bon soit-il pour organiser ta bibliothèque, reste un logiciel de bureau : pas d'accès distant natif.

**Calibre-Web** règle ce problème précis, et monter calibre web docker chez toi prend moins de temps qu'il n'en faut pour créer un compte sur un service tiers. C'est une interface web légère, open-source, qui se branche sur une bibliothèque Calibre existante et l'expose en HTTP : navigation par auteur, série ou tag, lecture directe dans le navigateur, flux OPDS pour les apps de lecture mobile, et synchronisation avec les liseuses Kobo. Le tout sous licence GPL-3.0, maintenu activement par janeczku sur GitHub.

Dans mon [guide des services essentiels à auto-héberger avec Docker](/docker-debutant-services-auto-heberger/), je recommande de commencer par les outils qui remplacent un usage quotidien concret. Calibre-Web en fait partie : il transforme un dossier de fichiers EPUB qui dort sur un disque en vraie bibliothèque consultable depuis n'importe quel appareil de la maison. Si tu cherches une alternative aux liseuses cloud fermées, calibre web docker est une des options les plus simples à déployer.

## Table des matières

## Calibre-Web : ce que c'est, ce que ça fait

Calibre-Web ne remplace pas Calibre. Il le complète. Calibre, sur ton PC, reste l'outil d'import, d'édition de métadonnées et de gestion fine de ta collection. Calibre-Web lit ensuite le fichier `metadata.db` généré par Calibre et sert cette bibliothèque en web.

**Fonctionnalités principales :**
- Navigation par auteur, série, tag, langue et note
- Lecture directe en navigateur pour EPUB, PDF, TXT et plusieurs autres formats
- Flux OPDS compatible avec les applications de lecture mobile (KyBook, Moon+ Reader, etc.)
- Synchronisation native avec les liseuses Kobo
- Gestion d'utilisateurs avec permissions granulaires par compte
- Authentification LDAP et OAuth (Google, GitHub)
- Conversion de formats via les binaires Calibre, si tu les ajoutes au conteneur

Le point à retenir : Calibre-Web, par défaut, ne convertit rien et ne génère rien. Il lit ce qui existe dans ta bibliothèque. Pour la conversion EPUB vers MOBI ou l'édition de métadonnées à distance, il faut lui donner accès aux binaires Calibre, ce qu'on verra plus bas avec le module `universal-calibre`.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose installés
- Une bibliothèque Calibre déjà constituée (un dossier contenant `metadata.db` et tes fichiers ebooks), ou un dossier vide que tu rempliras ensuite
- Un reverse proxy pour l'exposition HTTPS si tu comptes accéder à ta bibliothèque hors de ton réseau local
- 1 cœur CPU et 512 Mo de RAM suffisent largement, davantage si tu actives la conversion de formats

Si Docker Compose t'est encore flou, passe par mon [guide Docker pour débutants](/docker-debutant-services-auto-heberger/) avant de continuer.

## Installer calibre web docker avec Docker Compose

Crée un dossier dédié :

```bash
mkdir -p ~/calibre-web && cd ~/calibre-web
```

Voici le `docker-compose.yml` complet pour calibre web docker, basé sur l'image officielle maintenue par linuxserver :

```yaml
services:
  calibre-web:
    image: lscr.io/linuxserver/calibre-web:latest
    container_name: calibre-web
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Paris
      - DOCKER_MODS=linuxserver/mods:universal-calibre
    volumes:
      - ./config:/config
      - /chemin/vers/ta/bibliotheque:/books
    ports:
      - "8083:8083"
    restart: unless-stopped
```

Quelques précisions :

- `PUID` et `PGID` : récupère les tiens avec `id $USER`. Le conteneur doit pouvoir lire et écrire dans `/books` avec les mêmes droits que ton utilisateur hôte.
- `./config` : stocke la base interne de Calibre-Web (utilisateurs, paramètres, cache de couvertures). Sans ce volume, tu perds toute ta configuration au redémarrage.
- `/chemin/vers/ta/bibliotheque:/books` : pointe vers ton dossier Calibre existant, celui qui contient `metadata.db`. Si tu n'as pas encore de bibliothèque, pointe vers un dossier vide, Calibre-Web proposera de la créer.
- `DOCKER_MODS=linuxserver/mods:universal-calibre` : installe les binaires Calibre dans le conteneur pour activer la conversion de formats. Disponible uniquement en x86-64, retire la ligne sur ARM.

Lance le conteneur :

```bash
docker compose up -d
```

Vérifie qu'il tourne :

```bash
docker ps | grep calibre-web
```

Ouvre `http://<ip-du-serveur>:8083`. Identifiants par défaut : `admin` / `admin123`. **Change ce mot de passe tout de suite**, c'est la première chose à faire après le premier login.

## Configuration initiale

### Pointer vers ta bibliothèque

Au premier lancement, Calibre-Web te demande le chemin de ta base Calibre. Dans l'interface, c'est `/books` (le chemin interne du conteneur, pas ton chemin hôte). Si `metadata.db` existe déjà à cet endroit, Calibre-Web l'importe directement avec tous tes livres, tags et métadonnées.

### Créer des comptes utilisateurs

Va dans **Admin > Gérer les utilisateurs**. Chaque compte peut avoir des droits distincts : lecture seule, upload, édition de métadonnées, administration. Pratique si toute la famille partage le même serveur mais que tu veux garder le contrôle sur qui peut modifier la bibliothèque.

### Activer le flux OPDS

Le flux OPDS se trouve sous `/opds`. Dans une appli de lecture mobile compatible (KyBook sur iOS, Moon+ Reader sur Android), ajoute une nouvelle bibliothèque OPDS avec l'URL `http://ton-domaine/opds` et tes identifiants. Tu retrouves alors toute ta collection, triable et téléchargeable, directement depuis l'appli.

### Synchronisation Kobo

Dans **Admin > Configuration de base**, active la synchronisation Kobo. Chaque utilisateur reçoit un jeton à entrer dans les paramètres de sa liseuse. Une fois configurée, la liseuse synchronise automatiquement les nouveaux livres ajoutés à ta bibliothèque, et remonte même la progression de lecture.

## Reverse proxy avec Caddy

Exposer le port 8083 brut sur Internet n'a aucun intérêt sans HTTPS. Voici la config Caddy minimale :

```
calibre.tondomaine.com {
  reverse_proxy localhost:8083
}
```

Avec Traefik, ajoute les labels suivants au service :

```yaml
services:
  calibre-web:
    image: lscr.io/linuxserver/calibre-web:latest
    container_name: calibre-web
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Paris
    volumes:
      - ./config:/config
      - /chemin/vers/ta/bibliotheque:/books
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.calibreweb.rule=Host(`calibre.tondomaine.com`)"
      - "traefik.http.routers.calibreweb.entrypoints=websecure"
      - "traefik.http.routers.calibreweb.tls.certresolver=letsencrypt"
    networks:
      - traefik

networks:
  traefik:
    external: true
```

## Alimenter sa bibliothèque au quotidien

Une fois Calibre-Web en place, la question devient : comment faire grossir la collection sans repasser par un PC. Deux approches courantes.

Première option, l'upload direct : dans l'interface, un utilisateur avec les droits suffisants peut uploader un fichier EPUB ou PDF, Calibre-Web l'intègre à la base et en extrait les métadonnées disponibles. Pratique pour ajouter un document isolé, moins pour gérer un flux régulier.

Deuxième option, pour les ebooks libres de droits ou tes propres publications récupérées en lot : passe par un client torrent dédié comme [Transmission](/transmission-docker-client-torrent/), qui dépose les fichiers dans un dossier surveillé, puis synchronise ce dossier vers `/books`. Reste dans le cadre légal : domaine public, licences libres, ou tes propres fichiers.

Pour organiser les fichiers avant import, qu'il s'agisse de trier des PDF scannés ou de renommer un lot d'EPUB récupérés en vrac, [File Browser](/filebrowser-docker-gestionnaire-fichiers/) fait un bon sas intermédiaire : une interface web simple pour manipuler les fichiers côté serveur avant de les pousser dans ta bibliothèque Calibre.

## Sauvegarde et persistance

Deux dossiers comptent : `config` (comptes, paramètres, cache) et ton dossier `books` (la bibliothèque elle-même, avec `metadata.db`). Une sauvegarde basique :

```bash
tar czf calibre-web-backup-$(date +%F).tar.gz config/
```

Le dossier `books` mérite un traitement à part : il grossit vite et contient l'essentiel de la valeur (tes fichiers ebooks). Si tu as déjà [Duplicati](/duplicati-docker-sauvegarde/) en place pour tes autres services, ajoute simplement ce dossier à sa politique de sauvegarde chiffrée. C'est le genre de collection qu'on reconstitue difficilement si elle disparaît, autant la traiter comme prioritaire au même titre que tes photos ou tes documents.

## Sécurité : les bonnes pratiques

Exposer calibre web docker sur Internet sans précaution revient à publier ta bibliothèque et tes identifiants admin à n'importe qui scanne le port 8083.

**1. Change les identifiants par défaut immédiatement.** `admin` / `admin123` est connu de tout le monde, y compris des scanners automatiques qui parcourent Internet.

**2. Ne jamais exposer le port 8083 directement.** Reverse proxy avec HTTPS, systématiquement, si l'accès dépasse ton réseau local.

**3. Limite les droits par compte.** Donne l'upload et l'édition uniquement aux comptes qui en ont vraiment besoin. Un compte lecture seule suffit pour la majorité des usages familiaux.

**4. Mets à jour régulièrement.**

```bash
docker compose pull && docker compose up -d
```

L'image linuxserver reçoit des mises à jour régulières, un pull mensuel suffit largement pour un usage domestique.

## Dépannage courant

**La conversion de formats ne fonctionne pas**
Vérifie que `DOCKER_MODS=linuxserver/mods:universal-calibre` est bien présent dans ton `docker-compose.yml`, et que tu es sur une architecture x86-64. Sur ARM, ce module n'est pas disponible, et la conversion reste indisponible dans le conteneur.

**Les couvertures ne s'affichent pas**
Vérifie les permissions du dossier `books`. Le conteneur doit pouvoir lire les fichiers avec le `PUID`/`PGID` que tu as défini. Teste avec :

```bash
docker exec -it calibre-web ls -la /books
```

**La base metadata.db n'est pas détectée**
Assure-toi que le fichier `metadata.db` se trouve directement à la racine du volume monté sur `/books`, pas dans un sous-dossier. Calibre-Web cherche à cet emplacement précis.

**Le conteneur redémarre en boucle**
Vérifie les logs :

```bash
docker logs calibre-web
```

Le plus souvent, c'est un problème de permissions sur `/config` qui empêche l'écriture de la base interne.

## Conclusion

Calibre web docker fait une chose, et la fait bien : transformer une bibliothèque Calibre statique en service accessible depuis n'importe quel appareil de la maison, sans dépendre d'un cloud tiers ni d'un format propriétaire. Une image Docker, deux volumes, et ta collection d'ebooks devient consultable depuis ta liseuse, ta tablette ou le navigateur de ton salon.

Ce qui en fait un bon candidat pour débuter l'auto-hébergement de contenu personnel, c'est sa simplicité d'exploitation : pas de base de données externe à gérer, une configuration qui tient dans un seul fichier Compose, et une maintenance qui se résume à un pull occasionnel. Associe-le à une politique de sauvegarde sérieuse sur le dossier `books`, et ta bibliothèque survit à n'importe quelle panne de disque.
