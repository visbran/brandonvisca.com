---
title: "Ladybird Browser : Le navigateur web qui refuse de se soumettre à Google (et tant mieux)"
pubDatetime: "2025-06-13T18:47:21+02:00"
description: "Découvrez Ladybird, le nouveau navigateur open source construit from scratch. Architecture, financement, timeline et pourquoi ça change tout pour le web."
tags:
  - autres
---

-----------

- [Architecture technique : du multi-processus qui assume](#architecture-technique-du-multi-processus-qui-assume)
  - [LibWeb et LibJS : les moteurs faits maison](#lib-web-et-lib-js-les-moteurs-faits-maison)
- [Compilation et installation : pour les courageux](#compilation-et-installation-pour-les-courageux)
- [Financement : l’argent sans les contraintes](#financement-largent-sans-les-contraintes)
- [Pourquoi ça compte pour l’écosystème web](#pourquoi-ca-compte-pour-lecosysteme-web)
- [Timeline et réalisme](#timeline-et-realisme)
- [Pour qui et pourquoi tester](#pour-qui-et-pourquoi-tester)
- [Ce qui manque encore (et c’est normal)](#ce-qui-manque-encore-et-cest-normal)
- [Conclusion](#conclusion)
- [Soutenir le projet](#soutenir-le-projet)


Non, ce n’est pas encore un autre fork de Chromium avec une interface redessinée et trois fonctionnalités « révolutionnaires ». C’est carrément plus ambitieux que ça.

Andreas Kling et son équipe ont eu une idée assez folle : repartir de zéro. Complètement. Même pas de code recyclé de WebKit, Blink ou Gecko. Du pur travail artisanal, comme on sait encore le faire dans l’open source quand on a du temps, de la passion et, accessoirement, des financements sérieux.

Un navigateur né d’un hobby qui a mal tourné
--------------------------------------------

L’histoire commence en 2018 avec SerenityOS, le projet « thérapie » d’Andreas Kling après sa sortie de cure de désintoxication. Ce qui devait être un simple OS personnel s’est transformé en écosystème complet avec son propre navigateur web. Sauf qu’à un moment, Andreas s’est dit : « Et si on sortait ce navigateur de SerenityOS pour en faire quelque chose de vraiment cross-platform ? »

Le 4 juillet 2022, première démo publique de Ladybird avec une interface Qt basique. Deux ans plus tard, en juillet 2024, le projet annonce son indépendance totale avec la création de la **Ladybird Browser Initiative**, une 501(c)(3) non-profit financée par Chris Wanstrath (co-fondateur de GitHub) et d’autres sponsors comme Shopify et Proton VPN.

**Message reçu** : quand vous avez assez d’argent et pas d’objectifs commerciaux douteux, vous pouvez vous permettre de dire non aux « default search deals » et autres joyeusetés du business model publicitaire.

Architecture technique : du multi-processus qui assume
------------------------------------------------------

Contrairement au Safari de base ou à Chrome dans ses mauvais jours, Ladybird mise tout sur une **architecture multi-processus robuste** :

- **Processus UI principal** : interface utilisateur
- **Processus WebContent** : rendu des pages (un par onglet)
- **Processus ImageDecoder** : décodage d’images isolé
- **Processus RequestServer** : gestion réseau séparée

Chaque onglet est sandboxé du reste du système. Si une page malveillante plante, elle n’emmène pas tout le navigateur avec elle. Du bon sens technique, enfin.

### LibWeb et LibJS : les moteurs faits maison

Le cœur de Ladybird, c’est **LibWeb** (moteur de rendu) et **LibJS** (moteur JavaScript), tous deux développés from scratch. Pas de récupération de code existant, pas de raccourcis. L’équipe veut créer une implémentation des standards web qui leur appartient totalement.

**Côté performance** : on n’est pas encore au niveau de Chrome ou Safari, mais selon les Web Platform Tests (mars 2025), Ladybird se classe déjà **4ème** derrière Chrome, Safari et Firefox. Pas mal pour un projet de quelques années.

Compilation et installation : pour les courageux
------------------------------------------------

Attention, Ladybird n’est pas encore prêt pour votre grand-mère. Le projet vise une alpha en **été 2026**, une beta en **2027** et une release stable pour le grand public en **2028**.

Pour les développeurs qui veulent jouer avec :

```bash
# Clone le repo
git clone https://github.com/LadybirdBrowser/ladybird.git
cd ladybird

# Installation des dépendances (Ubuntu/Debian)
sudo apt update
sudo apt install build-essential cmake ninja-build qt6-base-dev

# Compilation (comptez 1-2h la première fois)
./Meta/build.sh

# Lancement
./Build/ladybird

```

