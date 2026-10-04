---
title: "File Browser Docker : ton gestionnaire de fichiers web auto-hébergé"
description: Héberge ton propre gestionnaire de fichiers web avec File Browser sous Docker. Installation complète, config sécurisée, reverse proxy Caddy.
pubDatetime: "2026-06-12T08:00:00.000Z"
author: Brandon Visca
tags:
  - auto-hebergement
  - docker
  - linux
  - intermediaire
featured: false
draft: false
ogImage: "" 
faqs:
  - question: "File Browser remplace-t-il Nextcloud ?"
    answer: "Pour gérer et partager des fichiers, oui, avec environ 20 Mo de RAM et sans base de données externe. Pour la collaboration (édition de documents, calendrier, contacts), Nextcloud reste plus complet."
  - question: "Comment limiter un utilisateur à un seul dossier ?"
    answer: "Avec les scopes : chaque utilisateur reçoit un sous-dossier racine, par exemple /srv/photos, et ne voit rien en dehors. Ça se règle dans Paramètres > Gestion des utilisateurs ou avec la commande filebrowser users add et l'option --scope."
  - question: "Pourquoi File Browser ne peut-il pas écrire dans mes dossiers ?"
    answer: "Le conteneur tourne avec l'UID et le GID définis dans user. Si le dossier monté appartient à root, l'écriture échoue : corrige le propriétaire avec chown pour l'aligner sur cet utilisateur."
  - question: "File Browser est-il encore maintenu ?"
    answer: "Non. Le projet est archivé depuis le 1er septembre 2026 : plus de nouvelles versions ni de correctifs de sécurité. Il fonctionne toujours, mais ne l'utilise plus que sur ton réseau local ou derrière un VPN."
  - question: "Peut-on exposer File Browser directement sur internet ?"
    answer: "Non. Il ne gère pas le HTTPS lui-même et, depuis son archivage, ne reçoit plus de correctifs de sécurité. Garde-le sur ton réseau local, ou derrière un VPN et un reverse proxy avec authentification."
---
> 💡 **TL;DR**
> - File Browser est un gestionnaire de fichiers web léger, moderne et open-source
> - Une image Docker officielle, un volume monté, et tu as un navigateur de fichiers accessible depuis ton navigateur
> - Parfait alternative à FTP, SMB mal configuré ou Nextcloud quand tu veux juste gérer des fichiers
> - Docker Compose complet + reverse proxy Caddy inclus ci-dessous

