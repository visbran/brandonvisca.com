---
title: "Pulse Docker : monitoring Proxmox, Docker et Kubernetes avec IA"
description: Installe Pulse Docker pour monitorer Proxmox, Docker et Kubernetes en temps réel, avec alertes IA Patrol et dashboard unique. Guide complet 2026.
pubDatetime: "2026-10-29T11:01:11+01:00"
modDatetime: "2026-10-28T08:00:00.000Z"
author: Brandon
tags:
  - securite
  - docker
  - monitoring
  - dashboard
  - automation
  - intermediaire
featured: false
draft: false
focusKeyword: pulse docker
faqs:
  - question: "Pulse Docker remplace-t-il Prometheus et Grafana ?"
    answer: "Pas vraiment. Pulse Docker vise la supervision immédiate sans configuration, alors que Prometheus et Grafana restent la référence pour agréger des dizaines de serveurs avec des dashboards sur mesure. Pour un homelab de quelques machines, Pulse suffit largement."
  - question: "Pulse Patrol est-il payant ?"
    answer: "Les vérifications planifiées de Patrol restent gratuites si tu fournis ta propre clé d'API pour un fournisseur IA ou un modèle local. L'enquête automatique sur chaque alerte et le regroupement des causes communes appartiennent à l'offre Pro, facturée à partir de 79 dollars par an."
  - question: "Faut-il installer un agent sur chaque VM Proxmox ?"
    answer: "Non. Proxmox VE, PBS et PMG sont interrogés en lecture seule via leur API, sans rien installer dans les VMs. L'agent unifié ne devient nécessaire que pour superviser des hôtes Docker, Kubernetes ou d'autres systèmes comme TrueNAS."
---
> 💡 **TL;DR**
> - Pulse Docker surveille Proxmox VE/PBS/PMG sans agent (API en lecture seule), plus Docker, Kubernetes, TrueNAS et vSphere via un agent unifié.
> - Dashboard sur le port 7655, installation en une commande (Docker, LXC Proxmox auto-créé ou Helm), édition Community gratuite et open source (MIT).
> - Pulse Patrol ajoute des vérifications planifiées par IA (ta propre clé LLM ou un modèle local), avec enquête automatique sur les alertes dans l'offre Pro à partir de 79 $/an.

## Pulse Docker : le dashboard qui unifie Proxmox, Docker et Kubernetes

Tu as un Proxmox qui tourne, trois ou quatre VMs, une pile de conteneurs Docker, et aucune vue d'ensemble. Tu switches entre l'interface Proxmox, `docker stats` dans un terminal SSH, et ta mémoire pour savoir si tout va bien. Spoiler : ça va marcher un moment, jusqu'au jour où un disque se remplit en silence pendant que tu es en vacances.

C'est exactement le trou que **Pulse** vient combler. Le projet, maintenu par le développeur connu sous le pseudo rcourtman sur GitHub, se présente comme un tableau de bord de supervision en temps réel pour les homelabs et les infrastructures auto-hébergées. Dans cet article je vais l'appeler Pulse Docker, parce que c'est par Docker que la plupart d'entre nous vont le déployer, même si Proxmox n'a besoin d'aucun agent pour être surveillé.

Chez moi, c'est devenu l'écran que j'ouvre en premier le matin. Une page, tous les hôtes, tous les conteneurs, et une alerte si quelque chose cloche.

## Table des matières

## Pourquoi Pulse Docker plutôt que Prometheus + Grafana ou Zabbix

Monter une stack Prometheus + Grafana pour surveiller trois VMs et dix conteneurs, c'est un peu comme sortir le camion-grue pour planter une tomate. Il faut un serveur Prometheus qui scrape, un exporter par cible, une base de séries temporelles à entretenir, des dashboards Grafana à importer, et des règles d'alerte en YAML à écrire à la main.

[Zabbix](/zabbix-docker-monitoring-infrastructure/) va encore plus loin dans la puissance industrielle : templates, découverte automatique, agents sur chaque hôte. Génial pour une infra d'entreprise avec une équipe dédiée. Clairement surdimensionné pour un homelab d'un seul admin qui veut juste savoir si le NAS a de la place.

Pulse Docker prend le chemin inverse. Pour Proxmox, aucun agent : tu donnes un token API en lecture seule et le dashboard affiche déjà l'état des nœuds, des VMs, des conteneurs LXC et des sauvegardes PBS. Pour Docker et Kubernetes, un seul agent unifié suffit par hôte. Le projet est open source sous licence MIT pour l'édition Community, et les docs officielles mentionnent déjà une branche v6 (un guide de migration depuis la v5 existe), signe d'un projet qui a eu le temps de mûrir.

