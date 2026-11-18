---
title: "Komodo Docker : piloter tes conteneurs sur plusieurs serveurs depuis une seule interface"
description: "Komodo Docker : une alternative open source à Portainer pour piloter conteneurs et stacks sur plusieurs serveurs depuis un seul tableau de bord."
pubDatetime: "2026-11-15T11:01:44+01:00"
modDatetime: "2026-11-14T08:00:00.000Z"
author: Brandon
tags:
  - docker
  - monitoring
  - automation
  - dashboard
  - intermediaire
featured: false
draft: false
focusKeyword: komodo docker
faqs:
  - question: "Komodo Docker est-il vraiment gratuit ?"
    answer: "Oui. Komodo est open source sous licence GPL-3.0, sans limite au nombre de serveurs connectés. L'éditeur, Mogh Technologies, propose juste un lien de don, pas d'offre payante séparée."
  - question: "Komodo fonctionne-t-il avec Podman ou seulement avec Docker ?"
    answer: "Les deux. L'agent Periphery sait piloter un moteur Podman en plus de Docker, pratique si tu migres progressivement un serveur vers des conteneurs rootless."
  - question: "Que se passe-t-il si un serveur perd la connexion avec Core ?"
    answer: "Les conteneurs continuent de tourner normalement sur ce serveur, Periphery étant autonome. Core affiche juste le serveur en statut inaccessible jusqu'au rétablissement de la connexion."
---
> 💡 **TL;DR**
> - Komodo Docker te donne un tableau de bord unique pour piloter conteneurs, stacks et builds sur tous tes serveurs, sans ouvrir dix sessions SSH
> - Architecture en deux parties : Core (le serveur web central) et Periphery (un petit agent installé sur chaque machine à gérer)
> - Open source sous licence GPL-3.0, installation en Docker Compose, agent Periphery déployé en une commande sur chaque nœud distant

## Table des matières

## Qu'est-ce que Komodo Docker et pourquoi il change la gestion multi-serveurs

Tu as commencé avec un serveur Docker. Puis un deuxième pour isoler tes services exposés sur Internet. Puis un troisième parce que ton NAS fait aussi tourner deux ou trois conteneurs. Résultat : trois terminaux ouverts, trois historiques de commandes à retenir, et cette sensation désagréable de ne jamais savoir d'un coup d'œil ce qui tourne où. Chez moi, ça a duré six mois avant que je craque.

Komodo Docker répond exactement à ce problème. C'est un outil de gestion, de build et de déploiement qui se connecte à tous tes serveurs Docker (et Swarm, et Podman) depuis une seule interface web. Tu vois l'état de chaque conteneur, tu consultes les logs, tu ouvres un shell dans n'importe quelle machine, et tu déploies des stacks Compose sans jamais changer de fenêtre de terminal.

Le projet est maintenu par Mogh Technologies, le code est public sur GitHub sous licence GPL-3.0, et la dernière version majeure (v2.0.0, sortie en mars 2026) a ajouté le support natif de Docker Swarm, l'authentification par paires de clés et un système de clés d'onboarding pour connecter un nouveau serveur en quelques secondes. Ce n'est pas un side-project qui dort depuis deux ans : les releases suivent un rythme régulier.

Ce que Komodo Docker fait concrètement :

- **Supervision centralisée** : CPU, RAM, disque de chaque serveur, avec alertes configurables
- **Gestion de conteneurs et stacks** : définis dans l'interface, sur le disque de l'hôte, ou directement dans un dépôt git avec redéploiement automatique au push
- **Clusters Docker Swarm** : nœuds, services, configs et secrets, gérés depuis le même endroit que tes hôtes Docker classiques
- **Builds d'images** : à partir d'un Dockerfile ou d'un repo git, avec option d'utiliser des instances spot AWS EC2 pour les builds lourds
- **Procédures automatisées** : des séquences d'actions multi-étapes planifiables, utile pour chaîner un déploiement, un test de santé et une notification
- **Variables et secrets partagés** entre tes stacks, avec interpolation, et un journal d'audit complet de qui a fait quoi

