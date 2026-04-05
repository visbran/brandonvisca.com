---
title: "iTerm2 sur macOS : Le guide complet pour dompter votre terminal (2025)"
pubDatetime: "2025-03-31T15:19:31+02:00"
description: "Transformez votre terminal macOS avec iTerm2 ! Installation, themes, Oh My Zsh, plugins indispensables - Le guide ultime pour booster votre productivité..."
tags:
  - iterm2
  - terminal
  - macos
  - oh-my-zsh
  - productivite
  - developpement
  - guide
  - intermediaire
---

--------

- [Installation d’iTerm2 : Les bonnes méthodes](#installation-di-term-2-les-bonnes-methodes-installation-iterm-2)
  - [Méthode recommandée : Homebrew (pour les pros)](#methode-recommandee-homebrew-pour-les-pros)
  - [Méthode manuelle : Old school mais efficace](#methode-manuelle-old-school-mais-efficace)
- [Configuration de base : Les indispensables](#configuration-de-base-les-indispensables-configuration-base)
  - [Thèmes et couleurs qui claquent](#themes-et-couleurs-qui-claquent-themes-couleurs)
  - [Polices : Fini les caractères illisibles](#polices-fini-les-caracteres-illisibles-polices-lisibles)
  - [Raccourcis clavier : Votre nouvelle routine](#raccourcis-clavier-votre-nouvelle-routine-raccourcis-clavier)
- [Personnalisation avancée : On passe au niveau supérieur](#personnalisation-avancee-on-passe-au-niveau-superieur-personnalisation-avancee)
  - [Oh My Zsh : Le couteau suisse du terminal](#oh-my-zsh-le-couteau-suisse-du-terminal-oh-my-zsh)
  - [Plugins qui changent la vie](#plugins-qui-changent-la-vie-plugins-utiles)
      - [Les essentiels](#les-essentiels)
      - [Installation des plugins communautaires](#installation-des-plugins-communautaires)
      - [Les plugins de niche (mais utiles)](#les-plugins-de-niche-mais-utiles)
  - [Prompt personnalisé : Votre signature](#prompt-personnalise-votre-signature-prompt-personnalise)
- [Tips de pro et configuration ultime](#tips-de-pro-et-configuration-ultime-tips-pro)
  - [Le hotkey window : Votre terminal toujours accessible](#le-hotkey-window-votre-terminal-toujours-accessible)
  - [Profils multiples : Un terminal pour chaque contexte](#profils-multiples-un-terminal-pour-chaque-contexte)
  - [Synchronisation cloud](#synchronisation-cloud)
  - [Sessions et restauration](#sessions-et-restauration)
- [Un terminal propre mérite une barre de menu organisée](#un-terminal-propre-merite-une-barre-de-menu-organisee)
- [Conclusion : Votre terminal de guerre est prêt](#conclusion-votre-terminal-de-guerre-est-pret-conclusion)
  - [Le récap des indispensables :](#le-recap-des-indispensables)
  - [Et maintenant ?](#et-maintenant)
  - [Ressources utiles :](#ressources-utiles)

--------------------------------------

Soyons honnêtes : le **Terminal natif de macOS**, c’est un peu comme conduire une Twingo quand on pourrait avoir une Tesla. Ça fait le job, mais **iTerm2**, c’est le **meilleur terminal macOS 2025** qui comprend vos besoins de **développeur moderne**.

Au programme : **split-screen**, **recherche avancée**, **hotkey window**, **autocomplete intelligent**… Et surtout, une personnalisation qui fait que votre terminal devient réellement **VOTRE** outil de travail.

> **Fun fact :** iTerm2 existe depuis 2009 et a survécu à tous les changements d’Apple. Autant dire que c’est du solide !

Installation d’iTerm2 : Les bonnes méthodes
-------------------------------------------

### Méthode recommandée : Homebrew (pour les pros)

Si vous n’avez pas encore Homebrew sur votre Mac… qu’est-ce que vous attendez ? 😄

```bash
# Installation via Homebrew (la classe)
brew install --cask iterm2

```

# Import automatique de thèmes supplémentaires
git clone https://github.com/mbadolato/iTerm2-Color-Schemes.git
# Puis : Preferences > Profiles > Colors > Color Presets > Import


### Polices : Fini les caractères illisibles

Une bonne police monospace, c’est **50% de votre confort** de dev. Voici les championnes :

**Les valeurs sûres :**

- **JetBrains Mono** : Créée par des devs pour des devs (ligatures incluses)
- **Fira Code** : Les ligatures qui rendent le code plus lisible
- **Source Code Pro** : Adobe sait y faire
- **Hack** : Simple, efficace, open source

**Installation express :**

```bash
# Via Homebrew Fonts
brew tap homebrew/cask-fonts
brew install --cask font-jetbrains-mono
brew install --cask font-fira-code

```

sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"


> **Installation détaillée :** Pour un guide complet avec troubleshooting et customisation avancée 👉 [**Installation complète de Oh My Zsh**](https://brandonvisca.com/installation-de-oh-my-zsh/)

**Ce qui change immédiatement :**

- **Autocomplétion intelligente** : Tab devient votre meilleur ami
- **Aliases Git** : `gco` au lieu de `git checkout`
- **Navigation améliorée** : `..` pour remonter, `...` pour remonter deux fois
- **Historique partagé** : Entre tous vos onglets

### Plugins qui changent la vie

Voici ma sélection **testée et approuvée** en production :

#### Les essentiels

```bash
# Dans ~/.zshrc, section plugins=(...)
plugins=(
  git                    # Aliases Git partout
  docker                 # Autocomplétion Docker
  brew                   # Autocomplétion Homebrew
  macos                  # Raccourcis macOS spécifiques
  zsh-autosuggestions   # Suggestions basées sur l'historique
  zsh-syntax-highlighting # Coloration syntaxique en temps réel
)

```

# zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# zsh-syntax-highlighting  
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting


#### Les plugins de niche (mais utiles)

- **web-search** : `google "comment faire du café"`
- **extract** : `extract fichier.zip` (fonctionne avec tout)
- **z** : Navigation intelligente (`z project` pour aller dans n’importe quel dossier projet)

### Prompt personnalisé : Votre signature

Votre prompt, c’est votre **signature**. Voici mes recommandations :

**Pour les minimalistes :** `robbyrussell` (par défaut, efficace) **Pour les infos complètes :** `agnoster` (branch Git, status, chemin) **Pour les fans de couleurs :** `powerlevel10k` (le Rolls des prompts)

```bash
# Installation de Powerlevel10k (le plus populaire)
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k

# Dans ~/.zshrc
ZSH_THEME="powerlevel10k/powerlevel10k"

```

