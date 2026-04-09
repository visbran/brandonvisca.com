---
title: "iTerm2 sur macOS : Le guide complet pour dompter votre terminal (2025)"
pubDatetime: "2025-03-31T15:19:31+02:00"
author: Brandon Visca
description: "Transformez votre terminal macOS avec iTerm2 ! Installation, themes, Oh My Zsh, plugins indispensables - Le guide ultime pour booster votre productivité..."
tags:
  - macos
  - developpement
  - intermediaire
  - terminal
  - guide
  - productivite
---

# iTerm2 sur macOS : Le Guide Complet d'Installation et Configuration (2025)

Vous en avez marre du Terminal par défaut de macOS qui manque de fonctionnalités ? iTerm2 est LA solution qui va transformer votre expérience en ligne de commande. Dans ce guide, nous allons voir ensemble comment installer, configurer et optimiser iTerm2 pour booster votre productivité de développeur.

## Qu'est-ce qu'iTerm2 et pourquoi l'adopter ?

iTerm2 est un émulateur de terminal gratuit et open-source spécialement conçu pour macOS. Il remplace avantageusement le Terminal natif d'Apple en apportant des fonctionnalités avancées que tout développeur ou administrateur système devrait avoir dans sa boîte à outils.

### Les avantages clés d'iTerm2

- **Split Panes** : Divisez votre fenêtre en plusieurs panneaux pour travailler simultanément
- **Recherche avancée** : Trouvez instantanément n'importe quel texte dans votre historique
- **Hotkey Window** : Invoquez iTerm2 depuis n'importe où avec un raccourci clavier
- **Thèmes et personnalisation** : Plus de 200 thèmes de couleurs disponibles
- **Session Restoration** : Récupérez automatiquement vos sessions après un redémarrage
- **Badges et annotations** : Ajoutez des informations contextuelles à vos onglets

## Installation d'iTerm2 : 3 méthodes efficaces

### Méthode 1 : Téléchargement direct (Recommandée)

La méthode la plus simple pour installer iTerm2 :

