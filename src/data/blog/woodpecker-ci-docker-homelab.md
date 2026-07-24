---
title: "Woodpecker CI Docker : CI/CD léger pour ton homelab"
description: "Guide woodpecker ci docker : déploie un pipeline CI/CD léger dans ton homelab avec Docker Compose, agents et workflows YAML prêts à l'emploi."
pubDatetime: "2026-07-24T08:00:00.000Z"
modDatetime: "2026-07-24T08:00:00.000Z"
author: Brandon
tags:
  - woodpecker
  - ci-cd
  - docker
  - auto-hebergement
  - intermediaire
  - devops
featured: false
draft: false
focusKeyword: woodpecker ci docker
faqs:
  - question: "Woodpecker CI est-il gratuit et open-source ?"
    answer: "Oui, Woodpecker CI est un fork open-source de Drone CI 1.0, écrit en Go et distribué sous licence Apache-2.0. Il est développé activement par la communauté sur GitHub et ne possède pas de version payante ou propriétaire."
  - question: "Quelle est la différence entre Woodpecker CI et Drone CI ?"
    answer: "Woodpecker CI est un fork communautaire de Drone CI 1.0 créé après le passage de Drone en licence propriétaire. Woodpecker conserve la syntaxe YAML originale tout en restant 100 % open-source et communautaire, alors que Drone est désormais orienté entreprise avec un modèle payant."
  - question: "Quelles forges Git sont compatibles avec Woodpecker CI ?"
    answer: "Woodpecker CI supporte nativement Gitea, Forgejo, GitHub, GitLab et Bitbucket. La configuration se fait via des variables d'environnement qui activent le driver correspondant, ce qui le rend très flexible pour un homelab."
  - question: "Combien de RAM consomme Woodpecker CI avec Docker ?"
    answer: "Une installation complète serveur + agent consomme environ 200 Mo de RAM au repos. Le serveur lui-même est un binaire Go de quelques dizaines de mégaoctets, ce qui en fait l'une des solutions CI/CD les plus légères disponibles."
ogImage: ""
---
> 💡 **TL;DR**
> - Woodpecker CI est un fork open-source de Drone CI 1.0, écrit en Go sous licence Apache-2.0
> - Serveur + agent Docker, environ 200 Mo de RAM au total, idéal pour un homelab
> - Syntaxe YAML par pipeline, compatible avec la plupart des forges Git (Gitea, Forgejo, GitHub, GitLab)
> - Docker Compose complet ci-dessous avec exemple de build et push d'image

## Table des matières

## Pourquoi Woodpecker CI dans ton homelab ?

Tu as déjà un serveur Git auto-hébergé avec [Gitea](/gitea-serveur-git-docker-auto-hebergement/) ou [Forgejo](/forgejo-docker-serveur-git/). Tu as peut-être testé Gitea Actions, mais tu cherches quelque chose de plus léger, plus direct, et qui ne nécessite pas de runner lourd à configurer. Ou tu veux simplement un CI/CD découplé de ta forge, pour garder chaque service focalisé sur un seul rôle.

**Woodpecker CI est une solution de CI/CD open-source extrêmement légère.** Contrairement à GitLab CI qui avale 4 Go de RAM rien que pour démarrer, ou à Jenkins qui fait souffrir ton SSD avec ses centaines de plugins, Woodpecker se compose d'un simple serveur et d'un ou plusieurs agents. Le tout tient dans deux conteneurs Docker et consomme moins de 200 Mo au repos.

Les points forts qui justifient l'adoption de woodpecker ci docker dans un homelab :

- **Légèreté** : le serveur est un binaire Go de quelques dizaines de mégaoctets
- **Syntaxe YAML simple** : un fichier `.woodpecker.yml` à la racine du repo suffit
- **Multi-forge** : Gitea, Forgejo, GitHub, GitLab, Bitbucket
- **Agents éphémères** : chaque pipeline s'exécute dans un conteneur Docker jetable
- **Pas de base de données lourde** : SQLite par défaut, PostgreSQL ou MySQL en option

