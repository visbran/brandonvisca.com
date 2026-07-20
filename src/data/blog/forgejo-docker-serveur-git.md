---
title: "Forgejo Docker : le fork Gitea 100% libre que tu devrais déjà utiliser"
description: "Forgejo Docker : déploie ce fork open-source de Gitea, libre et communautaire. Guide complet avec Docker Compose, comparaison et astuces."
pubDatetime: "2026-07-20T08:00:00.000Z"
modDatetime: "2026-07-20T08:00:00.000Z"
author: Brandon Visca
tags:
  - intermediaire
  - auto-hebergement
  - docker
  - git
  - homelab
  - forgejo
featured: false
draft: false
focusKeyword: forgejo docker
faqs: []
ogImage: ""
---
> 💡 **TL;DR**
> - Forgejo est un fork communautaire de Gitea, 100 % open-source sous licence copyleft, géré par une fondation indépendante
> - Forgejo Docker : container officiel `codeberg.org/forgejo/forgejo` (≈300 Mo, compatible arm64 et amd64)
> - Mêmes fonctionnalités que Gitea : repos Git, pull requests, issues, Actions CI/CD, packages
> - Docker Compose complet ci-dessous avec SQLite ou PostgreSQL + volume persistant
> - Migration depuis Gitea en quelques clics via l'interface web

## Table des matières

## Forgejo Docker : pourquoi un autre serveur Git ? Gitea ne suffisait pas ?

Tu as peut-être déjà lu mon guide sur [Gitea avec Docker](/gitea-serveur-git-docker-auto-hebergement/). C'est un excellent serveur Git : léger, rapide, open-source. Mais en octobre 2022, la situation a changé. Gitea Inc., la société derrière le projet, a signé un accord de licence propriétaire avec une entreprise commerciale. L'objectif affiché était de financer le développement. Le problème : cette licence propriétaire empêchait la communauté de contribuer sur certains aspects, et posait la question de la gouvernance à long terme.

Résultat : une partie de la communauté a fait ce que font les gens intelligents quand un projet open-source se fait capturer par des intérêts commerciaux. Ils ont forké.

Forgejo est né de cette scission. Le nom vient du basque (*forja* = forge, *jo* = aller vers). L'idée : une forge logicielle qui avance vraiment vers la communauté, pas vers un business plan.

**Ce que Forgejo apporte de plus que Gitea :**
- Gouvernance par une fondation indépendante (Codeberg e.V.), pas une startup
- Licence 100 % copyleft (GPL et AGPL selon les composants), pas de clause propriétaire cachée
- Feuille de route communautaire, pas dictée par des investisseurs
- Compatible à 99 % avec Gitea : mêmes API, même interface, même base de données
- Actions CI/CD natives, registry de packages, et mirror de repos intégrés

En clair, si tu aimes Gitea mais que tu préfères soutenir un projet dont le code appartient vraiment à la communauté, Forgejo est ton nouvel ami.

## Qu'est-ce que Forgejo exactement ?

Forgejo est une forge logicielle auto-hébergée, forkée depuis le code de Gitea. Elle reprend l'intégralité des fonctionnalités de son parent, avec une gouvernance différente et une orientation résolument communautaire.

**Ce qu'il fait nativement :**
- Hébergement de dépôts Git (publics et privés, sans limite)
- Pull requests avec revue de code, commentaires inline et approbations
- Issues avec labels, milestones, assignations et templates
- Wiki par projet avec édition en Markdown
- Actions CI/CD (workflows YAML compatibles GitHub Actions)
- Registry de packages (Docker, npm, Maven, PyPI, Go, etc.)
- Mirror de dépôts externes (GitHub, GitLab, etc.)
- Authentification LDAP, SAML, OAuth et OpenID Connect
- Interface web épurée, responsive, thème clair/sombre
- API REST complète pour l'automatisation

La différence avec GitLab ? Forgejo consomme environ 300 Mo de RAM au repos. GitLab demande 4 Go minimum juste pour démarrer. Sur un Raspberry Pi 4 ou un VPS à 3 €/mois, Forgejo tourne comme sur des roulettes. GitLab te ferait pleurer avant même d'avoir ouvert la page d'admin.

