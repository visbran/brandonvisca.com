---
title: "Zabbix Docker : monitoring complet de ton infrastructure"
description: Déploie Zabbix sous Docker pour superviser ton infrastructure complète. Guide Docker Compose zabbix docker, templates intégrés et comparatif vs Prometheus.
pubDatetime: "2026-06-28T08:00:00.000Z"
modDatetime: "2026-07-04T14:00:00.000Z"
author: Brandon Visca
tags:
  - securite
  - docker
  - linux
  - monitoring
  - zabbix
  - intermediaire
featured: false
draft: false
focusKeyword: zabbix docker
faqs:
  - question: "Quelle différence entre Zabbix agent et Zabbix agent 2 ?"
    answer: "Zabbix agent 2 est réécrit en Go, plus rapide, plus léger, et supporte nativement des plugins comme Docker, MySQL ou PostgreSQL sans configuration complexe. Pour un déploiement Zabbix Docker moderne, c'est clairement l'agent à choisir."
  - question: "Zabbix Docker consomme-t-il beaucoup de ressources ?"
    answer: "Le stack complet demande environ 1,5 à 2 Go de RAM au repos. C'est raisonnable pour une solution qui supervise l'infrastructure complète. Sur un petit VPS, limite la rétention des données dans Housekeeping pour économiser l'espace disque."
  - question: "Peut-on superviser des conteneurs Docker avec Zabbix ?"
    answer: "Oui. En montant le socket Docker dans le conteneur agent, Zabbix remonte automatiquement le statut, le CPU, la RAM et les événements de chaque conteneur via le plugin natif de l'agent 2."
  - question: "Zabbix ou Prometheus pour un homelab ?"
    answer: "Zabbix est plus simple à mettre en route et plus complet pour la supervision système traditionnelle (SNMP, agents natifs). Prometheus brille dans les environnements Kubernetes cloud-native. Pour un homelab classique, Zabbix Docker reste le premier choix."
---
> 💡 **TL;DR**
> - Zabbix est la solution de monitoring open-source la plus complète : métriques, logs, alerting, cartes réseau, tout y est
> - Un stack Docker Compose (Serveur + Frontend + Agent + Base de données) te fait tourner le bazar en 10 minutes
> - Les templates intégrés te font gagner des heures de config pour Docker, Linux, MySQL, nginx et j'en passe
> - Comparatif inclus : Zabbix reste le roi de la supervision "clé en main", Prometheus brille plus sur le cloud-native pur

## Table des matières

## Pourquoi choisir Zabbix Docker plutôt qu'un script maison ?

On a tous été là. Tu as un serveur qui tourne tranquille, puis un matin tu te réveilles et ton site est KO. Pas d'alerte, pas de mail, rien. Juste un beau downtime de 6 heures que tu découvres parce que ta mère t'a envoyé un SMS : "Ton truc marche plus ?"

Le monitoring, c'est pas un luxe. C'est aussi vital que les sauvegardes. Et si tu as déjà lu mon guide sur [Beszel](/beszel-monitoring-docker/), tu sais qu'il y a des solutions légères pour commencer. Pour la sécurité active, j'ai aussi publié un guide sur [CrowdSec Docker](/crowdsec-docker-securite-collaborative/) qui détecte et bloque les attaques en temps réel sur ton homelab. Mais Zabbix, c'est la version premium open-source. Celui qui ne se contente pas de te dire "ta RAM est à 90%", il te trace une carte réseau, il t'envoie une alerte Telegram, il te loggue l'erreur MySQL, et si tu lui demandes gentiment, il te prévient avant que le disque soit plein.

Zabbix existe depuis 1998. C'est pas un petit nouveau sorti de nulle part. Il est mature, il a une communauté massive, et surtout : il sait tout faire. Métriques système (CPU, RAM, disque, réseau), supervision applicative (MySQL, PostgreSQL, nginx, Apache), monitoring réseau ([SNMP](/snmpd-docker-monitorer-reseau/), ping, discovery automatique), alerting multi-canal (email, Slack, Telegram, webhook), cartes réseau visuelles, tableaux de bord personnalisés... Tu veux un graphique de la température de ton NAS ? Il le fait. Tu veux une alerte si ton conteneur Docker redémarre trop souvent ? Il le fait aussi.

