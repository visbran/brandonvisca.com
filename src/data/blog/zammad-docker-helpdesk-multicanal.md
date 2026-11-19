---
title: "Zammad Docker : helpdesk multi-canal auto-hébergé"
description: "Déploie Zammad Docker : helpdesk open source multicanal auto-hébergé avec email, chat et réseaux sociaux. Guide Compose complet et comparatif GLPI."
pubDatetime: "2026-11-19T11:00:54+01:00"
modDatetime: "2026-11-18T08:00:00.000Z"
author: Brandon
tags:
  - sysadmin
  - auto-hebergement
  - glpi
  - intermediaire
featured: false
draft: false
focusKeyword: zammad docker
faqs:
  - question: "Zammad Docker en self-hosted est-il vraiment gratuit ?"
    answer: "Oui. Le logiciel est publié sous licence AGPLv3 par Zammad GmbH, sans frais de licence en auto-hébergement. Seuls les contrats de support, à partir de 2 999 euros par an, sont payants et restent optionnels."
  - question: "Combien de RAM faut-il pour faire tourner Zammad en Docker ?"
    answer: "La documentation officielle recommande au moins 4 Go de RAM pour les conteneurs. Avec Elasticsearch actif pour la recherche plein texte, prévois une marge supplémentaire plutôt que de viser le strict minimum."
  - question: "Zammad peut-il remplacer GLPI pour gérer mon parc informatique ?"
    answer: "Non, pas directement. Zammad est un helpdesk multicanal centré sur le ticketing et la relation client, sans module d'inventaire matériel. GLPI reste la référence si tu dois suivre ton parc en plus du support."
---
> 💡 **TL;DR**
> - Zammad Docker te donne un helpdesk open source multicanal (email, chat, réseaux sociaux) gratuit en auto-hébergement
> - Installation officielle en deux commandes : `git clone` du dépôt zammad-docker-compose puis `docker compose up -d`
> - Comparatif avec GLPI inclus, plus la configuration des canaux, la maintenance et le dépannage courant

## Zammad Docker : le helpdesk open source qui centralise tous tes canaux

Tu gères le support de ton équipe entre trois boîtes mail, un canal Slack et des messages WhatsApp qui arrivent on ne sait trop comment. Résultat : des tickets perdus, des clients qui relancent deux fois, et toi qui cherches un historique dans cinq outils différents. Chez moi, ça a duré un an avant que je craque.

**Zammad** règle ce problème précis. C'est un helpdesk open source développé par Zammad GmbH, publié sous licence AGPLv3 et soutenu par la Zammad Foundation. La version stable actuelle est la branche 7.x, avec une 7.2.2 sortie en octobre 2026. L'idée centrale : un seul outil qui reçoit tes tickets quel que soit le canal d'origine, email, formulaire web, chat sur ton site ou réseaux sociaux, et qui les affiche dans une seule file d'attente pour ton équipe.

La bonne nouvelle, c'est que l'auto-hébergement de Zammad est gratuit. Zammad vend des offres cloud payantes (de 7 à 25 euros par agent et par mois) et des contrats de support pour l'auto-hébergement, mais le logiciel lui-même ne te coûte rien si tu le déploies sur ton propre serveur. Avec Docker, ce déploiement se résume à deux commandes.

## Table des matières

## Prérequis et ressources nécessaires

Avant de lancer ta stack Zammad Docker, vérifie ces quatre points :

- **Docker et Docker Compose** installés et à jour sur ton serveur ou ta VM.
- **4 Go de RAM minimum**, selon la documentation officielle de Zammad. La stack embarque Elasticsearch pour la recherche plein texte, et ce composant est gourmand. Si ton serveur fait aussi tourner d'autres services, vise plus large.
- **Un réglage noyau pour Elasticsearch** : le paramètre `vm.max_map_count` doit être porté à au moins 262144 sur l'hôte, sinon Elasticsearch refuse de démarrer.
- **Un nom de domaine** si tu veux exposer Zammad en HTTPS derrière un reverse proxy. En local, l'accès par IP et port suffit pour tester.

