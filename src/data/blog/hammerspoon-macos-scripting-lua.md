---
title: "Hammerspoon macOS : scripting Lua ultra-puissant pour automatiser tout"
description: "Hammerspoon macOS : automatise ton workflow avec des scripts Lua ultra-puissants. Raccourcis, fenêtres, lancement d'apps, tout devient programmable."
pubDatetime: "2026-08-29T06:00:00.000Z"
modDatetime: "2026-08-29T06:00:00.000Z"
author: Brandon Visca
tags:
  - macos
  - productivite
  - automation
  - lua
  - scripting
  - debutant
featured: false
draft: false
focusKeyword: hammerspoon macos
faqs: []
ogImage: ""
---
> 💡 **TL;DR**
> - Hammerspoon est un framework d'automatisation macOS basé sur Lua, gratuit et open-source
> - Tu crées des scripts personnalisés pour gérer les fenêtres, les raccourcis clavier, le lancement d'apps et bien plus
> - Une courbe d'apprentissage douce pour un potentiel quasi illimité, du débutant au power user

## Table des matières

## Qu'est-ce que Hammerspoon macOS ?

Tu connais peut-être AutoHotkey sur Windows. Cet outil magique qui te permet de binder n'importe quelle touche à n'importe quelle action, de redimensionner des fenêtres à la volée, et de transformer ton PC en machine sur mesure. Sur macOS, l'équivalent existe. Il s'appelle **Hammerspoon**.

Hammerspoon est un framework d'automatisation open-source pour macOS. Il utilise le langage **Lua**, léger et expressif, pour te donner un contrôle total sur ton système. Tu écris un fichier de configuration (`init.lua`), Hammerspoon l'interprète en temps réel, et soudain ton Mac obéit à tes ordres personnalisés.

Pas de GUI tape-à-l'œil. Pas de marketplace d'extensions. Juste toi, un éditeur de texte, et la documentation. Ça peut faire peur au premier abord, mais une fois passé le cap, tu ne reviens pas en arrière. Tout devient scriptable. Tout.

## Pourquoi se fatiguer quand on peut scripter ?

macOS est un excellent système d'exploitation, mais il a un défaut de taille : il pense savoir mieux que toi comment tu veux travailler. Les fenêtres s'ouvrent n'importe où. Les raccourcis clavier sont rigides. Le lancement d'applications demande un détour par le Dock ou Spotlight.

Avec Hammerspoon, tu reprends le contrôle. Voici quelques exemples concrets de ce que tu peux faire :

- **Gérer les fenêtres** : redimensionner, déplacer, centrer, splitter l'écran en deux, trois ou quatre zones, tout au clavier
- **Créer des raccourcis clavier globaux** : lancer une app, coller du texte, ouvrir un fichier, exécuter un script shell, depuis n'importe où
- **Surveiller les événements système** : détecter le changement de résolution d'écran, le passage sur batterie, le verrouillage de session
- **Automatiser les applications** : contrôler Spotify, régler le volume, envoyer des notifications personnalisées
- **Manipuler le presse-papiers** : historique du clipboard, transformations de texte, snippets
- **Créer des menus personnalisés** dans la barre de menus pour accéder rapidement à tes fonctions favorites

Bref, si tu peux l'écrire en Lua, Hammerspoon peut l'exécuter. C'est aussi simple que ça.

Si tu veux un panneau de contrôle rapide sans coder, j'ai testé [One Switch](/one-switch-macos-panneau-controle/). C'est moins puissant, mais parfait pour les réglages système en un clic.

## Installation en 30 secondes

Tu as deux options : Homebrew ou téléchargement manuel. La première est évidemment recommandée.

Via Homebrew :

```bash
brew install --cask hammerspoon
```

Puis lance l'application depuis le dossier Applications. Tu verras une icône marteau en forme de losange apparaître dans ta barre de menus. C'est le cœur de Hammerspoon, toujours actif en arrière-plan.

Le fichier de configuration vit dans `~/.hammerspoon/init.lua`. Si ce dossier n'existe pas, crée-le :

```bash
mkdir -p ~/.hammerspoon
touch ~/.hammerspoon/init.lua
```

