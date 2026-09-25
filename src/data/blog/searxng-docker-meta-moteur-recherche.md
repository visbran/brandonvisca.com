---
title: "SearXNG Docker : méta-moteur de recherche auto-hébergé et personnalisable"
description: "SearXNG Docker en pratique : installation en 10 minutes, configuration des moteurs, sécurisation, et comparatif honnête face à Whoogle et Google."
pubDatetime: "2026-09-25T11:02:11+02:00"
modDatetime: "2026-09-24T08:00:00.000Z"
author: Brandon
tags:
  - auto-hebergement
  - docker
  - guide
  - intermediaire
featured: false
draft: false
focusKeyword: searxng docker
faqs:
  - question: "SearXNG Docker consomme combien de ressources sur un homelab ?"
    answer: "Compte 150 a 300 Mo de RAM pour le conteneur principal au repos, un peu plus si plusieurs personnes cherchent en meme temps. Ca tient largement sur un Raspberry Pi 4 ou une petite VM avec 1 vCPU."
  - question: "Faut-il un nom de domaine pour utiliser SearXNG Docker ?"
    answer: "Non, une utilisation locale sur ton reseau via l'IP et le port 8080 suffit. Le nom de domaine devient utile si tu veux acceder a ton instance depuis ton telephone en dehors de chez toi."
  - question: "SearXNG Docker peut-il remplacer Google au quotidien pour toute la famille ?"
    answer: "Oui pour l'essentiel des recherches generales, images et actualites. Prevois quand meme de garder un moteur classique sous la main pour les recherches tres locales ou les resultats Google Shopping, que SearXNG n'agrege pas aussi bien."
---
> 💡 **TL;DR**
> - SearXNG Docker agrège les résultats de dizaines de moteurs (Google, Bing, DuckDuckGo, Brave, Wikipedia...) sans jamais transmettre ta requête ni ton IP à ces services en ton nom propre
> - Installation officielle en Docker Compose en une dizaine de minutes, configuration des moteurs et du thème depuis l'interface web
> - Contrairement à Whoogle, désormais mort, SearXNG ne dépend d'aucun moteur unique : tu coupes une source qui bloque, les autres continuent de fonctionner

## SearXNG Docker : le méta-moteur qui te sort vraiment de Google

Tu en as marre que chaque recherche parte direct chez Google, avec le profilage publicitaire qui va derrière ? SearXNG Docker règle le problème d'une manière plus solide que la plupart des alternatives « privacy » : au lieu de proxyfier un seul moteur, il interroge plusieurs dizaines de sources en parallèle et te renvoie une page de résultats unifiée, sans jamais révéler ton identité à aucune d'entre elles.

Chez moi, SearXNG tourne depuis des mois sur une petite VM du homelab, réglé comme moteur par défaut sur tous mes appareils. Zéro pub, zéro tracking, et surtout zéro dépendance à un seul acteur qui pourrait décider du jour au lendemain de te fermer la porte.

## Table des matières

## SearXNG Docker : qu'est-ce qu'un méta-moteur de recherche

SearXNG est un projet open source né en 2021, fork du projet Searx original. Il agrège les résultats d'une longue liste de moteurs (Google, Bing, DuckDuckGo, Brave, Qwant, StartPage, Wikipedia, et bien d'autres selon les catégories activées) sans jamais faire remonter ta requête directement chez eux avec ton adresse IP réelle. C'est l'instance SearXNG qui fait écran, elle interroge les moteurs en son nom, récupère les résultats, les fusionne, et te les présente.

La différence avec un moteur « privé » classique comme DuckDuckGo, c'est que tu n'as pas à faire confiance à un seul acteur pour ta vie privée. Le code tourne chez toi, la config est entièrement entre tes mains, et le projet est publié sous licence AGPL-3.0 avec des contributions régulières de la communauté.

Concrètement, ça change quoi pour toi :

