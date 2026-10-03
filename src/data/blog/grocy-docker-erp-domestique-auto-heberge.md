---
title: "Grocy Docker : ERP domestique auto-hébergé (stocks, courses, tâches)"
description: "Grocy Docker : installe cet ERP domestique auto-hébergé pour gérer stocks, courses, recettes et tâches ménagères sans dépendre du cloud."
pubDatetime: "2026-09-29T11:02:12+02:00"
modDatetime: "2026-09-28T08:00:00.000Z"
author: Brandon
tags:
  - auto-hebergement
  - docker
  - stockage
  - automation
  - intermediaire
featured: false
draft: false
focusKeyword: grocy docker
faqs:
  - question: "Combien de ressources consomme Grocy sur mon serveur ?"
    answer: "Grocy tourne sur PHP et SQLite, donc l'empreinte reste légère. Un petit conteneur LXC ou un Raspberry Pi suffisent largement pour un usage familial, pas besoin d'une grosse VM dédiée."
  - question: "Que se passe-t-il si je perds l'accès à mon conteneur Grocy ?"
    answer: "Si tu as sauvegardé le dossier config monté en volume, tu recrées le conteneur et tu restaures ce dossier. Sans backup, tu perds l'historique des stocks, des courses et des recettes."
  - question: "Faut-il un lecteur de codes-barres pour utiliser Grocy ?"
    answer: "Non, tu peux tout saisir à la main depuis le navigateur ou l'app mobile. Un scanner accélère juste la saisie quotidienne, il n'est jamais obligatoire pour faire tourner l'ERP."
---
> 💡 **TL;DR**
> - Grocy Docker installe un ERP domestique auto-hébergé qui gère stocks, courses, recettes et tâches ménagères depuis un seul dashboard
> - Déploiement via l'image linuxserver/grocy, port 9283, volume config persistant, identifiants par défaut admin/admin à changer immédiatement
> - Projet open source gratuit maintenu par Bernd Bestel depuis 2017, aucune dépendance cloud, tes données restent chez toi

## Grocy Docker : ton ERP domestique auto-hébergé

Tu jettes des yaourts périmés que t'avais oubliés au fond du frigo. Tu refais trois fois la liste de courses parce que t'as encore oublié le produit vaisselle. Bref, ta cuisine tourne à l'improvisation.

Grocy règle ça. C'est un ERP (progiciel de gestion) pensé pour la maison plutôt que pour l'entreprise : stocks alimentaires, courses, recettes, planning des repas et tâches ménagères, le tout dans une seule appli web que tu héberges toi-même. Avec Grocy Docker, tu montes l'ensemble en quelques minutes, sans dépendre d'un service cloud qui pourrait fermer boutique demain.

## Table des matières

## Pourquoi passer par Grocy Docker plutôt qu'un tableau Excel

Un tableur, ça marche cinq minutes. Puis tu oublies de le mettre à jour, il traîne dans un coin de ton disque, et tu reviens à la mémoire (mauvaise) de ton frigo.

Grocy fonctionne autrement. Chaque produit que tu ajoutes en stock a une date de péremption, une quantité minimale, un emplacement. Dès que tu descends sous le seuil défini, l'article part automatiquement sur ta liste de courses. Tu consommes un produit, tu décrémentes le stock, et le système sait exactement ce qu'il te reste.

Ce qui distingue vraiment Grocy d'un simple tracker de stock, c'est l'approche ERP :

- **Gestion des stocks** avec lecture de codes-barres et dates de péremption
- **Listes de courses** générées automatiquement selon les seuils définis
- **Recettes** qui vérifient si tu as les ingrédients disponibles avant de cuisiner
- **Plan de repas** avec suggestions pour écouler ce qui va périmer
- **Tâches et corvées** récurrentes (nettoyage du frigo, entretien du lave-linge)
- **API REST complète** pour brancher tes propres automatisations

Le projet est développé par Bernd Bestel depuis 2017, en open source et gratuit. Pas d'abonnement, pas de compte tiers, pas de publicité planquée dans les recettes.

## Installation de Grocy avec Docker Compose

L'image communautaire la plus maintenue est celle de linuxserver.io. Elle embarque Grocy, PHP et SQLite dans un seul conteneur, prêt à l'emploi.

Crée un fichier `docker-compose.yml` :

```yaml
services:
  grocy:
    image: lscr.io/linuxserver/grocy:latest
    container_name: grocy
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Paris
    volumes:
      - /path/to/grocy/config:/config
    ports:
      - 9283:80
    restart: unless-stopped
```

Adapte `/path/to/grocy/config` vers un dossier réel sur ton serveur, et vérifie que `PUID`/`PGID` correspondent à ton utilisateur (`id -u` et `id -g` te donnent les valeurs). Lance le tout :

```bash
docker compose up -d
```

Rends-toi ensuite sur `http://ip-de-ton-serveur:9283`. Grocy tourne derrière le port interne 80, remappé sur 9283 côté hôte.

⚠️ Les identifiants par défaut sont `admin` / `admin`. Change ce mot de passe à la première connexion, avant même de commencer à remplir tes stocks. Un ERP domestique exposé avec des identifiants par défaut sur ton réseau, c'est une porte ouverte inutile.

