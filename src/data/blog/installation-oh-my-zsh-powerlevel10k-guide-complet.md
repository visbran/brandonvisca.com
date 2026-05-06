---
title: "Oh My Zsh + Powerlevel10k : guide complet installation 2026"
description: "Oh My Zsh + Powerlevel10k 2026 : installe et configure ton terminal en 15 min. Plugins indispensables, thèmes pro, config avancée."
pubDatetime: 2025-03-31 15:55:32+02:00
modDatetime: 2026-05-06 00:00:00+01:00
author: Brandon Visca
tags:
  - oh-my-zsh
  - powerlevel10k
  - zsh
  - macos
  - productivite
  - intermediaire
featured: false
draft: false
focusKeyword: Oh My Zsh
faqs:
  - question: "Oh My Zsh fonctionne-t-il sur Linux ?"
    answer: "Oui. Oh My Zsh fonctionne sur macOS, Linux et WSL. La procédure d'installation est identique — curl ou wget, même commande."
  - question: "Powerlevel10k ralentit-il le terminal ?"
    answer: "Non, c'est l'inverse. Powerlevel10k est 10 à 100x plus rapide que les thèmes classiques grâce à son rendu asynchrone. Il ne bloque jamais le prompt."
  - question: "Comment désinstaller Oh My Zsh ?"
    answer: "Lance uninstall_oh_my_zsh dans ton terminal. La commande restaure ta configuration Zsh précédente automatiquement."
  - question: "Puis-je utiliser Oh My Zsh avec Fish ou Bash ?"
    answer: "Non. Oh My Zsh est un framework pour Zsh uniquement. Pour Fish, l'équivalent est Oh My Fish (omf)."
---
> 💡 **TL;DR**
> - Oh My Zsh transforme Zsh en cockpit de dev : autocomplétion intelligente, 300+ plugins, thèmes en quelques minutes
> - Installe-le en une commande `curl`, configure Powerlevel10k via wizard interactif
> - Résultat : un terminal rapide, informatif et personnalisé, en moins de 15 minutes

T'en as marre de ton terminal terne et basique ? Oh My Zsh + Powerlevel10k, c'est la combinaison qui change tout. En 15 minutes, tu passes d'un terminal par défaut à un cockpit de développeur que tes collègues vont envier.

Voici le guide complet : installation, configuration, plugins et personnalisation avancée.

