---
title: "Paperless-AI : classement automatique de tes documents par IA"
description: Paperless-AI classe automatiquement tes documents Paperless-ngx via Ollama ou OpenAI, mais le projet tourne en maintenance minimale en 2026.
pubDatetime: "2026-11-08T11:01:03+01:00"
modDatetime: "2026-11-07T08:00:00.000Z"
author: Brandon
tags:
  - auto-hebergement
  - docker
  - automation
  - intermediaire
featured: false
draft: false
focusKeyword: paperless-ai
faqs:
  - question: "Paperless-AI fonctionne-t-il sans Paperless-ngx déjà installé ?"
    answer: "Non, c'est une brique qui vient se greffer dessus : il lui faut l'URL de ton instance Paperless-ngx et un token API généré dans ses réglages pour pouvoir lire et taguer tes documents."
  - question: "Faut-il un GPU pour faire tourner Ollama avec Paperless-AI ?"
    answer: "Non. Des petits modèles comme Phi-3 ou Gemma-2 tournent correctement sur CPU pour un usage perso, mais un GPU accélère nettement l'analyse si tu traites beaucoup de documents."
  - question: "Paperless-AI est-il encore fiable à utiliser en 2026 malgré l'arrêt de la maintenance active ?"
    answer: "Il reste fonctionnel aujourd'hui et le code est open source sous licence MIT, mais sans mises à jour ni support garanti : pèse le risque avant de t'en servir pour des documents sensibles."
---
> 💡 **TL;DR**
> - Paperless-AI lit tes documents dans Paperless-ngx et leur assigne automatiquement titre, tags, type et correspondant via un modèle IA
> - Compatible Ollama en local (Mistral, Llama, Phi-3, Gemma-2) ou API cloud (OpenAI, DeepSeek, Gemini), installation en un conteneur Docker
> - Gratuit et open source, mais le dépôt n'est actuellement plus maintenu activement : à utiliser en connaissance de cause

## Paperless-AI, classer tes documents sans y passer tes soirées

Si t'as déjà un Paperless-ngx qui tourne chez toi, tu connais le problème. L'OCR fait son job, les PDF sont indexés, mais le tri reste sur ton dos. Tu scannes une facture, tu dois lui donner un titre correct, un correspondant, un type de document, des tags. Au bout de la 200e facture, tu zappes des étapes, et ton bureau numérique devient un vrac numérique.

C'est exactement le trou que **Paperless-AI** vient combler. Un outil tiers, pas une fonctionnalité native, qui se branche sur ton instance Paperless-ngx et laisse un modèle de langage faire le sale boulot de classement à ta place. Spoiler : ça marche plutôt bien, mais il y a un vrai bémol sur sa pérennité qu'on va aborder sans détour.

## Table des matières

## Paperless-AI, c'est quoi concrètement