Ouvre ce fichier dans ton éditeur préféré (VS Code, Neovim, Sublime Text, peu importe) et prépare-toi à écrire ton premier script.

## Ton premier script Lua

Lua est un langage simple. Pas besoin d'être développeur pour lire ce qui suit. Commençons par quelque chose de basique : afficher une alerte quand Hammerspoon se recharge.

Ajoute ceci dans ton `init.lua` :

```lua
hs.alert.show("Hammerspoon est prêt !")
```

Sauvegarde, puis recharge la config depuis l'icône de la barre de menus (Reload Config). Tu devrais voir une notification s'afficher en haut de l'écran. Ça marche ? Parfait. Tu viens d'écrire ton premier script Hammerspoon.

Voyons quelque chose d'utile maintenant. Un raccourci clavier pour lancer ton terminal préféré :

```lua
hs.hotkey.bind({"cmd", "alt"}, "T", function()
    hs.application.launchOrFocus("Terminal")
end)
```

Ce script dit : quand j'appuie sur `Cmd + Alt + T`, lance ou donne le focus à l'application Terminal. Simple, efficace, immédiat.

## Gérer les fenêtres comme un pro

C'est probablement l'usage le plus populaire de Hammerspoon. macOS gère mal les fenêtres. Tu ouvres une app, elle apparaît n'importe où. Tu veux la mettre à gauche de l'écran ? Tu dois la traîner à la main comme au siècle dernier.

Hammerspoon corrige ça en quelques lignes. Voici un exemple qui centre la fenêtre active :

```lua
hs.hotkey.bind({"cmd", "alt"}, "C", function()
    local win = hs.window.focusedWindow()
    if win then
        local f = win:frame()
        local screen = win:screen():frame()
        f.x = screen.x + (screen.w - f.w) / 2
        f.y = screen.y + (screen.h - f.h) / 2
        win:setFrame(f)
    end
end)
```

`Cmd + Alt + C` et ta fenêtre se centre parfaitement sur l'écran. Pas besoin de souris.

Tu veux splitter l'écran en deux ? Facile :

```lua
hs.hotkey.bind({"cmd", "alt", "ctrl"}, "Left", function()
    local win = hs.window.focusedWindow()
    if win then
        local f = win:frame()
        local screen = win:screen():frame()
        f.x = screen.x
        f.y = screen.y
        f.w = screen.w / 2
        f.h = screen.h
        win:setFrame(f)
    end
end)

hs.hotkey.bind({"cmd", "alt", "ctrl"}, "Right", function()
    local win = hs.window.focusedWindow()
    if win then
        local f = win:frame()
        local screen = win:screen():frame()
        f.x = screen.x + (screen.w / 2)
        f.y = screen.y
        f.w = screen.w / 2
        f.h = screen.h
        win:setFrame(f)
    end
end)
```

`Cmd + Alt + Ctrl + Flèche Gauche` colle la fenêtre sur la moitié gauche. `Flèche Droite` sur la moitié droite. Tu as maintenant un window snapping digne de ce nom, natif et sans application tierce lourde.

Pour customiser le notch de ton MacBook, [Boring Notch](/boring-notch-macbook-dynamic-island/) fait des miracles. C'est un autre outil open-source qui transforme cette encoche en hub d'informations utiles.

## Raccourcis clavier sur mesure

Les raccourcis clavier sont le cœur de Hammerspoon. Tu peux binder n'importe quelle combinaison à n'importe quelle action. Voici quelques exemples pratiques que j'utilise quotidiennement.

Lancer rapidement mes apps favorites :

```lua
local appLaunchKeys = {
    {"B", "Brave Browser"},
    {"S", "Slack"},
    {"V", "Visual Studio Code"},
    {"F", "Finder"},
}

for _, combo in ipairs(appLaunchKeys) do
    hs.hotkey.bind({"cmd", "alt"}, combo[1], function()
        hs.application.launchOrFocus(combo[2])
    end)
end
```

Avec ce bloc, `Cmd + Alt + B` ouvre Brave, `Cmd + Alt + S` ouvre Slack, etc. Cinq lignes pour remplacer un launcher entier.

