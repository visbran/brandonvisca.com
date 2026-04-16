---
title: "Thème Vim : installer Catppuccin avec vim-plug en 5 minutes"
description: "Installe le thème Catppuccin dans Vim en 5 minutes : vim-plug, configuration .vimrc et dépannage des couleurs 256. Fonctionne sur macOS et Linux."
pubDatetime: "2025-03-31T15:43:24+02:00"
modDatetime: 2026-04-16 00:00:00+01:00
author: Brandon Visca
tags:
  - vim
  - theme
  - catppuccin
  - linux
  - guide
  - debutant
featured: false
draft: false
focusKeyword: catppuccin
---
> 💡 **TL;DR** — Catppuccin est le thème Vim le plus populaire en 2025. Installe vim-plug, ajoute 2 lignes dans ton `.vimrc`, lance `:PlugInstall`. C'est tout. Si les couleurs ne s'affichent pas, ajoute `set termguicolors` dans ton `.vimrc`.

J'utilise Catppuccin Mocha sur tous mes terminaux et dans Vim. C'est le thème qui tient le mieux sur les fonds sombres sans fatiguer les yeux après 4 heures de session. Voilà comment l'installer proprement.

## Table des matières

## Prérequis : installer vim-plug

Avant d'installer un thème, tu as besoin d'un gestionnaire de plugins. [vim-plug](https://github.com/junegunn/vim-plug) est le plus simple :

```bash
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
```

Si tu pars de zéro avec Vim, [commence par le guide d'installation complet](/installation-vim-guide-complet/) avant de revenir ici.

## Installation du thème Catppuccin

Ouvre ton `.vimrc` et ajoute le bloc vim-plug avec le plugin Catppuccin :

```vim
call plug#begin()
Plug 'catppuccin/vim', { 'as': 'catppuccin' }
call plug#end()
```

Sauvegarde, puis lance Vim et exécute :

```vim
:PlugInstall
```

vim-plug télécharge le thème depuis GitHub. Attends la fin de l'installation (quelques secondes).

## Configuration du thème Vim

Une fois le plugin installé, active le thème dans ton `.vimrc` :

```vim
colorscheme catppuccin_mocha
```

Catppuccin propose 4 variantes : `catppuccin_latte` (clair), `catppuccin_frappe`, `catppuccin_macchiato`, `catppuccin_mocha` (sombre). Je reste sur Mocha.

Pour personnaliser les options avant d'activer le thème :

```vim
let g:catppuccin_flavour = "mocha"
let g:catppuccin_transparent_background = 1  " Fond transparent
```

Recharge la config sans quitter Vim :

```vim
:source ~/.vimrc
```

> 💡 **Astuce** — Ajoute `colorscheme catppuccin_mocha` à la fin de ton `.vimrc` pour que le thème se charge automatiquement à chaque ouverture.

## Vérification et dépannage

### Les couleurs ne s'affichent pas correctement

Si tu vois des blocs de couleurs bizarres ou un thème très différent du screenshot, ton terminal ne supporte probablement pas les couleurs 24-bit. Ajoute cette ligne dans ton `.vimrc` **avant** le `colorscheme` :

```vim
set termguicolors
```

Recharge et teste. Si ça ne suffit pas, vérifie que ton terminal supporte les couleurs 256 :

```bash
echo $TERM
# Doit afficher xterm-256color ou screen-256color
```

Si tu te connectes via SSH, [Termius gère les couleurs 24-bit nativement](/termius-client-ssh-windows-guide-complet/). C'est souvent la solution la plus rapide pour ce type de problème.

### Le thème disparaît après redémarrage

Le `colorscheme catppuccin_mocha` doit être dans ton `.vimrc`, pas seulement exécuté en mode commande. Si tu l'avais tapé à la main dans Vim sans l'écrire dans le fichier, c'est ça le problème.

## Installation manuelle (sans vim-plug)

Si tu n'utilises pas de gestionnaire de plugins ou si vim-plug pose des problèmes, installe Catppuccin manuellement :

```bash
git clone https://github.com/catppuccin/vim.git /tmp/catppuccin-vim
mkdir -p ~/.vim/colors
cp /tmp/catppuccin-vim/colors/*.vim ~/.vim/colors/
```

Puis dans ton `.vimrc`, la ligne `colorscheme catppuccin_mocha` suffit : vim-plug n'est plus nécessaire.

> ⚠️ **Attention** — Avec l'installation manuelle, tu ne recevras pas les mises à jour automatiques du thème. Répète le `git clone` + `cp` pour mettre à jour.

## Conclusion

Catppuccin dans Vim, c'est 5 minutes de setup pour des heures d'utilisation agréable. Une fois le thème en place, l'étape suivante est d'harmoniser ton terminal entier : shell, prompt et éditeur avec la même palette. Le [guide Oh My Zsh + Powerlevel10k](/installation-oh-my-zsh-powerlevel10k-guide-complet/) couvre exactement ça.

## Pour aller plus loin

- [Vim : installation, .vimrc et plugins en 30 minutes](/installation-vim-guide-complet/)
- [Oh My Zsh + Powerlevel10k : transforme ton terminal](/installation-oh-my-zsh-powerlevel10k-guide-complet/)
- [Termius : client SSH moderne pour Windows et macOS](/termius-client-ssh-windows-guide-complet/)
