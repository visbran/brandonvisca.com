---
title: "Installation d'homebrew sur MacOS"
pubDatetime: "2025-03-31T15:28:09+02:00"
author: Brandon Visca
description: "Homebrew est le gestionnaire de paquets le plus populaire pour macOS. Il simplifie considérablement l''installation et la gestion des logiciels sur votr..."
tags:
  - macos
  - developpement
  - debutant
  - homebrew
  - guide
  - cli
---

![](norwalkbrewhouse-cerveza-smooth-craft-beer-2xloq6w2wweu0fgdpi.gif)

Introduction à Homebrew

Homebrew est le gestionnaire de paquets le plus populaire pour macOS. Il simplifie considérablement l’installation et la gestion des logiciels sur votre Mac.

- - - - - -

Sommaire

- [Prérequis système](#prerequis-systeme)
- [Processus d’installation](#processus-dinstallation)
- [Vérification de l’installation](#verification-de-linstallation)
- [Utilisation basique](#utilisation-basique)
- [Les apps essentielles à installer immédiatement](#les-apps-essentielles-a-installer-immediatement)
  - [L’essentiel pour démarrer :](#lessentiel-pour-demarrer)
- [Dépannage courant](#depannage-courant)


Prérequis système

- MacOS 11 (Big Sur) ou plus récent
- Xcode Command Line Tools
- Terminal ou Autre (iTerm2)

Processus d’installation

Pour installer Homebrew, ouvrez le Terminal et exécutez la commande suivante :

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

brew doctor

> Une fois Homebrew installé, vous pouvez installer des outils  
> comme **iTerm2** 👉 [Guide complet iTerm2 macOS](/lien-iterm2)«

Utilisation basique

Voici les commandes de base pour utiliser Homebrew :

- `brew search [paquet]` – Rechercher un paquet
- `brew install [paquet]` – Installer un paquet
- `brew uninstall [paquet]` – Désinstaller un paquet
- `brew update` – Mettre à jour Homebrew
- `brew upgrade` – Mettre à jour tous les paquets

Les apps essentielles à installer immédiatement

Maintenant que **Homebrew tourne comme une horloge suisse**, voici les premières applications à installer pour transformer votre Mac en machine de guerre :

### L’essentiel pour démarrer :

iterm2 le remplaçant de Terminal :

```bash
brew install --cask iterm2
```

brew install --cask visual-studio-code

L’alternative à Bartender, gratuite et opensource :

```bash
brew install --cask jordanbaird-ice
```

brew install --cask docker

**AppCleaner** pour désinstaller proprement tes apps ([guide complet](/appcleaner-mac-alternative-gratuite-cleanmymac/))

```bash
brew install --cask appcleaner
```
