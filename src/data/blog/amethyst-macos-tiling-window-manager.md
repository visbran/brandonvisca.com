---
title: "Amethyst macOS : tiling window manager gratuit pour un workflow au clavier"
description: "Amethyst macOS : tiling window manager gratuit et open-source. Organise tes fenêtres au clavier sans lever les mains du clavier."
pubDatetime: "2026-08-06T10:00:00.000Z"
modDatetime: "2026-08-06T10:00:00.000Z"
author: Brandon
tags:
  - macos
  - productivite
  - debutant
  - amethyst
  - tiling
featured: false
draft: false
focusKeyword: amethyst macos
faqs:
  - question: "Amethyst est-il compatible avec Apple Silicon (M1/M2/M3/M4) ?"
    answer: "Oui, Amethyst est compilé en natif pour Apple Silicon depuis la version 0.16. Aucune émulation Rosetta 2 nécessaire."
  - question: "Puis-je utiliser Amethyst avec un clavier AZERTY ?"
    answer: "Oui, mais tu devras probablement remapper certains raccourcis par défaut qui utilisent des touches spécifiques au QWERTY. La configuration se fait dans les préférences de l'app."
  - question: "Amethyst consomme-t-il beaucoup de ressources ?"
    answer: "Non, Amethyst consomme environ 20-40 Mo de RAM et moins de 1% de CPU au repos. C'est un outil léger comparé à d'autres gestionnaires de fenêtres."
  - question: "Quelle est la différence entre Amethyst et Yabai ?"
    answer: "Amethyst est un tiling manager en user-space qui utilise les API macOS standard. Yabai modifie le window server de macOS via un injection de code, ce qui lui donne plus de contrôle mais nécessite de désactiver SIP."
ogImage: ""
---
> 💡 **TL;DR**
> - Amethyst est un tiling window manager **gratuit** et **open-source** pour macOS qui organise automatiquement tes fenêtres
> - Tu gères tout au clavier : split, fullscreen, focus, swap, zéro souris nécessaire
> - Installation en 30 secondes via `brew install --cask amethyst`, configuration en 2 minutes
> - Idéal pour les développeurs et les geeks de la productivité qui veulent un workflow sans friction

## Table des matières

Sur macOS, gérer ses fenêtres, c'est une expérience à l'ancienne.

Tu ouvres un terminal. Puis un navigateur. Puis VS Code. Et là, paf : trois fenêtres empilées les unes sur les autres comme des crêpes maladroites. Tu passes ton temps à faire du resize à la main, à chercher celle qui est perdue derrière les autres, à jongler entre la souris et le trackpad.

Apple a bien essayé d'apporter un window tiling natif avec macOS Sequoia. C'est sympa, mais ça reste limité : tu dois activer manuellement le mode, et c'est loin d'être aussi fluide qu'un vrai tiling manager.

Si tu veux un workflow vraiment optimisé, où tes fenêtres s'organisent toutes seules et où tu pilotes tout au clavier, il existe une solution open-source, gratuite et légère : **Amethyst**.

Et non, ce n'est pas réservé aux hardcore Linux users qui rêvent de i3wm. Amethyst est accessible, simple à configurer, et il va transformer ta relation avec les fenêtres sur macOS.

## Amethyst macOS : qu'est-ce que c'est exactement ?

Amethyst est un **tiling window manager** pour macOS, inspiré de Xmonad (un gestionnaire de fenêtres très populaire sur Linux). Contrairement aux gestionnaires classiques comme [Magnet](/magnet-macos-gestionnaire-fenetres-guide-complet/) qui te demandent de snapper manuellement chaque fenêtre, Amethyst **organise automatiquement** tes fenêtres selon un layout prédéfini.

Tu ouvres une app ? Elle prend sa place. Tu en ouvres une deuxième ? L'écran se splitte automatiquement. Tu en veux une troisième ? Le tiling s'adapte. Tout se fait au clavier, sans que tu aies à toucher la souris.

Le gros avantage : c'est **100% gratuit**, **open-source** (licence MIT), et maintenu activement sur GitHub. Pas de licence, pas d'abonnement, pas de freemium qui te bloque derrière un paywall.

## Installation rapide en 30 secondes

La méthode la plus simple, c'est Homebrew. Si tu n'as pas encore installé Homebrew, c'est le moment, c'est le gestionnaire de paquets indispensable sur macOS que j'utilise dans mon guide des [10 outils low-tech macOS](/10-outils-low-tech-macos-guide-complet/).

