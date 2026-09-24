---
title: "Homepage Docker : dashboard homelab personnalisable avec widgets"
description: "Installe Homepage Docker sur ton homelab : dashboard personnalisable, widgets natifs, config YAML claire et intégrations Docker en direct."
pubDatetime: "2026-09-24T11:00:13+02:00"
modDatetime: "2026-09-23T08:00:00.000Z"
author: Brandon
tags:
  - docker
  - homelab
  - monitoring
  - guide
  - intermediaire
featured: false
draft: false
focusKeyword: homepage docker
faqs:
  - question: "Homepage Docker consomme combien de ressources sur mon serveur ?"
    answer: "Très peu. C'est une app Next.js statique, elle tourne confortablement sur un Raspberry Pi ou un petit LXC avec moins de 100 Mo de RAM en usage normal."
  - question: "Homepage peut-il afficher l'état de mes conteneurs Docker automatiquement ?"
    answer: "Oui, en montant le socket Docker en lecture seule, Homepage détecte tes conteneurs et peut générer des cartes de service via les labels, sans toucher au YAML."
  - question: "Comment sécuriser l'accès à mon dashboard Homepage si je l'expose sur internet ?"
    answer: "Mets-le derrière un reverse proxy avec authentification, ou encore mieux passe par un Cloudflare Tunnel pour ne jamais ouvrir de port entrant sur ta box."
---
> 💡 **TL;DR**
> - Homepage Docker est un dashboard homelab open source (GPL-3.0), configuré en YAML, avec plus de 100 intégrations de widgets natifs
> - Installation en un `docker-compose.yml` : un volume de config, le socket Docker en option, port 3000
> - Widgets services (Sonarr, Uptime Kuma, Proxmox...), widgets info (météo, ressources système) et découverte automatique via labels Docker

## Homepage Docker : le dashboard qui remplace ton onglet de favoris

Tu as combien d'onglets épinglés pour accéder à tes services homelab ? Jellyfin, Proxmox, ton NAS, ton Uptime Kuma, ton routeur. Chez moi c'était n'importe quoi avant. La vraie question c'est : pourquoi je clique encore à l'aveugle alors qu'un dashboard peut tout centraliser avec le statut en direct ?

**Homepage Docker** répond à ça. C'est un dashboard auto-hébergé, pensé pour les homelabs, qui se configure en fichiers YAML et qui tourne dans un simple conteneur Docker. Pas de base de données à gérer, pas d'interface web à cliquer pendant des heures pour ajouter une tuile. Tu écris ton YAML, tu sauvegardes, la page se recharge.

Le projet est maintenu par la communauté sous l'organisation [gethomepage](https://github.com/gethomepage/homepage) sur GitHub, sous licence GPL-3.0, avec plus de 32 000 étoiles et un développement actif. C'est du sérieux, pas un side-project abandonné après trois commits.

## Table des matières

## Pourquoi Homepage Docker plutôt que Dashy ou Homer

Le terrain des dashboards homelab est déjà bien occupé. J'ai déjà couvert [Dashy](/dashy-docker-dashboard-homelab/) et [Homer](/homer-dashboard-docker-homelab/) ici, et les trois outils ne jouent pas exactement dans la même cour.

Homer est minimaliste : un seul fichier YAML, zéro backend, zéro widget dynamique. Parfait si tu veux juste une page de liens jolie et rapide.

Dashy pousse le curseur vers la personnalisation visuelle à fond : thèmes, statuts de santé, interface d'édition en direct dans le navigateur. C'est plus lourd, mais tu peux tout modifier sans toucher un fichier.

Homepage se positionne entre les deux, avec un vrai avantage : les widgets d'intégration. Sonarr, Radarr, Proxmox, Portainer, Uptime Kuma, ta météo locale, l'usage CPU/RAM du serveur qui héberge le dashboard lui-même. Le tout affiché en direct sur les cartes de service, sans ouvrir chaque appli. Si Homer te suffit pour une simple page de liens et que Dashy te semble trop pour ce que tu veux faire, Homepage tape exactement au milieu : configuration texte, widgets riches, zéro base de données.

