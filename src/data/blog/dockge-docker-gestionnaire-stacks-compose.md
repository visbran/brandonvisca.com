---
title: "Dockge Docker : gérer tes stacks Compose depuis une interface web"
description: "Dockge docker : installe cette interface web pour créer, éditer et mettre à jour tes stacks Compose sans taper une ligne SSH."
pubDatetime: "2026-10-08T22:29:26+02:00"
modDatetime: "2026-10-08T08:00:00.000Z"
author: Brandon
tags:
  - docker
  - auto-hebergement
  - dashboard
  - intermediaire
featured: false
draft: false
focusKeyword: dockge docker
faqs:
  - question: "Dockge remplace-t-il complètement Portainer ?"
    answer: "Non, pas pour tous les usages. Dockge se concentre sur les stacks Compose et fait ça très bien. Portainer gère en plus les images, les volumes, les réseaux et les conteneurs isolés via une interface plus large. Si tu ne jures que par docker compose, Dockge suffit largement."
  - question: "Est-ce que Dockge touche à mes fichiers compose.yaml existants ?"
    answer: "Non. Dockge lit et écrit directement dans le dossier de stacks que tu lui donnes, au format standard. Tes fichiers restent utilisables avec la commande docker compose classique, avec ou sans Dockge installé."
  - question: "Dockge peut-il gérer plusieurs serveurs Docker depuis une seule interface ?"
    answer: "Oui, depuis la version 1.4.0, via le système d'agents. Tu installes un agent Dockge sur chaque hôte distant et tu les rattaches à ton instance principale pour piloter toutes tes stacks depuis un seul écran."
---
> 💡 **TL;DR**
> - Dockge est une interface web qui gère tes stacks Docker Compose : création, édition, démarrage, logs, update d'images
> - Zéro verrouillage : tes fichiers compose.yaml restent lisibles et utilisables en ligne de commande, Dockge ne les capture pas
> - Installation en trois commandes, port 5001, et un terminal web intégré pour debugger sans ouvrir SSH

## Table des matières

Tu gères combien de stacks Compose à la main en ce moment ? Chez moi, à un moment donné, c'était onze dossiers dans `/opt/stacks`, chacun avec son `docker compose up -d`, son `docker compose logs -f` et sa petite danse SSH pour vérifier qu'un conteneur n'était pas reparti en crash loop. Ça marche, mais ça use.

**Dockge Docker** règle ce problème sans te forcer à migrer vers Kubernetes ni à apprendre une syntaxe propriétaire. C'est signé Louis Lam, le développeur d'Uptime Kuma, donc la philosophie "interface simple, pas de magie noire" est la même.

## Qu'est-ce que Dockge Docker exactement ?

Dockge Docker est un gestionnaire web open-source pour fichiers `compose.yaml`. Il tourne dans un conteneur, surveille un dossier de ton serveur (par défaut `/opt/stacks`), et t'affiche chaque stack qu'il y trouve.

Pour chaque stack, tu peux :

- créer, éditer et supprimer un `compose.yaml` via un éditeur interactif dans le navigateur
- démarrer, arrêter et redémarrer la stack entière en un clic
- mettre à jour les images Docker d'une stack
- suivre la sortie terminal en temps réel pendant un déploiement
- ouvrir un vrai terminal web connecté au conteneur, sans passer par SSH
- convertir une commande `docker run` existante en `compose.yaml` propre

Le point qui compte le plus à mes yeux : Dockge Docker ne kidnappe pas tes fichiers. Contrairement à certains outils qui stockent la config dans leur propre base de données, Dockge lit et écrit directement sur le disque, au format standard. Tu peux toujours lancer `docker compose up -d` à la main dans le dossier d'une stack, Dockge ne s'en offusquera pas.

Depuis la version 1.4.0, Dockge supporte aussi la gestion multi-agents : tu rattaches des hôtes Docker distants à ton instance principale et tu pilotes toutes tes stacks, peu importe la machine, depuis un seul écran.

## Installation de Dockge avec Docker Compose

