---
title: "Vikunja Docker : gestionnaire de tâches auto-hébergé (alternative Todoist)"
description: "Vikunja docker : installe ce gestionnaire de tâches open source avec vues liste, Kanban et Gantt, sans dépendre de Todoist."
pubDatetime: "2026-10-14T11:02:12+02:00"
modDatetime: "2026-10-13T08:00:00.000Z"
author: Brandon Visca
tags:
  - auto-hebergement
  - docker
  - intermediaire
featured: false
draft: false
focusKeyword: vikunja docker
faqs:
  - question: "Vikunja consomme combien de ressources sur un petit serveur ?"
    answer: "Peu. L'image est un seul binaire Go avec frontend intégré. En SQLite et usage perso, ça tourne confortablement sur un Raspberry Pi ou un petit LXC avec 512 Mo de RAM alloués."
  - question: "Peut-on importer ses tâches Todoist dans Vikunja ?"
    answer: "Oui. Vikunja propose un import natif depuis Todoist, Trello et Microsoft To-Do, accessible dans les paramètres utilisateur une fois connecté à ton instance."
  - question: "Faut-il une base de données externe pour faire tourner Vikunja Docker ?"
    answer: "Non pour démarrer. Vikunja embarque SQLite par défaut. Pour une instance qui grossit ou plusieurs utilisateurs actifs, PostgreSQL ou MySQL encaissent mieux la charge sur la durée."
---
> 💡 **TL;DR**
> - Vikunja Docker est un gestionnaire de tâches open source (AGPLv3) avec vues liste, Kanban et Gantt, alternative crédible à Todoist
> - Une seule image `vikunja/vikunja`, port 3456, SQLite par défaut : installable en une commande `docker run`
> - Import natif depuis Todoist, Trello et Microsoft To-Do pour migrer sans tout retaper à la main

## Table des matières

Todoist, c'est bien tant que tu ne regardes pas la facture annuelle ni la question de savoir où vivent tes tâches. Chez moi, la bascule s'est faite le jour où j'ai voulu exporter mes projets pour les relire tranquillement : format propriétaire, API limitée côté gratuit, et une dépendance totale à un service dont je ne contrôle rien.

**Vikunja Docker** répond à ce problème sans rien enlever côté fonctionnalités. Listes, Kanban, Gantt, tableau, partage de projet : tout ce qu'on attend d'un gestionnaire de tâches sérieux, en auto-hébergé.

## Qu'est-ce que Vikunja exactement

Vikunja est un gestionnaire de tâches open source sous licence AGPLv3, développé par une petite équipe indépendante et financé en bootstrap, sans levée de fonds ni rachat par un éditeur SaaS. Le code est public, l'hébergement cloud optionnel est fait en Europe, et rien n'empêche de tout faire tourner chez soi.

Côté fonctionnalités, le logiciel couvre large :

- **Quatre vues** par projet : liste classique, Kanban façon Trello, Gantt pour les délais, et vue tableau
- **Partage de projets** et assignation de tâches à plusieurs personnes, utile en famille ou en petite équipe
- **Sous-tâches, étiquettes, priorités et dates d'échéance** avec rappels
- **Import natif** depuis Todoist, Trello et Microsoft To-Do, pour migrer sans tout retaper
- **API REST documentée**, pratique si tu veux brancher un script ou un second outil dessus

Le point qui compte le plus pour une install maison : depuis les versions récentes, l'API et le frontend sont fusionnés dans **une seule image Docker**. Fini le temps où il fallait lancer deux conteneurs séparés et les faire discuter correctement.

## Installation rapide de Vikunja Docker

La commande la plus simple utilise SQLite, donc aucune base externe à gérer. Crée d'abord les dossiers qui vont stocker tes données :

```bash
mkdir -p ~/vikunja/files ~/vikunja/db
cd ~/vikunja
chown 1000 files db
```

Lance ensuite le conteneur :

```bash
docker run -d --name vikunja \
  -p 3456:3456 \
  -v $PWD/files:/app/vikunja/files \
  -v $PWD/db:/db \
  -e VIKUNJA_CORS_ENABLE=false \
  --restart unless-stopped \
  vikunja/vikunja
```