- **Aucun profilage publicitaire** : pas de compte, pas de cookie de tracking transmis aux moteurs sous-jacents
- **Pas de dépendance à un seul point de défaillance** : si un moteur bloque l'accès demain, tu le désactives et les autres continuent
- **Résultats agrégés et dédoublonnés** : SearXNG fusionne les réponses de plusieurs sources et retire les doublons
- **Personnalisation totale** : catégories, langues, thème, moteurs actifs, tout se règle depuis l'interface

## Installer SearXNG Docker avec Docker Compose

L'installation officielle passe par Docker Compose, avec les fichiers publiés directement sur le dépôt GitHub du projet. Crée un dossier dédié :

```bash
mkdir -p ~/docker/searxng && cd ~/docker/searxng
```

Récupère les fichiers officiels :

```bash
curl -fsSL \
  -O https://raw.githubusercontent.com/searxng/searxng/master/container/docker-compose.yml \
  -O https://raw.githubusercontent.com/searxng/searxng/master/container/.env.example
cp .env.example .env
```

Ouvre le fichier `.env` et renseigne au minimum le nom d'hôte et la clé de session :

```bash
SEARXNG_HOSTNAME=recherche.tondomaine.fr
SEARXNG_SECRET=$(openssl rand -hex 32)
```

Le `SEARXNG_SECRET` sert à signer les sessions internes. Génère une vraie valeur aléatoire avec `openssl` plutôt que de laisser tourner la valeur par défaut du fichier d'exemple, c'est le genre de détail qu'on oublie et qui traîne des mois sur une instance exposée.

Lance ensuite le tout :

```bash
docker compose up -d
```

Vérifie que ça tourne avec les logs :

```bash
docker compose logs -f core
```

Ouvre `http://IP_DE_TON_SERVEUR:8080` dans ton navigateur. Tu arrives directement sur l'interface de recherche, sobre et rapide. Pas d'installation de base de données à part, pas de dépendance externe compliquée : le conteneur embarque tout ce qu'il faut.

## Configurer les moteurs, les catégories et le thème SearXNG Docker

Une fois l'instance lancée, va dans **Préférences** en haut de l'interface. Chaque moteur se coche ou se décoche individuellement, classé par catégorie (général, images, cartes, vidéos, IT, science, réseaux sociaux).

Pour un usage quotidien réactif, garde quatre à cinq sources généralistes plutôt que de tout activer. Plus tu ajoutes de moteurs, plus SearXNG doit attendre la réponse la plus lente pour afficher une page complète.

⚠️ Un moteur qui traîne systématiquement ralentit toutes tes recherches. Si tu remarques une lenteur, désactive les moteurs les plus capricieux un par un pour identifier le coupable.

Dans l'onglet **General**, tu peux forcer le HTTPS sur les liens de résultats et activer le mode sécurisé pour filtrer le contenu explicite, pratique si l'instance est partagée en famille. Le thème s'ajuste aussi ici : plusieurs variantes claires et sombres sont proposées nativement.

## Sécuriser une instance SearXNG Docker exposée sur Internet

Si tu comptes utiliser SearXNG comme moteur par défaut depuis ton téléphone en dehors de ton réseau local, tu vas forcément l'exposer derrière un nom de domaine et un reverse proxy. Un moteur de recherche ouvert publiquement attire vite des bots qui testent des injections ou tentent du brute-force sur l'admin, donc deux réflexes s'imposent.

Le premier, place une couche d'authentification devant l'interface si tu ne veux pas la rendre accessible à n'importe qui qui tombe sur l'URL. [Authelia Docker : authentification double facteur centralisée pour ton homelab](/authelia-docker-authentification-2fa-homelab/) se branche facilement devant n'importe quel service derrière un reverse proxy, et ça évite qu'une instance oubliée devienne un relais anonyme pour n'importe qui.

Le second, protège le port exposé contre les tentatives répétées de connexion ou de scan automatisé. [Fail2Ban Docker : bloquer les attaques brute-force automatiquement](/fail2ban-docker-securite-serveur/) fait exactement ça à partir des logs de ton reverse proxy, sans configuration lourde.

✅ Avec ces deux briques en place, tu passes d'un service exposé à l'arrache à une vraie stack protégée correctement.

