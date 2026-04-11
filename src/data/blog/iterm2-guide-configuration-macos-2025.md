---
title: "Guide iTerm2 macOS : Installation et configuration complète (2026)"
description: "Guide iTerm2 macOS : installation, thèmes, raccourcis, Oh My Zsh et plugins essentiels. Tout ce qu'il faut pour booster ta productivité terminal."
pubDatetime: 2025-03-31 15:19:31+02:00
modDatetime: 2026-04-11 00:00:00+02:00
author: Brandon Visca
tags:
  - macos
  - productivite
  - iterm2
  - terminal
  - intermediaire
  - guide
featured: false
draft: false
focusKeyword: iTerm2 macOS
faqs:
  - question: "iTerm2 est-il gratuit ?"
    answer: "Oui, iTerm2 est complètement gratuit et open-source. Aucune limitation ni version premium."
  - question: "Puis-je utiliser iTerm2 avec Fish ou Bash ?"
    answer: "Absolument. iTerm2 fonctionne avec tous les shells : Zsh, Bash, Fish, etc. C'est un émulateur de terminal, pas un shell."
  - question: "Comment sauvegarder ma configuration iTerm2 ?"
    answer: "Va dans Preferences > General > Preferences et clique sur Save Current Settings to Folder. Tu peux ensuite versionner ce dossier avec Git pour le synchroniser entre machines."
  - question: "iTerm2 ralentit-il mon Mac ?"
    answer: "Non. iTerm2 est optimisé et consomme généralement moins de ressources que le Terminal par défaut de macOS, surtout avec de gros volumes de texte."
  - question: "Puis-je synchroniser mes réglages iTerm2 entre plusieurs Macs ?"
    answer: "Oui. Sauvegarde tes préférences dans un dossier versionné avec Git, ou pointe vers un dossier Dropbox/iCloud dans Preferences > General > Preferences."
---
T'en as marre du Terminal macOS qui ressemble à une interface sortie des années 90 ? Même ressenti. iTerm2 règle ça en 5 minutes, et une fois configuré correctement, tu ne regardes plus jamais en arrière.

Voici tout ce qu'il faut savoir pour l'installer, le configurer et en tirer le maximum.

## Table des matières

## Qu'est-ce qu'iTerm2 et pourquoi l'adopter ?

iTerm2 est un émulateur de terminal gratuit et open-source conçu exclusivement pour macOS. Il remplace le Terminal natif d'Apple avec des fonctionnalités que tout dev ou admin sys utilise au quotidien.

### Les avantages clés d'iTerm2

- **Split Panes** : divise ta fenêtre en plusieurs panneaux pour travailler en parallèle
- **Recherche avancée** : trouve instantanément n'importe quel texte dans ton historique
- **Hotkey Window** : invoque iTerm2 depuis n'importe où avec un raccourci global
- **Thèmes et personnalisation** : plus de 200 thèmes de couleurs disponibles
- **Session Restoration** : récupère automatiquement tes sessions après un redémarrage
- **Badges et annotations** : ajoute des informations contextuelles à tes onglets

## Installation d'iTerm2 : 3 méthodes

### Méthode 1 : Téléchargement direct (recommandée)