## Installation de Homepage Docker : le docker-compose minimal

Direct au but. Voici le fichier officiel, adapté pour un déploiement homelab classique :

```yaml
services:
  homepage:
    image: ghcr.io/gethomepage/homepage:latest
    container_name: homepage
    restart: unless-stopped
    ports:
      - 3000:3000
    volumes:
      - ./config:/app/config
      - /var/run/docker.sock:/var/run/docker.sock:ro
    environment:
      HOMEPAGE_ALLOWED_HOSTS: dashboard.tondomaine.lan
```

Trois choses à retenir sur ce fichier.

D'abord, `HOMEPAGE_ALLOWED_HOSTS` est obligatoire depuis les versions récentes. Sans elle, Homepage refuse les requêtes qui n'ont pas le bon en-tête `Host`, et tu te retrouves avec une erreur au lieu de ton dashboard. Mets-y ton nom de domaine ou ton IP locale, avec le port si tu n'es pas en 80/443.

Ensuite, le montage du socket Docker (`/var/run/docker.sock:ro`) est optionnel mais c'est lui qui débloque la découverte automatique des conteneurs. Si tu ne veux pas exposer le socket dans un conteneur, tu peux tout configurer à la main en YAML et t'en passer.

Enfin, le volume `./config` va contenir tous tes fichiers de configuration. Crée le dossier avant de lancer le conteneur, sinon Docker le crée en root et tu vas galérer avec les permissions plus tard.

Lance ensuite :

```bash
mkdir -p ./config
docker compose up -d
```

Au premier démarrage, Homepage Docker génère des fichiers YAML par défaut dans `./config`. C'est là que tout se passe.

## Configuration YAML : services, widgets, bookmarks

Le dossier `config/` contient plusieurs fichiers, chacun avec un rôle précis :

- `settings.yaml` : titre du dashboard, thème couleur, langue
- `services.yaml` : tes groupes et cartes de service
- `widgets.yaml` : les widgets d'information affichés en haut de page (météo, horloge, ressources)
- `bookmarks.yaml` : une section de liens simples sans widget
- `docker.yaml` : les hôtes Docker si tu veux piloter plusieurs machines

Voici un exemple de `services.yaml` avec un groupe et un widget intégré :

```yaml
- Infra:
    - Proxmox:
        icon: proxmox.png
        href: https://proxmox.lan:8006
        description: Hyperviseur principal
        widget:
          type: proxmox
          url: https://proxmox.lan:8006
          username: monitoring@pve
          password: motdepasse-api
```

