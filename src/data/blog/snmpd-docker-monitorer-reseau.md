---
title: "SNMPd Docker : monitorer ton réseau simplement"
description: "Guide SNMPd Docker complet : déploie un agent SNMP simple dans Docker pour superviser ton réseau, tes switchs et serveurs en quelques minutes."
pubDatetime: "2026-06-30T08:00:00.000Z"
modDatetime: "2026-07-04T14:00:00.000Z"
author: Brandon Visca
tags:
  - intermediaire
  - reseau
  - monitoring
  - docker
  - sysadmin
featured: false
draft: false
focusKeyword: snmpd docker
---
> 💡 **TL;DR**
> - SNMPd transforme n'importe quelle machine en agent de monitoring réseau standardisé, exploitable par Zabbix, LibreNMS ou un simple script.
> - Dockerisé, il se déploie en 2 minutes, isole sa config du système hôte et fonctionne sur toutes les architectures.
> - Un docker-compose.yml de 15 lignes + un snmpd.conf minimal = monitoring réseau fonctionnel sans toucher au système.

Tu as un switch, un routeur ou un petit serveur dont tu veux récupérer les métriques réseau, températures ou uptime, mais tu ne veux pas installer trois tonnes de métrologie dessus ? **SNMP** reste le protocole le plus simple et universel pour ça. Il est supporté nativement par quasiment tous les équipements réseau, et quand c'est pas le cas, tu peux l'ajouter en quelques secondes avec **snmpd**.

Dans cet article, je te montre comment faire tourner un agent SNMP dans un conteneur Docker. Zéro pollution système, zéro dépendance sur l'hôte, et une config qui suit le conteneur partout où tu le balances. Si tu cherches une solution de monitoring complète pour agréger toutes ces données, j'ai aussi publié un [guide Zabbix sous Docker](/zabbix-docker-monitoring-infrastructure/) qui s'intègre parfaitement avec SNMP.

## Table des matières

## Qu'est-ce que SNMP et pourquoi l'utiliser en Docker ?

**SNMP** (Simple Network Management Protocol) est un protocole de supervision réseau vieux de bientôt 40 ans et toujours d'actualité. Son principe est simple :

- Un **agent SNMP** (snmpd) tourne sur la machine à surveiller et expose des données structurées (OID).
- Un **manager SNMP** (Zabbix, LibreNMS, Nagios, ou un simple `snmpwalk`) interroge cet agent pour récupérer CPU, RAM, interfaces réseau, disques, etc.

Les avantages de SNMP sont son universalité et sa légèreté : pas de client lourd, pas de base de données locale, juste un démon qui répond à des requêtes UDP sur le port 161.

**Pourquoi Docker ?** Parce que la configuration native de snmpd sur Linux est pénible. Fichiers de config éparpillés dans `/etc/snmp/`, droits compliqués sur les MIBs, et si tu te plantes, tu pollues le système. Avec Docker, tu as un `snmpd.conf` propre, versionné, et tu peux le copier sur n'importe quel hôte en deux secondes. Si tu débutes avec Docker, mon [guide des services Docker pour débutants](/docker-debutant-services-auto-heberger/) couvre les bases indispensables.

## Architecture et vocabulaire en 30 secondes

Avant de copier-coller du YAML, quelques termes à connaître :

- **OID** (Object Identifier) : une adresse numérique qui représente une métrique. Exemple : `1.3.6.1.2.1.1.3.0` = uptime système.
- **MIB** (Management Information Base) : la "traduction" humaine des OID. `sysUpTimeInstance` au lieu de `1.3.6.1.2.1.1.3.0`.
- **Community string** (SNMP v1/v2c) : un mot de passe en clair qui protège l'accès. Par défaut souvent `public`. À changer immédiatement.
- **SNMPv3** : version sécurisée avec utilisateur, mot de passe et chiffrement. Obligatoire en production.
- **TRAP** : message envoyé spontanément par l'agent vers le manager (alerte, panne, etc.).
- **GET / WALK** : requêtes du manager vers l'agent pour lire une valeur (GET) ou toutes les valeurs d'une branche (WALK).

