---
title: "Ollama + Open WebUI Docker : ton ChatGPT 100 % local"
description: "Ollama et Open WebUI Docker : installe ton ChatGPT privé en local, configure le GPU, sécurise l'accès et choisis tes modèles sans dépendre du cloud."
pubDatetime: "2026-11-09T11:00:35+01:00"
modDatetime: "2026-11-08T08:00:00.000Z"
author: Brandon
tags:
  - docker
  - intermediaire
featured: false
draft: false
focusKeyword: open webui docker
faqs:
  - question: "Ollama et Open WebUI Docker, ça consomme combien de RAM ?"
    answer: "Open WebUI seul tient en quelques centaines de Mo. La vraie consommation vient du modèle chargé par Ollama : compte au moins 4 à 8 Go de RAM libre pour un petit modèle, bien plus pour les gros."
  - question: "Peut-on faire tourner Ollama et Open WebUI Docker sans carte graphique ?"
    answer: "Oui, tout fonctionne sur CPU. Les réponses sont plus lentes, surtout avec de gros modèles, mais les modèles légers restent parfaitement utilisables sans GPU dédié."
  - question: "Mes conversations avec Ollama et Open WebUI Docker sont-elles vraiment privées ?"
    answer: "Oui, tant que tu utilises un modèle local : rien ne quitte ta machine. Seule une connexion volontaire à une API cloud dans les paramètres changerait ça."
---
> 💡 **TL;DR**
> - Ollama fait tourner le modèle, Open WebUI Docker lui colle une interface façon ChatGPT, le tout en local et sans compte cloud.
> - Un seul fichier `docker-compose.yml` suffit pour déployer les deux services ensemble, avec ou sans GPU Nvidia.
> - Rien ne sort de ta machine : aucune clé API, aucun abonnement, tes prompts restent chez toi.

Tu utilises ChatGPT tous les jours mais une partie de toi n'aime pas trop l'idée d'envoyer tes prompts, tes bouts de code et tes questions perso vers un serveur qui ne t'appartient pas. Bonne nouvelle : avec Ollama et Open WebUI Docker, tu montes la même expérience de chat, avec choix du modèle, historique de conversations et interface propre, mais entièrement sur ta machine. Pas de clé API à payer, pas d'abonnement mensuel, pas de données qui partent on ne sait où. On installe les deux, on les connecte, et on lance ton premier modèle.

## Table des matières

## Pourquoi faire tourner son IA en local plutôt que sur ChatGPT

Trois raisons reviennent systématiquement quand on me demande pourquoi s'embêter à monter sa propre IA au lieu d'ouvrir un onglet ChatGPT.

La confidentialité d'abord. Avec un modèle local, tes prompts ne transitent par aucun serveur tiers. Si tu colles du code client, des données médicales ou des documents internes dans une discussion, ça reste sur ton disque. C'est le même réflexe qui te pousse à préférer [FreshRSS](/freshrss-docker-lecteur-rss/) à Google Reader ou [Vikunja](/vikunja-docker-gestionnaire-taches/) à Todoist : reprendre la main sur tes propres données plutôt que les confier à un tiers.

Le coût ensuite. Une fois le matériel acheté, tu ne paies plus par token ni par requête. Un gros usage quotidien d'un modèle local ne fait grimper aucune facture mensuelle, seulement ta note d'électricité.

Le contrôle enfin. Tu choisis ton modèle, tu le changes quand tu veux, tu le fais tourner même sans connexion internet une fois téléchargé. Ollama est distribué sous licence MIT et son code est public sur GitHub, ce qui veut dire que personne ne peut te couper l'accès du jour au lendemain ni changer les conditions d'utilisation en cours de route.

La contrepartie, c'est que tu gères toi-même l'installation, la sécurité et le dimensionnement matériel. C'est justement ce qu'on fait maintenant.

## Installer Ollama en Docker : le moteur qui fait tourner les modèles

