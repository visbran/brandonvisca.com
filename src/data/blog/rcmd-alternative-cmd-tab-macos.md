---
title: "rcmd : Alternative Cmd+Tab réimaginée pour macOS"
description: "rcmd, l'alternative Cmd+Tab macOS : switche entre apps en 1 touche (Right Cmd + lettre), fuzzy search, Space switching instantané, 16 thèmes. Guide complet 2026."
pubDatetime: "2025-11-27T00:00:00+01:00"
modDatetime: "2026-08-24T00:00:00+01:00"
author: Brandon Visca
tags:
  - macos
  - productivite
  - debutant
featured: true
draft: false
focusKeyword: rcmd alternative cmd+tab mac
faqs:
  - question: "rcmd est-il gratuit ?"
    answer: "rcmd coûte 15 € en achat unique (jusqu'à 5 Macs). Une version d'essai de 14 jours est disponible, puis un mode Free reste accessible avec les fonctions de base."
  - question: "Quelle différence entre rcmd et AltTab ?"
    answer: "AltTab améliore Cmd+Tab pour naviguer entre les fenêtres avec des aperçus. rcmd est un app switcher complet qui permet de sauter directement vers une app, de rechercher en fuzzy, de switcher entre Spaces et de sauvegarder des layouts de fenêtres."
  - question: "Que se passe-t-il si deux apps commencent par la même lettre ?"
    answer: "rcmd bascule entre toutes les apps assignées à cette lettre à chaque pression. Tu peux aussi assigner des lettres manuellement dans les préférences pour éviter les collisions."
  - question: "rcmd fonctionne-t-il avec plusieurs Spaces macOS ?"
    answer: "Oui, rcmd bascule vers l'app même si elle est dans un autre Space, avec ou sans animation selon tes réglages. Il peut aussi déplacer une fenêtre vers un autre Space depuis le clavier."
---

> 💡 **TL;DR**
> - Cmd+Tab est lent : 3 à 4 Tab à chaque fois pour atteindre la bonne app
> - rcmd remplace ça par Right Command + la lettre de l'app, accès direct en 0,2 s
> - Un raccourci dédié par app (Right Cmd + S pour Safari, + V pour VS Code)
> - Fuzzy search, Space switching instantané, 16 thèmes et Stages (workspaces)
> - 15 € one-time pour 5 Macs, 14 jours d'essai puis un mode Free

![rcmd app switcher](rcmd-screenshot.webp)

---

## Table des matières

## Introduction : Cmd+Tab, c'est 2005

Cmd+Tab sur macOS est pratique, mais lent.

Tu veux passer de Safari à iTerm2 ? Cmd+Tab, Tab, Tab, Tab... j'ai dépassé, Shift+Tab pour revenir.

Le constat : tu perds 3-4 secondes à chaque fois. Sur une journée de travail, c'est facilement 5-10 minutes de perdues juste à naviguer entre tes apps.

Il existe un outil qui permet de switcher vers n'importe quelle app en une seule combinaison de touches :

Right Command + S = Safari. Right Command + I = iTerm2. Right Command + V = VS Code.

Instantané, précis, sans friction.

