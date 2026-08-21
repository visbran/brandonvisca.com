---
title: "Yabai macOS : le tiling window manager avancé pour pros (SIP off)"
description: "Yabai macOS : tiling WM avancé avec espaces virtuels dynamiques. Tuto complet : install, config, skhd, et pourquoi désactiver SIP."
pubDatetime: 2026-08-21 06:00:00+00:00
modDatetime: 2026-08-21 06:00:00+00:00
author: Brandon Visca
tags:
  - intermediaire
  - macos
  - productivite
  - tiling
  - window-manager
featured: false
draft: false
focusKeyword: yabai macos
faqs:
  - question: "Est-ce que Yabai fonctionne avec SIP activé ?"
    answer: "Oui, mais avec des fonctionnalités limitées. Tu auras le tiling de base (bsp, float) et le focus, mais pas la création dynamique d'espaces virtuels ni les notifications d'événements de fenêtre. Pour 100 % des capacités, SIP doit être désactivé."
  - question: "Quelle différence entre Yabai et Amethyst ?"
    answer: "Amethyst est un tiling manager en Swift qui fonctionne sans désactiver SIP. Yabai est un daemon C plus rapide et plus programmable, mais il exige SIP off pour les fonctionnalités avancées comme les espaces virtuels dynamiques et l'injection dans le Dock."
  - question: "Comment désactiver SIP sur macOS ?"
    answer: "Redémarre en Recovery Mode (Cmd+R), ouvre Terminal depuis le menu Utilities, tape `csrutil disable`, puis redémarre. Vérifie avec `csrutil status`."
ogImage: "" 
---
> 💡 **TL;DR**
>
> - Yabai est un tiling window manager pour macOS qui organise automatiquement tes fenêtres via un daemon C ultra-rapide
> - Contrairement à [Amethyst](/amethyst-macos-tiling-window-manager/), il exige de désactiver SIP (System Integrity Protection) pour accéder aux fonctionnalités avancées
> - Couplé à skhd pour les raccourcis clavier, il offre des espaces virtuels dynamiques et des layouts bsp/stack/float dignes d'i3 ou dwm

## Pourquoi Yabai et pas un autre ?

Sur macOS, la gestion des fenêtres est un goulot d'étranglement. Apple te donne Mission Control, des espaces virtuels manuels et du drag-and-drop approximatif. Si tu viens de Linux (i3, Awesome, Hyprland) ou que tu bosses avec plusieurs terminaux, IDE et navigateurs en parallèle, tu sais déjà que le tiling n'est pas un luxe, c'est une nécessité.

Tu as probablement déjà testé [Amethyst](/amethyst-macos-tiling-window-manager/). C'est solide, gratuit, open-source, et ça marche sans toucher à SIP. Parfait pour débuter. Mais si tu veux aller plus loin, espaces virtuels créés à la volée, règles de fenêtres granulaires, layouts programmables, et un daemon qui réagit en millisecondes, Yabai est le niveau supérieur.

Yabai fonctionne comme un daemon C léger qui interagit avec le WindowServer de macOS via l'API d'accessibilité et, quand SIP est désactivé, via des injections dans le Dock pour gérer les espaces. Résultat : un contrôle total sur le tiling, la focus, et les transitions d'espace, avec une latence imperceptible.

## Le prix à payer : System Integrity Protection (SIP)

Apple a introduit SIP en 2015 avec El Capitan. C'est un mécanisme de sécurité qui empêche les processus root de modifier des fichiers système, d'injecter du code dans des apps signées, et surtout, ce qui nous concerne, d'interagir avec le WindowServer et le Dock pour créer ou détruire des espaces virtuels.

Yabai peut tourner en mode "scripting addition" limité avec SIP activé. Tu auras le tiling de base (bsp, float), le focus et quelques règles. Mais pas la création dynamique d'espaces, pas le changement d'espace instantané via skhd, pas les notifications d'événements de fenêtre. Bref, tu coupes les ailes à l'outil.

