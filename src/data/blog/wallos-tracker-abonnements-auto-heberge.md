---
title: "Wallos Docker : tracker d'abonnements auto-hébergé"
description: "Guide Wallos Docker complet : déploie ce tracker d'abonnements open-source et auto-hébergé, avec notifications et support multi-devises intégré."
pubDatetime: "2026-10-28T11:01:12+01:00"
modDatetime: "2026-10-27T08:00:00.000Z"
author: Brandon
tags:
  - docker
  - auto-hebergement
  - dashboard
  - sauvegarde
  - debutant
featured: false
draft: false
focusKeyword: wallos docker
faqs:
  - question: "Wallos est-il vraiment gratuit ?"
    answer: "Oui. Wallos est open-source sous licence GPL-3.0, publié sur GitHub (ellite/wallos). Tu l'installes sur ton propre serveur sans abonnement, sans palier payant et sans limite d'abonnements suivis."
  - question: "Wallos peut-il m'envoyer une alerte avant un prélèvement ?"
    answer: "Oui, par email, Discord, Telegram, Pushover, Gotify ou webhook générique. Tu règles le délai d'alerte abonnement par abonnement, par exemple trois jours avant le renouvellement."
  - question: "Wallos supporte-t-il l'authentification SSO via OIDC ?"
    answer: "Oui. Une série de variables d'environnement OIDC_* permet de brancher Wallos sur un fournisseur SSO existant (Authelia, Keycloak ou équivalent) et même de désactiver le login par mot de passe."
---
> 💡 **TL;DR**
> - Wallos est un tracker d'abonnements open-source et auto-hébergeable en PHP + SQLite, pensé pour repérer tes dépenses récurrentes avant qu'elles ne te surprennent
> - L'installation Wallos Docker se fait en quelques minutes avec Docker Compose, deux volumes à sauvegarder, et des notifications par email, Discord, Telegram, Pushover ou Gotify
> - Gratuit sous licence GPL-3.0, multi-devises, compatible OIDC pour brancher ton SSO existant, et sans aucune connexion bancaire requise

## Wallos Docker : repérer où part ton argent en abonnements

Tu regardes ton relevé bancaire. Il y a une ligne à 11,99 € que tu ne reconnais pas. Tu creuses. C'est un essai gratuit d'un outil SaaS que t'avais oublié d'annuler en mars. Chez moi c'était un VPN testé pendant les vacances, jamais désactivé depuis huit mois. Bon, on va pas se mentir : entre Netflix, Spotify, le stockage cloud, le nom de domaine qui se renouvelle tout seul et la newsletter payante qu'on ne lit plus, personne ne sait vraiment combien il paie chaque mois en abonnements cumulés.

C'est exactement le problème que **Wallos** résout. C'est un projet open-source hébergé sur GitHub (`ellite/wallos`), sous licence GPL-3.0, écrit en PHP avec une base SQLite embarquée. Rien à payer, rien à héberger ailleurs que chez toi. Tu listes chaque abonnement une bonne fois, et Wallos te prévient avant chaque prélèvement.

Concrètement, Wallos gère :

- **Des catégories personnalisables** pour ranger tes abonnements (streaming, SaaS, hébergement, assurances…)
- **Le multi-devises**, avec conversion automatique via l'API Fixer si tu paies en dollars et en euros à la fois
- **Les notifications** sur plusieurs canaux : email, Discord, Telegram, Pushover, Gotify, ou un webhook générique pour brancher ce que tu veux
- **Un tableau de bord avec vue calendrier**, pour voir d'un coup d'œil tous les prélèvements à venir du mois
- **Des comptes pour les membres du foyer**, pratique si tu partages un abonnement Netflix ou un cloud familial
- **L'authentification OIDC**, pour brancher Wallos sur ton fournisseur SSO plutôt que de créer un mot de passe de plus
- **Des recommandations générées par IA** (ChatGPT, Gemini ou un modèle Ollama local) pour repérer les doublons ou les abonnements à renégocier

Une précision importante : Wallos ne se connecte à aucune banque. Tu entres chaque abonnement à la main, ce qui veut dire zéro donnée bancaire transmise à un tiers, mais aussi zéro détection automatique de prélèvement surprise. C'est le prix de la confidentialité. Si tu as déjà un stack auto-hébergé avec des flux RSS suivis via [FreshRSS](/freshrss-docker-lecteur-rss/), l'esprit est le même : tu reprends la main sur une donnée que les géants du cloud géraient à ta place.

