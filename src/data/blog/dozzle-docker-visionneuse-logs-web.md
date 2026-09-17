---
title: "Dozzle Docker : visionneuse de logs Docker en temps réel via web"
description: "Guide dozzle docker complet : installe cette visionneuse de logs Docker temps réel, léger, sans base de données, avec ou sans authentification."
pubDatetime: "2026-09-17T11:01:11+02:00"
modDatetime: "2026-09-16T08:00:00.000Z"
author: Brandon
tags:
  - docker
  - auto-hebergement
  - monitoring
  - intermediaire
featured: false
draft: false
focusKeyword: dozzle docker
faqs:
  - question: "Dozzle Docker consomme combien de RAM ?"
    answer: "Très peu. L'image fait autour de 7 Mo et le conteneur tourne confortablement sous 30 Mo de RAM au repos, même avec une dizaine de conteneurs surveillés."
  - question: "Dozzle Docker peut-il surveiller plusieurs hôtes Docker à la fois ?"
    answer: "Oui, via DOZZLE_REMOTE_HOST ou le mode agent DOZZLE_REMOTE_AGENT, tu regroupes plusieurs machines Docker dans une seule interface web sans configuration réseau complexe."
  - question: "Faut-il une base de données pour faire tourner Dozzle Docker ?"
    answer: "Non. Dozzle lit directement le socket Docker et les fichiers de logs des conteneurs, sans base de données ni fichier de configuration obligatoire pour l'usage de base."
---
> 💡 **TL;DR**
> - Dozzle Docker est une visionneuse de logs web légère (image ~7 Mo) qui lit le socket Docker en direct, sans base de données
> - Installation en une commande `docker run` ou un compose de quelques lignes, port 8080 par défaut
> - Authentification simple intégrée (users.yml), multi-hôtes, actions sur conteneurs et shell dans le navigateur en option

## Table des matières

## Le problème avec `docker logs -f`

Tu as cinq conteneurs qui tournent. Un souci de connexion sur ton reverse proxy. Tu ouvres un terminal, tu tapes `docker logs -f traefik`, rien de suspect. Tu fermes, tu rouvres sur `docker logs -f authelia`. Toujours rien. Tu enchaînes les onglets de terminal comme un standardiste des années 80.

Le vrai problème, c'est pas de lire un log. C'est de lire dix logs en même temps, sans devenir fou, et sans donner un accès SSH complet à ton coloc qui veut juste vérifier si Jellyfin tourne bien.

Dozzle Docker règle ça avec une interface web qui affiche tous tes conteneurs, en direct, dans un seul écran. Pas de base de données à sauvegarder, pas d'agent lourd à maintenir. Un conteneur, un socket Docker monté en lecture, et c'est parti.

## Qu'est-ce que Dozzle Docker exactement

Dozzle est développé par Amir Raminfar, publié sous licence MIT, avec le code source ouvert sur GitHub (`amir20/dozzle`). C'est gratuit, sans version payante déguisée, sans compte à créer pour l'usage de base.

Concrètement, installer dozzle docker revient à connecter l'outil au socket Docker (`/var/run/docker.sock`) et lit les flux de logs des conteneurs directement, sans les dupliquer sur disque. Pas de Elasticsearch, pas de Loki, pas de stack à cinq services pour voir un `stdout`. C'est **dozzle docker** dans sa forme la plus honnête : un binaire Go compilé `FROM scratch`, une image de quelques mégaoctets, et une page web qui se met à jour en websocket.

Les fonctionnalités qui dépassent le simple `docker logs` :

- **Multi-conteneurs côte à côte** : tu ouvres plusieurs logs en même temps, dans des colonnes ou des onglets, sans jongler entre terminaux.
- **Statistiques en direct** : CPU, mémoire, réseau par conteneur, avec des graphiques qui bougent en temps réel.
- **Recherche et filtres** : tu tapes un mot-clé, Dozzle surligne les lignes qui matchent, sur tous les conteneurs affichés.
- **Multi-hôtes et Swarm** : tu regroupes plusieurs machines Docker (via `DOZZLE_REMOTE_HOST` ou en mode agent) dans une seule interface, avec TLS entre les nœuds.
- **Actions et shell** : démarrer, arrêter, redémarrer un conteneur, ou ouvrir un shell dedans, directement depuis le navigateur (à activer explicitement).
- **Alertes webhook** : notifications vers Slack, Discord ou ntfy quand un pattern précis apparaît dans les logs.
- **Support MCP** : Dozzle expose un serveur Model Context Protocol pour brancher un assistant IA sur tes logs, si ce genre de chose t'intéresse.

