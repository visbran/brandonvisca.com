---
title: "Gitea Actions Docker : CI/CD self-hosted intégré à Gitea"
description: "Déploie Gitea Actions Docker pour un CI/CD self-hosted intégré à Gitea. Guide complet avec act_runner, workflows YAML et Docker Compose pour ton homelab."
pubDatetime: "2026-07-22T08:00:00.000Z"
modDatetime: "2026-07-22T08:00:00.000Z"
author: Brandon
tags:
  - intermediaire
  - auto-hebergement
  - docker
  - ci-cd
  - git
  - gitea
featured: false
draft: false
focusKeyword: gitea actions docker
faqs: []
ogImage: "" 
---
> 💡 **TL;DR**
> - Gitea Actions = CI/CD intégré directement dans ton serveur Git, syntaxe compatible GitHub Actions
> - Tu as besoin de deux choses : Gitea (déjà en place) + un runner `act_runner` dans un conteneur Docker
> - Les workflows vont dans `.gitea/workflows/` à la racine de chaque repo
> - Un runner Docker auto-hébergé peut builder, tester et pousser tes images sans jamais sortir de ton infrastructure
> - Budget ressources : Gitea ~300 Mo + runner ~500 Mo selon les workloads

## Table des matières

## Pourquoi un CI/CD intégré à ton serveur Git ?

Tu as déployé [Gitea avec Docker](/gitea-serveur-git-docker-auto-hebergement/). Tes repos sont là, tes clés SSH sont configurées, tout roule. Mais à chaque fois que tu pousses du code, tu dois manuellement builder, tester, puis déployer. C'est fastidieux et source d'erreurs.

Les solutions externes existent. GitHub Actions, GitLab CI, CircleCI. Elles fonctionnent bien. Mais elles imposent deux contraintes majeures : tes sources transitent par des serveurs tiers, et tu dépends de leur disponibilité. Quand GitHub est down, ton pipeline s'arrête. Quand ils changent leurs tarifs, tu subis.

**Gitea Actions apporte le CI/CD directement dans ton instance Gitea.** Pas de service externe. Pas de données qui quittent ton serveur. Une syntaxe YAML quasi identique à GitHub Actions, avec un runner open-source qui s'exécute dans un conteneur Docker. C'est le même principe que GitHub Actions, mais sur ton infrastructure. L'intégration de Gitea Actions Docker te permet de conserver la maîtrise totale de ta chaîne de déploiement.

## Qu'est-ce que Gitea Actions exactement ?

Gitea Actions est le système de CI/CD natif de Gitea, introduit dans les versions récentes. Il repose sur le standard `act` (un moteur d'exécution de workflows GitHub Actions en local) et permet de définir des pipelines en YAML dans tes dépôts. C'est la pierre angulaire d'une stack Gitea Actions Docker complètement auto-hébergée.

**Ce que ça fait :**
- Déclenche des jobs à chaque push, pull request, tag, ou cron programmé
- Exécute des commandes dans des conteneurs Docker éphémères
- Supporte les services (bases de données, caches Redis) comme sidecars
- Gère les secrets au niveau organisation, repo ou environnement
- Affiche les logs en temps réel dans l'interface web de Gitea
- Supporte les matrices de builds (tester sur plusieurs versions de Node, Python, etc.)

**La différence avec GitHub Actions :**
- Pas de marketplace d'actions publiques : tu utilises des images Docker ou des actions locales
- Les runners sont auto-hébergés par défaut : c'est toi qui les provisionnes et les maintiens
- Pas de facturation à la minute : si tu as déjà un serveur, le runner tourne dessus sans surcoût

## Architecture de Gitea Actions Docker

Le système Gitea Actions se compose de deux entités distinctes :

**1. Le serveur Gitea**
Il lit les fichiers `.gitea/workflows/*.yml`, stocke les définitions de workflows, orchestre les exécutions et affiche les résultats dans l'interface web. Il n'exécute pas directement les jobs. Il les met en file d'attente et attend qu'un runner vienne les récupérer.

**2. Le runner `act_runner`**
C'est le worker qui fait le travail. Développé par l'équipe Gitea, ce runner est un binaire qui se connecte à ton instance Gitea via un token d'enregistrement, récupère les jobs en attente, et les exécute dans des conteneurs Docker. Il utilise le moteur `nektos/act` sous le capot, ce qui explique la compatibilité avec la syntaxe GitHub Actions.

**Le flux d'exécution :**
1. Tu pousses du code sur une branche
2. Gitea détecte le fichier `.gitea/workflows/ci.yml` et crée un job
3. Le runner connecté interroge Gitea toutes les X secondes
4. Il récupère le job, clone le repo, et exécute les étapes dans un conteneur
5. Les logs remontent en temps réel dans l'interface Gitea

## Prérequis

Avant de commencer, vérifie ces points :

- Une instance Gitea fonctionnelle (v1.21+ recommandé pour Gitea Actions stable)
- Docker et Docker Compose sur le serveur hôte
- Au moins 2 Go de RAM disponibles (Gitea + runner consomment ensemble entre 500 Mo et 1,5 Go selon les workloads)
- Un sous-domaine ou un accès réseau interne entre Gitea et le runner
- Connaissances de base Docker et YAML

Si tu n'as pas encore Gitea en place, commence par [mon guide complet sur l'installation avec Docker](/gitea-serveur-git-docker-auto-hebergement/).