**Pour débloquer Yabai à 100 %, tu dois désactiver SIP.** C'est la condition sine qua non pour l'installation complète de la scripting addition.

### Comment désactiver SIP (Recovery Mode)

1. Redémarre ton Mac en maintenant `Cmd + R` jusqu'à l'apparition du logo Apple
2. Une fois en Recovery Mode, ouvre le menu Utilities > Terminal
3. Tape :

```bash
csrutil disable
```

4. Redémarre (`reboot`)

5. Pour vérifier que SIP est bien off :

```bash
csrutil status
```

Tu dois voir `System Integrity Protection status: disabled`.

**Avertissement sérieux** : désactiver SIP retire une couche de protection du système. Ne télécharge pas de binaires suspects, garde Gatekeeper actif (`spctl --master-enable`), et assure-toi que FileVault est allumé pour chiffrer ton disque. Sur un Mac dédié au dev et à la productivité, le risque est acceptable si tu fais pas le con. Sur une machine sensible (travail, données critiques), réfléchis bien.

## Installation via Homebrew

Si tu n'as pas encore Homebrew, installe-le d'abord :

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Puis installe Yabai et skhd (le gestionnaire de raccourcis clavier) :

```bash
brew install koekeishiya/formulae/yabai
brew install koekeishiya/formulae/skhd
```

### Autoriser l'accessibilité

macOS bloque Yabai et skhd par défaut. Va dans :

**System Settings > Privacy & Security > Accessibility**

Ajoute `yabai` et `skhd` à la liste. Si tu les vois pas, ajoute-les manuellement depuis `/opt/homebrew/bin/yabai` et `/opt/homebrew/bin/skhd` (ou `/usr/local/bin` sur Intel).

### Installer la scripting addition (SIP off obligatoire)

Avec SIP désactivé, charge le composant additionnel dans le Dock :

```bash
sudo yabai --install-sa
```

Puis injecte-le :

```bash
sudo yabai --load-sa
```

Pour que ça persiste après redémarrage, ajoute cette ligne dans ta configuration (voir `yabairc` ci-dessous).

## Configuration de base

### yabairc

Crée le dossier de config et le fichier :

```bash
mkdir -p ~/.config/yabai
touch ~/.config/yabai/yabairc
chmod +x ~/.config/yabai/yabairc
```

Voici une configuration de départ complète et commentée :

```bash
#!/usr/bin/env sh

# Charger la scripting addition (nécessite SIP off)
sudo yabai --load-sa

# ===== Général =====
yabai -m config layout                       bsp
yabai -m config external_bar                 all:0:0
yabai -m config window_shadow                float
yabai -m config window_opacity_duration        0.15
yabai -m config active_window_opacity        1.0
yabai -m config normal_window_opacity          0.90
yabai -m config window_animation_duration      0.15

# ===== Marges et padding =====
yabai -m config top_padding                  8
yabai -m config bottom_padding               8
yabai -m config left_padding                 8
yabai -m config right_padding                8
yabai -m config window_gap                   8

# ===== Règles spécifiques par application =====
# Les apps qui ne doivent jamais être tilées (flottantes)
yabai -m rule --add app="^System Settings$" manage=off
yabai -m rule --add app="^Calculator$"      manage=off
yabai -m rule --add app="^Finder$"          manage=off
yabai -m rule --add app="^Spotify$"         manage=off layer=above
yabai -m rule --add app="^Docker Desktop$"  manage=off
yabai -m rule --add title="^(Add|General)"  manage=off

# Taille par défaut pour les fenêtres flottantes
yabai -m config auto_balance                 off
yabai -m config split_ratio                  0.50
yabai -m config split_type                   auto

# ===== Mouse =====
yabai -m config mouse_follows_focus          off
yabai -m config focus_follows_mouse          off
yabai -m config mouse_modifier               fn
yabai -m config mouse_action1                move
yabai -m config mouse_action2                resize

echo "yabai configuration loaded.."
```