Prérequis : Docker 20 ou plus récent (Podman fonctionne aussi avec `podman-docker` sur Debian), et un dossier dédié aux stacks que tu veux superviser.

Crée les deux dossiers nécessaires et récupère le fichier Compose officiel :

```bash
mkdir -p /opt/stacks /opt/dockge
cd /opt/dockge
curl https://raw.githubusercontent.com/louislam/dockge/master/compose.yaml --output compose.yaml
```

Voici le contenu de ce fichier, que tu peux ajuster avant de lancer :

```yaml
services:
  dockge:
    image: louislam/dockge:1
    restart: unless-stopped
    ports:
      - 5001:5001
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./data:/app/data
      - /opt/stacks:/opt/stacks
    environment:
      - DOCKGE_STACKS_DIR=/opt/stacks
      - PUID=1000
      - PGID=1000
```

Trois points qui méritent attention avant de lancer quoi que ce soit :

- Le chemin du dossier de stacks (`/opt/stacks`) doit être **identique** côté hôte et côté conteneur. Dockge s'en sert pour résoudre les chemins quand il lit un `compose.yaml` : un mismatch écrit les données au mauvais endroit.
- Le socket Docker (`/var/run/docker.sock`) donne à Dockge un accès complet à ton démon Docker. C'est nécessaire pour qu'il puisse démarrer et arrêter des stacks, mais ça veut dire qu'il faut traiter cette interface comme sensible, au même titre qu'un accès root sur l'hôte.
- `PUID` et `PGID` sont facultatifs mais recommandés. Sans eux, les fichiers créés par Dockge appartiennent à `root`, ce qui complique l'édition manuelle plus tard.

Lance ensuite le conteneur :

```bash
cd /opt/dockge
docker compose up -d
```

Dockge Docker est accessible sur `http://IP_DU_SERVEUR:5001`. La première connexion te demande de créer un compte administrateur, stocké localement dans le volume `./data`.

Si tu préfères choisir ton port et ton dossier de stacks dès la commande `curl`, le projet expose un générateur :

```bash
curl "https://dockge.kuma.pet/compose.yaml?port=5001&stacksPath=/opt/stacks" --output compose.yaml
```

## Dockge vs Portainer : lequel choisir

C'est la question qu'on me pose le plus souvent dès qu'on parle de Dockge Docker. Les deux outils ne visent pas exactement la même cible.

| Critère | Dockge | Portainer |
|---|---|---|
| Focus | Stacks Docker Compose uniquement | Conteneurs, images, volumes, réseaux, stacks |
| Fichiers Compose | Lus/écrits directement sur disque | Stockés dans la base interne de Portainer |
| Terminal web intégré | Oui | Oui (édition CE/BE) |
| Multi-hôtes | Oui, via agents (depuis 1.4.0) | Oui, avec l'édition Business |
| Courbe d'apprentissage | Minimale si tu connais déjà Compose | Plus large, plus d'options à explorer |
| Ressources | Léger, une seule image | Plus lourd selon les fonctionnalités activées |

Mon avis après usage des deux : si ta stack homelab tourne déjà entièrement sur `docker compose` et que tu veux juste arrêter de taper les mêmes commandes SSH en boucle, Dockge fait le travail sans détour. Si tu as besoin de gérer des conteneurs isolés hors stack, des registres privés ou une politique d'accès par équipe, Portainer couvre un terrain plus large. Rien n'empêche d'installer les deux côte à côte, ils ne se gênent pas.

## Gérer tes stacks Compose au quotidien

Une fois Dockge Docker lancé, chaque sous-dossier de `/opt/stacks` contenant un `compose.yaml` apparaît automatiquement dans la liste. Tu peux cliquer sur une stack existante pour voir son statut, ses logs en direct et son fichier de config.

Pour en créer une nouvelle depuis l'interface : bouton "Compose", tu nommes ta stack, tu colles ou tapes ton YAML dans l'éditeur, puis "Deploy". Dockge crée le dossier correspondant sous `/opt/stacks` et lance `docker compose up -d` pour toi, avec la sortie terminal affichée en direct.

