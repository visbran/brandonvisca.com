---
title: "Ghostty macOS : le terminal GPU qui fait de l'ombre à iTerm2"
description: "Ghostty macOS : terminal GPU gratuit et open source. Installation Homebrew, configuration complète et comparatif face à iTerm2 et Warp."
pubDatetime: "2026-11-04T11:03:02+01:00"
modDatetime: "2026-11-03T08:00:00.000Z"
author: Brandon
tags:
  - macos
  - terminal
  - homebrew
  - zsh
  - intermediaire
featured: false
draft: false
focusKeyword: ghostty macos
faqs:
  - question: "Ghostty est-il vraiment gratuit ?"
    answer: "Oui, licence MIT, code source ouvert, aucun palier payant. Le projet est devenu une organisation à but non lucratif sous Hack Club fin 2025, financée par les dons."
  - question: "Ghostty consomme-t-il moins de RAM qu'iTerm2 ou Warp ?"
    answer: "Oui en général. C'est un binaire natif qui délègue le rendu au GPU, sans la couche Electron ou les process web de certains concurrents."
  - question: "Où se trouve le fichier de configuration de Ghostty sur macOS ?"
    answer: "Dans ~/Library/Application Support/com.mitchellh.ghostty/config.ghostty, ou dans ~/.config/ghostty/config si tu préfères le chemin XDG."
---
> 💡 **TL;DR**
> - Ghostty macOS est un terminal gratuit, open source (MIT), qui rend tout via le GPU au lieu de repeindre du texte en CPU
> - Install en une ligne avec Homebrew, config dans un simple fichier texte `clé = valeur`, rechargement à chaud avec `cmd+shift+,`
> - Face à iTerm2 et Warp, Ghostty gagne sur la légèreté et la latence, perd sur l'écosystème de plugins et la maturité de l'interface

## Ghostty macOS : le terminal qui mise tout sur le GPU

Si t'es sur iTerm2 depuis dix ans comme moi, tu connais la routine. Ça marche, ça a toujours marché, mais ça commence à sentir le vieux parquet. Ghostty macOS arrive avec une promesse simple : un terminal natif, rapide, qui ne sacrifie rien sur les fonctionnalités modernes (onglets, splits, thèmes) tout en restant discret sur les ressources.

Le projet est signé Mitchell Hashimoto, le cofondateur de HashiCorp (Terraform, Vault). Ça ne garantit rien en soi, mais ça explique pourquoi Ghostty a débarqué avec une base technique sérieuse dès sa version 1.0, sortie en décembre 2024, plutôt qu'avec un prototype bricolé en weekend.

Mon setup a tourné sur iTerm2 pendant des années. Je suis passé à Ghostty il y a quelques mois sur ma machine principale, et la différence se sent surtout sur les gros dumps de logs ou les sessions tmux avec beaucoup de splits actifs. Spoiler : ça va marcher, mais il y a deux ou trois réglages à connaître avant que ce soit vraiment confortable.

## Table des matières

## Qu'est-ce que Ghostty, concrètement

Ghostty macOS est un émulateur de terminal natif, écrit en Zig, qui s'appuie sur le GPU de ta machine pour le rendu plutôt que sur le CPU. Concrètement, chaque caractère affiché passe par le pipeline graphique (Metal sur macOS) au lieu d'être redessiné pixel par pixel par le processeur. Le résultat : un scroll plus fluide, moins de latence quand tu balances des milliers de lignes d'un coup, et une consommation CPU au repos proche de zéro.

Côté licence, Ghostty est entièrement open source sous MIT. Le code est public sur GitHub, organisation `ghostty-org`. Fin 2025, le projet est devenu une organisation à but non lucratif parrainée par Hack Club, financée par les dons plutôt que par une vente de licences. Pas de version Pro, pas de palier payant caché : tout est dans la version gratuite.

Ce que Ghostty embarque nativement, sans plugin tiers :

- **Onglets et splits** : horizontaux, verticaux, redimensionnables à la souris ou au clavier
- **Thèmes** : des dizaines intégrés, plus la possibilité d'en charger des custom
- **Shell integration automatique** : détection de zsh, bash et fish pour le titre de fenêtre et le répertoire courant
- **Rendu GPU via Metal** : accélération matérielle native sur Apple Silicon et Intel
- **Configuration en texte brut** : un seul fichier, pas d'interface de préférences à cliquer

