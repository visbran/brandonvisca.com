---
title: "Scrutiny Docker : monitoring SMART de tes disques avec alertes"
description: "Scrutiny Docker : surveille la santé SMART de tes disques en temps réel, reçois des alertes avant la panne. Guide déploiement complet homelab 2026."
pubDatetime: "2026-09-10T11:02:11+02:00"
modDatetime: "2026-09-09T08:00:00.000Z"
author: Brandon
tags:
  - docker
  - auto-hebergement
  - monitoring
  - intermediaire
featured: false
draft: false
focusKeyword: scrutiny docker
faqs:
  - question: "Scrutiny Docker peut-il surveiller des disques NVMe ?"
    answer: "Oui, Scrutiny prend en charge les disques NVMe via smartmontools. Ajoute /dev/nvme0 et /dev/nvme0n1 dans la section devices du docker-compose.yml et Scrutiny détecte automatiquement le protocole NVMe et ses attributs spécifiques."
  - question: "Quelle différence entre Scrutiny et smartd en natif ?"
    answer: "smartd natif envoie des alertes email basiques sans historique. Scrutiny Docker ajoute un dashboard web avec scoring de santé par disque, historique des attributs SMART dans le temps, et des notifications vers des dizaines de services via Shoutrrr."
  - question: "Scrutiny Docker fonctionne-t-il sur plusieurs machines ?"
    answer: "Oui, avec le modèle hub/spoke : un conteneur hub centralise les données et affiche le dashboard, et un conteneur spoke collector tourne sur chaque machine supervisée. Les données remontent vers le hub via HTTP sur le port 8080."
---
> 💡 **TL;DR**
> - Scrutiny Docker est un dashboard web SMART auto-hébergé qui surveille la santé de tes disques et t'alerte avant la panne.
> - Mode omnibus pour une seule machine, hub/spoke pour agréger plusieurs serveurs depuis un seul dashboard.
> - Alertes vers Telegram, Ntfy, Slack, Discord et des dizaines d'autres services via la bibliothèque Shoutrrr.

Un disque dur qui lâche sans prévenir, c'est la catastrophe classique du homelab. Les données partent, la nuit est longue. Pourtant, SMART (Self-Monitoring, Analysis and Reporting Technology) surveille la santé des disques depuis des décennies. Le problème ? `smartctl -a /dev/sda` crache une page de métriques cryptiques que personne ne lit, et `smartd` envoie des emails qui finissent dans les spams.

