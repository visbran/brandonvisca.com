---
title: "Swish macOS : gère tes fenêtres avec des gestures trackpad (4 doigts)"
description: "Swish macOS : gère tes fenêtres avec des gestes trackpad à 4 doigts. Guide complet d'installation, configuration et avis après test approfondi."
pubDatetime: "2026-08-19T06:00:00.000Z"
modDatetime: "2026-08-19T06:00:00.000Z"
author: Brandon Visca
tags:
  - macos
  - productivite
  - intermediaire
  - gestion-fenetres
  - trackpad
featured: false
draft: false
focusKeyword: swish macos
faqs:
  - question: "Swish est-il compatible avec les puces Apple Silicon (M1/M2/M3/M4) ?"
    answer: "Oui, Swish fonctionne en natif sur Apple Silicon et Intel depuis macOS 10.13 High Sierra jusqu'à macOS 15 Sequoia."
  - question: "Swish fonctionne-t-il avec une Magic Mouse ou une souris classique ?"
    answer: "Non. Swish est conçu exclusivement pour le trackpad Apple (MacBook, Magic Trackpad). Une souris ne peut pas reproduire les gestes multi-doigts nécessaires."
  - question: "Swish est-il un abonnement ou un achat unique ?"
    answer: "C'est un achat unique d'environ 16$. Pas d'abonnement mensuel, pas de cloud, licence perpétuelle."
  - question: "Combien de gestes Swish propose-t-il ?"
    answer: "Swish supporte plus de 30 gestes trackpad personnalisables : swipe dans 8 directions, pinch ouvert/fermé, double-tap, et combinaisons sur la barre de titre."
  - question: "Swish ou Magnet : lequel choisir ?"
    answer: "Magnet est meilleur pour le clavier et le drag \u0026 drop avec la souris. Swish est supérieur si tu utilises principalement le trackpad et que tu veux une gestion entièrement gestuelle."