## Qu'est-ce que Woodpecker CI exactement ?

Woodpecker CI est un projet open-source forké depuis Drone CI 1.0 (avant que Drone ne bascule en licence propriétaire). Le code est écrit en Go, distribué sous licence Apache-2.0, et développé activement par la communauté sur GitHub (`woodpecker-ci/woodpecker`).

**Ce que ça fait :**

- Déclenche des pipelines à chaque push, pull request, tag ou cron
- Exécute chaque étape dans un conteneur Docker distinct et isolé
- Supporte les services (base de données, cache) en sidecar
- Gère les secrets et les variables d'environnement par repo
- Affiche les logs en temps réel dans une interface web minimaliste
- Supporte les matrices de builds et les pipelines conditionnels
- Fournit une API REST et une CLI pour l'automatisation

**La différence avec Drone CI actuel :**

- Woodpecker est 100 % open-source et communautaire
- Drone CI est devenu propriétaire (Entreprise / Cloud payant)
- Woodpecker conserve la syntaxe YAML de Drone 1.0, donc la migration est quasi transparente
- Woodpecker évolue plus vite sur les fonctionnalités demandées par la communauté self-hosted

## Architecture serveur + agent

Woodpecker se compose de deux briques indépendantes :

**1. Le serveur (`woodpeckerci/woodpecker-server`)**
Il expose l'interface web, l'API, et communique avec ta forge Git pour récupérer les webhooks. Il stocke les métadonnées des pipelines (état, logs, configuration) dans une base SQLite, PostgreSQL ou MySQL. Il ne fait pas tourner les jobs lui-même. Il les délègue.

**2. L'agent (`woodpeckerci/woodpecker-agent`)**
C'est le worker. Il se connecte au serveur, récupère les jobs en attente, et les exécute dans des conteneurs Docker. Tu peux en lancer plusieurs agents sur des machines différentes pour répartir la charge. Chaque agent est autonome et communique avec le serveur via une API interne.

**Le flux d'exécution :**

1. Tu pousses du code sur une branche
2. La forge Git envoie un webhook au serveur Woodpecker
3. Le serveur lit le fichier `.woodpecker.yml` du repo et crée un pipeline
4. Un agent disponible récupère le job
5. Il clone le repo et exécute chaque étape dans un conteneur
6. Les logs remontent au serveur en temps réel

## Prérequis

Avant de déployer Woodpecker CI Docker, vérifie ces points :

- Un serveur Linux avec Docker et Docker Compose installés
- Au moins 1 Go de RAM disponible (serveur ~50 Mo + agent ~150 Mo selon les images)
- Une forge Git accessible en webhook (Gitea, Forgejo, GitHub, etc.)
- Un sous-domaine si tu veux exposer l'interface web en HTTPS
- Connaissances de base en Docker et YAML

Si tu n'as pas encore de serveur Git auto-hébergé, [mon guide sur Gitea Actions Docker](/gitea-actions-docker-ci-cd/) détaille une approche CI/CD intégrée, tandis que Forgejo offre [une alternative 100 % libre](/forgejo-docker-serveur-git/).

## Docker Compose complet pour woodpecker ci docker

Voici une configuration prête à l'emploi. Elle lance le serveur et un agent sur la même machine, avec SQLite comme backend.

```yaml
version: "3.8"

services:
  woodpecker-server:
    image: woodpeckerci/woodpecker-server:latest
    container_name: woodpecker-server
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - WOODPECKER_OPEN=true
      - WOODPECKER_HOST=https://ci.tondomaine.fr
      - WOODPECKER_GITEA=true
      - WOODPECKER_GITEA_URL=https://git.tondomaine.fr
      - WOODPECKER_GITEA_CLIENT=TON_CLIENT_ID
      - WOODPECKER_GITEA_SECRET=TON_CLIENT_SECRET
      - WOODPECKER_ADMIN=ton_user_gitea
      - WOODPECKER_AGENT_SECRET=une_chaine_secrete_longue_et_aleatoire
    volumes:
      - ./woodpecker-data:/var/lib/woodpecker
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    networks:
      - woodpecker

  woodpecker-agent:
    image: woodpeckerci/woodpecker-agent:latest
    container_name: woodpecker-agent
    restart: unless-stopped
    depends_on:
      - woodpecker-server
    environment:
      - WOODPECKER_SERVER=woodpecker-server:9000
      - WOODPECKER_AGENT_SECRET=une_chaine_secrete_longue_et_aleatoire
      - WOODPECKER_MAX_WORKFLOWS=2
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    networks:
      - woodpecker

networks:
  woodpecker:
    driver: bridge
```

