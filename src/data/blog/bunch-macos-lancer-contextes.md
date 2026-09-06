---
title: "Bunch macOS : lance des contextes complets en un clic"
description: "Bunch macOS : lance des contextes complets (apps, fichiers, sites) en un clic. Gratuit, open-source et parfait pour switcher entre projets."
pubDatetime: 2026-08-31 06:00:00+00:00
modDatetime: 2026-08-31 06:00:00+00:00
author: Brandon
tags:
  - bunch
  - macos
  - productivite
  - debutant
  - automation
featured: false
draft: false
focusKeyword: bunch macos
ogImage: ""
---
> 💡 **TL;DR**
>
> - Bunch lance des groupes d'applications et fichiers en un clic
> - Parfait pour switcher entre contextes de travail sur macOS
> - Gratuit et open-source avec des raccourcis clavier et AppleScript

## Table des matières

## Qu'est-ce que Bunch ?

Bunch, c'est une petite appli macOS gratuite et open-source créée par Brett Terpstra (un gars qui connait un rayon sur l'automation macOS, tu peux lui faire confiance les yeux fermés). Son job ? Te permettre de lancer des **contextes complets** en un seul clic ou raccourci clavier.

Un contexte, c'est quoi ? Imagine que tu passes ta journée à jongler entre plusieurs projets. Le matin, tu bosses sur ton site web : il te faut VS Code, Safari avec trois onglets précis, l'aperçu d'une image dans Preview et peut-être un terminal. L'après-midi, tu passes en mode rédaction : tu ouvres Ulysses, Spotify pour la playlist focus, et Notion pour tes notes. Le soir, tu décompresses avec Messages et Apple Music.

À chaque fois, tu perds cinq minutes à ouvrir, fermer, repositionner des fenêtres. **Bunch élimine cette friction.** Tu crées un fichier texte qui dit "ouvre ça, ferme ça, mets ça là", et hop, un raccourci plus tard, ton Mac passe instantanément d'un univers à l'autre. C'est un peu comme avoir des profils de session, mais en plus rapide et sans la lourdeur.

Si tu es déjà un fan de l'automation sur macOS, Bunch s'intègre parfaitement dans une chaîne d'outils qui inclut par exemple [Hammerspoon](https://brandonvisca.com/hammerspoon-macos-scripting-lua/) pour aller encore plus loin dans le scripting avancé.

## Comment ça marche ?

Là où Bunch est brillant, c'est dans sa simplicité technique. Pas d'interface graphique complexe, pas de base de données opaque. Tu crées des fichiers texte avec l'extension `.bunch` dans un dossier spécial (`~/Bunch` par défaut), et Bunch les détecte automatiquement.

Chaque fichier `.bunch` est une liste d'instructions que Bunch exécute séquentiellement. Voici à quoi ressemble un fichier basique :

```
Slack
Visual Studio Code
~/Documents/Projet-2026.md
https://notion.so/
```

Quand tu déclenches ce bunch, Bunch lance Slack, ouvre VS Code, ouvre ton fichier Markdown et ouvre Notion dans Safari. C'est tout. Pas de magie noire, juste de l'exécution propre et rapide.

Tu peux aussi faire des choses plus subtiles. Par exemple, faire quitter des apps :

```
!Safari
!Messages
Slack
Visual Studio Code
```

Le `!` devant une app signifie "ferme-la". C'est parfait pour isoler ton environnement. Tu peux aussi cacher des apps plutôt que les fermer avec `@`, ou les affrir avec `%`. Tu veux qu'une app se lance en arrière-plan sans prendre le focus ? Pas de souci, Bunch gère ça.

Et parce que tout repose sur des fichiers texte, tu peux versionner tes bunches avec Git, les synchroniser via iCloud Drive, ou les partager avec ton équipe. C'est du pur geek-friendly.

## Cas d'usage concrets

Pour te donner une idée concrète, voici trois contextes que j'utilise personnellement et qui ont changé ma routine.

### Contexte "Morning Routine"

```
%Mail
%Calendar
https://news.ycombinator.com
https://brandonvisca.com/admin
Messages
```

Je lance ça avec un raccourci clavier (`Cmd + Shift + 1`) dès que j'allume mon Mac. Il m'affiche Mail et Calendar, ouvre mes deux sites du matin, et garde Messages accessible. Trois secondes, et je suis opérationnel.

### Contexte "Blog"

```
!Slack
!Mail
Ulysses
~/Sites/brandonvisca/images/
Safari
- https://brandonvisca.com
- https://analytics.brandonvisca.com
```

Le soir quand j'écris, je veux pas être distrait. Ce bunch ferme Slack et Mail, ouvre Ulysses, le dossier images, et Safari avec deux onglets préchargés. Zéro notification, zéro tentation.

