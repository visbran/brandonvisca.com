---
title: "GLPI Agent Docker : monitorer tes postes clients"
description: "Déploie GLPI Agent Docker pour inventorier automatiquement ton parc informatique. Guide complet avec docker-compose et dépannage."
pubDatetime: "2026-06-25T08:00:00.000Z"
modDatetime: "2026-06-25T08:00:00.000Z"
author: Brandon
tags:
  - docker
  - auto-hebergement
  - intermediaire
  - glpi
  - inventaire
featured: false
draft: false
focusKeyword: glpi agent docker
ogImage: "" 
---
> 💡 **TL;DR**
> - GLPI Agent scanne et remonte l'inventaire hardware/software de tes postes clients vers ton serveur GLPI
> - Le déployer en Docker simplifie l'installation, la mise à jour et la suppression sur n'importe quel OS
> - Un docker-compose.yml de 30 lignes suffit à faire tourner l'agent avec les bonnes variables d'environnement
> - Tu peux fusionner les données avec FusionInventory ou utiliser l'agent en mode standalone

## Qu'est-ce que GLPI Agent et pourquoi l'utiliser en Docker ?

GLPI Agent est le successeur de FusionInventory Agent. C'est un petit logiciel qui tourne sur tes postes clients et qui remonte régulièrement un inventaire complet vers ton serveur GLPI : processeur, RAM, disques, cartes réseau, logiciels installés, périphériques USB, imprimantes, etc.

Sans agent, GLPI reste un beau formulaire vide. Avec un agent, il devient un véritable centre de gestion de parc informatique où tu vois en temps réel ce qui est installé sur chaque machine, qui l'utilise, et quand elle a été vue pour la dernière fois.

**Pourquoi Docker ?** Parce que l'installation native de GLPI Agent est chiante. Sur Windows, c'est un MSI à déployer via GPO (si t'as un AD), sur Mac c'est un pkg, sur Linux c'est un paquet par distro. Avec Docker, tu balances le même conteneur partout. Même image, même config, zéro dépendance système. Si tu débutes avec Docker, jette un oeil à mon [guide des services Docker pour débutants](/docker-debutant-services-auto-heberger/) avant de continuer.

Et surtout, Docker te permet de faire tourner l'agent sur des postes où l'installation native est impossible ou contraignante : Mac M1/M2 sans paquet ARM, vieux Windows 10 sans droits admin, ou machines Linux exotiques.

## Prérequis

Avant de balancer ton docker-compose.yml, vérifie que tu as :

- **Docker et Docker Compose** installés sur la machine cliente. Si ce n'est pas le cas, le [guide Docker débutant](/docker-debutant-services-auto-heberger/) couvre l'installation sur Linux, Windows (WSL2) et macOS.
- **Un serveur GLPI accessible en HTTP/HTTPS** depuis le réseau de tes postes clients. L'agent communique avec GLPI via des appels REST. Pas besoin que GLPI soit sur le même réseau, juste qu'il soit joignable.
- **Les identifiants d'un utilisateur GLPI** avec les droits d'ecriture sur l'inventaire (souvent le compte `glpi` par defaut si tu n'as pas sécurisé ton instance).

Si tu n'as pas encore de serveur GLPI, tu peux l'installer via Docker aussi, mais ce n'est pas le sujet de cet article. L'agent et le serveur sont deux choses distinctes. Pour aller plus loin, j'ai publié un tutoriel étape par étape pour [déployer GLPI avec Docker](/glpi-docker-itsm-auto-heberge/).

## Docker Compose complet

Crée un dossier `glpi-agent` et un fichier `docker-compose.yml` dedans :

```yaml
version: "3.8"

services:
  glpi-agent:
    image: glpi/agent:latest
    container_name: glpi-agent
    restart: unless-stopped
    # L'agent a besoin de privilèges pour scanner le hardware
    privileged: true
    # Monter le système de fichiers hôte pour l'inventaire
    volumes:
      - /:/host:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    environment:
      # URL de ton serveur GLPI (obligatoire)
      - GLPI_SERVER=https://glpi.tondomaine.local
      # Mode localinventory pour générer un fichier XML/JSON
      # ou server pour envoyer directement à GLPI
      - GLPI_MODE=server
      # Intervalle entre deux inventaires (en heures)
      - GLPI_INTERVAL=24
      # Tag pour regrouper tes machines dans GLPI
      - GLPI_TAG=docker-homelab
      # Forcer le scan même si le serveur est injoignable temporairement
      - GLPI_FORCE=1
```

Quelques explications sur les paramètres clés :

