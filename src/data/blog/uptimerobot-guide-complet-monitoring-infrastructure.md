---
title: "UptimeRobot : surveille ton infrastructure gratuitement (guide 2026)"
description: "UptimeRobot : surveille ton infrastructure gratuitement avec alertes Slack et pages de statut. Guide 2026, 50 moniteurs gratuits, API incluse."
pubDatetime: "2025-10-22T15:42:22+02:00"
modDatetime: "2026-04-14T00:00:00+01:00"
author: Brandon Visca
tags:
  - uptimerobot
  - monitoring
  - sysadmin
  - devops
  - guide
  - intermediaire
featured: false
draft: false
focusKeyword: UptimeRobot
---
> 💡 **TL;DR**
> - UptimeRobot surveille tes sites, serveurs et services depuis l'extérieur — si ça tombe, tu es prévenu en 5 minutes max (email, Slack, Discord, SMS)
> - Plan gratuit : 50 moniteurs, vérifications toutes les 5 minutes, pages de statut publiques incluses
> - API complète pour automatiser la création de monitors via script Python ou Terraform

*Tu as déjà eu cette sueur froide en découvrant que ton site est down depuis 3 heures ? Ou pire, c'est un client qui te prévient ?*

La surveillance d'infrastructure, c'est comme l'assurance auto : personne ne trouve ça sexy jusqu'au jour où tu en as vraiment besoin. Sauf que contrairement à l'assurance, **un bon système de monitoring peut t'épargner bien plus qu'une facture de carrosserie**.

Je parle de :

- **Ta réputation** : un site down = des clients mécontents
- **Ton sommeil** : te réveiller à 3h du mat' pour un serveur tombé, ça use
- **Ton temps** : réparer en réactif prend 10x plus de temps que prévenir

J'utilise UptimeRobot depuis des années sur mon homelab et pour les sites de clients. Plan gratuit, zéro config serveur, alertes Discord en 5 minutes : c'est le premier outil que j'installe sur tout projet qui part en prod.

## Table des matières

## Qu'est-ce qu'UptimeRobot ?

**UptimeRobot** est un service de surveillance de disponibilité qui vérifie régulièrement que tes sites, serveurs et services sont bien vivants. Si quelque chose tombe, tu es alerté immédiatement par email, SMS, Slack, Discord ou n'importe quel webhook que tu configures.

### Pourquoi UptimeRobot plutôt qu'une autre solution ?

**Les avantages :**

- ✅ **Plan gratuit généreux** : 50 moniteurs, vérifications toutes les 5 minutes
- ✅ **Zero configuration serveur** : pas besoin d'installer d'agent
- ✅ **Surveillance externe** : détecte les problèmes réseau/DNS que tu ne verrais pas en interne
- ✅ **Interface simple** mais puissante
- ✅ **API complète** pour automatiser tout ce qui bouge
- ✅ **Pages de statut publiques** (comme status.github.com)

**Ce qu'il ne fait PAS :**

- ❌ Monitoring de métriques système (CPU, RAM, disque) → pour ça, regarde Prometheus/Grafana
- ❌ Logs applicatifs détaillés
- ❌ Surveillance réseau interne complexe

### Pour qui ?

- **Sysadmins débutants** qui veulent une solution rapide et fiable
- **Freelances** qui gèrent plusieurs sites clients
- **Équipes DevOps** qui veulent un monitoring externe en complément
- **Homelabbers** qui auto-hébergent des services

> 💡 **À savoir :** UptimeRobot vérifie depuis l'extérieur. Si ton site fonctionne localement mais est inaccessible depuis Internet (DNS, firewall…), tu seras alerté. C'est exactement ce qu'on veut.