Ollama, c'est le moteur d'inférence : le programme qui charge un modèle de langage en mémoire et répond à tes requêtes. Il tourne en arrière-plan et expose une API sur le port 11434, qu'une interface comme Open WebUI Docker vient ensuite consommer.

Pour un déploiement simple sur CPU :

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

Cette commande télécharge l'image officielle `ollama/ollama`, crée un volume nommé `ollama` monté sur `/root/.ollama` pour conserver les modèles téléchargés entre deux redémarrages, et expose l'API sur le port 11434 de ta machine hôte.

Si ton serveur dispose d'une carte Nvidia, active le GPU pour accélérer drastiquement les réponses :

```bash
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

Attention, `--gpus=all` ne fonctionne que si le NVIDIA Container Toolkit est déjà installé sur l'hôte. Sans lui, Docker ne voit tout simplement pas ta carte graphique et la commande échoue.

Une fois le container lancé, vérifie que l'API répond :

```bash
curl http://localhost:11434
```

Tu devrais voir un message du type « Ollama is running ». À ce stade, Ollama tourne, mais tu n'as encore aucune interface pour discuter avec lui, uniquement une API brute. C'est le rôle d'Open WebUI Docker.

## Ajouter Open WebUI Docker : l'interface façon ChatGPT

Open WebUI Docker, c'est la couche visuelle : une interface de chat qui ressemble à s'y méprendre à ChatGPT, avec historique des conversations, sélection de modèle en un clic et gestion multi-utilisateurs. Le projet est maintenu par la communauté sous l'organisation GitHub `open-webui`, créée à l'origine par Timothy Jaeryang Baek, et distribué sous la licence Open WebUI License, une licence proche de BSD-3-Clause avec une clause imposant de conserver le branding du projet.

Pour tester vite, un seul container suffit :

```bash
docker run -d -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

L'interface est accessible sur `http://localhost:3000`, même si en interne le container écoute sur le port 8080. Mais pour durer, autant brancher Ollama et Open WebUI Docker ensemble dans un seul `docker-compose.yml`, avec un réseau dédié pour qu'ils se parlent directement par nom de service :

```yaml
services:
  ollama:
    image: ollama/ollama
    container_name: ollama
    restart: unless-stopped
    volumes:
      - ollama-data:/root/.ollama
    networks:
      - ia-locale

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    restart: unless-stopped
    depends_on:
      - ollama
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    ports:
      - "3000:8080"
    volumes:
      - open-webui-data:/app/backend/data
    networks:
      - ia-locale

volumes:
  ollama-data:
  open-webui-data:

networks:
  ia-locale:
```

Ici, `OLLAMA_BASE_URL=http://ollama:11434` dit à Open WebUI Docker où trouver Ollama en utilisant le nom du service plutôt qu'une adresse IP, puisque les deux containers partagent le réseau `ia-locale`. Pour le GPU, ajoute un bloc `deploy.resources.reservations.devices` avec `driver: nvidia` sous le service `ollama`, à côté du reste de la config.

Si tu gères déjà plusieurs stacks Compose sur ton serveur, [Dockge](/dockge-docker-gestionnaire-stacks-compose/) te permet de piloter celle-ci depuis une interface web plutôt qu'en jonglant avec des fichiers YAML en SSH.

Lance le tout avec `docker compose up -d`, puis ouvre `http://localhost:3000`.

## Télécharger un modèle et lancer ta première conversation

Au premier accès à Open WebUI Docker, un écran « Create Admin Account » t'invite à créer ton premier compte. Ce compte devient automatiquement administrateur, et l'inscription publique se désactive d'elle-même une fois ce compte créé. Si tu veux ouvrir l'accès à d'autres personnes plus tard, l'option se trouve dans Paramètres > Admin > Authentication, avec approbation manuelle des nouvelles inscriptions.

Il te reste à télécharger un modèle. Deux façons de faire : directement depuis le sélecteur de modèle dans Open WebUI Docker, qui propose une recherche et un téléchargement en un clic, ou en ligne de commande dans le container Ollama :

