---
title: "Dashy Docker : ton dashboard homelab ultra-personnalisable avec widgets"
description: "Guide Dashy Docker : crée un dashboard homelab ultra-personnalisable avec widgets, monitoring de services et statuts en temps réel."
pubDatetime: "2026-07-10T08:00:00.000Z"
modDatetime: "2026-07-10T08:00:00.000Z"
author: Brandon Visca
tags:
  - intermediaire
  - auto-hebergement
  - docker
  - dashboard
  - homelab
featured: false
draft: false
focusKeyword: dashy docker
faqs:
  - question: "Quelle est la différence entre Dashy et Homer Dashboard ?"
    answer: "Dashy est un dashboard dynamique avec widgets intégrés (météo, bourse, monitoring système) et une interface de configuration visuelle. Homer reste 100% statique et léger, sans widgets ni backend. Si vous voulez du monitoring visuel sans outil externe, Dashy est plus adapté. Pour une page d'accueil minimaliste et rapide, préférez Homer."
  - question: "Dashy fonctionne-t-il sans connexion Internet ?"
    answer: "Oui, Dashy fonctionne entièrement en local. Seuls les widgets tiers (météo, bourse, news) nécessitent une connexion Internet pour récupérer leurs données. Le monitoring système via les widgets intégrés et les statuts des services utilisent vos propres API locales."
  - question: "Comment mettre à jour Dashy sans perdre sa configuration ?"
    answer: "Montez le répertoire /app/public/conf.yml dans un volume Docker persistant. Avant chaque mise à jour, faites une sauvegarde de ce fichier. Puis relancez le conteneur avec docker compose pull && docker compose up -d. La configuration est conservée car elle réside en dehors du conteneur."
  - question: "Dashy peut-il remplacer un outil de monitoring comme Netdata ou Uptime Kuma ?"
    answer: "Non. Dashy reste un tableau de bord de liens avec des widgets basiques. Il affiche l'état des services (up/down) mais ne conserve pas d'historique, ne génère pas d'alertes et ne propose pas de métriques détaillées. Pour du monitoring approfondi, gardez Netdata ou Uptime Kuma en parallèle et intégrez leurs URLs dans Dashy."
ogImage: "" 
---
> 💡 **TL;DR**
> - **C'est quoi ?** Un dashboard homelab dynamique avec widgets intégrés (météo, bourse, monitoring, statuts services) et une interface web de configuration
> - **Pourquoi ?** Parce qu'un simple tableau de liens ne suffit plus quand tu veux voir la température de ton NAS, le cours du Bitcoin et l'état de tes conteneurs en un coup d'œil
> - **Comment ?** Un conteneur Docker, un fichier `conf.yml` ou l'éditeur visuel intégré, et tu as une page d'accueil vivante pour tout ton homelab

## Un tableau de liens, c'est bien. Un tableau de liens vivant, c'est mieux.

Tu as déjà monté un [Homer Dashboard](/homer-dashboard-docker-homelab/) ou un équivalent statique. Tu as tes jolies icônes, tes groupes de services, tout est bien rangé. Mais à force, tu te retrouves à ouvrir cinq onglets supplémentaires rien que pour vérifier :

- La charge CPU de ton serveur
- Si ton NAS ne chauffe pas trop
- Le cours de tes cryptos ou de tes actions
- La météo de demain pour planifier ta session de jardinage numérique
- L'état de tes services Docker qui tombent parfois sans prévenir

**Dashy résout ce problème en ajoutant des widgets directement sur ta page d'accueil.** Pas dans une autre appli. Pas dans un onglet caché. Directement à côté de tes liens Plex, Nextcloud et Portainer. C'est le dashboard homelab qui passe au niveau supérieur.

## Table des matières

## Qu'est-ce que Dashy et pourquoi l'installer avec Docker ?