Bon, on va pas se mentir : Zammad n'est pas le service le plus léger à auto-héberger. Entre PostgreSQL, Redis, Elasticsearch, Memcached et les conteneurs applicatifs eux-mêmes, tu fais tourner facilement six à sept conteneurs en permanence. Ne tente pas ça sur un Raspberry Pi.

## Docker Compose : la stack complète

Monter Zammad Docker revient à récupérer un dépôt déjà préconfiguré. Zammad maintient officiellement son propre dépôt `zammad-docker-compose`, qui embarque tous les services nécessaires. Pas besoin d'écrire ton propre fichier YAML de zéro.

Commence par régler le noyau pour Elasticsearch :

```bash
sudo sysctl -w vm.max_map_count=262144
```

⚠️ Ce réglage ne survit pas à un redémarrage si tu ne le persistes pas. Ajoute la ligne `vm.max_map_count=262144` dans `/etc/sysctl.conf` pour éviter la mauvaise surprise au prochain reboot du serveur.

Clone ensuite le dépôt officiel et lance la stack :

```bash
git clone https://github.com/zammad/zammad-docker-compose.git
cd zammad-docker-compose
docker compose up -d
```

Le `docker compose up -d` télécharge et démarre l'ensemble : base PostgreSQL, Redis pour le cache et les jobs en arrière-plan, Elasticsearch pour la recherche, Memcached, le serveur applicatif Rails, le scheduler des tâches planifiées, le serveur websocket pour le temps réel, et Nginx en frontal. Le cache Redis mérite un mot à part : si tu veux comprendre ce qui tourne réellement sous le capot d'une base clé-valeur comme celle-ci, j'ai un [guide Redis Docker](/redis-docker-base-donnees-cle-valeur/) qui détaille son fonctionnement.

Compte une bonne minute avant que tous les conteneurs soient prêts, le temps que PostgreSQL initialise ses tables et qu'Elasticsearch monte son index.

✅ Pour les mises à jour futures, le dépôt se met à jour avec un simple `git pull` suivi d'un nouveau `docker compose pull && docker compose up -d`. On y revient plus bas.

## Premier lancement et configuration multicanal

