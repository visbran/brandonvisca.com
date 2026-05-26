---
title: "Netdata Docker : monitorer ton serveur en temps réel sans te ruiner"
description: Installe Netdata Docker pour monitorer CPU, RAM, disques et réseau en temps réel. Dashboard intégré, alertes natives, guide auto-hébergement 2026.
pubDatetime: 2026-05-19 12:00:00+02:00
modDatetime: 2026-05-26 00:00:00+01:00
author: Brandon Visca
tags:
  - docker
  - auto-hebergement
  - monitoring
  - intermediaire
featured: false
draft: false
focusKeyword: netdata docker
faqs:
  - question: "Netdata remplace-t-il Grafana ?"
    answer: "Non. Grafana est un outil de visualisation qui se connecte à des bases de données de métriques. Netdata est un agent de monitoring autonome avec son propre dashboard. Tu peux les utiliser ensemble si tu veux centraliser plusieurs serveurs."
  - question: "Quelle différence entre Netdata et Uptime Kuma ?"
    answer: "Uptime Kuma surveille la disponibilité de sites web et services. Netdata mesure les ressources système (CPU, RAM, disques, réseau) en temps réel. Ce sont des outils complémentaires."
  - question: "Peut-on utiliser Netdata sans Docker ?"
    answer: "Oui, Netdata propose un script d'installation natif. Mais Docker est plus propre pour un homelab : isolation du service, mises à jour simplifiées, suppression en une commande."
  - question: "Combien de ressources consomme Netdata ?"
    answer: "Sur un serveur standard, environ 1 à 3 % de CPU et 100 à 300 Mo de RAM. C'est négligeable comparé à la valeur des métriques collectées."
---
> 💡 **TL;DR** — Ce qu'il faut retenir :
> - Netdata surveille CPU, RAM, disques, réseau, processes et conteneurs en temps réel.
> - Dashboard web intégré accessible sur le port 19999.
> - Pas de configuration complexe : l'image Docker détecte automatiquement ce qu'elle peut monitorer.
> - Alertes natives sans éditer un fichier YAML kilométrique.

## Table des matières

## Pourquoi Netdata plutôt qu'une stack Prometheus + Grafana ?

Prometheus + Grafana, c'est le couple star du monitoring. Puissant, modulaire, industrialisé. Mais dans un homelab avec deux ou trois services, c'est comme utiliser un bulldozer pour planter une tulipe.

La stack demande :
- Un serveur Prometheus qui scrappe les métriques
- Un exporteur sur chaque machine cible
- Une base de données Time-Series à gérer
- Un Grafana à configurer avec ses dashboards JSON
- Des règles d'alerte en YAML à éditer à la main

**Netdata** supprime toute cette complexité. Une image Docker, un port ouvert, et tu as un dashboard qui affiche déjà 800+ métriques en temps réel. Pas de config initiale, pas de dashboards à importer, pas de DSL d'alerte à apprendre.

Le projet est open-source (GPL-3.0), hébergé sur GitHub avec 78 000+ étoiles et une version stable à 2.10.3. La communauté est active, les releases sortent régulièrement, et l'image Docker est mise à jour quotidiennement sur Docker Hub.

*(Si tu débutes avec Docker, commence par mon guide [Docker pour les débutants](/docker-debutant-services-auto-heberger/), il couvre les fondations.)*

