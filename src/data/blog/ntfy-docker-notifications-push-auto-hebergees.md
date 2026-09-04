---
title: "Ntfy Docker : notifications push auto-hébergées pour ton homelab"
description: "Guide Ntfy Docker : reçois des notifications push gratuites et auto-hébergées depuis tes services Docker, scripts et monitoring vers ton téléphone."
pubDatetime: 2026-09-04 11:00:00+01:00
modDatetime: 2026-09-04 11:00:00+01:00
author: Brandon Visca
tags:
  - intermediaire
  - docker
  - linux
  - auto-hebergement
  - notifications
  - homelab
featured: false
draft: false
focusKeyword: ntfy docker
faqs:
  - question: "Ntfy est-il vraiment gratuit ?"
    answer: "Oui, l'auto-hébergement est totalement gratuit et open-source. Tu peux aussi utiliser le serveur public ntfy.sh sans créer de compte si tu ne veux pas auto-héberger."
  - question: "Peut-on envoyer des notifications depuis un script Python ou Bash ?"
    answer: "Absolument. Un simple curl POST sur ton topic suffit. Pas besoin de librairie compliquée."
  - question: "Ntfy fonctionne-t-il avec un reverse proxy et HTTPS ?"
    answer: "Oui, et c'est recommandé. Nginx Proxy Manager ou Traefik gèrent très bien le TLS pour Ntfy."
  - question: "Les notifications restent-elles si mon téléphone est hors ligne ?"
    answer: "Oui, le serveur Ntfy conserve les messages jusqu'à ce que ton appareil se reconnecte, comme un broker MQTT."
---
> 💡 **TL;DR**

> Ntfy est un serveur de notifications push auto-hébergé. Tu publies un message via HTTP et il arrive instantanément sur ton téléphone. Parfait pour les alertes monitoring, les scripts de backup ou les notifications domotique.

---

T'en as marre des emails pour tes alertes monitoring ? Ou pire, des webhooks Slack/Discord où tu dois créer un compte et configurer une intégration à la main ?

**Ntfy** résout ça en deux lignes de YAML et un `curl`. C'est un serveur de notifications push open-source qui tourne dans Docker et qui envoie des messages instantanés sur Android, iOS, ou même ton navigateur. Zéro compte, zéro API tierce, zéro complexité inutile.

Dans ce guide, on installe Ntfy via Docker Compose, on le branche à un reverse proxy pour le HTTPS, et on connecte quelques services classiques (Uptime Kuma, Beszel, scripts Bash). Objectif : recevoir une notif push quand quelque chose cloche dans ton homelab.

## Qu'est-ce que Ntfy et pourquoi l'utiliser ?

Ntfy (prononcé "notify") est un service de publication/souscription HTTP. Tu publies sur un topic public ou privé, et tous les abonnés reçoivent la notification en temps réel.

**Ce qui le différencie :**

- **Pas d'app tierce** : pas besoin de Telegram, Pushover, Slack ou Discord
- **Auto-hébergement possible** : ton serveur, tes données, tes topics
- **Protocol simple** : HTTP POST/GET, rien d'exotique
- **Multi-plateforme** : app Android native, app iOS via PWA, notifications web
- **Priorités et actions** : tu peux envoyer une notif avec un bouton "Marquer comme lu" ou "Redémarrer le service"
- **Léger** : un seul conteneur Docker, moins de 50 Mo de RAM

**Cas d'usage typiques :**

- Alertes monitoring (Uptime Kuma, Beszel, Zabbix)
- Fin de backup avec succès ou échec
- Détection de mouvement caméra IP (Frigate, MotionEye)
- Scripts cron qui veulent te prévenir sans envoyer d'email
- Domotique (Home Assistant → Ntfy)

## Prérequis

- Un serveur avec Docker et Docker Compose installés
- Un reverse proxy (Nginx Proxy Manager ou Traefik) pour le HTTPS
- L'app Ntfy sur ton téléphone (Android) ou accès web (iOS/PWA)

## Installation Docker Compose

