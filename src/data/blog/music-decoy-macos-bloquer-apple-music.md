---
title: "Music Decoy macOS : Bloquer Apple Music au Démarrage (Solution Gratuite 2025)"
pubDatetime: "2025-11-26T22:15:32+01:00"
author: Brandon Visca
description: "Music Decoy empêche Apple Music de se lancer avec la touche Play sur macOS. Solution minimaliste gratuite pour utilisateurs Spotify ou YouTube Music."
tags:
  - macos
  - productivite
  - debutant
  - guide
  - utilitaire
  - music-decoy
---

TL;DR

Tu appuies sur la touche Play de ton clavier Mac pour lancer Spotify. Et là, Apple Music se lance. Encore. Pour la 47ème fois cette semaine.

Tu l’as jamais ouvert Apple Music. Tu l’ouvriras jamais. T’as un abonnement Spotify/YouTube Music/Deezer. Mais macOS s’en fout : par défaut, la touche Play du clavier = Apple Music.

**Music Decoy macOS** résout ce problème agaçant en **3 secondes**. C’est une micro-app qui intercepte la touche Play et empêche Apple Music de se lancer. C’est tout. Pas de configuration, pas de menu, juste une solution qui marche.

Dans ce guide ultra-rapide, je te montre comment installer Music Decoy macOS, le configurer pour qu’il démarre automatiquement, et les alternatives si ça te suffit pas.

- - - - - -

Le problème : macOS force Apple Music comme lecteur par défaut

Apple a codé en dur dans macOS : **touche Play = ouvrir Apple Music**.

Peu importe que tu utilises Spotify, YouTube Music, VLC, ou IINA. La touche Play du clavier (ou des AirPods, ou d’un clavier externe) lance **toujours** Apple Music en premier.

- - - - - -