### Contexte "Développement"

```
iTerm
Visual Studio Code
~/Code/mon-projet/
!Spotify
```

Le matin quand je code, j'ai besoin d'un terminal propre, VS Code sur le bon dossier, et Spotify fermé parce que je concentre mieux dans le silence. Un raccourci clavier, et c'est réglé.

Tout ça paraît peut-être anodin, mais accumulé sur une journée, une semaine, un mois, ça représente **des heures gagnées** et une charge mentale en moins. Plus besoin de te demander "qu'est-ce que j'avais ouvert hier pour ce projet ?", ton Mac revient exactement dans l'état où tu l'as laissé.

## Fonctionnalités avancées

Bunch ne se limite pas à ouvrir et fermer des applications. Brett Terpstra a pensé à pas mal de scénarios avancés qui font la différence.

### Variables dynamiques

Tu peux définir des variables dans tes bunches pour rendre les champs réutilisables. Par exemple, un bunch "Projet" qui prend un nom de dossier en paramètre. C'est utile quand tu as des dizaines de projets et que tu veux pas créer un bunch par projet.

### Scripts shell et AppleScript

Bunch peut exécuter des commandes shell ou des scripts AppleScript directement. Ça ouvre des perspectives énormes. Tu veux changer la résolution de ton écran, activer un mode focus, ou lancer une sauvegarde rsync avant d'ouvrir tes apps ? Intègre un script dans ton bunch et c'est parti.

### Raccourcis clavier

