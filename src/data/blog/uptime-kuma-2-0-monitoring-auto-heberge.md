---
title: "Uptime Kuma 2.0 : le monitoring auto-hébergé qui remplace les services payants"
description: "Uptime Kuma 2.0 : MariaDB, Docker rootless et 90+ intégrations. Installation et migration V1→V2 pour ton homelab auto-hébergé."
pubDatetime: 2025-10-13 17:08:33+02:00
modDatetime: "2026-04-14T00:00:00+01:00"
author: Brandon Visca
tags:
  - homelab
  - monitoring
  - docker
  - uptime-kuma
  - guide
  - debutant
featured: true
draft: false
focusKeyword: Uptime Kuma
---
> 💡 **TL;DR**
> - Uptime Kuma 2.0 introduit MariaDB (exit SQLite pour les gros setups), Docker rootless et 90+ canaux de notification dont Home Assistant
> - La migration V1→V2 est automatique au démarrage mais nécessite une sauvegarde complète avant, prévois 30 min
> - Gratuit, open source, monitors illimités : c'est la solution évidente pour tout homelab qui se respecte

Tu en as marre de payer 50€/mois pour surveiller tes 10 services auto-hébergés ? Ou pire, tu utilises encore un script shell qui t'envoie des emails quand ça plante (et tu t'en rends compte 3 jours après) ?

**Uptime Kuma vient de passer en version 2.0** et franchement, ça envoie du lourd. MariaDB qui débarque, Docker rootless pour les paranos de la sécurité (coucou), et une flopée de nouvelles intégrations qui font que ton homelab va enfin avoir un vrai monitoring digne de ce nom.

Spoiler : si tu pensais que la version 1.x était déjà solide, prépare-toi à être surpris. Cette V2 n'est pas juste un lifting cosmétique, c'est une vraie refonte avec des breaking changes qui vont te forcer à lire ce guide (oui, même toi qui sautes toujours les docs).

## Table des matières

## Les nouveautés qui changent tout

### MariaDB : enfin de la scalabilité sérieuse

Jusqu'ici, Uptime Kuma tournait exclusivement sur SQLite. Pratique pour débuter, mais dès que tu surveilles 200+ endpoints, ça commence à ramer sévère. La V2 introduit le support MariaDB, et crois-moi, pour les gros déploiements, c'est le jour et la nuit.

**Concrètement, ça change quoi ?**

- Performances multipliées sur les requêtes complexes
- Stockage optimisé pour l'historique (fini les bases de 2 Go qui gonflent)
- Réplication possible pour la haute disponibilité
- Backups simplifiés avec les outils classiques MySQL

> ⚠️ **Attention :** la migration de SQLite vers MariaDB n'est pas automatique. Tu vas devoir suivre le guide officiel et te taper une petite session de SQL. Prévois 30 minutes et une sauvegarde complète avant de te lancer.

Si ton setup de monitoring fait partie d'une infrastructure plus large, cette évolution vers MariaDB s'intègre parfaitement dans [une stratégie de sécurisation serveur Linux](/securite-de-votre-serveur-linux/) où chaque composant est isolé et optimisé.

### Docker rootless : la sécurité avant tout

Les conteneurs tournent désormais sans privilèges root, ce qui réduit drastiquement la surface d'attaque en cas de compromission. Si tu héberges Uptime Kuma sur un VPS ou dans un cluster Kubernetes, c'est une évolution majeure.

Imagine qu'un attaquant exploite une faille dans Uptime Kuma. Avec un conteneur rootless :

- Il ne peut pas escalader ses privilèges sur l'hôte
- Il ne peut pas modifier les fichiers système
- Il ne peut pas installer des backdoors persistantes
- Il reste confiné dans son conteneur avec des droits limités

```bash
# Avant (V1) — conteneur avec root
docker run -d --name uptime-kuma -p 3001:3001 louislam/uptime-kuma:1

# Maintenant (V2) — conteneur rootless
docker run -d \
  --name uptime-kuma \
  --user 1000:1000 \
  -p 3001:3001 \
  -v /chemin/vers/data:/app/data \
  louislam/uptime-kuma:2
```