- `privileged: true` : indispensable. L'agent doit accéder à `/proc`, `/sys` et `dmidecode` pour lire la RAM, le CPU, le serial number de la carte mère. Sans ça, tu récupères un inventaire à minima.
- `volumes: - /:/host:ro` : le conteneur monte le filesystem racine de l'hôte en lecture seule. C'est comme ça qu'il lit les paquets installés, les fichiers de config réseau, etc.
- `GLPI_SERVER` : l'URL complète de ton serveur GLPI. Si tu utilises un reverse proxy comme Caddy ou Traefik, mets l'URL publique. Si c'est en interne, mets l'IP ou le nom DNS local.
- `GLPI_MODE=server` : envoie directement les données à GLPI. Si tu préfères générer un fichier local pour l'importer manuellement, mets `localinventory`.
- `GLPI_INTERVAL=24` : par défaut, l'agent scanne toutes les heures. Pour un parc stable, 24 heures suffisent largement et ça évite de spammer ton serveur.

Si tu cherches une stack monitoring complète pour superviser tes machines en plus de les inventorier, mon article sur [Beszel Docker](/beszel-monitoring-docker/) montre comment ajouter des métriques temps réel.

## Configuration avancée GLPI Agent Docker : variables d'environnement, tags et FusionInventory

L'image Docker `glpi/agent` expose pas mal de variables pour affiner le comportement. Voici celles que j'utilise en production :

| Variable | Description | Exemple |
|----------|-------------|---------|
| `GLPI_SERVER` | URL du serveur GLPI | `https://glpi.maboite.fr` |
| `GLPI_MODE` | `server` ou `localinventory` | `server` |
| `GLPI_INTERVAL` | Intervalle entre scans (heures) | `24` |
| `GLPI_TAG` | Tag libre pour filtrer dans GLPI | `prod`, `docker`, `homelab` |
| `GLPI_USER` | Utilisateur GLPI (si auth requise) | `glpi` |
| `GLPI_PASSWORD` | Mot de passe utilisateur | `SuperSecret123` |
| `GLPI_DEBUG` | Mode debug verbose | `1` |

Le `GLPI_TAG` est particulièrement utile si tu as plusieurs sites ou plusieurs types de machines. Dans GLPI, tu pourras filtrer les agents par tag et appliquer des règles d'import différenciées. Par exemple, taguer `docker-laptop` pour les portables et `docker-server` pour les machines fixes.

### FusionInventory vs GLPI Agent natif

Si ton serveur GLPI utilise encore le plugin FusionInventory, pas de panique. GLPI Agent est rétro-compatible avec le protocole FusionInventory. C'est d'ailleurs le protocole utilisé par défaut quand tu mets `GLPI_MODE=server`. L'agent envoie un XML au format FusionInventory, et GLPI (avec le plugin activé) l'ingère comme avant.

Si tu es passé à la version récente de GLPI (10.x) avec le système d'inventaire natif intégré, l'agent utilise le endpoint `/front/inventory.php` automatiquement. Pas de plugin nécessaire.

## Déploiement sur différents OS

Le gros avantage de Docker, c'est que tu écris la config une fois et tu la déploies partout. Voici les spécificités par OS.

### Linux (Debian/Ubuntu/Fedora/Arch)

C'est le cas le plus simple. Tu copies ton `docker-compose.yml`, tu fais un `docker compose up -d`, et c'est parti. Le conteneur monte `/` et `/var/run/docker.sock` sans restriction. Privilège root disponible natif.

Pour les distributions sans Docker Desktop (la majorité), assure-toi que l'utilisateur est dans le groupe `docker` ou exécute les commandes avec `sudo`.

### Windows 10/11 (WSL2 ou Docker Desktop)

Sur Windows, Docker Desktop utilise une VM Linux via WSL2. Quand tu montes `/` dans le conteneur, ce n'est pas le filesystem Windows qui est exposé, mais celui de la VM WSL2. Résultat : l'inventaire remonte les specs de la VM WSL2, pas celles de Windows.

**Solution** : pour inventorier un poste Windows proprement, il vaut mieux utiliser l'agent natif MSI. Docker sur Windows n'est pas adapté au scan hardware du système hôte. Cependant, si tu as un serveur Windows qui fait tourner Docker pour d'autres services, l'agent dans un conteneur peut quand même scanner les conteneurs eux-mêmes.

### macOS (Intel et Apple Silicon)

Sur Mac, Docker Desktop utilise aussi une VM Linux. Donc même problème que Windows : le conteneur scanne la VM, pas le Mac physique. Tu obtiens les specs de la VM, pas le serial number réel, pas les apps macOS installées.

**Verdict** : Docker est parfait pour déployer GLPI Agent sur des serveurs Linux. Pour les postes Windows et Mac, garde l'agent natif. L'interet de Docker sur ces OS se limite aux tests ou aux environnements où tu n'as pas les droits admin pour installer le paquet natif.

## Vérification : comment confirmer que l'agent remonte bien dans GLPI

Une fois le conteneur lancé, tu veux savoir si ça marche. Voici la checklist :

1. **Vérifie les logs du conteneur** :
   ```bash
   docker logs glpi-agent
   ```
   Tu dois voir des lignes du type `[info] sending inventory to https://glpi...` ou `[info] target server...`. Si tu vois `[error]`, lis le message. Souvent c'est une URL mal configurée ou un certificat SSL auto-signé refusé.

