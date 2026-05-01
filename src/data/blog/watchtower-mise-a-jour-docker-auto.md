---
title: "Watchtower : mets tes conteneurs Docker à jour sans lever le petit doigt"
description: Configure Watchtower pour mettre à jour automatiquement tes conteneurs Docker. Notifications, exclusions, planning — guide complet homelab.
pubDatetime: 2026-05-01 00:00:00+01:00
modDatetime: 2026-05-01 00:00:00+01:00
author: Brandon Visca
tags:
  - docker
  - watchtower
  - auto-hebergement
  - homelab
  - debutant
  - guide
featured: false
draft: false
focusKeyword: watchtower docker
faqs:
  - question: "Watchtower met-il à jour tous les conteneurs automatiquement ?"
    answer: "Par défaut, oui. Mais tu peux exclure des conteneurs avec le label com.centurylinklabs.watchtower.enable=false pour garder le contrôle total."
  - question: "Watchtower peut-il envoyer des notifications sur Discord ?"
    answer: "Oui. Via la variable d'environnement WATCHTOWER_NOTIFICATION_URL avec une webhook Discord. Telegram et Slack sont aussi supportés."
  - question: "Watchtower redémarre-t-il les conteneurs même sans mise à jour ?"
    answer: "Non, tant que l'image n'a pas changé sur le registry. Le conteneur reste inchangé si l'image locale est identique à la distante."
  - question: "Peut-on programmer les vérifications de Watchtower ?"
    answer: "Oui, avec la variable WATCHTOWER_SCHEDULE au format cron. Par exemple : 0 0 4 * * * pour vérifier tous les jours à 4h du matin."
---
# Watchtower : mets tes conteneurs Docker à jour sans lever le petit doigt

> 💡 **TL;DR** — Ce qu'il faut retenir :
> - Watchtower surveille tes images Docker et redémarre les conteneurs automatiquement quand une nouvelle version sort.
> - Une seule commande Docker suffit pour le lancer. Zéro configuration obligatoire.
> - Tu peux exclure certains conteneurs, programmer les vérifications et recevoir des notifications sur Discord ou Telegram.

## Table des matières

Tu as suivi mon guide pour installer [10 services Docker essentiels](/docker-debutant-services-auto-heberger), ton [Nextcloud](/nextcloud-docker-installation-complete-2025) tourne bien, ton [Vaultwarden](/vaultwarden-docker-gestionnaire-mots-de-passe) aussi. Tu te sens presque un admin système.

Et puis un matin, tu te connectes à Portainer (ou tu fais un `docker ps`) et tu vois que 7 de tes 12 conteneurs utilisent une image vieille de 3 semaines. Des patchs de sécurité sont sortis. Des bugs corrigés. Mais toi, t'as la flemme de faire `docker compose pull && docker compose up -d` sur chaque stack à la main.

C'est normal. C'est aussi exactement pour ça que Watchtower existe.

## Watchtower, c'est quoi exactement ?

Watchtower est un conteneur Docker qui observe les autres conteneurs. Toutes les X minutes, il interroge les registries Docker Hub, GHCR, etc. pour savoir si les images utilisées localement ont été mises à jour. Si oui, il télécharge la nouvelle image et recrée le conteneur avec les mêmes paramètres que l'original.

C'est un robot de ménage pour ton homelab. Il ne répare pas ton carrelage, mais il garde tes services à jour sans que tu aies à y penser.

Point clé : Watchtower ne touche pas aux données. Les volumes sont remontés exactement comme avant. Seul le binaire à l'intérieur du conteneur change.

## L'installation la plus simple possible

Tu veux tester sans te prendre la tête ? Voilà la commande :

```bash
docker run -d \
  --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower
```

C'est tout. Vraiment.

Watchtower va maintenant vérifier toutes les 24 heures (par défaut) si tes images ont changé. S'il trouve une nouvelle version, il la télécharge et redémarre le conteneur concerné.

Pas de fichier YAML, pas de configuration complexe. Un volume pour parler à Docker et c'est parti.

## Passage au docker-compose.yml (la méthode propre)

Si tu gères ton homelab proprement avec des fichiers `docker-compose.yml`, voici la version déclarative :

