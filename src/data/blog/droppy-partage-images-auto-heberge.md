---
title: "Droppy Docker : partage d'images auto-hébergé léger"
description: "Droppy Docker : déploie un partage d'images auto-hébergé léger. Alternative à Imgur, installation en 5 min avec Docker Compose. Guide complet."
pubDatetime: "2026-07-17T08:00:00.000Z"
modDatetime: "2026-07-17T08:00:00.000Z"
author: Brandon Visca
tags:
  - docker
  - auto-hebergement
  - debutant
featured: false
draft: false
focusKeyword: droppy docker
ogImage: "" 
---
> 💡 **TL;DR**
> - Droppy est un serveur de partage d'images auto-hébergé, ultra-léger et open-source
> - Une image Docker, un volume pour les fichiers, et tu as ton propre Imgur privé en 5 minutes
> - Parfait pour héberger des screenshots, des memes, des photos de documentation sans dépendre d'un service tiers
> - Docker Compose complet + reverse proxy Caddy inclus ci-dessous

## Table des matières

## Pourquoi auto-héberger le partage d'images ?

Tu connais la routine. Tu prends un screenshot d'une erreur pour l'envoyer à un collègue. Tu uploades sur Imgur, tu copies le lien, tu l'envoies. Trois mois plus tard, Imgur a supprimé l'image pour "violation des conditions d'utilisation" (alors que c'était juste un log d'erreur Nginx). Ou pire : le service a changé de politique et ton lien est mort.

Le problème des services de partage d'images gratuits, c'est triple. D'abord, tes données ne sont pas vraiment à toi : elles vivent sur des serveurs américains, soumises à des politiques de modération opaque qui changent sans prévenir. Ensuite, les liens ne sont pas pérennes : un service qui ferme, une politique qui évolue, et toutes tes images intégrées dans des forums, des tickets ou des documentations deviennent des carrés gris. Enfin, tu nourris un modèle économique qui revend tes métadonnées (IP, user-agent, referer) à des réseaux publicitaires.

Il existe une alternative radicalement simple : **Droppy**. C'est un serveur de partage d'images auto-hébergé, open-source, qui tourne dans un conteneur Docker et qui te permet d'uploader, de visualiser et de partager tes images depuis ton propre serveur. Pas de compte obligatoire, pas de limite de taille imposée par un tiers, pas de suppression arbitraire. Tes images restent chez toi, sur ton disque, sous ton contrôle.

Dans mon [guide des services essentiels à auto-héberger avec Docker](/docker-debutant-services-auto-heberger/), je recommande de commencer par les outils qui résolvent un problème concret du quotidien. Droppy est exactement ça : il remplace Imgur, Postimage ou ImgBB par une solution que tu contrôles entièrement, et il se déploie en moins de temps qu'il ne faut pour créer un compte sur un service tiers.

## Qu'est-ce que Droppy exactement ?

Droppy est un serveur de fichiers web avec une spécialisation pour les images. Développé par silverwind, le projet est hébergé sur GitHub et distribué sous licence BSD-2-Clause. Le concept est minimaliste : tu lances le serveur, tu ouvres l'interface web, tu glisses-déposes tes images, et tu récupères un lien direct. Point final.

**Stack technique :**
- Node.js comme runtime serveur
- Interface web vanilla JavaScript, sans framework lourd
- Support du drag-and-drop natif
- Génération automatique de vignettes (thumbnails)
- Support des fichiers texte et markdown en plus des images
- Aucune base de données requise : les fichiers sont stockés directement sur le disque
- Aucune dépendance externe : pas de Redis, pas de PostgreSQL, pas de MariaDB

L'image Docker officielle `silverwind/droppy` est maintenue activement. Elle supporte amd64, arm64 et armv7. La taille de l'image est d'environ 150 Mo, le démarrage est instantané, et la consommation mémoire tourne autour de 60 Mo au repos. C'est l'un des services Docker les plus légers que je connaisse pour le partage de fichiers.

