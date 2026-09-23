---
title: "Whoogle Docker : pourquoi le projet est mort et par quoi le remplacer"
description: "Whoogle Docker est abandonné depuis aout 2026, Google bloque ses requetes. Le point complet et la vraie alternative auto-hebergee : SearXNG."
pubDatetime: "2026-09-23T11:01:12+02:00"
modDatetime: "2026-09-22T08:00:00.000Z"
author: Brandon
tags:
  - auto-hebergement
  - docker
  - guide
  - intermediaire
featured: false
draft: false
focusKeyword: whoogle docker
faqs:
  - question: "Pourquoi Whoogle Docker ne fonctionne plus en 2026 ?"
    answer: "Google bloque depuis debut 2025 toutes les requetes de recherche faites sans JavaScript, en bannissant en continu les User-Agent qui fonctionnaient encore. Whoogle reposait entierement sur ce mode de requete, le projet a ete archive le 14 aout 2026."
  - question: "SearXNG consomme combien de ressources sur un homelab ?"
    answer: "Compte environ 150 a 300 Mo de RAM pour le conteneur principal au repos, un peu plus sous charge avec plusieurs utilisateurs simultanes. Ca tourne sans souci sur un Raspberry Pi 4 ou une petite VM avec 1 vCPU."
  - question: "Peut-on encore faire tourner une instance Whoogle deja deployee ?"
    answer: "Techniquement oui, l'image Docker existe toujours et demarre normalement, mais les resultats de recherche eux-memes ne remontent plus de facon fiable puisque Google bloque le mode de requete sur lequel Whoogle s'appuyait."
---
> 💡 **TL;DR**
> - Whoogle Docker est officiellement mort : le depot a ete archive le 14 aout 2026, Google ayant fini de bloquer les requetes sans JavaScript qui faisaient tourner le projet
> - Les mainteneurs eux-memes annoncent l'arret et recommandent de migrer, l'image Docker demarre encore mais ne renvoie plus de resultats fiables
> - La vraie alternative auto-hebergee qui fonctionne encore en 2026, c'est SearXNG : meme philosophie sans tracking, mais appuyee sur des dizaines de moteurs au lieu d'un seul

## Whoogle Docker : le projet que tu voulais installer n'existe plus vraiment

Tu es sans doute arrive ici en cherchant comment monter Whoogle Docker sur ton serveur. Mauvaise nouvelle : c'est trop tard. Le depot GitHub `benbusby/whoogle-search` a ete archive le 14 aout 2026, et ce n'est pas un simple abandon de maintenance, c'est un arret net signe par l'auteur lui-meme.

Je vais pas te faire un tuto qui marche a moitie juste pour cocher la case "article sur Whoogle". Autant te dire tout de suite pourquoi ca ne sert plus a rien, et te montrer ce qui marche vraiment a la place pour avoir un moteur de recherche auto-heberge sans tracking ni pubs.

## Table des matières

## Pourquoi Whoogle Docker a fini par mourir

Le principe de Whoogle etait malin : un conteneur Docker qui interroge Google a ta place, sans JavaScript, sans cookies de tracking, et qui te renvoie une page de resultats nettoyee. Ca a marche pendant des annees. Le probleme, c'est que ce fonctionnement reposait entierement sur un point faible : Google acceptait encore des requetes de recherche sans JavaScript.

Depuis debut 2025, Google a change de politique de facon methodique. Le moteur bannit en continu les chaines User-Agent qui permettaient encore de passer, au fur et a mesure qu'elles etaient decouvertes et partagees. Chez Whoogle, ca donnait une course sans fin : chaque contournement tenait quelques semaines, puis se faisait bloquer a son tour.

Les mainteneurs l'ecrivent noir sur blanc dans l'annonce d'archivage : la partie n'est plus jouable. Interroger Google sans JavaScript, filtrer le tracking, et proxyfier proprement le resultat vers l'utilisateur, c'etait le socle technique du projet. Sans ce socle, il ne reste rien a maintenir.