Ce qui manque encore par rapport à iTerm2 : pas de gestionnaire de profils graphique aussi poussé, et l'écosystème de scripts et d'extensions reste jeune comparé aux quinze ans d'historique d'iTerm2.

## Installer Ghostty macOS en quelques minutes

Deux façons d'installer Ghostty macOS, selon ton flux habituel.

**Via Homebrew** (ma méthode, la plus simple à maintenir) :

```bash
brew install --cask ghostty
```

Si tu n'as pas encore Homebrew sur ta machine, j'ai détaillé toute l'installation dans mon [guide Homebrew macOS](/installation-homebrew-macos/). Ça prend deux minutes et ça sert pour toutes les apps CLI qui vont suivre.

**Via le DMG officiel** : télécharge le fichier depuis le site officiel du projet, ouvre-le, glisse Ghostty dans le dossier Applications. Les binaires sont signés et notarisés par le projet Ghostty, donc macOS Gatekeeper ne devrait pas te bloquer au premier lancement.

Une fois Ghostty macOS installé, lance l'app depuis Spotlight ou le Launchpad. Au premier démarrage, l'app tourne avec une config par défaut déjà fonctionnelle : thème sombre, police système, raccourcis clavier standards. Tu peux t'arrêter là si tu veux juste un terminal qui marche. Mais la vraie question c'est ce que tu peux en tirer une fois que tu touches au fichier de config.

## Configurer Ghostty : le fichier config.ghostty

Ghostty n'a pas de fenêtre de préférences graphique classique. Toute la configuration passe par un fichier texte, au format `clé = valeur`, un réglage par ligne. Sur macOS, ce fichier s'appelle `config.ghostty` et vit dans :

```
~/Library/Application Support/com.mitchellh.ghostty/config.ghostty
```

Ghostty respecte aussi le chemin XDG classique si tu préfères centraliser tes dotfiles :

```
~/.config/ghostty/config
```

