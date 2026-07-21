---
title: "CrowdSec Docker : sécurité collaborative contre les attaques"
description: Installe CrowdSec en Docker pour protéger ton homelab grâce à une intelligence collective contre les attaques brute-force et les scans malveillants.
pubDatetime: "2026-07-21T08:00:00.000Z"
modDatetime: "2026-07-21T08:00:00.000Z"
author: Brandon Visca
tags:
  - intermediaire
  - securite
  - docker
  - homelab
  - fail2ban
featured: false
draft: false
focusKeyword: crowdsec docker
ogImage: ""
---
> 💡 **TL;DR**
> - CrowdSec analyse tes logs en temps réel, détecte les attaques et bloque les IPs grâce à une base de signatures collaborative
> - Un agent Docker + un bouncer pour ton reverse proxy = protection active en 10 minutes
> - C'est la version "2026" de Fail2Ban : même principe, mais avec une communauté qui partage les signatures d'attaques

## Pourquoi CrowdSec plutôt que Fail2Ban ?

Si tu as déjà suivi mon guide sur [Fail2Ban Docker](/fail2ban-docker-securite-serveur/), tu sais que bloquer les IPs à la main, c'est efficace mais limité. Fail2Ban observe **ton** serveur, repère les motifs suspects dans **tes** logs et bannit en conséquence. Le problème ? Chaque serveur apprend seul. Un bot qui scanne des milliers de machines répère les faiblesses avant que ton Fail2Ban ne déclenche.

**CrowdSec** change la donne avec une approche collaborative. Lorsque l'agent CrowdSec détecte une attaque sur ton serveur, il peut remonter les informations (de façon anonymisée) vers une base collective. Tu bénéficies alors des signatures partagées par des milliers d'autres sysadmins. Un IP qui brute-force du SSH sur un serveur en Allemagne sera bloquée chez toi avant même qu'elle n'essaie.

En bref :

- **Fail2Ban** = protection locale, siloée, règles statiques
- **CrowdSec** = protection collaborative, intelligence partagée, signatures à jour en continu

Ce n'est pas que CrowdSec est "mieux" dans l'absolu. Pour un petit serveur isolé, Fail2Ban fait parfaitement le job. Mais si tu veux une couche de sécurité proactive qui apprend de la communauté mondiale, CrowdSec est la suite logique.

## L'architecture CrowdSec en trois briques

CrowdSec n'est pas un outil monolithique. Il repose sur trois composants distincts qui communiquent entre eux :

### 1. L'Agent

L'agent est le cerveau de la détection. Il lit les fichiers de logs (SSH, nginx, Traefik, Apache, etc.), applique des **scénarios** (des règles YAML décrivant une attaque) et décide si un comportement est malveillant. Quand un seuil est franchi, il génère une **décision** ("bannir cette IP") et l'envoie à l'API locale.

### 2. La Local API (LAPI)

La Local API est le point central sur ton serveur. Elle stocke les décisions prises par l'agent, les remonte éventuellement à la communauté, et les expose aux bouncers. Tu peux aussi l'interroger avec `cscli` pour inspecter les alertes et les bannissements actifs.

### 3. Les Bouncers

Un bouncer, c'est le muscle. Il lit les décisions de la LAPI et applique concrètement le blocage : ajouter une règle `iptables`, rejeter une requête au niveau de Traefik, ou même pousser un bannissement vers Cloudflare. Il existe des bouncers pour Nginx, Traefik, pfSense, Cloudflare, et même des bouncers "firewall" génériques.

Cette séparation agent/bouncer est astucieuse : un agent peut tourner sur ton serveur principal, et un bouncer sur ton edge router ou ton reverse proxy, même physiquement séparé.

## Ce qu'il te faut pour commencer