L'agent snmpd n'a besoin de rien d'autre que d'un port UDP ouvert et d'un fichier de configuration. C'est son travail d'interroger le système hôte pour les métriques réseau et de les exposer.

## Prérequis

Tu as besoin de très peu de choses :

- Une machine avec Docker et Docker Compose installés
- Un accès au port UDP 161 (ou un autre si tu changes la config)
- Un client SNMP sur une autre machine pour tester (`snmp` ou `snmpwalk`, paquet `snmp` sous Debian/Ubuntu)

Contrairement à un agent monitoring classique, snmpd ne nécessite pas de base de données ni de dashboard. Il se contente de répondre aux questions.

## Docker Compose complet

Crée un dossier `snmpd` et un fichier `docker-compose.yml` :

```yaml
services:
  snmpd:
    image: polinux/snmpd:latest
    container_name: snmpd
    restart: unless-stopped
    # Mode réseau host indispensable pour accéder aux interfaces réelles
    network_mode: host
    cap_add:
      - NET_RAW
    volumes:
      - ./snmpd.conf:/etc/snmp/snmpd.conf:ro
      - /proc:/host/proc:ro
```

Quelques explications sur les choix techniques :

- `network_mode: host` : snmpd a besoin de voir les interfaces réseau réelles de l'hôte pour remonter le bon état des liens, leur débit et leurs statistiques. Le bridge Docker masque tout ça.
- `cap_add: NET_RAW` : permet au conteneur d'accéder aux raw sockets et de remonter les stats réseau correctement.
- `/proc:/host/proc:ro` : snmpd lit `/proc/net/dev`, `/proc/loadavg`, `/proc/meminfo`, etc. pour construire les OID système.

> ⚠️ **Note** : `network_mode: host` ne fonctionne que sous Linux. Sur macOS ou Windows, snmpd en Docker ne peut pas voir les interfaces hôte. Pour ces OS, installe snmpd nativement.

## Le fichier snmpd.conf minimaliste

Crée un `snmpd.conf` dans le même dossier. Voici une config **SNMPv2c** fonctionnelle pour un homelab (à durcir ensuite) :

```text
# Emplacement : ./snmpd.conf
# Agent écoute sur toutes les interfaces UDP 161
agentAddress udp:161

# Informations système
sysLocation    "Homelab"
sysContact     "admin@tondomaine.local"
sysServices    72

# Community string par défaut (à CHANGER !)
rocommunity tonsecret 127.0.0.1 -V systemonly
rocommunity tonsecret 192.168.1.0/24 -V systemonly

# Ne pas exposer tout le système, juste les bases
# Accès limité aux OID système standard
view   systemonly  included   .1.3.6.1.2.1.1
view   systemonly  included   .1.3.6.1.2.1.2
view   systemonly  included   .1.3.6.1.2.1.25

# Désactiver les services inutiles pour réduire la surface d'attaque
dontLogTCPWrappersConnects yes
```

Paramètres clés à adapter :

- `agentAddress` : si tu veux écouter sur une interface spécifique, mets `udp:192.168.1.10:161` au lieu de `udp:161`.
- `rocommunity` : remplace `tonsecret` par une chaîne de caractères solide. C'est le mot de passe en clair de SNMPv2c.
- `192.168.1.0/24` : limite l'accès à ton LAN. **Ne laisse jamais `public` sans restriction d'IP**, c'est la porte ouverte à tout le monde.

Lance le conteneur :

```bash
docker compose up -d
```

## Passer à SNMPv3 (recommandé en production)

SNMPv2c envoie la community string en clair sur le réseau. Pour un homelab isolé ce n'est pas critique, mais si tes métriques passent sur un VLAN partagé ou un lien WiFi, préfère **SNMPv3**.

