---
title: "Fail2Ban Docker : bloquer les attaques brute-force automatiquement"
description: "Guide Fail2Ban Docker : protège ton serveur contre les attaques brute-force. Docker Compose, filtres personnalisés et bonnes pratiques."
pubDatetime: "2026-06-02T08:00:00.000Z"
modDatetime: "2026-06-02T08:00:00.000Z"
author: Brandon Visca
tags:
  - debutant
  - securite
  - docker
  - linux
  - auto-hebergement
featured: false
draft: false
---
**TL;DR** — On va installer Fail2Ban via Docker pour bloquer automatiquement les IP qui s'acharnent sur tes services. Container officiel `crazymax/fail2ban`, un `docker-compose.yml`, trois fichiers de config et tu dors tranquille. Pas besoin d'installer quoique ce soit sur l'hôte, sauf Docker.

## Pourquoi Fail2Ban en 2026 ?

Ouvrir un serveur sur internet, c'est comme laisser ta porte d'entrée sur un trottoir parisien. En cinq minutes, tu vois passer des dizaines de robots qui testent des mots de passe en SSH, sniffent tes endpoints web ou essaient d'exploiter des failles connues.

Fail2Ban, c'est le videur de la discothèque : il observe les logs, repère les comportements suspects et bannit les adresses IP indésirables. C'est un outil qui existe depuis 2004, qui est encore maintenu aujourd'hui et qui continue de faire le job sans se prendre la tête.

Le problème, c'est que l'installation native demande de toucher au système hôte et de gérer des dépendances Python. En Docker, on isole le service, on versionne la config et on déploie en deux commandes. C'est propre. C'est reproductible. Et ça marche aussi bien sur un serveur dédié que sur un Raspberry Pi dans un placard.

## Fail2Ban natif VS Docker : que choisir ?


| Critère | Fail2Ban natif | Fail2Ban Docker (`crazymax/fail2ban`) | Alternative (CrowdSec) |
|---------|----------------|--------------------------------------|------------------------|
| **Installation** | `apt install fail2ban` + config système | `docker compose up -d` | `apt install` ou Docker |
| **Isolation** | Process sur l'hôte | Container isolé, pas de Python sur l'hôte | Agent lourd, cloud optionnel |
| **Persistance** | Dossiers système (`/etc/fail2ban`) | Volumes Docker bindés | Base locale + API |
| **Intégration Docker** | Manuelle via loghost ou socket | Accès direct aux logs des containers | Bouncer natif dispo |
| **Complexité** | Modérée | Facile | Avancée |
| **Communauté** | Très grande | Grande, mainteneur actif | En croissance rapide |
| **Cas d'usage idéal** | Serveur monolithique classique | Stack Docker Compose, NAS, homelab | Infra multi-nœuds, SOC |

Mon choix pour cet article : **Docker**. Parce que si tu lis ce blog, tu as probablement déjà une dizaine de services qui tournent en containers et que tu ne veux pas pourrir ton hôte avec des packages sysadmin.

CrowdSec est excellent, mais il est surdimensionné quand on veut juste protéger un serveur perso sans dépendre d'un tiers. On garde la focale sur Fail2Ban aujourd'hui.

## Prérequis

- Un serveur Linux avec Docker et Docker Compose installés.
- Quelques logs à surveiller (SSH, Traefik, Nginx Proxy Manager, etc.).
- Un minimum de confort avec `docker compose`.

Si tu as mis en place un reverse proxy comme [Nginx Proxy Manager](/nginx-proxy-manager-docker-guide/), tu auras déjà des logs HTTP à analyser. C'est l'occasion de faire bosser Fail2Ban sur les accès suspicieux à ton tableau de bord.

## Architecture : comment ça marche ?

Fail2Ban lit des fichiers de logs, applique des expressions régulières (les "filtres") et déclenche des actions quand une IP dépasse un seuil configuré. L'action la plus courante : ajouter une règle `iptables` pour bloquer l'adresse pendant un certain temps.

En Docker, le container Fail2Ban a besoin de :
- **Accès aux logs** des autres services, via des volumes bindés.
- **Capacité réseau** suffisante pour manipuler les règles de pare-feu de l'hôte (`NET_RAW`, parfois `NET_ADMIN`).
- **Le socket Docker** si on veut bannir directement via des labels ou des events (optionnel).

## Le Docker Compose complet

Crée un dossier `fail2ban` et place dedans un fichier `docker-compose.yml` :

```yaml
services:
  fail2ban:
    image: crazymax/fail2ban:latest
    container_name: fail2ban
    network_mode: host
    cap_add:
      - NET_ADMIN
      - NET_RAW
    volumes:
      - "./data:/data"
      - "/var/log/auth.log:/var/log/auth.log:ro"
      - "/var/log/syslog:/var/log/syslog:ro"
      - "/path/to/traefik/logs:/var/log/traefik:ro"
    environment:
      - "TZ=Europe/Paris"
      - "F2B_LOG_LEVEL=INFO"
      - "F2B_DB_PURGE_AGE=30d"
      - "F2B_MAXRETRY=5"
      - "F2B_FINDTIME=10m"
      - "F2B_BANTIME=1h"
    restart: always
```