Concretement, si tu deploies quand meme l'image `benbusby/whoogle-search` aujourd'hui, le conteneur demarre sans probleme, l'interface s'affiche, mais les recherches remontent des pages vides ou des erreurs de blocage. Ce n'est pas un bug ponctuel que tu pourrais patcher en changeant une variable d'environnement, c'est la fondation du projet qui a cede.

## Ce que dit officiellement l'auteur du projet

Ben Busby, le createur de Whoogle, a ete transparent sur la situation. Le message d'archivage precise que le projet reste disponible sous licence MIT pour qui veut forker le code, mais qu'il n'y aura plus ni commit, ni correction de bug, ni revue de pull request. Les instances existantes ne beneficient plus d'aucun support.

Fait notable, l'auteur mentionne meme sa propre solution de repli personnelle : passer sur Kagi, un moteur de recherche payant. C'est un choix honnete de sa part, mais ca ne repond evidemment pas au besoin de base de ceux qui cherchaient Whoogle Docker au depart, a savoir un moteur auto-heberge, gratuit et sans compte a creer chez un tiers.

C'est ce vide-la qu'il faut combler autrement.

## SearXNG : la vraie alternative auto-hebergee en 2026

Si l'objectif etait de sortir de l'ecosysteme Google et de garder la main sur tes recherches, SearXNG fait le job, et il le fait mieux que Whoogle ne l'a jamais fait. Le principe est different : au lieu de proxyfier un seul moteur, SearXNG agrege les resultats de dizaines de sources (Google, Bing, DuckDuckGo, Brave, Wikipedia, et bien d'autres selon ta config) sans jamais transmettre ta requete a un moteur en ton nom propre.

Concretement, ca veut dire deux choses. D'abord, aucune adresse IP ni cookie ne circule directement entre toi et Google ou Bing, SearXNG fait ecran. Ensuite, et c'est le point qui compte le plus vu ce qui vient d'arriver a Whoogle, SearXNG ne depend pas d'un seul point de defaillance. Si un moteur durcit ses conditions d'acces demain, tu desactives juste ce moteur dans la config et tu continues avec les autres.

Le projet est activement maintenu, sous licence AGPL-3.0, avec des releases regulieres. Pas de mauvaise surprise a attendre sur celui-la.

## Installer SearXNG avec Docker Compose

L'installation officielle recommandee passe par Docker Compose. Cree un dossier dedie sur ton serveur :

```bash
mkdir -p ~/docker/searxng && cd ~/docker/searxng
```

Recupere les fichiers officiels directement depuis le depot :

```bash
curl -fsSL \
  -O https://raw.githubusercontent.com/searxng/searxng/master/container/docker-compose.yml \
  -O https://raw.githubusercontent.com/searxng/searxng/master/container/.env.example
cp .env.example .env
```

Ouvre le fichier `.env` et renseigne au minimum deux variables :

```bash
SEARXNG_HOSTNAME=recherche.tondomaine.fr
SEARXNG_SECRET=$(openssl rand -hex 32)
```

Le `SEARXNG_SECRET` sert a signer les sessions internes, genere une valeur unique avec la commande `openssl` ci-dessus plutot que de laisser une valeur par defaut trainer dans ta config.

Lance ensuite le tout :

```bash
docker compose up -d
```

Compte quelques secondes pour que le conteneur demarre, puis ouvre `http://IP_DE_TON_SERVEUR:8080` dans ton navigateur. Tu tombes directement sur l'interface de recherche, sobre, rapide, sans pub.

## Exposer SearXNG sur Internet sans te faire scanner en boucle

Si tu comptes utiliser SearXNG comme moteur par defaut sur tous tes appareils, tu vas forcement l'exposer derriere un nom de domaine et un reverse proxy. C'est le moment de penser securite, parce qu'un moteur de recherche ouvert publiquement attire vite des bots qui testent des injections ou tentent du brute-force sur l'admin.

