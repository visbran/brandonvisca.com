---
title: "Beszel Docker monitoring : auto-hébergé ultra-léger pour ton homelab"
description: "Guide Beszel Docker monitoring : installe ce monitoring auto-hébergé ultra-léger pour surveiller CPU, RAM et disque de tes serveurs."
pubDatetime: 2026-05-28 06:00:00+00:00
modDatetime: 2026-05-31 00:00:00+01:00
author: Brandon Visca
tags:
  - intermediaire
  - docker
  - auto-hebergement
  - homelab
  - monitoring
featured: false
draft: false
focusKeyword: beszel docker
faqs:
  - question: "Combien de RAM consomme l'agent Beszel ?"
    answer: "Très peu — l'agent tourne en binaire Go et consomme moins de 20 Mo de RAM, ce qui le rend idéal pour un Raspberry Pi ou un petit VPS."
  - question: "Beszel peut-il superviser des conteneurs Docker ?"
    answer: "Oui. En montant le socket Docker en lecture seule dans l'agent, Beszel remonte les stats par conteneur en plus des métriques système."
  - question: "Peut-on recevoir les alertes ailleurs que par email ?"
    answer: "Oui. Beszel envoie les alertes par email via PocketBase, mais tu peux brancher un webhook vers Discord, Slack, n8n ou Uptime Kuma."
timezone: Europe/Paris
---
> 💡 **TL;DR** — Beszel en bref :
> - Monitoring auto-hébergé ultra-léger (binaire Go) : CPU, RAM, disque et réseau collectés via SSH.
> - Pensé pour un homelab de 3 à 10 machines, sans Prometheus ni Grafana ni base externe.
> - Hub + agents déployés en 10 minutes avec Docker Compose.

T'as déjà perdu une nuit à configurer Prometheus + Grafana pour monitorer un simple Raspberry Pi ? Tu te retrouvais avec dix conteneurs, des règles YAML kafkaïennes et un dashboard que t'arrivais pas à lire sans ton bac+5 en observabilité ? T'inquiète pas, j'ai mangé la même soupe 🍜

Aujourd'hui je te présente **Beszel**, un outil de monitoring auto-hébergé écrit par henrygd en Go sous licence MIT. Une Go binary, un dashboard web ultra-minimaliste, une comm' SSH, zéro port supplémentaire à ouvrir. Et tu peux le mettre en route en 10 minutes. Let's go.

## Table des matières


## Qu'est-ce que Beszel et pourquoi il te fera gagner du temps

Beszel, c'est le petit dernier de la famille monitoring auto-hébergé. C'est un système de monitoring de serveurs **open-source** qui se veut minimaliste : pas de base de données externe à configurer, pas de TSDB, pas de PromQL. Juste un **hub** central qui collecte des métriques via SSH auprès d'**agents** installés sur chaque machine.

Les métriques collectées couvrent l'essentiel :

- 🖥️ **CPU** : usage total par cœur et temps d'attente I/O
- 🧠 **RAM** : usage, buffer, cache
- 💾 **Disques** : espace utilisé, I/O (lecture/écriture)
- 🌐 **Réseau** : débit entrant/sortant, paquets perdus
- 🧑‍🔬 **Processus** : top processus par CPU ou mémoire
- 🌡️ **Température** : capteurs disponibles (si exposés par `sensors`)

Le tout est stocké dans un **SQLite intégré** au hub. Oui, ça tient dans un fichier. Oui, c'est suffisant pour un petit homelab. Non, ça ne remplace pas un Datadog à 500€/mois. C'est **l'outil parfait pour celui qui veut voir l'état de ses 4-5 machines sans lancer un cluster Kubernetes** 🎯

En plus, Beszel est **responsive** : il tourne aussi bien sur un VPS chez Contabo qu'une armée de Raspberry Pi chez toi. Et le client est léger : l'agent consomme moins de 20 Mo de RAM.

## L'architecture hub + agents en 30 secondes

Le vocabulaire est simple :