## Komodo vs Portainer : lequel choisir pour ton homelab

La question revient tout le temps dès que tu gères plus de deux serveurs. Portainer reste excellent, j'en ai parlé en détail dans mon guide sur [Portainer Docker](/portainer-docker-interface-web-conteneurs/), mais sa gestion multi-hôtes vit historiquement derrière des agents et une édition payante pour le contrôle d'accès avancé.

| Critère | Komodo | Portainer CE/BE |
|---|---|---|
| Multi-serveurs natif | Oui, pensé pour ça dès le départ | Oui via agents, RBAC avancé en payant |
| Déploiement depuis git | Oui, stacks et builds synchronisés | Limité côté CE |
| Docker Swarm | Géré nativement en v2 | Support partiel |
| Licence | GPL-3.0, tout gratuit | CE gratuit, BE payant par nœud |
| Procédures automatisées | Intégrées (actions multi-étapes) | Absent en CE |

Si tu gères un seul serveur avec juste quelques stacks Compose à éditer de temps en temps, inutile de sortir l'artillerie : [Dockge Docker : gérer tes stacks Compose depuis une interface web](/dockge-docker-gestionnaire-stacks-compose/) fait le travail avec une interface plus légère. Komodo Docker devient pertinent au moment où tu dépasses deux ou trois serveurs et que tu veux un vrai inventaire centralisé plutôt qu'une collection d'onglets de navigateur.

## Architecture Core et Periphery : comment ça communique

Komodo Docker repose sur deux composants distincts, et comprendre cette séparation évite pas mal de confusion au moment de l'installation.

**Core** est le serveur central. Il héberge la base de données, l'API REST et WebSocket, et l'interface web par laquelle tu passes pour tout piloter. Tu n'installes Core qu'une seule fois, sur le serveur qui te sert de point d'entrée.

**Periphery** est un agent léger et sans état qui tourne sur chaque machine que tu veux superviser, y compris sur le serveur de Core lui-même si tu veux aussi gérer ses propres conteneurs. Periphery exécute les actions demandées par Core, lit les métriques système et remonte les logs des conteneurs locaux. Il ne stocke rien de durable : toute la configuration vit côté Core.

La communication se fait en WebSocket, authentifiée par paires de clés générées automatiquement depuis la v2.0.0 (les anciennes passkeys manuelles sont dépréciées). Depuis cette version, Periphery peut aussi initier lui-même la connexion sortante vers Core, pratique si le serveur distant est derrière un NAT strict et que tu ne veux pas ouvrir de port entrant dessus.

⚠️ Point de compatibilité à vérifier avant de te lancer : les binaires v2 sont compilés sur Debian Bookworm avec OpenSSL v3. Si un de tes serveurs tourne encore sur Debian Bullseye ou Ubuntu 20.04, Periphery peut refuser de démarrer tant que tu n'as pas mis à jour la distribution.

## Installer Komodo Core avec Docker Compose

Komodo Docker a besoin d'une base de données : MongoDB (recommandé) ou FerretDB avec Postgres si ton système ne supporte pas les dernières versions de MongoDB. On part sur MongoDB, c'est le chemin documenté par défaut.

Crée un dossier dédié et récupère les fichiers officiels :

```bash
mkdir -p ~/komodo && cd ~/komodo
curl -O https://raw.githubusercontent.com/moghtech/komodo/main/compose/mongo.compose.yaml
curl -O https://raw.githubusercontent.com/moghtech/komodo/main/compose/compose.env
```

Le fichier `compose.env` contient les variables à adapter avant de démarrer quoi que ce soit :

```bash
KOMODO_DATABASE_USERNAME=admin
KOMODO_DATABASE_PASSWORD=change-moi
KOMODO_INIT_ADMIN_PASSWORD=change-moi-aussi
KOMODO_WEBHOOK_SECRET=une-chaine-aleatoire-longue
KOMODO_JWT_SECRET=une-autre-chaine-aleatoire
KOMODO_HOST=https://komodo.tondomaine.com
```