**Explications des variables importantes :**

- `WOODPECKER_OPEN=true` : permet aux utilisateurs de s'inscrire via OAuth depuis la forge Git configurée
- `WOODPECKER_HOST` : l'URL publique de ton instance Woodpecker. Le serveur l'utilise pour générer les URLs de webhook
- `WOODPECKER_GITEA=true` : active le driver Gitea/Forgejo. Woodpecker supporte aussi `GITHUB`, `GITLAB`, `BITBUCKET`
- `WOODPECKER_GITEA_URL` : l'URL de ton instance Gitea ou Forgejo
- `WOODPECKER_GITEA_CLIENT` et `WOODPECKER_GITEA_SECRET` : le client ID et secret OAuth générés côté Gitea
- `WOODPECKER_ADMIN` : le nom d'utilisateur qui devient administrateur Woodpecker à la première connexion
- `WOODPECKER_AGENT_SECRET` : une clé partagée entre le serveur et l'agent pour l'authentification interne
- `WOODPECKER_MAX_WORKFLOWS=2` : nombre maximum de pipelines exécutés en parallèle par cet agent

Lance les services :

```bash
mkdir -p /opt/woodpecker && cd /opt/woodpecker
docker compose up -d
```

Attends 10-20 secondes, puis ouvre `http://IP_DU_SERVEUR:8000` dans ton navigateur.

## Créer l'application OAuth dans Gitea ou Forgejo

Pour que Woodpecker puisse lire tes repos et recevoir les webhooks, il faut créer une application OAuth côté forge.

**Dans Gitea / Forgejo :**

1. Connecte-toi et va dans **Paramètres > Applications > Gérer les tokens OAuth2**
2. Clique sur **Créer une application OAuth2**
3. Nom : `Woodpecker CI`
4. URI de redirection : `https://ci.tondomaine.fr/authorize`
5. Sauvegarde et récupère le **Client ID** et le **Client Secret**
6. Copie ces valeurs dans les variables `WOODPECKER_GITEA_CLIENT` et `WOODPECKER_GITEA_SECRET`
7. Redémarre Woodpecker : `docker compose restart woodpecker-server`

## Passer les secrets via un fichier `.env`

Plutôt que d'inscrire les tokens en dur dans le `docker-compose.yml`, crée un fichier `.env` :

```bash
WOODPECKER_GITEA_CLIENT=abc123...
WOODPECKER_GITEA_SECRET=def456...
WOODPECKER_AGENT_SECRET=super_secret_long_et_aleatoire_64_chars
```

Et modifie le `docker-compose.yml` :

```yaml
    environment:
      - WOODPECKER_GITEA_CLIENT=${WOODPECKER_GITEA_CLIENT}
      - WOODPECKER_GITEA_SECRET=${WOODPECKER_GITEA_SECRET}
      - WOODPECKER_AGENT_SECRET=${WOODPECKER_AGENT_SECRET}
```

N'oublie pas d'ajouter `.env` à ton `.gitignore` si tu versionnes ce dossier.

## Écrire ton premier pipeline

Les pipelines Woodpecker se définissent dans un fichier `.woodpecker.yml` à la racine du repo. La syntaxe est volontairement simple.

Voici un exemple qui teste un projet Node.js à chaque push :

```yaml
steps:
  test:
    image: node:20-alpine
    commands:
      - npm ci
      - npm test
```

**Analyse du fichier :**