## Activer Gitea Actions dans l'interface d'administration

Avant de lancer le runner, il faut activer le système d'actions côté Gitea. Par défaut, il est désactivé.

**Étape 1 :** Connecte-toi en admin sur Gitea, puis va dans **Administration > Configuration > Actions**.

**Étape 2 :** Active les cases suivantes :
- `ENABLED` : activer le module Actions
- `ARTIFACT_RETENTION_DAYS` : nombre de jours de conservation des artifacts (10 par défaut)

**Étape 3 :** Va dans **Administration > Runners** et clique sur **Créer un nouveau runner**.

**Étape 4 :** Choisis le scope :
- `Instance` : le runner traite les jobs de tous les repos de l'instance
- `Organisation` : limité à une organisation spécifique
- `Repository` : limité à un repo spécifique

Pour un homelab, `Instance` est le plus simple. Gitea te génère alors un token d'enregistrement sous la forme `A1B2C3D4E5...` et une URL de connexion (`https://git.tondomaine.fr`). Conserve ces deux informations, elles servent à configurer le runner.

## Déployer le runner avec Docker Compose

Voici la configuration complète. Le runner est packagé sous forme d'image Docker officielle `gitea/act_runner`.

Crée un dossier dédié et un fichier `docker-compose.yml` :

```yaml
version: "3.8"

services:
  runner:
    image: gitea/act_runner:latest
    container_name: gitea-runner
    restart: unless-stopped
    environment:
      - GITEA_INSTANCE_URL=https://git.tondomaine.fr
      - GITEA_RUNNER_REGISTRATION_TOKEN=TON_TOKEN_ICI
      - GITEA_RUNNER_NAME=docker-runner-01
      - GITEA_RUNNER_LABELS=ubuntu-latest:docker://node:20-bullseye,self-hosted
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./runner-data:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    networks:
      - gitea-runner

networks:
  gitea-runner:
    driver: bridge
```

**Points importants sur cette configuration :**

- `GITEA_INSTANCE_URL` : l'URL publique de ton instance Gitea. Le runner doit pouvoir l'atteindre en réseau. Si Gitea et le runner sont sur la même machine, tu peux utiliser `http://gitea:3000` si ils partagent un réseau Docker commun.

- `GITEA_RUNNER_REGISTRATION_TOKEN` : le token généré à l'étape précédente. **Ne le commit pas.** Utilise un fichier `.env` ou un secret Docker pour le passer.

- `GITEA_RUNNER_NAME` : le nom d'affichage du runner dans l'interface Gitea.

- `GITEA_RUNNER_LABELS` : définit les labels auxquels ce runner répond. La syntaxe `ubuntu-latest:docker://image` mappe le label `ubuntu-latest` vers une image Docker spécifique. Tu peux en définir plusieurs, séparés par des virgules.

- `/var/run/docker.sock:/var/run/docker.sock` : le runner a besoin de lancer des conteneurs. Il utilise le Docker daemon de l'hôte via le socket. C'est une pratique standard mais qui accorde au conteneur runner des privilèges élevés. Assure-toi que ce runner est isolé et que tu contrôles les repos qui s'exécutent dessus.

Lance le runner :

```bash
mkdir -p /opt/gitea-runner && cd /opt/gitea-runner
docker compose up -d
```

Attends 10-20 secondes, puis vérifie dans **Administration > Runners** de Gitea : ton runner doit apparaître avec un statut vert `Idle`.

## Passer le token via un fichier `.env` (recommandé)

Plutôt que d'inscrire le token en dur dans le `docker-compose.yml`, crée un fichier `.env` :

```bash
GITEA_RUNNER_REGISTRATION_TOKEN=A1B2C3D4E5...
```

Et modifie le `docker-compose.yml` :

