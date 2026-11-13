---
title: "AeroSpace macOS : le tiling façon i3 sans désactiver SIP"
description: "AeroSpace macOS : installe ce tiling window manager type i3, gratuit et open-source, sans toucher à SIP. Config aerospace.toml et raccourcis inclus."
pubDatetime: "2026-11-13T11:01:50+01:00"
modDatetime: "2026-11-12T08:00:00.000Z"
author: Brandon
tags:
  - macos
  - tiling
  - intermediaire
featured: false
draft: false
focusKeyword: aerospace macos
faqs:
  - question: "AeroSpace macOS est-il vraiment gratuit, et faut-il désactiver SIP ?"
    answer: "Oui, AeroSpace est open-source sous licence MIT, entièrement gratuit, et il n'exige jamais de désactiver SIP. Il s'appuie uniquement sur l'API d'accessibilité publique de macOS (AXUIElement), celle qu'utilisent aussi VoiceOver ou les lecteurs d'écran."
  - question: "AeroSpace cohabite-t-il avec les Spaces natifs de macOS ?"
    answer: "Non, et c'est volontaire. Ses workspaces sont virtuels : les fenêtres inactives sont déplacées hors de l'écran visible plutôt que rangées dans un Space macOS. Désactive Mission Control et les raccourcis de Spaces pour éviter les conflits de raccourcis clavier."
  - question: "Que faire si AeroSpace ne se lance pas après une mise à jour macOS ?"
    answer: "Vérifie d'abord la permission Accessibilité dans Réglages Système, elle sautille parfois après une mise à jour majeure. Si ça ne suffit pas, lance la commande brew upgrade --cask nikitabobko/tap/aerospace : l'app n'étant pas notarisée par Apple, un build à jour règle la quasi-totalité des soucis de compatibilité."
---
> 💡 **TL;DR**
> - AeroSpace macOS est un tiling window manager gratuit et open-source, inspiré d'i3, qui ne demande jamais de désactiver SIP
> - Installation en une ligne via Homebrew (`brew install --cask nikitabobko/tap/aerospace`), config dans un simple fichier `aerospace.toml`
> - Workspaces virtuels, raccourcis clavier natifs, aucun daemon tiers à surveiller : juste l'API d'accessibilité publique de macOS

## AeroSpace macOS : le tiling façon i3 sans désactiver SIP

Tu viens de Linux, tu as connu i3 ou Hyprland, et tu détestes devoir attraper une fenêtre à la souris pour la coller à moitié d'écran. Je suis passé par là. Sur macOS, les deux options classiques pour du vrai tiling sont [Yabai](/yabai-macos-tiling-avance/), qui exige de désactiver SIP pour ses fonctionnalités avancées, et [Amethyst](/amethyst-macos-tiling-window-manager/), plus doux mais plus limité sur les workspaces.

AeroSpace macOS se pose entre les deux, et pour beaucoup de gens, il règle le dilemme : du tiling sérieux, une config texte façon i3, et zéro compromis sur la sécurité du système. Pas de SIP désactivé, pas de daemon C qui s'injecte dans le Dock. Juste l'API d'accessibilité publique d'Apple, celle que tout logiciel d'assistance utilise déjà.

## Table des matières

## Pourquoi AeroSpace macOS plutôt que Yabai ou Amethyst

AeroSpace macOS est développé par Nikita Bobko, distribué sous licence MIT sur GitHub, entièrement gratuit. Pas de version Pro, pas de palier payant caché. La promesse affichée par le projet est simple : un tiling window manager i3-like qui ne touche jamais à System Integrity Protection.

La différence avec Yabai tient dans l'architecture. Yabai est un daemon qui s'injecte dans le WindowServer et le Dock pour obtenir un contrôle total, ce qui réclame SIP désactivé pour les espaces virtuels dynamiques et les notifications d'événements de fenêtre. AeroSpace fait l'inverse : il se contente de l'API AXUIElement, l'interface d'accessibilité que macOS expose publiquement. Moins de pouvoir brut sur le système, mais aucun risque supplémentaire pour ta machine.

Face à Amethyst, la comparaison se joue sur la richesse de la config. Amethyst tourne très bien pour un usage simple, mais sa personnalisation reste limitée à quelques layouts et raccourcis prédéfinis. AeroSpace expose chaque commande via un fichier TOML éditable à la main, avec des modes de liaison façon Vim, des conteneurs imbriqués, et une CLI complète pour scripter ton environnement.

