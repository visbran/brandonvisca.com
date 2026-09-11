---
title: "Beszel Docker monitoring : auto-hébergé ultra-léger pour ton homelab"
description: "Guide Beszel Docker : monitoring auto-hébergé ultra-léger, agents connectés en WebSocket avec token, et les nouveautés ZFS de la version 0.19."
pubDatetime: 2026-05-28 06:00:00+00:00
modDatetime: "2026-09-11T22:30:00+02:00"
author: Brandon Visca
tags:
  - docker
  - auto-hebergement
  - monitoring
  - intermediaire
featured: false
draft: false
focusKeyword: beszel
faqs:
  - question: "Combien de RAM consomme l'agent Beszel ?"
    answer: "Très peu, l'agent tourne en binaire Go et consomme moins de 20 Mo de RAM, ce qui le rend idéal pour un Raspberry Pi ou un petit VPS."
  - question: "Beszel peut-il superviser des conteneurs Docker ?"
    answer: "Oui. En montant le socket Docker en lecture seule dans l'agent, Beszel remonte les stats par conteneur en plus des métriques système."
  - question: "Peut-on recevoir les alertes ailleurs que par email ?"
    answer: "Oui. Beszel envoie les alertes par email via PocketBase, mais tu peux brancher un webhook vers Discord, Slack, n8n ou Uptime Kuma."
  - question: "Mes agents ne se connectent plus depuis la mise à jour 0.19, pourquoi ?"
    answer: "La 0.19 fait vérifier le certificat HTTPS du hub par les agents. Si ton hub est en certificat auto-signé ou en autorité privée, il faut pointer la variable CA_CERT_FILE de l'agent vers le certificat de cette autorité, sinon la connexion est refusée."
timezone: Europe/Paris
---
> 💡 **TL;DR**
> - Monitoring auto-hébergé ultra-léger (binaire Go) : CPU, RAM, disque et réseau, sans TSDB ni base de données externe.
> - L'agent ouvre une connexion WebSocket sortante vers le hub avec un token, donc ni IP fixe ni clé SSH à déposer machine par machine.
> - Hub et agents déployés en 10 minutes avec Docker Compose, en version 0.19 (ZFS, alertes conteneurs et systemd).

T'as déjà perdu une nuit à configurer Prometheus + Grafana pour monitorer un simple Raspberry Pi ? Tu te retrouvais avec dix conteneurs, des règles YAML kafkaïennes et un dashboard que t'arrivais pas à lire sans ton bac+5 en observabilité ? T'inquiète pas, j'ai mangé la même soupe 🍜

Aujourd'hui je te présente **Beszel**, un outil de monitoring auto-hébergé écrit par henrygd en Go sous licence MIT. Un binaire Go, un dashboard web ultra-minimaliste, une connexion sortante depuis chaque agent, zéro port à ouvrir sur les machines surveillées. Et tu peux le mettre en route en 10 minutes. Let's go.

> 🔄 **Mise à jour du 11 septembre 2026.** La première version de ce guide décrivait l'architecture d'origine, celle où le hub allait chercher chaque agent en SSH. Depuis la version 0.12 (juillet 2025), c'est l'inverse qui se pratique : l'agent ouvre une connexion WebSocket vers le hub avec un token. J'ai donc réécrit l'installation de l'agent, ajouté le token universel, et intégré les nouveautés de la 0.19 sortie le 3 septembre 2026.

## Table des matières

## Beszel Docker : ce que c'est et pourquoi tu vas gagner du temps

Beszel, c'est le petit dernier de la famille monitoring auto-hébergé. C'est un système de monitoring de serveurs **open-source** qui se veut minimaliste : pas de base de données externe à configurer, pas de TSDB, pas de PromQL. Juste un **hub** central et des **agents** installés sur chaque machine, qui lui remontent leurs métriques.

Les métriques collectées couvrent l'essentiel :

- 🖥️ **CPU** : usage total par cœur, temps d'attente I/O et temps volé (steal)
- 🧠 **RAM** : usage, buffer, cache
- 💾 **Disques** : espace utilisé, I/O (lecture/écriture), pools et datasets ZFS depuis la 0.19
- 🌐 **Réseau** : débit entrant/sortant, paquets perdus
- 🧑‍🔬 **Processus** : top processus par CPU ou mémoire
- 🌡️ **Température** : capteurs disponibles (si exposés par `sensors`)