## SearXNG Docker vs Whoogle vs Google : lequel choisir en 2026

La comparaison revient souvent parce que Whoogle occupait le même créneau : un moteur auto-hébergé, sans pub, sans compte. Sauf que Whoogle reposait entièrement sur un seul principe fragile, interroger Google sans JavaScript, et ce mode d'accès est aujourd'hui bloqué. Le dépôt a été archivé, et le conteneur qui démarre encore ne renvoie plus de résultats fiables.

SearXNG évite ce piège par construction. Il n'a jamais dépendu d'un seul moteur, donc quand une source durcit ses conditions d'accès, tu perds une entrée dans la liste, pas le service entier. C'est la différence entre une architecture avec un point de défaillance unique et une architecture agrégée.

| Critère | SearXNG Docker | Whoogle | Google directement |
|---|---|---|---|
| Auto-hébergé | Oui | Oui (mais mort) | Non |
| Tracking | Aucun | Aucun (en théorie) | Profilage publicitaire complet |
| Dépendance à un seul moteur | Non, dizaines de sources | Oui, Google uniquement | N/A |
| Maintenance active | Oui, releases régulières | Non, dépôt archivé | N/A |
| Résultats fiables en 2026 | Oui | Non | Oui |

Le verdict est net : si tu cherchais Whoogle, cherche SearXNG à la place. Même philosophie, fondation technique bien plus solide.

## Dépannage courant sur SearXNG Docker

**La page reste blanche après le démarrage du conteneur.** Vérifie que `SEARXNG_HOSTNAME` correspond exactement au nom de domaine ou à l'IP utilisée pour accéder au service. Une valeur incohérente casse la génération des liens internes de l'interface.

**Les résultats mettent plusieurs secondes à s'afficher.** Normal dans une certaine mesure : SearXNG interroge plusieurs moteurs en parallèle et attend les réponses les plus lentes. Réduis le nombre de moteurs actifs si le délai devient gênant.

**Un moteur précis renvoie toujours une erreur.** Certains moteurs changent leur structure HTML ou durcissent leurs conditions d'accès de temps en temps. Désactive-le temporairement dans les préférences, le reste de l'agrégation continue de fonctionner normalement.

**Le conteneur redémarre en boucle.** Regarde les logs avec `docker compose logs -f core`, c'est généralement une variable mal formée dans le `.env`, en particulier un `SEARXNG_SECRET` vide ou mal généré.

Une fois l'instance stable, pense aussi au suivi dans le temps. Si tu veux savoir quand un moteur externe change ses conditions d'utilisation ou quand une page que tu surveilles évolue, [Changedetection Docker : guide complet pour surveiller n'importe quel site web (alternative Distill.io)](/changedetection-docker-surveillance-web/) fait ce travail de veille automatiquement, sans que tu aies à revérifier une page à la main chaque semaine.

Pense enfin à sauvegarder ta configuration. Le volume Docker de SearXNG (moteurs activés, thème, préférences par défaut) n'est pas volumineux, mais reconstruire ça à la main après un crash de serveur est chiant. [Duplicati Docker : sauvegarde chiffrée auto-hébergée](/duplicati-docker-sauvegarde/) tourne en tâche de fond et couvre ce volume comme n'importe quel autre.

## Conclusion

SearXNG Docker fait ce que Whoogle promettait sans jamais vraiment tenir la distance : un moteur de recherche chez toi, sans tracking, sans pub, sans compte à créer ailleurs, et surtout sans dépendre d'un seul acteur qui peut te couper l'herbe sous le pied du jour au lendemain.

L'installation prend dix minutes en Docker Compose, la configuration se fait entièrement depuis l'interface, et le projet reste activement maintenu. Si tu veux reprendre la main sur tes recherches sans sacrifier la pertinence des résultats, c'est clairement l'option la plus solide en 2026.

Installe-le ce week-end sur un coin de ton homelab, règle quatre ou cinq moteurs, et remplace ton moteur par défaut. Tu ne reviendras pas en arrière.