Tu veux aussi coller du texte préformaté ? Pas besoin d'outil dédié. Hammerspoon gère le presse-papiers :

```lua
hs.hotkey.bind({"cmd", "shift"}, "V", function()
    hs.pasteboard.setContents("contact@brandonvisca.fr")
    hs.alert.show("Email copié !")
end)
```

## Aller plus loin : les API Hammerspoon

Hammerspoon expose des dizaines d'APIs couvrant quasiment tous les aspects de macOS. Voici les principales que tu vas utiliser régulièrement :

- **`hs.application`** : lancer, fermer, lister les applications en cours d'exécution, obtenir le focus
- **`hs.window`** : redimensionner, déplacer, lister les fenêtres, passer d'une fenêtre à l'autre
- **`hs.screen`** : détecter les écrans connectés, obtenir leur résolution, gérer les espaces
- **`hs.hotkey`** : créer des raccourcis clavier globaux
- **`hs.pasteboard`** : manipuler le presse-papiers système
- **`hs.wifi`** : surveiller l'état du Wi-Fi, changer de réseau
- **`hs.battery`** : obtenir le niveau de batterie, détecter le passage sur secteur
- **`hs.pathwatcher`** : surveiller les modifications de fichiers et recharger automatiquement la config
- **`hs.notify`** : envoyer des notifications macOS personnalisées
- **`hs.dialog`** : afficher des boîtes de dialogue pour des interactions rapides

Voici un exemple un peu plus avancé : afficher une alerte quand tu passes sur batterie, pour te rappeler de vérifier ton chargeur :

```lua
local batteryWatcher = hs.battery.watcher.new(function()
    if not hs.battery.isCharging() and hs.battery.percentage() < 30 then
        hs.notify.new({
            title = "Batterie faible",
            informativeText = "Il reste " .. math.floor(hs.battery.percentage()) .. "% de batterie. Branche le chargeur !"
        }):send()
    end
end)
batteryWatcher:start()
```

Ce watcher tourne en arrière-plan et te prévient automatiquement. Zéro interaction manuelle.

## Exemple complet : un mini workflow productivité

Pour te donner une idée concrète, voici un extrait de ma configuration personnelle. C'est un workflow simple qui gère mes fenêtres, lance mes apps, et me donne des infos rapides.

```lua
-- Reloader la config automatiquement quand init.lua change
hs.pathwatcher.new(os.getenv("HOME") .. "/.hammerspoon/", hs.reload):start()

-- Centrer la fenêtre active
hs.hotkey.bind({"cmd", "alt"}, "C", function()
    local win = hs.window.focusedWindow()
    if win then win:centerOnScreen() end
end)

-- Maximize la fenêtre active
hs.hotkey.bind({"cmd", "alt"}, "M", function()
    local win = hs.window.focusedWindow()
    if win then win:maximize() end
end)

-- Lancer les apps du quotidien
hs.hotkey.bind({"cmd", "alt"}, "B", function()
    hs.application.launchOrFocus("Brave Browser")
end)

hs.hotkey.bind({"cmd", "alt"}, "T", function()
    hs.application.launchOrFocus("Terminal")
end)

-- Notification de confirmation au rechargement
hs.alert.show("Config Hammerspoon rechargée")
```

Ce fichier fait à peine vingt lignes et remplace déjà trois ou quatre utilitaires différents. Pas besoin d'un tiling manager externe, pas besoin d'un launcher d'apps, pas besoin d'un gestionnaire de clipboard.

Si c'est du tiling window manager que tu cherches, [Amethyst](/amethyst-macos-tiling-window-manager/) est plus simple à configurer. C'est une alternative solide si tu ne veux pas écrire de Lua. Mais Hammerspoon reste bien plus flexible à long terme.

## Alternatives et comparatif

Hammerspoon n'est pas le seul outil d'automatisation sur macOS. Voici comment il se compare aux autres solutions populaires :

**Karabiner-Elements** est excellent pour remapper les touches et créer des layers de clavier. Il est plus bas niveau que Hammerspoon, mais il ne gère pas les fenêtres ni les applications. Les deux se complètent très bien.