L'interface est accessible sur `http://IP_DU_SERVEUR:3456`. La variable `VIKUNJA_CORS_ENABLE=false` désactive une vérification CORS qui, par défaut, attend une URL publique configurée : sans elle, tu risques des erreurs bizarres côté navigateur si tu testes en local.

Premier démarrage, Vikunja te propose de créer un compte administrateur. Rien n'est préconfiguré, pas de mot de passe par défaut qui traîne dans la doc.

## Installation avec Docker Compose et PostgreSQL

La commande `docker run` suffit pour tester, mais pour une instance qui dure, Compose avec une vraie base de données tient mieux la charge si plusieurs comptes écrivent en même temps. Crée un dossier dédié avec un `compose.yaml` :

```yaml
services:
  vikunja:
    image: vikunja/vikunja
    restart: unless-stopped
    environment:
      VIKUNJA_SERVICE_PUBLICURL: http://IP_DU_SERVEUR:3456
      VIKUNJA_DATABASE_HOST: db
      VIKUNJA_DATABASE_TYPE: postgres
      VIKUNJA_DATABASE_USER: vikunja
      VIKUNJA_DATABASE_PASSWORD: change-moi
      VIKUNJA_DATABASE_DATABASE: vikunja
      VIKUNJA_SERVICE_SECRET: colle-ici-une-chaine-aleatoire-longue
    ports:
      - "3456:3456"
    volumes:
      - ./files:/app/vikunja/files
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:18
    restart: unless-stopped
    environment:
      POSTGRES_USER: vikunja
      POSTGRES_PASSWORD: change-moi
    volumes:
      - ./db:/var/lib/postgresql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -h localhost -U $$POSTGRES_USER"]
      interval: 30s
      start_period: 15s
      start_interval: 5s
```

Trois points avant de lancer `docker compose up -d` :

- `VIKUNJA_SERVICE_PUBLICURL` doit correspondre à l'adresse réelle par laquelle tu accèdes à Vikunja, sinon certains liens internes (notifications, partage) pointeront au mauvais endroit.
- `VIKUNJA_SERVICE_SECRET` sert à signer les sessions. Génère une vraie chaîne aléatoire, par exemple avec `openssl rand -hex 32`, et ne la change plus une fois des comptes créés.
- Change les deux `change-moi` avant le premier démarrage. Les reprendre tels quels sur une instance accessible depuis l'extérieur, c'est une porte ouverte gratuite.

## Vikunja vs Todoist : ce qui change concrètement

La question qu'on me pose dès que je montre mon instance Vikunja : "c'est aussi bien que Todoist ?" Oui et non, ça dépend de ce que tu cherches.

| Critère | Vikunja | Todoist |
|---|---|---|
| Coût | Gratuit, auto-hébergé | Gratuit limité, payant au-delà |
| Contrôle des données | Total, chez toi | Chez l'éditeur |
| Vue Gantt | Incluse | Réservée aux formules payantes |
| Vue Kanban | Incluse | Réservée aux formules payantes |
| Maintenance | À ta charge | Aucune |
| Mobile natif | Appli officielle, moins polie | Très soignée |
| Import | Depuis Todoist, Trello, MS To-Do | - |

Mon avis après usage réel : Todoist reste plus fluide au quotidien sur mobile, l'appli est clairement plus travaillée. Mais pour qui veut du Kanban et du Gantt sans payer un abonnement, et garder ses tâches chez soi, Vikunja couvre largement le besoin. L'import natif rend la bascule indolore : pas besoin de retaper trois ans de tâches à la main.

## Sécuriser ton instance Vikunja

⚠️ Une instance de gestion de tâches contient souvent plus d'infos perso qu'on ne le pense : rendez-vous médicaux, mots de passe oubliés dans une note de tâche, projets pro. Quelques réflexes avant d'exposer Vikunja sur Internet :

