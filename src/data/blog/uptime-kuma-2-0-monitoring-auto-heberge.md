---
title: Uptime Kuma 2.0 débarque avec MariaDB, Docker rootless et notifications Home Assistant. Le monitoring auto-hébergé devient enfin une vraie alternative pro.
pubDatetime: 2025-10-13T17:08:33+02:00
author: Brandon Visca
tags:
  - guide
  - monitoring
  - debutant
featured: true
draft: false
focusKeyword: monitoring
---
# Uptime Kuma 2.0 : Le Monitoring Auto-Hébergé qui Fait Trembler les Services Payants


## Introduction : Quand un outil gratuit met la pression aux pros

Tu en as marre de payer 50€/mois pour surveiller tes 10 services auto-hébergés ? Ou pire, tu utilises encore un script shell qui t'envoie des emails quand ça plante (et tu t'en rends compte 3 jours après) ?

**Uptime Kuma vient de passer en version 2.0** et franchement, ça envoie du lourd. MariaDB qui débarque, Docker rootless pour les paranos de la sécurité (coucou), et une flopée de nouvelles intégrations qui font que ton homelab va enfin avoir un vrai monitoring digne de ce nom.

Spoiler : si tu pensais que la version 1.x était déjà solide, prépare-toi à être surpris. Cette V2 n'est pas juste un lifting cosmétique, c'est une vraie refonte avec des breaking changes qui vont te forcer à lire ce guide (oui, même toi qui sautes toujours les docs).

## Table of content


---

## 🆕 Les nouveautés qui changent tout

### 1. MariaDB : Enfin de la scalabilité sérieuse

Jusqu'ici, Uptime Kuma tournait exclusivement sur SQLite. Pratique pour débuter, mais dès que tu surveilles 200+ endpoints, ça commence à ramer sévère. La V2 introduit le support MariaDB, et crois-moi, pour les gros déploiements, c'est le jour et la nuit.

**Concrètement, ça change quoi ?**

- 🚀 **Performances multipliées** sur les requêtes complexes
- 📊 **Stockage optimisé** pour l'historique (fini les bases de 2 Go qui gonflent)
- 🔄 **Réplication possible** pour la haute disponibilité
- 💾 **Backups simplifiés** avec les outils classiques MySQL

**Le piège à éviter :** La migration de SQLite vers MariaDB n'est pas automatique. Tu vas devoir suivre le guide officiel et te taper une petite session de SQL. Prévois 30 minutes et une sauvegarde complète avant de te lancer.

Si ton setup de monitoring fait partie d'une infrastructure plus large, cette évolution vers MariaDB s'intègre parfaitement dans [une stratégie de sécurisation serveur Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/) où chaque composant est isolé et optimisé.

---

### 2. Docker rootless : La sécurité avant tout

Les conteneurs tournent désormais sans privilèges root, ce qui réduit drastiquement la surface d'attaque en cas de compromission. Si tu héberges Uptime Kuma sur un VPS ou dans un cluster Kubernetes, c'est une évolution majeure.

**Pourquoi c'est important ?**

Imagine qu'un attaquant exploite une faille dans Uptime Kuma. Avec un conteneur rootless :

- ❌ Il ne peut **pas** escalader ses privilèges sur l'hôte
- ❌ Il ne peut **pas** modifier les fichiers système
- ❌ Il ne peut **pas** installer des backdoors persistantes
- ✅ Il reste confiné dans son conteneur avec des droits limités

```bash
# Avant (V1) - Conteneur avec root
docker run -d --name uptime-kuma -p 3001:3001 louislam/uptime-kuma:1

# Maintenant (V2) - Conteneur rootless
docker run -d \
  --name uptime-kuma \
  --user 1000:1000 \
  -p 3001:3001 \
  -v /chemin/vers/data:/app/data \
  louislam/uptime-kuma:2
```