Si les deux fichiers existent, le chemin macOS est chargé en second et prend le dessus en cas de conflit. Crée le fichier et ouvre-le avec ton éditeur préféré. Si c'est vim, j'ai un [guide complet d'installation et de configuration de vim](/installation-vim-guide-complet/) qui couvre le `.vimrc` de base.

Un exemple de config de départ, raisonnable pour commencer :

```
font-family = "JetBrains Mono"
font-size = 14
background = 1e1e2e
foreground = cdd6f4
background-opacity = 0.92
window-padding-x = 10
window-padding-y = 10
cursor-style = block
copy-on-select = true
```

Chaque clé fonctionne aussi comme un flag en ligne de commande, pratique pour tester un réglage sans toucher au fichier : `ghostty --background-opacity=0.8`.

Deux commandes à connaître pour ne pas perdre de temps à déboguer une config cassée :

```bash
ghostty +validate-config
ghostty +show-config --default --docs
```

La première te dit immédiatement si une ligne est mal formée. La seconde liste toutes les options disponibles avec leur description, utile pour découvrir des réglages dont tu ne soupçonnais pas l'existence.

⚠️ Après une modification, pas besoin de relancer l'app. Le raccourci `cmd+shift+,` recharge la config à chaud dans la fenêtre active. Certaines options (surtout celles qui touchent au rendu ou à la fenêtre) ne s'appliquent qu'aux nouvelles fenêtres ouvertes après le rechargement, pas à celle en cours.

## Thèmes, police et transparence : personnaliser l'interface

Ghostty embarque une collection de thèmes prêts à l'emploi, sans rien installer en plus. Pour lister ceux disponibles :

```bash
ghostty +list-themes
```

Pour en appliquer un, une seule ligne dans `config.ghostty` :

```
theme = catppuccin-mocha
```

Si aucun thème livré ne te convient, tu peux définir tes propres couleurs manuellement avec les clés `background`, `foreground`, et les seize couleurs de la palette ANSI (`palette = 0=#...`). C'est plus verbeux qu'un thème tout fait, mais ça te donne un contrôle total si tu veux reproduire exactement ton setup iTerm2 actuel.

Sur la police, Ghostty fonctionne avec n'importe quelle police installée sur le système, Nerd Fonts compris pour les icônes dans ta barre de statut shell. Les polices à ligatures (JetBrains Mono, Fira Code, Cascadia Code) sont bien gérées, ce qui n'était pas garanti sur toutes les versions d'iTerm2.

Pour la transparence, `background-opacity` accepte une valeur entre 0 et 1. Attention à ne pas descendre trop bas si tu lis beaucoup de logs : à 0.7 et moins, la lisibilité sur fond clair en arrière-plan devient vite pénible.

✅ Petite astuce que j'utilise au quotidien : garder `background-opacity` autour de 0.9 à 0.95. Assez pour deviner le bureau derrière, assez opaque pour ne jamais avoir à plisser les yeux sur un paragraphe de logs d'erreur.

## Ghostty vs iTerm2 vs Warp : lequel choisir

La vraie question c'est de savoir si ça vaut le coup de migrer. Chez moi, le verdict dépend de ce que tu fais de ton terminal.

**Face à iTerm2** : Ghostty gagne sur la légèreté et la réactivité du rendu GPU, surtout avec beaucoup de panneaux ouverts en même temps. iTerm2 garde l'avantage sur la maturité, le gestionnaire de profils par SSH, et quinze ans de scripts communautaires. J'ai détaillé la configuration complète d'iTerm2 dans [mon guide iTerm2 macOS 2026](/iterm2-guide-configuration-macos-2025/) si tu veux comparer les deux configs ligne à ligne avant de trancher.

**Face à Warp** : Warp mise sur l'IA intégrée et des blocs de commande interactifs, avec une interface plus proche d'une app web qu'un terminal classique. Ghostty reste résolument minimaliste et natif, sans fonctionnalité IA, sans compte à créer. J'ai testé Warp en détail dans [mon comparatif Warp Terminal face à iTerm2](/warp-terminal-2025-iterm2-killer-ou-simple-hype-test-complet-ia/), utile si tu hésites entre les trois options plutôt qu'entre deux.

Bon, on va pas se mentir : aucun des trois n'est objectivement meilleur dans l'absolu. Si tu veux de la vitesse brute et une config qui vit dans un fichier texte versionnable sur Git, Ghostty macOS coche toutes les cases. Si tu dépends de plugins iTerm2 précis ou de fonctionnalités IA façon Warp, le calcul change.

## Dépannage : les problèmes qu'on rencontre vraiment

Quelques soucis récurrents quand on configure Ghostty macOS pour la première fois, et comment les résoudre.

**La config ne se recharge pas après modification.** Vérifie d'abord que le fichier ne contient pas d'erreur de syntaxe avec `ghostty +validate-config`. Une ligne mal formée bloque le rechargement de l'ensemble du fichier, pas juste de la ligne fautive.

**Les ligatures de police ne s'affichent pas.** Confirme que `font-family` pointe vers le nom exact de la police, pas vers un alias. Lance `ghostty +show-config` pour voir la valeur réellement interprétée.

**Le shell n'affiche pas le bon répertoire dans le titre de la fenêtre.** La shell integration automatique de Ghostty attend un shell standard (zsh, bash, fish) lancé normalement. Si tu passes par un wrapper custom ou un multiplexeur comme tmux sans la bonne config, cette intégration peut ne pas se déclencher.

**macOS bloque le lancement au premier démarrage.** Si tu as téléchargé le DMG en dehors du site officiel ou via un mirror non vérifié, Gatekeeper peut refuser l'ouverture. Réinstalle depuis le DMG officiel ou via Homebrew, les deux sources sont signées et notarisées.

## Conclusion

Ghostty macOS, au quotidien, n'est pas une révolution qui va faire disparaître iTerm2 du jour au lendemain, mais c'est clairement l'option la plus intéressante si tu veux un terminal natif, rapide, gratuit, et dont toute la config tient dans un fichier texte que tu peux versionner avec le reste de tes dotfiles.

Pour moi, la bascule s'est faite progressivement : d'abord en test sur une machine secondaire, puis en usage principal une fois le fichier `config.ghostty` calé avec mon thème et mes raccourcis habituels. Si t'es du genre à encore te battre avec les menus de préférences d'iTerm2, essaie Ghostty un week-end. Tu reviendras peut-être en arrière, mais au moins tu sauras pourquoi.