Deux reflexes a avoir ici. Le premier, place une couche d'authentification devant l'interface si tu ne veux pas la rendre publique a tout le monde. J'ai deja detaille la mise en place avec [Authelia Docker : authentification double facteur centralisee pour ton homelab](/authelia-docker-authentification-2fa-homelab/), qui se branche facilement devant n'importe quel service expose derriere un reverse proxy.

Le second reflexe, protege le port expose contre les tentatives repetees de connexion ou de scan automatise. [Fail2Ban Docker : bloquer les attaques brute-force automatiquement](/fail2ban-docker-securite-serveur/) fait exactement ca a partir des logs de ton reverse proxy, sans configuration lourde.

Ces deux briques combinees, tu passes d'un service expose a l'arrache a une vraie stack auto-hebergee protegee correctement.

## Configurer les moteurs et le mode de confidentialite

Une fois SearXNG lance, va dans **Preferences** en haut de l'interface. Tu peux activer ou desactiver chaque moteur de recherche individuellement : Google, Bing, DuckDuckGo, Brave, Qwant, Wikipedia, StartPage, et une bonne trentaine d'autres selon les categories (general, images, cartes, videos, IT, science).

Pour un usage quotidien equilibre, garde actives quatre a cinq sources generalistes plutot que de toutes les cocher. Plus tu ajoutes de moteurs, plus une recherche prend de temps a agreger les reponses.

Dans l'onglet **General**, tu peux aussi forcer le mode HTTPS uniquement pour les liens de resultats, et activer le mode securise pour filtrer le contenu explicite si l'instance est partagee en famille.

## Sauvegarder ta configuration

Ta configuration SearXNG (moteurs actives, theme, preferences par defaut) vit dans le dossier monte par le volume Docker. Ce n'est pas une base critique en taille, mais c'est chiant a reconstruire a la main si ton serveur crashe. Si tu as deja une routine de sauvegarde pour ton homelab, ajoute simplement ce volume dedans. Sinon, [Duplicati Docker : sauvegarde chiffree auto-hebergee](/duplicati-docker-sauvegarde/) fait tourner une sauvegarde chiffree planifiee sans effort supplementaire une fois configure.

## Depannage courant

**La page reste blanche apres le demarrage du conteneur.** Verifie que `SEARXNG_HOSTNAME` correspond bien au nom de domaine ou a l'IP que tu utilises pour acceder au service, une valeur incoherente casse la generation des liens internes de l'interface.

**Les resultats mettent plusieurs secondes a s'afficher.** Normal dans une certaine mesure, SearXNG interroge plusieurs moteurs en parallele et attend les reponses les plus lentes. Reduis le nombre de moteurs actifs si le delai te derange vraiment.

**Un moteur precis renvoie toujours une erreur.** Certains moteurs changent leur structure HTML ou durcissent leurs conditions d'acces de temps en temps, exactement le probleme qui a tue Whoogle mais applique ici a une seule source parmi beaucoup. Desactive temporairement ce moteur dans les preferences, le reste de l'agregation continue de fonctionner normalement.

**Le conteneur redemarre en boucle.** Regarde les logs avec `docker compose logs -f searxng`, c'est generalement une variable d'environnement mal formee dans le `.env`, en particulier un `SEARXNG_SECRET` vide ou avec des caracteres non echappes.

## Conclusion

Whoogle Docker a eu son heure de gloire, mais l'histoire est terminee : le projet est archive, la fondation technique sur laquelle il reposait a cede face aux blocages de Google, et il n'y aura pas de nouvelle version pour corriger ca. Continuer a le deployer en 2026, c'est installer une coquille vide.

SearXNG reprend le flambeau avec une approche plus solide, moins dependante d'un seul acteur, et toujours activement maintenue. L'installation prend dix minutes, la configuration se fait depuis l'interface, et tu gardes exactement ce que tu cherchais au depart avec Whoogle : un moteur de recherche chez toi, sans tracking, sans pub, sans compte a creer ailleurs.