Si t'es du genre à empiler les services Docker sur ton serveur, Dozzle vient naturellement compléter un stack où tu gères déjà des accès et des pare-feux fins avec [UFW Docker](/ufw-docker-pare-feu-linux/) ou une authentification centralisée via [Authelia](/authelia-docker-authentification-2fa-homelab/).

## Pourquoi pas juste `docker logs -f` ou Portainer

Avant de choisir dozzle docker plutôt qu'un autre outil, autant comparer aux options que tu utilises déjà. `docker logs -f` marche très bien pour un conteneur, en SSH, tout seul. Le problème arrive à l'échelle : tu ne peux pas suivre dix conteneurs dans un seul terminal, tu ne peux pas partager ça facilement avec quelqu'un qui n'a pas d'accès shell, et tu perds l'historique dès que tu fermes la session.

Portainer fait déjà une partie du travail, avec une vue logs par conteneur. Mais c'est un outil de gestion complet, plus lourd, pensé pour administrer toute ta stack Docker. Si tu veux juste un écran de logs qui reste ouvert sur un deuxième moniteur, ou un accès en lecture seule pour un collègue, Dozzle fait ce job précis et rien d'autre. Moins de surface d'attaque, moins de RAM, démarrage en une seconde.

## Installation de Dozzle Docker

### Commande rapide avec `docker run`

Pour tester en trente secondes :

```bash
docker run --name dozzle -d \
  --volume=/var/run/docker.sock:/var/run/docker.sock \
  -v dozzle_data:/data \
  -p 8080:8080 \
  amir20/dozzle:latest
```

Tu accèdes ensuite à l'interface sur `http://ton-serveur:8080`. Le volume `dozzle_data` conserve les paramètres et les futurs fichiers d'authentification.

### Installation propre de dozzle docker avec Docker Compose

Pour un déploiement qui survit à un `docker compose down` sans perdre la config, crée un dossier dédié :

```bash
mkdir -p ~/dozzle && cd ~/dozzle
```

Et un `docker-compose.yml` :

```yaml
services:
  dozzle:
    image: amir20/dozzle:latest
    container_name: dozzle
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - dozzle_data:/data
    ports:
      - "8080:8080"
    environment:
      - DOZZLE_LEVEL=info
      - DOZZLE_NO_ANALYTICS=true

volumes:
  dozzle_data:
```

Lance-le :

```bash
docker compose up -d
```

⚠️ Le socket Docker donne un accès équivalent root sur ta machine à qui le contrôle. Ne publie jamais Dozzle sans authentification sur une IP publique, et passe par un reverse proxy avec TLS si tu y accèdes depuis l'extérieur de ton réseau local.

## Activer l'authentification simple sur Dozzle Docker

Par défaut, dozzle docker démarre sans mot de passe. Sur un homelab isolé derrière un VPN, ça passe. Sur un réseau partagé ou exposé, active l'authentification intégrée avant de faire quoi que ce soit d'autre.

Génère un fichier `users.yml` avec la commande intégrée à l'image dozzle docker :

```bash
docker run -it --rm amir20/dozzle generate admin \
  --password ton-mot-de-passe \
  --email admin@exemple.fr \
  --name "Brandon" > users.yml
```

Omets `--password` si tu ne veux pas le voir traîner dans ton historique shell : Dozzle te le demandera de façon interactive.

Place ensuite `users.yml` dans le volume `/data` et active le fournisseur d'authentification :

```yaml
services:
  dozzle:
    image: amir20/dozzle:latest
    container_name: dozzle
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./data:/data
    ports:
      - "8080:8080"
    environment:
      - DOZZLE_AUTH_PROVIDER=simple
```

Le fichier `users.yml` généré doit se trouver dans `./data/users.yml`. Au prochain démarrage, dozzle docker demande un login avant d'afficher le moindre log.

Si tu gères déjà plusieurs services derrière une authentification unique, regarde plutôt du côté d'une couche SSO comme [Authelia](/authelia-docker-authentification-2fa-homelab/) plutôt que de multiplier les comptes locaux service par service.

## Variables d'environnement utiles pour dozzle docker