> 💡 **Astuce :** si tu utilises Nginx comme reverse proxy, sécurise tes [headers HTTP](/securiser-nginx-avec-headers-http/) pour compléter cette couche de protection.

### Nouvelles intégrations : Home Assistant, Brevo & Co

La V2 ajoute des intégrations avec Nextcloud Talk, Brevo et Home Assistant. Pour les passionnés de domotique, pouvoir déclencher des automatisations depuis Uptime Kuma, c'est une petite révolution.

**Cas d'usage concret :**

```yaml
# Automation Home Assistant
automation:
  - alias: "Alerte serveur down"
    trigger:
      platform: webhook
      webhook_id: uptime_kuma_alert
    action:
      - service: light.turn_on
        entity_id: light.bureau
        data:
          rgb_color: [255, 0, 0]
      - service: notify.mobile_app
        data:
          message: "Serveur {{ trigger.json.monitor_name }} est DOWN !"
```

Les autres nouveaux providers : **Brevo** (ex-Sendinblue), **Nextcloud Talk**, **Evolution API** (WhatsApp Business). Tu cumules maintenant **plus de 90 canaux de notification** différents. Impossible de rater une alerte.

### Interface modernisée et performances boostées

L'UI a pris un coup de jeune, surtout pour gérer des centaines de monitors.

- Chargement instantané des dashboards (même avec 500+ monitors)
- Dark mode amélioré (pour les yeux sensibles à 3h du mat)
- Interface mobile revue (enfin un vrai responsive)

## Breaking changes : ce qui va te faire mal

Autant être honnête : cette V2 contient plusieurs changements majeurs qui cassent la compatibilité.

### Les badges changent de format

Les endpoints de badges (uptime et ping) acceptent maintenant **uniquement** ces valeurs : `24h`, `30d`, `1y`.

```markdown
<!-- Ancien format (V1) — ne marche plus -->
![Uptime](https://uptime.mondomaine.com/api/badge/1/uptime/7)

<!-- Nouveau format (V2) -->
![Uptime](https://uptime.mondomaine.com/api/badge/1/uptime/24h)
```

Si tu affiches des badges dans ton site ou ta doc, mise à jour obligatoire.

### Fini la sauvegarde JSON

La fonction Backup/Restore depuis JSON a été supprimée. Tu dois maintenant sauvegarder directement le répertoire `data/`.

```bash
# Sauvegarde manuelle (à automatiser avec cron)
tar -czf uptime-kuma-backup-$(date +%Y%m%d).tar.gz /path/to/data/

# Ou avec Docker volume
docker run --rm -v uptime-kuma-data:/data -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz /data
```

### Notifications SMTP passent à LiquidJS

Les templates d'emails utilisent maintenant **LiquidJS** au lieu d'un parser maison. Si tu avais customisé tes emails, il faut tout refaire.

```liquid
<!-- Ancien template (V1) -->
Monitor {{monitor_name}} is DOWN!

<!-- Nouveau template (V2) avec LiquidJS -->
{{ monitor.name }} est DOWN depuis {{ downtime }}
URL: {{ monitor.url }}
Dernière vérification: {{ last_check | date: "%d/%m/%Y %H:%M" }}
```

### Navigateurs obsolètes : adieu Internet Explorer

Le support des navigateurs legacy a été retiré. Navigateurs supportés : Chrome/Edge 90+, Firefox 88+, Safari 14+.

## Installation et migration

### Installation fraîche (Docker recommandé)

```bash
# 1. Créer le volume de données
docker volume create uptime-kuma-data

# 2. Lancer Uptime Kuma 2.0
docker run -d \
  --name uptime-kuma \
  --restart unless-stopped \
  --user 1000:1000 \
  -p 3001:3001 \
  -v uptime-kuma-data:/app/data \
  louislam/uptime-kuma:2

# 3. Accéder à l'interface
# http://ton-ip:3001
```