Dashy est un tableau de bord auto-hébergé créé par [Alicia Sykes](https://github.com/Lissy93), distribué sous licence MIT. Le projet est hébergé sur GitHub sous le nom `Lissy93/dashy` et compte aujourd'hui plus de 18 000 étoiles. Ce n'est pas rien.

Contrairement à un dashboard purement statique, Dashy embarque un backend Node.js léger, une interface Vue.js réactive et un système de widgets très complet. Tu peux tout configurer via un fichier YAML (`conf.yml`) ou directement depuis l'interface web, modification en temps réel incluse.

**Ce qui le distingue :**

- Widgets natifs : météo, bourse, crypto, monitoring système, horloge, mots du jour, news RSS, et bien d'autres
- Statuts des services en temps réel (ping HTTP, vérification de port, monitoring d'uptime)
- Éditeur visuel intégré : clique, glisse, modifies, ça s'enregistre tout seul
- Thèmes sombres/clairs personnalisables avec un système de couleurs CSS variables
- Support du mode plein écran, des favoris, de la recherche instantanée
- Export/Import de la configuration en JSON ou YAML
- Authentification intégrée (basique, Keycloak, ou header HTTP)
- Progressive Web App (PWA) : tu peux l'installer comme une app sur ton téléphone

## Dashy vs Homer : quand choisir l'un ou l'autre ?

Si tu hésites avec [Homer Dashboard](/homer-dashboard-docker-homelab/), voici la règle simple : Homer est une page d'accueil statique et légère. Dashy est un cockpit interactif. Si tu as 40 services et un Raspberry Pi 3, Homer est probablement plus sage. Si tu as un serveur avec un peu de marge et que tu veux des widgets visuels, Dashy est fait pour toi.

| Critère | Homer | Dashy |
|---------|-------|-------|
| Poids | Ultra-léger (~1 Mo) | Plus lourd (Node.js + Vue.js) |
| Widgets | Aucun | Météo, bourse, monitoring, etc. |
| Configuration | YAML manuel | YAML + éditeur visuel |
| Statuts services | Ping simple | Ping + vérification de port + uptime |
| Personnalisation CSS | Oui | Oui + thèmes préfaits |
| Authentification | Non native | Basique, Keycloak, headers |
| Idéal pour | Page d'accueil minimaliste | Dashboard central interactif |

## Prérequis

Avant de commencer, il te faut :

- Un serveur avec Docker et Docker Compose installés
- Un accès SSH ou terminal
- Au moins 512 Mo de RAM disponible pour le conteneur (Dashy est plus gourmand qu'un dashboard statique)
- Optionnel : un reverse proxy (Traefik, Nginx Proxy Manager) si tu veux l'exposer en HTTPS

## Dashy Docker : installation avec Docker Compose

La méthode la plus propre et la plus simple reste Docker Compose. Tu crées un dossier dédié, un fichier `compose.yml`, et c'est parti.

Crée un répertoire pour Dashy :

```bash
mkdir -p ~/docker/dashy && cd ~/docker/dashy
```

Crée le fichier `compose.yml` :

```yaml
services:
  dashy:
    image: lissy93/dashy:latest
    container_name: dashy
    restart: unless-stopped
    ports:
      - "8080:80"
    volumes:
      - ./conf.yml:/app/public/conf.yml
    environment:
      - NODE_ENV=production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 1m
      timeout: 10s
      retries: 3
```

Lance le conteneur :

```bash
docker compose up -d
```

Attends une dizaine de secondes que le build interne se termine (Dashy compile le frontend au premier démarrage), puis ouvre `http://IP_DU_SERVEUR:8080` dans ton navigateur.

**Pourquoi monter `conf.yml` en volume ?** Parce que toute la configuration de Dashy vit dans ce fichier. Si tu ne le montes pas en volume persistant, tu perds tout à chaque redémarrage du conteneur. C'est la règle d'or.

## Configuration de base avec conf.yml

Dashy se configure principalement via un fichier YAML. Voici un exemple minimal et fonctionnel pour démarrer :

```yaml
pageInfo:
  title: Mon Homelab
  description: Tableau de bord central de mes services
  navLinks:
    - title: GitHub
      path: https://github.com
    - title: Documentation
      path: https://dashy.to/docs

appConfig:
  theme: adventure
  layout: auto
  iconSize: medium
  language: fr
  auth:
    enableGuestAccess: true

sections:
  - name: Média
    icon: "fas fa-film"
    items:
      - title: Plex
        description: Serveur multimédia
        icon: "hl-plex"
        url: http://192.168.1.10:32400
        target: sametab
        statusCheck: true
        statusCheckInterval: 60

      - title: Jellyfin
        description: Alternative open source à Plex
        icon: "hl-jellyfin"
        url: http://192.168.1.10:8096
        target: sametab
        statusCheck: true

  - name: Administration
    icon: "fas fa-server"
    items:
      - title: Portainer
        description: Gestion des conteneurs Docker
        icon: "hl-portainer"
        url: http://192.168.1.10:9000
        target: sametab
        statusCheck: true

      - title: Nextcloud
        description: Cloud personnel
        icon: "hl-nextcloud"
        url: http://192.168.1.10:8080
        target: sametab
        statusCheck: true
```

**Les points essentiels à retenir :**

- `statusCheck: true` active le ping automatique sur chaque service. Dashy affiche une petite pastille verte si le service répond, rouge sinon
- `statusCheckInterval: 60` définit la fréquence de vérification en secondes. Par défaut c'est 30, tu peux l'augmenter si tu as beaucoup de services
- `target: sametab` ouvre le lien dans le même onglet. `newtab` pour un nouvel onglet
- Les icônes `hl-*` viennent de la bibliothèque Home-Lab-Icons intégrée à Dashy. Tu peux aussi utiliser Font Awesome (`fas fa-*`)

## Les widgets : le cœur de Dashy

C'est ici que Dashy distance tous les dashboards statiques. Tu peux insérer des widgets directement dans tes sections, à côté de tes liens.

### Widget météo

Affiche la météo actuelle et les prévisions pour une ville donnée :

```yaml
sections:
  - name: Informations
    icon: "fas fa-cloud-sun"
    widgets:
      - type: weather
        options:
          city: Paris
          units: metric
          apiKey: TA_CLE_OPENWEATHERMAP
```

Tu dois créer une clé API gratuite sur [OpenWeatherMap](https://openweathermap.org/api). Le widget affiche la température, l'humidité et une icône météo animée.

### Widget bourse et crypto

Pour suivre le cours de tes actions ou cryptos en direct :

```yaml
      - type: stock-price
        options:
          symbols:
            - BTC-USD
            - ETH-USD
            - AAPL
          chart: true
```

Les données proviennent de Yahoo Finance. Pas besoin de clé API.

### Widget monitoring système

Dashy propose un widget qui récupère les métriques du système hôte via une petite API. Pour cela, tu dois d'abord installer l'agent système de Dashy sur ton serveur ou utiliser un endpoint compatible.

```yaml
      - type: system-info
        options:
          hostname: true
          uptime: true
          cpu: true
          memory: true
          os: true
```

Si tu utilises déjà [Netdata](/netdata-docker/) pour monitorer ton infrastructure, tu peux aussi intégrer un widget iframe pointant vers ton dashboard Netdata. Ce n'est pas aussi élégant qu'un widget natif, mais ça fonctionne parfaitement.

### Widget horloge et date

Simple mais efficace, surtout quand tu gères des serveurs dans plusieurs fuseaux horaires :

```yaml
      - type: clock
        options:
          timeZone: Europe/Paris
          format: 24
          showDate: true
```

### Widget RSS / News

Pour afficher les derniers articles d'un flux RSS directement sur ton dashboard :

```yaml
      - type: rss-feed
        options:
          rssUrl: https://www.cert.ssi.gouv.fr/alerte/feed/
          limit: 5
```

Pratique pour suivre les alertes de sécurité ou les actualités tech sans quitter ton homelab.

### Widget recherche

Ajoute une barre de recherche qui peut interroger plusieurs moteurs ou ton propre système :

```yaml
      - type: search
        options:
          searchEngines:
            - name: Google
              url: https://www.google.com/search?q=
            - name: Reddit
              url: https://www.reddit.com/search/?q=
```

## Les statuts des services : ton NOC personnel

Le système de statuts de Dashy est plus évolué qu'un simple ping. Tu peux configurer :

- La méthode de vérification (GET, HEAD, ping ICMP)
- Le port à scanner
- L'intervalle entre deux checks
- Le timeout
- Une URL alternative pour le statut (par exemple une route `/health` spécifique)

Exemple avancé :

```yaml
      - title: Uptime Kuma
        url: http://192.168.1.10:3001
        statusCheck: true
        statusCheckUrl: http://192.168.1.10:3001/api/status-page
        statusCheckInterval: 120
        statusCheckAllowInsecure: false
```

Sur le dashboard, chaque service affiche une pastille colorée :

- Vert : tout va bien, le service répond
- Jaune : réponse lente ou partielle
- Rouge : le service ne répond pas
- Gris : la vérification est en cours ou non configurée

Si tu as [Uptime Kuma](/uptime-kuma-2-0-monitoring-auto-heberge/) déjà en place pour l'historique et les alertes, les statuts Dashy servent de complément visuel immédiat. Tu ouvres ton dashboard, tu vois en un coup d'œil ce qui est up et ce qui est down. Pas besoin de naviguer dans une autre interface.

## Thèmes et personnalisation visuelle

Dashy embarque une douzaine de thèmes prêts à l'emploi. Tu changes de thème dans l'éditeur visuel ou directement dans le YAML :

```yaml
appConfig:
  theme: adventure
```

Les thèmes disponibles incluent `callisto`, `night`, `minimal-light`, `adventure`, `nord`, `matrix`, `cyberpunk`, `lissy`, et bien d'autres. Chaque thème modifie les couleurs, les polices, les arrondis et les effets visuels.

Tu peux aussi créer ton propre thème en surchargeant les variables CSS. Dans `appConfig` :

```yaml
  customCss: |
    :root {
      --primary: #ff6b6b;
      --background: #1a1a2e;
      --card-background: #16213e;
    }
```

L'éditeur visuel te permet de prévisualiser les changements en temps réel. C'est addictif, ne m'en veux pas si tu passes ta soirée dessus.

## Sécurité et exposition sur Internet

Par défaut, Dashy n'a pas d'authentification. Si tu l'exposes sur Internet, configure au minimum l'un des trois modes d'auth disponibles.

### Authentification basique

Dans le YAML :

```yaml
appConfig:
  auth:
    enableGuestAccess: false
    users:
      - user: admin
        hash: MON_HASH_BCRYPT
        type: admin
```

Le hash doit être un bcrypt. Tu peux le générer avec la commande fournie dans la documentation officielle de Dashy.

### Derrière un reverse proxy

Si tu utilises Traefik ou Nginx Proxy Manager, configure Dashy pour écouter en local et laisse ton reverse proxy gérer le HTTPS. C'est le setup recommandé pour un homelab sécurisé.

Exemple avec Traefik (labels Docker) :

```yaml
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.dashy.rule=Host(`dashy.tondomaine.com`)"
      - "traefik.http.routers.dashy.tls=true"
      - "traefik.http.routers.dashy.tls.certresolver=letsencrypt"
      - "traefik.http.services.dashy.loadbalancer.server.port=80"
```

N'oublie pas de désactiver le port mapping direct (`ports: - "8080:80"`) si tu passes par Traefik, pour éviter l'exposition directe.

## Mise à jour et sauvegarde

Dashy évolue régulièrement. Pour mettre à jour sans perdre ta configuration :

```bash
cd ~/docker/dashy

# Sauvegarde
cp conf.yml conf.yml.$(date +%Y%m%d).bak

# Mise à jour
docker compose pull
docker compose up -d
```

Le conteneur recompilera le frontend au premier démarrage. Cela peut prendre 30 à 60 secondes. Sois patient.

Pour sauvegarder ta config à long terme, versionne ton `conf.yml` dans Git ou dans ton système de backup habituel. C'est un fichier texte de quelques kilo-octets, il ne coûte rien à conserver.

## Débogage et pièges courants

**Le dashboard reste blanc au démarrage**
Dashy compile le frontend au premier lancement. Attends 30 à 60 secondes. Vérifie les logs avec `docker logs dashy`.

**Les widgets météo ne fonctionnent pas**
Vérifie ta clé API OpenWeatherMap. Le plan gratuit est limité à 1000 appels par jour, ce qui largement suffit pour un usage personnel.

**Les statuts des services affichent tous le rouge**
Assure-toi que les conteneurs Dashy peuvent joindre les IPs et ports de tes services. Si tes services tournent dans des réseaux Docker isolés, Dashy doit soit être sur le même réseau, soit utiliser les IPs publiques de l'hôte.

**La personnalisation CSS ne s'applique pas**
Le champ `customCss` doit être une chaîne multiligne YAML avec le pipe (`|`). Une simple ligne ne fonctionnera pas.

## Conclusion

Dashy transforme ton homelab d'une simple collection de liens en un cockpit de pilotage véritablement utile. Entre les widgets de monitoring, les statuts en temps réel et la personnalisation poussée, c'est l'outil qu'il te faut si tu dépasses le stade du dashboard statique.

Il demande un peu plus de ressources qu'une page HTML brute, mais il en rend le double en fonctionnalités. Monte-le en Docker, sauvegarde ton `conf.yml`, et tu auras un tableau de bord qui grandit avec ton infrastructure sans jamais te demander où en est ton serveur.