> ✅ **Ce qu'il faut retenir** : Pulse Docker ne remplace pas une stack d'observabilité d'entreprise. Il remplace le réflexe de tout vérifier à la main, hôte par hôte.

## Installer Pulse Docker avec Docker Compose

Le plus simple reste Docker Compose. Crée un répertoire `pulse` avec ce fichier :

```yaml
services:
  pulse:
    image: rcourtman/pulse:latest
    container_name: pulse
    restart: unless-stopped
    ports:
      - "7655:7655"
    volumes:
      - pulse_data:/data
    environment:
      - PULSE_DEPLOYMENT_METHOD=docker_compose

volumes:
  pulse_data:
```

⚠️ En production, évite le tag `latest` : va plutôt piocher un tag de version précis sur la page des releases GitHub du projet (`rcourtman/Pulse`) et fixe-le dans le `image:`. Tu évites ainsi une mise à jour surprise un lundi matin.

Lance le conteneur :

```bash
docker compose up -d
```

Le volume `pulse_data` monté sur `/data` conserve la configuration et l'historique entre deux redémarrages. Une fois le conteneur levé, le dashboard écoute sur le port **7655**. Avant d'ouvrir `http://IP-DU-SERVEUR:7655` dans ton navigateur, récupère le jeton de démarrage qui te servira à créer le compte admin :

```bash
docker exec pulse /app/pulse bootstrap-token
```