- `steps` : liste des étapes du pipeline. Chaque étape s'exécute dans un conteneur Docker propre.
- `test` : le nom de l'étape. Il apparaît dans l'interface web.
- `image` : l'image Docker utilisée pour exécuter cette étape.
- `commands` : les commandes shell à exécuter, dans l'ordre.

Pousse ce fichier sur une branche :

```bash
git add .woodpecker.yml
git commit -m "feat(ci): ajoute pipeline Woodpecker"
git push origin main
```

Va dans l'interface web de Woodpecker. Si le webhook est bien configuré, le pipeline s'exécute automatiquement et tu vois les logs en temps réel.

## Pipeline Docker avancé avec build et push

Voici un exemple plus complet : à chaque push sur `main`, on build une image Docker et on la pousse vers le registry de Gitea.

```yaml
steps:
  build:
    image: docker:25-dind
    commands:
      - docker build -t git.tondomaine.fr/utilisateur/mon-repo:latest .
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock

  push:
    image: docker:25-dind
    commands:
      - docker login -u $${CI_REPO_OWNER} -p $${CI_TOKEN} git.tondomaine.fr
      - docker push git.tondomaine.fr/utilisateur/mon-repo:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    when:
      branch: main
```

**Ce qui est spécifique à Woodpecker :**

- `$${CI_REPO_OWNER}` et `$${CI_TOKEN}` : variables d'environnement injectées automatiquement par Woodpecker. La double syntaxe `$$` est nécessaire pour éviter l'interpolation par le serveur.
- `when: branch: main` : conditionne l'exécution de l'étape à la branche `main`.
- Le montage du socket Docker permet à l'étape de lancer des commandes Docker sur l'hôte. C'est la même approche que pour Gitea Actions Docker ou d'autres runners CI.

## Services sidecar dans les pipelines

Woodpecker supporte les services qui démarrent en parallèle du pipeline. C'est utile pour les tests qui nécessitent une base de données.

```yaml
steps:
  test:
    image: node:20-alpine
    commands:
      - npm ci
      - npm test
    environment:
      - DATABASE_URL=postgres://woodpecker:secret@database:5432/tests

services:
  database:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=woodpecker
      - POSTGRES_PASSWORD=secret
      - POSTGRES_DB=tests
```

Le service `database` démarre avant l'étape `test` et est accessible sur le hostname `database` depuis le conteneur du step.

## Gérer les secrets et les variables

Les pipelines ont souvent besoin de tokens API, clés de déploiement ou mots de passe. Woodpecker gère les secrets via son interface web.

**Ajouter un secret :**

1. Dans l'interface Woodpecker, va dans ton repo
2. Onglet **Secrets**
3. Clique sur **Add secret**
4. Nom : `DEPLOY_KEY`
5. Valeur : ta clé ou token
6. Coche **Images** si tu veux restreindre l'usage à certaines images Docker

**Utiliser un secret dans le pipeline :**

```yaml
steps:
  deploy:
    image: alpine:latest
    commands:
      - echo "Déploiement avec la clé $${DEPLOY_KEY}"
    secrets: [deploy_key]
```

Le secret est injecté comme variable d'environnement. Woodpecker masque automatiquement sa valeur dans les logs.

## Sécurité : ne fais pas n'importe quoi

Lancer du code arbitraire dans un agent Docker, c'est pratique mais dangereux. Quelques règles pour garder ton homelab en sécurité :

- **Ne partage pas ton agent** avec des utilisateurs non vérifiés. Un pipeline malveillant peut exécuter n'importe quelle commande via le socket Docker.
- **Limite l'accès au socket Docker** : si possible, utilise Docker-in-Docker (DinD) plutôt que le socket de l'hôte. C'est plus lourd mais mieux isolé.
- **Network policies** : isole Woodpecker dans un réseau Docker dédié. L'agent n'a pas besoin d'accéder à tous les services de ton homelab.
- **Pas de secrets en clair** : jamais de mot de passe dans le code source. Utilise toujours les secrets Woodpecker.
- **Scanner les images** : si tu build des images Docker dans tes pipelines, ajoute une étape de scan avec Trivy avant de pousser vers le registry.
- **HTTPS obligatoire** : expose Woodpecker via un reverse proxy avec HTTPS. [Caddy Docker](/caddy-docker-reverse-proxy-guide/) fait ça en quelques lignes avec renouvellement automatique Let's Encrypt.