**Attention :** Si tu utilises Nginx comme reverse proxy, pense à [sécuriser tes headers HTTP](https://brandonvisca.com/securiser-nginx-avec-headers-http/) pour compléter cette couche de protection.

---

### 3. Nouvelles intégrations notifications : Home Assistant, Brevo & Co

La V2 ajoute des intégrations avec Nextcloud Talk, Brevo et Home Assistant. Pour les passionnés de domotique, pouvoir déclencher des automatisations Home Assistant depuis Uptime Kuma, c'est une petite révolution.

**Cas d'usage concret :**

```yaml
# Exemple automation Home Assistant
automation:
  - alias: "Alerte serveur down"
    trigger:
      platform: webhook
      webhook_id: uptime_kuma_alert
    action:
      - service: light.turn_on
        entity_id: light.bureau
        data:
          rgb_color: [255, 0, 0]  # Rouge = problème
      - service: notify.mobile_app
        data:
          message: "🚨 Serveur {{ trigger.json.monitor_name }} est DOWN !"
```

Les autres nouveaux providers :

- **Brevo** (ex-Sendinblue) : Pour les emails transactionnels pros
- **Nextcloud Talk** : Notifications dans ton instance Nextcloud
- **Evolution API** : Pour WhatsApp Business

Tu cumules maintenant **plus de 90 canaux de notification** différents. Impossible de rater une alerte.

---

### 4. Interface modernisée et performances boostées

L'UI a pris un coup de jeune, surtout pour gérer des centaines de monitors. Les performances ont été améliorées, notamment sur le chargement des listes importantes.

**Ce qui change visuellement :**

- ⚡ Chargement instantané des dashboards (même avec 500+ monitors)
- 🎨 Dark mode amélioré (pour les yeux sensibles à 3h du mat)
- 📱 Interface mobile revue (enfin un vrai responsive)
- 🌍 Support de nouvelles langues dont le slovaque (essentiel ?)

---

## ⚠️ Breaking changes : Ce qui va te faire mal

Autant être honnête : cette V2 contient plusieurs changements majeurs qui cassent la compatibilité. Voici ce qui va te concerner :

### 1. Les badges changent de format

Les endpoints de badges (uptime et ping) acceptent maintenant **uniquement** ces valeurs :

- `24` ou `24h` (24 heures)
- `30d` (30 jours)
- `1y` (1 an)

```markdown
<!-- Ancien format (V1) - Ne marche plus ❌ -->
![Uptime](https://uptime.mondomaine.com/api/badge/1/uptime/7)

<!-- Nouveau format (V2) - OK ✅ -->
![Uptime](https://uptime.mondomaine.com/api/badge/1/uptime/24h)
```

**Action requise :** Si tu affiches des badges dans ton site ou ta doc, mise à jour obligatoire.

---

### 2. Fini la sauvegarde JSON

La fonction Backup/Restore depuis JSON a été supprimée. Maintenant, tu dois sauvegarder directement le répertoire `data/`.

```bash
# Sauvegarde manuelle (à automatiser avec cron)
tar -czf uptime-kuma-backup-$(date +%Y%m%d).tar.gz /path/to/data/

# Ou avec Docker volume
docker run --rm -v uptime-kuma-data:/data -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz /data
```

**Astuce pro :** Intègre ça dans ton setup de gestion automatique, exactement comme expliqué dans le [guide de gestion du swap Linux](https://brandonvisca.com/guide-swap-linux-configuration-optimisation/) où l'automatisation est clé.

---

### 3. Notifications SMTP passent à LiquidJS

Les templates d'emails utilisent maintenant **LiquidJS** au lieu d'un parser maison. Si tu avais customisé tes emails, il faut tout refaire.

```liquid
<!-- Ancien template (V1) -->
Monitor {{monitor_name}} is DOWN!

<!-- Nouveau template (V2) avec LiquidJS -->
{{ monitor.name }} est DOWN depuis {{ downtime }}
URL: {{ monitor.url }}
Dernière vérification: {{ last_check | date: "%d/%m/%Y %H:%M" }}
```

---

### 4. Navigateurs obsolètes : Adieu Internet Explorer

Le support des navigateurs legacy a été retiré. Si t'es encore sous IE11 ou Edge Legacy... ben désolé, mais c'est 2025 quoi.

**Navigateurs supportés :**

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

---

## 📦 Installation et migration : Le guide complet

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

Si tu exposes Uptime Kuma sur Internet, un reverse proxy est indispensable. Voici une conf Nginx sécurisée qui s'appuie sur les [bonnes pratiques de configuration Nginx](https://brandonvisca.com/nginx-location-bloc-et-securite/) :

```nginx
server {
    listen 443 ssl http2;
    server_name uptime.mondomaine.com;

    ssl_certificate /etc/letsencrypt/live/mondomaine.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mondomaine.com/privkey.pem;

    # Headers de sécurité
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

---

### Migration depuis V1 : Procédure étape par étape

**⚠️ IMPORTANT : Fais une sauvegarde complète avant de commencer !**

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

```
[2025-10-26 10:00:00] INFO: Starting migration from v1 to v2...
[2025-10-26 10:00:15] INFO: Migrating database schema...
[2025-10-26 10:05:42] INFO: Migration completed successfully!
[2025-10-26 10:05:43] INFO: Uptime Kuma is listening on http://0.0.0.0:3001
```

**Signes que ça part en cacahuète :**

```
[2025-10-26 10:00:00] ERROR: Database lock detected
[2025-10-26 10:00:01] ERROR: Migration failed
```

➡️ **Solution :** Restaure ta sauvegarde et consulte les logs détaillés avec `docker logs uptime-kuma > debug.log`.

---

## 🎯 Configuration optimale pour homelabbers

### Monitorer tes services auto-hébergés

Voici une config type pour surveiller un homelab classique :

```yaml
Monitors à créer :
├── HTTP(S) Monitor
│   ├── Nextcloud (https://cloud.maison.local)
│   ├── Jellyfin (https://media.maison.local)
│   ├── Home Assistant (https://home.maison.local)
│   └── Immich (https://photos.maison.local)
│
├── Ping Monitor
│   ├── Routeur principal (192.168.1.1)
│   ├── Switch manageable (192.168.1.10)
│   └── NAS Synology (192.168.1.50)
│
├── Port Monitor
│   ├── SSH serveur principal (22)
│   ├── WireGuard VPN (51820)
│   └── PostgreSQL (5432)
│
└── Docker Container Monitor
    ├── Uptime Kuma lui-même (meta!)
    ├── Traefik
    └── Watchtower
```

### Notifications intelligentes

Pour éviter le spam d'alertes (et la panique inutile à 3h du mat), configure des **groupes de monitors** :

```
Groupe "Services Critiques" → Alerte immédiate (Telegram + Email)
├── Nextcloud
├── Serveur DNS
└── VPN WireGuard

Groupe "Services Optionnels" → Alerte après 5 minutes (Email uniquement)
├── Jellyfin
├── Immich
└── Wiki.js
```

---

## 🔧 Dépannage : Les erreurs fréquentes

### Problème 1 : La migration échoue

**Symptôme :** Le conteneur redémarre en boucle après le passage en V2.

**Solution :**

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

---

### Problème 2 : Badges cassés après migration

**Symptôme :** Tes badges affichent "Invalid duration".

**Solution :** Mets à jour tous tes badges avec les nouvelles valeurs autorisées :

```markdown
<!-- Remplace partout -->
/uptime/7    → /uptime/24h
/uptime/14   → /uptime/30d
/uptime/90   → /uptime/1y
```

---

### Problème 3 : Permissions Docker avec rootless

**Symptôme :** Erreur "Permission denied" au démarrage.

**Solution :**

```bash
# 1. Vérifier l'UID du volume
docker run --rm -v uptime-kuma-data:/data alpine ls -la /data

# 2. Corriger les permissions si nécessaire
docker run --rm -v uptime-kuma-data:/data alpine chown -R 1000:1000 /data

# 3. Relancer avec le bon user
docker run -d --name uptime-kuma --user 1000:1000 ...
```

---

## 💡 Cas d'usage avancés

### 1. Monitoring distribué avec MariaDB

Si tu gères plusieurs sites ou serveurs, tu peux centraliser le monitoring :

```
Site A (Paris)        →  Uptime Kuma Local  →
Site B (Lyon)         →  Uptime Kuma Local  →  MariaDB Centralisé
Site C (Marseille)    →  Uptime Kuma Local  →
```

Avantage : Un seul dashboard pour tout surveiller, avec réplication de la base pour la redondance.

---

### 2. Intégration avec Grafana

Tu peux exporter les métriques vers Grafana via l'API :

```python
import requests
import json

# Script à lancer en cron toutes les 5 minutes
response = requests.get('http://localhost:3001/api/monitors')
monitors = response.json()

# Envoyer vers Prometheus/InfluxDB
for monitor in monitors:
    print(f"Monitor: {monitor['name']}, Status: {monitor['status']}")
```

---

### 3. Alertes conditionnelles avancées

Avec la V2, tu peux créer des alertes sophistiquées :

```javascript
// Exemple : Alerter seulement si DOWN pendant >5 minutes ET en heures de bureau
if (downtime > 300 && currentHour >= 9 && currentHour <= 18) {
    sendAlert("Telegram");
    sendAlert("Email");
} else {
    sendAlert("Email"); // Juste l'email la nuit
}
```

---

## 📊 Alternatives et comparaisons

### Uptime Kuma VS autres solutions

|Critère|Uptime Kuma|Uptime Robot|Pingdom|StatusCake|
|---|---|---|---|---|
|**Prix**|Gratuit|58€/an (50 monitors)|120€/an|75€/an|
|**Auto-hébergé**|✅ Oui|❌ Non|❌ Non|❌ Non|
|**Monitors illimités**|✅ Oui|❌ 50 max|❌ 10 max|❌ 30 max|
|**Personnalisation**|✅ Totale|❌ Limitée|❌ Limitée|❌ Limitée|
|**Notifications**|90+ canaux|7 canaux|15 canaux|10 canaux|
|**Docker**|✅ Oui|❌ N/A|❌ N/A|❌ N/A|
|**Open Source**|✅ MIT|❌ Propriétaire|❌ Propriétaire|❌ Propriétaire|

**Verdict :** Pour l'auto-hébergement, Uptime Kuma écrase la concurrence. Pour du monitoring externe depuis plusieurs régions géographiques, les services payants gardent un avantage.

---

## 🎓 Pour aller plus loin

### Articles complémentaires sur brandonvisca.com

Si tu mets en place Uptime Kuma dans ton homelab, ces guides vont t'aider :

1. **[Sécuriser ton serveur Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/)** : Indispensable avant d'exposer Uptime Kuma sur Internet. Firewall, fail2ban, SSH durci... tout y est.
    
2. **[Configuration avancée Nginx](https://brandonvisca.com/nginx-location-bloc-et-securite/)** : Pour mettre Uptime Kuma derrière un reverse proxy propre avec Let's Encrypt.
    
3. **[Gestion du Swap Linux](https://brandonvisca.com/guide-swap-linux-configuration-optimisation/)** : Parce qu'un serveur de monitoring qui swap, c'est ballot. Optimise ta RAM.
    
4. **[Scavenging DNS Windows](https://brandonvisca.com/dns-scavenging-windows-server-guide/)** : Si tu surveilles des serveurs Windows, comprendre le nettoyage DNS automatique est crucial pour éviter les faux positifs.
    

### Ressources externes

- 📖 [Documentation officielle Uptime Kuma](https://github.com/louislam/uptime-kuma/wiki)
- 🔧 [Guide de migration V1→V2](https://github.com/louislam/uptime-kuma/wiki/Migration-From-v1-To-v2)
- 💬 [Discord communauté](https://discord.gg/uptime-kuma)
- 🐛 [Signaler un bug](https://github.com/louislam/uptime-kuma/issues)

---

## Conclusion : Le monitoring gratuit devient adulte

Uptime Kuma 2.0 franchit un cap avec MariaDB, Docker rootless et des intégrations professionnelles. C'est simple : si t'auto-héberges ne serait-ce que 5 services, t'as **zéro excuse** pour pas installer Uptime Kuma.

**Les vrais plus de cette V2 :**

- ✅ Scalabilité enfin au rendez-vous (merci MariaDB)
- ✅ Sécurité renforcée (rootless Docker = game changer)
- ✅ Intégrations qui font sens (Home Assistant ❤️)
- ✅ Performances qui tiennent la charge

**Les trucs relous :**

- ⚠️ Migration pas 100% automatique (prévois 1h)
- ⚠️ Breaking changes sur les badges (mise à jour manuelle)
- ⚠️ Documentation encore partielle sur certains points

Dans mon homelab, Uptime Kuma tourne H24 depuis 2 ans et surveille 47 endpoints (Nextcloud, Jellyfin, Home Assistant, des VPS, mon routeur, etc.). Depuis le passage en V2, j'ai divisé par 2 les faux positifs et la base SQLite gonflée a disparu avec MariaDB.

**Mon conseil final :** Teste d'abord en parallèle avec ton monitoring existant pendant 2 semaines. Tu verras vite si ça tient la charge et si les alertes sont pertinentes. Et si t'as des doutes sur la sécu, relis mon [guide complet sur la sécurisation Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/).

Allez, au boulot, et que tes dashboards restent en vert ! 🟢
