---
title: "Grafana Prometheus Docker : monitoring pro pour 0€"
description: "Guide complet Grafana Prometheus Docker : déploie une stack monitoring pro gratuite avec Docker Compose, dashboards et alertes."
pubDatetime: 2026-08-14 06:00:00+00:00
modDatetime: 2026-08-14 06:00:00+00:00
author: Brandon Visca
tags:
  - intermediaire
  - docker
  - monitoring
  - prometheus
  - grafana
  - linux
featured: false
draft: false
focusKeyword: grafana prometheus docker
faqs:
  - question: "Quelle différence entre Prometheus et Grafana ?"
    answer: "Prometheus est le collecteur de métriques. Il scrape les données, les stocke en TSDB et évalue les alertes. Grafana est le visualiseur. Il se connecte à Prometheus (et d'autres sources) pour afficher des dashboards interactifs. Les deux sont complémentaires et open-source."
  - question: "Combien de RAM consomme la stack Grafana + Prometheus Docker ?"
    answer: "Environ 500 Mo à 1 Go selon le nombre de cibles scrapées et la rétention. Prometheus est le plus gourmand, surtout si tu scrapes beaucoup de métriques à haute fréquence. Pour un homelab classique, 2 Go de RAM suffisent pour toute la stack."
  - question: "Peut-on monitorer des conteneurs Docker avec Prometheus ?"
    answer: "Oui. En montant le socket Docker et en déployant cAdvisor, Prometheus scrape automatiquement les métriques CPU, RAM, réseau et disque de chaque conteneur. C'est le setup standard pour le monitoring Docker."
  - question: "Faut-il obligatoirement Alertmanager pour les alertes ?"
    answer: "Non. Prometheus peut évaluer les règles d'alerte seul, mais il ne peut pas envoyer de notifications sans Alertmanager. Si tu veux des emails, Slack ou Telegram, tu dois ajouter Alertmanager dans ta stack."
ogImage: ""
---
> 💡 **TL;DR**
> - Prometheus collecte les métriques, Grafana les affiche : c'est le couple open-source de référence pour le monitoring
> - En 15 minutes avec Docker Compose, tu as une stack pro qui monitor CPU, RAM, disque, réseau et conteneurs Docker
> - cAdvisor + Node Exporter + Alertmanager complètent le setup pour un monitoring infrastructure complet
> - Totalement gratuit, pas de SaaS, pas de limites de séries, tes données restent chez toi

## Table des matières

## Pourquoi Grafana + Prometheus plutôt qu'une solution clé en main

T'as déjà testé Datadog, New Relic ou Grafana Cloud ? C'est nickel, jusqu'au moment où tu reçois la facture. 50€/mois pour monitorer trois serveurs, c'est du vol légalisé. Et les solutions légères comme [Beszel](/beszel-monitoring-docker/) ou [Uptime Kuma](/uptime-kuma-2-0-monitoring-auto-heberge/) sont géniales pour l'essentiel, mais elles manquent de profondeur quand tu veux vraiment creuser.

Prometheus + Grafana, c'est le standard de l'industrie. C'est ce qui tourne derrière Netflix, SoundCloud et la moitié des startups tech. Et le meilleur : c'est 100% open-source, 100% gratuit, et ça se déploie en Docker en quelques minutes.

Ce que tu obtiens :

- 📊 **Métriques en temps réel** : CPU, RAM, disque, réseau, température, custom metrics
- 📈 **Dashboards interactifs** : zoom, time range, variables, templating
- 🔔 **Alertes flexibles** : seuils, tendances, absences de données, multi-canal
- 🐳 **Monitoring Docker natif** : stats par conteneur, images, volumes
- 🔌 **Écosystème massif** : exporters pour MySQL, nginx, PostgreSQL, Redis, etc.

Si tu cherches une solution complète de [monitoring infrastructure](/zabbix-docker-monitoring-infrastructure/), Zabbix reste un excellent choix clé en main. Mais Prometheus + Grafana offrent plus de flexibilité pour ceux qui aiment bidouiller et optimiser.

## L'architecture de la stack en 2 minutes

Avant de copier-coller du YAML, comprenons ce qu'on déploie :