**La vraie question c'est** : as-tu besoin du contrôle total de Yabai, ou juste d'un tiling propre et configurable sans prise de risque ? Si tu coches la deuxième case, AeroSpace macOS est probablement ton meilleur choix en 2026.

## Installation via Homebrew et permissions d'accessibilité

AeroSpace macOS n'est pas dans le dépôt Homebrew officiel `homebrew/cask`. Il vit dans son propre tap, maintenu directement par l'auteur :

```bash
brew install --cask nikitabobko/tap/aerospace
```

Petit détail qui a son importance : l'application n'est pas notarisée par Apple. Sans ça, macOS bloquerait le premier lancement avec un avertissement Gatekeeper. Homebrew s'en occupe automatiquement en retirant l'attribut de quarantaine `com.apple.quarantine` posé sur l'app après téléchargement, donc tu n'as rien à faire de spécial. Si jamais tu récupères le binaire ailleurs que par Homebrew, tu devras retirer cet attribut toi-même.

Au premier lancement, macOS te demande la permission Accessibilité. Si la fenêtre ne s'affiche pas automatiquement :

**Réglages Système > Confidentialité et sécurité > Accessibilité**

Ajoute AeroSpace à la liste et active le bouton. Sans cette permission, l'app ne peut tout simplement rien faire : aucune fenêtre ne bougera.

> ⚠️ Désactive en parallèle les raccourcis Mission Control et les gestes de changement de Space dans les réglages macOS. AeroSpace utilise ses propres raccourcis alt + chiffre pour ses workspaces virtuels, et un conflit avec les Spaces natifs crée une confusion pénible.

Pour lancer AeroSpace automatiquement à la connexion, pas besoin de LaunchAgent manuel, l'option existe nativement dans la config.

## Configuration : le fichier aerospace.toml

AeroSpace macOS lit sa config dans `~/.aerospace.toml`, ou dans `${XDG_CONFIG_HOME}/aerospace/aerospace.toml` si tu utilises cette variable. Si aucun fichier n'existe, il charge une configuration par défaut embarquée dans l'app, suffisante pour tester avant de personnaliser.

Commence par copier la config par défaut puis édite-la, plutôt que de partir de zéro :

```bash
mkdir -p ~/.config/aerospace
touch ~/.aerospace.toml
```

Voici une base de départ réaliste, avec `config-version = 2` qui est désormais recommandé pour profiter des options récentes comme `persistent-workspaces` :

```toml
config-version = 2
start-at-login = true
auto-reload-config = true
accordion-padding = 30

default-root-container-layout = 'tiles'
default-root-container-orientation = 'auto'

on-focused-monitor-changed = ['move-mouse monitor-lazy-center']
automatically-unhide-macos-hidden-apps = false

key-mapping.preset = 'qwerty'

[gaps]
inner.horizontal = 8
inner.vertical   = 8
outer.left       = 8
outer.right      = 8
outer.top        = 8
outer.bottom     = 8

[mode.main.binding]
alt-h = 'focus left'
alt-j = 'focus down'
alt-k = 'focus up'
alt-l = 'focus right'

alt-shift-h = 'move left'
alt-shift-j = 'move down'
alt-shift-k = 'move up'
alt-shift-l = 'move right'

alt-1 = 'workspace 1'
alt-2 = 'workspace 2'
alt-3 = 'workspace 3'

alt-shift-1 = 'move-node-to-workspace 1'
alt-shift-2 = 'move-node-to-workspace 2'
alt-shift-3 = 'move-node-to-workspace 3'

alt-slash = 'layout tiles horizontal vertical'
alt-comma = 'layout accordion horizontal vertical'

alt-r = 'mode resize'

[mode.resize.binding]
h = 'resize width -50'
j = 'resize height +50'
k = 'resize height -50'
l = 'resize width +50'
enter = 'mode main'
esc = 'mode main'
```

`auto-reload-config = true` recharge la config à chaque sauvegarde du fichier, pratique pendant que tu ajustes tes raccourcis. Les gaps se règlent en pixels, séparément pour l'intérieur (`inner`) et les bords d'écran (`outer`). Si tu bosses sur un MacBook avec un écran externe, tu peux même définir des gaps différents par moniteur.

## Commandes, raccourcis et workspaces virtuels

AeroSpace macOS utilise un système de modes de liaison inspiré de Vim. `[mode.main.binding]` contient tes raccourcis quotidiens, et tu peux créer des modes supplémentaires comme `[mode.resize.binding]` ci-dessus, activés avec la commande `mode <nom>` et quittés avec `esc` ou `enter`.