Pour débugger un conteneur qui boucle en restart, inutile de ressortir le SSH : le bouton terminal de la stack t'ouvre un shell connecté au conteneur lui-même. Pratique quand tu veux juste vérifier un fichier de config monté ou tester une variable d'environnement sans redéployer.

Si tu veux une visibilité plus poussée sur les logs de l'ensemble de tes conteneurs, pas seulement stack par stack, j'ai publié un guide sur [Dozzle](/dozzle-docker-visionneuse-logs-web/), une visionneuse de logs en temps réel qui complète bien Dockge sans faire doublon.

## Exemples de stacks à gérer avec Dockge Docker

Dockge Docker brille surtout quand tu accumules les services. Voici le genre de stacks que je déploie et mets à jour depuis son interface :

- Une base [Redis Docker](/redis-docker-base-donnees-cle-valeur/) en support de cache pour d'autres applications
- Un lecteur [FreshRSS Docker](/freshrss-docker-lecteur-rss/) qui tourne en tâche de fond toute l'année
- Un serveur [Headscale Docker](/headscale-docker-tailscale-self-hosted/) pour le VPN entre mes machines

Chacune de ces stacks reste un dossier Compose classique. Dockge n'ajoute aucune couche propriétaire par-dessus, donc migrer d'une gestion SSH manuelle vers Dockge, ou en sortir, se fait sans douleur.

Si ton nombre de stacks continue de grossir et que tu commences à vouloir de l'orchestration automatique entre plusieurs machines physiques, jette un œil à [K3s Docker](/k3s-docker-kubernetes-leger-homelab/). Ça reste un autre niveau de complexité, mais Dockge n'est pas conçu pour ça : il gère des stacks indépendantes, pas un cluster avec scheduling automatique.

## Sécuriser ton instance Dockge Docker

⚠️ Le socket Docker monté dans le conteneur donne à Dockge (et à quiconque accède à son interface) un contrôle total sur ton hôte. Quelques réflexes avant d'exposer quoi que ce soit :

- Ne mets jamais le port 5001 directement sur Internet sans reverse proxy TLS devant. Caddy ou Nginx Proxy Manager font l'affaire en quelques minutes.
- Choisis un mot de passe long pour le compte admin créé à la première connexion, Dockge n'a pas de limite de tentatives configurable nativement à ce jour.
- Si tu n'accèdes à Dockge que depuis ton réseau local, bloque le port au niveau du firewall plutôt que de compter sur l'auth applicative seule :

```bash
sudo ufw deny 5001/tcp
sudo ufw allow from 192.168.1.0/24 to any port 5001
```

- Si tu n'as pas d'IP publique fixe, passe par un tunnel sortant plutôt que d'ouvrir un port entrant.

✅ Garde aussi en tête que Dockge lui-même n'a pas de permissions par stack : toute personne connectée à l'interface peut arrêter ou modifier n'importe quelle stack du dossier surveillé. Pas d'usage multi-utilisateur fin pour l'instant, donc réserve l'accès aux personnes de confiance.

## Mettre à jour Dockge Docker

Comme toute image Docker, la mise à jour se fait en deux commandes depuis le dossier d'installation :

```bash
cd /opt/dockge
docker compose pull && docker compose up -d
```

Le volume `./data` conserve ton compte admin et la configuration de l'interface entre deux mises à jour. Rien à reconfigurer.

## Conclusion

Dockge Docker ne révolutionne rien, et c'est exactement pour ça que je l'ai gardé. C'est une interface honnête sur des fichiers Compose honnêtes, sans base de données propriétaire à migrer si un jour tu changes d'outil. Pour qui gère plus de deux ou trois stacks sur un serveur, le gain de confort dépasse largement le temps d'installation.

Si tu tapes encore `cd /opt/stacks/un-service && docker compose logs -f` par cœur plusieurs fois par semaine, installe Dockge Docker ce soir : dix minutes de setup, et ce réflexe disparaît.