- **Prometheus** : le cœur. Il scrape (récupère) les métriques à intervalles réguliers via HTTP, les stocke dans sa base de données temporelle (TSDB), et évalue les règles d'alerte.
- **Grafana** : les yeux. Il se connecte à Prometheus et affiche des dashboards. Tu peux aussi brancher d'autres sources (InfluxDB, Loki, etc.).
- **Node Exporter** : l'espion système. Installé sur chaque machine à surveiller, il expose les métriques OS (CPU, RAM, disque, réseau, température).
- **cAdvisor** : l'espion Docker. Il expose les métriques des conteneurs : CPU, mémoire, I/O disque, réseau par container.
- **Alertmanager** : le messager. Il reçoit les alertes de Prometheus et les route vers email, Slack, Telegram, etc.

La communication est simple : Prometheus scrape tout le monde toutes les X secondes. Grafana lit Prometheus. Alertmanager reçoit les alertes. Pas de base de données externe compliquée, pas d'agent propriétaire.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose installés
- 2 Go de RAM minimum pour toute la stack (4 Go recommandés)
- Un accès root ou sudo
- Un reverse proxy si tu veux exposer Grafana en HTTPS (optionnel mais recommandé)

## Docker Compose : la stack complète

Crée un répertoire `monitoring` et ce `docker-compose.yml` :

```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: unless-stopped
    volumes:
      - ./prometheus:/etc/prometheus
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=15d'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
    ports:
      - "9090:9090"
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    restart: unless-stopped
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin123
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana_data:/var/lib/grafana
    ports:
      - "3000:3000"
    networks:
      - monitoring
    depends_on:
      - prometheus

  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    restart: unless-stopped
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.rootfs=/rootfs'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    ports:
      - "9100:9100"
    networks:
      - monitoring

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: cadvisor
    restart: unless-stopped
    privileged: true
    devices:
      - /dev/kmsg
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    ports:
      - "8080:8080"
    networks:
      - monitoring

  alertmanager:
    image: prom/alertmanager:latest
    container_name: alertmanager
    restart: unless-stopped
    volumes:
      - ./alertmanager:/etc/alertmanager
      - alertmanager_data:/alertmanager
    command:
      - '--config.file=/etc/alertmanager/alertmanager.yml'
      - '--storage.path=/alertmanager'
    ports:
      - "9093:9093"
    networks:
      - monitoring

volumes:
  prometheus_data:
  grafana_data:
  alertmanager_data:

networks:
  monitoring:
    driver: bridge
```

⚠️ **Change le mot de passe Grafana** (`GF_SECURITY_ADMIN_PASSWORD`) avant de lancer. `admin123`, c'est bien pour un test, pas pour la prod.

## Configuration de Prometheus

Crée le dossier `prometheus/` à côté du compose, et ce fichier `prometheus/prometheus.yml` :

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

rule_files:
  - "alert_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']
