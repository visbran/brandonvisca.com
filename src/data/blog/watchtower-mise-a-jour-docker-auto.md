---
title: "Watchtower Docker : containrrr est archivé, le fork qui le remplace en 2026"
description: "Watchtower Docker : containrrr est archivé et casse sous Docker 29. Migre vers le fork maintenu en 2 minutes, labels et notifications inclus."
pubDatetime: 2026-05-01 00:00:00+01:00
modDatetime: "2026-10-17T00:00:00+02:00"
author: Brandon Visca
tags:
  - docker
  - auto-hebergement
  - homelab
  - debutant
  - guide
featured: false
draft: false
focusKeyword: watchtower docker
faqs:
  - question: "Le projet containrrr/watchtower est-il abandonné ?"
    answer: "Oui. Le dépôt containrrr/watchtower a été archivé le 17 décembre 2025 et sa dernière version (v1.7.1) date de novembre 2023. Le fork nicholas-fedor/watchtower, publié sous l'image nickfedor/watchtower, est activement maintenu (v1.23.1 en octobre 2026)."
  - question: "Comment migrer de containrrr/watchtower vers le fork ?"
    answer: "Remplace l'image containrrr/watchtower par nickfedor/watchtower (ou ghcr.io/nicholas-fedor/watchtower) dans ton docker-compose.yml, puis lance docker compose up -d. Les variables WATCHTOWER_* et les labels com.centurylinklabs.watchtower.* restent identiques."
  - question: "Pourquoi Watchtower affiche « client version 1.25 is too old » ?"
    answer: "Docker Engine 29 a relevé la version minimale de l'API à 1.44. L'image containrrr/watchtower parle une API trop ancienne et se fait refuser. Le fork négocie la version d'API automatiquement et fonctionne avec Docker 29."
  - question: "Watchtower peut-il envoyer des notifications sur Discord ou Telegram ?"
    answer: "Oui, via la variable WATCHTOWER_NOTIFICATION_URL au format Shoutrrr : discord://token@webhookid pour Discord, telegram://token@telegram?chats=ID pour Telegram. Plusieurs URL peuvent être séparées par une virgule."
  - question: "Peut-on programmer les vérifications de Watchtower ?"
    answer: "Oui, avec WATCHTOWER_SCHEDULE au format cron à 6 champs, par exemple 0 17 4 * * * pour 4h17 chaque jour. Pense à définir TZ, sinon le planning tourne en UTC."
---
> 💡 **TL;DR**
> - `containrrr/watchtower` est archivé depuis décembre 2025 et plante avec Docker 29. Le fork maintenu s'appelle `nickfedor/watchtower`.
> - La migration tient en une ligne : tu changes l'image, tes variables `WATCHTOWER_*` et tes labels restent valables.
> - Le fork ajoute des choses utiles, comme un délai de refroidissement avant de déployer une image toute fraîche.

Tu as suivi mon guide pour installer [10 services Docker essentiels](/docker-debutant-services-auto-heberger), ton [Nextcloud](/nextcloud-docker-installation-complete-2025) tourne bien, ton [Vaultwarden](/vaultwarden-docker-gestionnaire-mots-de-passe) aussi. Et depuis des mois, Watchtower met tout ça à jour pendant que tu dors.

Sauf qu'un jour, tu mets à jour Docker sur l'hôte, et Watchtower se met à boucler sur une erreur que tu n'as jamais vue. Tu vas sur GitHub voir ce qui se passe, et tu tombes sur un bandeau jaune : *This repository was archived by the owner*.

Pas de panique. Watchtower n'est pas mort, il a juste changé d'adresse.

## Table des matières

## containrrr/watchtower est archivé : ce qui s'est passé

Le dépôt historique `containrrr/watchtower` a été archivé le 17 décembre 2025. Dans les faits, il ne bougeait plus depuis longtemps : sa dernière version, la v1.7.1, date de novembre 2023. Deux ans sans release pour un outil qui a la main sur tous tes conteneurs, ça commençait à faire long.