Crée ton fichier `docker-compose.yml` :

```yaml
services:
  ntfy:
    image: binwiederhier/ntfy:latest
    container_name: ntfy
    restart: unless-stopped
    command:
      - serve
    volumes:
      - ./ntfy-cache:/var/cache/ntfy
      - ./ntfy-data:/etc/ntfy
    ports:
      - "2586:80"
    environment:
      - TZ=Europe/Paris
```

**Points clés :**

- Le port interne est `80` (l'image écoute sur ce port par défaut)
- Deux volumes persistants : le cache des messages et la configuration
- La commande `serve` lance le serveur

Lance le conteneur :

```bash
docker compose up -d
```

Vérifie que ça tourne :

```bash
curl http://localhost:2586/v1/health
```

Tu dois avoir un `{"health":"green"}`.

## Configuration avancée : authentification et accès privé

Par défaut, Ntfy fonctionne en mode public. Tout le monde peut publier et s'abonner à n'importe quel topic. Pour un homelab, c'est mieux d'activer l'authentification.

Crée le fichier `./ntfy-data/server.yml` :

```yaml
base-url: "https://ntfy.tondomaine.com"
listen-http: ":80"
auth-file: "/etc/ntfy/user.db"
auth-default-access: "deny-all"
```

Puis crée un utilisateur :

```bash
docker exec -it ntfy ntfy user add --role=admin tonuser
```

Et définis un mot de passe quand il te le demande.

**Pourquoi `auth-default-access: deny-all` ?**

Cela bloque l'accès public par défaut. Seuls les utilisateurs authentifiés peuvent publier et s'abonner.

Redémarre le conteneur pour prendre en compte la config :

```bash
docker compose restart
```

## Reverse proxy et HTTPS

### Avec Nginx Proxy Manager

Dans l'interface web de NPM :

1. **Proxy Hosts** → **Add Proxy Host**
2. Domain Name : `ntfy.tondomaine.com`
3. Forward Hostname/IP : `ntfy`
4. Forward Port : `80`
5. Active **WebSockets Support** (obligatoire pour les notifications temps réel)
6. SSL → Request a new SSL certificate
7. Active **HTTP/2 Support**

### Avec Traefik

Ajoute ces labels à ton service ntfy dans Docker Compose :

```yaml
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.ntfy.rule=Host(`ntfy.tondomaine.com`)"
      - "traefik.http.routers.ntfy.entrypoints=websecure"
      - "traefik.http.routers.ntfy.tls.certresolver=cloudflare"
      - "traefik.http.services.ntfy.loadbalancer.server.port=80"
      - "traefik.http.services.ntfy.loadbalancer.passhostheader=true"
```

**WebSockets est critique.** Sans ça, les notifications arrivent avec retard ou pas du tout sur l'app mobile.

## Envoyer une notification : le curl basique

Depuis n'importe quel serveur ou script :

```bash
curl -d "Ton disque est plein à 95%" https://ntfy.tondomaine.com/alertes-disque
```

Et paf, la notif arrive sur ton téléphone en 2 secondes.

**Avec authentification :**

```bash
curl -u tonuser:tonmdp -d "Alerte critique" https://ntfy.tondomaine.com/monitoring
```

**Avec titre et priorité :**

```bash
curl \
  -H "Title: Uptime Kuma" \
  -H "Priority: urgent" \
  -H "Tags: warning" \
  -d "Le serveur Proxmox ne répond plus depuis 5 minutes" \
  https://ntfy.tondomaine.com/monitoring
```

## Intégration avec Uptime Kuma

Dans Uptime Kuma :

1. **Settings** → **Notifications** → **Setup Notification**
2. Type : **Ntfy**
3. Server URL : `https://ntfy.tondomaine.com`
4. Topic : `uptime-kuma`
5. (Optionnel) Username / Password si tu as activé l'auth
6. Teste la notification

Maintenant, chaque panne de service déclenche une notif push instantanée.

## Intégration avec Beszel

Dans la config Beszel, ajoute un webhook qui pointe vers ton topic Ntfy. Beszel n'a pas d'intégration native Ntfy, mais un webhook générique fait très bien le job.

URL du webhook :

```
https://ntfy.tondomaine.com/beszel-alerts
```

Et dans le payload JSON, configure le titre et le message pour qu'ils correspondent au format attendu par Ntfy.

## Intégration dans un script Bash ou Python

### Script Bash (ex: fin de backup BorgBackup)

```bash
#!/bin/bash
TOPIC="https://ntfy.tondomaine.com/backups"
BACKUP_DIR="/mnt/backups"

if borg create --stats "::$BACKUP_DIR::$(date +%Y%m%d)" /data; then
  curl -H "Title: Backup OK" -d "Sauvegarde terminée avec succès" "$TOPIC"
else
  curl -H "Title: Backup FAIL" -H "Priority: urgent" -d "La sauvegarde a échoué" "$TOPIC"
fi
```

### Script Python

```python
import requests

def notify(title, message, priority="default"):
    requests.post(
        "https://ntfy.tondomaine.com/python-scripts",
        headers={
            "Title": title,
            "Priority": priority,
        },
        data=message,
        auth=("tonuser", "tonmdp")  # si auth activée
    )

notify("Script terminé", "L'import CSV s'est bien passé", "low")
```

## Sécurité : quelques bonnes pratiques

- **N'utilise pas les topics publics** pour des données sensibles. Même si tu n'as pas d'auth, n'importe qui peut s'abonner à un topic public.
- **Active l'authentification** si ton instance est exposée sur Internet.
- **Utilise des topics uniques et complexes** si tu veux une sécurité par obscurité temporaire (ex: `monitors-prod-x7k9`).
- **HTTPS obligatoire** pour les notifications web et iOS.
- **Limite la rétention** des messages dans la config si tu stockes beaucoup de données.

## Dépannage courant

**Les notifications n'arrivent pas sur mobile**

- Vérifie que WebSockets est bien activé sur ton reverse proxy
- Teste avec `curl` directement depuis le serveur pour isoler le problème
- Sur Android, vérifie que l'app Ntfy a les autorisations de notification

**Les messages arrivent avec retard**

- C'est souvent lié à l'absence de WebSockets. Le fallback en HTTP polling est plus lent.
- Vérifie aussi que ton téléphone n'est pas en mode économie d'énergie agressif pour l'app Ntfy.

**Erreur 401 Unauthorized**

- L'authentification est activée mais tu n'envoies pas de credentials
- Vérifie que ton `server.yml` est bien monté et pris en compte (redémarrage du conteneur)

## Alternatives à Ntfy

| Outil | Auto-hébergé | Complexité | Avantage principal |
|-------|-------------|------------|-------------------|
| **Ntfy** | Oui | Très faible | Simplicité extrême, notifications push natives |
| Gotify | Oui | Faible | Messages persistant côté serveur, app Android |
| Pushover | Non | Faible | Riche, mais payant au-delà de 7500 notifs/mois |
| Telegram Bot | Non | Moyenne | Très flexible, mais dépend de Telegram |
| Discord Webhooks | Non | Faible | Bien pour les équipes, mais trop lourd pour une alerte simple |

**Verdict** : Ntfy gagne pour l'auto-hébergement simple. Gotify est une alternative solide si tu préfères une interface web plus riche.

## Conclusion

Ntfy est l'outil qu'il te manquait si tu veux des notifications push sans dépendre d'un service tiers. Deux minutes de setup, un `curl`, et tu reçois tes alertes partout.

Le combo Ntfy + Uptime Kuma + Beszel couvre 90% des besoins de monitoring d'un homelab. Le reste, ce sont des scripts maison qui appellent ton topic.

Et toi, tu utilises quoi pour tes alertes ? Des emails ? Un bot Telegram ? Tu as testé Ntfy ? Dis-moi en commentaire, non, attends, j'ai pas de commentaires. Envoie-moi un MP si tu veux qu'on en discute.