Voici une config SNMPv3 à remplacer dans `snmpd.conf` :

```text
agentAddress udp:161

sysLocation    "Homelab Securise"
sysContact     "admin@tondomaine.local"

# Créer un utilisateur SNMPv3
# Syntaxe : createUser <user> SHA <authpass> AES <privpass>
createUser monuser SHA "monmotdepasse" AES "macleprivee"

# Droits en lecture seule pour cet utilisateur
rouser monuser authPriv .1.3.6.1.2.1
```

> ⚠️ **Important** : la directive `createUser` doit être faite dans un fichier lu au démarrage. Avec l'image Docker, elle est prise en compte au premier lancement. Si tu changes le mot de passe, supprime le conteneur (`docker compose down`) et relance (`docker compose up -d`) pour que la création d'utilisateur soit reprise.

Pour tester en SNMPv3 depuis un client :

```bash
snmpwalk -v3 -u monuser -l authPriv -a SHA -A "monmotdepasse" -x AES -X "macleprivee" 192.168.1.10 1.3.6.1.2.1.1
```

## Tester ton agent SNMP

Si tu as un client `snmp` sur ta machine locale ou une autre machine du réseau, voici les commandes de base.

**Récupérer l'uptime (SNMPv2c)** :

```bash
snmpget -v2c -c tonsecret 192.168.1.10 1.3.6.1.2.1.1.3.0
```

**Lister toutes les interfaces réseau (SNMPv2c)** :

```bash
snmpwalk -v2c -c tonsecret 192.168.1.10 1.3.6.1.2.1.2.2.1.2
```

**Récupérer le load average (SNMPv2c)** :

```bash
snmpwalk -v2c -c tonsecret 192.168.1.10 1.3.6.1.4.1.2021.10.1.3.1
```