## Monitoring et résolution des problèmes

**Le serveur ne démarre pas :**
Vérifie les logs : `docker logs woodpecker-server`. Les causes fréquentes sont une URL de forge inaccessible, un client OAuth incorrect, ou des permissions insuffisantes sur le volume de données.

**L'agent n'apparaît pas dans l'interface :**
Vérifie que `WOODPECKER_AGENT_SECRET` est identique côté serveur et agent. Vérifie aussi que les deux conteneurs partagent le même réseau Docker ou peuvent se joindre via le hostname `woodpecker-server`.

**Le pipeline reste en attente "Pending" :**
L'agent n'est pas connecté, ou `WOODPECKER_MAX_WORKFLOWS` est atteint. Vérifie les logs de l'agent : `docker logs woodpecker-agent`.

**Erreur "Cannot connect to the Docker daemon" :**
Le socket Docker n'est pas monté correctement dans le conteneur agent. Vérifie que `/var/run/docker.sock:/var/run/docker.sock` est bien dans les volumes.

**Les webhooks ne déclenchent pas les pipelines :**
Dans les paramètres du repo côté Gitea/Forgejo, vérifie que le webhook pointe bien vers `https://ci.tondomaine.fr/hook`. Teste-le manuellement depuis l'interface de la forge.

## Comparaison avec les alternatives

||| Critère | Woodpecker CI | Gitea Actions | GitLab CI/CD | GitHub Actions |
|---|---|---|---|---|---|
||| **Coût** | Gratuit (ton serveur) | Gratuit (ton serveur) | Gratuit limité, payant ensuite | Gratuit limité, payant ensuite |
||| **Hébergement** | Self-hosted | Self-hosted | Cloud ou self-hosted (lourd) | Cloud uniquement |
||| **Syntaxe** | YAML simple | YAML compatible GitHub | YAML distinct | YAML natif |
||| **Poids** | Très léger (~200 Mo) | Léger (~500 Mo avec runner) | Lourd (>4 Go) | N/A (cloud) |
||| **Base de données** | SQLite par défaut | SQLite par défaut | PostgreSQL obligatoire | N/A |
||| **Isolation** | Conteneur par step | Conteneur par job | Conteneur ou shell | Cloud |

Pour un homelab où chaque megaoctet de RAM compte, woodpecker ci docker est le compromis idéal. Il offre la puissance d'un CI/CD moderne sans la complexité et la lourdeur des solutions d'entreprise. Si tu cherches une intégration native au sein de ta forge, [Gitea Actions Docker](/gitea-actions-docker-ci-cd/) reste une excellente alternative.

## Conclusion

Woodpecker CI est l'outil de CI/CD que ton homelab mérite. Un serveur Go de quelques megaoctets, un agent Docker qui exécute tes pipelines dans des conteneurs isolés, et une syntaxe YAML si simple que tu écris ton premier pipeline en cinq minutes.

Il ne remplacera pas GitHub Actions pour un projet open-source qui a besoin de visibilité publique. Mais pour tes projets privés, tes déploiements internes, et ta forge auto-hébergée, Woodpecker CI Docker est un choix rationnel et élégant.

Si tu veux sécuriser l'accès à ton instance avec HTTPS automatique, [Caddy Docker](/caddy-docker-reverse-proxy-guide/) s'intègre en quelques lignes. Et si tu cherches à construire une stack homelab cohérente, l'association d'un serveur Git comme Forgejo avec Woodpecker CI te donne une forge logicielle complète, légère, et totalement sous ton contrôle.

Ton code mérite un pipeline qui travaille pour toi, pas une plateforme qui te facture à la minute.
