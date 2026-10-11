---
title: "Wallabag Docker : lecture différée auto-hébergée (alternative Pocket)"
description: "Wallabag docker en auto-hébergement : installation Docker Compose, migration depuis Pocket, extensions et dépannage de ta lecture différée."
pubDatetime: "2026-10-11T11:01:11+02:00"
modDatetime: "2026-10-10T08:00:00.000Z"
author: Brandon
tags:
  - auto-hebergement
  - reverse-proxy
  - sauvegarde
  - intermediaire
featured: false
draft: false
focusKeyword: wallabag docker
faqs:
  - question: "Wallabag docker consomme combien de ressources sur mon serveur ?"
    answer: "Avec MariaDB et Redis dans le même compose, compte environ 512 Mo de RAM au repos. Un petit VPS ou un conteneur LXC suffit largement pour un usage perso."
  - question: "Je peux migrer mes articles Pocket vers wallabag docker ?"
    answer: "Oui, wallabag importe les exports Pocket, Instapaper et Readability au format JSON ou HTML depuis la section Import de ton compte, article par article."
  - question: "Comment je sauvegarde une instance wallabag docker ?"
    answer: "Deux volumes à archiver : le dossier MariaDB et le dossier des images des articles. Un dump SQL régulier avec mysqldump complète la sauvegarde des fichiers."
---
> 💡 **TL;DR**
> - Wallabag docker auto-hébergé remplace Pocket : tu sauvegardes un article depuis ton navigateur ou ton téléphone et tu le lis plus tard, sans pub ni tracking
> - Installation via Docker Compose avec MariaDB et Redis, image officielle `wallabag/wallabag`, migration directe depuis un export Pocket
> - Extensions Firefox/Chrome, appli mobile Android/iOS, export vers liseuse Kindle ou Kobo, tout reste chez toi

## Wallabag docker : ta lecture différée sans dépendre d'un GAFAM

Tu tombes sur un article intéressant en pleine réunion, tu n'as pas le temps de le lire, tu le mets de côté. Chez la plupart des gens, ça finit dans un onglet ouvert depuis trois semaines ou dans Pocket, racheté par Mozilla puis fermé en 2025. Spoiler : ça va marcher autrement chez toi.