Recharge la config à tout moment avec :

```bash
yabai -m config --load
```

### skhdrc (raccourcis clavier)

Crée la config de skhd :

```bash
mkdir -p ~/.config/skhd
touch ~/.config/skhd/skhdrc
```

Voici un mapping complet pour naviguer sans souris :

```bash
# Relancer skhd
ctrl + alt + cmd - r : skhd --restart-service

# Focus fenêtre (vim style)
alt - h : yabai -m window --focus west
alt - j : yabai -m window --focus south
alt - k : yabai -m window --focus north
alt - l : yabai -m window --focus east

# Échanger fenêtres
shift + alt - h : yabai -m window --swap west
shift + alt - j : yabai -m window --swap south
shift + alt - k : yabai -m window --swap north
shift + alt - l : yabai -m window --swap east

# Déplacer fenêtre dans l'espace + suivre
shift + alt - 1 : yabai -m window --space 1; yabai -m space --focus 1
shift + alt - 2 : yabai -m window --space 2; yabai -m space --focus 2
shift + alt - 3 : yabai -m window --space 3; yabai -m space --focus 3
shift + alt - 4 : yabai -m window --space 4; yabai -m space --focus 4
shift + alt - 5 : yabai -m window --space 5; yabai -m space --focus 5

# Focus espace
alt - 1 : yabai -m space --focus 1
alt - 2 : yabai -m space --focus 2
alt - 3 : yabai -m space --focus 3
alt - 4 : yabai -m space --focus 4
alt - 5 : yabai -m space --focus 5

# Toggle float / tiling
alt - t : yabai -m window --toggle float --grid 4:4:1:1:2:2

# Toggle zoom (fullscreen within layout)
alt - f : yabai -m window --toggle zoom-fullscreen

# Balance / rotate tree
shift + alt - e : yabai -m space --balance
shift + alt - r : yabai -m space --rotate 90

# Toggle layout bsp / stack / float
alt - b : yabai -m space --layout bsp
alt - s : yabai -m space --layout stack
alt - d : yabai -m space --layout float
```

Puis lance les services :

```bash
yabai --start-service
skhd --start-service
```

Sur macOS Sonoma et plus, Homebrew gère les services via `brew services`. Si `--start-service` marche pas, utilise :

```bash
brew services start yabai
brew services start skhd
```

## Les trois layouts expliqués

Yabai gère trois modes de disposition. Tu peux basculer à la volée avec skhd ou via la commande CLI.

### BSP (Binary Space Partitioning)

C'est le mode par défaut et le plus puissant. Chaque nouvelle fenêtre divise l'espace disponible en deux. La direction de la scission (horizontale ou verticale) alterne automatiquement ou selon ta config. Tu obtiens un arbre binaire où chaque nœud est soit une fenêtre, soit un conteneur.

Avantage : utilisation optimale de l'espace, peu importe le nombre de fenêtres.
Inconvénient : si tu veux une fenêtre plus large qu'une autre, il faut ajuster manuellement le ratio.

### Stack

Toutes les fenêtres d'un même espace sont empilées les unes sur les autres. Seule la fenêtre au sommet est visible. Tu navigues entre elles avec `alt - j/k` ou `alt - n/p`.

Avantage : parfait quand tu veux plusieurs apps sur le même espace mais qu'une seule occupe l'écran (ex: terminal plein écran + navigateur + Slack).
Inconvénient : pas de vue simultanée.

### Float

Le mode classique de macOS. Les fenêtres restent libres, redimensionnables à la souris, sans tiling automatique. Yabai les laisse tranquilles sauf si tu ajoutes une règle spécifique.

Tu peux forcer une fenêtre spécifique à flotter avec :

```bash
yabai -m window --toggle float
```

## Règles de fenêtres par application

