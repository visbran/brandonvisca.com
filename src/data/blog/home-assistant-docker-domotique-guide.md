---
title: "Home Assistant Docker : domotique auto-hébergée"
description: "Guide complet Home Assistant Docker : déploie ta domotique auto-hébergée avec Docker Compose, Zigbee, MQTT et automatisations. Zéro cloud, 100% contrôle."
pubDatetime: "2026-06-11T08:00:00.000Z"
author: Brandon Visca
tags:
  - docker
  - auto-hebergement
  - domotique
  - debutant
  - home-assistant
  - smart-home
featured: false
draft: false
focusKeyword: home assistant docker
faqs:
  - question: "Home Assistant Docker fonctionne-t-il sans Internet ?"
    answer: "Oui, une fois configuré, Home Assistant tourne entièrement en local. L'accès Internet n'est requis que pour les mises à jour et certaines intégrations cloud (météo, notifications push). Tes appareils Zigbee et WiFi locaux continuent de fonctionner sans connexion."
  - question: "Quelle différence entre Home Assistant Container et Home Assistant OS ?"
    answer: "Home Assistant OS est l'installation complète avec superviseur et add-ons (image dédiée pour Raspberry Pi ou VM). Home Assistant Container est l'image Docker officielle plus légère, sans superviseur. Tu dois gérer toi-même les dépendances comme MQTT ou Zigbee2MQTT dans des conteneurs séparés."
  - question: "Peut-on migrer sa config Home Assistant existante vers Docker ?"
    answer: "Oui, en copiant le dossier `.storage` et `configuration.yaml` depuis une installation existante. Restaure ces fichiers dans le volume Docker puis redémarre. Les automatisations, dashboards et appareils appairés sont conservés."
  - question: "Home Assistant consomme-t-il beaucoup de ressources ?"
    answer: "Non, environ 500 Mo à 1 Go de RAM selon le nombre d'intégrations actives. Un Raspberry Pi 4 avec 4 Go de RAM suffit pour un usage domestique standard. Pour la reconnaissance vocale ou de grosses bases de données, prévois 2 Go de RAM."
---
> 💡 **TL;DR**
> - Home Assistant est la plateforme de domotique open-source la plus mature et la plus flexible du marché
> - L'image Docker officielle (`homeassistant/home-assistant:stable`) te donne le contrôle total sans superviseur ni cloud
> - Stack complète : HA + PostgreSQL + Zigbee2MQTT + MQTT broker dans un seul Docker Compose
> - Zigbee, Z-Wave, WiFi, Bluetooth : tout communique en local, zéro dépendance aux serveurs de Xiaomi ou Philips
> - Automatisations en YAML ou via l'interface visuelle, notifications locales, et backup chiffré avec Duplicati

## Table des matières

## Pourquoi Home Assistant Docker pour ta domotique

Tu as des ampoules connectées Xiaomi, un thermostat Netatmo, des capteurs de porte Aqara et une prise connectée TP-Link. Chacun tourne dans son cloud, avec son appli, ses mises à jour forcées et ses conditions de service changeantes. Un jour, Xiaomi coupe l'accès API européen. Le lendemain, Netatmo exige un abonnement pour exporter tes données. Tu découvres que ton salon dépend de la bonne volonté de cinq entreprises américaines et chinoises.

**L'auto-hébergement de la domotique, c'est pas du militantisme geek.** C'est du bon sens :
- Tes scénarios d'éclairage et de chauffage fonctionnent même si ta connexion Internet tombe
- Personne ne collecte tes horaires de présence, tes habitudes de chauffage ou les mouvements détectés chez toi
- Tu n'es pas tributaire d'une fermeture de service, d'un changement de politique ou d'une mise à jour qui casse tout
- Tout communique en local : Zigbee, Z-Wave, MQTT, Thread. Pas de requêtes vers Shenzhen ou Seattle pour allumer une lampe
- Tu intègres ce que tu veux, quand tu veux, sans attendre qu'un écosystème propriétaire daigne supporter ton capteur à 8 € trouvé sur AliExpress