1. Rendez-vous sur [iterm2.com](https://iterm2.com/)
2. Cliquez sur "Download" pour récupérer la dernière version stable
3. Ouvrez le fichier `.zip` téléchargé
4. Glissez l'application iTerm2 dans votre dossier Applications
5. Lancez iTerm2 depuis le Launchpad ou Spotlight

### Méthode 2 : Installation via Homebrew

Pour les adeptes de Homebrew (gestionnaire de paquets pour macOS), voici la commande :

```bash
# Installation de iTerm2 via Homebrew Cask
brew install --cask iterm2
```

**Note** : Homebrew est un gestionnaire de paquets qui simplifie l'installation de logiciels sur macOS via la ligne de commande.

### Méthode 3 : Version beta (pour les early adopters)

Si vous voulez tester les dernières fonctionnalités :

```bash
# Installation de la version beta
brew install --cask iterm2-beta
```

## Configuration initiale : Les réglages essentiels

### Paramètres généraux

Après l'installation, accédez aux préférences avec `Cmd + ,` et configurez ces éléments :

**Onglet General :**

- **Startup** : Cochez "Use System Window Restoration Setting"
- **Closing** : Décochez "Confirm closing multiple sessions" si vous trouvez cela agaçant
- **Magic** : Activez "Save copy/paste and command history to disk"

### Configuration des profils

Les profils dans iTerm2 permettent de créer différentes configurations pour différents usages (développement local, connexions SSH, etc.).

**Création d'un profil personnalisé :**

1. Allez dans `Preferences > Profiles`
2. Cliquez sur le `+` pour créer un nouveau profil
3. Nommez votre profil (ex: "Dev Local", "Production SSH")
4. Configurez les paramètres spécifiques

### Optimisation des couleurs et police

**Choix de la police :**

- **Police recommandée** : "Fira Code" ou "JetBrains Mono" (supportent les ligatures)
- **Taille** : 14pt minimum pour un confort optimal
- **Ligatures** : Activez-les si votre police les supporte

```bash
# Installation de Fira Code via Homebrew
brew tap homebrew/cask-fonts
brew install --cask font-fira-code
```

**Thèmes de couleurs populaires :**

|Thème|Usage|Avantages|
|---|---|---|
|One Dark|Développement|Faible fatigue oculaire|
|Solarized Dark|Travail prolongé|Scientifiquement optimisé|
|Dracula|Polyvalent|Très populaire, bien contrasté|
|Gruvbox|Vintage|Couleurs chaudes et agréables|

## Fonctionnalités avancées : Maximisez votre productivité

### Split Panes : Multipliez vos espaces de travail

Les split panes permettent de diviser votre fenêtre en plusieurs panneaux :

- **Division verticale** : `Cmd + D`
- **Division horizontale** : `Cmd + Shift + D`
- **Navigation entre panneaux** : `Cmd + Option + flèches`
- **Fermeture d'un panneau** : `Cmd + W`

### Hotkey Window : Accès instantané

Configurez une fenêtre iTerm2 accessible globalement :

1. `Preferences > Keys > Hotkey`
2. Cochez "Create a Dedicated Hotkey Window"
3. Définissez votre raccourci (ex: `Option + Space`)
4. Choisissez l'animation (recommandé : "Slide in from top")

### Search et Navigation

iTerm2 offre des capacités de recherche exceptionnelles :

- **Recherche** : `Cmd + F`
- **Recherche avec regex** : Activez "Regular Expression" dans la barre de recherche
- **Recherche dans l'historique** : `Cmd + Shift + H`

### Automatic Profile Switching

Changez automatiquement de profil selon le contexte :

```bash
# Exemple : changement automatique pour les connexions SSH
echo -e "\033]50;SetProfile=SSH Profile\a"
```

## Raccourcis clavier essentiels

Maîtrisez ces raccourcis pour une efficacité maximale :

|Raccourci|Action|
|---|---|
|`Cmd + T`|Nouvel onglet|
|`Cmd + W`|Fermer onglet/panneau|
|`Cmd + 1-9`|Basculer entre onglets|
|`Cmd + F`|Rechercher|
|`Cmd + R`|Effacer l'écran|
|`Cmd + K`|Effacer le buffer|
|`Cmd + ;`|Autocomplétion|
|`Cmd + Shift + H`|Historique des presse-papiers|

## Intégrations et plugins recommandés

### Oh My Zsh : Sublimez votre shell

Oh My Zsh est un framework qui améliore considérablement l'expérience Zsh :

```bash
# Installation d'Oh My Zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

**Plugins recommandés pour Oh My Zsh :**

- `git` : Raccourcis Git pratiques
- `zsh-autosuggestions` : Suggestions basées sur l'historique
- `zsh-syntax-highlighting` : Coloration syntaxique en temps réel

### Powerlevel10k : Un prompt surpuissant

```bash
# Installation de Powerlevel10k
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k
echo 'source ~/powerlevel10k/powerlevel10k.zsh-theme' >>~/.zshrc
```

## Dépannage et problèmes courants

### iTerm2 ne se lance pas

**Solutions :**

1. Vérifiez les permissions dans `Sécurité et confidentialité`
2. Réinstallez depuis le site officiel
3. Videz le cache : `rm -rf ~/Library/Preferences/com.googlecode.iterm2.plist`

### Problèmes de police

Si les caractères s'affichent mal :

1. Installez les polices dans `Font Book`
2. Redémarrez iTerm2
3. Vérifiez que la police supporte les caractères UTF-8

### Performance lente

**Optimisations :**

- Réduisez la taille du buffer de défilement
- Désactivez la transparence si activée
- Fermez les onglets/panneaux inutilisés

## FAQ : Questions fréquentes

### iTerm2 est-il gratuit ?

Oui, iTerm2 est complètement gratuit et open-source. Aucune limitation ou version premium.

### Puis-je utiliser iTerm2 avec Fish ou Bash ?

Absolument ! iTerm2 fonctionne avec tous les shells : Zsh, Bash, Fish, etc. Il s'agit d'un émulateur de terminal, pas d'un shell.

### Comment sauvegarder ma configuration iTerm2 ?

Allez dans `Preferences > General > Preferences` et cliquez sur "Save Current Settings to Folder". Vous pouvez ensuite versionner ce dossier avec Git.

### iTerm2 ralentit-il mon Mac ?

Non, iTerm2 est optimisé et consomme généralement moins de ressources que le Terminal par défaut de macOS, surtout avec de gros volumes de texte.

### Puis-je synchroniser mes réglages entre plusieurs Macs ?

Oui, en sauvegardant vos préférences dans un service cloud (Dropbox, iCloud, etc.) et en les important sur vos autres machines.

## Résumé : Votre terminal transformé

iTerm2 transforme radicalement l'expérience terminal sur macOS. Avec ses split panes, sa hotkey window, ses thèmes personnalisables et ses intégrations avancées, vous gagnerez un temps précieux au quotidien.

Les points clés à retenir :

- **Installation simple** via le site officiel ou Homebrew
- **Configuration progressive** selon vos besoins spécifiques
- **Raccourcis clavier** pour une navigation ultra-rapide
- **Intégrations** avec Oh My Zsh et Powerlevel10k pour un workflow optimal

**Prêt à franchir le cap ?** Téléchargez iTerm2 dès maintenant et découvrez pourquoi des millions de développeurs ont abandonné le Terminal par défaut. Votre productivité vous remerciera !

_Vous avez des questions sur iTerm2 ou des configurations spécifiques ? Partagez votre expérience en commentaires ci-dessous._