Les commandes les plus utiles au quotidien :

- `focus (left|down|up|right)` : déplace le focus entre fenêtres voisines
- `move (left|down|up|right)` : déplace la fenêtre focalisée
- `join-with (left|down|up|right)` : regroupe deux fenêtres dans un même conteneur
- `layout tiles|accordion|floating` : change la disposition du nœud focalisé
- `workspace <nom>` : bascule sur un espace de travail
- `move-node-to-workspace <nom>` : envoie la fenêtre focalisée sur un autre workspace
- `resize (width|height) [+|-]<nombre>` : redimensionne la fenêtre active
- `reload-config` : recharge `aerospace.toml` sans relancer l'app

Le point qui dérange au début, puis qui devient logique : les workspaces d'AeroSpace ne sont **pas** des Spaces macOS. Ce sont des conteneurs virtuels. Quand tu quittes un workspace, AeroSpace déplace simplement les fenêtres hors de la zone visible de l'écran, elles existent toujours, elles tournent toujours, elles sont juste repoussées hors champ. Ça évite les lenteurs de transition des Spaces natifs et ça permet de créer autant de workspaces que tu veux, sans préallocation.

Pour lancer une app directement depuis un raccourci, utilise `exec-and-forget`, utilisable uniquement dans la config :

```toml
alt-enter = 'exec-and-forget open -na /Applications/Ghostty.app'
```

💡 Si tu jongles aussi avec plusieurs navigateurs selon le contexte (perso, boulot, client), jette un œil à [Velja](/velja-macos-choisir-navigateur/) : ça complète bien un setup clavier-first comme celui-ci.

## Dépannage courant

### AeroSpace macOS ne bouge aucune fenêtre

Dans 90 % des cas, c'est la permission Accessibilité qui n'est pas accordée ou qui a sauté après une mise à jour macOS. Retourne dans **Réglages Système > Confidentialité et sécurité > Accessibilité**, retire AeroSpace de la liste puis rajoute-le. Ça force macOS à réémettre le token de permission.

### La config ne se recharge pas

Vérifie que `auto-reload-config` est à `true`, ou force manuellement avec la commande CLI :

```bash
aerospace reload-config
```

Si rien ne se passe, c'est souvent une erreur de syntaxe TOML silencieuse. Relis les indentations et les guillemets, le parseur n'affiche pas toujours une erreur explicite dans le terminal.

### Conflit avec Mission Control ou un autre tiling manager

N'installe pas AeroSpace macOS en parallèle de Yabai, Amethyst ou Rectangle. Deux gestionnaires de fenêtres qui tentent de contrôler les mêmes raccourcis et le même WindowServer se battent, et tu finis avec des comportements erratiques. Choisis-en un.

### L'app refuse de se lancer après une mise à jour macOS majeure

Comme AeroSpace n'est pas notarisé par Apple, un changement de politique Gatekeeper sur une nouvelle version de macOS peut bloquer temporairement le binaire. Mets à jour via Homebrew :

```bash
brew upgrade --cask nikitabobko/tap/aerospace
```

C'est généralement suffisant, le mainteneur publie des correctifs rapidement après chaque sortie majeure de macOS.

## Conclusion

AeroSpace macOS comble un vrai trou : du tiling sérieux, une config texte lisible, des workspaces virtuels, sans jamais te demander de baisser la garde sur la sécurité de ta machine. Si tu arrives de Linux et que tu cherches ton i3 sur Mac sans toucher à SIP, c'est probablement l'outil qu'il te faut.

Ceux qui veulent plus de puissance brute, au prix de SIP désactivé, iront voir [Yabai](/yabai-macos-tiling-avance/). Ceux qui veulent démarrer sans toucher à un fichier de config iront vers [Amethyst](/amethyst-macos-tiling-window-manager/). Entre les deux, AeroSpace prend le meilleur des deux mondes : la liberté de config d'un vrai tiling manager, la tranquillité d'esprit de ne rien avoir désactivé.

Chez moi, la bascule a pris une soirée : installation, permissions, copie de la config par défaut, ajustement des raccourcis à ma sauce. Depuis, je ne touche plus ma souris pour organiser mes fenêtres. Et si tu veux pousser ton setup macOS encore plus loin côté productivité, j'ai recensé [10 outils macOS gratuits que j'utilise](/10-outils-low-tech-macos-guide-complet/) qui complètent bien ce genre de workflow clavier-first.