Si tu veux exposer Grocy proprement en dehors de ton réseau local, passe-le derrière un reverse proxy avec HTTPS plutôt que de forwarder le port 9283 directement sur ta box.

## Premiers pas : configuration et prise en main

Une fois connecté, commence par la section **Réglages** pour définir ta langue, ta devise et le fuseau horaire (déjà réglé côté conteneur, mais Grocy a aussi son propre réglage interne).

Crée ensuite tes **emplacements de stock** : frigo, congélateur, placard, cave. Chaque produit que tu ajoutes est rattaché à un emplacement, ce qui t'évite de chercher pendant dix minutes où tu as bien pu ranger cette boîte de conserve.

Ajoute quelques produits de base avec leur quantité minimale souhaitée. C'est ce seuil qui déclenche l'ajout automatique à la liste de courses dès que tu passes en dessous. Pas besoin de tout remplir le premier jour : Grocy prend son sens au fur et à mesure que tu enregistres tes achats et tes consommations.

## Gérer tes stocks, tes courses et tes recettes

Le workflow quotidien tient en trois gestes. Tu achètes, tu ajoutes le produit au stock (scan du code-barres ou saisie manuelle). Tu consommes, tu retires la quantité utilisée. Le stock reflète toujours la réalité, et la liste de courses se construit toute seule.

Côté recettes, Grocy compare les ingrédients requis à ton stock actuel et t'indique ce qui te manque avant même de commencer à cuisiner. Tu peux planifier tes repas sur la semaine et laisser Grocy te suggérer les plats qui utilisent les produits proches de leur date de péremption. C'est probablement la fonctionnalité qui réduit le plus concrètement le gaspillage.

✅ Petite astuce : configure des règles de péremption par défaut pour les catégories de produits que tu achètes souvent (lait, légumes frais). Tu gagnes du temps à chaque ajout plutôt que de ressaisir une date à la main.

Grocy gère aussi les tâches ménagères récurrentes et l'entretien des équipements (changement de filtre, nettoyage du four), un peu comme un backlog domestique. Si tu documentes déjà tes procédures maison ailleurs, un wiki comme [BookStack](/bookstack-docker-wiki-equipe/) complète bien Grocy pour tout ce qui ne rentre pas dans une fiche produit : mode d'emploi d'un appareil, recette longue, notes d'entretien.

Et si ton objectif dépasse la cuisine pour couvrir tout le budget du foyer, [Actual Budget](/actual-budget-docker-gestion-budget/) suit la même philosophie que Grocy : auto-hébergé, sans abonnement, données chez toi. Les deux se complètent bien pour piloter une maison sans dépendre d'apps tierces.

## Sauvegarder et sécuriser ton instance Grocy

Toute la base de données de Grocy vit dans le dossier `config` que tu as monté en volume. Si ce dossier disparaît sans backup, tu perds l'historique complet : stocks, courses, recettes, tâches.

Mets en place une sauvegarde automatique de ce volume. [Duplicati](/duplicati-docker-sauvegarde/) fait très bien le travail pour chiffrer et planifier des sauvegardes régulières vers un stockage distant, sans effort manuel une fois configuré.

Pense aussi à limiter l'exposition réseau de Grocy. Si tu dois y accéder depuis l'extérieur, un VPN ou un reverse proxy avec authentification supplémentaire reste plus sûr qu'un port ouvert directement sur internet.

Après chaque mise à jour de l'image Docker, Grocy exécute ses migrations de base de données automatiquement à la première visite de la page d'accueil. Prévois donc toujours une sauvegarde juste avant de tirer une nouvelle version de l'image.

## Limites et points de vigilance

Grocy demande de la discipline. Si tu n'enregistres pas systématiquement tes achats et tes consommations, le stock affiché ne colle plus à la réalité et l'outil perd tout son intérêt. C'est le même problème que n'importe quel outil de suivi : la valeur vient de la régularité, pas du logiciel seul.

L'interface, bien que fonctionnelle, reste un peu datée visuellement comparée à des apps commerciales récentes. Ce n'est pas gênant au quotidien, mais autant le savoir avant de te lancer.

Enfin, l'app mobile facilite la saisie en magasin mais elle n'est pas aussi polie que l'interface web. Pour un usage confortable, prévois de scanner tes achats depuis ton téléphone puis de peaufiner les détails (recettes, plan de repas) depuis un écran plus grand.

💡 À lire aussi : [Calibre Web Docker : bibliothèque ebooks auto-hébergée](/calibre-web-docker-bibliotheque-ebooks/), dans la même veine que cet article.

## Conclusion

Grocy Docker te donne un vrai ERP domestique, sans les efforts habituels de déploiement d'un ERP d'entreprise. Un fichier compose, un port, un volume à sauvegarder, et tu passes du frigo mystère à un stock que tu maîtrises vraiment.

Ce n'est pas magique : ça demande de la régularité dans la saisie. Mais une fois le réflexe pris, tu arrêtes de jeter de la nourriture périmée et tu arrêtes de refaire ta liste de courses trois fois par semaine. Chez moi, c'est ce genre d'outil discret qui finit par devenir indispensable sans qu'on s'en rende compte.