```bash
brew install --cask amethyst
```

Une fois installé, ouvre Amethyst depuis le dossier Applications. Tu verras une icône en forme de diamant violet apparaître dans ta barre de menus. C'est tout.

Alternativement, tu peux télécharger le `.dmg` directement depuis la page [GitHub Releases d'Amethyst](https://github.com/ianyh/Amethyst/releases).

## Configuration initiale : Accorder les permissions

Amethyst a besoin d'une permission pour fonctionner : **l'Accessibilité**. Sans ça, l'app ne peut pas déplacer ni redimensionner tes fenêtres.

Au premier lancement, macOS va te demander d'accorder cette permission. Va dans :

```bash
Réglages Système → Confidentialité et sécurité → Accessibilité
```

Coche **Amethyst** dans la liste. Si elle n'apparaît pas, clique sur le `+`, navigue jusqu'à Applications et sélectionne Amethyst.

Cette étape est **obligatoire**. Sans elle, Amethyst ne fait absolument rien. Tu peux passer 10 minutes à te demander pourquoi ça ne marche pas, je te dis ça parce que ça m'est arrivé. 😅

## Les layouts : choisir comment tes fenêtres s'organisent

Amethyst propose plusieurs layouts de tiling prédéfinis. Tu bascules entre eux avec un raccourci clavier (par défaut : `⌥⇧Espace`).

Voici les principaux :

### Tall (le classique)

C'est le layout par défaut. Une fenêtre principale à gauche prend environ 60% de l'espace, et les autres fenêtres s'empilent à droite en colonnes égales. Parfait pour travailler avec un éditeur de code à gauche et un terminal + navigateur à droite.

### Wide

Le même principe, mais inversé : la fenêtre principale est en haut, les autres s'empilent en dessous. Idéal pour les écrans ultra-wide.

### Fullscreen

Chaque fenêtre occupe tout l'écran, et tu navigues entre elles. C'est le mode "focus total" quand tu veux éviter les distractions.

### Column

Toutes les fenêtres se répartissent en colonnes égales. 2 fenêtres = 50/50. 3 fenêtres = 33/33/33. Simple, efficace, démocratique.

### Row

Pareil que Column, mais en lignes horizontales. Utile pour les écrans en portrait ou pour comparer du code ligne par ligne.

### BSP (Binary Space Partitioning)

Le mode le plus avancé. Chaque nouvelle fenêtre coupe l'espace disponible en deux de manière récursive. Tu obtiens un tiling intelligent qui s'adapte à n'importe quel nombre de fenêtres.

### Floating

Ce n'est pas vraiment un layout, mais c'est essentiel : tu peux mettre certaines applications en mode flottant pour qu'Amethyst ne les touche pas. Pratique pour les apps comme Spotify, les fenêtres de chat, ou les pop-ups système.

## Les raccourcis clavier essentiels

Voici les raccourcis par défaut (tous utilisent la touche `⌥⇧` comme modificateur) :

| Action | Raccourci |
|--------|-----------|
| Changer de layout | `⌥⇧Espace` |
| Focus fenêtre suivante | `⌥⇧J` |
| Focus fenêtre précédente | `⌥⇧K` |
| Swap avec fenêtre suivante | `⌥⇧↩` |
| Rétrécir fenêtre principale | `⌥⇧H` |
| Agrandir fenêtre principale | `⌥⇧L` |
| Basculer vers écran suivant | `⌥⇧W` |
| Basculer vers écran précédent | `⌥⇧E` |
| Mettre en fullscreen | `⌥⇧D` |
| Relancer le layout | `⌥⇧Z` |

Personnellement, j'ai rapidement remappé les raccourcis pour qu'ils collent mieux à ma configuration. Dans les préférences d'Amethyst (`⌥,`), onglet **Shortcuts**, tu peux tout personnaliser.

Si tu utilises déjà [Raycast](/raycast-macos-outil-productivite-ultime/) comme launcher, tu peux même créer des hotkeys Raycast pour contrôler Amethyst via des scripts, c'est un combo de productivité redoutable.

## Amethyst vs les alternatives : le comparatif

Tu te demandes peut-être pourquoi choisir Amethyst plutôt qu'un autre gestionnaire de fenêtres. Voici la vérité crue.

### Amethyst vs Magnet

[Magnet](/magnet-macos-gestionnaire-fenetres-guide-complet/) est une app payante (environ 9€) qui te permet de snapper des fenêtres avec des raccourcis clavier ou en les glissant vers les bords de l'écran. C'est excellent pour un usage classique.

Mais Magnet ne fait pas du tiling automatique. Tu dois **toi-même** décider où va chaque fenêtre. Avec Amethyst, c'est le système qui s'occupe de tout. Tu ouvres une app, elle se place. Tu en fermes une, le reste se réajuste.

**Verdict** : Magnet pour le contrôle manuel, Amethyst pour l'automatisation.

### Amethyst vs Rectangle

Rectangle est gratuit et open-source, comme Amethyst. Il fonctionne sur le même principe que Magnet (snap manuel avec raccourcis). C'est une excellente alternative gratuite si tu veux juste du snapping.

Même distinction que Magnet : Rectangle ne tile pas automatiquement. C'est un gestionnaire de snapping, pas un tiling manager pur.

**Verdict** : Rectangle est plus simple à prendre en main. Amethyst demande un peu d'adaptation mais offre un gain de productivité supérieur.

### Amethyst vs Yabai

Yabai est le tiling manager le plus puissant sur macOS. Il peut créer des espaces virtuels dynamiques, gérer des règles de floating complexes, et offre un contrôle quasi-total sur le window server.

Mais Yabai nécessite de **désactiver SIP** (System Integrity Protection) pour certaines fonctionnalités avancées. C'est un gros non pour un Mac professionnel ou si tu tiens à la sécurité de ton système.

Amethyst reste en user-space et n'a besoin que de la permission Accessibilité. C'est moins puissant, mais infiniment plus sûr et simple à maintenir.

**Verdict** : Yabai pour les power users prêts à bidouiller le système. Amethyst pour tout le monde.

## Astuces pour bien démarrer avec Amethyst

Passer à un tiling window manager demande une période d'adaptation. Voici ce qui m'a aidé à m'y faire sans rage-quit au bout de 10 minutes.

### Commence par le layout Tall

Le layout Tall est le plus intuitif. Une grande fenêtre à gauche (ton éditeur), et le reste s'empile à droite. C'est le setup classique "développeur" et il fonctionne immédiatement.

### Configure tes apps flottantes

Certaines apps n'ont rien à faire dans un tiling manager. Les fenêtres de préférences système, les petites pop-ups de confirmation, les apps de musique... Ajoute-les à la liste des apps flottantes dans les préférences d'Amethyst.

Tu peux aussi mettre une app en flottant temporairement avec le raccourci `⌥⇧T`.

### Désactive le tiling natif de macOS

Si tu es sur macOS Sequoia ou plus récent, le window tiling natif peut entrer en conflit avec Amethyst. Va dans Réglages Système → Bureau et Dock, et désactive les options de tiling automatique.

### Utilise plusieurs espaces virtuels

Amethyst gère mal (ou pas) les fenêtres sur plusieurs bureaux virtuels en même temps. Le workflow optimal, c'est un espace virtuel = un contexte. Par exemple : Bureau 1 pour le dev, Bureau 2 pour la navigation, Bureau 3 pour la communication.

### Personnalise les marges

Par défaut, Amethyst colle les fenêtres les unes contre les autres. Si tu trouves ça oppressant, augmente la marge dans les préférences (`⌥,` → **General** → **Window Margins**). 5-10 pixels suffisent à rendre l'ensemble plus aéré.

## Configuration avancée via le fichier JSON

Pour les config geeks, Amethyst expose un fichier de configuration JSON que tu peux éditer à la main. Va dans les préférences, onglet **General**, et clique sur **Export/Import JSON**.

Voici un exemple de config minimaliste optimisée pour un écran 16 pouces :

```json
{
  "window-margins": 5,
  "window-margin-size": 5,
  "floating": [
    "com.apple.systempreferences",
    "com.apple.ActivityMonitor",
    "com.spotify.client"
  ],
  "layouts": [
    "tall",
    "wide",
    "fullscreen",
    "column",
    "bsp"
  ],
  "mod1": [
    "option",
    "shift"
  ],
  "mod2": [
    "option",
    "shift",
    "control"
  ]
}
```

Tu peux aussi modifier ce fichier directement à l'emplacement `~/.amethyst.yml` ou via l'interface graphique, les deux se synchronisent.

## Les limites d'Amethyst (autant être honnête)

Amethyst n'est pas parfait. Voici les points qui peuvent te faire hésiter.

### Certains apps résistent

Les apps qui utilisent des fenêtres non standard (certaines apps Electron mal codées, des fenêtres de plugin VST, etc.) peuvent se comporter bizarrement avec Amethyst. Elles peuvent refuser de se redimensionner, ou apparaître à des tailles étranges.

La solution : les ajouter à la liste des apps flottantes. C'est un peu pénible au début, mais une fois configuré, tu n'y penses plus.

### Pas de support natif multi-écran avancé

Amethyst gère le multi-écran, mais moins finement que Yabai. Tu ne peux pas facilement faire traverser une fenêtre d'un écran à l'autre tout en maintenant le tiling. C'est possible, mais moins fluide.

### Courbe d'apprentissage

Les premiers jours, tu vas régulièrement te battre contre Amethyst. Tu vas ouvrir une fenêtre, te dire "mais je la voulais là, pas là !", et devoir la repositionner manuellement. C'est normal.

Au bout d'une semaine, ce qui paraissait contraignant devient naturel. Au bout d'un mois, tu ne pourras plus revenir en arrière.

## Mon workflow quotidien avec Amethyst

Voici concrètement comment j'utilise Amethyst dans ma journée de travail.

**Le matin**, j'ouvre mon Mac. Amethyst se lance automatiquement via les éléments de connexion. J'ouvre mon éditeur de code (VS Code) : il prend la moitié gauche de l'écran. J'ouvre un terminal (iTerm) : il se place en haut à droite. J'ouvre un navigateur pour la doc : il se place en bas à droite. Tout est parfaitement aligné, sans que j'aie touché la souris.

**Quand je code**, je reste en layout Tall. Si j'ai besoin de plus d'espace pour le terminal, je fais `⌥⇧L` pour agrandir la zone principale.

**Quand j'écris un article** (comme celui-ci), je passe en layout Fullscreen. Une seule fenêtre, zéro distraction.

**Quand je fais du multitâche** (Slack + mail + calendrier), je passe en Column pour avoir tout visible d'un coup.

Ce qui me fait gagner le plus de temps, c'est la suppression de la friction. Je n'ai plus à penser à l'organisation de mes fenêtres. C'est automatique. Mon cerveau reste concentré sur le travail, pas sur le window management.

## FAQ : Les questions qu'on me pose souvent

### Amethyst est-il compatible avec Apple Silicon (M1/M2/M3/M4) ?

Oui, Amethyst est compilé en natif pour Apple Silicon depuis la version 0.16. Aucune émulation Rosetta 2 nécessaire.

### Puis-je utiliser Amethyst avec un clavier AZERTY ?

Oui, mais tu devras probablement remapper certains raccourcis par défaut qui utilisent des touches spécifiques au QWERTY. La configuration se fait dans les préférences de l'app.

### Amethyst consomme-t-il beaucoup de ressources ?

Non, Amethyst consomme environ 20-40 Mo de RAM et moins de 1% de CPU au repos. C'est un outil léger comparé à d'autres gestionnaires de fenêtres.

### Quelle est la différence entre Amethyst et Yabai ?

Amethyst est un tiling manager en user-space qui utilise les API macOS standard. Yabai modifie le window server de macOS via un injection de code, ce qui lui donne plus de contrôle mais nécessite de désactiver SIP.

## Conclusion : Est-ce que ça vaut le coup ?

Si tu passes ta journée sur macOS avec plusieurs fenêtres ouvertes, que tu détestes perdre du temps à les repositionner, et que tu aimes piloter ton ordinateur au clavier, **Amethyst est un game-changer**.

C'est gratuit, open-source, et une fois la configuration initiale passée, il devient invisible. Il fait son travail en arrière-plan, et tes fenêtres sont toujours exactement là où elles devraient être.

N'attends pas d'être un expert Linux pour essayer un tiling window manager. Amethyst rend cette expérience accessible à n'importe quel utilisateur de macOS. Installe-le, donne-lui une semaine, et dis-moi si tu peux encore t'en passer.

**Lien utile** : [Repository GitHub d'Amethyst](https://github.com/ianyh/Amethyst), pour les releases, les issues, et la documentation complète.