```yaml
    environment:
      - GITEA_INSTANCE_URL=https://git.tondomaine.fr
      - GITEA_RUNNER_REGISTRATION_TOKEN=${GITEA_RUNNER_REGISTRATION_TOKEN}
      - GITEA_RUNNER_NAME=docker-runner-01
```

N'oublie pas d'ajouter `.env` à ton `.gitignore` si tu versionnes ce dossier.

## Écrire ton premier workflow

Les workflows Gitea Actions se placent dans le dossier `.gitea/workflows/` à la racine du repo. La syntaxe est volontairement proche de GitHub Actions.

Voici un exemple de workflow qui teste un projet Node.js à chaque push :

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout du code
        uses: actions/checkout@v4

      - name: Installer Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Installer les dépendances
        run: npm ci

      - name: Lancer les tests
        run: npm test
```

**Analyse du fichier :**

- `on` : quand déclencher le workflow. Ici, à chaque push sur `main` ou `develop`, et à chaque pull request vers `main`.
- `jobs` : définit un ou plusieurs jobs. Chaque job s'exécute dans un conteneur Docker propre.
- `runs-on: ubuntu-latest` : demande un runner qui a le label `ubuntu-latest`. Le runner va alors utiliser l'image Docker que tu as configurée dans ses labels (`node:20-bullseye` dans notre exemple).
- `steps` : les étapes du job. Chaque step est une commande shell ou une action réutilisable.

Pousse ce fichier sur une branche :

```bash
git add .gitea/workflows/ci.yml
git commit -m "feat(ci): ajoute workflow Gitea Actions"
git push origin main
```

Ouvre l'onglet **Actions** de ton repo dans Gitea. Tu dois voir le workflow s'exécuter avec les logs en temps réel.

## Workflow Docker avancé avec Gitea Actions

Voici un exemple plus ambitieux : à chaque push sur `main`, on build une image Docker et on la pousse vers un registry (ici le registry intégré de Gitea, mais tu peux adapter pour Docker Hub).

```yaml
name: Build and Push Docker

on:
  push:
    branches: [main]
    tags: ['v*']