Droppy n'est pas une galerie photo. Ce n'est pas PhotoPrism avec reconnaissance faciale et carte géographique. Ce n'est pas Nextcloud avec sync multi-appareils et partage collaboratif. C'est un outil de partage rapide : tu uploades, tu récupères un lien, tu partages. Si tu cherches une solution complète pour organiser et visualiser ta bibliothèque photo, [PhotoPrism avec Docker](/photoprism-docker-galerie-photo/) reste la référence. Mais si ton besoin est juste de héberger des images rapidement et de générer des liens directs, Droppy est plus léger, plus rapide et plus simple.

## Droppy vs les alternatives : tableau comparatif

| Outil | Auto-hébergé | Docker officiel | Poids | Base de données | Partage lien direct | Vignettes |
|-------|-------------|-----------------|-------|-----------------|---------------------|-----------|
| **Droppy** | Oui | Oui (`silverwind/droppy`) | ~60 Mo RAM | Non | Oui, instantané | Oui |
| **Imgur** | Non (SaaS) | N/A | N/A | Inconnu | Oui | Oui |
| **Chevereto** | Oui | Oui (`chevereto/chevereto`) | ~256 Mo RAM | MySQL | Oui | Oui |
| **Piwigo** | Oui | Oui (`linuxserver/piwigo`) | ~512 Mo RAM | MySQL | Oui | Oui |
| **Lutim** | Oui | Oui | ~80 Mo RAM | Non | Oui, avec expiration | Non |
| **File Browser** | Oui | Oui (`filebrowser/filebrowser`) | ~20 Mo RAM | SQLite | Oui | Limité |

Mon choix pour un usage homelab : **Droppy** quand tu veux un partage d'images instantané sans base de données. Chevereto si tu veux une galerie communautaire complète avec commentaires et albums. File Browser si tu veux un gestionnaire de fichiers généraliste avec upload multi-fichiers. Pour gérer tes fichiers sur le même serveur, [File Browser avec Docker](/filebrowser-docker-gestionnaire-fichiers/) est un excellent complément.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose installés
- Un dossier pour stocker les images (SSD recommandé pour la génération de vignettes)
- Un reverse proxy pour l'exposition HTTPS (Caddy, Traefik, Nginx Proxy Manager)
- 1 cœur CPU et 256 Mo de RAM minimum (512 Mo recommandés pour la génération de vignettes)

Si tu débutes avec Docker et que tout ça te paraît flou, commence par mon article sur [les services essentiels à auto-héberger avec Docker](/docker-debutant-services-auto-heberger/). Il t'explique les bases de Docker Compose, les volumes, les reverse proxy et les bonnes pratiques. Une fois que tu as ces bases, Droppy est un excellent premier service pour te faire la main.

## Installation avec Docker Compose

Crée un dossier dédié et le fichier `docker-compose.yml` :

```bash
mkdir -p ~/droppy && cd ~/droppy
```

Voici le `docker-compose.yml` complet et fonctionnel :

```yaml
services:
  droppy:
    image: silverwind/droppy:latest
    container_name: droppy
    restart: unless-stopped
    environment:
      - TZ=Europe/Paris
    volumes:
      - ./files:/files
      - ./config:/config
    ports:
      - "8989:8989"
```

Quelques explications :

- `./files:/files` : monte le dossier local `files` dans le conteneur. C'est là que toutes les images uploadées seront stockées. Tu peux remplacer `./files` par un chemin absolu vers un disque externe ou un NAS.
- `./config:/config` : persiste la configuration de Droppy (utilisateurs, permissions, préférences). Sans ce volume, ta config disparaît au redémarrage.
- `ports: "8989:8989"` : expose Droppy sur le port 8989 de ton serveur. Change le port gauche si 8989 est déjà pris.

Lance le conteneur :

```bash
docker compose up -d
```

La première initialisation crée la configuration par défaut. Attends 5 secondes, puis vérifie que le conteneur tourne :

```bash
docker ps | grep droppy
```

Ouvre ton navigateur à l'adresse `http://<ip-du-serveur>:8989`. Tu devrais voir l'interface de Droppy avec un dossier vide et une zone de drop au centre.

## Configuration initiale et création d'utilisateurs

Par défaut, Droppy crée un compte administrateur au premier démarrage. Les identifiants par défaut sont affichés dans les logs du conteneur. Récupère-les :