**BetterTouchTool** est une solution tout-en-un avec une interface graphique. Il gère les fenêtres, les raccourcis, les gestures trackpad. C'est puissant, mais c'est payant et moins flexible que le Lua pur.

**Raycast** ou **Alfred** sont des launchers avec des workflows. Ils sont géniaux pour lancer des scripts et rechercher des fichiers, mais ils ne tournent pas en arrière-plan pour surveiller le système comme Hammerspoon.

**Apple Shortcuts** est de plus en plus capable sur macOS, mais il reste limité par son approche visuelle. Certaines actions avancées sont impossibles ou demandent des contournements complexes.

Si tu cherches juste à lancer des groupes d'applications et de fichiers sans écrire une ligne de code, [Bunch](https://brandonvisca.com/bunch-macos-lancer-contextes/) est une alternative légère et gratuite qui utilise de simples fichiers texte pour définir tes contextes de travail.

Hammerspoon trône au sommet en termes de flexibilité brute. Le prix à payer est une courbe d'apprentissage plus raide. Si tu aimes bidouiller et comprendre ce qui se passe sous le capot, c'est l'outil idéal.

## Astuces pour bien démarrer

Premier conseil : ne copie pas une configuration entière trouvée sur GitHub sans comprendre ce qu'elle fait. Tu vas te retrouver avec des dizaines de raccourcis conflictuels et un fichier illisible. Pars de zéro, ajoute une fonctionnalité à la fois, teste-la, puis passe à la suivante.

Deuxième conseil : utilise le logger intégré de Hammerspoon pour déboguer. La console est accessible depuis l'icône de la barre de menus (Open Console). Tu y vois les erreurs Lua en temps réel. C'est indispensable quand ton script ne fait pas ce que tu attends. Tu peux aussi utiliser `hs.inspect` pour afficher le contenu des tables Lua dans la console.

Troisième conseil : la documentation officielle est excellente. Le site [Hammerspoon.org/docs](https://www.hammerspoon.org/docs/) référence toutes les APIs avec des exemples. Garde-le sous le coude. Chaque module est documenté avec ses méthodes, ses paramètres et des snippets prêts à l'emploi.

Quatrième conseil : pense à commenter ton code. Même si Lua est simple, six mois plus tard tu ne te souviendras plus de pourquoi tu as écrit ce watcher bizarre à 2 heures du matin. En Lua, une ligne de commentaire commence par deux tirets consécutifs, et les blocs multi-lignes s'ouvrent et se ferment par deux tirets suivis de deux crochets.

Cinquième conseil : si tu es sur un MacBook avec puce Apple Silicon, Hammerspoon tourne nativement en ARM64. Pas besoin de Rosetta 2. C'est fluide, léger, et il consomme moins de 50 Mo de RAM au repos. Tu peux le laisser tourner en permanence sans impacter tes performances.

Sixième conseil : Hammerspoon fonctionne parfaitement avec les gestionnaires de fenêtres existants. Tu peux l'utiliser en parallèle d'Amethyst ou de Rectangle si tu veux. Il n'y a pas de conflit majeur, sauf si tu bindes les mêmes raccourcis dans les deux outils.

## Verdict

Hammerspoon macOS est un outil d'une puissance rare. Il transforme ton Mac en une machine véritablement personnalisée, où chaque action peut être scriptée, optimisée, et adaptée à ton workflow exact. La barrière à l'entrée est le Lua, mais ce langage est tellement accessible que tu seras opérationnel en une heure.

Si tu passes plus de dix minutes par jour à repositionner des fenêtres, à chercher des apps dans le Dock, ou à répéter des actions mécaniques, Hammerspoon va te faire gagner un temps fou. Et une fois que tu auras goûté à l'automatisation totale, tu ne pourras plus t'en passer.

Installe-le ce weekend. Écris trois raccourcis. Teste. Puis ajoute-en un quatrième. Puis un cinquième. Au bout de quelques semaines, ton `init.lua` sera devenu le fichier le plus précieux de ton Mac. Et tu te demanderas pourquoi Apple ne propose pas ça en natif.

**Lien utile** : [Site officiel Hammerspoon](https://www.hammerspoon.org) pour la documentation complète, les APIs, et les exemples de la communauté.