Paperless-AI est un projet open source hébergé sur [GitHub par clusterzx](https://github.com/clusterzx/paperless-ai), sous licence MIT. Le principe est simple sur le papier : l'outil se connecte à l'API de ton instance Paperless-ngx, détecte les documents fraîchement scannés, les envoie à un modèle IA avec un prompt d'analyse, puis réinjecte automatiquement les métadonnées proposées (titre, tags, type de document, correspondant) dans Paperless-ngx.

Il embarque aussi une fonctionnalité de chat en RAG (retrieval-augmented generation) : tu peux poser des questions en langage naturel sur le contenu de tes documents indexés, un peu comme une recherche sémantique sur ta propre bibliothèque de PDF.

Si tu n'as pas encore Paperless-ngx chez toi, inutile d'aller plus loin dans cet article : commence par mon guide sur [Paperless-ngx, votre bureau numérique auto-hébergé avec OCR](/paperless-ngx-docker-guide-auto-hebergement/), Paperless-AI vient toujours en complément, jamais en remplacement.

## Installer Paperless-AI avec Docker

L'installation passe exclusivement par Docker, et c'est tant mieux. La commande documentée dans le wiki du projet :

```bash
docker run -d --name paperless-ai --network bridge -v paperless-ai_data:/app/data -p 3000:3000 --restart unless-stopped clusterzx/paperless-ai
```

Si tu préfères gérer ça en Compose, comme pour le reste de ton homelab, voici l'équivalent :

```yaml
services:
  paperless-ai:
    image: clusterzx/paperless-ai
    container_name: paperless-ai
    restart: unless-stopped
    ports:
      - "3000:3000"
    volumes:
      - paperless-ai_data:/app/data

volumes:
  paperless-ai_data:
```

Deux points de vigilance avant de lancer le `docker compose up -d` :

- ⚠️ L'image pèse plus de 4 Go. Elle embarque Node, les dépendances du moteur RAG, et tout ce qu'il faut pour l'analyse de documents. Prévois la place sur ton disque.
- ⚠️ Le tag `latest` de l'image n'a pas été reconstruit depuis environ un an au moment où j'écris ces lignes. Ce n'est pas bloquant pour l'usage, mais ça confirme ce qu'on va voir plus bas sur l'état du projet.

Si tu gères déjà une pile de conteneurs à la main et que ça commence à devenir confus, j'utilise [Dockge Docker pour gérer mes stacks Compose depuis une interface web](/dockge-docker-gestionnaire-stacks-compose/), ça évite de perdre le fil entre dix `docker-compose.yml` éparpillés.

Une fois le conteneur levé, rends-toi sur `http://ton-serveur:3000`. Toute la configuration se fait depuis le navigateur, pas de variable d'environnement à remplir à la main : l'URL de ton instance Paperless-ngx, un token API que tu génères dans ses réglages, et le choix de ton moteur IA.

## Connecter Paperless-AI à Ollama ou à un service cloud

C'est là que Paperless-AI devient intéressant pour qui veut garder ses documents hors des serveurs d'un tiers. L'outil supporte Ollama en local, avec des modèles comme Mistral, Llama, Phi-3 ou Gemma-2. Tout le pipeline d'analyse, lecture du document, extraction, classement, reste alors sur ta propre infra.

Si tu préfères la puissance d'un modèle cloud plutôt que la confidentialité totale, Paperless-AI parle aussi à OpenAI, DeepSeek, Gemini, OpenRouter, Perplexity, Together.ai, et plus largement à tout service compatible API OpenAI (LiteLLM, vLLM, FastChat en passerelle).

💡 Mon conseil : commence avec Ollama et un petit modèle comme Phi-3 pour valider que le classement te convient, avant d'ouvrir la porte à une API externe. Tes factures et tes relevés bancaires n'ont rien à faire sur un serveur que tu ne contrôles pas.

Après la configuration initiale (clés, préférences), un redémarrage du conteneur Paperless-AI est nécessaire pour construire l'index utilisé par le chat RAG. Ce n'est en revanche pas requis pour les mises à jour suivantes.

## Ce que Paperless-AI classe automatiquement pour toi

Une fois branché, Paperless-AI scanne les nouveaux documents entrants dans Paperless-ngx et leur assigne :

- **Un titre** cohérent, basé sur le contenu réel du document plutôt que sur le nom du fichier scanné
- **Des tags** pertinents, repris du vocabulaire déjà utilisé dans ton instance
- **Un type de document** (facture, contrat, relevé, courrier...)
- **Un correspondant**, détecté à partir de l'en-tête ou de la signature du document

C'est exactement le genre de tâche répétitive qui ne mérite pas ton attention humaine. Tu scannes, Paperless-AI range, tu valides ou tu corriges si besoin. Le gain de temps est réel dès que tu dépasses la dizaine de documents par semaine.

Si un classement te semble bizarre, ouvre les logs du conteneur pour comprendre ce que le modèle a vu. J'utilise [Dozzle Docker comme visionneuse de logs en temps réel via le web](/dozzle-docker-visionneuse-logs-web/) pour ce genre de vérification rapide, sans taper une seule commande `docker logs`.

## Statut du projet : une maintenance en pause

Bon, on va pas se mentir, c'est le point le plus important de cet article et il serait malhonnête de le glisser en bas de page. Le README du dépôt est explicite : le projet n'est **actuellement pas maintenu**. L'auteur, `clusterzx`, explique qu'il retravaille entièrement le code sur son temps libre, sans garantie de délai ni de support actif.

Il avance aussi une raison à cette pause : une intégration IA native annoncée côté Paperless-ngx lui-même, qui rendrait potentiellement Paperless-AI redondant. Je n'ai pas pu confirmer ce point de façon indépendante sur les canaux officiels de Paperless-ngx, donc je le rapporte comme une déclaration de l'auteur, pas comme un fait établi.

Concrètement, qu'est-ce que ça change pour toi aujourd'hui :

- ✅ Le code reste disponible, fonctionnel, et sous licence MIT : tu peux l'auditer, le forker, le modifier.
- ✅ L'image Docker tourne toujours et répond, même si son tag n'a pas bougé depuis un moment.
- ⚠️ Aucune garantie de correctif si une faille est découverte, ni de compatibilité avec les futures versions de Paperless-ngx.
- ⚠️ Le support communautaire (issues GitHub) risque de rester sans réponse.

La vraie question c'est : est-ce que tu veux dépendre d'un outil en pause pour une tâche qui touche tes documents administratifs ? Pour un usage perso sur un homelab, avec une sauvegarde régulière de ta base Paperless-ngx, le risque reste raisonnable. Pour un usage professionnel ou sur des documents sensibles, je serais plus prudent.

## Limites, alternatives et cas d'usage pour ton homelab

Paperless-AI n'est pas magique. Quelques limites concrètes à connaître avant de l'adopter :

- **Pas d'apprentissage continu** : chaque document est analysé indépendamment, l'outil ne construit pas de profil de classement propre à tes habitudes au fil du temps.
- **Dépendance totale à Paperless-ngx** : sans instance Paperless-ngx déjà configurée et accessible via API, Paperless-AI ne fait rien.
- **Qualité du classement liée au modèle choisi** : un petit modèle local en CPU classera correctement des documents simples, mais hésitera davantage sur des contrats longs ou mal scannés.

Si tu veux comparer avant de t'engager, deux projets occupent le même créneau : **Paperless-GPT**, qui mise sur l'extraction OCR via des modèles de vision, et **Paperless AIssist**, qui déclenche l'analyse via un tag manuel plutôt qu'automatiquement. Aucun des trois n'est une fonctionnalité native de Paperless-ngx à ce jour.

Dans mon propre homelab, Paperless-AI tourne à côté d'autres briques auto-hébergées comme [Vikunja pour la gestion de tâches](/vikunja-docker-gestionnaire-taches/) : l'idée derrière tout ça, c'est de garder le contrôle sur mes données administratives sans dépendre d'un SaaS tiers qui change ses conditions tous les deux ans.

## Conclusion

Paperless-AI fait ce qu'il promet : il te débarrasse du tri manuel de tes documents scannés dans Paperless-ngx, en local si tu le branches à Ollama, ou via une API cloud si tu préfères la puissance. L'installation Docker prend cinq minutes, la configuration se fait entièrement depuis le navigateur.

Le vrai point d'attention, c'est l'état de maintenance du projet. Fonctionnel aujourd'hui, open source, mais sans garantie de suivi. Si tu peux vivre avec ça, c'est-à-dire si tu gardes une sauvegarde saine de ta base documentaire et que tu n'y mets rien de critique sans vérification, Paperless-AI reste un gain de temps net pour ton bureau numérique auto-hébergé.