## Table des matières

## Prérequis avant d'installer Wallos Docker

Rien d'exotique pour faire tourner **Wallos Docker** sur ton serveur :

- Docker et Docker Compose installés sur un serveur Linux (une VM, un LXC Proxmox ou un Raspberry Pi suffisent largement, le tout étant du PHP + SQLite)
- Un port libre côté hôte, 8282 par défaut dans les exemples du projet
- Un reverse proxy si tu veux exposer Wallos en HTTPS sur un sous-domaine (Caddy, Traefik ou Nginx Proxy Manager)
- Une clé API gratuite chez Fixer si tu veux la conversion automatique multi-devises
- Un peu d'espace disque pour deux volumes : la base de données et les logos d'abonnements téléchargés automatiquement

## Installation de Wallos avec Docker Compose

Crée un dossier dédié :

```bash
mkdir -p ~/wallos && cd ~/wallos
```

Voici le `docker-compose.yml`, repris du dépôt officiel :

```yaml
services:
  wallos:
    container_name: wallos
    image: bellamy/wallos:latest
    ports:
      - "8282:80"
    environment:
      TZ: "Europe/Paris"
    volumes:
      - ./db:/var/www/html/db
      - ./logos:/var/www/html/images/uploads/logos
    restart: unless-stopped
```

L'image `bellamy/wallos` est celle recommandée dans le README du projet : il n'existe pas (encore) d'image publiée sous l'organisation GitHub du projet lui-même. Lance le conteneur :

```bash
docker compose up -d
```

Vérifie que ça démarre correctement :

```bash
docker compose logs -f
```

Une fois le conteneur up, ouvre `http://ip-de-ton-serveur:8282`. L'assistant de première connexion te demande de créer ton compte administrateur. Si tu gères déjà plusieurs stacks Compose sur ton serveur, [Dockge](/dockge-docker-gestionnaire-stacks-compose/) te permet de piloter cette installation Wallos Docker depuis une interface web plutôt qu'en ligne de commande, pratique si tu n'as pas envie de rouvrir un terminal pour chaque mise à jour.

### Avec un reverse proxy Caddy

Si tu veux du HTTPS automatique, ajoute ceci à ton `Caddyfile` :

```caddyfile
abonnements.tondomaine.com {
    reverse_proxy localhost:8282
}
```

Relance Caddy et c'est en place, certificat Let's Encrypt inclus.

## Configuration initiale : abonnements, catégories, devises

Une fois ton install Wallos Docker connectée, trois réglages à faire avant de saisir ton premier abonnement :

### 1. Devise de base et clé Fixer

Dans les paramètres, choisis ta devise par défaut (EUR dans la plupart des cas) puis colle ta clé API Fixer si tu as des abonnements facturés dans une autre devise (un VPN payé en dollars, par exemple). Sans cette clé, Wallos affiche les montants bruts sans conversion.

### 2. Ajout d'un abonnement

Pour chaque abonnement, renseigne :

- Le nom (Wallos va chercher le logo automatiquement pour les services connus)
- Le prix et la devise
- La fréquence de facturation (mensuelle, annuelle, ou un cycle personnalisé)
- La catégorie
- La méthode de paiement (utile pour savoir quelle carte va être débitée)
- La date du prochain prélèvement

Le tableau de bord recalcule aussitôt ton coût mensuel et annuel cumulé, toutes devises converties.

### 3. Comptes pour les membres du foyer

Si un abonnement est partagé (streaming familial, cloud commun), ajoute les membres du foyer concernés dans les paramètres. Chacun voit ce qui le concerne sans que tout le monde ait accès au compte administrateur.

Une fois cette liste à jour, pense à programmer une revue mensuelle. Un simple rappel récurrent dans [Vikunja](/vikunja-docker-gestionnaire-taches/) suffit pour relire ton tableau de bord Wallos une fois par mois et couper ce qui ne sert plus.

## Notifications et intégrations : ne rater aucun prélèvement

Le vrai intérêt de ta configuration Wallos Docker, c'est de recevoir une alerte avant que l'argent ne parte, pas de découvrir la ligne après coup sur ton relevé. Les canaux disponibles :

- **Email** via un serveur SMTP classique
- **Discord**, via un webhook de salon
- **Telegram**, via un bot dédié
- **Pushover** et **Gotify**, pour les notifications push sur mobile
- **Webhook générique**, si tu veux brancher ton propre automate (n8n, par exemple)

