---
title: "Homebrew macOS : Guide d'Installation Complet (2026)"
description: Comment installer Homebrew macOS en 1 commande. Prérequis, installation, commandes essentielles, apps incontournables et dépannage.
pubDatetime: 2025-03-31 15:28:09+02:00
modDatetime: 2026-04-11 00:00:00+01:00
author: Brandon Visca
tags:
  - macos
  - developpement
  - homebrew
  - terminal
  - debutant
  - guide
featured: false
draft: false
focusKeyword: homebrew macos
faqs:
  - question: "Homebrew est-il gratuit ?"
    answer: "Oui, Homebrew est un projet open source entièrement gratuit. Il fonctionne sur n'importe quel Mac sous macOS 11 (Big Sur) ou plus récent."
  - question: "Comment mettre à jour Homebrew ?"
    answer: "Lance brew update pour mettre à jour Homebrew, puis brew upgrade pour mettre à jour tous les paquets installés. Un brew cleanup ensuite supprime les vieilles versions."
  - question: "Homebrew ralentit-il le Mac ?"
    answer: "Non. Homebrew ne tourne pas en arrière-plan. Il s'exécute uniquement quand tu lances une commande brew. Aucun daemon, aucun impact sur les performances au repos."
---
## Table des matières

T'as besoin d'installer un outil sur macOS et tu tombes sur une doc qui commence par "first, install Homebrew" ? Homebrew macOS s'installe en une commande :

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Ça prend 2-3 minutes, ça demande ton mot de passe macOS, et c'est réglé. Mais si tu veux comprendre ce que tu fais et maîtriser l'outil, lis la suite.

## Qu'est-ce que Homebrew macOS ?

Homebrew, c'est le gestionnaire de paquets de facto sur macOS. Tu peux installer des outils en ligne de commande (git, ffmpeg, node...) et des applications graphiques depuis le terminal, sans passer par le Mac App Store ni traîner sur des pages de téléchargement.

Deux types de packages :

- **Formulae** : outils CLI (git, wget, python, ffmpeg...)
- **Casks** : applications macOS avec interface graphique (iTerm2, Docker, Firefox...)

## Prérequis

- macOS 11 (Big Sur) minimum — Monterey, Ventura, Sequoia : OK
- Connexion internet
- Les Xcode Command Line Tools (Homebrew les installe automatiquement si absents)

> 💡 **Astuce** : Sur Apple Silicon (M1/M2/M3/M4), Homebrew s'installe dans `/opt/homebrew/` au lieu de `/usr/local/`. Le comportement reste identique.

## Installer Homebrew sur macOS

Ouvre le Terminal (ou [iTerm2](https://brandonvisca.com/iterm2-guide-configuration-macos-2025/) si tu l'as déjà) et colle cette commande :

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

L'installateur va :

1. Télécharger et installer les Xcode Command Line Tools si nécessaires
2. Créer le répertoire Homebrew
3. Configurer ton PATH

Sur Apple Silicon, une étape supplémentaire apparaît à la fin du script. Suis les instructions affichées pour ajouter Homebrew à ton PATH (une ligne à copier dans ton `.zprofile`).

### Vérifier l'installation

```bash
brew doctor
```

La réponse attendue : `Your system is ready to brew.` Les warnings en jaune sont souvent inoffensifs. Les erreurs en rouge méritent attention.

```bash
brew --version
```

Affiche la version installée. Homebrew se met à jour automatiquement à chaque commande `brew install`.

## Les commandes Homebrew essentielles

| Commande | Action |
|---|---|
| `brew search <terme>` | Rechercher un paquet |
| `brew install <paquet>` | Installer un outil CLI |
| `brew install --cask <app>` | Installer une app graphique |
| `brew uninstall <paquet>` | Désinstaller |
| `brew update` | Mettre à jour Homebrew |
| `brew upgrade` | Mettre à jour tous les paquets |
| `brew upgrade <paquet>` | Mettre à jour un paquet précis |
| `brew list` | Lister ce qui est installé |
| `brew info <paquet>` | Infos sur un paquet |
| `brew cleanup` | Supprimer les vieilles versions |
| `brew autoremove` | Supprimer les dépendances orphelines |

> ⚠️ **Attention** : `brew upgrade` met à jour tout ce qui est installé. Sur des projets qui dépendent d'une version précise (Python, Node), préfère `brew upgrade <paquet>` pour cibler uniquement ce que tu veux.

## Premières apps à installer

Homebrew en place, voici ce qui mérite d'être là dès le départ.

**[iTerm2](https://brandonvisca.com/iterm2-guide-configuration-macos-2025/)**, le terminal qui remplace Terminal.app :

```bash
brew install --cask iterm2
```

**[ICE](https://brandonvisca.com/ice-macos-gestionnaire-barre-menu-gratuit-2025/)**, pour gérer la barre de menu (alternative gratuite à Bartender) :

```bash
brew install --cask jordanbaird-ice
```

**[AppCleaner](https://brandonvisca.com/appcleaner-mac-alternative-gratuite-cleanmymac/)**, pour désinstaller proprement tes apps sans laisser de fichiers fantômes :

```bash
brew install --cask appcleaner
```

**Wget**, parce qu'il manque sur macOS par défaut :

```bash
brew install wget
```

**Git** en version à jour (macOS livre une vieille version) :

```bash
brew install git
```

> 💡 **Astuce** : Tu préfères une interface graphique pour gérer tes packages ? [WailBrew](https://brandonvisca.com/wailbrew-interface-graphique-homebrew/) est une app open source qui visualise et met à jour tout ça sans toucher au terminal.

## Dépannage courant

**`brew: command not found` après installation**

Sur Apple Silicon, le PATH n'est pas configuré automatiquement. Ajoute cette ligne dans ton `~/.zprofile` :

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
source ~/.zprofile
```

**Permission denied lors de l'installation**

Homebrew ne se lance pas en `sudo`. Si tu as ce message, vérifie que ton utilisateur a les droits admin macOS.

**Conflit entre Homebrew et des outils système**

`brew doctor` identifie la plupart des problèmes. Lance-le, lis les messages, et suis les corrections proposées. La majorité sont des warnings sans impact réel.

**Mettre à jour une seule formule sans tout casser**

```bash
brew upgrade <nom-paquet>
```

Si quelque chose ne marche pas, c'est souvent un PATH mal configuré ou un conflit avec un outil installé manuellement avant Homebrew.

---

Homebrew macOS en place, la vraie question c'est : qu'est-ce que tu vas en faire ? Les outils comme `ffmpeg`, `yt-dlp` ou `mas` (pour le Mac App Store en ligne de commande) changent complètement le rapport au Mac. Commence par `brew search` et explore.