Colle la chaîne affichée (pas le contenu brut d'un fichier) dans l'écran de première connexion, et tu es dans le dashboard.

Si tu préfères que Pulse tourne directement dans un LXC Proxmox, le projet fournit un script d'installation signé qui détecte l'hôte PVE et crée lui-même un conteneur optimisé. Le script est vérifié avec `ssh-keygen -Y verify` avant exécution, ce qui évite d'exécuter n'importe quel script téléchargé à l'aveugle sur un hyperviseur de production. Une installation via Helm existe aussi si ton homelab tourne déjà sous Kubernetes.

## Connecter Proxmox VE sans agent

C'est la partie la plus élégante de l'outil. Proxmox VE, Proxmox Backup Server et Proxmox Mail Gateway sont interrogés en lecture seule via leur API native : rien à installer dans les VMs, rien à ouvrir côté hyperviseur en dehors de l'accès existant.

Dans le dashboard, va dans **Settings → Infrastructure**, clique sur **Add infrastructure**, puis choisis Proxmox. L'assistant génère un script qui crée un compte dédié `pulse-monitor` avec son propre token API et des ACL limitées à la supervision. Relis ce script avant de l'exécuter sur ton nœud, surtout si ton organisation gère déjà ses propres rôles Proxmox : adapte-le plutôt que de l'exécuter tel quel sans comprendre ce qu'il fait.

La bonne pratique, documentée par le projet lui-même, est d'utiliser un token distinct par plateforme ou par frontière de confiance, avec seulement les permissions nécessaires. Jamais le compte interactif d'un administrateur, jamais un token qui a des droits d'écriture dont Pulse n'a pas besoin. Pour faire tourner un token, crée le nouveau avant de révoquer l'ancien : tu gardes une connexion active pendant la transition.

Une fois le nœud ajouté, tu vois apparaître l'état de chaque VM et conteneur LXC, l'usage CPU/RAM/disque par nœud, et l'état des jobs de sauvegarde PBS. Tout ça sans toucher à une seule VM.

## Monitorer tes hôtes Docker avec l'agent unifié

Pour Docker (et Podman, les deux sont supportés), il faut un agent sur l'hôte : c'est lui qui lit le socket `/var/run/docker.sock` et remonte l'inventaire. Génère la commande d'installation depuis **Settings → Infrastructure**, à l'étape du jeton, puis exécute-la sur la machine à surveiller.

Une case mérite ton attention pendant l'installation : **« Allow Pulse to run commands on this host »**. Laisse-la décochée si tu veux de la supervision pure. Cochée, elle active un profil complet avec des droits d'exécution root, nécessaire si tu veux plus tard démarrer, arrêter ou mettre à jour un conteneur directement depuis Pulse. Pour ces actions, Pulse te demande toujours une approbation explicite, et elles ne fonctionnent pas si l'agent est déconnecté ou si son inventaire est obsolète.

Une fois l'agent actif, l'onglet **Docker → Overview** affiche pour chaque conteneur son état, sa santé, son usage CPU, et surtout une flèche bleue dès qu'une mise à jour d'image est disponible (Pulse compare le digest local à celui du registre). Pour les registres privés, connecte-toi avec `docker login` sous l'utilisateur qui fait tourner l'agent.

Pulse Docker reste un outil de supervision, pas un gestionnaire de conteneurs au quotidien. Pour agir vraiment sur tes stacks (redémarrer, éditer un compose, voir les variables d'environnement), je continue à passer par [Portainer](/portainer-docker-interface-web-conteneurs/), qui fait ça depuis des années sans prétendre faire du monitoring avancé. Et pour lire des logs en direct sans ouvrir un `docker logs -f` dans chaque terminal, [Dozzle](/dozzle-docker-visionneuse-logs-web/) reste imbattable en complément. Les trois outils ne se marchent pas sur les pieds : chacun fait une chose bien.

## Pulse Patrol : les alertes IA

Les alertes classiques de Pulse Docker couvrent déjà beaucoup : email, Discord, Slack, Teams, Telegram, ntfy, Gotify, Pushover, PagerDuty ou webhook générique. Tu configures des seuils (RAM, disque, température, état d'un conteneur) et tu reçois une notification sur le canal de ton choix.

Le volet qui justifie le « avec IA » du titre s'appelle **Pulse Patrol**. Concrètement, Patrol lance des vérifications planifiées en s'appuyant sur ton propre fournisseur d'IA (ta clé API chez le fournisseur de ton choix) ou sur un modèle local si tu préfères tout garder chez toi. L'intérêt, c'est de repérer des dérives que des seuils fixes ratent souvent : un pool ZFS qui se remplit plus vite que la semaine dernière, une sauvegarde qui n'a « juste » pas tourné depuis trop longtemps sans qu'aucune métrique brute ne soit franchement rouge.

Ces constats de base restent gratuits tant que tu fournis ta propre clé ou un modèle local. L'offre Pro (à partir de 79 dollars par an selon le site officiel du projet) va plus loin : Patrol enquête automatiquement sur chaque alerte dès qu'elle se déclenche, regroupe celles qui partagent la même cause racine, propose la commande exacte pour corriger le problème, et peut l'exécuter selon la politique d'approbation que tu choisis. Chaque action proposée est vérifiée et journalisée, donc tu gardes la main.

💡 Un adaptateur MCP est aussi fourni, ce qui permet d'interroger Pulse depuis un client compatible comme Claude Code. Pratique si ton homelab fait déjà tourner d'autres automatisations pilotées par un agent IA.

## Sécuriser l'accès et limiter les privilèges

Un dashboard qui voit l'état de tout ton homelab est une cible intéressante. Quelques règles simples, tirées des recommandations du projet lui-même :

- **Jamais de clé SSH privée de l'hôte** copiée dans le conteneur Pulse. Si tu as besoin d'exécuter des commandes à distance, passe par l'agent dédié, pas par un accès SSH direct planqué dans un volume.
- **Profil `--least-privilege`** côté agent Linux : le service tourne alors sous un utilisateur système dédié, `pulse-agent`, plutôt qu'en root. L'exécution de commandes et l'inventaire Docker des invités via `pct exec` restent réservés au profil root, désactivés par défaut.
- **Un agent dans une VM ou un LXC ne voit que cet invité.** Il n'obtient aucun accès à l'hyperviseur qui l'héberge, même si tu lui donnes tous les droits à l'intérieur.
- **N'expose jamais le dashboard brut sur Internet.** Passe par un reverse proxy avec authentification, ou mieux, par un tunnel VPN vers ton réseau local.

Pulse Docker te dit si un service est en panne ou si un disque déborde. Il ne remplace pas une vraie supervision de sécurité : logs d'authentification, détection d'intrusion, intégrité des fichiers. Pour ce volet, j'utilise [Wazuh](/wazuh-docker-siem-securite-homelab/) en complément, qui couvre exactement ce que Pulse ne regarde pas.

## Conclusion

Pulse Docker ne cherche pas à remplacer une stack d'observabilité d'entreprise, et c'est précisément pour ça qu'il marche dans un homelab : zéro agent pour Proxmox, un seul agent léger pour Docker et Kubernetes, un dashboard unique sur le port 7655, et une couche d'alertes qui va jusqu'à l'analyse IA si tu le souhaites. L'édition Community reste gratuite et open source, largement suffisante pour surveiller un ou deux hôtes. La bascule vers Pro ne vaut le coup que si tu veux vraiment que Patrol enquête et propose des correctifs à ta place.

Si tu veux pousser l'agrégation encore plus loin et centraliser Pulse avec d'autres widgets homelab (météo, statuts de services tiers, flux RSS), jette un œil à [Glance](/glance-docker-dashboard-homelab/) en page d'accueil de ton infra. Les deux outils se complètent très bien : Glance pour la vue d'ensemble personnalisée, Pulse Docker pour la vérité technique derrière chaque métrique.