Pour chaque abonnement, tu règles le délai d'alerte : trois jours avant, une semaine avant, le jour même. C'est ce réglage, abonnement par abonnement, qui évite la mauvaise surprise.

### SSRF et webhooks internes

Si ton webhook ou ton serveur SMTP tourne sur une adresse IP interne de ton réseau plutôt que sur un nom de domaine public, Wallos bloque la requête par sécurité (protection anti-SSRF). Il faut alors ajouter l'hôte ou l'IP à la variable d'environnement `SSRF_ALLOWLIST` dans ton `docker-compose.yml` pour l'autoriser explicitement.

### Authentification OIDC

Si tu as déjà un fournisseur SSO (Authelia, Keycloak ou équivalent), Wallos peut s'y brancher via une série de variables `OIDC_ENABLED`, `OIDC_CLIENT_ID`, `OIDC_CLIENT_SECRET`, `OIDC_ISSUER` et quelques autres listées dans le README. Tu peux même désactiver complètement le login par mot de passe une fois l'OIDC validé, pour n'avoir qu'un seul point d'authentification sur tout ton homelab.

## Sauvegarde et dépannage

### Sauvegarder tes données

Tout ce que ta stack Wallos Docker sait de tes abonnements vit dans le dossier `./db` du conteneur, et tes logos dans `./logos`. Si le disque lâche, tu perds l'historique complet. Une sauvegarde manuelle rapide :

```bash
cd ~/wallos && tar czf /backup/wallos-$(date +%Y%m%d).tar.gz db/ logos/
```

Branche cette commande sur un cron quotidien, ou sur ton outil de sauvegarde habituel si tu en as déjà un dans ton homelab.

### Le conteneur redémarre en boucle

Vérifie les permissions sur le dossier de données :

```bash
docker compose logs wallos
sudo chown -R $USER:$USER ~/wallos/db ~/wallos/logos
docker compose up -d
```

### Le port 8282 est déjà pris

Change simplement le mapping côté hôte dans le `docker-compose.yml` :

```yaml
ports:
  - "8283:80"
```

### Les notifications ne partent pas

Vérifie d'abord les identifiants SMTP ou le token du bot Telegram dans les paramètres. Si c'est un webhook vers une IP interne, repasse par la case `SSRF_ALLOWLIST` plus haut, c'est la cause la plus fréquente.

### Lire les logs sans repasser par le terminal

Si tu préfères une interface web pour surveiller tes conteneurs plutôt que `docker compose logs -f` à chaque souci, [Dozzle](/dozzle-docker-visionneuse-logs-web/) affiche les logs de Wallos et du reste de ta stack en temps réel dans un navigateur.

## FAQ : Wallos Docker

### Wallos est-il vraiment gratuit ?

Oui. Wallos est open-source sous licence GPL-3.0, publié sur GitHub (`ellite/wallos`). Tu l'installes sur ton propre serveur sans abonnement, sans palier payant et sans limite d'abonnements suivis.

### Wallos peut-il m'envoyer une alerte avant un prélèvement ?

Oui, par email, Discord, Telegram, Pushover, Gotify ou webhook générique. Tu règles le délai d'alerte abonnement par abonnement, par exemple trois jours avant le renouvellement.

### Wallos supporte-t-il l'authentification SSO via OIDC ?

Oui. Une série de variables d'environnement `OIDC_*` permet de brancher Wallos sur un fournisseur SSO existant (Authelia, Keycloak ou équivalent) et même de désactiver le login par mot de passe.

## Conclusion

Wallos Docker ne révolutionne rien, et c'est justement ce qui en fait un bon outil de homelab : il fait une seule chose, lister tes abonnements et te prévenir avant qu'ils ne se renouvellent, et il la fait bien. Pas de connexion bancaire à autoriser, pas de données financières qui transitent chez un tiers, juste une base SQLite qui t'appartient.

L'installation tient en un fichier Compose et deux volumes. Le vrai travail, c'est de prendre vingt minutes pour lister tous tes abonnements actuels, comptes partagés compris, puis de régler une alerte quelques jours avant chaque échéance. Après ça, programme ta revue mensuelle, sauvegarde le dossier `db/`, et tu ne découvriras plus jamais un prélèvement oublié sur ton relevé bancaire.
