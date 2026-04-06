---
title: "Installation d'un thème sous Vim : Guide complet"
pubDatetime: "2025-03-31T15:43:24+02:00"
description: "Nous allons voir comment installer et configurer un thème dans vim, en prenant comme exemple le populaire thème Catppuccin."
tags:
  - linux
  - macos
  - developpement
  - guide
  - debutant
  - vim
---

-----------
## Table des matières


- [2. Installation du thème Catppuccin](#2-installation-du-theme-catppuccin)
- [3. Configuration du thème](#3-configuration-du-theme)
- [4. Vérification et dépannage](#4-verification-et-depannage)
- [5. Installation manuelle des fichiers de thème](#5-installation-manuelle-des-fichiers-de-theme)
- [Sources](#sources)


1. Prérequis
------------

Avant de commencer l’installation d’un thème, nous devons d’abord installer un gestionnaire de plugins. Vim-plug est l’un des plus populaires et des plus simples à utiliser.

```bash
curl -fLo ~/.vim/autoload/plug.vim --create-dirs 
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
```

call plug#begin()
Plug 'catppuccin/vim', { 'as': 'catppuccin' }
call plug#end()

Ensuite, lancez Vim et exécutez la commande :

```bash
:PlugInstall
```

colorscheme catppuccin_mocha

Si vous souhaitez personnaliser les couleurs, vous pouvez modifier certaines variables avant d’activer le thème :

```bash
let g:catppuccin_flavour = "mocha"
let g:catppuccin_transparent_background = 1  " Pour un fond transparent
```

:source ~/.vimrc

Problèmes courants et solutions :

- Si les couleurs ne s’affichent pas correctement, vérifiez que votre terminal supporte les couleurs 256 :

```bash
set termguicolors
```

git clone https://github.com/catppuccin/vim.git
mkdir -p ~/.vim/colors
cp vim/colors/*.vim ~/.vim/colors/

Cette méthode permet d’avoir un contrôle direct sur les fichiers de thème et peut être utile en cas de problème avec vim-plug.

Sources
-------

- [Documentation officielle de vim-plug](https://github.com/junegunn/vim-plug)
- [Documentation du thème Catppuccin pour Vim](https://github.com/catppuccin/vim)
- [Documentation officielle de Vim](https://www.vim.org/docs.php)