Chaque bunch peut se lier à un raccourci clavier global. Si tu as déjà lu mon article sur [Cheatsheet](https://brandonvisca.com/cheatsheet-macos-raccourcis-clavier/), tu sais à quel point les raccourcis clavier sont essentiels sur macOS. Avec Bunch, tu peux créer ta propre couche de raccourcis métier sans toucher à System Settings.

### AppleScript et URL schemes

Bunch est scriptable via AppleScript, ce qui signifie que tu peux le déclencher depuis d'autres apps comme Alfred, Raycast, ou Keyboard Maestro. Tu peux aussi utiliser des URL schemes pour lancer des bunches depuis des liens ou des automations.

### Single-file apps

Certaines apps macOS sont en fait des "Single File" (comme TextEdit avec un document spécifique). Bunch gère ça nativement : au lieu de lancer l'app seule, il ouvre le fichier avec l'app associée. C'est un détail, mais ça montre la finesse de l'outil.

## Installation et mise en route

Bunch est disponible sur le Mac App Store ou directement depuis le site officiel ([bunchapp.co](https://bunchapp.co)). La version Mac App Store est gratuite, la version directe est aussi gratuite mais permet plus facilement les mises à jour via Sparkle.

Une fois installé :

1. Lance Bunch. Il crée automatiquement le dossier `~/Bunch`.
2. Crée un fichier texte avec l'extension `.bunch` dans ce dossier.
3. Écris tes instructions (une app ou URL par ligne).
4. Bunch détecte le fichier et l'affiche dans sa barre de menu.
5. Clique dessus ou assigne un raccourci clavier dans les préférences.

Pas besoin de redémarrer, pas besoin de permissions complexes (hors accessibilité pour les raccourcis clavier globaux). C'est plug-and-play.

Si tu cherches un équivalent plus visuel pour gérer les paramètres système rapidement, j'ai aussi testé [One Switch](https://brandonvisca.com/one-switch-macos-panneau-controle/), un autre outil macOS qui complète bien Bunch pour les toggles rapides.

## Avantages et inconvénients

Comme tout outil qui vaut le coup, Bunch a ses forces et ses limites. Soyons honnêtes.

### Les gros points forts

- **Légèreté** : L'appli pèse quelques mégaoctets et consomme quasiment rien en RAM. Pas de Electron, pas de framework lourd.
- **Vitesse** : L'exécution est instantanée. Bunch envoie des événements système, pas de scripts lourds à parser.
- **Scriptabilité** : Entre les variables, les scripts shell, AppleScript et les URL schemes, tu peux l'intégrer dans n'importe quel workflow existant.
- **Prix** : Gratuit et open-source. Pas de freemium, pas de paywall caché.
- **Fichiers texte** : Versionnable, éditable dans n'importe quel éditeur, synchronisable via iCloud, Dropbox, Git, ce que tu veux.

### Les limites

- **Courbe d'apprentissage fichier texte** : Si t'es habitué aux interfaces glisser-déposer, l'édition de fichiers `.bunch` peut paraître austère au début. Mais bon, t'es sur mon site, je présuppose que tu n'as pas peur d'un fichier texte.
- **Pas d'interface visuelle de configuration** : C'est le corollaire du point précédent. Pas de GUI pour builder ton contexte, c'est à toi de taper les noms d'apps exacts.
- **macOS uniquement** : Évidemment, si tu bosses sur Linux ou Windows, c'est pas pour toi.
- **Dépendance aux noms d'apps** : Si tu renommes une app ou si le nom diffère de celui du bundle macOS, Bunch ne la trouvera pas. Il faut utiliser le nom exact.

## Les alternatives

Bunch n'est pas le seul joueur dans l'arène de l'automation contextuelle sur macOS. Voici les principaux concurrents et comment ils se positionnent.

**Keyboard Maestro** : Le mastodonte de l'automation macOS. Il fait mille fois plus que Bunch, mais il est payant (36 $) et a une courbe d'apprentissage bien plus raide. Si tu veux juste lancer des groupes d'apps, Bunch est plus léger et gratuit. Si tu veux des macros complexes avec conditions, boucles et interfaces, Keyboard Maestro est le choix.

**Raycast** : L'alternative moderne à Spotlight fait de plus en plus dans l'automation. Tu peux créer des "Quicklinks" et des scripts, mais la gestion de contextes complets avec ouverture/fermeture d'apps n'est pas aussi fluide que Bunch. Raycast excelle ailleurs (recherche, calculatrice, fenêtres), Bunch est plus spécialisé.

**Shortcuts macOS natif** : Depuis Monterey, Shortcuts est sur Mac. Tu peux théoriquement faire des choses similaires, mais l'interface visuelle devient vite lourde pour des contextes complexes, et la gestion des apps ouvertes/fermées est moins élégante. Shortcuts est mieux pour des séquences linéaires simples.

**Hammerspoon** : Mentionné plus haut, [Hammerspoon](https://brandonvisca.com/hammerspoon-macos-scripting-lua/) est bien plus puissant mais demande d'écrire du Lua. Bunch est à Hammerspoon ce que une visseuse électrique est à une boîte à outils complète. Parfois, tu veux juste la visseuse.

## Verdict

Bunch, c'est l'outil parfait pour les geeks productifs qui passent leur journée à switcher de casquettes. Développeur le matin, rédacteur l'après-midi, créateur le soir : chaque transition se fait en une seconde au lieu de cinq minutes de manipulation de fenêtres.

Son approche par fichiers texte est à la fois son plus grand atout et son principal filtre. Si l'idée d'éditer un `.bunch` dans VS Code ou Vim te fait sourire, c'est fait pour toi. Si tu cherches une interface graphique avec des icônes et des boutons, regarde plutôt du côté de Raycast ou Keyboard Maestro.

Personnellement, Bunch a trouvé sa place dans mon workflow quotidien entre [One Switch](https://brandonvisca.com/one-switch-macos-panneau-controle/) pour les toggles système et les raccourcis clavier pour les actions rapides. C'est devenu un muscle mémoire : `Cmd + Shift + 1` pour le matin, `Cmd + Shift + 2` pour le blog, `Cmd + Shift + 3` pour le code. Simple, rapide, efficace.

Tu devrais l'essayer. Ça prend cinq minutes à installer et à configurer ton premier contexte, et je parie que tu ne reviendras pas en arrière. Dans un monde où chaque seconde compte, automatiser les transitions entre tes modes de travail n'est pas un luxe, c'est une nécessité. Bunch rend ça accessible, gratuit, et sans friction. Essaie-le, et dis-moi pas merci.

## FAQ

**Bunch est-il gratuit ?**
Oui, Bunch est entièrement gratuit et open-source. Tu peux le télécharger sur le Mac App Store ou directement depuis le site officiel bunchapp.co sans payer un centime.

**Bunch fonctionne-t-il sur Windows ou Linux ?**
Non, Bunch est exclusivement disponible sur macOS. Si tu cherches un équivalent sur Linux, des solutions comme AutoKey ou des scripts bash peuvent partiellement remplir ce rôle.

**Bunch peut-il remplacer Keyboard Maestro ?**
Pour la gestion de contextes simples (ouvrir/fermer des apps), oui. Mais Keyboard Maestro fait bien plus (macros complexes, conditions, interfaces). Bunch est plus léger et spécialisé.

**Comment assigner un raccourci clavier à un bunch ?**
Dans les préférences de Bunch, tu peux lier chaque bunch à un raccourci clavier global. L'app demande les permissions d'accessibilité macOS pour que ça fonctionne.

**Où sont stockés les fichiers de configuration ?**
Les fichiers `.bunch` sont stockés dans `~/Bunch` par défaut. Tu peux les éditer dans n'importe quel éditeur de texte, les versionner avec Git, ou les synchroniser via iCloud/Dropbox.