Et le meilleur dans tout ça : on peut le déployer en quelques minutes avec Docker. Fini les installations à base de `apt install zabbix-server-mysql` qui te pourrissent ta distro avec des dépendances à la pelle.

## Ce qu'il te faut pour commencer

- Un serveur Linux avec Docker et Docker Compose installés (si ce n'est pas déjà fait, jette un œil à mon guide [Docker pour débutants](/docker-debutant-services-auto-heberger/))
- 2 Go de RAM minimum pour le stack Zabbix complet (4 Go c'est plus confortable)
- Un accès root ou sudo
- Un cerveau en état de marche (optionnel mais recommandé)

## L'architecture Zabbix en bref

Avant de balancer le `docker-compose.yml`, comprenons ce qu'on déploie. Zabbix, c'est un écosystème, pas un simple binaire.

- **Zabbix Server** : Le cerveau. Il collecte les données, traite les alertes, exécute les actions. C'est lui qui décide si ton serveur est en train de mourir ou juste de pédaler dans la semoule.
- **Zabbix Frontend** : L'interface web. C'est là que tu crées tes dashboards, tes hôtes, tes templates. C'est en PHP, donc on va le coller derrière un serveur web.
- **Zabbix Agent** : Le soldat. Installé sur chaque machine à superviser, il remonte les métriques au Server. En mode Docker, on peut aussi utiliser l'agent pour monitorer le host et les conteneurs.
- **Base de données** : MySQL ou PostgreSQL. C'est là que tout est stocké. MySQL est plus simple, PostgreSQL est plus robuste sur de gros volumes. On va prendre MySQL ici pour rester pragmatique.
- **Zabbix Web Server** : nginx ou Apache qui sert le frontend. On prend nginx, parce que c'est 2026 et que nginx c'est la vie.

Le tout communique via des ports bien définis. Le Server écoute sur le 10051 pour les agents. Le Frontend est sur le 8080 (qu'on exposera via reverse proxy si besoin). La DB reste en interne, pas besoin de l'exposer sur Internet.

Et oui, si tu as déjà mis en place un pare-feu avec [nftables](/nftables-docker-pare-feu-linux/), n'oublie pas d'ouvrir les ports nécessaires pour que tes agents puissent pousser leurs métriques.

## Zabbix Docker : le Docker Compose complet

Crée un répertoire `zabbix` quelque part sur ton serveur, et jette ce `docker-compose.yml` dedans :

```yaml
services:
  zabbix-mysql:
    image: mysql:8.0
    container_name: zabbix-mysql
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword_tres_fort
      MYSQL_DATABASE: zabbix
      MYSQL_USER: zabbix
      MYSQL_PASSWORD: zabbixpassword_tres_fort
    volumes:
      - zabbix-mysql-data:/var/lib/mysql
    networks:
      - zabbix-net
    command: --character-set-server=utf8mb4 --collation-server=utf8mb4_bin

  zabbix-server:
    image: zabbix/zabbix-server-mysql:ubuntu-7.0-latest
    container_name: zabbix-server
    restart: unless-stopped
    environment:
      DB_SERVER_HOST: zabbix-mysql
      MYSQL_DATABASE: zabbix
      MYSQL_USER: zabbix
      MYSQL_PASSWORD: zabbixpassword_tres_fort
      MYSQL_ROOT_PASSWORD: rootpassword_tres_fort
      ZBX_STARTVMWARECOLLECTORS: 0
      ZBX_VMWAREPERFREQUENCY: 0
    ports:
      - "10051:10051"
    volumes:
      - zabbix-server-data:/var/lib/zabbix
      - zabbix-server-alertscripts:/usr/lib/zabbix/alertscripts
      - zabbix-server-externalscripts:/usr/lib/zabbix/externalscripts
    networks:
      - zabbix-net
    depends_on:
      - zabbix-mysql

  zabbix-web:
    image: zabbix/zabbix-web-nginx-mysql:ubuntu-7.0-latest
    container_name: zabbix-web
    restart: unless-stopped
    environment:
      ZBX_SERVER_HOST: zabbix-server
      DB_SERVER_HOST: zabbix-mysql
      MYSQL_DATABASE: zabbix
      MYSQL_USER: zabbix
      MYSQL_PASSWORD: zabbixpassword_tres_fort
      PHP_TZ: Europe/Paris
    ports:
      - "8080:8080"
    networks:
      - zabbix-net
    depends_on:
      - zabbix-mysql
      - zabbix-server

  zabbix-agent:
    image: zabbix/zabbix-agent2:ubuntu-7.0-latest
    container_name: zabbix-agent
    restart: unless-stopped
    environment:
      ZBX_HOSTNAME: "Zabbix server"
      ZBX_SERVER_HOST: zabbix-server
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/hostfs:ro
    networks:
      - zabbix-net
    pid: host
    depends_on:
      - zabbix-server

volumes:
  zabbix-mysql-data:
  zabbix-server-data:
  zabbix-server-alertscripts:
  zabbix-server-externalscripts:

networks:
  zabbix-net:
    driver: bridge
```

Quelques explications pour les curieux :

- On utilise l'agent Zabbix 2 (`zabbix-agent2`), qui est en Go, plus rapide, et surtout capable de récupérer les métriques Docker nativement grâce au montage du socket Docker.
- Les volumes `/proc`, `/sys` et `/` montés en lecture seule permettent à l'agent d'accéder aux métriques système du host, pas seulement du conteneur.
- `pid: host` est indispensable pour que l'agent voie les processus du host et pas juste ceux de son propre namespace.
- Le port 10051 est exposé pour que les agents externes puissent se connecter. Si tout est sur la même machine, tu pourrais même le laisser fermé et utiliser le réseau Docker interne, mais pour monitorer d'autres serveurs, tu auras besoin de ce port.

Pour démarrer le bazar :

```bash
cd /chemin/vers/zabbix
docker compose up -d
```

Attends 30 à 60 secondes que MySQL initialise la base (premier démarrage), puis ouvre `http://IP_DU_SERVEUR:8080` dans ton navigateur. Les identifiants par défaut sont **Admin** / **zabbix**.

## Premiers pas dans l'interface

Une fois connecté, tu vas voir une interface austère. Ne panique pas, c'est normal. Zabbix a un design qui date un peu, mais il est efficace.

**Monitoring > Hosts** : C'est la liste des machines supervisées. Par défaut, il y a juste "Zabbix server", qui est l'agent qu'on a déployé dans le compose.

**Data collection > Hosts** : C'est là que tu ajoutes des hôtes, que tu attaches des templates, que tu configures les interfaces. C'est le cœur de la configuration.

**Monitoring > Latest data** : Les données brutes remontées par les agents. CPU, mémoire, espace disque... Tout y est.

**Dashboards** : Le tableau de bord principal. Tu peux le personnaliser à mort avec des widgets, des graphiques, des cartes réseau.

Ton premier réflexe devrait être de changer le mot de passe Admin. Va dans **Users > Users > Admin > Change password**. Fais-le maintenant, je t'attends.

## Superviser Docker avec Zabbix en temps réel

Le gros avantage de l'agent 2, c'est qu'il a un plugin Docker natif. Grâce au montage du socket Docker (`/var/run/docker.sock:/var/run/docker.sock:ro`), Zabbix peut remonter automatiquement :

- Le statut de chaque conteneur (up, down, restarting...)
- L'utilisation CPU par conteneur
- L'utilisation mémoire par conteneur
- Le nombre de conteneurs en cours d'exécution
- Les événements Docker (création, destruction, redémarrage)

Pour activer ça, rien de plus simple. Va dans **Data collection > Hosts**, clique sur "Zabbix server", puis dans l'onglet **Templates**. Ajoute le template **"Docker by Zabbix agent 2"** (c'est un template officiel livré avec Zabbix 6.0+). Attends une minute, et dans **Monitoring > Latest data**, tu verras apparaître des items liés à Docker.

Si tu veux monitorer d'autres conteneurs sur d'autres machines, il te suffit d'installer l'agent Zabbix 2 sur ces machines (aussi en Docker ou en binaire natif) et de lier le même template. C'est aussi simple que ça.

## Les templates : ton meilleur ami

Zabbix livre des centaines de templates prêts à l'emploi. C'est une des raisons pour lesquelles il écrase la concurrence sur le terrain de la facilité de déploiement.

- **Linux by Zabbix agent** : CPU, RAM, disque, réseau, processus, système de fichiers. Le classique.
- **Docker by Zabbix agent 2** : Tout ce qu'on a vu au-dessus.
- **MySQL by Zabbix agent 2** : Connexions, requêtes lentes, taille des tables, replication.
- **Nginx by Zabbix agent** : Connexions actives, requêtes par seconde, statut des workers.
- **PostgreSQL by Zabbix agent 2** : Transactions, locks, vacuum, replication.
- **SNMP devices** : Routeurs, switches, imprimantes... Si ça parle SNMP, Zabbix le comprend.

Attacher un template, c'est deux clics. Clique sur l'hôte, onglet Templates, "Link new templates", sélectionne, "Update". C'est fait. Tu viens de gagner 2 heures de configuration manuelle.

Et si un template ne te convient pas, tu peux le cloner et le modifier. C'est entièrement personnalisable. Tu veux une alerte si ton conteneur [Chrony](/chrony-docker-serveur-ntp-homelab/) redémarre ? Tu crées un trigger personnalisé basé sur l'item Docker.

## L'alerting dans Zabbix Docker : ne rate plus jamais une panne

Un monitoring sans alerting, c'est comme une Ferrari sans essence. Ça fait joli, mais ça ne sert à rien.

Zabbix gère l'alerting de manière très granulaire. Tu peux configurer :

- **Des médias** : Email, Slack, Telegram, Discord, webhook personnalisé, Jira, SMS...
- **Des actions** : Quand un trigger passe en PROBLEM, envoie un message à l'équipe SysAdmin. Quand il revient en OK, envoie un message de récupération.
- **Des escalades** : Si personne ne réagit dans les 30 minutes, envoie un SMS au boss.
- **Des conditions** : Alertes différentes selon le groupe d'hôtes, la sévérité, l'heure du jour...

Pour configurer Telegram (parce que c'est pratique et que tout le monde a Telegram sur son téléphone), va dans **Alerts > Media types > Telegram**. Tu auras besoin de créer un bot via @BotFather sur Telegram, de récupérer le token, et de coller ton chat ID. Teste la connexion. Si ça marche, va dans **Users > Users**, sélectionne ton utilisateur, onglet **Media**, et ajoute Telegram avec le chat ID.

Pour les triggers, Zabbix en a déjà pas mal de créés par les templates. Mais tu peux en ajouter. Par exemple, un trigger personnalisé qui vérifie si un conteneur spécifique a disparu de la liste des conteneurs actifs (la clé `docker.containers` ne liste que les conteneurs en cours d'exécution par défaut) :

```bash
find(/Zabbix server/docker.containers,,"like","mon_conteneur")=0
```

Sévérité : High. Et hop, tu reçois un message Telegram dès que ton conteneur tombe.

## Zabbix Docker vs Prometheus : le match

Ce comparatif est inévitable. Prometheus est partout dans l'écosystème cloud-native. Alors lequel choisir ?

**Zabbix** est la solution "tout-en-un". Il fait du pull et du push (les agents peuvent pousser les données, ou le serveur peut les récupérer). Il a une base de données relationnelle structurée. Il gère nativement le SNMP, le JMX, l'IPMI. Il a un frontend web complet avec gestion des utilisateurs, cartes réseau, rapports. C'est la solution idéale si tu veux un monitoring clé en main sans passer 3 semaines à écrire des règles d'alerting en YAML.

**Prometheus** est un pull-only time-series database ultra-optimisé pour le scraping HTTP. Il brille dans les environnements Kubernetes, les microservices, et les stacks cloud-native. Il est très rapide, très scalable, et s'intègre parfaitement avec Grafana pour la visualisation. Mais il demande beaucoup plus de boulot pour arriver au même résultat : il faut configurer chaque exporter, écrire les règles d'alerting en PromQL, configurer Alertmanager séparément, et monter Grafana pour avoir une interface utilisable.

Mon avis ? Si tu as un homelab traditionnel avec des VMs, des serveurs physiques, des switches SNMP, et que tu veux quelque chose qui marche tout de suite : **Zabbix**. Si tu fais du Kubernetes à grande échelle et que tu aimes bricoler : Prometheus + Grafana.

La bonne nouvelle : tu peux même faire cohabiter les deux. Zabbix pour la supervision système traditionnelle, Prometheus pour le monitoring applicatif Kubernetes, et Grafana pour centraliser les dashboards. Le meilleur des deux mondes.

## Astuces pour ne pas te planter

**Les mots de passe par défaut** : On en a déjà parlé, mais c'est important. Admin / zabbix, c'est le premier couple testé par les bots. Change-le immédiatement.

**La rétention des données** : Par défaut, Zabbix garde l'historique des items pendant 90 jours et les tendances pendant 365 jours. Sur un petit VPS, ça peut faire grossir la base MySQL à plusieurs gigas. Va dans **Administration > Housekeeping** pour ajuster selon tes besoins. Tu peux aussi activer la compression de tables si tu es sur MySQL 8.

**Les triggers trop sensibles** : Un trigger qui s'enclenche à chaque pic de CPU de 5 secondes, c'est un trigger inutile. Utilise les fonctions comme `avg()` ou `min()` sur une fenêtre de temps pour éviter le bruit. Par exemple : `avg(/Linux server/system.cpu.util[,user],5m)>90`, c'est bien plus fiable qu'un `last()` brut.

**Le reverse proxy** : Exposer Zabbix sur le port 8080 en direct, c'est moche. Mets un reverse proxy nginx ou [Caddy](/caddy-docker-reverse-proxy-guide/) devant avec HTTPS. Le frontend Zabbix fonctionne très bien derrière un reverse proxy, il suffit de bien configurer les en-têtes `X-Forwarded-For` et `X-Forwarded-Proto`.

**Les sauvegardes** : La base MySQL contient TOUTES tes configurations, templates, hôtes, triggers, historiques. Sauvegarde-la régulièrement. Un simple `mysqldump` quotidien vers un répertoire qui est sync vers ton NAS ou S3, et tu dors tranquille.

## FAQ

**Quelle différence entre Zabbix agent et Zabbix agent 2 ?**
Zabbix agent 2 est réécrit en Go, il est plus rapide, plus léger, et supporte nativement des plugins comme Docker, MySQL ou PostgreSQL sans configuration complexe. Pour un déploiement Zabbix Docker moderne, c'est clairement l'agent à choisir.

**Zabbix Docker consomme-t-il beaucoup de ressources ?**
Le stack complet (serveur + frontend + agent + MySQL) demande environ 1,5 à 2 Go de RAM au repos. C'est raisonnable pour une solution qui supervise ton infrastructure complète. Sur un petit VPS, limite la rétention des données dans Housekeeping pour économiser l'espace disque.

**Peut-on superviser des conteneurs Docker avec Zabbix ?**
Oui, et c'est un des gros atouts de l'agent 2. En montant le socket Docker dans le conteneur agent, Zabbix remonte automatiquement le statut, le CPU, la RAM et les événements de chaque conteneur sans configuration supplémentaire.

**Zabbix ou Prometheus pour un homelab ?**
Zabbix est plus simple à mettre en route et plus complet pour la supervision système traditionnelle (SNMP, agents natifs). Prometheus brille dans les environnements Kubernetes cloud-native. Pour un homelab classique, Zabbix Docker reste mon premier choix.

## Conclusion

Zabbix sur Docker, c'est la combinaison gagnante pour qui veut un monitoring professionnel sans la complexité d'une installation native. En 10 minutes, tu as un serveur qui surveille ton CPU, ta RAM, tes conteneurs, ta base de données, et qui te prévient par Telegram si quelque chose dérape.

Le vrai pouvoir de Zabbix ne réside pas dans l'installation. Il réside dans la granularité de ses templates, la richesse de son alerting, et la maturité de son écosystème. Que tu gères un petit homelab ou une infrastructure de 200 serveurs, Zabbix scale avec toi.

Alors oui, l'interface manque de modernité. Oui, la courbe d'apprentissage est un peu plus raide que Beszel. Mais une fois que tu as goûté à un monitoring qui anticipe les problèmes plutôt que de constater les pannes, tu ne reviendras jamais en arrière.

Un serveur non monitoré est un serveur qui va tomber un jour. Un serveur monitoré avec Zabbix, c'est un serveur dont tu maîtrises le destin.
