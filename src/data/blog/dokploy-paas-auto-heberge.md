---
title: "Dokploy Docker : ton PaaS auto-hébergé (alternative Vercel)"
description: "Dokploy Docker : installe un PaaS auto-hébergé gratuit pour déployer apps et bases de données comme sur Vercel, sans la facture mensuelle."
pubDatetime: "2026-10-24T11:01:11+02:00"
modDatetime: "2026-10-23T08:00:00.000Z"
author: Brandon
tags:
  - docker
  - reverse-proxy
  - ci-cd
  - monitoring
  - intermediaire
featured: false
draft: false
focusKeyword: dokploy docker
faqs:
  - question: "Dokploy tourne avec combien de RAM minimum ?"
    answer: "Ça dépend surtout de ce que tu déploies dessus, mais compte large dès le départ : un petit VPS à 1 Go suffit pour tester, deux à quatre Go te mettent à l'aise pour plusieurs apps en prod."
  - question: "Et si le serveur qui héberge Dokploy tombe en panne ?"
    answer: "Tes apps tombent avec lui, comme sur tout VPS unique. C'est pour ça que Dokploy propose le déploiement multi-serveurs : tu gardes la gestion centralisée mais tu répartis la charge réelle."
  - question: "Dokploy est-il vraiment gratuit ou y a-t-il une version payante ?"
    answer: "Le logiciel en lui-même est open source et gratuit, tu l'auto-héberges sur ton serveur. Dokploy propose en plus une offre cloud managée payante si tu préfères ne pas gérer le VPS toi-même."
---
> 💡 **TL;DR**
> - Dokploy est un PaaS open source et auto-hébergé : tu déploies des apps et des bases de données sur ton propre serveur avec une interface web qui gère Docker, Traefik et les certificats SSL pour toi
> - Installation en une commande (`curl -sSL https://dokploy.com/install.sh | sh`), déploiement depuis Git, Dockerfile ou Compose, templates prêts à l'emploi pour une trentaine d'apps populaires
> - Gratuit et open source tant que tu l'héberges toi-même, multi-serveurs, monitoring CPU/RAM intégré, mais un seul point de défaillance si tu ne répartis pas sur plusieurs machines

## Dokploy Docker : ton PaaS qui remplace Vercel sur ton propre serveur

T'as un abonnement Vercel, Netlify ou Heroku qui grossit chaque mois alors que tes apps tournent à peine ? Chez moi, la question s'est posée pareil : je paie pour de la simplicité, pas pour des serveurs qui tournent 24/7 à 2% de charge. Entre nous, un VPS à 10€/mois fait le même boulot si on lui donne la bonne couche logicielle par-dessus.

C'est exactement le rôle de **Dokploy**. C'est un PaaS, une plateforme qui gère le déploiement de tes applications à ta place, sauf qu'ici c'est toi qui héberges la plateforme. Tu gardes l'expérience "push et ça déploie" sans donner ta carte bancaire à un tiers qui facture à la seconde de build.

## Table des matières

## Pourquoi passer à Dokploy Docker plutôt qu'à Vercel ou Heroku

Dokploy Docker repose sur une idée simple : tout ce que Vercel ou Heroku font en coulisses (build, conteneurisation, reverse proxy, certificats, logs) est en réalité construit avec des briques open source que tu peux faire tourner toi-même. Docker pour l'exécution, Traefik pour le routage HTTPS, et une interface web qui orchestre tout ça sans que tu touches à un `docker-compose.yml` à la main.

La différence avec un simple VPS nu, c'est que Dokploy Docker t'évite la partie pénible :

- **Déploiement depuis Git** : tu connectes ton repo GitHub, GitLab ou Bitbucket, chaque push déclenche un build et un déploiement automatique
- **Trois méthodes de build** : Nixpacks (détection automatique du langage, comme Heroku), Buildpacks, ou un Dockerfile si tu veux garder le contrôle total
- **Bases de données managées** : PostgreSQL, MySQL, MariaDB, MongoDB et [Redis](/redis-docker-base-donnees-cle-valeur/) en quelques clics, avec sauvegardes programmées
- **Traefik intégré** : HTTPS automatique via Let's Encrypt, domaines personnalisés, sans configurer un seul fichier de certificat
- **Multi-serveurs** : un serveur Dokploy peut piloter le déploiement sur plusieurs machines, utile si tu veux séparer prod et staging

Le vrai argument, c'est le prix. Zéro euro de licence, zéro facturation à l'usage. Tu payes ton VPS, point. Pour un homelab ou une petite boîte qui héberge cinq à dix apps, la différence se compte en centaines d'euros par an.

## Installation : le script qui monte tout en 5 minutes

Avant de lancer quoi que ce soit, prévois un serveur Linux propre, de préférence Ubuntu ou Debian récent, avec un accès root ou sudo. Évite d'installer Dokploy sur une machine qui fait déjà tourner d'autres conteneurs Docker en Swarm mode, l'installeur configure le mode Swarm pour toi et peut entrer en conflit.

Connecte-toi en SSH et lance :

```bash
curl -sSL https://dokploy.com/install.sh | sh
```