- [Le problème : macOS force Apple Music comme lecteur par défaut](#le-probleme-mac-os-force-apple-music-comme-lecteur-par-defaut)
  - [Pourquoi c’est chiant ?](#pourquoi-cest-chiant)
- [Music Decoy macOS : la solution minimaliste](#music-decoy-mac-os-la-solution-minimaliste)
  - [Comment ça marche ?](#comment-ca-marche)
  - [Ce que Music Decoy fait PAS](#ce-que-music-decoy-fait-pas)
- [Installation de Music Decoy macOS](#installation-de-music-decoy-mac-os)
  - [Méthode 1 : Téléchargement direct](#methode-1-telechargement-direct)
  - [Méthode 2 : Via Homebrew (recommandé)](#methode-2-via-homebrew-recommande)
  - [Vérifier que ça fonctionne](#verifier-que-ca-fonctionne)
- [Configuration : lancement automatique au démarrage](#configuration-lancement-automatique-au-demarrage)
  - [Ajouter aux Login Items](#ajouter-aux-login-items)
- [Cas d’usage : qui a besoin de Music Decoy ?](#cas-dusage-qui-a-besoin-de-music-decoy)
  - [1. Tu utilises Spotify](#1-tu-utilises-spotify)
  - [2. Tu utilises YouTube Music](#2-tu-utilises-you-tube-music)
  - [3. Tu écoutes des podcasts via Overcast/Pocket Casts](#3-tu-ecoutes-des-podcasts-via-overcast-pocket-casts)
  - [4. Tu utilises VLC ou IINA pour lire des vidéos](#4-tu-utilises-vlc-ou-iina-pour-lire-des-videos)
- [Alternatives à Music Decoy macOS](#alternatives-a-music-decoy-mac-os)
  - [1. BeardedSpice (contrôle navigateur)](#1-bearded-spice-controle-navigateur)
  - [2. NoTunes (alternative similaire)](#2-no-tunes-alternative-similaire)
  - [3. Raccourcis clavier personnalisés (solution manuelle)](#3-raccourcis-clavier-personnalises-solution-manuelle)
- [Combiner Music Decoy avec d’autres outils](#combiner-music-decoy-avec-dautres-outils)
  - [Music Decoy + Raycast = Contrôle total Spotify](#music-decoy-raycast-controle-total-spotify)
  - [Music Decoy + IINA = Lecture vidéo sans interruption](#music-decoy-iina-lecture-video-sans-interruption)
- [Erreurs fréquentes avec Music Decoy macOS](#erreurs-frequentes-avec-music-decoy-mac-os)
  - [« Apple Music se lance toujours »](#apple-music-se-lance-toujours)
  - [« Music Decoy consomme trop de CPU »](#music-decoy-consomme-trop-de-cpu)
  - [« Les touches média ne fonctionnent plus du tout »](#les-touches-media-ne-fonctionnent-plus-du-tout)
- [Music Decoy sur différents devices](#music-decoy-sur-differents-devices)
  - [AirPods / AirPods Pro](#air-pods-air-pods-pro)
  - [Clavier externe Bluetooth](#clavier-externe-bluetooth)
  - [Touch Bar (MacBook Pro 2016-2020)](#touch-bar-mac-book-pro-2016-2020)
- [Désinstaller Music Decoy macOS](#desinstaller-music-decoy-mac-os)
- [Conclusion : Music Decoy, l’utilitaire qui règle un problème stupide](#conclusion-music-decoy-lutilitaire-qui-regle-un-probleme-stupide)
- [FAQ Music Decoy macOS](#faq-music-decoy-mac-os)
- [Liens utiles](#liens-utiles)


### Pourquoi c’est chiant ?

1. **Apple Music se lance** alors que tu veux juste lire sur Spotify
2. **Ça ralentit le Mac** (Apple Music démarre, charge, puis tu dois le quitter)
3. **Tu perds 3-5 secondes** à chaque fois à fermer Apple Music
4. **C’est frustrant** : t’as payé Spotify, pourquoi macOS force Apple Music ?

C’est pas un bug, c’est un « feature » voulu par Apple pour pousser Apple Music. Sauf que si t’utilises pas leur service, c’est juste relou.

- - - - - -

Music Decoy macOS : la solution minimaliste

![Music Decoy macOS 11-24 at 22.09.03@2x](Music-Decoy-macOS-11-24-at-22.09.03@2x.webp)Music Decoy est une app ultra-simple qui fait **une seule chose** : elle se place entre la touche Play et Apple Music, et dit « non ».

### Comment ça marche ?

1. Music Decoy tourne en arrière-plan (invisible)
2. Quand tu appuies sur Play, Music Decoy intercepte le signal
3. Au lieu de lancer Apple Music, il ne fait **rien**
4. Ton lecteur actif (Spotify, YouTube Music, VLC…) reçoit le signal et démarre la lecture

C’est transparent. T’appuies sur Play, ta musique démarre. Pas d’Apple Music qui popup.

### Ce que Music Decoy fait PAS

- ❌ Music Decoy ne contrôle pas Spotify (pas de play/pause/skip)
- ❌ Music Decoy ne change pas le lecteur par défaut (c’est impossible sur macOS)
- ❌ Music Decoy n’a pas d’interface (pas de fenêtre, pas de menu)

C’est juste un **bloqueur Apple Music**. Pour contrôler Spotify avec les touches média, utilise [Raycast](../raycast-macos-outil-productivite-ultime/.md) (extension Spotify intégrée).

- - - - - -

Installation de Music Decoy macOS

### Méthode 1 : Téléchargement direct

1. Va sur le [repo GitHub de Music Decoy](https://github.com/simonbs/MusicDecoy)
2. Télécharge le fichier `.app` depuis les Releases
3. Glisse **Music Decoy.app** dans `/Applications`
4. Lance l’app (clic droit &gt; Ouvrir si macOS bloque)

**Boom, c’est terminé.** Pas de configuration, pas de menu, rien. Music Decoy tourne en arrière-plan.

### Méthode 2 : Via Homebrew (recommandé)

Si t’utilises [Homebrew](https://brandonvisca.com/installation-homebrew-macos/), c’est encore plus rapide :

```bash
brew install --cask music-decoy

```

## Articles connexes

- [Magnet macOS : Le gestionnaire de fenêtres qui va transforme](/magnet-macos-gestionnaire-fenetres-guide-complet/)
- [Ice : L'alternative gratuite à Bartender qui révolutionne vo](/ice-macos-gestionnaire-barre-menu-gratuit-2025/)