[**Créer un compte UptimeRobot gratuitement**](https://uptimerobot.com/?red=brando5751b9)

## Configuration initiale

### Créer ton premier monitor en 2 minutes

1. **Inscription** : Va sur [UptimeRobot](https://uptimerobot.com/?red=brando5751b9), crée un compte (email + mot de passe)
2. **Premier monitor** :
   - Clique sur « Add New Monitor »
   - **Monitor Type** : « HTTP(s) »
   - **Friendly Name** : « Site Prod – brandonvisca.com » (sois explicite, ton toi de 3h du mat' te remerciera)
   - **URL** : `https://brandonvisca.com`
   - **Monitoring Interval** : 5 minutes (gratuit) ou 1 minute (plan payant)
3. **Alert Contacts** : Configure au moins ton email principal

En moins de 2 minutes, ton site est surveillé. Si demain ton serveur tombe, tu es prévenu dans les 5 minutes max.

### Checklist de démarrage

✅ Monitor principal configuré (site/app la plus critique)
✅ Email d'alerte validé (check tes spams !)
✅ Période de maintenance planifiée (si t'as des maintenances régulières)
✅ Page de statut publique activée (optionnel mais pro)

## Types de monitoring disponibles

UptimeRobot ne fait pas que pinger ton site. Il supporte plusieurs protocoles et méthodes de vérification.

### HTTP(s) — Le classique

Envoie une requête GET à ton URL, vérifie le code HTTP (200 = OK) et peut chercher un texte spécifique dans la page.

**Cas d'usage :** sites WordPress, applications web, API REST.

**Configuration avancée :**

```text
Monitor Type: HTTP(s)
URL: https://brandonvisca.com/health-check
Keyword Monitoring: Contains "status:ok"
```

### Ping — Pour les serveurs bruts

Envoie un ping ICMP vers ton serveur. Utile pour surveiller des machines qui n'exposent pas de service HTTP (serveurs de base de données, VPN, etc.).

**Cas d'usage :** VPS, NAS, serveurs de backup, machines sur réseau privé exposées via tunnel.

### Port Monitoring — Services spécifiques

Vérifie qu'un port TCP est ouvert et répond. Parfait pour les services non-HTTP.

```text
Monitor Type: Port
Port: 22
Server: 192.168.1.100
```

Si ton serveur de base de données externe tombe, tu es prévenu immédiatement.

### Keyword Monitoring — Surveillance de contenu

Le plus sous-estimé. UptimeRobot peut vérifier la présence (ou l'absence) d'un texte sur ta page.

**Cas d'usage concrets :**

- Vérifier qu'il n'y a pas « Error » ou « Warning » dans ta page
- Confirmer que « Login » est présent (sinon = page d'erreur)
- Détecter si un hacker a modifié du contenu

**Exemple :**

```text
URL: https://monsite.com
Keyword Type: NOT EXISTS
Keyword Value: "Fatal error"
```

## Système d'alertes avancé

### Canaux d'alerte multiples

UptimeRobot supporte nativement : email, SMS, Slack, Discord, Telegram, PagerDuty, webhooks personnalisés.

**Configuration Slack :**

```text
Webhook URL: https://hooks.slack.com/services/T00000000/B00000000/XXXX
Channel: #monitoring
Alert When: Down, Up, Started
```

**Webhook personnalisé**, pour envoyer vers n'importe quelle API (PagerDuty, ton propre système…) :

```json
POST https://monapi.com/alert
{
  "monitorID": "*monitorID*",
  "monitorURL": "*monitorURL*",
  "alertType": "*alertType*",
  "alertDateTime": "*alertDateTime*"
}
```

### Alertes conditionnelles — éviter le spam

Configure des fenêtres de maintenance pour silencer les alertes pendant les opérations planifiées :

```text
Maintenance Window: Dimanche 02h00 - 04h00
Silenced: true
```

Pendant cette période, aucune alerte même si le service est down.

### Escalade progressive

**Plan payant uniquement**, mais puissant pour les équipes :

```text
Étape 1 (0 min)  : Email au sysadmin
Étape 2 (15 min) : Si toujours down → SMS manager
Étape 3 (30 min) : Si toujours down → Appel téléphonique + email direction
```

## Intégration API et automatisation

### Créer des monitors en masse via script

Tu gères 20 sites clients ? Script Python pour tout créer en une fois :

```python
import requests

API_KEY = "ur123456-abcdef1234567890"
API_URL = "https://api.uptimerobot.com/v2/newMonitor"

sites = [
    {"name": "Site Client 1", "url": "https://client1.com"},
    {"name": "Site Client 2", "url": "https://client2.com"},
    # ... 18 autres
]

for site in sites:
    payload = {
        "api_key": API_KEY,
        "format": "json",
        "type": 1,       # HTTP(s)
        "friendly_name": site["name"],
        "url": site["url"],
        "interval": 300  # 5 minutes
    }
    response = requests.post(API_URL, data=payload)
    print(f"Monitor créé pour {site['name']}: {response.json()}")
```

En 10 secondes, tes 20 sites sont monitorés.

### Récupérer les statuts pour un dashboard perso

```bash
curl -X POST https://api.uptimerobot.com/v2/getMonitors \
  -d "api_key=ur123456-abcdef1234567890" \
  -d "format=json"
```

**Réponse :**

```json
{
  "monitors": [
    {
      "id": 123456,
      "friendly_name": "Site Prod",
      "url": "https://brandonvisca.com",
      "status": 2,
      "all_time_uptime_ratio": "99.98"
    }
  ]
}
```

`status: 2` = Up, `status: 9` = Down. Intègre ça dans un widget sur ton dashboard. Tes clients adorent voir « 99.98% uptime » en gros.

### Intégration avec Terraform

Pour les fanas d'Infrastructure as Code :

```hcl
provider "uptimerobot" {
  api_key = var.uptimerobot_api_key
}

resource "uptimerobot_monitor" "prod_site" {
  friendly_name = "Site Production"
  url           = "https://brandonvisca.com"
  type          = "http"
  interval      = 300
}
```

## Cas d'usage concrets

### Freelance : surveiller 30 sites clients

Avec le plan gratuit (50 moniteurs), tu couvres facilement 30 clients. Utilise le script Python ci-dessus pour créer tous les monitors d'un coup, puis configure des alertes séparées par client (webhook Slack distinct par client ou email dédié).

> ⚠️ **Attention :** configure bien les contacts d'alerte avant de livrer un site. Rien de pire qu'un client down et toi qui n'es pas notifié.

### Startup : stack complète à surveiller

```text
1. https://app.startup.com          → HTTP(s)
2. https://api.startup.com/health   → HTTP(s) + Keyword "ok"
3. db.startup.com:5432              → Port
4. smtp.startup.com:25              → Port
5. cdn.startup.com                  → HTTP(s)
```

**Alertes :**

- App/API down → SMS + Slack #incidents (critique)
- DB/SMTP down → Slack #tech (important mais pas critique côté user)
- CDN down → Email (Cloudflare gère, juste pour info)

### Homelab : auto-hébergement

Tu auto-héberges Nextcloud, Plex, Jellyfin, Pi-hole chez toi ? UptimeRobot est parfait pour détecter quand un service crash ou quand ta box redémarre.

```text
https://nextcloud.mondomaine.com
https://plex.mondomaine.com
http://192.168.1.10:8096   # Jellyfin
http://192.168.1.2         # Pi-hole
```

Ajoute un endpoint `/health` à tes apps custom avec du Keyword Monitoring pour détecter les erreurs applicatives :

```php
// /health.php
header('Content-Type: application/json');

$status = [
    'database' => check_db(),
    'cache'    => check_redis(),
    'disk'     => check_disk_space()
];

if (all_ok($status)) {
    http_response_code(200);
    echo json_encode(['status' => 'ok']);
} else {
    http_response_code(500);
    echo json_encode(['status' => 'error', 'details' => $status]);
}
```

## UptimeRobot vs alternatives

### vs Uptime Kuma (self-hosted)

| | UptimeRobot | Uptime Kuma |
|---|---|---|
| Hébergement | Cloud (externe) | Self-hosted |
| Prix | Gratuit (50 monitors) | Gratuit (illimité) |
| Surveillance externe | ✅ Depuis les serveurs UR | ❌ Depuis ton propre serveur |
| Setup | 2 minutes | 30 minutes (Docker) |
| Idéal pour | Débutants, freelances | Homelabbers qui veulent tout maîtriser |

Si tu veux une surveillance vraiment externe (détecter que ton IP est bloquée, ton DNS KO, etc.), Uptime Kuma self-hosted ne peut pas faire ça. C'est le point fort d'UptimeRobot.

### vs Pingdom

Pingdom coûte 40-50$/mois pour des fonctionnalités comparables. La migration vers UptimeRobot est simple :

1. **Export Pingdom** (pas d'export officiel) :

```bash
curl -u email:password https://api.pingdom.com/api/3.1/checks
```

2. **Import UptimeRobot** via API (script Python section précédente)
3. **Période de transition** : garde les deux actifs 1 semaine, compare les alertes
4. **Bascule** : désactive Pingdom

**Économie : 43$/mois → 0$/mois (plan gratuit) ou 7$/mois (plan pro)**

### vs Zabbix / Prometheus

Zabbix et Prometheus sont des outils de monitoring système (métriques CPU/RAM/disque/réseau). Ils ne font pas de surveillance externe. Ils mesurent ce qui se passe à l'intérieur du serveur.

UptimeRobot + Prometheus/Grafana = la stack complète. L'un ne remplace pas l'autre.

## Bonnes pratiques et pièges à éviter

### ✅ Bonnes pratiques

**1. Endpoint `/health` dédié**

Ne monitore pas la homepage si t'as une app dynamique. La homepage peut charger depuis le cache même si la DB est morte. Crée un endpoint `/health` qui vérifie vraiment les composants critiques.

**2. Maintenances planifiées**

Tu fais une mise à jour tous les dimanches matin ? Configure UptimeRobot pour ne pas t'alerter pendant cette période :

```text
Maintenance Window: Dimanche 02:00 - 04:00 UTC
```

**3. Runbook dans les notes du monitor**

Ajoute directement dans les notes du monitor ce qu'il faut faire si ça tombe :

```text
Monitor: Site Production
Notes:
- Si down : Check https://status.ovh.com (hébergeur)
- Restart: ssh user@server "systemctl restart nginx"
- Escalade si > 15min : tel +33612345678 (manager)
```

**4. Teste tes alertes régulièrement**

Clique sur « Test Alert Contact » toutes les semaines. Vérifie que ton email/Slack/SMS fonctionne toujours.

### ❌ Pièges à éviter

**1. Monitorer uniquement la homepage** — voir bonnes pratiques ci-dessus.

**2. Trop de monitors = alerte fatigue** — 50 monitors gratuits ne veut pas dire en créer 50. Commence par 5-10 services critiques, ajoute progressivement.

**3. Ignorer les patterns** — si ton site tombe tous les jeudis à 14h, c'est ton script de backup qui bouffe toute la RAM. Analyse les logs.

> ⚠️ **Erreur fréquente :** configurer des alertes sans plan d'action. Être alerté c'est bien, savoir quoi faire après c'est mieux.

## Optimisation avancée

### Status Pages — transparence avec tes clients

UptimeRobot génère des pages de statut publiques (comme status.github.com).

1. Dashboard → Status Pages → Create Status Page
2. Sélectionne les monitors à afficher publiquement
3. Personnalise le design (logo, couleurs)
4. Partage l'URL : `https://status.brandonvisca.com`

Résultat : transparence totale avec tes users, moins de tickets support, et un signal de sérieux vis-à-vis des clients.

### Intégration avec ta stack Grafana/Prometheus

Si tu as déjà du Grafana/Prometheus pour les métriques internes, combine avec UptimeRobot via webhook → API → Prometheus. Tu obtiens un dashboard unifié avec la dispo externe ET les métriques serveur internes.

### Détection d'anomalies (plan payant)

UptimeRobot apprend le comportement normal de ton site (temps de réponse moyen) et t'alerte si un écart anormal est détecté, même si le site est techniquement « up » :

```text
Temps de réponse habituel : 200-300ms
Aujourd'hui               : 2500ms
→ Alerte déclenchée
```

Tu peux anticiper les problèmes avant qu'ils deviennent critiques.

## Conclusion

Un serveur sans monitoring, c'est conduire sans rétroviseurs. Tu sauras que t'as eu un accident uniquement quand tu t'en remets.

UptimeRobot règle ça en 5 minutes. 50 moniteurs gratuits, alertes Discord/Slack configurées, page de statut publique si tu veux faire pro. Et quand tu auras épuisé le plan gratuit, le plan pro à 7$/mois reste ridicule face à Pingdom ou Datadog.

[Configure ton premier monitor maintenant](https://uptimerobot.com/?red=brando5751b9). Dans 5 minutes, ton infra est surveillée.

## Pour aller plus loin

- [Sécuriser ton serveur Linux — SSH, firewall, fail2ban](/securite-de-votre-serveur-linux/)
- [Documentation officielle UptimeRobot](https://uptimerobot.com/help) : référence complète
- [API UptimeRobot v2](https://uptimerobot.com/api) : endpoints et paramètres