```yaml
services:
  watchtower:
    image: containrrr/watchtower:latest
    container_name: watchtower
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - WATCHTOWER_CLEANUP=true
      - WATCHTOWER_SCHEDULE=0 0 4 * * *
      - WATCHTOWER_NOTIFICATION_URL=discord://TOKEN@WEBHOOK_ID
      - TZ=Europe/Paris
    labels:
      - com.centurylinklabs.watchtower.enable=false
```

Quelques explications sur les variables :

- `WATCHTOWER_CLEANUP=true` : supprime l'ancienne image locale après mise à jour. Sans ça, ton disque se remplit de layers orphelins jusqu'à ce que tu fasses un `docker system prune` en pleine nuit de désespoir.
- `WATCHTOWER_SCHEDULE` : un cron classique. Ici, tous les jours à 4h du matin. C'est le moment idéal pour pas te réveiller avec une notification Discord pendant ton repas.
- `WATCHTOWER_NOTIFICATION_URL` : on y revient juste en dessous.

## Notifications : savoir ce qui s'est passé

Par défaut, Watchtower travaille dans le silence. C'est pratique, mais un peu flippant. Tu aimes savoir quand ton Vaultwarden a été redémarré à 4h du matin sans ton consentement explicite.

### Discord

Récupère l'URL de webhook de ton serveur Discord. Elle ressemble à ça :

```
https://discord.com/api/webhooks/123456789/abcdefgh
```

Et utilise-la comme ceci :

```
WATCHTOWER_NOTIFICATION_URL=discord://abcdefgh@123456789
```

Note bien : le token est avant l'arobase, l'ID du webhook est après. Watchtower inverse par rapport à l'URL originale. Pas la peine de chercher la logique, c'est comme ça.

### Telegram

```
WATCHTOWER_NOTIFICATION_URL=telegram://BOT_TOKEN@CHAT_ID
```

Crée un bot avec @BotFather, récupère ton chat ID avec @userinfobot, et le tour est joué.

### Email (par Gmail ou ton serveur SMTP)

```
WATCHTOWER_NOTIFICATION_URL=smtp://user:password@smtp.gmail.com:587?from=watchtower@example.com&to=tonmail@example.com
```

C'est plus verbeux, mais ça marche dans un environnement pro où Discord est considéré comme un jouet.

## Exclure des conteneurs du processus

Tu as certains services que tu ne veux pas mettre à jour automatiquement ? Un conteneur critique, une version spécifique de base de données, ou simplement un service expérimental ?

Ajoute ce label dans ton `docker-compose.yml` :

```yaml
services:
  ma_base_de_donnees:
    image: postgres:15
    labels:
      - com.centurylinklabs.watchtower.enable=false
```

Watchtower passera son chemin. Ce conteneur devient invisible pour lui.

Tu peux aussi faire l'inverse : ne surveiller que certains conteneurs. Lance Watchtower avec `--label-enable` et ajoute le label `com.centurylinklabs.watchtower.enable=true` uniquement sur les services que tu veux auto-updater. C'est plus sûr si tu as un gros homelab avec plein de stacks.

## Le mode "monitor only" : regarder sans toucher

Tu es un peu parano ? Tu veux savoir quand une mise à jour est disponible sans que Watchtower la déploie automatiquement ?

```yaml
environment:
  - WATCHTOWER_MONITOR_ONLY=true
```

Dans ce mode, Watchtower envoie une notification dès qu'une image est obsolète, mais ne touche à rien. Tu fais la mise à jour toi-même quand ça t'arrange. C'est le mode recommandé pour les débutants qui veulent comprendre ce qui se passe avant d'automatiser.

## Le planning personnalisé

Par défaut, Watchtower vérifie toutes les 86400 secondes, soit 24h. Si tu veux un contrôle plus fin, utilise `WATCHTOWER_SCHEDULE` au format cron standard :

- `0 0 4 * * *` : tous les jours à 4h du matin
- `0 0 */6 * * *` : toutes les 6 heures
- `0 0 3 * * 1` : tous les lundis à 3h du matin

Le format est : `seconde minute heure jour_du_mois mois jour_de_la_semaine`. Six champs, pas cinq. C'est une variante cron légèrement plus précise que le classique Linux.