Le script installe Docker s'il n'est pas déjà présent, active le mode Swarm, puis déploie la stack Dokploy (l'app elle-même, PostgreSQL pour la base interne, Redis pour les files de tâches). Ça prend deux à trois minutes selon ta connexion.

Une fois le script terminé, tu accèdes à l'interface sur `http://<ip-de-ton-serveur>:3000`. Premier écran, tu crées ton compte admin. C'est le seul compte local : pas de serveur central qui stocke tes identifiants, tout reste chez toi.

> ⚠️ Vérifie avant de lancer le script que les ports 80, 443 et 3000 sont libres. Si tu as déjà un reverse proxy comme Nginx qui écoute sur 80/443, il va falloir soit le désactiver, soit dédier une machine entière à Dokploy. Traefik n'aime pas partager ces ports.

Pour le nom de domaine, pointe un enregistrement A vers l'IP de ton serveur avant de configurer quoi que ce soit dans l'interface. Dokploy Docker demande la résolution DNS à jour pour générer les certificats Let's Encrypt, sinon la demande échoue silencieusement et tu te retrouves à débugger un certificat qui ne sort jamais.

## Premiers pas : déployer ta première app et une base de données

Dans l'interface, tout s'organise par **projets**. Un projet regroupe une ou plusieurs applications qui partagent un contexte : ton blog et sa base PostgreSQL, par exemple.

Pour une première app, le chemin le plus rapide reste de connecter ton compte Git. Dokploy te demande d'autoriser l'accès via OAuth, puis tu choisis le repo et la branche à suivre. À chaque push sur cette branche, un webhook déclenche automatiquement un nouveau build.

Si ton app a déjà un `Dockerfile`, Dokploy le détecte et s'en sert directement. Sinon, Nixpacks tente de deviner le langage (Node, Python, Go, PHP...) et génère l'image à ta place. C'est bluffant pour une app Node standard, moins fiable sur des stacks exotiques où je préfère écrire le Dockerfile moi-même pour garder la main sur les versions.

Pour une base de données, c'est encore plus direct : onglet "Databases", tu choisis le moteur, tu définis le nom et les identifiants, et Dokploy provisionne le conteneur avec un volume persistant. L'app et la base communiquent via le réseau interne Docker, pas besoin d'exposer le port de la base sur internet.

Dokploy propose aussi une bibliothèque de **templates** : des stacks Compose prêtes à déployer pour des outils comme Supabase, Cal.com, PocketBase, Uptime Kuma et une trentaine d'autres projets. Pratique pour tester rapidement un outil sans écrire le moindre fichier de configuration. Si tu héberges déjà une newsletter en interne, le même principe s'applique à [Listmonk](/listmonk-docker-newsletter-auto-hebergee/) : une stack Compose, un domaine, et c'est en ligne.

## Dokploy vs Coolify vs Dockge : lequel choisir

Dokploy n'est pas seul sur ce terrain. Coolify suit une philosophie très proche (PaaS complet, build automatique depuis Git, bases de données managées). Les deux se valent largement en fonctionnalités, la différence tient surtout à l'interface et à la communauté. J'ai basculé entre les deux sur mon homelab, honnêtement le choix se fait à la préférence d'ergonomie plus qu'à un vrai écart technique.

[Dockge](/dockge-docker-gestionnaire-stacks-compose/), en revanche, vise beaucoup plus bas et c'est voulu. C'est un gestionnaire de stacks Compose avec une interface web, pas un PaaS : pas de build automatique depuis Git, pas de gestion de domaines intégrée, pas de pipeline CI/CD. Si tu gères déjà tes déploiements à la main avec des fichiers `docker-compose.yml` et que tu veux juste une interface pour les démarrer/arrêter proprement, Dockge suffit et consomme beaucoup moins de ressources que Dokploy.

La vraie question c'est ton usage réel. Si tu déploies régulièrement du code applicatif (ton propre backend, un SaaS perso, un projet client), Dokploy Docker t'évite des heures de configuration manuelle. Si tu gères juste une dizaine de services tiers déjà packagés en Compose, Dockge fait le travail avec une empreinte beaucoup plus légère.

## Monitoring, logs et limites à connaître

Dokploy embarque un monitoring basique : CPU, RAM et réseau par conteneur, visible directement dans l'interface, sans rien configurer. Pour un œil rapide sur la santé d'un serveur, ça suffit largement.

Pour creuser dans les logs applicatifs en revanche, l'interface native de Dokploy reste sommaire. Chez moi, je branche en complément [Dozzle](/dozzle-docker-visionneuse-logs-web/) sur la même machine : une visionneuse de logs Docker en temps réel, légère, qui complète bien ce que Dokploy ne fait qu'à moitié.

Côté sauvegardes, Dokploy planifie des dumps réguliers de tes bases de données vers un stockage S3-compatible (Backblaze B2, Wasabi, ou ton propre MinIO). Configure-le dès le premier jour, pas après ton premier incident.

✅ Points forts confirmés après plusieurs mois d'usage : l'installation qui tient vraiment sa promesse de simplicité, le déploiement Git qui fonctionne sans surprise, et une communauté active qui pousse des mises à jour régulières.

⚠️ Points de vigilance : le mode Swarm imposé par l'installeur peut surprendre si tu gérais déjà du Docker Compose classique sur la même machine. L'interface change encore assez vite entre versions, certains écrans bougent d'une mise à jour à l'autre. Et sur un serveur unique, Dokploy reste un point de défaillance unique : si la machine tombe, toutes tes apps tombent avec elle, panneau d'administration compris. Le mode multi-serveurs existe justement pour limiter ce risque.

## Conclusion

Dokploy Docker fait ce qu'il promet : retrouver le confort d'un PaaS façon Vercel ou Heroku, sans la facture qui grimpe avec le trafic. L'installation prend cinq minutes, le déploiement depuis Git marche du premier coup, et les templates t'évitent de réécrire des stacks Compose pour les outils les plus courants.

Ce n'est pas magique pour autant : tu restes responsable du serveur qui l'héberge, de ses sauvegardes et de sa disponibilité. Pour un homelab ou une petite structure qui veut arrêter de payer pour du cloud géré, c'est clairement l'une des options les plus solides du moment. Teste-le sur un VPS à quelques euros avant de migrer quoi que ce soit en prod, tu verras vite si ça colle à ton usage.
