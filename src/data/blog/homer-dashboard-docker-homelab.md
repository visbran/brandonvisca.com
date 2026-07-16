---
title: "Homer Dashboard Docker : le tableau de bord ultime pour ton homelab"
description: "Guide Homer Dashboard Docker : tableau de bord auto-hébergé et statique pour centraliser tous tes services. Docker Compose inclus."
pubDatetime: "2026-06-21T08:00:00.000Z"
modDatetime: "2026-06-21T08:00:00.000Z"
author: Brandon
tags:
  - docker
  - auto-hebergement
  - homelab
  - dashboard
  - debutant
  - intermediaire
featured: false
draft: false
focusKeyword: homer dashboard docker
faqs: []
ogImage: "" 
---
> 💡 **TL;DR**
> - **C'est quoi ?** Un tableau de bord statique et ultra-léger pour regrouper tous tes services homelab derrière une jolie page d'accueil
> - **Pourquoi ?** Plus besoin de retenir 15 URLs par coeur. Un clic, tu arrives sur Plex, AdGuard, Nextcloud ou n'importe quel service
> - **Comment ?** Un conteneur Docker, un fichier `config.yml` et c'est en ligne en 2 minutes

## Tu as 15 services et zéro moyen de les retrouver ?

Ca te dit quelque chose ? Tu viens d'installer ton premier serveur, tu déploies Docker à gauche à droite, et au bout de trois semaines tu te retrouves avec :
- Plex qui tourne sur le port 32400
- AdGuard Home sur le 3000
- Portainer sur le 9000
- Nextcloud qui squatte le 8080
- Et cinq autres trucs dont tu as oublié l'existence

Tu ouvres un navigateur, tu tapes `192.168.1.42:32400`, tu attends, tu te demandes si c'est bien celui-là, tu retournes dans Portainer pour vérifier… Bref, c'est le bazar.

**C'est exactement le problème que Homer Dashboard résout.** Pas avec une usine à gaz. Avec une page HTML statique, jolie, configurable en YAML, qui pèse moins d'un méga et qui charge en quelques millisecondes.

## Qu'est-ce que Homer Dashboard ?