Le coup de grâce est venu de Docker lui-même. **Docker Engine 29 a relevé la version minimale de son API à 1.44.** L'ancienne image Watchtower parle une version bien plus ancienne de l'API, et le démon la refuse avec ce message :

```text
client version 1.25 is too old. Minimum supported API version is 1.44,
please upgrade your client to a newer version
```

Résultat : Watchtower tourne, mais ne met plus rien à jour. Et comme il échoue en silence si tu n'as pas configuré de notifications, tu peux passer des semaines sans t'en rendre compte.

> ⚠️ **Attention** : vérifie maintenant quelle image ton Watchtower utilise avec `docker inspect watchtower --format '{{.Config.Image}}'`. Si la réponse commence par `containrrr/`, tu es concerné, même si tout semble marcher aujourd'hui.

La relève existe déjà : le fork de Nicholas Fedor, [`nicholas-fedor/watchtower`](https://github.com/nicholas-fedor/watchtower). Même licence Apache-2.0, même fonctionnement, et des releases régulières (v1.23.1 le 13 octobre 2026 au moment où j'écris). Il négocie automatiquement la version d'API avec le démon, donc le problème de Docker 29 disparaît.

## Watchtower Docker, c'est quoi exactement ?

Si tu découvres l'outil : Watchtower est un conteneur Docker qui observe les autres conteneurs. À intervalle régulier, il interroge les registries (Docker Hub, GHCR, etc.) pour savoir si les images utilisées localement ont été mises à jour. Si oui, il télécharge la nouvelle image et recrée le conteneur avec les mêmes paramètres que l'original.

C'est un robot de ménage pour ton homelab. Il ne répare pas ton carrelage, mais il garde tes services à jour sans que tu aies à y penser.

Point clé : Watchtower ne touche pas aux données. Les volumes sont remontés exactement comme avant. Seul le binaire à l'intérieur du conteneur change.

Le fork assume d'ailleurs clairement sa cible : homelabs, media centers, environnements de dev. Pour de la prod commerciale, son README te renvoie vers Kubernetes et une vraie chaîne CI/CD. C'est honnête, et c'est exactement notre terrain de jeu.

## Migrer vers nickfedor/watchtower en 2 minutes

Bonne nouvelle : le fork garde les mêmes variables d'environnement `WATCHTOWER_*` et les mêmes labels `com.centurylinklabs.watchtower.*`. Tes exclusions, ton planning et tes notifications continuent de marcher tels quels.

Dans ton `docker-compose.yml`, change une seule ligne :

```yaml
services:
  watchtower:
    # image: containrrr/watchtower:latest   ← archivé
    image: nickfedor/watchtower:latest
```

Puis recrée le conteneur :

```bash
docker compose pull watchtower
docker compose up -d watchtower
docker logs watchtower --tail 20
```

Si tu préfères GitHub au Docker Hub (rate limits, politique interne, goût personnel), l'image existe aussi sur GHCR : `ghcr.io/nicholas-fedor/watchtower:latest`.

Dans les logs, tu dois voir Watchtower annoncer son planning et les notifications actives, sans erreur d'API. Si c'est le cas, c'est plié.

> 💡 **Astuce** : pour tester sans attendre la prochaine fenêtre du planning, lance un passage unique avec `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nickfedor/watchtower --run-once`. Il vérifie tout une fois, puis s'arrête.

## L'installation la plus simple possible

Tu pars de zéro ? Voilà la commande :

```bash
docker run -d \
  --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  nickfedor/watchtower
```

C'est tout. Vraiment.

Watchtower va vérifier toutes les 24 heures (86 400 secondes, la valeur par défaut) si tes images ont changé. S'il trouve une nouvelle version, il la télécharge et redémarre le conteneur concerné.

Pas de fichier YAML, pas de configuration complexe. Un volume pour parler à Docker et c'est parti. Le fork publie des images pour amd64, arm64, armhf, i386 et même riscv64 : ton Raspberry Pi est couvert.

## Passage au docker-compose.yml (la méthode propre)

Si tu gères ton homelab proprement avec des fichiers `docker-compose.yml`, voici la version déclarative :

```yaml
services:
  watchtower:
    image: nickfedor/watchtower:latest
    container_name: watchtower
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - WATCHTOWER_CLEANUP=true
      - WATCHTOWER_SCHEDULE=0 17 4 * * *
      - WATCHTOWER_NOTIFICATION_URL=discord://TOKEN@WEBHOOK_ID
      - TZ=Europe/Paris
```

Quelques explications sur les variables :

- `WATCHTOWER_CLEANUP=true` : supprime l'ancienne image locale après mise à jour. Sans ça, ton disque se remplit de layers orphelins jusqu'à ce que tu fasses un `docker system prune` en pleine nuit de désespoir.
- `WATCHTOWER_SCHEDULE` : un cron à 6 champs. Ici, tous les jours à 4h17. Pourquoi 17 et pas 00 ? On y revient dans la partie planning.
- `TZ` : obligatoire dès que tu utilises un planning, sinon ton « 4h du matin » tombe en UTC.
- `WATCHTOWER_NOTIFICATION_URL` : on y vient juste en dessous.

## Notifications : savoir ce qui s'est passé

Par défaut, Watchtower travaille dans le silence. C'est pratique, mais un peu flippant. Tu aimes savoir quand ton Vaultwarden a été redémarré à 4h du matin sans ton consentement explicite. Et après l'épisode Docker 29, tu sais aussi pourquoi un Watchtower muet est dangereux : il peut échouer sans que personne ne le remarque.

Les notifications passent par [Shoutrrr](https://github.com/nicholas-fedor/shoutrrr), une bibliothèque qui convertit une URL en message vers un service. Le fork maintient sa propre version de Shoutrrr.

### Discord

Récupère l'URL de webhook de ton serveur Discord. Elle ressemble à ça :

```text
https://discord.com/api/webhooks/123456789/abcdefgh
```

Et utilise-la comme ceci :

```text
WATCHTOWER_NOTIFICATION_URL=discord://abcdefgh@123456789
```

Note bien : le token est avant l'arobase, l'ID du webhook est après. C'est l'inverse de l'URL d'origine. Pas la peine de chercher la logique, c'est comme ça.

### Telegram

```text
WATCHTOWER_NOTIFICATION_URL=telegram://BOT_TOKEN@telegram?chats=CHAT_ID
```

Crée un bot avec @BotFather, récupère ton chat ID avec @userinfobot, et le tour est joué. Attention, le `@telegram` littéral fait partie de l'URL : ce n'est pas un placeholder.

### ntfy (auto-hébergé)

Si tu fais tourner ton propre [serveur de notifications ntfy](/ntfy-docker-notifications-push-auto-hebergees), tu restes 100 % chez toi :

```text
WATCHTOWER_NOTIFICATION_URL=ntfy://ntfy.mondomaine.fr/watchtower
```

### Email (Gmail ou ton serveur SMTP)

```text
WATCHTOWER_NOTIFICATION_URL=smtp://user:password@smtp.gmail.com:587/?fromaddress=watchtower@example.com&toaddresses=tonmail@example.com
```

C'est plus verbeux, mais ça marche dans un environnement pro où Discord est considéré comme un jouet.

Tu veux plusieurs canaux à la fois ? Sépare les URL par une virgule dans la même variable. Et comme ces URL contiennent des tokens, la doc du fork recommande de les passer via un secret Docker plutôt qu'en clair dans le compose.

## Exclure des conteneurs du processus

Tu as certains services que tu ne veux pas mettre à jour automatiquement ? Un conteneur critique, une version spécifique de base de données, ou simplement un service expérimental ?

Ajoute ce label dans ton `docker-compose.yml` :

```yaml
services:
  ma_base_de_donnees:
    image: postgres:16-alpine
    labels:
      - com.centurylinklabs.watchtower.enable=false
```

Watchtower passera son chemin. Ce conteneur devient invisible pour lui. Et oui, le label porte toujours le nom `centurylinklabs` (le créateur originel du projet) : le fork l'a gardé exprès pour ne casser personne.

Tu peux aussi faire l'inverse : ne surveiller que certains conteneurs. Active `WATCHTOWER_LABEL_ENABLE=true` et ajoute le label `com.centurylinklabs.watchtower.enable=true` uniquement sur les services que tu veux auto-updater. C'est plus sûr si tu as un gros homelab avec plein de stacks.

## Le mode "monitor only" : regarder sans toucher

Tu es un peu parano ? Tu veux savoir quand une mise à jour est disponible sans que Watchtower la déploie automatiquement ?

```yaml
environment:
  - WATCHTOWER_MONITOR_ONLY=true
```

Dans ce mode, Watchtower envoie une notification dès qu'une image est obsolète, mais ne touche à rien. Tu fais la mise à jour toi-même quand ça t'arrange, par exemple depuis [Portainer](/portainer-docker-interface-web-conteneurs). C'est le mode recommandé pour les débutants qui veulent comprendre ce qui se passe avant d'automatiser.

Le réglage existe aussi conteneur par conteneur, avec le label `com.centurylinklabs.watchtower.monitor-only=true`. Pratique pour surveiller une appli sensible sans la laisser se mettre à jour toute seule.

## Le planning personnalisé

Par défaut, Watchtower vérifie toutes les 24h. Pour un contrôle plus fin, utilise `WATCHTOWER_SCHEDULE` au format cron :

- `0 17 4 * * *` : tous les jours à 4h17
- `0 17 */6 * * *` : toutes les 6 heures, à la 17e minute
- `0 17 3 * * 1` : tous les lundis à 3h17

Le format est : `seconde minute heure jour_du_mois mois jour_de_la_semaine`. Six champs, pas cinq. C'est une variante cron légèrement plus précise que le classique Linux.

Deux pièges à connaître :

1. **Le fuseau horaire.** Sans `TZ` (ou sans monter `/etc/localtime` en lecture seule), le planning tourne en UTC.
2. **La minute `:00`.** La doc du fork le signale : sur GHCR, certains registries partagés (les images `lscr.io/linuxserver/*`, par exemple) sont vides pendant la première ou les deux premières minutes de chaque heure. Planifie à une minute « bizarre » comme `:17` et tu évites des échecs aléatoires.

Tu peux aussi utiliser `WATCHTOWER_POLL_INTERVAL` en secondes, mais pas en même temps que `WATCHTOWER_SCHEDULE` : c'est l'un ou l'autre.

## La nouveauté du fork : le délai de refroidissement

Voilà une fonction qui manquait vraiment à l'original. Avec `WATCHTOWER_COOLDOWN_DELAY`, Watchtower attend qu'une image ait un âge minimum avant de la déployer :

```yaml
environment:
  - WATCHTOWER_COOLDOWN_DELAY=3d
```

Ici, une image publiée il y a moins de 3 jours est ignorée. L'âge est lu dans les métadonnées de l'image sur le registry. Unités acceptées : `h`, `m`, `s`, `d`, `w` et `M` (30 jours), combinables (`1w12h`).

L'intérêt ? Laisser les autres essuyer les plâtres. Quand un mainteneur pousse une release cassée, les premiers utilisateurs le signalent vite et un correctif suit. Avec un cooldown, tu as une chance de ne jamais voir passer la version fautive.

Le revers, la doc le dit noir sur blanc : ce délai s'applique **aussi aux correctifs de sécurité**. Trois jours, c'est raisonnable sur un homelab. Un mois, c'est trop pour un service exposé sur Internet.

## Un cas pratique : mon compose Watchtower

Voici un `docker-compose.yml` de Watchtower tel que je le fais tourner dans mon homelab, mis à jour pour le fork. Il surveille tout, nettoie les vieilles images, attend 2 jours avant de déployer une nouveauté, envoie une notif Discord, et exclut volontairement les bases de données :

```yaml
services:
  watchtower:
    image: nickfedor/watchtower:latest
    container_name: watchtower
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - WATCHTOWER_CLEANUP=true
      - WATCHTOWER_SCHEDULE=0 17 4 * * *
      - WATCHTOWER_COOLDOWN_DELAY=2d
      - WATCHTOWER_NOTIFICATION_URL=discord://${WATCHTOWER_DISCORD_TOKEN}@${WATCHTOWER_DISCORD_ID}
      - WATCHTOWER_NOTIFICATIONS_LEVEL=info
      - TZ=Europe/Paris
```

Et dans la stack de ma base [PostgreSQL](/postgresql-docker-base-de-donnees) :

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

**Docker 29 et les vieilles images** : on l'a vu, `containrrr/watchtower` est incompatible avec l'API minimale de Docker Engine 29. Si tu vois `client version 1.25 is too old`, ne cherche pas plus loin : migre vers le fork. Forcer `DOCKER_API_VERSION` sur l'ancienne image est un pansement sur un projet qui ne recevra plus aucun correctif.

**Les mises à jour de base de données** : c'est le piège classique. PostgreSQL 16 vers 17 ne se fait pas tout seul. Si tu utilises un tag flottant, Watchtower va télécharger la nouvelle majeure, redémarrer le conteneur, et ça va planter parce que le volume de données est en 16. Solution : exclure les bases de données. Toujours.

> ✅ **Bonne pratique** : épingle les bases de données sur un tag de version majeure (`postgres:16-alpine`, `mariadb:11`) **et** pose le label d'exclusion. Ceinture et bretelles.

**Les images avec `latest` vs tags fixés** : si tu utilises `image: nextcloud`, Watchtower va te mettre à jour vers chaque nouvelle version majeure. Si tu utilises `image: nextcloud:29`, il ne suivra que les nouvelles publications du tag 29. C'est une différence majeure à comprendre avant de pleurer devant un Nextcloud cassé.

**Les réseaux personnalisés** : Watchtower recrée le conteneur avec les mêmes options, réseaux compris. Ça se passe bien dans l'immense majorité des cas, mais vérifie quand même la première fois sur une stack un peu exotique.

**La consommation réseau** : Watchtower interroge les registries à chaque cycle. Avec 20 conteneurs et un intervalle de 10 minutes, tu vas taper régulièrement sur l'API de Docker Hub et ses limites de requêtes. Une vérification par jour suffit largement sur un homelab.

## Watchtower vs Diun vs autres

L'alternative la plus connue reste [Diun](https://github.com/crazy-max/diun) (Docker Image Update Notifier), toujours activement maintenu (v4.33.0). La différence ? Watchtower redémarre les conteneurs tout seul. Diun ne fait qu'avertir. Si tu veux une notification sans action automatique, Diun est plus léger. Si tu veux tout le paquet (détection + action + notification), Watchtower fait le job.

Tu gères tes stacks depuis une interface ? Combine Diun pour l'alerte et [Dockge](/dockge-docker-gestionnaire-stacks-compose) pour lancer la mise à jour d'une stack toi-même. Moins automatique, plus de contrôle.

Pour un homelab, Watchtower reste mon choix par défaut, à condition de pointer vers le fork. Le projet d'origine a une immense base d'utilisateurs, et le fork en a hérité la doc, les conventions et la compatibilité.

## Conclusion

Tu as déployé Nextcloud, Vaultwarden, Jellyfin, Uptime Kuma, et tout le reste. C'était la partie fun. La partie chiante, c'est la maintenance : les mises à jour de sécurité, les patchs, les nouvelles versions mineures.

Watchtower transforme cette corvée en processus invisible. Mais l'archivage de `containrrr/watchtower` rappelle une règle simple : un outil qui a la main sur tous tes conteneurs doit lui-même être maintenu. Si ton compose pointe encore vers l'ancienne image, change cette ligne aujourd'hui.

Et n'oublie pas : l'automatisation n'excuse pas l'ignorance. Garde un œil sur tes notifications. Exclus tes bases de données. Et surtout, garde des sauvegardes. Un conteneur qui redémarre tout seul à 4h du matin, c'est génial. Un conteneur qui redémarre en boucle parce que l'image est corrompue, c'est beaucoup moins drôle.

Pour la configuration avancée (hooks de cycle de vie, registries privés, API HTTP), la [documentation officielle du fork](https://watchtower.nickfedor.com/) détaille toutes les options.

Maintenant, va vérifier quelle image ton Watchtower utilise. T'as peut-être une surprise.