Quelques précisions :

- `network_mode: host` est nécessaire pour qu'il puisse injecter des règles `iptables` directement sur l'hôte. Sans ça, il bloque dans son propre namespace réseau, donc zéro effet.
- `NET_ADMIN` et `NET_RAW` donnent les droits pour manipuler le pare-feu.
- Les volumes bindés vers `/var/log/auth.log` et `/var/log/syslog` permettent de superviser SSH. Si tu utilises `journald` sans fichier physique, il faudra passer par une autre stratégie (voir FAQ).
- Le dernier volume pointe vers les logs de Traefik ou Nginx Proxy Manager. Adapte le chemin à ton installation. Si tu utilises [Nginx Proxy Manager](/nginx-proxy-manager-docker-guide/), les logs sont généralement dans `/var/log/` ou exportés via un volume spécifique.

## Structure des fichiers de configuration

Dans le dossier `./data` du host, Fail2Ban s'attend à cette arborescence à la première exécution :

```
data/
├── fail2ban/
│   ├── jail.local
│   ├── jail.d/
│   │   └── custom.conf
│   ├── filter.d/
│   │   └── traefik-auth.conf
│   └── action.d/
│       └── custom-actions.conf
```

Le conteneur va créer automatiquement certaines choses, mais on va forcer nos propres configs pour garder le contrôle.

### Le fichier principal : `jail.local`

```ini
[DEFAULT]
# Les adresses à ne jamais bannir
ignoreip = 127.0.0.1/8 ::1 10.0.0.0/8 172.16.0.0/12 192.168.0.0/16

# Seuils de déclenchement
bantime = 3600
findtime = 600
maxretry = 5
backend = auto

# Action par défaut : ban via iptables-multiport
banaction = iptables-multiport

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
backend = auto
maxretry = 3
bantime = 3600

[traefik-auth]
enabled = true
filter = traefik-auth
logpath = /var/log/traefik/access.log
maxretry = 5
bantime = 7200
```

Note l'utilisation de `ignoreip`. Si tu te connectes depuis un réseau local ou un VPN, ajoute tes plages pour éviter de te bannir toi-même. C'est la première cause de désespoir chez les débutants Fail2Ban.

### Un filtre personnalisé : `filter.d/traefik-auth.conf`

Si tu utilises Traefik avec une authentification basique, un filtre simple pour repérer les 401 :

```ini
[Definition]
failregex = ^<HOST> .* "(GET|POST|PUT|DELETE) .* HTTP/[0-9.]+" 401.*$
ignoreregex =
```

L'expression capte les réponses HTTP 401 (non autorisé) dans les logs d'accès. `<HOST>` est une macro interne de Fail2Ban qui reconnaît automatiquement les adresses IP.

Pour Nginx Proxy Manager avec authentification, le filtre est similaire. Adapte juste le `logpath` dans le jail et le motif regex selon le format de tes logs.

### Pour SSH

Le filtre `sshd` est déjà fourni par l'image Docker. Il gère les erreurs PAM, les clés invalides et les échecs de mot de passe. Pas besoin de le réinventer.

## Lancer le container

```bash
cd fail2ban
docker compose up -d
```

Vérifie que tout est vert :

```bash
docker compose logs -f fail2ban
```

Tu devrais voir une ligne du style :

```
Server ready
```

## Vérifier que ça marche

Pour lister les prisons actives (les "jails") :

```bash
docker exec -it fail2ban fail2ban-client status
```

Pour inspecter une prison spécifique :

```bash
docker exec -it fail2ban fail2ban-client status sshd
```

Tu obtiens le nombre d'IP actuellement bannies, les timeouts, les fichiers log surveillés. C'est le tableau de bord minimaliste mais efficace de Fail2Ban.

Pour bannir manuellement une IP (test rapide) :

```bash
docker exec -it fail2ban fail2ban-client set sshd banip 42.42.42.42
```

Et pour débannir (indispensable si tu as banni ta propre IP par erreur) :

```bash
docker exec -it fail2ban fail2ban-client set sshd unbanip 42.42.42.42
```

Vérifie que les règles `iptables` sont bien appliquées sur l'hôte :

```bash
sudo iptables -L -n | grep fail2ban
```

Tu dois voir des chaînes `f2b-sshd` ou équivalentes.

## Intégration avec d'autres services Docker

Si tu n'as pas de logs persistantes sur le disque pour tes containers (parce que tu les as configurés en mode `json-file` dans Docker), Fail2Ban ne peut pas les lire directement via un volume.

Deux solutions :

1. **Rediriger les logs vers des fichiers persistants** en montant des volumes sur `/var/log/traefik` ou `/var/log/nginx`.
2. **Utiliser le driver syslog Docker** pour envoyer les logs vers le syslog de l'hôte, que Fail2Ban surveille déjà.

Pour Traefik, ajoute ceci dans son `docker-compose.yml` :