> ⚠️ **Projet archivé depuis le 1er septembre 2026.** Les mainteneurs de File Browser ont publié leur dernière version et annoncent qu'il n'y aura plus aucune mise à jour, ni correctif de sécurité. Deux faiblesses connues restent ouvertes : l'exécution de commandes (à laisser désactivée, c'est le cas par défaut) et des sessions impossibles à révoquer (un jeton reste valide jusqu'à son expiration, même après déconnexion ou changement de mot de passe). Si tu l'utilises encore, garde-le sur ton réseau local ou derrière un VPN, jamais exposé directement sur Internet.

## Table des matières

## Pourquoi File Browser en 2026 ?

Tu as un serveur auto-hébergé. Tu y ranges des backups, des documents, des logs, des photos. Jusqu'ici, pour y accéder à distance, tu avais trois options :

1. **SSH + SCP/rsync** : rapide, mais relou quand tu veux juste renommer un fichier ou prévisualiser une image
2. **SMB/NFS** : galère à exposer sur Internet, bourré de failles si mal configuré
3. **Nextcloud** : overkill quand tu veux juste un navigateur de fichiers. Nextcloud, c'est excellent, mais ça consomme des ressources et ça demande une base de données juste pour lister un dossier

File Browser résout ce problème. C'est un gestionnaire de fichiers web qui tourne dans un conteneur Docker, écrit en Go, qui consomme presque rien et qui te donne une interface moderne pour télécharger, uploader, renommer, prévisualiser et partager tes fichiers. Le projet vit sur GitHub (`filebrowser/filebrowser`), avec plus de 27 000 stars et une image Docker officielle multi-architecture (amd64, arm64, armv7), mais il est archivé depuis septembre 2026 (voir l'avertissement en tête d'article).

Dans mon [guide auto-hébergement complet](/auto-hebergement-guide-complet-2025/), je parle de services qui remplacent les outils propriétaires. File Browser, c'est ton remplaçant à Google Drive quand tu veux juste gérer des fichiers sur un serveur sans la surcharge d'un cloud complet.

## File Browser vs les alternatives : tableau comparatif

| Outil | Interface web | Docker officiel | Multi-user | Partage de liens | Ressources |
|-------|---------------|-----------------|------------|------------------|------------|
| **File Browser** | Oui, moderne | Oui (`filebrowser/filebrowser`) | Oui, avec rôles | Oui, avec expiration | ~20 Mo RAM |
| **Nextcloud** | Oui, complète | Oui (`nextcloud`) | Oui, avancé | Oui | ~512 Mo+ RAM |
| **SFTPGo** | Oui, limitée | Oui (`drakkan/sftpgo`) | Oui | Oui, via API | ~50 Mo RAM |
| **CloudCommander** | Oui, basique | Oui (`coderaiser/cloudcmd`) | Non | Non | ~100 Mo RAM |
| **FTP/SFTP natif** | Non (client nécessaire) | Non | Oui | Non | Négligeable |
| **Samba (SMB)** | Non | Non | Oui | Non | Variable |

Mon choix pour un homelab Dockerisé : **File Browser** quand tu veux un navigateur de fichiers web simple et sécurisé. Nextcloud reste supérieur pour la collaboration (édition de documents, calendrier, contacts), mais File Browser gagne en légèreté et en simplicité. Pas de base de données, pas de cron, pas de cache à vider. Un binaire Go de ~20 Mo qui lit directement le système de fichiers.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose installés
- Un dossier à exposer (ton homelab, un disque externe monté, un volume Docker…)
- Un utilisateur non-root pour faire tourner le conteneur (optionnel mais recommandé)
- Un reverse proxy pour l'exposition HTTPS (Caddy, Traefik, Nginx Proxy Manager)

Si tu débutes avec Docker, j'ai listé les services indispensables à auto-héberger dans mon guide [Docker pour débutants](/docker-debutant-services-auto-heberger/). File Browser mérite clairement sa place dans cette liste.

## Installation avec Docker Compose

Crée un dossier dédié et le fichier `docker-compose.yml` :

```yaml
services:
  filebrowser:
    image: filebrowser/filebrowser:latest
    container_name: filebrowser
    restart: unless-stopped
    user: "1000:1000"
    environment:
      - FB_DATABASE=/database/filebrowser.db
    volumes:
      - /path/to/your/data:/srv
      - ./database:/database
      - ./filebrowser.json:/config/settings.json
    ports:
      - "8080:80"
```

Crée aussi le fichier de configuration `filebrowser.json` à côté du `docker-compose.yml` :

```json
{
  "port": 80,
  "baseURL": "",
  "address": "",
  "log": "stdout",
  "database": "/database/filebrowser.db",
  "root": "/srv"
}
```

Quelques explications :

- `user: "1000:1000"` : exécute le conteneur avec tes permissions (remplace par `id $USER` pour connaître ton UID/GID). Sans ça, File Browser risque de ne pas pouvoir écrire dans tes dossiers.
- `/path/to/your/data:/srv` : monte le dossier que tu veux gérer dans `/srv` du conteneur. C'est le répertoire racine visible par File Browser.
- `./database:/database` : persiste la base SQLite de File Browser (utilisateurs, règles, partages). Sinon, tout disparaît au redémarrage.
- `./filebrowser.json:/config/settings.json` : monte la config personnalisée.

Lance le conteneur :

```bash
cd /chemin/vers/filebrowser
docker compose up -d
```

Au premier démarrage, File Browser crée l'utilisateur `admin` avec un mot de passe **aléatoire**, affiché une seule fois dans les logs. Récupère-le avec `docker compose logs filebrowser`, connecte-toi sur `http://IP_DU_SERVEUR:8080` et remplace-le par le tien. Les anciennes versions utilisaient `admin` / `admin`, ce n'est plus le cas.

## Configuration avancée : multi-dossiers et utilisateurs

### Gérer plusieurs utilisateurs avec des permissions différentes

File Browser supporte les scopes : chaque utilisateur peut avoir accès à un sous-dossier spécifique. Depuis l'interface web (`Paramètres > Gestion des utilisateurs`), tu crées des utilisateurs avec un scope restreint.

Exemple : un utilisateur `photos` avec scope `/srv/photos` verra uniquement ce dossier. Un utilisateur `docs` avec scope `/srv/documents` n'aura pas accès aux photos.

### Commandes CLI pour créer un utilisateur sans passer par la UI

File Browser expose une CLI via Docker :

```bash
docker exec -it filebrowser ./filebrowser users add utilisateur motdepasse --scope=/srv/documents --perm.create --perm.delete --perm.download --perm.modify
```

### Montage de plusieurs volumes

Si tu veux exposer plusieurs dossiers du système hôte, tu as deux options :

**Option A : un dossier parent commun**

Monte un dossier parent contenant des liens symboliques :

```yaml
    volumes:
      - /media/data:/srv
```

Sur l'hôte :

```bash
mkdir -p /media/data/{documents,photos,downloads}
```

**Option B : plusieurs sous-dossiers montés séparément**

File Browser ne supporte pas nativement plusieurs roots. Solution : monter un dossier parent ou utiliser des bind mounts union. Le plus simple reste de monter un dossier parent unique.

## Sécuriser File Browser

### 1. Changer le mot de passe admin par défaut

C'est la base. Connecte-toi avec `admin` et le mot de passe affiché dans les logs au premier démarrage, va dans `Paramètres > Profil`, et change-le.

### 2. Ne jamais exposer le port brut sur Internet

File Browser ne gère pas le HTTPS natif. Ne expose jamais le port 8080 directement sur Internet. Utilise un reverse proxy avec TLS.

### 3. Activer l'authentification

Par défaut, File Browser demande un login. Si tu veux un accès public en lecture seule, tu peux créer un utilisateur sans mot de passe avec des permissions limitées, mais c'est à éviter sur Internet.

### 4. Limiter les permissions du conteneur

Ajoute ces options de sécurité dans le `docker-compose.yml` :

```yaml
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - SETGID
      - SETUID
```

### 5. Backup de la base de données

La base SQLite est dans `./database/filebrowser.db`. Si tu veux sauvegarder tes utilisateurs et règles, inclue ce fichier dans tes backups. Si tu veux sauvegarder tes fichiers hébergés, j'ai publié un guide sur [Duplicati pour des backups chiffrés](/duplicati-docker-sauvegarde/).

## Reverse proxy avec Caddy

Pour exposer File Browser en HTTPS avec un joli nom de domaine, voici la config Caddy à ajouter dans ton `Caddyfile` :

```caddy
files.tondomaine.com {
    reverse_proxy filebrowser:80
}
```

Assure-toi que le conteneur File Browser et Caddy sont sur le même réseau Docker. Si tu utilises Docker Compose séparés, crée un réseau externe :

```yaml
networks:
  caddy:
    external: true
```

Et ajoute dans le service File Browser :

```yaml
    networks:
      - caddy
```

Pour exposer File Browser en HTTPS, tu peux utiliser Caddy comme reverse proxy, j'en parle dans mon guide dédié au [reverse proxy Caddy sous Docker](/caddy-docker-reverse-proxy-guide/).

Avec Caddy, tu obtiens automatiquement un certificat Let's Encrypt, du HTTPS forcé, et tu peux ajouter des headers de sécurité si nécessaire.

## Commandes utiles au quotidien

| Commande | Description |
|----------|-------------|
| `docker compose logs -f filebrowser` | Voir les logs en temps réel |
| `docker exec -it filebrowser ./filebrowser users ls` | Lister les utilisateurs en CLI |
| `docker exec -it filebrowser ./filebrowser users update admin -p "nouveaumdp"` | Changer le mot de passe admin en CLI |
| `docker compose down && docker compose up -d` | Redémarrer le conteneur |
| `docker exec -it filebrowser sh` | Shell dans le conteneur |

## Cas d'usage concrets

### Partager rapidement un fichier depuis ton serveur

Tu as un ISO Debian à envoyer à un collègue ? Glisse-le dans le dossier géré par File Browser, clique droit sur le fichier, « Partager », et tu obtiens un lien direct avec une URL propre. Pas besoin de configurer un serveur FTP ou d'ouvrir des ports supplémentaires. Si tu cherches un outil dédié uniquement au partage d'images avec génération de liens directs, j'ai aussi publié un guide sur [Droppy avec Docker](/droppy-partage-images-auto-heberge/), un serveur de partage d'images ultra-léger sans base de données.

### Gérer les fichiers d'un serveur sans interface graphique

Tu administres un VPS Debian headless. File Browser te donne une interface graphique pour télécharger des logs, uploader des scripts, renommer des dossiers, tout ça depuis ton téléphone si besoin.

### Remplacer l'accès SMB mal sécurisé

SMB sur Internet, c'est une mauvaise idée. File Browser via HTTPS derrière un reverse proxy, c'est propre, sécurisé et ça fonctionne depuis n'importe quel navigateur.

## Dépannage rapide

**File Browser ne voit pas mes fichiers ou ne peut pas écrire**

Vérifie les permissions du dossier monté. Le conteneur tourne avec l'UID/GID que tu as défini. Si le dossier appartient à root, File Browser ne pourra pas écrire.

```bash
ls -la /path/to/your/data
chown -R 1000:1000 /path/to/your/data
```

**La base de données est verrouillée ou corrompue**

Arrête le conteneur, supprime `./database/filebrowser.db` (tu perdras les utilisateurs), et relance. File Browser recrée la base avec un utilisateur `admin` et un nouveau mot de passe aléatoire, à récupérer dans les logs.

```bash
docker compose down
rm ./database/filebrowser.db
docker compose up -d
```

**Je veux changer le port d'écoute interne**

Modifie le `filebrowser.json` et redémarre. Mais garde en tête que le port dans `docker-compose.yml` (ex: `8080:80`) mappe le port externe 8080 vers le port interne 80.

## Conclusion

File Browser, c'est l'outil qu'il te manquait si tu trouvais Nextcloud trop lourd et FTP trop archaïque. En une dizaine de lignes de Docker Compose, tu as un gestionnaire de fichiers web moderne. Mais le projet étant archivé et sans correctifs de sécurité, réserve-le désormais à ton réseau local ou à un accès par VPN.

Il consomme moins de ressources qu'un onglet Chrome, il demande zéro base de données externe, et il fait exactement ce qu'on lui demande : gérer des fichiers. Pour l'auto-hébergement, c'est exactement ce genre d'outil simple et efficace qui fait la différence entre un homelab qui tourne et un homelab qui encombre.

Déploie-le, teste-le, et si tu cherches aussi à synchroniser tes fichiers automatiquement entre plusieurs appareils sans passer par un cloud, j'ai publié un guide complet sur [Syncthing avec Docker](https://brandonvisca.com/syncthing-docker-synchronisation-fichiers/).