Home Assistant est le logiciel qui rend tout ça possible. Développé en Python par Nabu Casa depuis 2013, c'est devenu la référence de la domotique auto-hébergée. Le projet est open-source (Apache 2.0), soutenu par une communauté massive, et il gère plus de 2 700 intégrations natives.

## Home Assistant vs les alternatives : tableau comparatif

| Critère | Home Assistant | openHAB | Jeedom | Domoticz | Google Home / Alexa natif |
|---------|---------------|---------|--------|----------|---------------------------|
| **Open source** | Oui (Apache 2.0) | Oui (EPL) | Partiel (core GPL) | Oui (GPL) | Non |
| **Hébergement** | Local / Docker / OS dédié | Local / Docker | Local uniquement | Local / Docker | Cloud uniquement |
| **Intégrations** | 2 700+ | 300+ | 300+ | 200+ | Limité écosystème propriétaire |
| **Zigbee natif** | Oui (via ZHA ou Zigbee2MQTT) | Oui (binding) | Oui (plugin) | Oui (plugin) | Non (hub externe requis) |
| **MQTT natif** | Oui (intégration complète) | Oui | Oui | Oui | Non |
| **Interface web** | Moderne, responsive | Datée, technique | Moderne | Basique | Appli mobile |
| **App mobile** | Excellente (gratuite, notifications push) | Basique | Moyenne | Aucune | Excellente mais cloud obligatoire |
| **Automatisations** | Très avancées (YAML + UI) | Complexes (règles) | Scénarios visuels | Scripts limités | Basiques (IFTTT-like) |
| **Consommation RAM** | 500 Mo - 1 Go | 1 Go+ | 1 Go+ | 200 Mo | N/A (cloud) |
| **Communauté FR** | Très active (forums, Discord) | Active | Active | Réduite | N/A |

**Mon verdict :** Si tu débutes et veux un écosystème riche sans t'arracher les cheveux, Home Assistant est la solution évidente. openHAB est plus puissant pour les cas extrêmes (protocoles industriels) mais sa courbe d'apprentissage est raide. Jeedom et Domoticz ont du retard sur les intégrations modernes. Quant aux assistants vocaux cloud, ils sont pratiques mais tu paies avec tes données et ta dépendance.

## Prérequis avant de commencer

- Un serveur Linux (Debian, Ubuntu), un Raspberry Pi 4/5, ou un NAS compatible Docker
- Docker Engine et Docker Compose installés
- Un dongle USB Zigbee (ConBee II, Sonoff ZBDongle-P/E, ou SLZB-06) si tu veux du Zigbee local
- Un dossier dédié pour persister les données (`./homeassistant/config`)
- Optionnel : un nom de domaine et un reverse proxy pour l'accès HTTPS distant

Si tu n'as pas encore de reverse proxy, j'ai publié un guide sur [Caddy avec Docker](/caddy-docker-reverse-proxy-guide/) qui configure le HTTPS automatiquement en quelques lignes. C'est l'approche la plus simple pour sécuriser ton accès à distance.

## Le Docker Compose complet

Voici la stack que j'utilise en production depuis deux ans. Elle inclut Home Assistant, PostgreSQL (base de données robuste pour éviter la corruption SQLite), Zigbee2MQTT (pour gérer les appareils Zigbee), et Eclipse Mosquitto (broker MQTT).