**Wallabag** fait exactement ce que faisait Pocket, sauvegarder une page web pour la lire plus tard en mode texte propre, sans pub, sans tracker. La différence, c'est que l'instance tourne sur ton serveur. Le projet est développé par Nicolas Lœuillet et une poignée de contributeurs, publié en open source sur [github.com/wallabag/wallabag](https://github.com/wallabag/wallabag). Dernière version stable au moment où j'écris : 2.6.14.

Avec wallabag docker, tu montes ton instance en quelques minutes derrière un docker-compose.yml. Pas de compte tiers, pas de limite d'articles sauvegardés, pas de décision éditoriale sur ce que tu as le droit de garder.

## Table des matières

## Pourquoi passer à wallabag docker plutôt que Pocket ou Instapaper

Pocket a fermé ses portes. Instapaper vit encore, mais reste un service tiers avec un modèle freemium qui limite les fonctionnalités gratuites. Les deux ont un point commun embêtant : tes habitudes de lecture, ce que tu gardes, ce que tu archives, appartiennent à leurs serveurs, pas aux tiens.

Ça inverse la logique. Trois raisons concrètes de franchir le pas :

- **Confidentialité réelle** : aucun tiers ne sait ce que tu lis ni quand. Pas de profilage publicitaire basé sur tes articles sauvegardés.
- **Pérennité** : un service gratuit peut fermer du jour au lendemain, comme Pocket. Ton instance auto-hébergée, elle, dure aussi longtemps que ton serveur tourne.
- **Pas de limite artificielle** : nombre d'articles, de tags, de règles de tri, tout est illimité puisque c'est ta base de données.

Si tu gères déjà un flux d'actualités en RSS avec [FreshRSS](/freshrss-docker-lecteur-rss/), wallabag docker vient compléter le duo naturellement : FreshRSS pour découvrir et trier, lui pour garder ce qui mérite une vraie lecture plus tard. Les deux outils ne se marchent pas sur les pieds, ils couvrent deux moments différents de ta consommation d'articles.

## Installation wallabag docker avec Docker Compose

L'image officielle est `wallabag/wallabag`, publiée sur Docker Hub. La documentation du projet recommande une stack complète avec MariaDB pour la base de données et Redis pour les files de tâches. Voici une configuration de départ :

```yaml
services:
  wallabag:
    image: wallabag/wallabag
    restart: unless-stopped
    environment:
      - SYMFONY__ENV__DATABASE_DRIVER=pdo_mysql
      - SYMFONY__ENV__DATABASE_HOST=db
      - SYMFONY__ENV__DATABASE_PORT=3306
      - SYMFONY__ENV__DATABASE_NAME=wallabag
      - SYMFONY__ENV__DATABASE_USER=wallabag
      - SYMFONY__ENV__DATABASE_PASSWORD=change_moi
      - SYMFONY__ENV__DATABASE_CHARSET=utf8mb4
      - SYMFONY__ENV__DOMAIN_NAME=https://lecture.tondomaine.fr
      - SYMFONY__ENV__SERVER_NAME="Mon wallabag"
      - SYMFONY__ENV__FOSUSER_REGISTRATION=false
      - MYSQL_ROOT_PASSWORD=change_moi_aussi
    ports:
      - "8085:80"
    volumes:
      - ./images:/var/www/wallabag/web/assets/images
    depends_on:
      - db
      - redis
  db:
    image: mariadb
    restart: unless-stopped
    environment:
      - MYSQL_ROOT_PASSWORD=change_moi_aussi
    volumes:
      - ./data:/var/lib/mysql
  redis:
    image: redis:alpine
    restart: unless-stopped
```

Trois points à vérifier avant de lancer. D'abord, `SYMFONY__ENV__DOMAIN_NAME` doit correspondre exactement à l'URL publique que tu vas utiliser, protocole inclus : l'appli refuse certaines actions si l'URL réelle diffère de celle déclarée. Ensuite, mets de vrais mots de passe, pas les valeurs d'exemple ci-dessus. Enfin, `SYMFONY__ENV__FOSUSER_REGISTRATION=false` ferme les inscriptions publiques, important si ton instance finit exposée sur internet.

Lance ensuite :

```bash
docker compose up -d
```

Si tu gères plusieurs stacks Docker sur ton homelab, [Dockge](/dockge-docker-gestionnaire-stacks-compose/) te donne une interface web pour éditer ce compose et suivre les logs de démarrage sans repasser par le terminal à chaque fois.

## Première configuration de ton instance wallabag docker

Au premier démarrage, l'instance crée la base de données et le compte administrateur par défaut, identifiants `wallabag` / `wallabag`. Change ce mot de passe immédiatement depuis le menu Config, onglet Informations utilisateur.

Passe ensuite ton instance derrière un reverse proxy en HTTPS, Nginx ou Caddy, plutôt que de l'exposer en HTTP brut sur un port. Il gère des identifiants de connexion et, potentiellement, du contenu sensible issu de newsletters ou de paywalls contournés : ça mérite un certificat valide, pas un port ouvert nu sur ta box.

Dans Config, section Articles RSS, active le flux RSS de ta liste "à lire" si tu veux la retrouver dans un lecteur externe. Et dans Config, section Règles, tu peux automatiser le tag ou l'archivage d'un article selon son domaine d'origine, pratique si tu sauvegardes beaucoup depuis les mêmes sites.

## Extensions, appli mobile et import depuis Pocket

Le vrai confort vient de ses points d'entrée. L'extension navigateur, disponible pour Firefox et Chrome, ajoute un bouton qui sauvegarde la page active en un clic, sans quitter ton onglet. Côté mobile, les applications Android et iOS officielles permettent de consulter ta liste hors ligne, pratique dans le métro ou en avion.

Pour les possesseurs de liseuse, il génère un export EPUB de tes articles non lus, directement envoyable sur un Kindle ou un Kobo. Fini les captures d'écran illisibles ou les PDF mal formatés.

Si tu migres depuis Pocket, exporte d'abord tes données depuis l'interface Pocket au format HTML ou JSON, puis importe ce fichier dans wallabag docker via Config, section Import. L'import conserve les tags et le statut lu/non lu de chaque article. Compte quelques minutes pour quelques centaines d'articles, le temps qu'il récupère le contenu propre de chaque page.

## Wallabag docker face aux alternatives self-hosted

Il n'est pas la seule option pour de la lecture différée auto-hébergée, mais il reste le plus mature. Omnivore, porté par une petite équipe, a fermé son service hébergé en 2025 et son avenir en self-hosted reste incertain. Readeck est un projet plus récent, plus léger, mais avec un écosystème d'extensions et d'applis mobiles encore limité comparé aux dix ans d'existence de wallabag.

Si ton besoin dépasse la simple lecture différée et touche à l'archivage de documents administratifs, factures ou contrats numérisés, [Paperless-ngx](/paperless-ngx-docker-guide-auto-hebergement/) répond à un problème voisin mais différent : lui classe des documents avec OCR, l'autre sauvegarde des pages web pour plus tard. Les deux cohabitent très bien sur le même serveur, chacun dans son rôle.

## Dépannage : les pièges classiques avec wallabag docker

**L'import d'articles ne récupère que le titre, pas le contenu.** Certains sites bloquent le user-agent du service de récupération de wallabag docker. Vérifie les logs du conteneur avec `docker logs wallabag`, ou passe par [Dozzle](/dozzle-docker-visionneuse-logs-web/) si tu veux une interface web plus confortable pour suivre ça en continu plutôt que de retaper la commande à chaque test.

**Impossible de se connecter après un changement de domaine.** Si tu modifies `SYMFONY__ENV__DOMAIN_NAME` après le premier démarrage, la valeur ne se met pas à jour toute seule en base. Il faut la corriger manuellement via la console Symfony du conteneur, ou repartir d'une base vierge si l'instance est encore vide.

**L'extension navigateur affiche une erreur d'authentification.** Elle utilise son API, qui a besoin d'un client OAuth généré depuis Config, section API. Un renouvellement de mot de passe administrateur invalide parfois ce client, il faut alors le régénérer et remettre les nouveaux identifiants dans l'extension.

**Les images des articles disparaissent après une mise à jour.** C'est que le volume `images` n'était pas monté correctement dans le compose. Vérifie que le chemin déclaré dans `volumes` existe bien sur l'hôte et appartient à l'utilisateur qui fait tourner Docker, sinon il écrit dans le vide à chaque sauvegarde.

## Conclusion

Wallabag docker coche toutes les cases qui manquaient à Pocket au moment où le service a fermé : tu possèdes tes données, tu décides de la durée de vie de ton instance, et tu n'as de compte à rendre à personne sur ce que tu lis. L'installation via Docker Compose prend dix minutes, la vraie valeur se construit après, au fil des articles que tu sauvegardes.

Mon conseil : commence petit, avec juste l'extension navigateur et l'appli mobile, avant de te lancer dans les règles d'automatisation ou l'export EPUB. Tu verras vite s'il remplace vraiment ton réflexe Pocket ou si tu préfères garder tes onglets ouverts pendant trois semaines, comme avant.