Yabai shine quand tu définis des règles automatiques. Tu ne veux pas que ton éditeur de code soit écrasé à côté de Finder, ni que Spotify se fasse couper en deux.

Syntaxe générale :

```bash
yabai -m rule --add app="^NomApp$" property=value [...]
```

Propriétés utiles :
- `manage=off`, la fenêtre reste flottante
- `layer=above|below|normal`, force la couche (utile pour Spotify flottant au-dessus)
- `sticky=on`, la fenêtre apparaît sur tous les espaces
- `grid=ROWS:COLS:X:Y:W:H`, taille et position si flottante (ex: `grid=4:4:1:1:2:2` = centrée, moitié de l'écran)
- `space=N`, envoie automatiquement sur l'espace N

Exemples concrets :

```bash
# Terminal toujours en plein écran sur l'espace 1
yabai -m rule --add app="^iTerm2$" space=1
yabai -m rule --add app="^Alacritty$" space=1

# Spotify flottant au-dessus, jamais tilé
yabai -m rule --add app="^Spotify$" manage=off layer=above

# Dialogues "Save" / "Open" toujours flottants
yabai -m rule --add title="^Save" manage=off
yabai -m rule --add title="^Open" manage=off

# Les fenêtres de paramètres des apps Electron (Slack, VS Code)
yabai -m rule --add title="^(Settings|Preferences|About)$" manage=off
```

## Espaces virtuels dynamiques

C'est là que Yabai distance Amethyst et [Swish](/swish-macos-gestion-fenetres-gestures/). Avec SIP off et la scripting addition chargée, tu peux créer et détruire des espaces à la volée.

Créer un nouvel espace et y envoyer la fenêtre focus :

```bash
yabai -m space --create
target=$(yabai -m query --spaces --display | jq '.[-1].index')
yabai -m window --space "${target}"
yabai -m space --focus "${target}"
```

Ou plus simplement, bindé dans skhd :

```bash
# Créer un espace + y envoyer la fenêtre focus + switcher
shift + alt - n : yabai -m space --create; yabai -m window --space last; yabai -m space --focus last

# Supprimer l'espace actuel (sauf s'il reste un seul)
shift + alt - x : yabai -m space --destroy
```

Avec quelques lignes de script, tu obtiens un workflow type i3 : chaque projet ou contexte de travail a son propre espace, créé quand tu en as besoin, détruit quand tu as fini. Pas besoin de préallouer 10 bureaux vides comme sur macOS vanilla.

### Script de focus intelligente

Si tu travailles avec plusieurs écrans, ce script dans skhd est pratique :

```bash
# Focus fenêtre suivante dans l'espace, même si c'est sur un autre écran
alt - tab : yabai -m window --focus next || yabai -m window --focus first
```

## Intégration avec skhd : la vraie puissance

skhd est le compagnon officiel de Yabai. C'est un gestionnaire de raccourcis clavier qui lit `~/.config/skhd/skhdrc` et traduit les keybindings en commandes shell. skhd est minimaliste : il écoute les touches et exécute. Rien d'autre.

Pourquoi pas Hammerspoon ici ? Parce que skhd est plus léger, démarre plus vite, et sa syntaxe de config est lisible en 5 minutes. Hammerspoon reste supérieur pour des automatisations complexes (changement de résolution, lancement de contextes, notifications), mais pour du tiling pur, skhd suffit amplement.

### Lancer des apps directement

Tu peux binder des lancements d'applications dans skhd :

```bash
# Lancer les apps favorites sur des espaces précis
alt - return : open -na Alacritty
shift + alt - b : open -na "Brave Browser"
shift + alt - c : open -na "Visual Studio Code"
```

### Séquences et modificateurs

skhd supporte les modificateurs classiques :
- `cmd`, `alt`, `shift`, `ctrl`, `fn`
- Combos : `cmd + shift`, `alt + shift`, etc.

Et les modes (comme Vim) si tu veux des couches de raccourcis. C'est overkill pour la plupart des users, mais ça existe.

## Dépannage courant

### Yabai ne se lance pas au démarrage

Vérifie que le service est bien enregistré :

```bash
brew services list | grep yabai
```

Si c'est `error`, relance avec :

```bash
yabai --stop-service
yabai --start-service
```

Et vérifie les logs :

```bash
tail -f /tmp/yabai_$USER.out.log
tail -f /tmp/yabai_$USER.err.log
```

### La scripting addition ne charge pas

Si tu vois des erreurs du type `payload does not support this macOS version`, ton build de Yabai est probablement en retard par rapport à ta version de macOS. Mets à jour :

```bash
brew upgrade yabai
sudo yabai --install-sa
sudo yabai --load-sa
```

### Les fenêtres ne se tile pas

Vérifie que l'app est pas dans une règle `manage=off`. Ensuite, vérifie que le layout de l'espace actuel est bien `bsp` :

```bash
yabai -m query --spaces --space
```

Si `type` vaut `float`, bascule en `bsp` avec `alt - b`.

### skhd ne capte pas les touches

Assure-toi qu'il a les droits d'accessibilité. Sur macOS Ventura+, va dans **System Settings > Privacy & Security > Input Monitoring** aussi, et ajoute skhd.

### Conflit avec Magnet, Rectangle ou autre

Désactive tout autre gestionnaire de fenêtres. Yabai + skhd remplacent complètement ces outils. Si tu veux du tiling, ne laisse pas deux outils se battre pour le contrôle du WindowServer.

## Dangers et avertissements

Je vais pas te mentir : désactiver SIP et laisser un daemon C tourner en arrière-plan avec des privilèges élevés, c'est pas anodin.

- **SIP off** = un malware root peut modifier des fichiers système. Mais macOS a d'autres défenses (Gatekeeper, FileVault, sandbox des apps).
- **yabai --load-sa** injecte du code dans le Dock. Si Yabai est compromis, théoriquement un attaquant pourrait abuser de ce canal. La solution : compile Yabai toi-même depuis les sources si tu es parano, et audit les releases.
- **Pas d'interface graphique** : si tu coches la config et que rien ne marche, tu es seul avec ton terminal. Pas de panneau "Réinitialiser".
- **Mise à jour macOS** : chaque mise à jour majeure de macOS peut casser la scripting addition. Il faut parfois attendre un patch du dev ou recompiler.

Mon conseil : teste Yabai sur un Mac secondaire d'abord, ou sur une partition dédiée. Quand tu es convaincu (et tu le seras), bascule sur ta machine principale. Garde toujours un backup de ta config (`~/.config/yabai/yabairc` + `~/.config/skhd/skhdrc`) sur GitHub ou dans un repo privé.

## Conclusion

Yabai n'est pas pour tout le monde. Si tu cherches juste à organiser deux-trois fenêtres sans prise de tête, [Amethyst](/amethyst-macos-tiling-window-manager/) reste le choix malin. Mais si tu passes ta journée entre un terminal, un IDE, un navigateur, Slack et un serveur local, et que tu en as marre de jouer à Tetris avec ta souris, Yabai est une révélation.

Le combo Yabai + skhd transforme macOS en un environnement de productivité aussi rapide et programmable que n'importe quel tiling manager Linux. Ça demande un investissement initial, désactiver SIP, écrire sa config, mémoriser les raccourcis, mais le retour est immédiat. Tu gagnes des heures chaque semaine rien en supprimant le besoin de gérer tes fenêtres à la main.

Yabai est l'outil que les devs pros utilisent quand ils ont dépassé le stade des gestionnaires de fenêtres grand public. Installer Yabai, c'est admettre que tu veux un contrôle total sur ton environnement, quitte à casser une sécurité Apple pour y arriver. C'est un choix. Et c'est le bon.