```yaml
services:
  homeassistant:
    image: homeassistant/home-assistant:stable
    container_name: homeassistant
    restart: unless-stopped
    environment:
      - TZ=Europe/Paris
      - PYTHONUNBUFFERED=1
    volumes:
      - ./homeassistant/config:/config
      - /etc/localtime:/etc/localtime:ro
    networks:
      - ha_network
    depends_on:
      - db
      - mqtt
    ports:
      - "8123:8123"
    # Privilégié nécessaire pour certains intégrations matérielles (Bluetooth, USB)
    privileged: true

  db:
    image: postgres:16-alpine
    container_name: ha-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_USER=homeassistant
      - POSTGRES_PASSWORD=CHANGE_ME_STRONG_PASSWORD
      - POSTGRES_DB=ha_database
    volumes:
      - ./postgres:/var/lib/postgresql/data
    networks:
      - ha_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U homeassistant -d ha_database"]
      interval: 5s
      timeout: 5s
      retries: 5

  mqtt:
    image: eclipse-mosquitto:2
    container_name: ha-mqtt
    restart: unless-stopped
    volumes:
      - ./mosquitto/config:/mosquitto/config:ro
      - ./mosquitto/data:/mosquitto/data
      - ./mosquitto/log:/mosquitto/log
    networks:
      - ha_network
    ports:
      - "1883:1883"
      - "9001:9001"

  zigbee2mqtt:
    image: koenkk/zigbee2mqtt:latest
    container_name: zigbee2mqtt
    restart: unless-stopped
    environment:
      - TZ=Europe/Paris
    volumes:
      - ./zigbee2mqtt:/app/data
      - /run/udev:/run/udev:ro
    networks:
      - ha_network
    ports:
      - "8080:8080"
    devices:
      - /dev/ttyACM0:/dev/ttyACM0

networks:
  ha_network:
    driver: bridge
```

**Points importants :**
- `privileged: true` sur Home Assistant est nécessaire si tu utilises des intégrations Bluetooth ou des périphériques USB complexes. Sur un serveur headless sans Bluetooth, tu peux l'enlever.
- Le port `8123` est l'interface web de Home Assistant
- Le port `1883` est le broker MQTT standard
- Le port `8080` est l'interface web de Zigbee2MQTT pour appairer et gérer tes appareils Zigbee
- `/dev/ttyACM0` correspond à un dongle Zigbee USB. Vérifie le chemin avec `ls /dev/ttyACM*` sur ton hôte

## Configuration de Mosquitto (MQTT)

Crée le fichier `mosquitto/config/mosquitto.conf` :

```ini
persistence true
persistence_location /mosquitto/data/
log_dest file /mosquitto/log/mosquitto.log

listener 1883
allow_anonymous true

listener 9001
protocol websockets
allow_anonymous true
```

> **Note sécurité :** `allow_anonymous true` est acceptable en local sur un réseau domestique. En production ou sur un VPS exposé, configure l'authentification avec un fichier de passwords Mosquitto.

## Configuration de Zigbee2MQTT

Crée le fichier `zigbee2mqtt/configuration.yaml` :

```yaml
homeassistant: true
permit_join: false
mqtt:
  server: mqtt://mqtt:1883
serial:
  port: /dev/ttyACM0
frontend:
  port: 8080
advanced:
  network_key: GENERATE
  pan_id: GENERATE
  log_level: info
```

**Explications :**
- `permit_join: false` : empêche les appareils inconnus de s'appairer seuls. Tu passes temporairement à `true` quand tu ajoutes un nouvel appareil
- `network_key: GENERATE` : Zigbee2MQTT génère automatiquement une clé de réseau sécurisée au premier démarrage
- Le broker MQTT est accessible via le hostname Docker `mqtt` grâce au réseau interne `ha_network`

Lance la stack :

```bash
cd /opt/homeassistant
docker compose up -d
```

Attends 30-60 secondes, puis accède à `http://<IP_SERVEUR>:8123` pour la configuration initiale de Home Assistant.

## Configuration initiale de Home Assistant

À la première connexion, Home Assistant te guide pour créer un compte administrateur. Quelques réglages essentiels :

1. **Crée ton compte admin** avec un mot de passe fort (stocké localement, pas dans un cloud)
2. **Localisation** : définis ta position précise pour la météo et le calcul du lever/coucher du soleil
3. **Intégration MQTT** : Va dans Paramètres > Appareils et services > Ajouter une intégration > MQTT. Le broker est automatiquement découvert s'il est sur le même réseau Docker
4. **Intégration Zigbee Home Automation (ZHA)** : Si tu préfères ZHA intégré à Zigbee2MQTT, ajoute ZHA et sélectionne ton dongle USB. Personnellement, je préfère Zigbee2MQTT pour sa flexibilité et son interface web dédiée