```

Et `prometheus/alert_rules.yml` pour tes premières alertes :

```yaml
groups:
  - name: alert_rules
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"
          description: "CPU usage is above 80% for more than 5 minutes."

      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage detected"
          description: "Memory usage is above 85% for more than 5 minutes."

      - alert: DiskSpaceLow
        expr: (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100 < 10
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Low disk space"
          description: "Less than 10% disk space remaining on root partition."

      - alert: ContainerDown
        expr: up{job="cadvisor"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "cAdvisor is down"
          description: "cAdvisor container is not reachable."
```

## Configuration d'Alertmanager

Crée `alertmanager/alertmanager.yml` :

```yaml
global:
  smtp_smarthost: 'smtp.gmail.com:587'
  smtp_from: 'ton-email@gmail.com'
  smtp_auth_username: 'ton-email@gmail.com'
  smtp_auth_password: 'ton-mot-de-passe-app'

route:
  receiver: 'default'
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h

receivers:
  - name: 'default'
    email_configs:
      - to: 'alertes@ton-domaine.com'
        send_resolved: true
```

🔧 **Astuce** : si tu n'as pas de SMTP, remplace la config email par un webhook vers Discord/Slack ou [n8n](/n8n-docker-workflow-automation/). Alertmanager supporte aussi PagerDuty, Telegram, OpsGenie, et plein d'autres.

## Lancer la stack

```bash
cd monitoring
docker compose up -d
```

Attends 30 secondes que tout démarre, puis vérifie :

- Prometheus : `http://IP_SERVEUR:9090`
- Grafana : `http://IP_SERVEUR:3000`
- cAdvisor : `http://IP_SERVEUR:8080`
- Alertmanager : `http://IP_SERVEUR:9093`

Va dans Prometheus → Status → Targets. Tu dois voir `node-exporter`, `cadvisor` et `prometheus` en vert (`UP`). Si c'est rouge, vérifie les noms de service et le réseau Docker.

## Configurer Grafana : data source + dashboards

1. Connecte-toi à Grafana (`admin` / le mot de passe que t'as mis)
2. Va dans **Connections → Data Sources → Add data source → Prometheus**
3. URL : `http://prometheus:9090`
4. Clique **Save & Test**

Maintenant les dashboards. Tu peux créer les tiens, mais pourquoi réinventer la roue ? Va dans **Dashboards → Import** et colle ces ID provenant de [grafana.com/dashboards](https://grafana.com/dashboards) :

- **Node Exporter Full** : `1860`, le dashboard complet pour le système (CPU, RAM, disque, réseau, température)
- **Docker and System Monitoring** : `893`, métriques Docker + système combinées
- **cAdvisor Exporter** : `14282`, stats détaillées par conteneur

En 5 minutes, tu as des graphes plus beaux que la moitié des startups parisiennes.

## Scraper d'autres machines : ajouter un Node Exporter distant

Pour monitorer un deuxième serveur, installe juste Node Exporter dessus (pas besoin de Prometheus ni Grafana) :

```bash
docker run -d \
  --name node-exporter \
  --restart unless-stopped \
  -p 9100:9100 \
  -v /proc:/host/proc:ro \
  -v /sys:/host/sys:ro \
  -v /:/rootfs:ro \
  prom/node-exporter:latest \
  --path.procfs=/host/proc \
  --path.rootfs=/rootfs \
  --path.sysfs=/host/sys
```

Puis ajoute dans `prometheus.yml` :

```yaml
  - job_name: 'node-exporter-remote'
    static_configs:
      - targets: ['IP_SERVEUR_2:9100']
```

Et recharge la config sans redémarrer Prometheus :

```bash
curl -X POST http://localhost:9090/-/reload
```

Boom, ton deuxième serveur apparaît dans Grafana.

## Exporters utiles pour aller plus loin

Prometheus est extensible à l'infini. Voici les exporters les plus utiles pour un homelab :

| Exporter | Métriques couvertes |
|----------|---------------------|
| [blackbox_exporter](https://github.com/prometheus/blackbox_exporter) | HTTP, ICMP, DNS, TCP probes (uptime, certificats SSL) |
| [mysqld_exporter](https://github.com/prometheus/mysqld_exporter) | Requêtes, connexions, replication, slow queries |
| [nginx_exporter](https://github.com/nginx/nginx-prometheus-exporter) | Requêtes HTTP, connexions actives, upstream status |
| [postgres_exporter](https://github.com/prometheus-community/postgres_exporter) | Transactions, connexions, vacuum, cache hits |
| [redis_exporter](https://github.com/oliver006/redis_exporter) | Commandes par seconde, mémoire, clients connectés |

Le principe est toujours le même : tu déploies l'exporter, tu ajoutes une cible dans `prometheus.yml`, et Grafana te fait des graphes.

## Sauvegarder les données et les dashboards

Les volumes Docker `prometheus_data` et `grafana_data` stockent tout. Pour sauvegarder :

```bash
# Sauvegarder les dashboards et data sources
docker exec grafana grafana-cli admin data-migration export

# Ou simplement copier les volumes
docker run --rm -v monitoring_grafana_data:/data -v $(pwd):/backup alpine tar czf /backup/grafana-backup.tar.gz -C /data .
docker run --rm -v monitoring_prometheus_data:/data -v $(pwd):/backup alpine tar czf /backup/prometheus-backup.tar.gz -C /data .
```

Grafana propose aussi le provisioning as-code : tu définis tes dashboards et data sources en JSON/YAML, et ils se déploient automatiquement au démarrage. C'est le Graal pour versionner ta config avec Git.

## Sécuriser l'accès

Par défaut, tout est en HTTP sans auth (sauf Grafana). En production :

1. **Mets un reverse proxy** ([Nginx Proxy Manager](/nginx-proxy-manager-docker-guide/), [Caddy](/caddy-docker-reverse-proxy-guide/) ou [Traefik](/traefik-reverse-proxy-docker/)) avec HTTPS
2. **Active l'authentification** sur Prometheus et Alertmanager via basic auth ou OAuth2
3. **Restreins les ports** avec un pare-feu ([UFW](/ufw-docker-pare-feu-linux/) ou [nftables](/nftables-docker-pare-feu-linux/))
4. **N'expose pas Prometheus sur Internet** : c'est une mine d'or pour un attaquant (liste des services, métriques internes)

Pour la sécurité globale de tes conteneurs, jette aussi un œil à mon guide [CrowdSec Docker](/crowdsec-docker-securite-collaborative/) qui détecte les comportements suspects en temps réel.

## Grafana vs Zabbix : quel outil choisir pour ton homelab ?

Si tu hésites avec [Zabbix](/zabbix-docker-monitoring-infrastructure/) que j'ai déjà présenté :

| Critère | Grafana + Prometheus | Zabbix |
|---------|----------------------|--------|
| Courbe d'apprentissage | Plus technique | Plus simple au début |
| Flexibilité des dashboards | ⭐⭐⭐ Irréprochable | ⭐⭐ Bonne mais moins interactive |
| Alertes | PromQL puissant, mais verbeux | Templates intégrés, prêt à l'emploi |
| Écosystème cloud-native | ⭐⭐⭐ Standard K8s | ⭐⭐ Supporté mais pas natif |
| Supervision réseau (SNMP) | Via exporters | ⭐⭐⭐ Natif et mature |
| Ressources | Leger (~500 Mo) | Plus gourmand (~1,5 Go) |
| Scénarios web (synthetics) | Via blackbox_exporter | ⭐⭐⭐ Natif |

**Mon conseil** : commence par Zabbix si tu veux du monitoring système "clé en main" sans te prendre la tête. Passe à Prometheus + Grafana quand tu veux des dashboards plus sexy, du monitoring applicatif poussé, ou que tu torientes vers Kubernetes.

## Troubleshooting : les problèmes courants

**Prometheus ne scrape pas mes cibles**

Vérifie que les conteneurs sont sur le même réseau Docker (`monitoring`), et que les noms de service correspondent bien à ceux définis dans `docker-compose.yml`.

**Grafana affiche "No data"**

Vérifie la data source (URL Prometheus), la plage de temps (peut-être que les données sont trop vieilles), et que Prometheus scrappe bien (`up == 1`).

**Les alertes ne partent pas**

Vérifie que `alertmanager.yml` est bien monté, que le réseau est accessible, et que la règle est bien chargée dans Prometheus → Alerts.

**cAdvisor ne remonte pas les métriques Docker**

Assure-toi que le conteneur cAdvisor est en `privileged: true` et que le socket Docker est bien monté en lecture seule.

**La base Prometheus devient énorme**

Ajoute `--storage.tsdb.retention.time=30d` ou moins dans la commande Prometheus. Par défaut, il garde tout.

## Conclusion

Prometheus + Grafana, c'est pas juste une stack de monitoring. C'est l'occasion de comprendre comment fonctionne l'observabilité moderne, sans passer par une carte bleue. Pour 0€, tu as un outil utilisé par les géants du web, qui scrape tout ce qui bouge, et qui te fait des dashboards dont tes collègues vont baver.

Le setup de base est en place en 15 minutes. Les dashboards s'enrichissent au fil du temps. Les alertes te réveillent la nuit (si tu les configures mal). Bref, c'est du vrai monitoring pro, auto-hébergé, et ça ne dépend de personne.

Maintenant, à toi de jouer. Lance le compose, importe tes dashboards, et commence à regarder ton infrastructure comme un pro. Parce que si tu ne mesures pas, tu ne peux pas améliorer.