**Configuration Nginx reverse proxy :**

```nginx
server {
    listen 443 ssl http2;
    server_name uptime.mondomaine.com;

    ssl_certificate /etc/letsencrypt/live/mondomaine.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mondomaine.com/privkey.pem;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Migration depuis V1 : procédure étape par étape

> ⚠️ **Important :** fais une sauvegarde complète avant de commencer !

```bash
# 1. Arrêter Uptime Kuma V1
docker stop uptime-kuma

# 2. Sauvegarder les données
docker run --rm -v uptime-kuma-data:/data -v $(pwd):/backup \
  alpine tar czf /backup/uptime-v1-backup.tar.gz /data

# 3. Récupérer la dernière image V2
docker pull louislam/uptime-kuma:2

# 4. Lancer la migration (automatique au démarrage)
docker run -d \
  --name uptime-kuma \
  --restart unless-stopped \
  --user 1000:1000 \
  -p 3001:3001 \
  -v uptime-kuma-data:/app/data \
  louislam/uptime-kuma:2

# 5. Surveiller les logs pendant la migration
docker logs -f uptime-kuma
# La migration peut prendre 5-15 minutes selon la taille de ta base
```

**Signes que ça se passe bien :**

```text
[2025-10-26 10:00:00] INFO: Starting migration from v1 to v2...
[2025-10-26 10:00:15] INFO: Migrating database schema...
[2025-10-26 10:05:42] INFO: Migration completed successfully!
[2025-10-26 10:05:43] INFO: Uptime Kuma is listening on http://0.0.0.0:3001
```

**Signes que ça part en cacahuète :**

```text
[2025-10-26 10:00:00] ERROR: Database lock detected
[2025-10-26 10:00:01] ERROR: Migration failed
```

Restaure ta sauvegarde et consulte les logs détaillés avec `docker logs uptime-kuma > debug.log`.

## Configuration optimale pour homelabbers

### Monitorer tes services auto-hébergés

Dans mon homelab, Uptime Kuma surveille 47 endpoints depuis 2 ans. Voici une config type pour un homelab classique :

```yaml
Monitors à créer :
├── HTTP(S) Monitor
│   ├── Nextcloud (https://cloud.maison.local)
│   ├── Jellyfin (https://media.maison.local)
│   ├── Home Assistant (https://home.maison.local)
│   └── Immich (https://photos.maison.local)
├── Ping Monitor
│   ├── Routeur principal (192.168.1.1)
│   ├── Switch manageable (192.168.1.10)
│   └── NAS Synology (192.168.1.50)
├── Port Monitor
│   ├── SSH serveur principal (22)
│   ├── WireGuard VPN (51820)
│   └── PostgreSQL (5432)
└── Docker Container Monitor
    ├── Uptime Kuma lui-même (meta!)
    ├── Traefik
    └── Watchtower
```

### Notifications intelligentes

Pour éviter le spam d'alertes (et la panique inutile à 3h du mat), configure des **groupes de monitors** :

```text
Groupe "Services Critiques" → Alerte immédiate (Telegram + Email)
├── Nextcloud
├── Serveur DNS
└── VPN WireGuard

Groupe "Services Optionnels" → Alerte après 5 minutes (Email uniquement)
├── Jellyfin
├── Immich
└── Wiki.js
```

## Dépannage : les erreurs fréquentes

### La migration échoue

**Symptôme :** le conteneur redémarre en boucle après le passage en V2.

```bash
# 1. Vérifier les logs détaillés
docker logs uptime-kuma 2>&1 | grep ERROR

# 2. Si corruption de base détectée
docker stop uptime-kuma
docker run --rm -v uptime-kuma-data:/data alpine rm /data/kuma.db-shm /data/kuma.db-wal
docker start uptime-kuma

# 3. En dernier recours : restaurer la V1 et réessayer
docker pull louislam/uptime-kuma:1
docker run -d --name uptime-kuma-v1 -v uptime-kuma-data:/app/data louislam/uptime-kuma:1
```

### Badges cassés après migration

**Symptôme :** tes badges affichent "Invalid duration".

```markdown
<!-- Remplace partout -->
/uptime/7    → /uptime/24h
/uptime/14   → /uptime/30d
/uptime/90   → /uptime/1y
```

### Permissions Docker avec rootless

**Symptôme :** erreur "Permission denied" au démarrage.

```bash
# 1. Vérifier l'UID du volume
docker run --rm -v uptime-kuma-data:/data alpine ls -la /data

# 2. Corriger les permissions si nécessaire
docker run --rm -v uptime-kuma-data:/data alpine chown -R 1000:1000 /data

# 3. Relancer avec le bon user
docker run -d --name uptime-kuma --user 1000:1000 ...
```

## Cas d'usage avancés

### Monitoring distribué avec MariaDB

Si tu gères plusieurs sites ou serveurs, tu peux centraliser le monitoring :

```text
Site A (Paris)      →  Uptime Kuma Local  →
Site B (Lyon)       →  Uptime Kuma Local  →  MariaDB Centralisé
Site C (Marseille)  →  Uptime Kuma Local  →
```

Un seul dashboard pour tout surveiller, avec réplication de la base pour la redondance.

### Intégration avec Grafana

Tu peux exporter les métriques vers Grafana via l'API :

```python
import requests

# Script à lancer en cron toutes les 5 minutes
response = requests.get('http://localhost:3001/api/monitors')
monitors = response.json()

for monitor in monitors:
    print(f"Monitor: {monitor['name']}, Status: {monitor['status']}")
```

### Alertes conditionnelles avancées

```javascript
// Alerter seulement si DOWN pendant >5 minutes ET en heures de bureau
if (downtime > 300 && currentHour >= 9 && currentHour <= 18) {
    sendAlert("Telegram");
    sendAlert("Email");
} else {
    sendAlert("Email"); // Juste l'email la nuit
}
```

## Uptime Kuma vs alternatives

| Critère | Uptime Kuma | UptimeRobot | Pingdom | StatusCake |
|---|---|---|---|---|
| Prix | Gratuit | 58€/an | 120€/an | 75€/an |
| Auto-hébergé | ✅ Oui | Non | Non | Non |
| Monitors illimités | ✅ Oui | 50 max | 10 max | 30 max |
| Notifications | 90+ canaux | 7 canaux | 15 canaux | 10 canaux |
| Open Source | ✅ MIT | Propriétaire | Propriétaire | Propriétaire |

Pour l'auto-hébergement, Uptime Kuma écrase la concurrence. Pour du monitoring externe depuis plusieurs régions géographiques, les services payants gardent un avantage. C'est là qu'[UptimeRobot](/uptimerobot-guide-complet-monitoring-infrastructure/) complète bien le setup.

## Conclusion

Uptime Kuma 2.0 franchit un cap. MariaDB règle le problème de scalabilité SQLite, le Docker rootless ferme une surface d'attaque réelle, et les 90+ intégrations couvrent tous les cas d'usage homelab.

Dans mon homelab, ça tourne H24 depuis 2 ans sur 47 endpoints. Depuis le passage en V2, j'ai divisé par 2 les faux positifs et la base SQLite gonflée a disparu avec MariaDB. Si t'auto-héberges ne serait-ce que 5 services, t'as **zéro excuse** pour pas l'installer.

Installe-le, configure tes groupes de monitors et tes alertes Telegram, et dors enfin tranquille.

## Pour aller plus loin

- [Sécuriser ton serveur Linux — SSH, firewall, fail2ban](/securite-de-votre-serveur-linux/)
- [Documentation officielle Uptime Kuma](https://github.com/louislam/uptime-kuma/wiki) : wiki GitHub complet
- [Guide de migration V1→V2](https://github.com/louislam/uptime-kuma/wiki/Migration-From-v1-To-v2) : procédure officielle