```bash
docker exec -it ollama ollama pull llama3.2
docker exec -it ollama ollama run mistral
```

`llama3.2` convient pour un usage généraliste léger, utilisable même sur une machine modeste. `mistral` tient mieux la route sur du raisonnement et du code. `gemma3` complète bien la liste pour des tâches de rédaction. Tu peux installer plusieurs modèles en parallèle et basculer de l'un à l'autre directement depuis le menu déroulant d'Open WebUI Docker, sans redémarrer quoi que ce soit.

Une fois le modèle chargé, ouvre une nouvelle conversation, tape ta question, et regarde la réponse se générer token par token, exactement comme sur ChatGPT. La différence, c'est que tout ce calcul se fait sur ton propre matériel.

## Sécuriser et dimensionner ta stack Ollama + Open WebUI Docker

Par défaut, rien dans cette configuration n'est pensé pour affronter internet directement. Si tu publies Open WebUI Docker au-delà de ton réseau local, passe par un reverse proxy avec TLS plutôt que d'exposer le port 3000 brut, et ne publie jamais le port 11434 d'Ollama en dehors de ton réseau interne : l'API n'a aucune authentification native.

Deux variables d'environnement méritent ton attention sur le container Open WebUI. `WEBUI_SECRET_KEY` doit rester fixe et identique à chaque redémarrage du container, sinon tous les comptes se retrouvent déconnectés à chaque recréation. `WEBUI_AUTH=False` désactive complètement l'authentification pour un usage strictement mono-utilisateur sur une machine déjà protégée, une bascule qu'il est impossible d'annuler ensuite sans repartir d'une base propre.

Pour suivre ce qui se passe dans les deux containers sans taper `docker logs -f` en boucle, [Dozzle](/dozzle-docker-visionneuse-logs-web/) affiche les journaux des deux services en direct dans un navigateur, pratique pour repérer un modèle qui refuse de charger ou une connexion qui traîne.

Côté dimensionnement, la règle est simple : plus le modèle est gros, plus il demande de mémoire. Sur CPU seul, les petits modèles répondent correctement mais avec un temps de génération qui s'allonge vite dès qu'on monte en taille. Une carte Nvidia avec suffisamment de VRAM accélère tout, sans changer une ligne de configuration côté Open WebUI Docker, puisque c'est Ollama qui gère le placement du modèle en mémoire.

## Cas d'usage concrets et limites à connaître

Une fois la stack en place, les usages s'enchaînent naturellement. Relecture et reformulation de texte sans envoyer le document à un tiers. Assistant de code pour du debug ponctuel ou de la génération de fonctions, utile même sans connexion internet une fois le modèle téléchargé. Résumé de notes ou de comptes-rendus avant de les ranger dans ton wiki perso.

Si tu exposes l'API d'Ollama à plusieurs applications internes de ton homelab, un cache [Redis](/redis-docker-base-donnees-cle-valeur/) placé devant les requêtes les plus répétées évite de refaire tourner le modèle pour la même question posée dix fois par dix outils différents.

Il faut aussi connaître les limites. Un modèle local reste moins capable sur du raisonnement complexe ou des connaissances très récentes que les plus gros modèles propriétaires accessibles uniquement en ligne, c'est le compromis entre confidentialité et puissance brute. Chaque modèle supplémentaire occupe aussi plusieurs gigaoctets sur disque, pense à surveiller l'espace disponible sur le volume `ollama-data` si tu accumules les versions.

## Conclusion

Ollama et Open WebUI Docker donnent accès à une vraie expérience de chat IA, sans dépendre d'un fournisseur cloud ni envoyer tes données ailleurs que sur ton propre serveur. L'installation tient en un fichier compose, la prise en main se fait en quelques minutes, et le choix du modèle reste entièrement entre tes mains. Lance la stack, télécharge un premier modèle, et juge par toi-même si ton usage quotidien de ChatGPT peut basculer en local.