```yaml
    volumes:
      - "/path/to/traefik-logs:/var/log/traefik"
    labels:
      - "traefik.http.middlewares.auth.basicauth.users=admin:$$apr1$$..."
```

Et configure Traefik pour écrire ses access logs dans `/var/log/traefik/access.log`.

## Monitoring et alerting

Bannir des IP, c'est bien. Savoir quand ça se produit, c'est mieux. Si tu as déjà installé un outil de surveillance comme [Netdata](/netdata-docker/) ou Beszel, tu peux surveiller les métriques réseau et les drops de paquets pour repérer une vague d'attaques.

Fail2Ban écrit aussi ses propres logs dans `/data/log/fail2ban.log`. Un grep simple sur "Ban" avec une notification webhook ou un script de parsing te donne un alerting minimaliste mais fonctionnel. Pour une stack plus robuste, route ces logs vers un Loki ou un Uptime Kuma.

## Bonnes pratiques et pièges à éviter

**Ne pas monter tout `/var/log` dans le container.** Monte uniquement ce dont Fail2Ban a besoin. Plus ciblé, plus sûr.

**Toujours configurer `ignoreip`.** Si tu utilises un VPN ou une IP fixe, ajoute-la. Se bannir soi-même en SSH est un classique du genre.

**Tester avant de déployer en production.** Fais un `fail2ban-regex` avec un extrait de tes logs et ton filtre pour confirmer qu'il matche bien.

Exemple :

```bash
docker exec -it fail2ban fail2ban-regex /var/log/traefik/access.log traefik-auth
```

**Ne pas mettre `bantime` à des valeurs démentielles.** Ban 24h c'est bien pour un bot qui scanne. Ban 30 jours, tu risques de bloquer des utilisateurs légitimes derrière des CGNAT ou des proxies sortants.

**Préférer `iptables` à `nftables` si tu ne maîtrises pas.** L'image `crazymax/fail2ban` joue bien avec `iptables`. Sur les distros récentes en `nftables` (Debian 12+, Ubuntu 24+), vérifie que la compatibilité legacy est activée ou adapte l'action pour `nftables-multiport`.

## Tableau de synthèse des jails recommandés

| Service | Filtre | Logpath | maxretry | bantime |
|---------|--------|---------|----------|---------|
| SSH | sshd | /var/log/auth.log | 3 | 1h |
| Traefik 401 | traefik-auth | /var/log/traefik/access.log | 5 | 2h |
| Nginx 401 | nginx-auth | /var/log/nginx/access.log | 5 | 2h |
| Nextcloud bruteforce | nextcloud | /var/log/nextcloud/nextcloud.log | 3 | 24h |
| WordPress login | wordpress | /var/log/wordpress/access.log | 5 | 1h |

Adapte les chemins à ta configuration. L'important est que chaque jail pointe vers un fichier de log lisible et cohérent.

## FAQ rapide

**Faut-il Fail2Ban si j'ai déjà des clés SSH et ufw ?**

Oui. Les clés SSH empêchent le bruteforce de mot de passe, mais pas les floods de connexions. Ufw est un pare-feu statique. Fail2Ban est réactif. C'est complémentaire. Et pour configurer UFW correctement avec Docker sans que tes règles de pare-feu soient contournées, j'ai un guide complet sur [UFW avec Docker](/ufw-docker-pare-feu-linux/). Si tu cherches à durcir l'ensemble de ton serveur, j'ai aussi publié un guide sur [la sécurité Linux](/securite-de-votre-serveur-linux/) qui couvre SSH, sysctl et pare-feu.

**Est-ce compatible avec Docker Swarm ou Kubernetes ?**

`crazymax/fail2ban` est prévu pour des hôtes uniques. En Swarm ou K8s, le réseau overlay rend `iptables` plus complexe. CrowdSec ou un WAF cloud deviennent alors plus pertinents.

**Et les logs journald sans fichier physique ?**

Le driver journald de Docker n'écrit pas de fichier texte. Deux options : basculer le driver vers `json-file` ou `syslog`, ou monter le socket journald dans le container avec un backend `systemd` compatible. C'est plus avancé.

**Que faire si l'IP est derrière un CDN ?**

Fail2Ban lit les logs du reverse proxy. Si tu vois l'IP du CDN au lieu du client, vérifie que ton Traefik ou Nginx configure bien `X-Forwarded-For` et que tes logs l'exploitent.

## Conclusion

Fail2Ban en Docker, c'est un gain de temps énorme pour sécuriser un serveur auto-hébergé sans encombrer l'OS hôte. Container `crazymax/fail2ban`, quelques fichiers de config, `docker compose up` et tu passes d'une cible facile à un serveur qui repousse les bots automatiquement.

Ce n'est pas une baguette magique. Ça ne remplace pas des mots de passe solides, des mises à jour régulières ou un monitoring actif. Mais c'est un filet de sécurité robuste, gratuit et éprouvé qui tourne depuis vingt ans. Dans ton homelab comme en production léger, il a sa place.