- **Hub** : le serveur central. C'est lui qui expose le dashboard web, stocke les données SQLite et initie les connexions SSH.
- **Agent** : une petite binaire Go installée sur chaque machine à surveiller. Elle collecte les métriques en local et les servit via SSH quand le hub demande.

La communication entre hub et agent se fait **exclusivement en SSH**. Le hub ouvre une connexion SSH vers chaque agent, ce qui signifie :

✅ Tu n'as pas besoin d'exposer de port supplémentaire sur le hub
✅ Tu peux utiliser tes clés SSH existantes
✅ Le trafic est chiffré natif (pas de WireGuard ou VPN obligatoire)
✅ L'agent peut être dans un réseau privé tant que le hub y arrive en SSH


## Prérequis avant d'installer Beszel

Tu vas avoir besoin de **deux choses** pour suivre ce guide :

1. Une machine qui hébergera le hub (peut être la même que l'agent si tu n'as qu'un seul serveur)
2. Docker et Docker Compose sur cette machine

Côté réseau, comme la communication passe par SSH, assure-toi que :

- le hub peut joindre chaque agent sur le port SSH (généralement 22)
- les clés SSH sont prêtes (le hub génère une paire automatiquement lors du premier lancement, tu n'as qu'à copier la clé publique)

Beszel fournit des images multi-arch, donc **ARM64 et AMD64 sont supportés** (bye bye les soucis de Raspberry Pi 🍓).


## Installation du hub avec Docker Compose

Sur la machine qui fera office de hub, crée un dossier et un fichier `compose.yaml` :

```yaml
services:
  beszel:
    image: henrygd/beszel:0.9
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

> 💡 **Astuce** : ne mets pas Beszel directement face à Internet sur le port 8090. On verra juste après comment le mettre derrière un reverse proxy avec SSL.

Une fois démarré, rends-toi sur `http://IP_DU_HUB:8090`. Crée un compte admin (Beszel utilise PocketBase pour l'authentification). Tu arrives sur une interface vide — c'est normal, on va ajouter des agents.


## Installation de l'agent sur une machine distante

### Méthode Docker (recommandée)

Sur chaque machine à monitorer, crée un dossier et ce `compose.yaml` :

```yaml
services:
  beszel-agent:
    image: henrygd/beszel-agent:0.9
    container_name: beszel-agent
    restart: unless-stopped
    network_mode: host
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    environment:
      - TZ=Europe/Paris
      - PORT=45876
      - KEY=<CLÉ_PUBLIQUE_DU_HUB>
```

Remplace `<CLÉ_PUBLIQUE_DU_HUB>` par la clé publique SSH affichée dans le dashboard Beszel (paramètres → "Add system" → copie la clé).

Lancer l'agent :

```bash
cd /opt/beszel-agent && docker compose up -d
```

> ⚠️ **Important** : `network_mode: host` permet à l'agent de lire correctement les interfaces réseau et les stats système. C'est l'option la plus simple et la plus fiable. Beszel ne sert pas de trafic web, il n'y a pas de risque de conflit de port HTTP.

### Ajouter dans le hub

Dans le dashboard Beszel :

1. Clique sur **Add system**
2. Mets un nom (ex: `rpi-lab-01`)
3. Renseigne l'IP et le port SSH de la machine (par défaut `22`)
4. Choisis la clé SSH générée par Beszel (ou upload la tienne)
5. Valide

Le hub va se connecter en SSH, récupérer la clé publique de l'agent, et commencer à collecter les métriques. En quelques secondes tu vois apparaître les graphes CPU, RAM et disque. C'est magique 🪄


## Configuration des alertes et notifications

Beszel intègre des alertes basées sur des seuils. Tu peux configurer :

- **CPU** : alerte si usage > seuil pendant N minutes
- **RAM** : alerte si usage > seuil
- **Disque** : alerte si espace libre < seuil
- **Réseau** : alerte si bande passante dépasse un cap

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

Si tu préfères tout centraliser, tu peux aussi utiliser n8n ou Ansible pour envoyer la commande à toutes tes machines en SSH. L'important est de ne pas laisser un agent obsolète tourner pendant des mois sur un serveur exposé.


## Ajoute un reverse proxy et un certificat SSL

Ton hub doit être accessible en HTTPS. Si tu utilises déjà [Nginx Proxy Manager](/nginx-proxy-manager-docker-guide/) ou [Traefik](/traefik-reverse-proxy-docker/), c'est trivial :

Avec Nginx Proxy Manager :

1. Ajoute un proxy host → `beszel.brandonvisca.com` (ou ton sous-domaine)
2. Forward Host : `beszel`, Port : `8090`
3. Active SSL Let's Encrypt
4. Mets une auth basique si tu veux une couche de sécurité en plus

Avec Traefik (si tu as un réseau `proxy` externe) :

```yaml
services:
  beszel:
    image: henrygd/beszel:0.9
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


## Limites et conseils d'usage

Beszel n'est pas parfait pour tout le monde. Voici ce qu'il faut savoir avant d'adopter :

### ✅ Les points forts
- **Ultra-léger** : un agent + hub Docker, c'est moins de 100 Mo de RAM combinés
- **Zéro dépendance** : pas de Prometheus, de Grafana ni de base de données externe
- **Multi-arch** : ARM64 et AMD64 sans se poser de questions
- **SSH natif** : pas de port exposé, pas de VPN nécessaire (mais possible si tu préfères)
- **Open-source MIT** : tu peux forker, contribuer ou l'auditer

### ⚠️ Les limites
- **Rétention** : les données sont stockées dans un fichier SQLite. Pour un historique de plusieurs années, il faudra peut-être penser à l'archivage. Pas de TSDB intégré.
- **Pas de dashboard custom** : tu as les graphes par machine, point. Pas de construction de dashboard multi-métriques comme Grafana.
- **Pas de templating d'alerte avancé** : les alertes sont des seuils simples, pas de règles complexes type PromQL.
- **Besoin d'une IP statique ou d'un DNS** pour chaque agent (le hub appelle en SSH, pas l'inverse)

### 🧠 Quand l'utiliser ?
- Pour monitorer 3 à 10 machines sans te compliquer la vie
- Quand tu veux un dashboard lisible sans formation
- Pour un monitoring de base sur un homelab ou un petit VPS

### 🚫 Quand passer à autre chose ?
- Plus de 20 serveurs ou besoin de métriques applicatives (requêtes HTTP, logs, traces)
- Besoin de dashboards complexe avec agrégations multi-serveurs
- Historique long terme (3+ ans) avec requêtes analytiques poussées

Dans ces cas, bascule sur une stack Prometheus + Grafana ou un outil comme Netdata ou Tianji.

## FAQ

### Combien de RAM consomme l'agent Beszel ?

Très peu — l'agent tourne en binaire Go et consomme moins de 20 Mo de RAM, ce qui le rend idéal pour un Raspberry Pi ou un petit VPS.

### Beszel peut-il superviser des conteneurs Docker ?

Oui. En montant le socket Docker en lecture seule dans l'agent, Beszel remonte les stats par conteneur en plus des métriques système.

### Peut-on recevoir les alertes ailleurs que par email ?

Oui. Beszel envoie les alertes par email via PocketBase, mais tu peux brancher un webhook vers Discord, Slack, n8n ou Uptime Kuma.

## Articles connexes

- [Netdata Docker : monitorer ton serveur en temps réel sans te ruiner](/netdata-docker/)
- [Nginx Proxy Manager : reverse proxy en 5 min avec Docker](/nginx-proxy-manager-docker-guide/)
- [Traefik v3 : le reverse proxy Docker qui gère le HTTPS tout seul](/traefik-reverse-proxy-docker/)
- [n8n Docker : remplace Zapier par du self-hosted](/n8n-docker-workflow-automation/)

Beszel ne révolutionnera pas l'industrie du monitoring, mais il remplit **parfaitement** le créneau "je veux voir mes serveurs sans y passer la nuit". Pour un homelab moderne, c'est un excellent compromis entre simplicité et efficacité 🔥