Les trois secrets (`KOMODO_DATABASE_PASSWORD`, `KOMODO_WEBHOOK_SECRET`, `KOMODO_JWT_SECRET`) acceptent aussi une variante `_FILE` si tu préfères passer par des secrets Docker plutôt que du texte en clair dans l'environnement. `KOMODO_HOST` sert à générer les URLs de webhook et de redirection OAuth, mets l'adresse réelle que tu vas utiliser.

Démarre la stack :

```bash
docker compose -p komodo -f mongo.compose.yaml --env-file compose.env up -d
```

Ce fichier déploie trois services : `mongo` pour la base de données, `core` (image `ghcr.io/moghtech/komodo-core`) qui expose le port **9120**, et un `periphery` local pour superviser le serveur de Core lui-même. Les volumes `mongo-data`, `mongo-config` et `keys` conservent tes données et les clés d'authentification entre deux redémarrages.

Ouvre `http://ton-serveur:9120`, crée ton compte administrateur avec le mot de passe défini dans `KOMODO_INIT_ADMIN_PASSWORD`, et tu es dans le tableau de bord.

✅ Mets Komodo Docker derrière un reverse proxy en HTTPS avant tout usage régulier. J'utilise [Caddy](https://caddyserver.com) chez moi pour ça, exactement comme je le détaille dans mon guide Portainer, et la logique est identique ici.

## Connecter tes serveurs distants avec l'agent Periphery

C'est l'étape qui donne tout son sens à Komodo Docker : une fois Core en place, tu connectes chacun de tes autres serveurs.

D'abord, crée une clé d'onboarding depuis l'interface de Core (section serveurs, « générer une clé »). Elle ne s'affiche qu'une fois, copie-la immédiatement.

Sur le serveur distant, installe Periphery avec le script officiel, en root :

```bash
curl -sSL https://raw.githubusercontent.com/moghtech/komodo/main/scripts/setup-periphery.py \
  | python3 - \
  --core-address="https://komodo.tondomaine.com" \
  --connect-as="$(hostname)" \
  --onboarding-key="O-ta-cle-ici"
```

Active le démarrage automatique :

```bash
sudo systemctl enable periphery
```

Periphery s'installe par défaut dans `/etc/komodo/periphery.config.toml`. Pour que Core puisse le joindre, il faut qu'une des deux conditions soit vraie : soit Periphery initie la connexion sortante vers l'adresse de Core que tu as passée en paramètre, soit Core arrive à joindre Periphery sur le port **8120** par défaut. Dans les deux cas, pas de gestion manuelle de clés après la première connexion : Periphery génère sa propre paire et n'envoie que la clé publique à Core.

Vérifie dans l'interface que le nouveau serveur passe au statut **OK**. Si ça reste bloqué sur « Unreachable », regarde d'abord le firewall entre les deux machines, c'est la cause numéro un.

⚠️ L'utilisateur qui lance Periphery doit pouvoir utiliser Docker sans `sudo` (appartenance au groupe `docker`), sinon l'agent remonte des erreurs de permission dès qu'il essaie de lister les conteneurs.

## Déployer et piloter tes stacks multi-serveurs

Une fois deux ou trois serveurs connectés, la vraie valeur de Komodo Docker apparaît. Depuis **Stacks**, tu crées une stack, tu choisis le serveur cible, tu colles ou tu lies un `docker-compose.yml` depuis un dépôt git, et tu déploies. L'avantage du git : chaque `push` peut redéclencher automatiquement le déploiement via webhook, sans que tu aies besoin de retourner dans l'interface.

Chez moi, Komodo pilote en parallèle [Paperless-ngx : votre bureau numérique auto-hébergé avec OCR](/paperless-ngx-docker-guide-auto-hebergement/) sur un serveur dédié au stockage, et [Redis Docker : déployer une base de données clé-valeur ultra-rapide](/redis-docker-base-donnees-cle-valeur/) sur une petite machine à part pour le cache, sans jongler entre deux sessions SSH différentes. J'y ai aussi mis [Vikunja Docker : gestionnaire de tâches auto-hébergé (alternative Todoist)](/vikunja-docker-gestionnaire-taches/) sur un troisième nœud, histoire de tester la limite du nombre de serveurs gérables en parallèle. Spoiler : ça tient très bien, l'interface reste fluide même avec une dizaine de stacks réparties sur plusieurs machines.