1. Va sur [iterm2.com](https://iterm2.com/)
2. Clique sur "Download" pour récupérer la dernière version stable
3. Ouvre le fichier `.zip` téléchargé
4. Glisse l'application iTerm2 dans ton dossier Applications
5. Lance iTerm2 depuis le Launchpad ou Spotlight

### Méthode 2 : Installation via Homebrew

Si tu utilises [Homebrew](https://brandonvisca.com/installation-homebrew-macos/), une seule commande suffit :

```bash
brew install --cask iterm2
```

✅ **Bonne pratique** : installe iTerm2 via Homebrew si tu gères déjà tes apps avec Cask. Mise à jour, désinstallation et réinstallation se font en une ligne.

### Méthode 3 : Version beta

Si tu veux tester les dernières fonctionnalités avant tout le monde :

```bash
brew install --cask iterm2-beta
```

⚠️ **Attention** : la beta peut introduire des régressions. Garde-la sur une machine secondaire ou un profil de test.

## Configuration initiale : les réglages essentiels

### Paramètres généraux

Après l'installation, ouvre les préférences avec `Cmd + ,` et configure ces points :

**Onglet General :**

- **Startup** : coche "Use System Window Restoration Setting"
- **Closing** : décoche "Confirm closing multiple sessions" si tu trouves ça agaçant
- **Magic** : active "Save copy/paste and command history to disk"

💡 **Astuce** : active "Load preferences from a custom folder or URL" pour pointer vers ton dossier de config versionné avec Git. Tu récupères ta config en 30 secondes sur n'importe quel Mac.

### Configuration des profils

Les profils permettent de créer des configurations distinctes selon l'usage : dev local, connexions SSH, serveur de prod, etc.

**Création d'un profil :**

1. Va dans `Preferences > Profiles`
2. Clique sur le `+` pour créer un nouveau profil
3. Nomme ton profil (ex: "Dev Local", "Production SSH")
4. Configure les paramètres spécifiques à cet usage

### Couleurs et police

**Police recommandée :** "Fira Code" ou "JetBrains Mono" (supportent les ligatures de code).

```bash
# Installation de Fira Code via Homebrew
brew tap homebrew/cask-fonts
brew install --cask font-fira-code
```

- **Taille** : 14pt minimum pour un confort optimal
- **Ligatures** : active-les si ta police les supporte (`->` devient `→`, etc.)

**Thèmes de couleurs populaires :**

| Thème | Usage | Avantage |
|---|---|---|
| One Dark | Développement | Faible fatigue oculaire |
| Solarized Dark | Travail prolongé | Contraste calibré scientifiquement |
| Dracula | Polyvalent | Très populaire, bien contrasté |
| Gruvbox | Vintage | Couleurs chaudes, très lisible |

💡 **Astuce** : télécharge les thèmes depuis [iterm2colorschemes.com](https://iterm2colorschemes.com/). Import direct dans `Preferences > Profiles > Colors > Color Presets`.

## Fonctionnalités avancées : tire le maximum d'iTerm2

### Split Panes : plusieurs terminaux dans une fenêtre

Les split panes divisent ta fenêtre sans ouvrir de nouvel onglet :

- **Division verticale** : `Cmd + D`
- **Division horizontale** : `Cmd + Shift + D`
- **Navigation entre panneaux** : `Cmd + Option + flèches`
- **Fermeture d'un panneau** : `Cmd + W`

✅ **Bonne pratique** : utilise un panneau pour ton éditeur, un autre pour les logs, un troisième pour Git. Plus besoin de basculer entre fenêtres.

### Hotkey Window : accès instantané depuis n'importe où

C'est la fonctionnalité qui change tout. Configure une fenêtre iTerm2 accessible globalement :

1. `Preferences > Keys > Hotkey`
2. Coche "Create a Dedicated Hotkey Window"
3. Définis ton raccourci (ex: `Option + Space`)
4. Choisis l'animation (recommandé : "Slide in from top")

La fenêtre s'affiche par-dessus n'importe quelle app. Un raccourci, et tu es dans ton terminal.

### Recherche et navigation

iTerm2 a une recherche bien plus puissante que le Terminal natif :

- **Recherche** : `Cmd + F`
- **Regex** : active "Regular Expression" dans la barre de recherche
- **Historique du presse-papiers** : `Cmd + Shift + H`

### Automatic Profile Switching

Change automatiquement de profil selon le contexte (utile pour les connexions SSH qui utilisent un profil avec fond rouge pour signaler l'environnement de prod) :

```bash
# Exemple : changement automatique pour les connexions SSH
echo -e "\033]50;SetProfile=SSH Profile\a"
```

## Raccourcis clavier essentiels

| Raccourci | Action |
|---|---|
| `Cmd + T` | Nouvel onglet |
| `Cmd + W` | Fermer onglet/panneau |
| `Cmd + 1-9` | Basculer entre onglets |
| `Cmd + F` | Rechercher |
| `Cmd + R` | Effacer l'écran |
| `Cmd + K` | Effacer le buffer |
| `Cmd + ;` | Autocomplétion |
| `Cmd + Shift + H` | Historique des presse-papiers |

## Intégrations recommandées

### Oh My Zsh : transforme ton shell

Oh My Zsh est le framework qui rend Zsh vraiment utilisable. Si tu ne l'as pas encore, c'est la priorité. J'ai un [guide complet Oh My Zsh + Powerlevel10k](https://brandonvisca.com/installation-oh-my-zsh-powerlevel10k-guide-complet/) si tu pars de zéro.

```bash
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

**Plugins à activer dans `.zshrc` :**

- `git` : alias Git pratiques (`gst`, `gco`, `gcmsg`, etc.)
- `zsh-autosuggestions` : suggestions basées sur l'historique
- `zsh-syntax-highlighting` : coloration syntaxique en temps réel

### Powerlevel10k : le prompt le plus configurable

```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k
echo 'source ~/powerlevel10k/powerlevel10k.zsh-theme' >>~/.zshrc
```

Lance `p10k configure` après l'installation. Tu passes 5 minutes à répondre à des questions visuelles, et tu te retrouves avec un prompt parfaitement ajusté à ton workflow.

## Dépannage : problèmes courants

### iTerm2 ne se lance pas

1. Vérifie les permissions dans `Sécurité et confidentialité > Confidentialité`
2. Réinstalle depuis le site officiel
3. Vide le cache si le problème persiste : `rm -rf ~/Library/Preferences/com.googlecode.iterm2.plist`

### Caractères mal affichés

Si les icônes ou symboles s'affichent mal (carrés, points d'interrogation) :

1. Installe les polices dans `Font Book`
2. Redémarre iTerm2
3. Vérifie que la police sélectionnée supporte les caractères UTF-8 et les Nerd Fonts si tu utilises Powerlevel10k

### Performance lente

- Réduis la taille du buffer de défilement (par défaut 10 000 lignes, souvent inutile)
- Désactive la transparence si tu l'as activée
- Ferme les onglets et panneaux que tu n'utilises pas

⚠️ **Attention** : avec Powerlevel10k, une lenteur au démarrage vient souvent d'un `~/.zshrc` surchargé. Lance `zprof` pour identifier les plugins lents.

## FAQ : questions fréquentes

### iTerm2 est-il gratuit ?

Oui, complètement. Gratuit, open-source, sans limitation ni version premium.

### Puis-je utiliser iTerm2 avec Fish ou Bash ?

Sans problème. iTerm2 fonctionne avec tous les shells : Zsh, Bash, Fish, etc. C'est un émulateur de terminal, pas un shell.

### Comment sauvegarder ma configuration iTerm2 ?

Va dans `Preferences > General > Preferences` et clique sur "Save Current Settings to Folder". Versionne ce dossier avec Git. Tu récupères toute ta config en 30 secondes sur un nouveau Mac.

### iTerm2 ralentit-il mon Mac ?

Non. Il consomme généralement moins de ressources que le Terminal par défaut, surtout avec de gros volumes de texte à l'écran.

### Puis-je synchroniser mes réglages entre plusieurs Macs ?

Oui. Sauvegarde tes préférences dans un dossier synchronisé (Dropbox, iCloud, ou repo Git privé), puis pointe iTerm2 vers ce dossier dans `Preferences > General > Preferences`.

## Résumé : ton terminal, enfin utilisable

iTerm2 transforme le terminal macOS en quelque chose qu'on a envie d'utiliser. La Hotkey Window seule justifie l'installation.

Priorités si tu pars de zéro :

1. Installe iTerm2 via Homebrew
2. Configure une Hotkey Window sur `Option + Space`
3. Installe [Oh My Zsh + Powerlevel10k](https://brandonvisca.com/installation-oh-my-zsh-powerlevel10k-guide-complet/)
4. Active les plugins `zsh-autosuggestions` et `zsh-syntax-highlighting`

Si tu hésites avec Warp ou un autre terminal IA, j'ai fait un [test complet iTerm2 vs Warp](https://brandonvisca.com/warp-terminal-2025-iterm2-killer-ou-simple-hype-test-complet-ia/) après 60 jours d'utilisation des deux.