- Passe par un reverse proxy avec TLS (Nginx Proxy Manager, Caddy) plutôt que d'exposer le port 3456 brut.
- Active l'inscription publique seulement si tu en as vraiment besoin. Par défaut, laisse la création de compte fermée et crée les comptes toi-même.
- Si l'accès reste interne à ton réseau, bloque le port au firewall en plus de compter sur l'authentification applicative :

```bash
sudo ufw deny 3456/tcp
sudo ufw allow from 192.168.1.0/24 to any port 3456
```

✅ Sauvegarde régulièrement le dossier `files` et, si tu es passé sur PostgreSQL, fais un `pg_dump` planifié du conteneur `db`. Une base de tâches perdue, ça fait mal plus vite qu'on l'imagine.

## Importer tes tâches Todoist dans Vikunja

Une fois connecté à ton instance, l'import se fait depuis les paramètres du compte, section migration. Vikunja te demande un export ou un jeton d'accès selon le service source, puis recrée les projets, les tâches et, dans la mesure du possible, les dates d'échéance et les étiquettes.

L'import ne casse rien côté Todoist : tu gardes ton compte d'origine actif pendant la transition, le temps de vérifier que tout est bien arrivé de l'autre côté avant de couper l'abonnement.

## Mettre à jour Vikunja Docker

Avec `docker run`, recrée simplement le conteneur avec la dernière image :

```bash
docker stop vikunja && docker rm vikunja
docker pull vikunja/vikunja
docker run -d --name vikunja [mêmes options qu'au premier lancement]
```

Avec Compose, deux commandes suffisent depuis le dossier d'installation :

```bash
docker compose pull && docker compose up -d
```

Les données SQLite ou PostgreSQL restent dans leurs volumes respectifs, aucune perte entre deux versions.

## Dépannage courant

**Erreur CORS dans la console navigateur.** Signe que `VIKUNJA_SERVICE_PUBLICURL` n'est pas défini ou ne correspond pas à l'URL réelle d'accès. En test local sans URL publique, ajoute `VIKUNJA_CORS_ENABLE=false`.

**Le conteneur refuse d'écrire dans `files`.** Vérifie les permissions du dossier côté hôte : l'image tourne avec l'UID 1000, un `chown 1000 files` mal appliqué bloque les uploads de pièces jointes.

**Connexion à PostgreSQL refusée au démarrage.** Le `depends_on` avec `condition: service_healthy` attend que le healthcheck Postgres passe avant de démarrer Vikunja. Si ça boucle, regarde les logs du conteneur `db` plutôt que ceux de Vikunja : le souci vient presque toujours de la base, pas de l'appli.

## Aller plus loin dans ton homelab

Vikunja ne fait qu'une chose, de la gestion de tâches, mais il s'intègre bien dans une stack homelab existante. Si tu gères déjà plusieurs conteneurs à la main, [Dockge](/dockge-docker-gestionnaire-stacks-compose/) te simplifie la vie pour éditer et mettre à jour ce genre de services Compose sans ressortir le SSH à chaque fois.

Pour suivre ce qui se passe sous le capot pendant que tu testes ta config Vikunja, [Dozzle](/dozzle-docker-visionneuse-logs-web/) donne une vue en direct sur les logs du conteneur, pratique pour repérer une erreur de base de données sans taper `docker logs -f` en boucle.

Côté organisation documentaire autour de tes projets, [Paperless-ngx](/paperless-ngx-docker-guide-auto-hebergement/) complète bien Vikunja : les tâches d'un côté, les documents scannés et classés de l'autre. Et si tu veux centraliser tes flux d'actualité en plus de tes tâches, [FreshRSS](/freshrss-docker-lecteur-rss/) tourne sur la même philosophie légère et sans verrouillage.

## Conclusion

Vikunja Docker fait le pari inverse de Todoist : moins poli sur mobile, mais totalement sous ton contrôle, avec Kanban et Gantt inclus sans palier payant. Pour qui gère déjà quelques services auto-hébergés et veut sortir ses tâches d'un silo propriétaire, l'installation d'un soir se rentabilise vite.

Si la seule chose qui te retient encore chez Todoist, c'est la peur de perdre tes listes actuelles, l'import natif règle ça en quelques clics. Le reste, c'est juste une image Docker et un port à ouvrir.