**rcmd**, développé par [The Low Tech Guys](https://lowtechguys.com/), repense le switch d'apps sur macOS.

Ce que tu vas apprendre dans ce guide :
- Installer rcmd via Homebrew ou le Mac App Store
- Configurer tes raccourcis personnalisés
- Les nouvelles fonctionnalités (fuzzy search, Spaces, Stages, thèmes)
- Pourquoi c'est différent de Raycast, Alfred ou AltTab
- Troubleshooting des problèmes courants

| App | Raccourci rcmd | Gain vs Cmd+Tab |
|-----|----------------|-----------------|
| Safari | Right Cmd + S | 4 secondes → 0.2s |
| iTerm2 | Right Cmd + I | 3 secondes → 0.2s |
| VS Code | Right Cmd + V | 4 secondes → 0.2s |

- **Résultat** : 10 min/jour gagnées = 60h économisées/an
- **Installation** : 2 minutes chrono (Homebrew ou Mac App Store)
- **Prix** : 15 € one-time (jusqu'à 5 Macs), 14 jours d'essai gratuits

---

## Qu'est-ce que rcmd ?

<video controls style="width:100%;border-radius:8px"><source src="/images/rcmd-demo-app-switch-assign.mp4" type="video/mp4"></video>

**rcmd** (prononce "are-command"), c'est un app switcher reimaginé par [The Low Tech Guys](https://lowtechguys.com/) pour macOS 13.0+. Il transforme la façon de naviguer entre tes applications.

### Le concept en 3 mots

**Right Command + Lettre = App**

Pas de menu. Pas d'interface lourde. Juste le clavier.

![Le concept rcmd](rcmd-app-switcher-ui.webp)

### Pourquoi c'est efficace

- **Muscle memory** : Ton cerveau associe chaque app à sa première lettre
- **Zero latence** : Pas d'overlay lourd, switch instantané
- **Leger** : Invisible en arriere-plan, zero impact sur les performances
- **Compatible Apple Silicon** : Optimise M1/M2/M3/M4
- **14 jours d'essai** : Tu testes sans risque avant d'acheter

---

## Changement important : le passage au payant

**Historique rapide** : rcmd etait gratuit en V2 via le Mac App Store. Le developpeur a annonce un changement de modele.

**Situation actuelle (2026)** :
- **Prix** : 15 € en achat unique
- **Licence** : Jusqu'a 5 Macs
- **Installation** : `brew install rcmd` (hors Mac App Store) ou telechargement direct
- **Mode Free** : Apres les 14 jours d'essai, un mode gratuit limite reste accessible (le switch instantane d'app reste fonctionnel)

**Ce qui n'a pas change** :
- Pas d'abonnement mensuel
- Pas de fonctions cachees derriere un paywall
- Developpement actif et reactif

---

## Installation de rcmd

### Via Homebrew (recommande)

```bash
brew install rcmd
```

### Via le site officiel

1. Telecharge rcmd : [lowtechguys.com/rcmd](https://lowtechguys.com/rcmd/)
2. Deplace l'app dans `/Applications`
3. Lance et autorise dans Reglages Systeme > Confidentialite et securite > Accessibilite

### Premiers pas

1. **Accessibilite** : Autoriser dans Reglages Systeme > Confidentialite
2. **Touche de declenchement** : Par defaut = Right Command (cmd droite)
3. **Lancer au demarrage** : Active dans les preferences

![Configuration rcmd](rcmd-themes-and-styling.webp)

---

## Configuration essentielle en 5 minutes

### Reglages de base recommandes

```
Trigger Key : Right Command (par defaut)
Cycle behavior : Enabled (pour apps avec meme lettre)
Launch at login : Enabled
Show in menu bar : Disabled (minimalisme)
```

**Pourquoi Right Command ?**
- Ta main droite est deja sur les lettres
- Aucun conflit avec les raccourcis systeme existants
- Muscle memory plus naturelle que Left Command

**Claviers externes ?** Si ton clavier n'a pas de Right Command distinct, tu peux changer la trigger key dans les settings (Control, Option, etc.)

---

## Utilisation : Les bases en 3 exemples

### Exemple 1 : Switcher vers une app

Tu veux ouvrir **Safari** ?

```
Right Command + S = Safari se lance/devient active
```

Simple, rapide, efficace.

### Exemple 2 : Apps avec meme premiere lettre

Tu as **Safari**, **Spotify** et **Slack** ?

Premiere pression : Right Command + S -> Safari
Deuxieme pression : Right Command + S -> Spotify
Troisieme pression : Right Command + S -> Slack

**Cycle automatique** entre les apps qui commencent par la meme lettre.

### Exemple 3 : Assigner une lettre custom

Tu veux que **Music.app** s'ouvre avec Right Command + U au lieu de M ?

1. Active Music.app
2. Presse Right Command + Right Option + U
3. C'est fait : desormais, Right Command + U = Music

---

## Fonctionnalites avancees (V2+)

rcmd a beaucoup evolue. Voici ce qui a ete ajoute au-dela du simple switch d'apps :

### 1. Fuzzy search

<video controls style="width:100%;border-radius:8px"><source src="/images/rcmd-demo-fuzzy-search.mp4" type="video/mp4"></video>

Tu ne te souviens pas de la lettre exacte ?

**Right Command + tape le nom de l'app** -> rcmd filtre et trouve instantanement.

Exemple : "ter" trouve iTerm2, Terminal, Hyper...

### 2. Instant Space switching

<video controls style="width:100%;border-radius:8px"><source src="/images/rcmd-demo-space-switching.mp4" type="video/mp4"></video>

Tu travailles avec plusieurs Spaces virtuels ?

- **Right Command + chiffre** = Switch vers le Space correspondant
- **Sans animation de glissement** (si configure)
- Tu peux aussi **deplacer une fenetre vers un autre Space** et la suivre, le tout depuis le clavier

### 3. Stages : sauvegarder des layouts de fenetres

**Stages** te permet de sauvegarder et restaurer des configurations de fenetres completes.

Cas d'usage concret :
- Un layout "Developpement" (VS Code + iTerm2 + Safari)
- Un layout "Ecriture" (Obsidian + Music)
- Un layout "Admin" (iTerm2 + Snipe-IT + Grafana)

Un raccourci -> tout se remet en place.

### 4. Window jumping

- **Option + lettre** = Saute vers une fenetre specifique (pas juste l'app)
- **Cmd + backtick** = Cycle entre les fenetres de la meme app

### 5. Keylume : hints a l'ecran

rcmd s'integre avec **Keylume**, le clavier virtuel companion, pour afficher les lettres assignees directement sur ton ecran pendant l'utilisation.

### 6. 16 themes integres

rcmd propose maintenant **16 themes visuels** avec personnalisation etendue :

![Themes rcmd](rcmd-themes-and-styling.webp)

| Theme | Ambiance |
|-------|----------|
| Frost | Clair et epure |
| Noir | Sobre et discret |
| Warm | Tons chaleureux |

![Theme Frost](rcmd-theme-frost.webp)
![Theme Noir](rcmd-theme-noir.webp)
![Theme Warm](rcmd-theme-warm.webp)

### 7. Mouse follows the focused app

Une option pratique : **la souris suit automatiquement l'app qui vient de recevoir le focus**. Utile quand tu switch entre plusieurs ecrans.

### 8. Command-Tab replacement ameliore

rcmd peut remplacer le Cmd+Tab natif en filtrant :
- Les fenetres minimisees
- Les fenetres situees sur d'autres Spaces

Resultat : un Cmd+Tab qui ne te montre que ce qui est reellement utile.

---

## rcmd vs les alternatives

### rcmd vs Cmd+Tab (macOS natif)

| Critere | rcmd | Cmd+Tab |
|---------|------|---------|
| **Vitesse** | Instantane | 3-4 Tab parfois |
| **Precision** | Touche dediee par app | Ordre chronologique |
| **Muscle memory** | Lettre = toujours meme app | Position change constamment |
| **Visuel** | Minimaliste (ou theme) | Overlay obligatoire |
| **Prix** | 15 € one-time | Gratuit |

Verdict : rcmd gagne sur la vitesse et la previsibilite.

---

### rcmd vs Raycast / Alfred

| Critere | rcmd | Raycast | Alfred |
|---------|------|---------|--------|
| **Focus** | Switch + search + Spaces | Launcher complet | Launcher + workflows |
| **Simplicite** | Simple | Moyen | Complexe |
| **Latence** | 0 ms | ~50 ms | ~50 ms |
| **Prix** | 15 € | Gratuit (Pro = 96$/an) | Gratuit (Powerpack = 59€) |
| **Courbe apprentissage** | 2 min | 1-2 jours | 1 semaine |

Verdict : rcmd est **complementaire** a Raycast/Alfred.

Usage ideal :
- **rcmd** pour switcher entre apps, rechercher fuzzy, gerer les Spaces
- **Raycast** pour lancer des commandes, snippets, extensions

---

### rcmd vs AltTab

**AltTab** est une autre alternative open source qui ameliore Cmd+Tab.

| Critere | rcmd | AltTab |
|---------|------|--------|
| **Approche** | Touche dediee + search + Spaces | Cmd+Tab ameliore |
| **Previsualisation fenetres** | Option + lettre | Avec thumbnails |
| **Vitesse** | Plus rapide | Legerement plus lent |
| **Simplicite** | Plus simple | Plus de features |
| **Prix** | 15 € | Gratuit |

Verdict : Si tu veux juste **switcher vite** et gerer les Spaces, prends rcmd. Si tu veux **voir** tes fenetres avant de switcher, prends AltTab.

---

## Cas d'usage concrets

### Workflow 1 : Developpeur

```
Right Command + I = iTerm2 (terminal)
Right Command + V = VS Code (editeur)
Right Command + S = Safari (docs/Stack Overflow)
Right Command + N = Notion (notes)
Right Command + P = Postman (API testing)
```

Avant rcmd : Cmd+Tab x4 = 4 secondes
Avec rcmd : Right Command + lettre = 0.2 seconde

Gain sur 8h de dev : ~10 minutes/jour

---

### Workflow 2 : Redaction d'articles (mon cas)

```
Right Command + O = Obsidian (redaction markdown)
Right Command + S = Safari (recherche web)
Right Command + F = Firefox (verif rendu)
Right Command + I = iTerm2 (deploiement)
Right Command + M = Music (concentration)
```

Resultat : Je ne quitte plus mon clavier. Zero friction cognitive.

---

### Workflow 3 : Admin systeme

```
Right Command + I = iTerm2 (SSH serveurs)
Right Command + L = LocalWP (tests WordPress local)
Right Command + S = Safari (docs techniques)
Right Command + N = Notion (runbooks)
Right Command + U = Uptime Kuma (monitoring)
```

Effet : Reactivite accrue pour les incidents. Pas de temps perdu a chercher la bonne app.

---

## Troubleshooting : Les pieges a eviter

### Probleme 1 : Right Command ne fonctionne pas

**Symptomes** : Rien ne se passe quand tu appuies sur Right Command + lettre.

**Causes possibles** :
1. Ton clavier externe envoie le mauvais keycode
2. Tu as mappe Right Command a autre chose dans Reglages Systeme

**Solution** :

1. Verifier les keycodes avec l'app [KeyCodes](https://files.alinpanaitiu.com/KeyCodes.zip)
2. Changer la trigger key dans les settings rcmd (essaye Right Option ou Right Control)

---

### Probleme 2 : Conflit avec Raycast/Alfred

**Symptome** : rcmd et Raycast se marchent dessus sur certaines touches.

**Solution** :

1. Dans Raycast : Utilise Cmd+Space (pas Right Command)
2. Dans rcmd : Utilise Right Command uniquement
3. Aucun conflit = usage complementaire optimal

---

### Probleme 3 : Une app ne se lance pas

**Symptome** : Right Command + S ne fait rien, alors que Safari est installe.

**Causes** :
1. Safari n'est pas dans `/Applications`
2. Le nom de l'app a change

**Solution** :

1. Verifie que l'app est bien dans `/Applications`
2. Assigne manuellement la touche : Ouvre Safari, puis Right Command + Right Option + S

---

### Probleme 4 : Fuzzy search ne trouve pas une fenetre

**Symptome** : Tu tapes le nom d'une fenetre mais elle n'apparait pas.

**Solution** :

1. Verifie que la fenetre n'est pas minimisee (peut etre exclue selon les reglages)
2. Active l'option "Include minimized windows" dans les preferences si necessaire
3. Pour les fenetres sur d'autres Spaces, assure-toi que l'option de suivi inter-Spaces est activee

---

## Alternatives et comparaisons

### Si rcmd ne te convient pas, essaie :

**1. [Raycast](/raycast-macos-outil-productivite-ultime/)** (launcher complet)
- Plus de features (snippets, extensions, AI)
- Courbe d'apprentissage plus longue
- Gratuit avec version Pro

**2. [AltTab macOS : Gestion Fenetres Style Windows (Alternative Gratuite 2025)](/alttab-macos-gestion-fenetres-windows/)** (Cmd+Tab ameliore)
- Previsualisation des fenetres
- Plus visuel que rcmd
- Gratuit et open source

**3. Contexts** (payant, 10$)
- Switch par fenetre (pas par app)
- Recherche fuzzy
- Plus complexe

**4. Witch** (payant, 14$)
- Tres customisable
- Lourd en features
- Overkill pour la plupart

---

## Conclusion : Faut-il adopter rcmd ?

Reponse courte : oui, si tu passes beaucoup de temps a switcher entre apps sur macOS.

**Les 3 raisons d'installer rcmd** :

1. C'est rapide : acces direct aux apps en 0.2s
2. Ca s'installe en 2 minutes (Homebrew ou manuel)
3. Impact immediat sur ta productivite

**Ce que j'aime** :
- Vitesse
- Muscle memory parfaite
- Fuzzy search et Space switching
- Stages pour sauvegarder mes layouts
- 16 themes pour matcher mon setup

**Ce qui pourrait freiner** :
- Payant (15 €), mais pas cher pour un achat unique a vie
- Pas de preview des fenetres integree (Option + lettre fait l'affaire)
- Courbe d'apprentissage de 2-3 jours pour oublier Cmd+Tab

**Mon verdict** : Je l'utilise tous les jours depuis plus d'un an, et je ne reviendrais pas en arriere. Combine avec [Raycast](/raycast-macos-outil-productivite-ultime/) et Ice, c'est un combo productivite macOS solide.

Temps d'adaptation : 2-3 jours pour que tes doigts oublient Cmd+Tab. Apres, ca devient instinctif.

---

## Articles connexes

- **[Raycast : L'outil qui transforme macOS en machine de productivite](/raycast-macos-outil-productivite-ultime/)** : Complementaire a rcmd pour les commandes et snippets
- **[Ice : Le gestionnaire de barre de menu gratuit pour macOS](/ice-macos-gestionnaire-barre-menu-gratuit-2025/)** : Garde ta barre de menu propre pendant que rcmd tourne
- **[iTerm2 : Guide complet configuration macOS](/iterm2-guide-configuration-macos-2025/)** : Optimise ton terminal (que tu vas ouvrir avec Right Command + I)
- **[Installation Homebrew sur macOS](/installation-homebrew-macos/)** : Indispensable pour installer rcmd et plein d'autres outils
- [Cling : Recherche fuzzy fichiers 10x plus rapide](/cling-recherche-fuzzy-fichiers-macos/)
- [Lunar : Controle la luminosite de tes ecrans externes sur macOS (enfin !)](/lunar-luminosite-ecrans-externes-macos/)
- [Grila vs Fantastical : Comparatif honnete apres 6 mois (2025)](/grila-vs-fantastical-comparatif-2025/)
- [AltTab macOS : Gestion Fenetres Style Windows (Alternative Gratuite 2026)](/alttab-macos-gestion-fenetres-windows/)

---

## Ressources utiles

- [Site officiel rcmd](https://lowtechguys.com/rcmd/)
- [FAQ officielle rcmd](https://lowtechguys.com/rcmd/#faq)
- [Low Tech Guys (tous leurs outils)](https://lowtechguys.com/)
- [Download direct rcmd](https://lowtechguys.com/rcmd/#download)
