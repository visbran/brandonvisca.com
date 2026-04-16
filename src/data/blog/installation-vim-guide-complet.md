---
title: "Vim sur macOS et Linux : installation, .vimrc et plugins en 30 minutes"
description: "Installe Vim sur macOS ou Linux en 30 min : .vimrc de base commenté, vim-plug, NERDTree et FZF. Tout ce qu'il faut pour débuter sérieusement."
pubDatetime: "2025-03-31T15:11:44+02:00"
modDatetime: 2026-04-16 00:00:00+01:00
author: Brandon Visca
tags:
  - vim
  - linux
  - macos
  - cli
  - guide
  - intermediaire
featured: false
draft: false
focusKeyword: vim
---
> 💡 **TL;DR** — Vim est disponible sur macOS via Homebrew (`brew install vim`) et sur Linux via le gestionnaire de paquets natif. Un `.vimrc` de 15 lignes suffit pour un éditeur fonctionnel. Ajoute vim-plug pour les plugins, NERDTree pour l'arbre de fichiers, FZF pour la recherche.

Vim intimide au premier abord. Mais une fois qu'on comprend la logique modale, c'est l'un des éditeurs les plus rapides qui soit. Je l'utilise quotidiennement sur mes serveurs Linux, et le `.vimrc` que je vais te montrer est exactement celui que je déploie partout.

## Table des matières

## Installation de Vim sur macOS

![vim, éditeur de texte|460](61d13605-e6bf-4767-a046-14fd78358c39.jpg)

### Via Homebrew

Homebrew est le gestionnaire de paquets de référence sur macOS. Si tu ne l'as pas encore, installe-le d'abord :

```bash
# Installation de Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Installation de Vim
brew install vim
```

Le `brew install vim` installe la v9.x, plus récente que la v8.x préinstallée sur macOS. Vérifie la version :

```bash
vim --version | head -1
```

### Installation depuis les sources

Si tu veux la toute dernière version ou des options de compilation personnalisées :

```bash
git clone https://github.com/vim/vim.git
cd vim
./configure --with-features=huge --enable-python3interp
make
sudo make install
```

> ⚠️ **Attention** — La compilation depuis les sources nécessite `gcc`, `make` et les headers Python3. Sur macOS : `xcode-select --install`. Sur Debian/Ubuntu : `sudo apt install build-essential python3-dev`.

## Installation de Vim sur Linux

Sur les distributions les plus courantes, Vim est dans les dépôts officiels :

```bash
# Debian / Ubuntu
sudo apt update && sudo apt install vim

# Fedora / RHEL
sudo dnf install vim

# Arch Linux
sudo pacman -S vim
```

Pour la version complète avec toutes les fonctionnalités (clipboard système, Python, etc.) :

```bash
# Ubuntu/Debian
sudo apt install vim-gtk3
```

## Configuration de base avec .vimrc

### Créer le fichier .vimrc

Le `.vimrc` est le fichier de config principal de l'éditeur. Il se charge à chaque démarrage :

```bash
touch ~/.vimrc
vim ~/.vimrc
```

### Paramètres essentiels commentés

Voici la config minimale que j'utilise sur tous mes serveurs :

```vim
" Numérotation des lignes
set number
set relativenumber

" Coloration syntaxique
syntax enable
syntax on

" Indentation intelligente
set autoindent
set smartindent
set tabstop=4
set shiftwidth=4
set expandtab          " Espaces au lieu de tabulations

" Encodage et affichage
set encoding=utf-8
set cursorline          " Surligne la ligne courante
set showmatch           " Montre les parenthèses correspondantes
set hlsearch            " Surligne les résultats de recherche
set incsearch           " Recherche incrémentale en temps réel

" Performance
set lazyredraw          " Accélère le rendu lors des macros
```

Enregistre et recharge sans quitter Vim :

```vim
:source ~/.vimrc
```

> 💡 **Astuce** — Ajoute `set clipboard=unnamedplus` à ton `.vimrc` pour synchroniser le presse-papiers Vim avec le presse-papiers système. Plus de `Ctrl+C` / `Ctrl+V` manqués.

## Personnalisation avancée avec vim-plug

### Installation de vim-plug

[vim-plug](https://github.com/junegunn/vim-plug) est le gestionnaire de plugins le plus simple et fiable :

```bash
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
```

### Plugins recommandés

Ajoute ce bloc dans ton `.vimrc` **avant** les autres paramètres :

```vim
call plug#begin('~/.vim/plugged')

" NERDTree — explorateur de fichiers latéral
Plug 'preservim/nerdtree'

" Airline — barre de statut améliorée
Plug 'vim-airline/vim-airline'

" Auto-pairs — fermeture automatique des parenthèses/guillemets
Plug 'jiangmiao/auto-pairs'

" FZF — recherche floue ultra-rapide
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'

call plug#end()
```

Puis installe les plugins depuis Vim :

```vim
:PlugInstall
```

### Raccourcis clavier personnalisés

```vim
" Touche leader = virgule (plus accessible que la barre oblique)
let mapleader = ","

" Ouvrir/fermer NERDTree
nnoremap <leader>n :NERDTreeToggle<CR>

" Navigation entre fenêtres splitées avec Ctrl+hjkl
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" Sauvegarder avec Ctrl+S (comme les autres éditeurs)
nnoremap <C-s> :w<CR>
inoremap <C-s> <Esc>:w<CR>a
```

Pour personnaliser le thème visuel, jette un œil à [mon guide d'installation de thèmes Vim](/installation-theme-vim-guide/). Ça change vraiment l'expérience.

## Dépannage courant

### Problèmes de permissions

Si l'éditeur se plaint de droits manquants sur `.vim/` ou `.vimrc` :

```bash
# Vérifier les permissions actuelles
ls -la ~/.vim
ls -la ~/.vimrc

# Corriger si nécessaire
chmod 644 ~/.vimrc
chmod -R u+rw ~/.vim
```

### Conflits de configuration

Si un plugin casse l'éditeur au démarrage, lance-le sans config pour isoler le problème :

```bash
vim -u NONE    # Vim sans .vimrc ni plugins
vim -u ~/.vimrc --noplugin   # .vimrc mais sans plugins
```

Ensuite :
- Commente progressivement les `Plug '...'` dans ton `.vimrc` pour identifier le plugin fautif
- Vérifie la compatibilité des plugins entre eux (certains entrent en conflit sur les mappings)
- Consulte les issues GitHub du plugin concerné

Si tu veux aller plus loin dans l'optimisation de ton terminal, regarde aussi [Oh My Zsh + Powerlevel10k](/installation-oh-my-zsh-powerlevel10k-guide-complet/). Vim + un shell propre, c'est imbattable.

## Conclusion

Vim a une courbe d'apprentissage abrupte les premiers jours. Mais une fois que tu as ton `.vimrc` calibré et tes plugins installés, tu réalises pourquoi les sysadmins y reviennent toujours : il est disponible partout, démarre en une seconde, et ne t'impose rien.

Commence par les bases : `hjkl` pour naviguer, `i` pour insérer, `:w` pour sauvegarder, `:q` pour quitter. Le reste vient naturellement. Et si tu veux pousser la personnalisation visuelle, le [guide thèmes dédié](/installation-theme-vim-guide/) est l'étape suivante logique.

## Pour aller plus loin

- [Installer un thème sous Vim : guide complet](/installation-theme-vim-guide/)
- [Oh My Zsh + Powerlevel10k : transforme ton terminal](/installation-oh-my-zsh-powerlevel10k-guide-complet/)
- [Termius : client SSH moderne pour Windows et macOS](/termius-client-ssh-windows-guide-complet/)