Le tout est stocké dans un **SQLite intégré** au hub. Oui, ça tient dans un fichier. Oui, c'est suffisant pour un petit homelab. Non, ça ne remplace pas un Datadog à 500€/mois. C'est **l'outil parfait pour celui qui veut voir l'état de ses 4-5 machines sans lancer un cluster Kubernetes** 🎯 Si tu veux aller plus loin avec des dashboards interactifs et du monitoring pro sans payer un centime, j'ai aussi publié un guide complet sur [Grafana + Prometheus sous Docker](/grafana-prometheus-docker-monitoring-pro/).

En plus, Beszel est **polyvalent** : il tourne aussi bien sur un VPS chez Contabo qu'une armée de Raspberry Pi chez toi. Et le client est léger : l'agent consomme moins de 20 Mo de RAM.

## L'architecture hub + agents en 30 secondes

Le vocabulaire est simple :

- **Hub** : le serveur central. C'est lui qui expose le dashboard web et stocke les données dans son SQLite.
- **Agent** : un petit binaire Go installé sur chaque machine à surveiller. Il collecte les métriques en local et les remonte au hub.

Ce qui a changé, et qui conditionne tout le reste, c'est **le sens de la connexion**.

**À l'origine**, le hub ouvrait une session SSH vers chaque agent pour aller lire ses métriques. Ça marchait, mais ça imposait que le hub sache joindre chaque machine : IP statique ou entrée DNS, port accessible, et une clé publique à déposer partout.

**Depuis la 0.12** (juillet 2025), l'agent ouvre lui-même une connexion **WebSocket sortante** vers le hub et s'authentifie avec un token. Si cette connexion aboutit, l'agent arrête son propre serveur SSH. Concrètement :

✅ Tes agents peuvent être derrière un NAT, en IP dynamique, chez un client, peu importe
✅ Tu n'ouvres aucun port entrant sur les machines surveillées
✅ Une seule URL à connaître, celle du hub
✅ Le mode SSH reste disponible, les deux mécanismes cohabitent

Depuis la 0.12.10, le hub affiche le type de connexion (WebSocket ou SSH) directement dans l'interface. Pratique pour repérer les agents restés à l'ancienne après une migration.

## Prérequis avant d'installer Beszel

Tu vas avoir besoin de **deux choses** pour suivre ce guide :