Chaque conteneur reste consultable individuellement : logs en direct, stats CPU/RAM, et un bouton shell qui ouvre un terminal dans le conteneur sans passer par `docker exec`. Si tu ne veux qu'une vue dédiée aux logs sans tout l'écosystème multi-serveurs, [Dozzle Docker : visionneuse de logs Docker en temps réel via web](/dozzle-docker-visionneuse-logs-web/) reste plus simple à déployer seul sur une machine unique.

Les **procédures** méritent un détour. C'est une fonctionnalité qu'on ne trouve pas dans Portainer CE : tu chaînes plusieurs actions (redéployer une stack, attendre que le healthcheck passe, envoyer une notification) dans une séquence réutilisable, planifiable par cron. Utile pour des mises à jour nocturnes automatisées sur plusieurs serveurs d'un coup, sans script bash maison à maintenir.

## Sécuriser ton installation et dépanner les problèmes courants

Komodo Docker a un accès direct au socket Docker de chaque serveur connecté, ce qui équivaut à un accès root sur ces machines. Traite l'accès à Core avec le même sérieux qu'un accès SSH root : mot de passe fort, HTTPS systématique, pas d'exposition directe du port 9120 sur Internet.

Depuis la v2.0.0, Komodo Docker intègre la 2FA (passkeys et TOTP) pour les comptes locaux, et sait lier un même compte à plusieurs fournisseurs (local, GitHub, Google, OIDC générique). Active-la dès la création du compte admin, ça prend trente secondes et ça change beaucoup en cas de mot de passe compromis.

**Core ne démarre pas** : vérifie les logs du conteneur et que MongoDB répond bien avant Core.

```bash
docker compose -p komodo logs core
```

**Un serveur reste « Unreachable »** : confirme que le port 8120 (ou l'adresse de Core configurée côté Periphery) n'est pas bloqué par un firewall entre les deux machines, et que le service tourne.

```bash
sudo systemctl status periphery
```

**Periphery refuse de démarrer après une mise à jour vers la v2** : regarde la version d'OpenSSL de ta distribution. Un Debian Bullseye ou un Ubuntu 20.04 encore en place est la cause la plus fréquente, la mise à jour du système règle le problème.

Sauvegarde le volume `mongo-data` avec la même rigueur que n'importe quelle base critique : toute la configuration de tes serveurs, stacks et utilisateurs y vit. Une stack [Listmonk Docker : newsletters auto-hébergées (alternative Mailchimp)](/listmonk-docker-newsletter-auto-hebergee/) perdue se recrée en dix minutes, un Komodo Core perdu sans sauvegarde te fait retaper la configuration de chaque serveur à la main.

💡 À lire aussi : [DIUN Docker : être alerté quand une image change sur le registre](/diun-docker-notification-image-registry/), dans la même veine que cet article.

## Conclusion

Komodo Docker ne réinvente pas la gestion de conteneurs, il répare le vrai problème : celui d'avoir trois, quatre, dix serveurs Docker et aucune vue d'ensemble cohérente. L'architecture Core/Periphery est simple à comprendre, l'installation tient en deux commandes par serveur, et le fait que tout soit gratuit et open source sous GPL-3.0 enlève une friction que Portainer impose dès que tu veux du contrôle d'accès avancé.

Si tu es encore sur un seul serveur, Dockge ou Portainer CE suffisent largement, pas besoin de complexifier pour rien. Mais au moment où tu ajoutes ce deuxième ou troisième serveur et que tu sens déjà la lassitude des sessions SSH qui s'accumulent, c'est le bon moment pour installer Komodo Core et connecter tes machines une par une avec l'agent Periphery. Dix minutes par serveur, et plus jamais besoin de te demander lequel tourne quoi.