Chaque service peut avoir une icône (Homepage embarque des centaines d'icônes via [dashboard-icons](https://github.com/homarr-labs/dashboard-icons)), une description, un lien, et un widget qui va interroger l'API du service pour afficher des données en direct : nombre de VMs actives, statut d'un téléchargement, dernier scan de sécurité.

💡 Si tu utilises déjà [Uptime Kuma pour ton monitoring](/uptime-kuma-2-0-monitoring-auto-heberge/), le widget Homepage correspondant affiche directement le statut de tes moniteurs sur la carte, sans ouvrir Uptime Kuma.

## Widgets natifs : ce que Homepage Docker sait afficher

La vraie force de Homepage Docker, c'est la bibliothèque de widgets intégrés. Plus de 100 services supportés nativement, avec authentification via API key ou identifiants selon le service. Quelques exemples qui parlent à un setup homelab typique :

- **Infrastructure** : Proxmox, Portainer, Synology, TrueNAS
- **Média** : Jellyfin, Plex, Sonarr, Radarr, qBittorrent
- **Réseau et sécurité** : [AdGuard Home](/adguard-home-docker-guide-2026/), [CrowdSec](/crowdsec-docker-securite-collaborative/), pfSense
- **Monitoring** : Uptime Kuma, Grafana, Prometheus
- **Système** : usage CPU, RAM, disque et température de la machine hôte, via un widget `resources` qui ne nécessite aucune clé API

Au-delà des widgets de service, il y a aussi des widgets d'information génériques : météo locale, recherche unifiée (avec plusieurs moteurs configurables), horloge multi-fuseaux si tu gères des serveurs ailleurs. Pratique si ton homelab a grandi au point d'avoir des ressources hébergées chez plusieurs providers.

## Sécuriser l'accès à ton dashboard

Un dashboard qui liste tous tes services internes est une cible de choix si tu l'exposes bêtement sur internet. Deux options sérieuses.

**Cloudflare Tunnel** : plutôt que d'ouvrir un port sur ta box, tu passes par [Cloudflare Tunnel Docker](/cloudflare-tunnel-docker-homelab/) pour exposer Homepage sans IP publique et sans port forwarding. Le trafic transite par l'infra de Cloudflare, ton port reste fermé côté maison.

**Reverse proxy avec authentification** : si tu préfères rester en local ou passer par ton propre reverse proxy, ajoute une couche d'authentification devant Homepage. Basic auth, Authelia, ou un simple VPN vers ton réseau interne, tout vaut mieux que rien.

⚠️ Ne mets jamais de clés API en clair et exposées si le fichier `services.yaml` traîne quelque part accessible. Utilise les variables d'environnement supportées par Homepage pour externaliser les secrets hors du YAML versionné.

## Cas concrets pour ton homelab

Voici à quoi ressemble mon usage quotidien avec ce genre de dashboard.

**Le matin, un coup d'œil, je sais tout.** Statut Uptime Kuma vert partout, usage disque du NAS sous 80%, dernier backup [BorgBackup Docker](/borgbackup-docker-sauvegarde/) qui s'est bien terminé cette nuit. Trois secondes, pas besoin d'ouvrir cinq onglets.

**Onboarding rapide pour un accès partagé.** Si quelqu'un d'autre à la maison a besoin d'accéder à [Rocket.Chat](/rocket-chat-docker-messagerie-auto-hebergee/) ou à Jellyfin, je lui donne l'URL du dashboard, pas dix liens différents à retenir.

**Debug express.** Un service qui répond plus ? Le widget affiche direct un statut rouge ou une erreur, avant même d'ouvrir l'appli concernée. Ça fait gagner des minutes sur chaque incident mineur.

## Limites et points de vigilance

Homepage Docker n'est pas magique. Quelques points à garder en tête avant de tout migrer dessus.

- **Config en YAML, pas d'interface graphique d'édition** : contrairement à Dashy, tu édites des fichiers texte. Confortable si t'es à l'aise avec un éditeur et Git, moins pratique si tu veux déléguer la gestion à quelqu'un de non technique.
- **Widgets qui dépendent d'API tierces** : si un service change son API (ça arrive), le widget correspondant peut casser jusqu'à une mise à jour de Homepage Docker. Rien de dramatique, mais surveille les releases si tu dépends de widgets critiques.
- **Le socket Docker monté en lecture seule reste un socket Docker** : même en `:ro`, l'exposer dans un conteneur élargit la surface d'attaque théorique. Pèse le pour et le contre si ton homelab est exposé.

## Conclusion

Homepage Docker coche les cases que je cherche dans un dashboard homelab : léger, configuré en texte versionnable, avec assez de widgets pour remplacer la moitié de mes onglets épinglés. L'installation tient en un `docker-compose.yml` et une poignée de lignes YAML pour le premier service.

Si tu pars de zéro, commence petit : un groupe, trois services, le widget `resources` pour voir ta machine respirer. Tu ajoutes le reste au fil de l'eau, service par service, sans jamais avoir à tout reconfigurer d'un coup.