1. Une machine qui hébergera le hub (peut être la même que l'agent si tu n'as qu'un seul serveur)
2. Docker et Docker Compose sur cette machine

Côté réseau, la contrainte s'est inversée par rapport à l'ancienne version de ce guide :

- chaque agent doit pouvoir joindre le hub en HTTP ou HTTPS
- le hub, lui, n'a plus besoin de joindre quoi que ce soit
- donc une seule machine à rendre accessible, et c'est celle que tu maîtrises

Beszel fournit des images multi-arch, donc **ARM64 et AMD64 sont supportés** (bye bye les soucis de Raspberry Pi 🍓).

## Installation du hub avec Docker Compose

Sur la machine qui fera office de hub, crée un dossier et un fichier `compose.yaml` :

```yaml
services:
  beszel:
    image: henrygd/beszel:0.19
    container_name: beszel
    restart: unless-stopped
    ports:
      - "8090:8090"
    volumes:
      - ./beszel_data:/beszel_data
    environment:
      - TZ=Europe/Paris
```

Puis lance :

```bash
cd /opt/beszel-hub && docker compose up -d
```

Le hub démarre sur le port `8090`. Les données SQLite sont persistées dans `./beszel_data`.

> 💡 **Astuce** : ne mets pas Beszel directement face à Internet sur le port 8090. On verra juste après comment le mettre derrière un reverse proxy avec SSL, et depuis la 0.19 ce n'est plus seulement une bonne pratique, c'est ce qui conditionne la connexion de tes agents.

Une fois démarré, rends-toi sur `http://IP_DU_HUB:8090`. Crée un compte admin (Beszel utilise PocketBase pour l'authentification). Tu arrives sur une interface vide, c'est normal, on va ajouter des agents.

## Installation de l'agent sur une machine distante

### Méthode Docker (recommandée)

Dans le dashboard, clique sur **Add system**, donne un nom à la machine, et le hub t'affiche les deux valeurs dont l'agent a besoin : un **token** et la **clé publique** du hub.

Sur la machine à monitorer, crée un dossier et ce `compose.yaml` :

```yaml
services:
  beszel-agent:
    image: henrygd/beszel-agent:0.19
    container_name: beszel-agent
    restart: unless-stopped
    network_mode: host
    volumes:
      - ./beszel_agent_data:/var/lib/beszel-agent
      - /var/run/docker.sock:/var/run/docker.sock:ro
    environment:
      TZ: Europe/Paris
      LISTEN: 45876
      HUB_URL: "https://beszel.tondomaine.com"
      TOKEN: "<TOKEN_AFFICHE_PAR_LE_HUB>"
      KEY: "<CLE_PUBLIQUE_DU_HUB>"
```

Lancer l'agent :

```bash
cd /opt/beszel-agent && docker compose up -d
```

Trois variables font le travail : `HUB_URL` dit où appeler, `TOKEN` sert à s'enregistrer, `KEY` permet à l'agent de vérifier qu'il parle bien à ton hub. Si tu préfères éviter les secrets en clair dans le compose, `TOKEN_FILE` et `KEY_FILE` lisent les mêmes valeurs depuis un fichier.

> ⚠️ **Important** : `network_mode: host` permet à l'agent de lire correctement les interfaces réseau et les stats système. C'est l'option la plus simple et la plus fiable. Beszel ne sert pas de trafic web, il n'y a pas de risque de conflit de port HTTP.

L'agent se connecte dans les secondes qui suivent et la machine passe au vert dans le dashboard. Pas d'IP à renseigner côté hub, pas de clé à copier dans l'autre sens : c'est tout l'intérêt du nouveau mode.

### Le mode SSH, si tu y tiens

L'ancien fonctionnement n'a pas disparu. Si tu ne renseignes ni `HUB_URL` ni `TOKEN`, l'agent se contente d'écouter sur son port `LISTEN` et le hub vient le chercher en SSH, comme avant. Tu renseignes alors l'IP et le port dans **Add system**.

C'est utile dans un cas précis : un agent qui ne doit surtout pas initier de trafic sortant, par exemple sur un segment réseau isolé. Pour tout le reste, le WebSocket te simplifiera la vie.

## Le token universel : enrôler toute ta flotte sans y penser

Créer un système à la main dans le hub pour récupérer un token, machine par machine, ça va pour trois serveurs. À vingt, c'est une corvée.

C'est exactement ce que règle le **token universel**, arrivé avec la 0.12 lui aussi. Tu le récupères dans les réglages du hub, page `/settings/tokens`, et tu le distribues à tous tes agents. Chaque agent qui démarre avec ce token **s'enregistre tout seul** dans le hub, sans que tu aies rien créé au préalable.

Quelques détails qui comptent en pratique :

- par défaut, l'agent s'enregistre sous le **hostname** de la machine. La variable `SYSTEM_NAME`, ajoutée en 0.13, te permet d'imposer un autre nom (pratique quand tes hostnames sont des `srv-prod-042`)
- depuis la **0.18**, tu peux rendre ce token **permanent** au lieu de le faire tourner. Pratique pour une image système ou un playbook Ansible que tu ne veux pas remettre à jour à chaque fois
- depuis la **0.18.7**, l'API du token universel est réservée aux comptes non superuser, une bonne chose pour ne pas avoir à manipuler un compte admin dans tes automatisations
- depuis la **0.18.8**, la clé publique du hub est affichée directement dans les réglages du token, tu récupères donc `TOKEN` et `KEY` au même endroit

Côté sécurité, garde en tête ce que ce token permet : **n'importe qui le possédant peut enregistrer une machine dans ton hub**. Ce n'est pas dramatique (ça pollue ton dashboard, ça n'ouvre pas l'accès à tes serveurs), mais évite de le laisser traîner dans un dépôt Git public, et préfère un token rotatif si tu n'as pas besoin du permanent.

## Ce que la 0.19 change, et le piège du certificat

La 0.19 est sortie le 3 septembre 2026 et elle embarque **un changement de comportement qui casse des installations existantes**. Autant le savoir avant de lancer le `docker compose pull`.

**Les agents vérifient désormais le certificat HTTPS du hub.** Si ton hub tourne derrière un certificat auto-signé, ou signé par une autorité interne, tes agents refusent la connexion. La solution tient en une variable : pointe `CA_CERT_FILE` vers le certificat de ton autorité, et monte ce fichier dans le conteneur de l'agent.

```yaml
    environment:
      CA_CERT_FILE: /certs/ma-ca.pem
    volumes:
      - ./ma-ca.pem:/certs/ma-ca.pem:ro
```

Si ton hub est derrière un Let's Encrypt classique, tu n'as rien à faire, c'est déjà valide.

Le reste de la 0.19 est plus agréable :

- **ZFS** : suivi des pools et des datasets, enfin de quoi surveiller un NAS sans bricoler un script
- **alertes de santé des conteneurs**, avec des extraits de logs directement dans la notification, ce qui évite un aller-retour en SSH pour comprendre
- **alertes sur échec de service systemd**, utile sur les machines qui ne font pas tourner de conteneurs
- **alertes sur le temps d'attente I/O et le temps volé du CPU**, deux métriques qui trahissent un VPS surbooké bien avant que la charge ne monte
- **totaux cumulés de lecture/écriture disque** sur la vue Disk I/O

## Configuration des alertes et notifications

Beszel intègre des alertes basées sur des seuils. Tu peux configurer :

- **CPU** : alerte si usage > seuil pendant N minutes, et depuis la 0.19 sur l'attente I/O et le temps volé
- **RAM** : alerte si usage > seuil
- **Disque** : alerte si espace libre < seuil
- **Réseau** : alerte si bande passante dépasse un cap
- **Conteneurs et services** : santé des conteneurs Docker et échecs de services systemd

Pour chaque système, clique sur **Alerts** puis règle tes valeurs. Les notifications partent par défaut **via email** (Beszel utilise le système de notifications de PocketBase). Tu peux aussi brancher un **webhook** pour envoyer les alertes vers Discord, Slack, n8n ou Uptime Kuma.

> 💡 Si tu veux centraliser tes alertes, n'hésite pas à relire mon article [n8n Docker : remplace Zapier par du self-hosted](/n8n-docker-workflow-automation/). Tu pourrais recevoir le webhook Beszel dans n8n et rediriger vers Telegram ou Discord selon la gravité.

## Mise à jour automatique avec Watchtower

Quand ton homelab grossit, la dernière chose à laquelle tu veux penser, c'est de mettre à jour manuellement chaque container. Beszel n'y échappe pas : il y a régulièrement des patchs de sécurité et des nouveautés sur le projet.

Si tu as déjà [Watchtower dans ton stack](/watchtower-mise-a-jour-docker-auto/), le hub Beszel se met à jour tout seul. Mais pour l'agent, il y a une petite subtilité : comme il tourne en `network_mode: host`, Watchtower peut parfois galérer à le redémarrer proprement.

La solution la plus fiable : laisser Watchtower s'occuper du hub, et mettre à jour l'agent via un cron simple sur chaque machine :

```bash
# ~/.local/bin/update-beszel-agent.sh
cd /opt/beszel-agent && docker compose pull && docker compose up -d
```

Puis un cron hebdomadaire :

```bash
0 3 * * 1 /home/brandon/.local/bin/update-beszel-agent.sh
```

Si tu préfères tout centraliser, tu peux aussi utiliser n8n ou Ansible pour envoyer la commande à toutes tes machines. L'important est de ne pas laisser un agent obsolète tourner pendant des mois sur un serveur exposé.

> ⚠️ Un conseil valable pour le passage en 0.19 : mets à jour **le hub avant les agents**, et vérifie que ton certificat est bien reconnu avant de laisser Watchtower propager la nouvelle image partout. Sinon tu découvres la panne sur vingt machines d'un coup.

## Ajoute un reverse proxy et un certificat SSL

Ton hub doit être accessible en HTTPS. Si tu utilises déjà [Nginx Proxy Manager](/nginx-proxy-manager-docker-guide/) ou [Traefik](/traefik-reverse-proxy-docker/), c'est trivial :

Avec Nginx Proxy Manager :

1. Ajoute un proxy host → `beszel.brandonvisca.com` (ou ton sous-domaine)
2. Forward Host : `beszel`, Port : `8090`
3. Active SSL Let's Encrypt
4. Mets une auth basique si tu veux une couche de sécurité en plus

Attention sur ce dernier point : si tes agents se connectent en WebSocket à travers ce reverse proxy, une auth basique globale les bloquera aussi. Réserve-la à l'interface web, ou laisse passer le chemin utilisé par les agents.

Avec Traefik (si tu as un réseau `proxy` externe) :

```yaml
services:
  beszel:
    image: henrygd/beszel:0.19
    container_name: beszel
    restart: unless-stopped
    volumes:
      - ./beszel_data:/beszel_data
    networks:
      - proxy
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.beszel.rule=Host(`beszel.tondomaine.com`)"
      - "traefik.http.routers.beszel.tls.certresolver=letsencrypt"
      - "traefik.http.services.beszel.loadbalancer.server.port=8090"

networks:
  proxy:
    external: true
```

Un certificat Let's Encrypt valide te met d'office en règle avec la vérification stricte de la 0.19. C'est l'option la plus simple.

## Limites et conseils d'usage

Beszel n'est pas parfait pour tout le monde. Voici ce qu'il faut savoir avant d'adopter :

### Les points forts
- **Ultra-léger** : un agent + hub Docker, c'est moins de 100 Mo de RAM combinés
- **Zéro dépendance** : pas de Prometheus, de Grafana ni de base de données externe
- **Multi-arch** : ARM64 et AMD64 sans se poser de questions
- **Connexion sortante** : aucun port à ouvrir sur les machines surveillées, le NAT et l'IP dynamique ne posent plus de problème
- **Enrôlement automatique** : un token universel et tes nouvelles machines apparaissent seules
- **Open-source MIT** : tu peux forker, contribuer ou l'auditer

### Les limites
- **Rétention** : les données sont stockées dans un fichier SQLite. Pour un historique de plusieurs années, il faudra peut-être penser à l'archivage. Pas de TSDB intégré.
- **Pas de dashboard custom** : tu as les graphes par machine, point. Pas de construction de dashboard multi-métriques comme Grafana.
- **Pas de templating d'alerte avancé** : les alertes sont des seuils simples, pas de règles complexes type PromQL.
- **Le hub doit être joignable et en HTTPS valide** : depuis la 0.19, un certificat auto-signé non déclaré coupe tes agents.
- **Un seul hub par agent en WebSocket** : si tu veux remonter la même machine vers deux hubs, tu restes sur le mode SSH.

### Quand l'utiliser ?
- Pour monitorer 3 à 10 machines sans te compliquer la vie
- Quand tu veux un dashboard lisible sans formation
- Pour un monitoring de base sur un homelab ou un petit VPS
- Quand tes machines sont dispersées derrière des box et des NAT

Si tu cherches aussi à inventorier ton parc informatique (machines, OS, logiciels installés), j'ai publié un guide pour [déployer GLPI Agent avec Docker](/glpi-agent-docker-monitorer-postes/) et peupler automatiquement ton inventaire IT.

### Quand passer à autre chose ?
- Plus de 20 serveurs ou besoin de métriques applicatives (requêtes HTTP, logs, traces)
- Besoin de dashboards complexe avec agrégations multi-serveurs
- Historique long terme (3+ ans) avec requêtes analytiques poussées

Dans ces cas, bascule sur une stack Prometheus + Grafana, un outil comme Netdata ou Tianji, ou si tu veux une solution de [monitoring infrastructure complète avec Zabbix](/zabbix-docker-monitoring-infrastructure/) qui inclut alerting, cartes réseau et templates prêts à l'emploi.

Pour superviser tes switchs et routeurs simplement, j'ai aussi publié un guide sur [SNMPd avec Docker](/snmpd-docker-monitorer-reseau/).

## FAQ

### Combien de RAM consomme l'agent Beszel ?

Très peu, l'agent tourne en binaire Go et consomme moins de 20 Mo de RAM, ce qui le rend idéal pour un Raspberry Pi ou un petit VPS.

### Beszel peut-il superviser des conteneurs Docker ?

Oui. En montant le socket Docker en lecture seule dans l'agent, Beszel remonte les stats par conteneur en plus des métriques système.

### Peut-on recevoir les alertes ailleurs que par email ?

Oui. Beszel envoie les alertes par email via PocketBase, mais tu peux brancher un webhook vers Discord, Slack, n8n ou Uptime Kuma.

### Mes agents ne se connectent plus depuis la mise à jour 0.19, pourquoi ?

La 0.19 fait vérifier le certificat HTTPS du hub par les agents. Si ton hub est en certificat auto-signé ou en autorité privée, il faut pointer la variable `CA_CERT_FILE` de l'agent vers le certificat de cette autorité, sinon la connexion est refusée.

Pour compléter ta stack de monitoring et surveiller aussi les changements sur des pages web extérieures (prix, disponibilité produit), tu peux utiliser [Changedetection.io](/changedetection-docker-surveillance-web/) que j'ai aussi couvert en Docker.

💡 À lire aussi : [Scrutiny Docker : monitoring SMART de tes disques avec alertes](/scrutiny-docker-monitoring-smart-disques/), dans la même veine que cet article.

## Articles connexes

- [Netdata Docker : monitorer ton serveur en temps réel sans te ruiner](/netdata-docker/)
- [Nginx Proxy Manager : reverse proxy en 5 min avec Docker](/nginx-proxy-manager-docker-guide/)
- [Traefik v3 : le reverse proxy Docker qui gère le HTTPS tout seul](/traefik-reverse-proxy-docker/)
- [n8n Docker : remplace Zapier par du self-hosted](/n8n-docker-workflow-automation/)

Beszel ne révolutionnera pas l'industrie du monitoring, mais il remplit **parfaitement** le créneau "je veux voir mes serveurs sans y passer la nuit". Pour un homelab moderne, c'est un excellent compromis entre simplicité et efficacité 🔥