2. **Dans l'interface GLPI**, va dans **Parc > Ordinateurs**. Ton apparait normalement dans la liste sous le nom hostname du conteneur (qui est le hostname de l'hôte par defaut).

3. **Clique sur la machine** et vérifie l'onglet **Composants**. Tu dois y voir le CPU, la RAM, les disques, les cartes réseau. Si c'est vide, c'est que le scan n'a pas eu accès au hardware (vérifie `privileged: true`).

4. **Dans Parc > Agents**, tu vois la liste des agents connectés avec leur dernière date de contact. L'agent Docker apparait avec son tag et son IP.

Si ton serveur GLPI n'est pas encore en place et que tu hésites entre GLPI et SnipeIT pour la gestion de parc, j'ai fait un [comparatif GLPI vs SnipeIT](/snipeit-vs-glpi-comparatif-itsm-inventaire-it/) après trois ans d'utilisation sur les deux outils.

## Tableau comparatif : GLPI Agent natif vs Docker vs Fusion Inventory

| Critère | GLPI Agent natif | GLPI Agent Docker | Fusion Inventory Agent |
|---------|------------------|-------------------|------------------------|
| **Installation** | Paquet MSI/pkg/deb par OS | Un docker-compose.yml partout | Paquet natif, obsolète |
| **Mise à jour** | Mise à jour manuelle par machine | `docker pull` + recréation | Plus maintenu |
| **Scan hardware** | Complet (accès natif) | Complet sur Linux, limité sur VM | Complet |
| **Scan logiciels** | Natif (registre, .deb, .app) | OK sur Linux (montage /) | Natif |
| **Windows/Mac** | Parfait | Inadapté (scanne la VM) | Parfait |
| **Isolation** | Aucune | Totale (conteneur) | Aucune |
| **Complexité** | Moyenne (déploiement GPO/script) | Faible (Docker partout) | Moyenne |
| **Actuellement maintenu** | Oui (2026) | Oui | Non (remplacé par GLPI Agent) |

Le verdict est clair : **Docker est la meilleure option pour tous tes serveurs Linux**. Pour les postes Windows et Mac, reste sur l'agent natif. Fusion Inventory Agent est mort, ne l'installe plus sur des nouvelles machines.

## Dépannage courant

### L'agent ne remonte pas dans GLPI et les logs affichent une erreur SSL

Si ton serveur GLPI utilise un certificat Let's Encrypt ou auto-signé, l'agent Docker peut refuser la connexion. Deux solutions :

- Utilise une URL en HTTP pour tester (pas en prod)
- Monte le certificat CA dans le conteneur en ajoutant un volume vers `/etc/ssl/certs`

### L'inventaire hardware est vide ou incomplet

C'est le problème le plus fréquent. Vérifie que `privileged: true` est bien dans ton docker-compose.yml. Sans privilèges élevés, le conteneur ne peut pas lire `/proc/cpuinfo`, `/sys/class/dmi/id/product_serial`, ni exécuter `dmidecode`. Relance le conteneur avec la bonne config.

### Le hostname dans GLPI est celui du conteneur, pas celui de la machine

Par defaut, Docker attribue un hostname aléatoire ou reprend celui de l'hôte selon la configuration. Pour forcer un hostname explicite, ajoute dans ton service Docker :

```yaml
hostname: mon-serveur-prod
```

Ou utilise la variable `GLPI_HOSTNAME` si l'image la supporte (vérifie la doc de l'image).

### L'agent s'arrête après le premier scan

L'image `glpi/agent:latest` est conçue pour scanner une fois et s'arrêter par defaut si tu la lances sans mode daemon. Assure-toi d'utiliser `GLPI_MODE=server` avec un intervalle défini, ou de lancer le conteneur avec une commande qui boucle. Le docker-compose fourni plus haut est correct pour un fonctionnement continu.

## Conclusion

GLPI Agent en Docker, c'est la solution la plus propre pour inventorier tes serveurs Linux sans pourrir ton système avec des paquets natifs. Un fichier docker-compose, deux variables d'environnement, et ton parc remonte automatiquement dans GLPI toutes les 24 heures.

Pour les postes de travail Windows et macOS, garde l'agent natif. Docker n'apporte rien sur ces OS et complique le scan hardware. Mais pour tout ce qui est serveur, VM, Raspberry Pi et conteneurs, Docker est le roi.

Maintenant que tes machines remontent leur inventaire, tu peux les monitorer en temps réel avec des outils comme Beszel. J'ai détaillé le déploiement dans mon guide [Beszel Docker monitoring](/beszel-monitoring-docker/), parfait complément à GLPI pour la supervision.

Et toi, tu déploies déjà tes agents en Docker ou tu restes sur l'installation classique ? Raconte en commentaire.