Pour les détails techniques, la [documentation officielle de Netdata](https://learn.netdata.cloud/) reste la référence.

## Ce que Netdata détecte automatiquement

Lance le conteneur, ouvre le dashboard, et tu vois déjà :

- **CPU** : usage par cœur, temps d'attente IO, context switches, soft/hard interrupts
- **Mémoire** : RAM totale, utilisée, buffers, cache, swap, OOM kills
- **Stockage** : lecture/écriture par disque, latence I/O, espace disponible par partition, inodes
- **Réseau** : trafic par interface, paquets, erreurs, drops, bande passante
- **Processus** : top 10 par CPU et RAM avec leurs lignes de commande
- **Conteneurs Docker** : CPU, RAM, réseau et I/O par conteneur sans configuration supplémentaire
- **Systèmes de fichiers** : NFS, ZFS, Btrfs, ext4, détectés automatiquement

Tu n'as rien à déclarer. Netdata inspecte `/proc`, `/sys` et le socket Docker. Chaque métrique est collectée toutes les secondes, ce qui change tout comparé aux outils qui agrègent par intervalles de 5 minutes.

## Fiche Docker Compose

Crée un répertoire `netdata` et un `docker-compose.yml` (j'utilise ce compose exact en production depuis plusieurs mois) :

```yaml
services:
  netdata:
    image: netdata/netdata:v2.10.3
    container_name: netdata
    restart: unless-stopped
    hostname: netdata.tondomaine.fr
    ports:
      - "19999:19999"
    volumes:
      - netdata_config:/etc/netdata
      - netdata_lib:/var/lib/netdata
      - netdata_cache:/var/cache/netdata
      - /etc/passwd:/host/etc/passwd:ro
      - /etc/group:/host/etc/group:ro
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    cap_add:
      - SYS_PTRACE
      - SYS_ADMIN
    security_opt:
      - apparmor:unconfined
```

Lance le conteneur :

```bash
docker compose up -d
```

Attends 10 secondes, puis ouvre `http://IP-DU-SERVEUR:19999`.

### Les volumes à comprendre

- `/host/proc` et `/host/sys` en lecture seule : Netdata lit les métriques système depuis le host. Sans ça, il ne voit que ses propres ressources conteneur.
- `/var/run/docker.sock` : indispensable pour lister et monitorer les conteneurs Docker. Lecture seule suffit.
- `/etc/passwd` et `/etc/group` : permettent de résoudre les UIDs des processus en noms d'utilisateur.
- `netdata_config`, `netdata_lib`, `netdata_cache` : volumes persistants pour conserver la configuration, l'historique et le cache de métriques entre redémarrages.

### Les caps à ne pas ignorer

- `SYS_PTRACE` : autorise Netdata à inspecter les processus. Sans cette capability, le daemon refuse de démarrer.
- `SYS_ADMIN` : nécessaire pour certaines métriques réseau avancées et l'accès à `/sys`.
- `apparmor:unconfined` : désactive le profil AppArmor du conteneur. Sur Ubuntu/Debian, AppArmor bloque l'accès à `/proc` et `/sys` par défaut. Cette option contourne la restriction de manière ciblée.

## Le dashboard : lecture rapide

L'interface web de Netdata est divisée en sections. Voici l'essentiel :

- **Overview** (vue d'ensemble) : CPU, RAM, load average, disques et réseau sur une seule page. Parfait pour un coup d'œil rapide.
- **CPU** : un graph par cœur, plus un graph agrégé. Tu vois immédiatement si un process monopolise un cœur.
- **Memory** : split entre utilisée, buffers, cache et swap. Le swap est le premier indicateur de souffrance mémoire.
- **Disk** : lecture/écriture en Mo/s et IOPS par disque. Un disque à 100 % d'utilisation avec une latence élevée = goulot d'étranglement.
- **Networking** : bande passante par interface. Utile pour vérifier si un conteneur flood le réseau.
- **Applications** : top processus triés par CPU ou RAM. Tu repères un conteneur en boucle infinie en 3 secondes.
- **Containers** : si le socket Docker est exposé, tu as une vue dédiée avec CPU, RAM, réseau et I/O par conteneur.

Chaque graphique est interactif : sélectionne une plage horaire, zoom, déplace la fenêtre. Le temps de rétention dépend de la RAM allouée. Avec 256 Mo de cache, tu gardes environ une heure de données à la seconde, puis l'agrégation descend à 1 minute, puis 1 heure.

## Les alertes : pas de YAML interminable

Netdata embarque des alertes par défaut. Pas besoin d'éditer un fichier Prometheus Alertmanager.

Par exemple :
- **ram_usage** : déclenche un warning si l'utilisation RAM dépasse 80 %, critique à 90 %
- **cpu_usage** : alerte si un cœur reste à 100 % pendant plus de 10 minutes
- **disk_space** : critique si une partition tombe sous 10 % d'espace libre
- **load** : compare le load average au nombre de cœurs
- **docker_container_health** : alerte si un conteneur devient unhealthy

Tu peux configurer des notifications vers Discord, Slack, Telegram, email ou webhooks depuis l'interface web (onglet **Alerts > Notifications**) ou en éditant les fichiers dans `/etc/netdata/health.d/`.

Pour activer une notification Discord par exemple, tu copies le fichier de stock et tu renseignes ton webhook URL :

```bash
docker exec -it netdata bash
cp /etc/netdata/health.d/discord.conf /etc/netdata/health.d/discord.conf.bak
# Édite /etc/netdata/health.d/discord.conf avec ton webhook
```

Relance le health service sans redémarrer le conteneur :

```bash
docker exec netdata netdatacli reload-health
```

## Monitoring des conteneurs Docker

C'est la partie qui fait toute la différence dans un homelab. Tu n'as pas un serveur à surveiller, tu en as 15 conteneurs qui tournent.

Avec le volume `/var/run/docker.sock:/var/run/docker.sock:ro`, Netdata affiche automatiquement :

- CPU et RAM par conteneur
- Trafic réseau entrant et sortant
- Lecture/écriture disque
- État du conteneur (running, unhealthy, exited)
- Ligne de commande complète du conteneur

Tu vois immédiatement quel conteneur bouffe toute la RAM ou sature le disque. Pas besoin d'entrer dans chaque conteneur pour faire un `htop` : une seule page web te montre tout.

## Persistance des métriques

Par défaut, Netdata garde les métriques en mémoire. Quand tu redémarres le conteneur, l'historique est perdu.

Pour conserver les données entre les redémarrages, active le mode "dbengine" en montant un volume persistent. Le fichier de configuration est dans `/etc/netdata/netdata.conf`.

Tu peux aussi exposer le répertoire `/var/lib/netdata` en volume, comme dans le compose ci-dessus. L'historique reste alors persistant tant que le volume existe.

## Sécuriser l'accès au dashboard

Le dashboard Netdata est puissant et montre des données sensibles. Ne l'expose pas sur Internet sans protection.

### Via Traefik avec authentification basique

Si tu as déjà configuré [Traefik](/traefik-reverse-proxy-docker/), ajoute ces labels à ton conteneur Netdata :

```yaml
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.netdata.rule=Host(`netdata.tondomaine.fr`)"
      - "traefik.http.routers.netdata.entrypoints=websecure"
      - "traefik.http.routers.netdata.tls.certresolver=letsencrypt"
      - "traefik.http.services.netdata.loadbalancer.server.port=19999"
      - "traefik.http.routers.netdata.middlewares=auth@docker"
```

Et ajoute le conteneur au réseau `proxy` externe.

### Via un tunnel WireGuard/Headscale

La méthode la plus sûre pour un homelab : ne pas exposer Netdata du tout. Tu accesses au dashboard via un tunnel VPN depuis ton réseau local ou depuis ton téléphone. Aucun port ouvert sur Internet, zéro risque de scan automatique.

## Quand Netdata ne suffit plus

Netdata est excellent pour un serveur unique ou une petite infrastructure. Quand tu atteins 5+ machines, les alertes deviennent difficiles à centraliser et le dashboard web ne scale pas pour visualiser 50 serveurs.

À ce stade, tu bascules vers une stack centralisée :
- **VictoriaMetrics** ou **Thanos** pour le stockage de métriques
- **Grafana** pour la visualisation
- **Alertmanager** pour la gestion des alertes

Mais pour 95 % des homelabs, Netdata fait le job sans cette complexité.

## Conclusion

**L'essentiel :** si tu passes plus de temps à configurer ton monitoring qu'à monitorer, tu as choisi le mauvais outil. Combine Netdata pour les métriques système avec [Uptime Kuma](/uptime-kuma-2-0-monitoring-auto-heberge/) pour la disponibilité des services : tu couvres 95 % des besoins homelab sans sortir la carte bleue.

## Pour aller plus loin

- [Traefik avec Docker : reverse proxy HTTPS auto](/traefik-reverse-proxy-docker/)
- [Uptime Kuma : monitoring de disponibilité auto-hébergé](/uptime-kuma-2-0-monitoring-auto-heberge/)
- [Auto-hébergement : guide complet 2025](/auto-hebergement-guide-complet-2025/)