- Un serveur Linux avec Docker et Docker Compose (si tu débutes, voir mon guide [Docker pour débutants](/docker-debutant-services-auto-heberger/))
- Des logs à surveiller : SSH (`/var/log/auth.log`), et/ou un reverse proxy (Traefik, Nginx)
- Un accès root ou un utilisateur dans le groupe docker
- Environ 512 Mo de RAM pour le stack CrowdSec (1 Go c'est confortable)

Si tu as déjà [Zabbix Docker](/zabbix-docker-monitoring-infrastructure/) d'installé, tu peux même superviser la santé du conteneur CrowdSec avec un template SNMP ou un agent Zabbix sur le host.

## Le Docker Compose complet

Crée un dossier `crowdsec` et place-y un fichier `docker-compose.yml` :

```yaml
services:
  crowdsec:
    image: crowdsecurity/crowdsec:latest
    container_name: crowdsec
    restart: unless-stopped
    environment:
      - "TZ=Europe/Paris"
      - "COLLECTIONS=crowdsecurity/linux crowdsecurity/traefik crowdsecurity/sshd"
    volumes:
      - "./data:/var/lib/crowdsec/data"
      - "./config:/etc/crowdsec"
      - "/var/log/auth.log:/var/log/auth.log:ro"
      - "/path/to/traefik/logs:/var/log/traefik:ro"
    networks:
      - crowdsec-net
    cap_add:
      - NET_ADMIN
      - NET_RAW
```

Quelques précisions importantes :

- `COLLECTIONS` définit les packs de scénarios installés au premier démarrage. `crowdsecurity/linux` couvre les bases (SSH, scans port). `crowdsecurity/traefik` ajoute les scénarios pour un reverse proxy Traefik. `crowdsecurity/sshd` cible spécifiquement les attaques SSH.
- Les volumes bindés vers `/var/log/auth.log` et `/var/log/traefik` donnent à l'agent l'accès aux logs à analyser. Adapte les chemins à ton installation.
- `NET_ADMIN` et `NET_RAW` sont nécessaires si tu comptes utiliser un bouncer firewall sur le même hôte. Si le bouncer tourne ailleurs, tu peux les retirer.
- Le dossier `./data` persiste la base locale des décisions. Le dossier `./config` contient les fichiers de configuration modifiés.

### Fichier de config persistant : acquis.yaml

CrowdSec doit savoir où trouver tes logs. Crée un fichier `./config/acquis.yaml` :

```yaml
filenames:
  - /var/log/auth.log
  - /var/log/traefik/access.log
labels:
  type: syslog
```

Ce fichier dit à l'agent : "Analyse ces fichiers, et considère qu'ils sont au format syslog ou log d'accès web". CrowdSec détecte automatiquement le type de service en parsant les lignes.

### Démarrer le conteneur

```bash
cd crowdsec
docker compose up -d
```

Attends quelques secondes, puis vérifie :

```bash
docker compose logs -f crowdsec
```

Tu devrais voir des lignes du genre :

```
INFO crowdsec is finished to populate database
INFO Starting processing data
```

Si tu vois des erreurs de parsing, vérifie que les chemins de logs sont corrects et que CrowdSec a bien accès en lecture.

## Installer le bouncer Traefik

Le bouncer le plus utile en homelab est celui de **Traefik**. Il lit les décisions de la LAPI et rejette directement les requêtes HTTP avant qu'elles n'atteignent tes services.

Ajoute dans le même `docker-compose.yml` :

```yaml
  bouncer-traefik:
    image: crowdsecurity/traefik-bouncer:latest
    container_name: crowdsec-bouncer-traefik
    restart: unless-stopped
    environment:
      - "CROWDSEC_BOUNCER_API_KEY=${CROWDSEC_API_KEY}"
      - "CROWDSEC_AGENT_HOST=crowdsec:8080"
    networks:
      - crowdsec-net
```

La variable `CROWDSEC_API_KEY` doit être générée depuis le conteneur CrowdSec. Connecte-toi et crée une clé pour le bouncer :

```bash
docker exec -it crowdsec cscli bouncers add traefik-bouncer
```

Copie la clé affichée dans un fichier `.env` à la racine du dossier `crowdsec` :

```
CROWDSEC_API_KEY=votre-cle-api-ici
```

Puis redémarre le bouncer :

```bash
docker compose restart bouncer-traefik
```

### Configurer Traefik pour utiliser le bouncer

Dans le middleware de ton conteneur Traefik, ajoute un plugin CrowdSec. Si tu utilises Traefik v3 avec le système de plugins, ajoute ceci dans ta configuration statique (`traefik.yml` ou via labels) :

```yaml
experimental:
  plugins:
    crowdsec-bouncer-traefik-plugin:
      moduleName: github.com/maxlerebourg/crowdsec-bouncer-traefik-plugin
      version: v1.3.2
```

Puis, sur chaque route que tu veux protéger, ajoute le middleware :

```yaml
    labels:
      - "traefik.http.middlewares.crowdsec.plugin.crowdsec-bouncer-traefik-plugin.enabled=true"
      - "traefik.http.middlewares.crowdsec.plugin.crowdsec-bouncer-traefik-plugin.crowdseclapikey=${CROWDSEC_API_KEY}"
      - "traefik.http.middlewares.crowdsec.plugin.crowdsec-bouncer-traefik-plugin.crowdseclapihost=http://crowdsec:8080"
      - "traefik.http.routers.monservice.middlewares=crowdsec@docker"
```

Dès qu'une IP malveillante est signalée par CrowdSec, Traefik rejette la requête avec un `403 Forbidden`. L'attaque ne touche même pas ton application.

Si tu n'utilises pas encore Traefik, j'ai un guide complet sur [Traefik v3](/traefik-reverse-proxy-docker/) qui couvre l'installation, les certificats Let's Encrypt et la découverte automatique des conteneurs.

## Le bouncer firewall (optionnel)

Si tu veux bloquer au niveau réseau (pas seulement HTTP), installe le bouncer `iptables` :

```yaml
  bouncer-firewall:
    image: crowdsecurity/cs-firewall-bouncer:latest
    container_name: crowdsec-bouncer-firewall
    restart: unless-stopped
    environment:
      - "CROWDSEC_BOUNCER_API_KEY=${CROWDSEC_API_KEY}"
      - "CROWDSEC_AGENT_HOST=crowdsec:8080"
    cap_add:
      - NET_ADMIN
      - NET_RAW
    network_mode: host
```

Avec `network_mode: host` et `NET_ADMIN`, ce conteneur injecte directement des règles `iptables` sur l'hôte. Les IPs bannies par CrowdSec sont bloquées avant même qu'elles n'atteignent Docker. C'est le niveau de protection maximum.

Attention : `network_mode: host` n'est pas compatible avec les réseaux Docker custom. Utilise soit le bouncer firewall en host, soit le bouncer Traefik en bridge, selon ton besoin.

## Scénarios de détection : que bloque CrowdSec ?

CrowdSec arrive avec des dizaines de scénarios préconfigurés. Voici ceux qui te protègent le plus rapidement :

### Brute-force SSH

Le scénario `crowdsecurity/sshd` détecte les tentatives de connexion échouées sur SSH. Après 5 échecs en 2 minutes, l'IP est bannie. Si tu as déjà [WireGuard Docker](/wireguard-docker-vpn-homelab/) d'installé et que tu n'exposes le SSH que via le VPN, ce scénario devient un filet de sécurité plutôt qu'une nécessité vitale. C'est d'ailleurs une bonne pratique : moins tu exposes de surface d'attaque, mieux tu te portes.

### Scans HTTP

Le scénario `crowdsecurity/http-bad-user-agent` repère les user-agents connus de bots malveillants (scripts de scan, vulnérabilité scanners, etc.). Le scénario `crowdsecurity/http-probing` détecte les parcours systématiques de répertoires (`/admin`, `/wp-login.php`, etc.).

### Attaques web applicatives

CrowdSec propose des collections spécifiques pour WordPress (`crowdsecurity/wordpress`), Nextcloud, Drupal, ou même des frameworks comme Symfony. Si tu auto-héberges une app web, cherche la collection dédiée avec `cscli collections list`.

## Inspection avec cscli

`cscli` est l'outil en ligne de commande qui te permet de dialoguer avec la LAPI. Voici les commandes essentielles :

Lister les décisions actives (les IPs actuellement bannies) :

```bash
docker exec -it crowdsec cscli decisions list
```

Afficher les alertes récentes :

```bash
docker exec -it crowdsec cscli alerts list
```

Bannir manuellement une IP (test rapide ou cas d'urgence) :

```bash
docker exec -it crowdsec cscli decisions add --ip 42.42.42.42 --duration 1h --reason "test manuel"
```

Débannir une IP :

```bash
docker exec -it crowdsec cscli decisions delete --ip 42.42.42.42
```

Voir les métriques et le nombre de signaux traités :

```bash
docker exec -it crowdsec cscli metrics
```

Vérifier la santé de la connexion avec la communauté :

```bash
docker exec -it crowdsec cscli hub update
docker exec -it crowdsec cscli hub list
```

La commande `hub list` affiche toutes les collections, parsers et scénarios installés. Tu peux en ajouter à tout moment sans redémarrer le conteneur.

## Dashboard web (console)

CrowdSec propose une interface web optionnelle pour visualiser les alertes, les IPs bannies et les tendances d'attaques. Elle s'installe comme un service Docker supplémentaire.

Ajoute dans ton `docker-compose.yml` :

```yaml
  crowdsec-dashboard:
    image: crowdsecurity/crowdsec-dashboard:latest
    container_name: crowdsec-dashboard
    restart: unless-stopped
    environment:
      - "CROWDSEC_API_URL=http://crowdsec:8080"
    ports:
      - "3000:3000"
    networks:
      - crowdsec-net
```

Accède ensuite à `http://IP_DU_SERVEUR:3000`. L'interface te montre :

- Une carte des attaques géolocalisées
- Les IPs les plus actives
- Les types d'attaques détectées par scénario
- L'évolution dans le temps

C'est pratique pour comprendre d'où viennent les menaces. Si tu as [Zabbix Docker](/zabbix-docker-monitoring-infrastructure/) qui supervise ton infrastructure, le dashboard CrowdSec complète parfaitement les alertes techniques de Zabbix avec une vision purement sécurité.

## Bonnes pratiques et limites

**Ne pas exposer la LAPI sur internet.** Le port 8080 de CrowdSec doit rester interne au réseau Docker. Si tu dois accéder à `cscli` depuis l'extérieur, passe par un tunnel SSH ou un [VPN WireGuard](/wireguard-docker-vpn-homelab/), jamais en exposant le port.

**Mettre à jour régulièrement les scénarios.** Les menaces évoluent. Lance `cscli hub update && cscli hub upgrade` une fois par semaine pour obtenir les dernières signatures.

**Ne pas bannir indéfiniment.** Un `bantime` de 4 heures est un bon équilibre. Les bots changent d'IP rapidement, et un bannissement trop long risque d'affecter des utilisateurs légitimes derrière des CGNAT.

**Vérifier la consommation CPU.** CrowdSec parse beaucoup de lignes de logs. Sur un Raspberry Pi avec des logs verbeux, ça peut devenir gourmand. Ajuste les `log_level` si nécessaire.

**Utiliser un bouncer approprié.** Un bouncer firewall bloque tout (TCP/UDP), un bouncer Traefik ne bloque que le HTTP. Choisis selon la surface d'attaque que tu veux protéger. Si tu n'as que des services web exposés, le bouncer Traefik suffit largement.

**Surveiller les faux positifs.** Si tu remarques qu'une IP légitime est bloquée, ajoute-la en whitelist via `cscli decisions delete` ou dans le fichier de configuration `whitelists.yaml`.

**CrowdSec n'est pas un WAF complet.** Il détecte les attaques connues et les comportements suspects, mais il ne remplace pas un vrai Web Application Firewall pour protéger contre les injections SQL complexes ou les zero-days sophistiqués. Pour une couche supplémentaire sur tes applications web, envisage un WAF comme ModSecurity ou Coraza derrière Traefik.

## CrowdSec VS Fail2Ban : tableau comparatif

| Critère | Fail2Ban | CrowdSec |
|---------|----------|----------|
| **Type de protection** | Locale, basée sur les logs de ta machine | Collaborative, intelligence partagée |
| **Installation** | Image Docker `crazymax/fail2ban` | Image officielle `crowdsecurity/crowdsec` |
| **Architecture** | Monolithique | Agent + LAPI + Bouncers (découplé) |
| **Mises à jour signatures** | Règles statiques (filtres regex) | Scénarios communautaires mis à jour via `cscli hub` |
| **Intégration Docker** | Lecture de logs bindés | Bouncers natifs pour Traefik, Nginx, firewall |
| **Complexité** | Facile | Intermédiaire |
| **Communauté** | Mature, stable | En forte croissance, très active |
| **Cas d'usage idéal** | Serveur unique, config simple | Homelab multi-services, infra évolutive |

Mon verdict personnel : Fail2Ban reste parfait pour un serveur monolithique avec SSH et un service web. CrowdSec brille quand tu commences à avoir une stack complète (reverse proxy, plusieurs services, monitoring) et que tu veux une protection qui grandit avec ton infra.

## Conclusion

CrowdSec en Docker, c'est la protection collaborative que ton homelab mérite. Tu installes l'agent, tu branches un bouncer sur ton reverse proxy, et d'un coup ton serveur ne se contente plus de réagir à ses propres logs : il tire parti de l'intelligence de milliers d'administrateurs qui partagent les signatures d'attaques en temps réel.

Ce n'est pas une baguette magique. Ça ne remplace pas des mots de passe solides, des mises à jour régulières ou un pare-feu bien configuré. Mais c'est un filet de sécurité actif, gratuit et en constante évolution qui transforme ton serveur isolé en membre d'une communauté de défense collective. Dans un monde où les attaques sont automatisées et massives, cette approche collaborative n'est pas un luxe. C'est un standard.