**Depuis un conteneur client SNMP temporaire** (pratique si tu n'as pas de client installé) :

```bash
docker run --rm -it alpine sh -c "apk add --no-cache net-snmp-tools >/dev/null && snmpwalk -v2c -c tonsecret 192.168.1.10 1.3.6.1.2.1.1"
```

Si tu obtiens des réponses avec des OID et des valeurs, ton agent est opérationnel.

## Les métriques les plus utiles à surveiller

Voici les OID essentiels pour un monitoring réseau basique :

| Métrique | OID | Description |
|---|---|---|
| Uptime | `1.3.6.1.2.1.1.3.0` | Temps depuis le dernier reboot |
| Nom système | `1.3.6.1.2.1.1.5.0` | Hostname de la machine |
| Description | `1.3.6.1.2.1.1.1.0` | OS et version du kernel |
| Interfaces | `1.3.6.1.2.1.2.2.1.2.X` | Nom de l'interface X |
| Octets IN | `1.3.6.1.2.1.2.2.1.10.X` | Total octets reçus sur interface X |
| Octets OUT | `1.3.6.1.2.1.2.2.1.16.X` | Total octets émis sur interface X |
| État interface | `1.3.6.1.2.1.2.2.1.8.X` | 1=up, 2=down, 3=testing |
| Load average | `1.3.6.1.4.1.2021.10.1.3.1` | Charge CPU (1 min) via UCD-SNMP |
| RAM totale | `1.3.6.1.4.1.2021.4.5.0` | Mémoire physique totale |
| RAM disponible | `1.3.6.1.4.1.2021.4.6.0` | Mémoire physique disponible (memAvailReal) |

Remplace `X` par l'index de l'interface (généralement 1, 2, 3...). Tu peux lister les index avec :

```bash
snmpwalk -v2c -c tonsecret 192.168.1.10 1.3.6.1.2.1.2.2.1.1
```

Ces métriques suffisent à alimenter un dashboard simple ou à déclencher des alertes sur l'état de tes liens réseau.

## Intégration avec un manager SNMP

SNMPd sans manager, c'est comme un téléphone sans interlocuteur. Voici comment brancher ton agent à une solution existante.

### Avec Zabbix

Si tu utilises déjà Zabbix pour superviser ton infrastructure, l'intégration SNMP est native. Crée un hôte dans Zabbix, ajoute l'interface SNMP avec l'IP de ta machine Docker, utilise la community string (ou les credentials v3), et associe le template **"Network Generic Device by SNMP"** ou **"Linux by SNMP"**. Les items se peuplent automatiquement.

### Avec LibreNMS

LibreNMS détecte automatiquement les hôtes SNMP. Ajoute simplement l'IP de ta machine, le protocole SNMP et la community. LibreNMS va découvrir les interfaces, les graphs de débit, et les alertes de port down sans que tu touches à quoi que ce soit.

### Avec un script personnalisé

Un simple script Python avec `pysnmp` ou `easysnmp` suffit pour récupérer une valeur et l'envoyer vers InfluxDB, Prometheus Pushgateway ou une API maison. SNMP est un protocole simple et bien documenté : pas besoin de SDK complexe.

Si tu cherches une solution de monitoring plus moderne et ultra-légère, mon article sur [Beszel Docker](/beszel-monitoring-docker/) couvre une approche à base de mini-agent ultra-léger qui complète bien SNMP pour les métriques système.

## Sécuriser ton agent SNMP

SNMPv1/v2c a une réputation de protocole peu sûr à juste titre. Quelques règles d'hygiène :

1. **Change la community string** immédiatement. `public` et `private` sont les premières valeurs testées par les scanners.
2. **Restreins par IP** avec `rocommunity` suivi d'un CIDR. Jamais sans restriction.
3. **Préfère SNMPv3** dès que possible, surtout sur un réseau WiFi ou partagé.
4. **Ferme le port 161** sur ton pare-feu externe. SNMP est un protocole LAN, pas WAN.
5. **Désactive les modules inutiles** dans `snmpd.conf` pour réduire la surface d'attaque (d'où les `view` limités dans l'exemple).

Sur un VPS cloud exposé à Internet, tu ne dois **jamais** exposer SNMP sans restriction d'IP et sans SNMPv3. Point barre.

## Dépannage courant

| Symptôme | Cause probable | Solution |
|---|---|---|
| `Timeout: No Response` | Port 161 filtré ou conteneur down | Vérifie `docker ps`, teste avec `nc -vu IP 161` depuis le client |
| `Cannot find module` | MIBs manquantes côté client | Installe `snmp-mibs-downloader` sur le client |
| Community string refusée | Mauvaise IP source ou typo | Vérifie le CIDR dans `rocommunity` et la casse |
| Valeurs système vides | Pas accès à `/proc` | Vérifie le volume `/proc:/host/proc:ro` dans le compose |
| Interfaces absentes | Pas de `network_mode: host` | Passe en mode host ou `--net=host` |

Si tu es sur un NAS Synology ou un routeur OpenWrt, snmpd est souvent préinstallé mais limité. L'image Docker te donne un snmpd complet sans toucher au firmware.

## Conclusion

SNMPd en Docker, c'est la solution la plus rapide pour rendre une machine Linux monitorable sans l'alourdir. Un fichier Compose, un `snmpd.conf` de 10 lignes, et tu peux brancher n'importe quel outil de supervision dessus. Que tu sois sur Zabbix, LibreNMS ou un simple script Python, le protocole est universel.

La force de cette approche, c'est l'**isolation** : ta config SNMP vit dans un fichier versionné, transportable d'une machine à l'autre, sans laisser de traces sur le système hôte. Pour un homelab, c'est l'idéal.

Prochaine étape : brancher ton agent à un manager. Si tu cherches une solution complète, je te recommande de jeter un oeil à mon [tutoriel Zabbix sous Docker](/zabbix-docker-monitoring-infrastructure/) pour orchestrer la supervision de tous tes agents SNMP depuis une seule interface.