Sur macOS, j'utilise tout ça dans [iTerm2](https://brandonvisca.com/iterm2-guide-configuration-macos-2025/), le combo parfait. Si tu hésites entre les terminaux, j'ai fait un [test iTerm2 vs Warp](https://brandonvisca.com/warp-terminal-2025-iterm2-killer-ou-simple-hype-test-complet-ia/) après 60 jours.

## Table des matières

## Prérequis : ce qu'il te faut avant de commencer

### Installation de Zsh

Avant de plonger dans Oh My Zsh, assure-toi d'avoir Zsh installé :

**Ubuntu/Debian :**

```bash
sudo apt update && sudo apt install zsh
```

**macOS (via [Homebrew](https://brandonvisca.com/installation-homebrew-macos/)) :**

```bash
brew install zsh
```

**CentOS/RHEL/Fedora :**

```bash
# CentOS/RHEL
sudo yum install zsh
# Fedora
sudo dnf install zsh
```

Vérifie l'installation :

```bash
zsh --version
# Devrait afficher : zsh 5.9 ou supérieur
```

### Installation de Git

Git est indispensable pour Oh My Zsh :

```bash
# Ubuntu/Debian
sudo apt install git

# macOS — déjà installé normalement
git --version
# Ou avec Homebrew : brew install git

# CentOS/RHEL
sudo yum install git
```

💡 **Astuce** : sur macOS, si Git n'est pas installé, la commande `git --version` déclenche automatiquement l'installation des Xcode Command Line Tools. Accepte et continue.

Bascule vers zsh si ce n'est pas encore ton shell par défaut :

```bash
source ~/.bashrc
exec zsh
```

## Installation de Oh My Zsh

### Méthode recommandée (curl)

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

**Ce qui se passe :**

1. Le script télécharge Oh My Zsh dans `~/.oh-my-zsh`
2. Sauvegarde ton `.zshrc` existant en `.zshrc.pre-oh-my-zsh`
3. Crée un nouveau `.zshrc` avec la config par défaut
4. Change ton shell par défaut vers zsh

### Méthode alternative (wget)

```bash
sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

✅ **À savoir** : l'installation te demandera si tu veux faire de zsh ton shell par défaut. Réponds « Y » sauf si tu as une bonne raison de ne pas le faire.

## Configuration de base

### Le fichier de configuration

Tout se passe dans `~/.zshrc`. Ouvre-le avec ton éditeur préféré :

```bash
nano ~/.zshrc
# ou
vim ~/.zshrc
# ou
code ~/.zshrc  # VS Code
```

La structure de base générée par Oh My Zsh :

```bash
# Chemin vers Oh My Zsh
export ZSH="$HOME/.oh-my-zsh"

# Thème (on va changer ça bientôt)
ZSH_THEME="robbyrussell"

# Plugins activés
plugins=(git)

# Source Oh My Zsh
source $ZSH/oh-my-zsh.sh

# Tes alias et configurations perso ici
```

### Premiers réglages utiles

Ajoute ces lignes à la fin de ton `.zshrc` :

```bash
# Historique plus long et intelligent
HISTSIZE=10000
SAVEHIST=10000
setopt HIST_VERIFY
setopt SHARE_HISTORY
setopt APPEND_HISTORY

# Navigation plus fluide
setopt AUTO_CD
setopt CORRECT
setopt CORRECT_ALL

# Autocomplétion case-insensitive
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}'
```

Recharge la config :

```bash
source ~/.zshrc
```

## Powerlevel10k : le thème qui tue tout

Oublie les thèmes basiques. **Powerlevel10k** (P10k pour les intimes) transforme ton terminal en vaisseau spatial.

### Pourquoi Powerlevel10k ?

- ⚡ **Ultra-rapide** : 10-100x plus rapide que les autres thèmes (rendu asynchrone)
- 🎨 **Magnifique** : icons, couleurs, informations utiles d'un coup d'œil
- 🔧 **Configurable** : wizard interactif pour tout personnaliser en 5 minutes
- 📊 **Informatif** : Git status, temps d'exécution, erreurs en temps réel

### Installation de Powerlevel10k

```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```

Dans ton `.zshrc`, change le thème :

```bash
# Remplace :
ZSH_THEME="robbyrussell"

# Par :
ZSH_THEME="powerlevel10k/powerlevel10k"
```

Recharge :

```bash
source ~/.zshrc
```

Lance le wizard de configuration :

```bash
p10k configure
```

**Mes recommandations pour le wizard :**

1. **Font icons** : réponds « Y » si tu vois les icônes correctement
2. **Prompt style** : « Rainbow » (option 3)
3. **Character set** : « Unicode »
4. **Show current time** : « 24-hour format »
5. **Prompt separators** : « Angled »
6. **Prompt heads** : « Sharp »
7. **Prompt tails** : « Flat »
8. **Prompt height** : « Two lines »
9. **Prompt spacing** : « Sparse »
10. **Icons** : « Many icons »
11. **Prompt flow** : « Concise »
12. **Transient prompt** : « Yes »

### Installation des polices Nerd Font

Pour que les icônes s'affichent correctement dans le terminal :

**macOS :** le wizard propose l'installation automatique. Accepte !

**Linux :**

```bash
# Téléchargement des polices recommandées
mkdir -p ~/.local/share/fonts
cd ~/.local/share/fonts

# MesloLGS NF (recommandée par Powerlevel10k)
wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf
wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf
wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Italic.ttf
wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold%20Italic.ttf

# Refresh du cache des polices
fc-cache -fv
```

Relance ensuite le wizard :

```bash
p10k configure
```

⚠️ **Prompt lent :** si ton prompt met plus d'une seconde à apparaître, trop de segments sont activés. Ouvre `~/.p10k.zsh` et commente les segments lourds comme `disk_usage`.

## Plugins essentiels

Oh My Zsh, c'est **300+ plugins** prêts à l'emploi. Voici ma sélection de ceux qui changent vraiment la vie.

### Ma config plugins de base

Dans ton `.zshrc`, remplace la ligne `plugins=(git)` par :

```bash
plugins=(
  git
  docker
  docker-compose
  node
  npm
  yarn
  python
  pip
  sudo
  history
  colored-man-pages
  command-not-found
  extract
  web-search
)
```

### Plugins communautaires indispensables

**zsh-autosuggestions** (suggestions basées sur ton historique) :

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

**zsh-syntax-highlighting** (coloration syntaxique en temps réel) :

```bash
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

Active-les dans `.zshrc` — `zsh-syntax-highlighting` toujours en dernier :

```bash
plugins=(
  git
  docker
  zsh-autosuggestions
  zsh-syntax-highlighting  # TOUJOURS en dernier !
)
```

### Plugins par cas d'usage

**Développement web :**

```bash
plugins=(git node npm yarn web-search)
```

**Sysadmin / DevOps :**

```bash
plugins=(git docker ssh-agent systemd ansible)
```

**Python :**

```bash
plugins=(git python pip virtualenv)
```

### Alias magiques

Ajoute ces alias dans ton `.zshrc` :

```bash
# Navigation rapide
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'

# Git shortcuts
alias gs='git status'
alias gd='git diff'
alias gl='git log --oneline --graph'

# Docker shortcuts
alias dps='docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'
alias dlog='docker logs -f'

# Système
alias h='history'
alias c='clear'
alias reload='source ~/.zshrc'

# Recherche avec couleurs
alias grep='grep --color=auto'
```

## Configuration avancée

### Fonctions utiles

```bash
# Création rapide de dossier + navigation
mkcd() {
  mkdir -p "$1" && cd "$1"
}

# Backup rapide d'un fichier
backup() {
  cp "$1" "$1.backup.$(date +%Y%m%d-%H%M%S)"
}

# Recherche dans l'historique
hist() {
  history | grep "$1"
}

# IP publique
myip() {
  curl -s https://ipinfo.io/ip
}
```

### Variables d'environnement

```bash
# Éditeur par défaut
export EDITOR='nano'  # ou vim, code...

# Langues
export LANG=fr_FR.UTF-8
export LC_ALL=fr_FR.UTF-8

# Paths personnalisés
export PATH="$HOME/bin:$PATH"
export PATH="/usr/local/bin:$PATH"
```

### Configuration Powerlevel10k avancée

Le fichier `~/.p10k.zsh` contient toute la config. Quelques tweaks sympas :

```bash
# Ouvre le fichier
nano ~/.p10k.zsh

# Personnalise les segments du prompt gauche/droit :
typeset -g POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(
  dir                     # Dossier actuel
  vcs                     # Git status
  prompt_char             # Caractère de prompt
)

typeset -g POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(
  status                  # Code de retour
  command_execution_time  # Temps d'exécution
  background_jobs         # Jobs en arrière-plan
  time                    # Heure
)
```

💡 **Astuce** : le fichier `~/.p10k.zsh` est très bien documenté. Chaque segment a un commentaire. Prends 15 minutes pour le parcourir — tu trouveras des options insoupçonnées.

## Maintenance et dépannage

### Mise à jour

**Oh My Zsh :**

```bash
omz update
```

**Powerlevel10k :**

```bash
git -C ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k pull
```

**Plugins communautaires :**

```bash
# Exemple pour zsh-autosuggestions
git -C ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions pull
```

### Problèmes courants

**Prompt qui se charge lentement :**

```bash
# Debug des temps de chargement
time zsh -i -c exit

# Si > 1 seconde, relance le wizard
p10k configure
# Désactive les segments lourds
```

**Fichier de complétion corrompu :**

```bash
rm ~/.zcompdump*
exec zsh
```

**Plugin qui ne marche pas :**

```bash
# Vérifie qu'il est dans la liste
echo $plugins

# Recharge la config
source ~/.zshrc

# Vérifie les erreurs
zsh -x ~/.zshrc
```

**Problème Git safe.directory :**

```bash
git config --global --add safe.directory /ton/repo
```

### Sauvegarde de ta config

```bash
# Backup du setup complet
tar -czf oh-my-zsh-backup.tar.gz ~/.zshrc ~/.p10k.zsh ~/.oh-my-zsh/custom/

# Restauration
tar -xzf oh-my-zsh-backup.tar.gz -C ~/
```

### Désinstallation

```bash
uninstall_oh_my_zsh
```

## Conclusion

Oh My Zsh + Powerlevel10k, c'est le combo que tu installes une fois et que tu gardes sur tous tes Macs et serveurs. En 15 minutes, ton terminal passe de "fonctionnel" à "je veux l'ouvrir tout le temps".

Si tu pars de zéro sur macOS, enchaîne avec iTerm2 : j'ai tout détaillé dans le [guide iTerm2 macOS complet](https://brandonvisca.com/iterm2-guide-configuration-macos-2025/) — configuration Hotkey Window, profils SSH et thèmes inclus.

## Pour aller plus loin

- [Guide iTerm2 macOS complet](https://brandonvisca.com/iterm2-guide-configuration-macos-2025/) : le terminal qui sublimera ce setup
- [Installer Homebrew sur macOS](https://brandonvisca.com/installation-homebrew-macos/) : prérequis indispensable sur Mac
- [Documentation officielle Oh My Zsh](https://github.com/ohmyzsh/ohmyzsh/wiki) : wiki complet avec tous les plugins
- [Powerlevel10k GitHub](https://github.com/romkatv/powerlevel10k) : config avancée et options cachées