Une fois ta stack Zammad Docker lancée, ouvre ton navigateur sur `http://localhost:8080` (ou l'IP de ton serveur suivie du port exposé). L'assistant de première configuration te demande de créer ton compte administrateur et de nommer ton organisation. Cinq minutes, pas plus.

La vraie question c'est : comment tu branches tes canaux existants là-dedans ?

Dans **Manage > Channels**, tu trouves les connecteurs disponibles :

- **Email** : tu configures un compte IMAP/SMTP (Gmail, Outlook, ton propre serveur mail) et Zammad récupère les messages entrants comme des tickets.
- **Formulaire web** : un widget à coller sur ton site, les soumissions deviennent des tickets automatiquement.
- **Chat en direct** : un widget JavaScript embarqué sur ton site, avec notification en temps réel côté agent.
- **Réseaux sociaux et Telegram** : ces connecteurs demandent chacun leurs propres identifiants d'application (clé API Twitter/X, app Facebook, bot Telegram). Sans ces clés, le connecteur reste grisé.

Chaque canal alimente la même file de tickets. Un client qui t'écrit par email puis relance sur le chat du site, ton agent voit l'historique complet au même endroit. C'est exactement le problème que je décrivais en intro, réglé.

💡 Si en plus du support client tu dois gérer des campagnes email ou une newsletter, ce n'est pas le rôle de Zammad. J'utilise [Listmonk](/listmonk-docker-newsletter-auto-hebergee/) pour ça, auto-hébergé aussi, mais pensé pour l'envoi de masse plutôt que le ticketing.

## Zammad vs GLPI : lequel choisir pour ton helpdesk

C'est la question qu'on me pose le plus souvent dès qu'on parle ITSM auto-hébergé : Zammad ou GLPI ?

Les deux sont open source, les deux se déploient facilement en Docker, mais ils ne répondent pas au même besoin.

**Zammad Docker** est centré sur la relation client et le ticketing multicanal. Email, chat, réseaux sociaux, tout converge vers une seule file. Pas de module d'inventaire matériel natif, pas de gestion de parc. C'est un outil de support, pensé pour des équipes qui répondent à des demandes venant de partout.

**GLPI** part d'une autre logique : inventaire de parc, suivi des licences, gestion des interventions techniques, avec un module de ticketing intégré mais moins orienté canaux externes. GLPI brille quand tu dois savoir quel ordinateur appartient à qui, avec quelle configuration, avant même de parler du ticket. Et si ton besoin touche aussi la gestion documentaire, classer tes contrats fournisseurs ou tes factures à côté de tes tickets passe plutôt par un outil dédié comme [Paperless-ngx](/paperless-ngx-docker-guide-auto-hebergement/), que j'ai détaillé de son côté.

Si ton problème c'est « je reçois des demandes clients de partout et je veux une seule file d'attente propre », prends Zammad. Si ton problème c'est « je dois gérer mon parc informatique et accessoirement du support interne », GLPI fait plus de sens. Rien n'empêche de faire tourner les deux côte à côte sur le même serveur, chacun pour son usage.

## Maintenance, mise à jour et dépannage

Une fois ta stack Zammad Docker en production, trois réflexes à prendre.

**La mise à jour.** Dans le dossier `zammad-docker-compose` :

```bash
git pull
docker compose pull
docker compose up -d
```

Zammad gère ses propres migrations de base de données au redémarrage. Sauvegarde quand même tes volumes avant une montée de version majeure.

**La surveillance des logs.** Avec sept conteneurs qui tournent, enchaîner les `docker compose logs -f` service par service devient vite pénible. Chez moi, j'utilise [Dozzle](/dozzle-docker-visionneuse-logs-web/) pour avoir tous les logs de la stack en temps réel dans une interface web, sans ouvrir un terminal SSH à chaque fois qu'un agent se plaint que « ça bug ».

**La gestion de la stack.** Si ce serveur héberge d'autres services Docker Compose à côté de Zammad, un outil comme [Dockge](/dockge-docker-gestionnaire-stacks-compose/) te permet de redémarrer, mettre à jour et surveiller plusieurs stacks depuis une interface unique, plutôt que de naviguer entre dix dossiers en SSH.

Sur une stack Zammad Docker, le problème le plus fréquent reste Elasticsearch qui refuse de démarrer après un redémarrage serveur, à cause du `vm.max_map_count` qui retombe à sa valeur par défaut. Si tu as oublié de le persister dans `/etc/sysctl.conf` comme indiqué plus haut, c'est la première chose à vérifier avec `docker compose logs elasticsearch`.

Deuxième souci classique : les emails qui n'arrivent pas dans Zammad. Vérifie d'abord que le compte IMAP configuré n'a pas son mot de passe expiré ou une authentification à deux facteurs qui bloque la connexion applicative. Les fournisseurs de messagerie grand public demandent souvent un mot de passe d'application dédié plutôt que ton mot de passe habituel.

## FAQ

**Zammad Docker en self-hosted est-il vraiment gratuit ?**
Oui. Le logiciel est publié sous licence AGPLv3 par Zammad GmbH, sans frais de licence en auto-hébergement. Seuls les contrats de support, à partir de 2 999 euros par an, sont payants et restent optionnels.

**Combien de RAM faut-il pour faire tourner Zammad en Docker ?**
La documentation officielle recommande au moins 4 Go de RAM pour les conteneurs. Avec Elasticsearch actif pour la recherche plein texte, prévois une marge supplémentaire plutôt que de viser le strict minimum.

**Zammad peut-il remplacer GLPI pour gérer mon parc informatique ?**
Non, pas directement. Zammad est un helpdesk multicanal centré sur le ticketing et la relation client, sans module d'inventaire matériel. GLPI reste la référence si tu dois suivre ton parc en plus du support.

## Conclusion

Zammad Docker résout un problème précis : arrêter de jongler entre cinq boîtes mail et un chat pour retrouver une conversation client. Deux commandes officielles suffisent pour avoir la stack complète qui tourne, et le logiciel reste gratuit tant que tu restes en auto-hébergement.

La partie qui prend du temps, c'est la configuration des canaux et l'adoption par ton équipe, pas l'installation. Branche d'abord l'email, fais tourner ça une semaine, puis ajoute le chat et les réseaux sociaux un par un. Tu éviteras de noyer tes agents sous cinq nouveaux flux le même jour.