| Variable | Rôle |
|---|---|
| `DOZZLE_LEVEL` | Niveau de log de Dozzle lui-même (`info` par défaut) |
| `DOZZLE_FILTER` | Filtre les conteneurs affichés (par label, nom, etc.) |
| `DOZZLE_NO_ANALYTICS` | Désactive la télémétrie envoyée par l'application |
| `DOZZLE_AUTH_PROVIDER` | `none`, `simple`, `oauth` ou `oidc` |
| `DOZZLE_ENABLE_SHELL` | Autorise l'ouverture d'un shell dans un conteneur depuis le navigateur |
| `DOZZLE_ENABLE_ACTIONS` | Autorise start/stop/restart depuis l'interface |
| `DOZZLE_REMOTE_HOST` | Liste d'hôtes Docker distants à agréger dans une seule vue |
| `DOZZLE_TIMEOUT` | Délai de connexion aux hôtes distants (`10s` par défaut) |

💡 Sur dozzle docker, `DOZZLE_ENABLE_SHELL` et `DOZZLE_ENABLE_ACTIONS` sont pratiques mais donnent un contrôle réel sur tes conteneurs depuis un navigateur. Ne les active que si l'accès à Dozzle est déjà verrouillé par une authentification et, idéalement, un accès réseau restreint.

## Surveiller plusieurs hôtes Docker

Si ton homelab tourne sur plusieurs machines, deux options existent. La plus simple : `DOZZLE_REMOTE_HOST` avec une liste d'adresses TCP Docker exposées. Elle suppose que chaque hôte distant a son démon Docker accessible sur le réseau, ce qui demande d'ouvrir le socket TCP proprement et de le protéger avec TLS.

L'autre approche, plus récente et recommandée par le projet dozzle docker, c'est le mode agent : tu lances un petit conteneur Dozzle en mode `DOZZLE_MODE=agent` sur chaque machine distante, et une instance principale les agrège via `DOZZLE_REMOTE_AGENT`. Chaque agent expose uniquement ce qu'il faut, sans ouvrir le socket Docker complet sur le réseau.

Si ton réseau homelab commence à avoir plusieurs segments et pare-feux entre les machines, vérifie que les ports utilisés par Dozzle passent bien tes règles [UFW Docker](/ufw-docker-pare-feu-linux/), qui a ses propres subtilités avec le NAT de Docker.

## Dépannage courant avec dozzle docker

**Dozzle Docker affiche une page vide ou "no containers found".** Vérifie que le socket Docker est bien monté avec le bon chemin (`/var/run/docker.sock` sur la plupart des distributions Linux, chemin différent sous Docker Desktop) et que l'utilisateur qui lance le conteneur a les droits dessus.

**Les logs n'apparaissent plus après un moment.** C'est en général lié à la rotation des logs Docker configurée dans `daemon.json` (`max-size`, `max-file`). Dozzle lit ce que Docker garde : si tu as réduit la rétention pour économiser du disque, Dozzle en verra moins.

**L'authentification simple ne se déclenche pas.** Vérifie que `DOZZLE_AUTH_PROVIDER=simple` est bien défini et que `users.yml` est accessible dans `/data` à l'intérieur du conteneur, pas juste sur l'hôte. Une erreur de chemin de volume est la cause la plus fréquente.

**Le mode agent multi-hôtes ne se connecte pas.** Vérifie que le port de l'agent est ouvert entre les machines et que les versions de Dozzle correspondent entre l'instance principale et les agents distants. Un décalage de version casse parfois le protocole interne.

## Aller plus loin autour de Dozzle

Une fois Dozzle en place, tu as une vue claire sur ce qui tourne, mais pas encore sur ce qui tombe en panne silencieusement. Pour ça, complète avec un outil de surveillance externe comme [Changedetection](/changedetection-docker-surveillance-web/) si tu veux aussi surveiller des changements sur des pages web liées à tes services.

Si ton homelab manque encore d'un DNS récursif propre pour résoudre tes noms internes sans dépendre d'un service externe, [Unbound Docker](/unbound-docker-dns-recursif/) complète bien la partie infrastructure. Et pour un espace de partage de fichiers léger à côté de tes outils de monitoring, [Droppy](/droppy-partage-images-auto-heberge/) reste une option simple à déployer.

## Conclusion

Dozzle Docker règle un problème précis : voir les logs de plusieurs conteneurs Docker sans multiplier les terminaux SSH. Pas de base de données, une image minuscule, une authentification suffisante pour un usage interne. C'est le genre d'outil qu'on installe en cinq minutes et qu'on oublie ensuite, jusqu'au jour où un conteneur plante à 3h du matin et que tu es content de pouvoir checker ça depuis ton téléphone sans ouvrir de terminal.

Si t'as déjà une dizaine de conteneurs qui tournent chez toi, la vraie question c'est pas si tu as besoin de Dozzle, c'est combien de temps tu as encore prévu de perdre avec `docker logs -f` en boucle.