ogImage: ""
---
> 💡 **TL;DR**
> - Swish transforme ton trackpad en télécommande de fenêtres : swipe à 4 doigts pour snapper, pinch pour quitter, tap pour maximiser
> - Prix unique d'environ 16$, développé par Highly Opinionated, compatible macOS 10.13+
> - Parfait pour les users MacBook qui détestent quitter le trackpad pour gérer leurs fenêtres
>
> ## Table des matières
>
> - [Swish macOS : qu'est-ce que c'est exactement ?](#swish-macos--quest-ce-que-cest-exactement-)
> - [Les gestes Swish : le répertoire complet](#les-gestes-swish--le-répertoire-complet)
> - [Installation et première configuration](#installation-et-première-configuration)
> - [Grille, zones et personnalisation avancée](#grille-zones-et-personnalisation-avancée)
> - [Swish vs les alternatives : où il se place](#swish-vs-les-alternatives--où-il-se-place)
> - [Les points forts de Swish](#les-points-forts-de-swish)
> - [Les limites et inconvénients](#les-limites-et-inconvénients)
> - [Mon workflow quotidien avec Swish](#mon-workflow-quotidien-avec-swish)
> - [Astuces pour bien maîtriser Swish](#astuces-pour-bien-maîtriser-swish)
> - [Conclusion : Est-ce que Swish vaut son prix ?](#conclusion--est-ce-que-swish-vaut-son-prix-)
> - [FAQ Swish macOS](#faq-swish-macos)

## Introduction : Quand le trackpad devient ton outil de window management

Sur macOS, on a deux écoles pour gérer ses fenêtres.

Première école : les fans de la souris. Ils glissent, ils redimensionnent, ils ragent quand la fenêtre refuse de s'aligner pile sur la moitié de l'écran. Deuxième école : les addicts du clavier. Raccourcis à gogo, toujours les mains sur le clavier, jamais un mouvement de souris inutile.

Et il y a une troisième école, celle que beaucoup oublient : **les accros du trackpad**. Ceux qui utilisent un MacBook Pro ou un Magic Trackpad et qui ont le geste à quatre doigts dans le sang. Pour eux, sortir les doigts du trackpad pour appuyer sur un raccourci clavier ou attraper la souris, c'est une fracture dans le flux de travail.

**Swish macOS** est fait pour cette troisième école. C'est un gestionnaire de fenêtres qui ne se contrôle pas au clavier ni à la souris. Il se contrôle **au trackpad**, avec des gestes. Et pas n'importe lesquels : des gestes précis, rapides et absolument addictifs.

Si tu as déjà utilisé [Magnet](/magnet-macos-gestionnaire-fenetres-guide-complet/) ou [Amethyst](/amethyst-macos-tiling-window-manager/), tu sais à quel point un bon gestionnaire de fenêtres change la vie. Swish apporte une approche totalement différente : au lieu de snapper avec des raccourcis ou du drag and drop, tu **swipes**.

## Swish macOS : qu'est-ce que c'est exactement ?

Swish macOS est un utilitaire macOS développé par **Highly Opinionated** (les mêmes qui font Yoink et Transnomino). Son principe est simple : utiliser les gestes natifs du trackpad pour organiser, déplacer et redimensionner les fenêtres.

Contrairement à Magnet qui se base sur le glisser-déposer vers les bords ou des raccourcis clavier, Swish s'active **directement sur la barre de titre** des fenêtres avec des gestes trackpad. Tu poses tes 4 doigts sur le trackpad, tu swipes vers le haut, et la fenêtre se maximise. Tu swipes vers la gauche, elle occupe la moitié gauche. C'est instantané, fluide et terriblement satisfaisant.

Swish fonctionne avec **tous les trackpads Apple** : celui des MacBook Pro/Air, le Magic Trackpad, et même les trackpads des Magic Keyboard avec touch ID. Il nécessite macOS 10.13 High Sierra minimum, mais tourne parfaitement sur macOS 15 Sequoia et les puces Apple Silicon.

### Les specs techniques

| Caractéristique | Détail |
|---|---|
| **Prix** | Environ 16$ (achat unique, pas d'abonnement) |
| **Développeur** | Highly Opinionated |
| **macOS minimum** | macOS 10.13 High Sierra |
| **Compatibilité** | Apple Silicon et Intel natif |
| **Poids** | ~15 Mo |
| **Modèle** | Licence perpétuelle, pas de cloud |
| **Site** | highlyopinionated.co/swish |

## Les gestes Swish macOS : le répertoire complet

Swish exploite le trackpad avec une granularité impressionnante. Voici ce que tu peux faire.

### Snap et redimensionnement (les gestes de base)

Ces gestes s'activent quand tu swipes **sur la barre de titre** d'une fenêtre avec **4 doigts** :

- **Swipe vers le haut** : Maximiser la fenêtre
- **Swipe vers le bas** : Restaurer la taille (dé-maximiser) ou minimiser selon la config
- **Swipe vers la gauche** : Occuper la moitié gauche de l'écran
- **Swipe vers la droite** : Occuper la moitié droite de l'écran
- **Swipe vers un coin** (diagonale haut-gauche, haut-droite, bas-gauche, bas-droite) : Occuper le quart correspondant

Ce qui change tout, c'est que tu ne quittes pas le trackpad. Tes doigts restent posés, tu swipes, et c'est fait. Pas besoin d'aller jusqu'au bord de l'écran, pas besoin de viser une zone de snapping. Le geste suffit.

### La grille personnalisable

Swish ne se limite pas aux moitiés et aux quarts. Il propose une **grille de snapping** personnalisable. Par défaut, tu peux diviser ton écran en 2x2, 3x2, ou même 3x3 selon tes besoins.

Quand la grille est active, un swipe vers le haut-gauche ne place pas juste la fenêtre en quart supérieur gauche : il peut la placer dans la cellule précise de la grille que tu vises. C'est particulièrement utile sur les grands écrans (27 pouces et plus) où un simple demi-écran fait trop large.

Pour activer la grille : **Préférences Swish > Grille** et choisis ta configuration (2x2, 3x2, 3x3, etc.).

### Pinch pour fermer et minimiser

- **Pinch fermé** (resserrer 4 doigts) sur la barre de titre : **Fermer** la fenêtre
- **Double-tap** avec 4 doigts : **Minimiser** la fenêtre dans le Dock

Ces gestes sont un peu plus techniques à maîtriser, mais une fois le muscle memory acquis, c'est bluffant de vitesse. Tu lis un article dans Safari, pinch fermé, et la fenêtre disparaît. Pas de clic sur la croix rouge, pas de raccourci clavier. Juste un geste.

### Déplacement entre écrans

Si tu utilises un setup multi-écrans, Swish gère aussi le déplacement d'une fenêtre d'un écran à l'autre :

- **Swipe vers la gauche** sur une fenêtre déjà à gauche : elle traverse vers l'écran précédent
- **Swipe vers la droite** sur une fenêtre déjà à droite : elle traverse vers l'écran suivant

C'est logique et ça évite d'avoir à traîner la fenêtre manuellement d'un écran à l'autre, ce qui est toujours un peu pénible sur macOS.

## Installation et première configuration

Swish n'est pas sur le Mac App Store. Il se télécharge directement depuis le site du développeur.

### Étape 1 : Téléchargement

1. Va sur [highlyopinionated.co/swish](https://highlyopinionated.co/swish)
2. Télécharge la dernière version (DMG)
3. Ouvre le DMG et glisse Swish dans `/Applications`

### Étape 2 : Permissions obligatoires

Au premier lancement, macOS va te demander plusieurs permissions. Sans elles, Swish ne fonctionne pas.

**1. Accessibilité**

Swish a besoin de cette permission pour déplacer et redimensionner les fenêtres.

```bash
Réglages Système → Confidentialité et sécurité → Accessibilité
```

Ajoute Swish et coche la case.

**2. Entrées au clavier (Keyboard Monitoring)**

Swish surveille certaines touches pour détecter quand tu es sur la barre de titre. C'est totalement local, pas de transmission de données.

```bash
Réglages Système → Confidentialité et sécurité → Entrées au clavier
```

Ajoute Swish ici aussi.

### Étape 3 : Configuration recommandée

Ouvre Swish (icône dans la barre de menu) et va dans **Preferences**.

**Onglet General :**

- Launch Swish at login : **coché** (indispensable)
- Show menu bar icon : laisse coché au début, tu peux le désactiver plus tard

**Onglet Gestures :**

- Sensitivity : **Normal** pour commencer. Augmente si tu trouves que les gestes ne répondent pas assez vite
- Require 4 fingers : **coché** (par défaut). Swish utilise 4 doigts pour éviter les conflits avec les gestes système macOS (qui utilisent souvent 3 doigts)

**Onglet Grille :**

- Grid size : **2x2** pour un usage classique, **3x2** si tu as un grand écran et que tu veux plus de finesse
- Show grid overlay : **coché** au début pour visualiser les zones. Décoche quand tu connais les gestes par cœur

### Étape 4 : Test rapide

Ouvre n'importe quelle fenêtre (Safari, Notes, ce que tu veux). Pose 4 doigts sur le trackpad, positionnés sur la barre de titre de la fenêtre. Swipe vers la gauche. La fenêtre doit occuper immédiatement la moitié gauche de l'écran.

Si ça ne marche pas, vérifie que tes 4 doigts sont bien reconnus par macOS dans **Réglages Système > Trackpad > Gestures avancés**. Et assure-toi que Swish est bien autorisé en Accessibilité.

## Grille, zones et personnalisation avancée

Swish est plus puissant qu'il n'y paraît. Derrière son apparente simplicité, il cache des options de personnalisation très poussées.

### Les zones de snapping

Quand tu actives l'overlay de grille (option "Show grid overlay"), Swish affiche une grille semi-transparente sur ton écran quand tu commences un geste. Cela te permet de voir exactement où va atterrir ta fenêtre avant de lâcher tes doigts.

C'est particulièrement utile pour les nouveaux utilisateurs. Après quelques jours, tu n'as plus besoin de l'overlay : le muscle memory fait le travail.

### Désactivation par application

Certaines applications n'apprécient pas qu'on leur fasse la loi avec des gestes. Swish permet de désactiver son comportement par app.

**Préférences > Excluded Apps**

Ajoute ici les apps qui posent problème. Typiquement : les jeux en plein écran, certaines apps de design comme Figma (qui ont leur propre système de panneaux), ou les apps de virtualisation.

### Sensibilité et gestes inversés

Dans les préférences avancées, tu peux ajuster :

- La **sensibilité du swipe** (vitesse minimale pour déclencher l'action)
- L'**inversion des directions** (utile si tu trouves que gauche/droite est contre-intuitif)
- Le **délai de déclenchement** (temps avant que Swish considère que tu es en train de faire un geste)

## Swish vs les alternatives : où il se place

J'ai déjà parlé de [Magnet](/magnet-macos-gestionnaire-fenetres-guide-complet/) et [Amethyst](/amethyst-macos-tiling-window-manager/) sur ce blog. Voyons où Swish se situe dans l'écosystème.

### Swish vs Magnet

Magnet est le roi du drag & drop et des raccourcis clavier. Tu glisses une fenêtre vers un bord, elle snap. Tu appuies sur `⌃ + ⌥ + ←`, elle va à gauche.

Swish ne fait pas ça. Swish ne fait pas de raccourcis clavier. Si tu es un puriste du clavier qui déteste le trackpad, Magnet (ou Amethyst) est fait pour toi.

Mais si tu passes ta journée les doigts sur le trackpad, Swish est **infiniment plus fluide**. Pas besoin de viser le bord de l'écran, pas besoin de mémoriser des raccourcis. Tu swipes, c'est fait.

### Swish vs Rectangle

Rectangle est gratuit et open-source. Il fait à peu près la même chose que Magnet (snap + raccourcis). Même constat : Rectangle est clavier/souris, Swish est trackpad. Ce n'est pas la même cible.

### Swish vs Amethyst

Amethyst est un tiling window manager automatique. Tu ouvres une fenêtre, il la place selon un layout prédéfini. Zéro geste, zéro réflexion, mais une courbe d'apprentissage plus rude.

Swish est le contraire : c'est manuel, gestuel, et très visuel. Amethyst organise tout pour toi. Swish te laisse le contrôle total, mais avec la vitesse du geste.

**Verdict** : Amethyst pour les devs qui veulent un workflow entièrement au clavier et automatique. Swish pour ceux qui préfèrent le contrôle tactile et visuel.

### Swish vs le tiling natif de macOS Sequoia

macOS 15 Sequoia a introduit un window tiling natif accessible depuis le bouton vert des fenêtres. C'est gratuit, intégré, et ça marche.

Mais le tiling natif demande de cliquer sur un bouton, puis de choisir dans un menu. Avec Swish, tu poses 4 doigts et tu swipes. La différence de vitesse est énorme quand tu le fais 50 fois par jour.

## Les points forts de Swish macOS

Après avoir testé Swish intensivement sur un MacBook Pro M3 et un setup avec écran externe + Magic Trackpad, voici ce qui m'a séduit.

### 1. La fluidité du geste

C'est le gros point fort. Le geste est instantané, sans latence perçue. Les fenêtres se repositionnent avec une animation rapide et propre. On est loin des utilitaires qui rament ou qui plantent quand tu swipes trop vite.

### 2. Pas besoin de quitter le trackpad

Sur un MacBook, ton workflow trackpad n'est jamais interrompu. Tu navigues dans Safari avec des gestes à 2 doigts, tu switches d'app avec 4 doigts (geste système), et tu organises tes fenêtres avec Swish, toujours avec 4 doigts. C'est cohérent.

### 3. La grille personnalisable

Le fait de pouvoir choisir entre 2x2, 3x2, 3x3, ou des configurations personnalisées fait de Swish un outil adaptable à n'importe quel écran. Sur un 14 pouces, 2x2 suffit. Sur un 32 pouces 4K, un 3x3 devient très utile.

### 4. Le pinch pour fermer

C'est un détail, mais c'est tellement satisfaisant. Swipe, pinch, tout se fait au trackpad. Tu n'as plus à viser la petite croix rouge en haut à gauche des fenêtres.

## Les limites et inconvénients

Autant être honnête : Swish n'est pas parfait pour tout le monde.

### 1. Trackpad obligatoire

Si tu utilises une souris en permanence et que ton trackpad est désactivé, Swish ne te servira à rien. C'est un outil conçu pour le trackpad, point final. Sur un Mac mini avec souris classique, oublie.

### 2. Pas de raccourcis clavier

Contrairement à Magnet, Rectangle ou Amethyst, Swish n'offre aucun raccourci clavier. Si tu es sur un clavier externe sans trackpad, tu ne peux pas utiliser Swish. C'est un choix de design, mais ça limite l'audience.

### 3. Le prix

16$ pour un gestionnaire de fenêtres, c'est cher comparé à Magnet (5$) ou Rectangle (gratuit). Cependant, c'est un achat unique et perpétuel. Pas d'abonnement, pas de freemium.

### 4. Courbe d'apprentissage des gestes avancés

Les gestes de base (swipe gauche/droite/haut/bas) s'apprennent en 5 minutes. Les gestes avancés comme le pinch fermé pour fermer une fenêtre demandent plus de pratique. Au début, tu vas fermer des fenêtres par accident. C'est normal.

### 5. Conflits potentiels avec les gestes système

macOS utilise déjà pas mal de gestes à 3 et 4 doigts (Mission Control, App Exposé, changer de bureau). Swish utilise 4 doigts pour éviter les conflits avec les gestes à 3 doigts, mais il faut s'assurer que tu n'as pas activé des gestes système à 4 doigts qui pourraient entrer en conflit.

Vérifie dans **Réglages Système > Trackpad > Gestures avancés** que tes gestes système à 4 doigts ne rentrent pas en collision avec Swish.

## Mon workflow quotidien avec Swish macOS

Voici comment j'utilise Swish concrètement dans ma journée.

**Le matin**, j'ouvre mon MacBook. Swish est déjà lancé (auto-start). J'ouvre Safari pour les mails : swipe 4 doigts vers le haut sur la barre de titre, Safari maximise. J'ouvre iTerm pour le terminal : swipe vers la droite, il occupe la moitié droite. J'ouvre VS Code : swipe vers la gauche, il occupe la moitié gauche.

Tout est aligné en 3 gestes. Pas de drag and drop, pas de raccourcis clavier.

**Pendant que je code**, j'ai souvent besoin de consulter la documentation. J'ouvre une nouvelle fenêtre Safari, je la pousse en quart inférieur droit avec un swipe diagonal. L'écran est maintenant partagé en trois zones : code à gauche, terminal en haut à droite, doc en bas à droite.

**Quand je finis une tâche**, je ferme les fenêtres avec un pinch fermé sur chaque barre de titre. C'est plus rapide que de viser la croix rouge.

**En fin de journée**, je branche mon MacBook sur un écran externe 27 pouces. La grille passe en 3x2 pour exploiter la largeur. Je déplace les fenêtres d'un écran à l'autre avec des swipes latéraux.

Ce qui me fait gagner du temps, c'est la **continuité du geste**. Je ne quitte jamais le trackpad. Pas de context switch entre souris, clavier et trackpad. C'est un flux continu.

## Astuces pour bien maîtriser Swish

Si tu te lances, voici quelques tips pour éviter la frustration des premiers jours.

### Commence par les gestes simples

Maîtrise d'abord les 4 directions de base (haut, bas, gauche, droite) avant d'essayer les diagonales et le pinch. Les gestes simples couvrent 80% de l'usage.

### Garde l'overlay visible au début

Laisse l'option "Show grid overlay" activée pendant une semaine. Elle te montre visuellement où va atterrir ta fenêtre. Une fois que tu anticipes les placements sans regarder l'écran, tu peux la désactiver pour plus de discrétion.

### Vérifie tes gestes système

Va dans **Réglages Système > Trackpad** et regarde quels gestes à 4 doigts sont activés. Désactive ceux que tu n'utilises pas pour éviter les conflits. Personnellement, je désactive "App Exposé" à 4 doigts car je ne l'utilise jamais.

### Utilise un Magic Trackpad en setup fixe

Si tu as un MacBook branché sur un écran externe avec clavier et souris, garde un Magic Trackpad à côté du clavier. Swish vaut vraiment le coup sur un trackpad physique Apple. Les trackpads Windows ou les souris avec gestes ne donnent pas la même précision.

### Combine avec Raycast pour le lancement d'apps

[Raycast](/raycast-macos-outil-productivite-ultime/) gère le lancement d'applications avec `⌘ + Espace`. Swish gère l'organisation des fenêtres au trackpad. Les deux cohabitent parfaitement : tu lances avec Raycast, tu organises avec Swish.

## Conclusion : Est-ce que Swish macOS vaut son prix ?

Swish est cher pour un gestionnaire de fenêtres. 16$, c'est le triple de Magnet et l'infini de Rectangle (qui est gratuit).

Mais Swish ne fait pas la même chose. C'est le seul outil à proposer une gestion complète des fenêtres **exclusivement par gestes trackpad**. Si tu es un utilisateur de MacBook qui vit sur le trackpad, cette différence change tout.

La vraie question n'est pas "est-ce que Swish vaut 16$ ?". La vraie question est : **est-ce que tu utilises suffisamment le trackpad pour rentabiliser l'investissement ?**

Si tu passes ta journée sur un MacBook Pro avec les doigts sur le trackpad, Swish deviendra aussi indispensable que le copier-coller. Si tu es sur un Mac mini avec une souris Logitech et que tu détestes le trackpad, passe ton chemin et prends Magnet ou Rectangle.

Pour ma part, Swish a trouvé sa place dans mon workflow quotidien. Il ne remplace pas Magnet sur mes machines desktop sans trackpad, mais sur mon MacBook Pro, c'est devenu un réflexe.

**Lien utile** : [Site officiel de Swish](https://highlyopinionated.co/swish) pour télécharger l'app et consulter la documentation officielle.

## FAQ Swish macOS

**Swish est-il compatible avec les puces Apple Silicon (M1/M2/M3/M4) ?**

Oui, Swish fonctionne en natif sur Apple Silicon et Intel depuis macOS 10.13 High Sierra jusqu'à macOS 15 Sequoia.

**Swish fonctionne-t-il avec une Magic Mouse ou une souris classique ?**

Non. Swish est conçu exclusivement pour le trackpad Apple (MacBook, Magic Trackpad). Une souris ne peut pas reproduire les gestes multi-doigts nécessaires.

**Swish est-il un abonnement ou un achat unique ?**

C'est un achat unique d'environ 16$. Pas d'abonnement mensuel, pas de cloud, licence perpétuelle.

**Combien de gestes Swish propose-t-il ?**

Swish supporte plus de 30 gestes trackpad personnalisables : swipe dans 8 directions, pinch ouvert/fermé, double-tap, et combinaisons sur la barre de titre.

**Swish ou Magnet : lequel choisir ?**

Magnet est meilleur pour le clavier et le drag & drop avec la souris. Swish est supérieur si tu utilises principalement le trackpad et que tu veux une gestion entièrement gestuelle.