Homer est un tableau de bord auto-hébergé créé par [Bastien Wirtz](https://github.com/bastienwirtz). Le projet est hébergé sur GitHub sous le nom `bastienwirtz/homer`, distribué sous licence Apache-2.0, et il compte aujourd'hui plus de 11 000 étoiles.

Contrairement à beaucoup de dashboards qui embarquent une base de données et un backend en PHP/Node, Homer reste **100% statique**. C'est une application en Vue.js compilée en fichiers HTML/CSS/JS. Tu lui donnes un `config.yml`, il génère une page web. Point final.

**Ce qui fait sa force :**
- Ultra-léger : aucune base de données, aucun runtime lourd
- Temps de chargement quasi instantané
- Configuration en YAML lisible et versionnable
- Thèmes et icônes personnalisables
- Ping automatique des services pour vérifier leur disponibilité
- Support des logos custom, des groupes de services, et même du CSS personnalisé

Et comme tout est statique, tu peux même le servir depuis n'importe quel serveur web. Pas besoin de Docker si tu ne veux pas. Mais avec Docker, c'est encore plus simple.

## Prérequis

Avant de commencer, il te faut :
- Un serveur avec Docker et Docker Compose installés
- Un accès SSH ou terminal sur ce serveur
- Optionnel : un nom de domaine si tu veux exposer Homer en HTTPS derrière un reverse proxy

Si tu n'as pas encore Docker d'installé, je t'ai préparé un guide complet sur [les services essentiels à auto-héberger avec Docker](/docker-debutant-services-auto-heberger/). Il t'explique tout depuis zéro.

## Installation via Docker Compose

Crée un dossier dédié et un fichier `docker-compose.yml` :

```bash
mkdir -p ~/docker/homer && cd ~/docker/homer
```

Voici le fichier Docker Compose complet et fonctionnel :

```yaml
version: "3.8"

services:
  homer:
    image: b4bz/homer:latest
    container_name: homer
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - TZ=Europe/Paris
    volumes:
      # Le fichier de configuration principal
      - ./assets/config.yml:/www/assets/config.yml
      # Icônes et logos personnalisés
      - ./assets/icons:/www/assets/icons
      # CSS personnalisé optionnel
      - ./assets/custom.css:/www/assets/custom.css
```

Puis lance le conteneur :

```bash
docker compose up -d
```

En 10 secondes, Homer est disponible sur `http://ton-ip:8080`.

**Quelques explications sur les choix :**
- `restart: unless-stopped` : le conteneur redémarre automatiquement après un reboot du serveur
- Le volume `./assets/config.yml` est le coeur du système. C'est là que tu déclares tous tes services
- Le dossier `./assets/icons` te permet d'ajouter tes propres logos (PNG, SVG, JPG)
- La variable `TZ` corrige les horloges si tu utilises des features temporelles (logs, statuts)

## Configuration du fichier config.yml

Voici un exemple de configuration fonctionnelle que tu peux adapter :

```yaml
title: "Mon Homelab"
subtitle: "Tableau de bord des services"
logo: "assets/icons/logo.png"
header: true
footer: "<p>Créé avec Homer</p>"

columns: "auto"
connectivityCheck: true

# Thème et couleurs
colors:
  light:
    highlight-primary: "#3367d6"
    highlight-secondary: "#4285f4"
    highlight-hover: "#5a95f5"
    background: "#f5f5f5"
    card-background: "#ffffff"
    text: "#363636"
    text-header: "#ffffff"
    text-title: "#303030"
    text-subtitle: "#424242"
  dark:
    highlight-primary: "#3367d6"
    highlight-secondary: "#4285f4"
    highlight-hover: "#5a95f5"
    background: "#131313"
    card-background: "#2b2b2b"
    text: "#eaeaea"
    text-header: "#ffffff"
    text-title: "#fafafa"
    text-subtitle: "#f5f5f5"

# Liens rapides en haut de page
links:
  - name: "GitHub"
    icon: "fab fa-github"
    url: "https://github.com/"
    target: "_blank"
  - name: "Reddit"
    icon: "fab fa-reddit"
    url: "https://reddit.com/r/selfhosted"
    target: "_blank"

# Groupes de services
services:
  - name: "Medias"
    icon: "fas fa-play-circle"
    items:
      - name: "Plex"
        logo: "assets/icons/plex.png"
        subtitle: "Serveur multimédia"
        tag: "app"
        keywords: "plex media server"
        url: "http://192.168.1.42:32400"
        target: "_blank"
      - name: "Navidrome"
        logo: "assets/icons/navidrome.svg"
        subtitle: "Streaming audio"
        tag: "app"
        url: "http://192.168.1.42:4533"
        target: "_blank"

  - name: "Outils"
    icon: "fas fa-tools"
    items:
      - name: "Portainer"
        logo: "assets/icons/portainer.png"
        subtitle: "Gestion Docker"
        tag: "admin"
        url: "http://192.168.1.42:9000"
        target: "_blank"
      - name: "AdGuard"
        logo: "assets/icons/adguard.png"
        subtitle: "Blocage DNS"
        tag: "admin"
        url: "http://192.168.1.42:3000"
        target: "_blank"

  - name: "Productivité"
    icon: "fas fa-check-circle"
    items:
      - name: "Nextcloud"
        logo: "assets/icons/nextcloud.png"
        subtitle: "Cloud perso"
        tag: "app"
        url: "http://192.168.1.42:8080"
        target: "_blank"
      - name: "Vaultwarden"
        logo: "assets/icons/vaultwarden.png"
        subtitle: "Gestionnaire de mots de passe"
        tag: "app"
        url: "http://192.168.1.42:80"
        target: "_blank"
```

**Les points essentiels à retenir :**
- `connectivityCheck: true` active la petite pastille verte/rouge à côté de chaque service. Homer ping chaque URL et affiche si le service répond
- `columns: "auto"` adapte le nombre de colonnes à la taille de l'écran
- Chaque service peut avoir un `tag` pour filtrer l'affichage
- Tu peux utiliser des icônes FontAwesome (`fas fa-xxx`, `fab fa-xxx`) ou tes propres images
- Les URLs peuvent pointer vers des IPs locales, des noms de domaine, ou même des services extérieurs

## Intégration avec un reverse proxy

Si tu veux accéder à Homer depuis l'extérieur avec un joli nom de domaine, il te faut un reverse proxy.

### Avec Caddy

Si tu utilises Caddy, j'ai déjà fait un guide complet sur [Caddy Docker : le reverse proxy HTTPS automatique](/caddy-docker-reverse-proxy-guide/). Voici la config minimale pour Homer :

```
homer.tondomaine.com {
    reverse_proxy homer:8080
}
```

Caddy gère tout seul le HTTPS Let's Encrypt. Tu n'as rien d'autre à faire.

### Avec Nginx Proxy Manager

Si tu préfères une interface graphique, ajoute un proxy host dans NPM :
- Domain Names : `homer.tondomaine.com`
- Forward Hostname/IP : `homer`
- Forward Port : `8080`
- Block Common Exploits : ON
- Request a new SSL Certificate : ON

### Sécuriser l'accès

Si Homer est exposé sur Internet, ajoute au minimum une authentification basique. Avec Caddy :

```text
homer.tondomaine.com {
    basicauth {
        admin $2a$14$...bcrypt_hash...
    }
    reverse_proxy homer:8080
}
```

Ou place-le derrière un VPN WireGuard/Tailscale. Ne laisse jamais un dashboard homelab accessible publiquement sans protection.

## Homer vs Heimdall vs Organizr vs Dashy

Tu hésites avec les alternatives ? Voici le comparatif honnête.

| Critère | Homer | Heimdall | Organizr | Dashy |
|---------|-------|----------|----------|-------|
| Poids | Ultra-léger (statique) | Léger (PHP/Laravel) | Moyen (PHP/Angular) | Lourd (Vue.js + Node backend) |
| Base de données | Non | SQLite | SQLite/MySQL | Non (fichiers JSON) |
| Configuration | YAML | Interface web | Interface web | YAML/JSON |
| Customisation visuelle | CSS custom complet | Limitée | Moyenne | Très poussée (widgets) |
| Ping/statuts | Oui (natif) | Oui (natif) | Oui (via API) | Oui (natif) |
| Widgets dynamiques | Non | Non | Oui (Sonarr, Radarr…) | Oui (très complets) |
| Licence | Apache-2.0 | Apache-2.0 | GPL-3.0 | MIT |
| Idéal pour | Minimalistes, YAML lovers | Débutants, interface web | Users *arr (Sonarr/Radarr) | Geeks, widgets addicts |

**Mon avis :**
- **Homer** si tu veux du léger, du rapide, et que tu n'as pas besoin de widgets complexes
- **Heimdall** si tu préfères configurer via une interface web et que tu veux des intégrations *arr
- **Organizr** si tu veux un hub centré autour de Sonarr/Radarr/Lidarr avec des vues unifiées
- **Dashy** si tu veux le top du widget (météo, bourse, monitoring système intégré)

Personnellement, Homer gagne sur mon serveur car il ne consomme quasiment rien et je versionne ma config avec Git. Un `git pull` sur mon serveur et mon dashboard est à jour. Pas de base de données à sauvegarder, pas de migrations, pas de bugs d'upgrade.

## Astuces avancées

### Ping avec intervalle personnalisé

Par défaut Homer ping les services toutes les 30 secondes. Tu peux régler cela dans le `config.yml` :

```yaml
connectivityCheck: true
connectivityCheckInterval: 60
```

### Logos personnalisés

Place tes images dans `./assets/icons/` et référence-les avec `logo: "assets/icons/monlogo.png"`. Pour les services populaires (Plex, Nextcloud, Portainer…), tu trouves des packs d'icônes sur le repo GitHub `walkxcode/dashboard-icons`.

### CSS custom

Crée un fichier `custom.css` et monte-le comme volume. Exemple :

```css
.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}
```

### Plusieurs instances

Tu peux faire tourner plusieurs instances Homer sur le même serveur avec un mapping de ports différent. Utile si tu veux un dashboard "famille" et un "admin" séparés.

### Backup de la config

Comme tout est dans un fichier YAML et quelques images, le backup est trivial :

```bash
rsync -av ~/docker/homer/assets/ /mon/backup/homer/
```

Ou mieux : un dépôt Git privé. Un commit quand tu ajoutes un service et c'est versionné.

## Checklist sécurité

Avant d'exposer quoi que ce soit sur Internet, vérifie ces points :

- [ ] HTTPS forcé via reverse proxy (Let's Encrypt ou autre)
- [ ] Authentification basique ou SSO si exposé publiquement
- [ ] Accès restreint par IP ou VPN si possible
- [ ] URLs internes masquées derrière le reverse proxy (pas de ports directs exposés)
- [ ] Container mis à jour régulièrement (`docker compose pull && docker compose up -d`)
- [ ] Backup du dossier `assets/` avant chaque modification majeure
- [ ] Pas de credentials dans le `config.yml` (URLs avec token ou clés API)

Homer étant statique, il n'y a pas de surface d'attaque serveur (pas de SQL injection, pas de RCE via un backend). Mais si tu exposes les URLs de tes services, un attaquant saura où taper. Garde tes services internes derrière un VPN quand c'est possible.

## Conclusion

Homer Dashboard est probablement le tableau de bord le plus sobre et efficace pour un homelab. Pas de base de données, pas de dependencies lourdes, juste un fichier YAML qui décrit tes services et une page web qui charge en un clin d'oeil.

Si tu débutes avec Docker et que tu cherches un moyen simple de centraliser tes services, c'est le candidat idéal. Tu peux le faire tourner sur un Raspberry Pi sans aucun souci, le configurer en 5 minutes, et l'oublier ensuite. Il tourne, il affiche, il ping. C'est tout ce qu'on lui demande.

Si tu veux pousser plus loin avec des widgets intégrés (météo, monitoring, statuts avancés), j'ai aussi testé [Dashy Docker](/dashy-docker-dashboard-homelab/), un dashboard dynamique et ultra-personnalisable.

Et pour surveiller les changements sur des pages web (prix, disponibilité, releases) tout en gardant ton homelab sous contrôle, jette un oeil à [Changedetection.io](/changedetection-docker-surveillance-web/), un autre outil Docker que j'ai couvert récemment.

Si tu as besoin d'un navigateur web accessible depuis n'importe quel appareil directement depuis ton homelab, j'ai publié un guide sur [Alcove Docker](/alcove-navigateur-auto-heberge/), un conteneur Chromium embarqué parfait pour accéder à tes ressources internes sans client lourd.

Homer reste le dashboard le plus sobre et efficace pour un homelab. Pas de base de données, pas de dependencies lourdes, juste un fichier YAML qui décrit tes services et une page web qui charge en un clin d'oeil.