**Scrutiny Docker** résout ça proprement : il enveloppe smartmontools dans une interface web lisible, historise les métriques SMART dans une base time-series locale, et envoie des alertes vers le service de ton choix. Projet open-source par AnalogJ, disponible sur [GitHub](https://github.com/AnalogJ/scrutiny).

## Table des matières

## Pourquoi surveiller ses disques avec Scrutiny

Les attributs SMART ne sont pas tous égaux. Certains prédisent une panne imminente, d'autres sont juste informatifs. `smartctl` les affiche tous de la même façon, sans hiérarchie. Tu regardes 50 lignes de chiffres et tu ne sais pas si ton disque est en train de mourir ou en parfaite santé.

Scrutiny classe ces attributs selon leur impact réel sur la fiabilité. Il s'appuie sur les taux de panne observés par Backblaze pour poser ses propres seuils, souvent bien plus stricts que ceux du constructeur, et en déduit le statut du disque. Il n'alerte que quand un attribut critique sort des limites, pas sur des métriques cosmétiques.

Trois attributs qui méritent une attention particulière :

- **Reallocated Sectors Count** : secteurs défectueux remplacés par des secteurs de réserve. En hausse = disque qui s'use vite.
- **Pending Sectors** : secteurs en attente de réallocation. Souvent signe de problème physique en cours.
- **Uncorrectable Sector Count** : secteurs que le disque n'a pas pu corriger. Le signal le plus sérieux.

Si tu surveilles déjà les performances système avec [Netdata Docker](/netdata-docker/), Scrutiny vient en complément pour la couche stockage. Netdata te donne les métriques I/O en temps réel, Scrutiny suit la santé matérielle des disques sur le long terme.

## Architecture de Scrutiny Docker : omnibus vs hub/spoke

Scrutiny Docker propose deux modes de déploiement selon ton infrastructure.

**Mode omnibus** : un seul conteneur fait tout, interface web et collecteur SMART. Idéal pour une machine unique. Simple à déployer, zéro overhead. C'est ce qu'on installe en premier.

**Mode hub/spoke** : un conteneur hub centralise les données et l'interface web, et un conteneur spoke tourne sur chaque machine à surveiller. Les spokes envoient leurs données SMART vers le hub via HTTP. Parfait pour surveiller plusieurs serveurs depuis un point central.

Les deux modes utilisent la même interface web et le même système d'alertes. La différence est purement topologique.

## Installer Scrutiny Docker en mode omnibus

Crée un dossier `scrutiny` et un `docker-compose.yml` :

```yaml
services:
  scrutiny:
    image: ghcr.io/analogj/scrutiny:master-omnibus
    container_name: scrutiny
    restart: unless-stopped
    cap_add:
      - SYS_RAWIO
    ports:
      - "8080:8080"
    volumes:
      - /run/udev:/run/udev:ro
      - ./config:/opt/scrutiny/config
      - ./influxdb:/opt/scrutiny/influxdb
    devices:
      - /dev/sda:/dev/sda
      - /dev/sdb:/dev/sdb
```

Lance le conteneur :

```bash
docker compose up -d
```

### Les points clés à comprendre

**`cap_add: SYS_RAWIO`** : capability Linux qui permet à smartmontools d'envoyer des commandes ATA directement aux disques. Sans ça, le collecteur ne peut pas interroger les données SMART.

**Section `devices`** : Scrutiny ne découvre pas automatiquement les disques de l'hôte par sécurité. Tu dois déclarer explicitement chaque disque à surveiller. Liste tous tes `/dev/sd*` et `/dev/nvme*`.

**`/run/udev:/run/udev:ro`** : donne accès aux informations udev pour identifier les disques correctement (modèle, numéro de série). Sans ça, les disques s'affichent avec des noms génériques.

**`./influxdb`** : InfluxDB tourne à l'intérieur du conteneur omnibus et stocke l'historique des métriques. Monte ce répertoire pour conserver l'historique entre les redémarrages.

> ⚠️ Avec des contrôleurs RAID matériel ou une carte HBA, il faudra peut-être ajouter `privileged: true` et préciser le type d'accès dans la config Scrutiny (`sat`, `atacam`, `scsi` selon le contrôleur).

### Ajouter des disques NVMe

Pour les disques NVMe, expose les deux nodes :

```yaml
    devices:
      - /dev/sda:/dev/sda
      - /dev/nvme0:/dev/nvme0
      - /dev/nvme0n1:/dev/nvme0n1
```

Scrutiny détecte automatiquement le protocole NVMe et adapte les attributs affichés. Les disques NVMe ont leurs propres métriques (Percentage Used, Available Spare, Data Units Written) que le dashboard traduit dans son scoring.

## Le dashboard et le statut de tes disques

Ouvre `http://IP-DU-SERVEUR:8080` après quelques secondes de démarrage. Le premier scan SMART se lance automatiquement.

La page d'accueil affiche un résumé par disque avec un statut **passed** ou **failed**. Le détail précise la raison : `failed: smart` quand c'est le disque lui-même qui se déclare en échec, `failed: scrutiny` quand ce sont les seuils de Scrutiny qui sonnent avant le constructeur, `failed: both` quand les deux tombent d'accord. Un disque sans données remontées reste en `unknown`.

Le détail par disque montre :
- Tous les attributs SMART avec valeur brute, valeur normalisée et seuil critique
- L'évolution graphique de chaque attribut dans le temps
- Les attributs en état `WARN` ou `FAIL` mis en évidence

La vue "Temperatures" donne l'historique thermique de chaque disque. Utile pour vérifier que tes disques ne cuisent pas dans un boîtier mal ventilé.

Après le scan initial, le collector repasse une fois par jour, à minuit (`0 0 * * *`). Pour changer cette fréquence, ajoute la variable `COLLECTOR_CRON_SCHEDULE` au conteneur. Et pour déclencher un scan tout de suite, sans attendre ni redémarrer quoi que ce soit :

```bash
docker exec scrutiny /opt/scrutiny/bin/scrutiny-collector-metrics run
```

## Configurer les alertes

Les alertes de Scrutiny Docker passent par **Shoutrrr**, une bibliothèque qui unifie les notifications vers des dizaines de services avec un format d'URL standardisé.

Crée un fichier `config/scrutiny.yaml` dans ton dossier `scrutiny` :

```yaml
notify:
  urls:
    - "ntfy://ntfy.ton-serveur.fr/scrutiny-alertes"
    - "telegram://token@telegram?chats=chatid"
```

Une seule clé, `urls`, et autant de destinations que tu veux. Ne cherche pas à filtrer les alertes ici : l'ancienne option `notify.filter_attributes` est dépréciée et Scrutiny refuse carrément de démarrer si elle traîne dans ton fichier. Le niveau de déclenchement se règle maintenant dans la page Settings du dashboard.

Quelques formats d'URL Shoutrrr courants :

| Service | Format URL |
|---|---|
| Ntfy (auto-hébergé) | `ntfy://ton-serveur/canal` |
| Telegram | `telegram://token@telegram?chats=chatid` |
| Discord | `discord://token@id` |
| Slack | `slack://token-a/token-b/token-c` |
| Email (SMTP) | `smtp://user:password@host:port/?fromaddress=scrutiny@mondomaine.fr&toaddresses=moi@mondomaine.fr` |

Redémarre le conteneur après avoir créé ou modifié la config :

```bash
docker compose restart scrutiny
```

Si tu utilises déjà [Beszel Docker](/beszel-monitoring-docker/) ou [Uptime Kuma](/uptime-kuma-2-0-monitoring-auto-heberge/) pour monitorer tes services, tu peux centraliser les notifications dans le même canal Ntfy ou le même webhook Discord. Scrutiny pointe vers la même destination.

## Surveiller plusieurs machines avec le hub/spoke

Pour un homelab multi-serveurs, le mode hub/spoke de Scrutiny Docker donne un seul dashboard qui agrège les données de toutes tes machines.

Attention à un piège : contrairement à l'image omnibus, l'image `-web` n'embarque pas InfluxDB. Le hub, c'est donc deux conteneurs, la base et l'interface.

**Sur le serveur qui héberge le dashboard (hub)** :

```yaml
services:
  influxdb:
    image: influxdb:2.8
    container_name: scrutiny-influxdb
    restart: unless-stopped
    volumes:
      - ./influxdb:/var/lib/influxdb2

  scrutiny-hub:
    image: ghcr.io/analogj/scrutiny:master-web
    container_name: scrutiny-hub
    restart: unless-stopped
    ports:
      - "8080:8080"
    volumes:
      - ./config:/opt/scrutiny/config
    environment:
      SCRUTINY_WEB_INFLUXDB_HOST: influxdb
    depends_on:
      - influxdb
```

Sans la variable `SCRUTINY_WEB_INFLUXDB_HOST`, le hub cherche sa base en local et ne démarre pas.

**Sur chaque machine à surveiller (spoke)** :

```yaml
services:
  scrutiny-collector:
    image: ghcr.io/analogj/scrutiny:master-collector
    container_name: scrutiny-collector
    restart: unless-stopped
    cap_add:
      - SYS_RAWIO
    volumes:
      - /run/udev:/run/udev:ro
    environment:
      - COLLECTOR_API_ENDPOINT=http://IP-DU-HUB:8080
      - COLLECTOR_HOST_ID=nom-du-serveur
    devices:
      - /dev/sda:/dev/sda
      - /dev/sdb:/dev/sdb
```

`COLLECTOR_HOST_ID` est l'identifiant de la machine dans le dashboard : mets quelque chose de lisible (`proxmox-main`, `nas-01`, `pi4`). Chaque collector remonte ses données vers le hub à son passage quotidien, et tu peux le forcer au premier démarrage avec `COLLECTOR_RUN_STARTUP: true` plutôt que d'attendre minuit.

Pour un monitoring réseau qui complète Scrutiny, mon article sur [SNMPd Docker](/snmpd-docker-monitorer-reseau/) couvre la supervision des interfaces et équipements réseau depuis Docker.

## Dépannage courant

| Symptôme | Cause probable | Solution |
|---|---|---|
| Dashboard vide, aucun disque affiché | Devices non déclarés dans compose | Liste tous tes `/dev/sd*` et `/dev/nvme*` dans `devices:` |
| `Permission denied` au démarrage | Manque `SYS_RAWIO` | Ajoute `cap_add: [SYS_RAWIO]` ou passe en `privileged: true` |
| Attributs manquants sur NVMe | Node `/dev/nvme0n1` absent | Ajoute à la fois `/dev/nvme0` et `/dev/nvme0n1` |
| Disque en `unknown`, aucun attribut | Scan pas encore passé | Attends minuit ou lance `scrutiny-collector-metrics run` |
| Alertes non reçues | URL Shoutrrr incorrecte | Vérifie la syntaxe exacte dans la doc Shoutrrr |
| Données perdues après redémarrage | Volume `influxdb` non monté | Monte `./influxdb:/opt/scrutiny/influxdb` dans le compose |
| Spoke ne remonte pas les données | URL hub incorrecte ou réseau isolé | Vérifie `COLLECTOR_API_ENDPOINT` et la connectivité entre les deux machines |

> 💡 Pour vérifier que smartmontools accède bien aux disques depuis le conteneur : `docker exec scrutiny smartctl -a /dev/sda`. Si ça sort des données SMART, le collecteur fonctionne.

## Conclusion

Scrutiny Docker, c'est le chaînon manquant entre `smartctl` qui crache du texte et une vraie supervision des disques. Dix minutes pour déployer le mode omnibus, et tu as un historique SMART de tous tes disques avec des alertes qui fonctionnent vraiment.

Le combo qui couvre l'essentiel d'un homelab : Scrutiny Docker pour la santé des disques, [Netdata Docker](/netdata-docker/) pour les métriques système en temps réel, et Uptime Kuma pour la disponibilité des services. Tu dors mieux la nuit.