## Forgejo vs Gitea : le match en 3 rounds

|| Critère | Forgejo | Gitea |
||---------|---------|-------|
|| Licence | GPL/AGPL (copyleft) | MIT + clause propriétaire pour Gitea Inc. |
|| Gouvernance | Fondation Codeberg e.V. | Gitea Inc. (société commerciale) |
|| Feuille de route | Communautaire | Dictée par les intérêts commerciaux |
|| Fonctionnalités | Identiques + améliorations communautaires | Identiques |
|| Container officiel | `codeberg.org/forgejo/forgejo` | `gitea/gitea` |
|| Migration depuis Gitea | Bouton "Migrate" natif | N/A |
|| Actions CI/CD | Oui, intégrées | Oui, intégrées |

**Verdict** : Sur le plan technique, Forgejo et Gitea sont quasi identiques. Forgejo gagne sur la philosophie et la gouvernance. Si la souveraineté du code te tient à cœur, le choix est vite fait.

## Prérequis

Avant de balancer le `docker compose up`, vérifie ces quelques points :

- Un serveur Linux (Debian, Ubuntu, AlmaLinux, peu importe) avec Docker et Docker Compose installés
- 1 Go de RAM minimum (2 Go recommandés si tu actives les Actions CI/CD)
- Un volume de stockage persistant pour les données Git
- Un nom de domaine ou un sous-domaine pointant vers ton serveur (optionnel mais vivement conseillé pour le HTTPS)
- Un reverse proxy pour le HTTPS (Caddy recommandé, [j'ai écrit un guide complet](/caddy-docker-reverse-proxy-guide/))

Forgejo fonctionne aussi sur ARM64, donc un Raspberry Pi 4 avec 4 Go de RAM est parfaitement capable de gérer une forge personnelle ou une petite équipe.

## Installation avec Docker Compose

Crée un dossier dédié et un fichier `docker-compose.yml` :

```bash
mkdir -p ~/forgejo && cd ~/forgejo
```

**Docker Compose minimal (SQLite) :**

```yaml
version: "3.8"

services:
  forgejo:
    image: codeberg.org/forgejo/forgejo:10
    container_name: forgejo
    restart: unless-stopped
    ports:
      - "3000:3000"
      - "2222:22"
    environment:
      - USER_UID=1000
      - USER_GID=1000
      - FORGEJO__database__DB_TYPE=sqlite3
      - FORGEJO__database__PATH=/data/gitea.db
    volumes:
      - ./forgejo-data:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
```

**Docker Compose avec PostgreSQL (recommandé pour la production) :**

```yaml
version: "3.8"

services:
  forgejo:
    image: codeberg.org/forgejo/forgejo:10
    container_name: forgejo
    restart: unless-stopped
    depends_on:
      - db
    ports:
      - "3000:3000"
      - "2222:22"
    environment:
      - USER_UID=1000
      - USER_GID=1000
      - FORGEJO__database__DB_TYPE=postgres
      - FORGEJO__database__HOST=db:5432
      - FORGEJO__database__NAME=forgejo
      - FORGEJO__database__USER=forgejo
      - FORGEJO__database__PASSWD=super_mot_de_passe_a_changer
    volumes:
      - ./forgejo-data:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    networks:
      - forgejo-net

  db:
    image: postgres:16-alpine
    container_name: forgejo-db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=forgejo
      - POSTGRES_PASSWORD=super_mot_de_passe_a_changer
      - POSTGRES_DB=forgejo
    volumes:
      - ./postgres-data:/var/lib/postgresql/data
    networks:
      - forgejo-net

networks:
  forgejo-net:
    driver: bridge
```

**Quelques explications sur les choix techniques :**
- `USER_UID=1000` et `USER_GID=1000` : Forgejo tourne avec un utilisateur non-root. Adapte selon ton système (`id $(whoami)` pour connaître ton UID/GID)
- Le port `3000` est l'interface web, le port `22` est le SSH Git interne au conteneur. On mappe le `2222` externe vers le `22` interne pour éviter les conflits avec le SSH du serveur hôte
- SQLite suffit pour une utilisation solo ou une petite équipe. PostgreSQL est plus robuste pour la production
- Les volumes `./forgejo-data` et `./postgres-data` assurent la persistance. Ne les perds pas, sinon tes repos disparaissent dans les limbes

Lance le tout :

```bash
docker compose up -d
```

Attends 10-20 secondes que la base s'initialise, puis ouvre `http://IP_DU_SERVEUR:3000` dans ton navigateur.

## Configuration initiale

La première fois que tu ouvres Forgejo, un wizard d'installation apparaît. Remplis les champs suivants :

- **Type de base de données** : SQLite (si tu as utilisé la config minimale) ou PostgreSQL
- **Chemin du fichier** : `/data/gitea.db` (laisser par défaut)
- **Hôte du serveur** : `localhost` ou l'IP de ton serveur
- **Nom du site** : ce que tu veux (ex: "Forgejo de Brandon")
- **Port de base** : `3000` (laisser par défaut)
- **Port SSH du serveur** : `22` (attention : c'est le port **interne** au conteneur, pas celui du serveur hôte)
- **URL de base** : `https://git.tondomaine.com` ou `http://IP:3000`
- **Créer un compte administrateur** : coche la case et choisis un nom d'utilisateur, email et mot de passe costaud

Clique sur "Installer Forgejo". L'opération prend une dizaine de secondes. Une fois terminée, tu arrives sur ton tableau de bord.

**Première chose à faire** : connecte-toi avec le compte admin créé, puis va dans **Administration > Configuration > Serveur** et vérifie que l'URL de base est correcte. Si tu as prévu un reverse proxy, mets l'URL publique (HTTPS) ici.

## Reverse proxy avec Caddy (optionnel mais conseillé)

Exposer Forgejo en HTTP pur sur le port 3000, c'est un peu comme laisser ta porte d'entrée ouverte avec un panneau "Entrez, y'a du Git dedans". Mieux vaut mettre un joli HTTPS devant.

Si tu utilises Caddy (et tu devrais, [j'ai expliqué pourquoi ici](/caddy-docker-reverse-proxy-guide/)), ajoute ça à ton `Caddyfile` :

```caddyfile
git.tondomaine.com {
    reverse_proxy forgejo:3000
}
```

Si Caddy est dans un autre réseau Docker, assure-toi que Forgejo et Caddy partagent un réseau commun, ou expose Forgejo sans le mapping de port et laisse Caddy gérer l'accès via le réseau Docker interne.

Avec Traefik, ajoute ces labels à ton service Forgejo :

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.forgejo.rule=Host(`git.tondomaine.com`)"
  - "traefik.http.routers.forgejo.tls.certresolver=letsencrypt"
  - "traefik.http.services.forgejo.loadbalancer.server.port=3000"
```

## Connexion en SSH pour Git

Pour cloner et pusher en SSH, tu dois configurer le port correctement. Sur la page d'accueil de chaque dépôt, Forgejo affiche l'URL SSH.

Avec le mapping `2222:22` dans Docker Compose, les commandes ressemblent à ça :

```bash
git clone ssh://git@tondomaine.com:2222/utilisateur/mon-repo.git
```

Si tu veux utiliser le port 22 standard, deux options :
1. Désactive le SSH du serveur hôte (`systemctl stop ssh`) et mappe `22:22`, mais tu perds l'accès SSH à ta machine
2. Utilise un reverse proxy SSH comme `traefik` ou configure un sous-domaine dédié avec un autre port

La solution la plus simple : garde le `2222` et ajoute un alias dans ton `~/.ssh/config` :

```sshconfig
Host forgejo
    HostName tondomaine.com
    Port 2222
    User git
    IdentityFile ~/.ssh/id_ed25519
```

Ensuite, clone simplement avec `git clone forgejo:utilisateur/mon-repo.git`.

## Actions CI/CD : le CI intégré

Forgejo embarque un système d'actions CI/CD inspiré de GitHub Actions. Tu peux définir des workflows dans des fichiers `.forgejo/workflows/` à la racine de tes dépôts.

Exemple de workflow simple qui lance des tests à chaque push :

```yaml
name: Tests

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lancer les tests
        run: make test
```

Pour que ça marche, tu dois activer les runners dans l'interface d'administration. Va dans **Administration > Actions > Runners**, puis crée un runner auto-hébergé. Forgejo te fournit un token et une commande à exécuter. Le runner peut tourner dans un conteneur Docker séparé ou directement sur le serveur.

Les runners consomment des ressources. Si tu n'as que 2 Go de RAM sur ton serveur, limite-toi à un runner et des workflows légers. Sinon, ton serveur va ramer comme un vieux portable sous Windows Vista.

## Migration depuis Gitea

Si tu as déjà un Gitea en place et que tu veux basculer vers Forgejo, la migration est presque insultante de simplicité :

1. Depuis l'interface Forgejo, va dans le menu "+" en haut à droite et choisis "Nouvelle migration"
2. Sélectionne "Gitea" comme source
3. Renseigne l'URL de ton instance Gitea, ton token d'accès, et choisis ce que tu veux importer (repos, issues, pull requests, wikis, etc.)
4. Forgejo clone tout automatiquement

Pour une migration complète (tous les repos + utilisateurs), la méthode propre consiste à :
1. Arrêter Gitea
2. Sauvegarder le dossier `/data` de Gitea
3. Lancer Forgejo avec le **même** dossier `/data` mappé en volume
4. Forgejo détecte automatiquement la base Gitea et propose de la mettre à jour

Oui, c'est aussi simple que ça. Forgejo est conçu pour être un drop-in replacement de Gitea.

## Astuces et sécurité

**Backup régulier** : le dossier `./forgejo-data` contient tout. Sauvegarde-le avec [Duplicati](/duplicati-docker-sauvegarde/), rsync, ou tout ce que tu veux. Un repo Git sans backup, c'est un repo qui va disparaître un jour. C'est pas une question de "si", c'est une question de "quand".

**Mises à jour** : Forgejo publie des mises à jour régulières. Pour mettre à jour :

```bash
cd ~/forgejo
docker compose pull
docker compose up -d
```

**Authentification à deux facteurs** : active-la immédiatement pour le compte admin. Va dans **Paramètres > Sécurité > Authentification à deux facteurs**.

**Webhook sécurisé** : si tu utilises des webhooks pour déclencher des déploiements, protège-les avec un secret. Forgejo signe les payloads avec un HMAC-SHA256. Vérifie cette signature côté receiver.

**Limiter les inscriptions** : par défaut, Forgejo autorise les inscriptions publiques. Si c'est une forge privée, désactive ça dans **Administration > Configuration > Compte**.

**Firewall** : si tu exposes Forgejo sur Internet, bloque tout sauf les ports 443 et le port SSH Git (2222 ou 22). Pas besoin d'exposer le port 3000 directement quand tu as un reverse proxy.

## Conclusion

Forgejo, c'est Gitea avec une conscience politique. Mêmes performances, même légèreté, même simplicité de déploiement, mais avec une gouvernance qui garantit que le code restera libre pour toujours. Pas de clause commerciale cachée, pas de levée de fonds qui transformerait ton serveur Git en produit d'entrée de gamme pour une entreprise.

Déployer **Forgejo avec Docker** prend littéralement 5 minutes. Une fois en place, tu as une forge complète : repos privés, issues, pull requests, CI/CD, registry de packages, et même des wikis. Le tout sur une machine qui consomme moins de RAM qu'un onglet Chrome.

Si tu cherches un serveur Git auto-hébergé, léger, et qui ne te fera pas regretter ton choix dans deux ans quand les investisseurs débarqueront, Forgejo est la réponse. Et si tu veux comprendre comment toute cette stack Docker s'articule dans un homelab cohérent, file lire mon [guide auto-hébergement complet](/auto-hebergement-guide-complet-2025/).