env:
  REGISTRY: git.tondomaine.fr
  IMAGE_NAME: ${{ gitea.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login au registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ gitea.actor }}
          password: ${{ secrets.GITEA_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}

      - name: Build et push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

**Ce qui change par rapport à GitHub Actions :**

- `${{ gitea.repository }}` et `${{ gitea.actor }}` : les variables contextuelles utilisent le préfixe `gitea` au lieu de `github`.
- `${{ secrets.GITEA_TOKEN }}` : Gitea génère automatiquement un token pour chaque exécution de workflow. Il a les permissions du compte qui a poussé le code.
- Le registry de Gitea est accessible à l'URL `git.tondomaine.fr/utilisateur/repo`.

## Gérer les secrets et variables d'environnement

Les workflows ont souvent besoin de mots de passe, tokens API, ou clés de déploiement. Gitea permet de stocker ces secrets à trois niveaux.

**Niveau repository :**
Dans ton repo, va dans **Paramètres > Secrets > Actions**. Ajoute un secret nommé `DEPLOY_KEY`. Tu peux ensuite l'utiliser dans le workflow avec `${{ secrets.DEPLOY_KEY }}`.

**Niveau organisation :**
Si tu as plusieurs repos sous la même organisation, tu peux définir des secrets communs dans **Organisation > Paramètres > Secrets**. C'est pratique pour une clé API partagée ou un token de déploiement.

**Niveau instance (admin) :**
Les admins peuvent définir des secrets globaux dans **Administration > Secrets**. Attention, ils sont accessibles à tous les workflows de l'instance.

**Variables (pas des secrets) :**
Pour des valeurs non sensibles (URL d'un service interne, version par défaut), utilise les **Variables** plutôt que les secrets. Elles sont visibles dans les logs, contrairement aux secrets qui sont masqués automatiquement.

## Labels de runner et images personnalisées

Par défaut, le runner ne connait que le label que tu lui as configuré. Si tu veux exécuter des jobs sur différentes images (Alpine, Debian, une image custom), tu dois les définir dans les labels du runner.

Exemple de configuration avec plusieurs labels :

```yaml
environment:
  - GITEA_RUNNER_LABELS=ubuntu-latest:docker://node:20-bullseye,alpine:docker://alpine:3.19,self-hosted
dans docker-compose.yml:
```

Dans ton workflow, tu peux alors cibler :

```yaml
jobs:
  test-alpine:
    runs-on: alpine
    steps:
      - run: apk add --no-cache bash && bash --version
```

**Créer une image custom :**
Si tu as besoin d'outils spécifiques (Terraform, Ansible, kubectl), le plus propre est de construire ta propre image Docker et de la référencer dans les labels du runner. Ça évite de réinstaller les outils à chaque exécution.

```dockerfile
FROM node:20-bullseye
RUN apt-get update && apt-get install -y \
    terraform \
    awscli \
    && rm -rf /var/lib/apt/lists/*
```

Build-la, pousse-la vers ton registry, et mets à jour le label du runner : `ubuntu-latest:docker://git.tondomaine.fr/utilisateur/custom-runner:latest`.

## Monitoring et résolution des problèmes

**Le runner n'apparaît pas dans Gitea :**
Vérifie les logs du conteneur : `docker logs gitea-runner`. Les causes fréquentes sont un token invalide, une URL Gitea inaccessible depuis le runner, ou un certificat SSL auto-signé non trusté.

**Le workflow reste en attente "Queued" :**
Le runner n'est pas enregistré, ou ses labels ne correspondent pas au `runs-on` du workflow. Vérifie dans **Administration > Runners** que le runner est bien `Idle` et qu'il a le label demandé.

**Erreur "Cannot connect to the Docker daemon" :**
Le socket Docker n'est pas monté correctement. Vérifie que `/var/run/docker.sock:/var/run/docker.sock` est bien dans les volumes du runner.

**Les jobs sont lents :**
Le runner télécharge les images Docker à chaque exécution. Active le cache Docker ou utilise une image de base déjà présente sur l'hôte. Si tu fais des builds fréquents, un volume `docker-cache` partagé entre le runner et l'hôte accélère considérablement.

**Secrets non résolus :**
Assure-toi que le secret est bien défini au niveau approprié (repo, org, ou instance). Si le workflow utilise `${{ secrets.XXX }}` et que le secret n'existe pas, Gitea remplace par une chaîne vide sans erreur explicite.

## Sécurité : ne fais pas n'importe quoi

Lancer du code arbitraire dans un runner Docker, c'est pratique mais dangereux. Quelques règles à respecter :

- **Ne partage pas ton runner** avec des utilisateurs non vérifiés. Un workflow malveillant peut exécuter n'importe quelle commande, y compris `docker rm -f $(docker ps -aq)`. Dans un contexte Gitea Actions Docker, cette isolation est encore plus critique.
- **Limite l'accès au socket Docker** : si possible, utilise Docker-in-Docker (DinD) plutôt que le socket de l'hôte. C'est plus lourd mais plus isolé.
- **Network policies** : isole le runner dans un réseau Docker séparé. Il n'a pas besoin d'accéder à tous les services de ton homelab.
- **Pas de secrets en clair** : jamais de mot de passe dans le code source. Utilise toujours `${{ secrets.XXX }}`.
- **Scanner les images** : si tu build des images Docker dans tes workflows, ajoute une étape de scan avec Trivy ou Clair avant de pousser vers le registry.

## Comparaison avec les alternatives

|| Critère | Gitea Actions | GitHub Actions | GitLab CI/CD |
||---|---|---|---|
|| **Coût** | Gratuit (ton serveur) | Gratuit limité, payant ensuite | Gratuit limité, payant ensuite |
|| **Hébergement** | Self-hosted | Cloud uniquement | Self-hosted (lourd) |
|| **Syntaxe** | YAML compatible GitHub | YAML natif | YAML distinct |
|| **Runners** | Auto-hébergés obligatoires | Cloud + self-hosted | Auto-hébergés |
|| **Ressources** | Léger (~500 Mo) | N/A (cloud) | Lourd (>2 Go) |
|| **Marketplace actions** | Non (images Docker) | Oui, très riche | Oui, plus limité |

Pour un homelab ou une petite équipe qui veut rester maître de sa chaîne de déploiement, Gitea Actions Docker est le meilleur compromis. Pas aussi riche que GitHub Actions, mais totalement suffisant pour builder, tester et déployer sans dépendre d'un tiers.

## Conclusion

Gitea Actions transforme ton serveur Git en plateforme CI/CD complète sans ajouter de complexité inutile. Avec un runner Docker et quelques fichiers YAML, tu automatises tes builds, tes tests et tes déploiements sans jamais sortir de ton infrastructure.

La mise en place prend moins d'une heure. Une fois configurée, elle te fait gagner du temps à chaque push. Et si tu cherches à aller encore plus loin dans l'auto-hébergement, tu peux coupler ça avec un reverse proxy comme [Traefik](/traefik-reverse-proxy-docker/) pour sécuriser les endpoints, ou [Caddy](/caddy-docker-reverse-proxy-guide/) pour une config HTTPS minimaliste.

Ton code mérite un pipeline qui travaille pour toi, pas pour une plateforme externe.