## Appairer tes premiers appareils Zigbee

Avec Zigbee2MQTT, l'appairage est simple :

1. Va sur l'interface Zigbee2MQTT (`http://<IP_SERVEUR>:8080`)
2. Va dans l'onglet **Outils** puis clique **Activer l'appairage (tous)**
3. Mets ton capteur/capteur en mode appairage (généralement : maintenir le bouton appuyé 5-10 secondes jusqu'à ce que la LED clignote)
4. L'appareil apparaît dans la liste avec son nom, son modèle et ses fonctionnalités supportées
5. Donne-lui un nom explicite : `capteur-porte-entree` plutôt que `0x00158d0007abcdef`

**Appareils Zigbee recommandés pour débuter (tous testés et compatibles) :**

| Appareil | Prix indicatif | Fonction | Protocole |
|----------|---------------|----------|-----------|
| Aqara Door & Window Sensor | ~8 € | Ouverture de porte/fenêtre | Zigbee |
| Aqara Temperature/Humidity | ~10 € | Température, humidité, pression | Zigbee |
| Sonoff SNZB-02P | ~7 € | Température et humidité | Zigbee |
| Philips Hue Bulb White | ~15 € | Ampoule LED dimmable | Zigbee |
| IKEA TRÅDFRI Remote | ~7 € | Télécommande 5 boutons | Zigbee |
| Sonoff ZBMINI-L2 | ~10 € | Micromodule interrupteur | Zigbee |

Tous ces appareils communiquent en local. Pas de compte Xiaomi, pas d'appli Philips Hue obligatoire, pas de cloud IKEA. Tu les appaires une fois dans Zigbee2MQTT et Home Assistant les voit automatiquement via MQTT.

## Créer des automatisations qui ont du sens

L'intérêt de la domotique, c'est pas d'allumer une lampe avec ton téléphone. C'est que la maison réagisse toute seule à des conditions réelles.

**Exemple 1 : allumer la lumière du couloir quand on rentre la nuit**

Dans Home Assistant, va dans Paramètres > Automatisations et créer une automatisation en mode visuel :
- Déclencheur : le capteur de porte d'entrée passe à "Ouvert"
- Condition : le soleil est couché (after sunset, before sunrise)
- Action : allumer la lumière du couloir à 80% pendant 5 minutes, puis éteindre

**Exemple 2 : notification si la porte du garage reste ouverte**

```yaml
alias: "Alerte porte garage ouverte"
trigger:
  - platform: state
    entity_id: binary_sensor.capteur_porte_garage
    to: "on"
    for: "00:10:00"
action:
  - service: notify.mobile_app_mon_telephone
    data:
      title: "Garage"
      message: "La porte du garage est ouverte depuis 10 minutes"
```

**Exemple 3 : baisser le chauffage quand personne n'est là**

Si tu as des capteurs de mouvement ou la présence détectée par le routeur (intégration Router), tu peux baisser automatiquement la température de consigne après 30 minutes d'absence. Le gain énergétique est immédiat.

## Exposer Home Assistant en HTTPS

Ne laisse jamais le port 8123 ouvert directement sur Internet. Utilise un reverse proxy avec authentification ou un VPN.

**Option 1 : Reverse proxy avec Caddy (recommandé)**

Si tu as suivi mon guide [Caddy Docker](/caddy-docker-reverse-proxy-guide/), ajoute ce bloc à ton Caddyfile :

```caddyfile
ha.tondomaine.fr {
    reverse_proxy homeassistant:8123 {
        header_up Host {host}
        header_up X-Forwarded-For {remote}
        header_up X-Forwarded-Proto {scheme}
    }
}
```

Dans `configuration.yaml` de Home Assistant, ajoute :

```yaml
http:
  use_x_forwarded_for: true
  trusted_proxies:
    - 172.0.0.0/8
```

**Option 2 : Accès local uniquement + VPN**

Si tu n'as pas besoin d'accès extérieur, garde Home Assistant sur ton LAN. Pour les accès distants, un VPN WireGuard sur ton routeur ou ton serveur est la solution la plus sécurisée.

## Sauvegarder ta configuration

Home Assistant stocke tout dans `/config` : appareils, automatisations, dashboards, historique. Perdre ce dossier, c'est repartir de zéro.

J'utilise Duplicati pour sauvegarder le dossier `homeassistant/config` vers un NAS et un cloud distant chiffré. Si tu cherches une solution de backup pour ton homelab complet, mon guide sur [Duplicati Docker](/duplicati-docker-sauvegarde/) détaille la configuration complète avec chiffrement AES-256.

Un script de backup minimal à intégrer dans un cron quotidien :

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M)
tar czf /backup/ha-config-${DATE}.tar.gz /opt/homeassistant/homeassistant/config
# Conserver les 7 derniers jours
find /backup -name "ha-config-*.tar.gz" -mtime +7 -delete
```

## MQTT et Zigbee2MQTT : comprendre l'architecture

Sous le capot, voici comment ça fonctionne :

1. **Le dongle Zigbee USB** reçoit les signaux radio des capteurs et ampoules
2. **Zigbee2MQTT** traduit ces signaux en messages MQTT (JSON) et les publie sur le broker
3. **Mosquitto** distribue ces messages aux abonnés
4. **Home Assistant** est abonné aux topics MQTT et met à jour les états des entités en temps réel
5. **Quand tu allumes une lumière depuis HA**, le chemin inverse se fait : HA publie un message MQTT → Mosquitto → Zigbee2MQTT → dongle USB → ampoule

Cette architecture découplée est ce qui rend le système si robuste. Si Home Assistant redémarre, tes appareils Zigbee continuent de communiquer avec Zigbee2MQTT. Si Zigbee2MQTT plante, Mosquitto garde les derniers états en mémoire.

## FAQ rapide

**Home Assistant fonctionne-t-il sans Internet ?**
Oui, entièrement. Les mises à jour et certaines intégrations cloud nécessitent Internet, mais le cœur de la domotique (Zigbee, WiFi local, MQTT, automatisations) tourne offline.

**Puis-je intégrer des appareils WiFi chinois (Tuya, Sonoff) ?**
Oui, via l'intégration Tuya (nécessite un compte cloud temporairement pour récupérer les tokens), ou mieux : flashe les appareils Sonoff avec Tasmota ou ESPHome pour du 100% local. Certains appareils Tuya récents supportent aussi le protocole LocalTuya qui évite le cloud.

**Zigbee ou Z-Wave, lequel choisir ?**
Zigbee est plus répandu, moins cher, et mieux supporté par Home Assistant. Z-Wave est plus fiable sur de longues distances et consomme moins d'énergie, mais les appareils coûtent 2 à 3 fois plus cher. Pour un début, Zigbee est le choix évident.

**Peut-on utiliser Home Assistant sans dongle USB ?**
Oui, si tu as uniquement des appareils WiFi (Tasmota, ESPHome, Shelly). Mais le Zigbee local est recommandé pour la fiabilité et la consommation énergétique des capteurs sur batterie.

## Conclusion

Home Assistant dans Docker, c'est la liberté retrouvée pour ta maison. Un Raspberry Pi 4, un dongle Zigbee à 15 €, et tu as un système de domotique complet qui ne dépend de personne. Pas d'abonnement, pas de cloud qui espionne tes habitudes, pas de service qui ferme du jour au lendemain.

La courbe d'apprentissage existe, mais elle est moins raide qu'on ne le dit. En une journée, tu installes la stack, tu appaires tes premiers capteurs, et tu as une automatisation qui allume la lumière quand tu rentres. En une semaine, tu ne comprends plus comment tu as pu vivre sans.

Si tu veux versionner ta configuration Home Assistant (et tu devrais), j'ai publié un guide sur [Gitea Docker](/gitea-serveur-git-docker-auto-hebergement/) pour héberger ton propre Git et tracker les changements de tes fichiers YAML. Et n'oublie pas de sauvegarder régulièrement : un backup testé vaut mieux que mille excuses.

Lance le Docker Compose ce weekend. Ton salon te remerciera.