```bash
docker logs droppy | grep -i "user\|password\|login"
```

**Immédiatement après le premier lancement, change le mot de passe par défaut.** Connecte-toi avec les identifiants affichés, clique sur l'icône utilisateur en haut à droite, et définis un nouveau mot de passe fort.

Pour créer des utilisateurs additionnels (si tu veux partager l'accès avec ta famille ou ton équipe), édite le fichier `config/config.json` ou utilise l'interface web. Chaque utilisateur a son propre dossier home dans `/files`. Les permissions sont gérées par un système simple de rôles : admin (tout voir, tout modifier) et user (son dossier uniquement).

Voici un exemple de configuration personnalisée dans `config/config.json` :

```json
{
  "listeners": [
    {
      "host": ["0.0.0.0"],
      "port": 8989,
      "protocol": "http"
    }
  ],
  "public": false,
  "timestamps": true,
  "linkLength": 5,
  "logLevel": 2,
  "maxFileSize": 0,
  "updateInterval": 1000,
  "pollingInterval": 0,
  "keepAlive": 20000,
  "allowFrame": false,
  "readInterval": 1000,
  "writeInterval": 1000,
  "keepPreview": false,
  "uploadTimeout": 86400000,
  "ignorePatterns": [],
  "watch": true,
  "db": "./db"
}
```

Les options importantes :
- `"public": false` : force l'authentification. Mets `true` si tu veux un accès public sans login (utile pour un partage ouvert, mais déconseillé sans reverse proxy et rate limiting).
- `"maxFileSize": 0` : aucune limite de taille de fichier. Tu peux définir une limite en octets si nécessaire.
- `"linkLength": 5` : longueur des liens de partage générés. Augmente si tu crains les collisions.

## Utilisation au quotidien

L'interface de Droppy est volontairement minimaliste. Voici comment l'utiliser efficacement :

**Uploader une image**
Glisse-dépose ton fichier dans la zone centrale, ou clique sur le bouton upload. L'image est immédiatement disponible avec un lien direct.

**Récupérer le lien direct**
Clique droit sur une image → "Copy link". Le lien est de la forme `https://ton-domaine.com/!/nom-du-fichier`. Ce lien pointe directement vers le fichier, sans interface web. Parfait pour les forums, les tickets, les documentations Markdown.

**Prévisualiser une image**
Clique sur le nom du fichier. Droppy affiche une vignette et permet de naviguer entre les images du dossier avec les flèches du clavier.

**Créer un dossier**
Clique sur l'icône dossier en haut à gauche. Les dossiers te permettent d'organiser tes images par projet, par date ou par catégorie.

**Renommer, déplacer, supprimer**
Clique droit sur un fichier pour accéder au menu contextuel. Les opérations sont instantanées car il n'y a pas de base de données à mettre à jour.

**Partager un dossier entier**
Sélectionne un dossier, clique sur "Share". Droppy génère un lien public vers le contenu du dossier. Tu peux révoquer le partage à tout moment.

## Reverse proxy avec Caddy

Exposer Droppy en HTTP pur sur Internet, c'est comme laisser ta porte d'entrée ouverte avec une pancarte "Entrez". Il faut du HTTPS. Voici la configuration Caddy complète :

```
droppy.tondomaine.com {
  reverse_proxy localhost:8989
}
```

Si tu utilises Traefik, ajoute ces labels à ton service dans le `docker-compose.yml` :

```yaml
services:
  droppy:
    image: silverwind/droppy:latest
    container_name: droppy
    restart: unless-stopped
    environment:
      - TZ=Europe/Paris
    volumes:
      - ./files:/files
      - ./config:/config
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.droppy.rule=Host(`droppy.tondomaine.com`)"
      - "traefik.http.routers.droppy.entrypoints=websecure"
      - "traefik.http.routers.droppy.tls.certresolver=letsencrypt"
    networks:
      - traefik

networks:
  traefik:
    external: true
```

Avec cette config, Droppy est accessible via `https://droppy.tondomaine.com` avec un certificat Let's Encrypt auto-renouvelé. Le port 8989 n'est plus exposé directement, tout passe par Traefik.

## Sauvegarde et persistance

Droppy stocke tout dans deux dossiers : `files` (les images) et `config` (la configuration et la base SQLite des utilisateurs). La sauvegarde est donc triviale :

```bash
# Sauvegarde complète
tar czf droppy-backup-$(date +%F).tar.gz files/ config/

# Restauration
tar xzf droppy-backup-2026-07-17.tar.gz
```

Si tu utilisons un outil de backup automatique comme Duplicati ou Restic, ajoute simplement les dossiers `files` et `config` à ta politique de sauvegarde. Pas de base de données à dumper, pas de tables à verrouiller. C'est l'un des avantages majeurs de Droppy par rapport à des solutions comme Chevereto ou Piwigo.

## Sécurité : les bonnes pratiques

Même si Droppy est un outil simple, quelques règles de sécurité s'imposent :

**1. Ne jamais exposer le port 8989 directement sur Internet**
Toujours passer par un reverse proxy avec HTTPS. Caddy et Traefik gèrent ça en deux lignes.

**2. Changer les identifiants par défaut immédiatement**
Le compte admin par défaut est un risque. Change le mot de passe dès le premier lancement.

**3. Limiter la taille des uploads si nécessaire**
Dans `config.json`, définis `"maxFileSize": 104857600` pour limiter à 100 Mo par fichier. Ça évite que quelqu'un uploade un fichier de 10 Go par erreur.

**4. Activer l'authentification**
Garde `"public": false` sauf si tu veux explicitement un accès anonyme. Même dans ce cas, ajoute un rate limiting côté reverse proxy pour éviter l'abus.

**5. Restreindre l'accès par IP si possible**
Si Droppy est destiné à un usage interne uniquement, configure ton reverse proxy pour n'accepter que les connexions depuis ton réseau local ou ton VPN.

**6. Mettre à jour régulièrement**
```bash
docker compose pull && docker compose up -d
```
L'image `silverwind/droppy:latest` est mise à jour régulièrement. Un pull hebdomadaire suffit.

## Dépannage courant

**Les vignettes ne se génèrent pas**
Vérifie que le conteneur a assez de RAM. La génération de thumbnails nécessite de la mémoire pour les images grandes. Augmente la limite mémoire du conteneur si nécessaire :

```yaml
services:
  droppy:
    deploy:
      resources:
        limits:
          memory: 512M
```

**L'upload échoue sur les fichiers lourds**
Vérifie que `maxFileSize` dans `config.json` est à 0 (illimité) ou supérieur à la taille de ton fichier. Vérifie aussi l'espace disque disponible dans le volume `files`.

**Le conteneur redémarre en boucle**
Vérifie les permissions du dossier `config`. Droppy doit pouvoir écrire dans ce dossier. Corrige avec :

```bash
chmod 755 config files
chown 1000:1000 config files
```

**Les liens de partage ne fonctionnent pas derrière le reverse proxy**
Vérifie que le reverse proxy transmet bien l'en-tête `Host`. Caddy et Traefik le font par défaut, mais Nginx manuel nécessite :

```nginx
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
```

## Conclusion

Droppy est l'exemple parfait de ce que l'auto-hébergement fait de mieux : prendre un service quotidien banal (héberger une image et générer un lien), le déployer chez soi en quelques minutes, et récupérer le contrôle total sur ses données. Pas de compte à créer chez un tiers, pas de limite arbitraire, pas de lien qui meurt après six mois.

Ce qui frappe avec Droppy, c'est sa radicalité. Pas de base de données, pas de dépendance externe, pas d'interface surchargée. Un conteneur Docker, un dossier sur le disque, et tu as un service de partage d'images opérationnel. C'est exactement ce genre d'outil léger qui rend l'auto-hébergement accessible à tous : tu n'as pas besoin d'être un administrateur système pour le faire tourner.

Dans un monde où chaque service cloud devient un abonnement mensuel avec des conditions qui changent tous les trimestres, héberger ses propres outils n'est pas une question de purisme technique. C'est une question de pragmatisme. Droppy te coûte zéro euro par mois, il ne disparaît pas quand un CEO décide de "pivoter", et tes screenshots de logs d'erreur restent disponibles aussi longtemps que tu le décides. C'est ça, l'indépendance numérique.