Tu peux aussi utiliser `WATCHTOWER_POLL_INTERVAL` en secondes si tu préfères, mais le cron est plus lisible et propre.

## Un cas pratique : l'homelab complet

Voici un `docker-compose.yml` de Watchtower tel que je le fais tourner dans mon homelab. Il surveille tout, nettoie les vieilles images, envoie une notif Discord, et exclut volontairement les bases de données :

```yaml
services:
  watchtower:
    image: containrrr/watchtower:latest
    container_name: watchtower
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - WATCHTOWER_CLEANUP=true
      - WATCHTOWER_SCHEDULE=0 0 4 * * *
      - WATCHTOWER_NOTIFICATION_URL=discord://${WATCHTOWER_DISCORD_TOKEN}@${WATCHTOWER_DISCORD_ID}
      - WATCHTOWER_NOTIFICATIONS_LEVEL=info
      - TZ=Europe/Paris
    labels:
      - com.centurylinklabs.watchtower.enable=false
```

Et dans la stack de ma base de données PostgreSQL :

```yaml
services:
  postgres:
    image: postgres:16-alpine
    container_name: postgres
    labels:
      - com.centurylinklabs.watchtower.enable=false
```

Simple, propre, contrôlé. Les applis (Nextcloud, Vaultwarden, Jellyfin) se mettent à jour toutes seules. La base de données reste en 16-alpine tant que je ne décide pas de la migrer manuellement.

## Pièges et limites à connaître

**Les conteneurs avec des réseaux personnalisés** : Watchtower recrée le conteneur avec les mêmes options, mais vérifie quand même que tes réseaux Docker internes sont bien configurés dans le compose d'origine. Si tu as des réseaux créés à la main, tout se passe bien. Sinon, rien ne casse, mais vérifie quand même la première fois.

**Les mises à jour de base de données** : c'est le piège classique. PostgreSQL 16 vers 17 ne se fait pas toute seule. Watchtower va télécharger la nouvelle image, redémarrer le conteneur, et ça va planter parce que le volume de données est en 16. Solution : exclure les bases de données. Toujours.

**Les images avec `latest` vs tags fixés** : si tu utilises `image: nextcloud`, Watchtower va te mettre à jour vers chaque nouvelle version majeure. Si tu utilises `image: nextcloud:29`, il ne fera rien tant que le tag 29 n'est pas repoussé. C'est une différence majeure à comprendre avant de pleurer devant un Nextcloud cassé.

**La consommation réseau** : Watchtower interroge les registries à chaque cycle. Si tu as 20 conteneurs et un intervalle toutes les 10 minutes, tu vas taper sur les API Docker Hub régulièrement. Ce n'est pas un problème sur un homelab perso, mais ça peut l'être sur un setup pro avec des limitations de rate limit.

## Watchtower vs Diun vs autres

Il existe des alternatives comme Diun (Docker Image Update Notifier) qui fait à peu près la même chose. La différence ? Watchtower redémarre les conteneurs tout seul. Diun ne fait qu'avertir. Si tu veux une notification sans action automatique, Diun est plus léger. Si tu veux le feuilleton complet (détection + action + notification), Watchtower reste le standard.

Pour un homelab, Watchtower est le choix par défaut. Il a une communauté immense, une doc claire, et il fait exactement ce qu'on attend de lui sans configuration excessive.

## Conclusion

Tu as déployé Nextcloud, Vaultwarden, Jellyfin, Uptime Kuma, et tout le reste. C'était la partie fun. La partie chiante, c'est la maintenance. Les mises à jour de sécurité, les patchs, les nouvelles versions mineures.

Watchtower transforme cette corvée en processus invisible. Une commande, une variable d'environnement, et tu peux dormir sur tes deux oreilles en sachant que tes services sont à jour.

Mais n'oublie pas : l'automatisation n'excuse pas l'ignorance. Garde un œil sur tes notifications. Exclus tes bases de données. Et surtout, garde des sauvegardes. Parce qu'un conteneur qui redémarre tout seul à 4h du matin, c'est génial. Un conteneur qui redémarre en boucle parce que l'image est corrompue, c'est beaucoup moins drôle.

Maintenant, arrête de faire `docker compose pull` à la main. T'as mieux à faire.
