---
title: "rcmd : Alternative Cmd+Tab gratuite et 10x plus rapide"
pubDatetime: "2025-11-27T00:00:00+00:00"
description: "rcmd : switch entre apps en 1 touche (Right Cmd + lettre). Alternative Cmd+Tab gratuite, 10x plus rapide. Installation 2 min + config complète."
tags:
  - macos
  - productivite
  - raccourcis
  - low-tech
  - outils-systeme
draft: false
---
# rcmd : Alternative Cmd+Tab gratuite et 10x plus rapide

![](https://res.cloudinary.com/dlkn3lxkk/image/upload/v1765129755/brandonviscacom/rcmd_mac_12-06_at_14.56.53_2x_1_ljjoew.webp)

---

## Introduction : Cmd+Tab, c'est 2005

Soyons honnêtes deux secondes : **Cmd+Tab sur macOS, c'est pratique, mais c'est lent**. 

Tu veux passer de Safari à iTerm2 ? Cmd+Tab, Tab, Tab, Tab... ah merde j'ai dépassé, Shift+Tab pour revenir. 

**Le constat** : Tu perds 3-4 secondes à chaque fois. Sur une journée de travail, ça fait **facilement 5-10 minutes de perdues** juste à naviguer entre tes apps.

Et si je te disais qu'il existe un outil gratuit qui te permet de **switcher vers n'importe quelle app en une seule combinaison de touches** ?

Genre Right Command + S = Safari. Right Command + I = iTerm2. Right Command + V = VS Code.

**Instantané. Précis. Zero friction.**

Bienvenue dans le monde de **rcmd**, l'outil qui va te faire oublier Cmd+Tab pour toujours.

💡 **Ce que tu vas apprendre dans ce guide** :
- Installer rcmd en 2 minutes via le mac apple store
- Configurer tes raccourcis personnalisés
- Les astuces de power users pour aller encore plus vite
- Pourquoi c'est mieux que Raycast, Alfred ou AltTab
- Troubleshooting des problèmes courants

Let's go ! 🚀

---

## TL;DR : rcmd en 30 secondes

**Le problème** : Cmd+Tab = lent (3-4 Tab minimum à chaque fois)

**La solution** : rcmd = Right Command + lettre de l'app

| App | Raccourci rcmd | Gain vs Cmd+Tab |
|-----|----------------|-----------------|
| Safari | Right Cmd + S | 4 secondes → 0.2s |
| iTerm2 | Right Cmd + I | 3 secondes → 0.2s |
| VS Code | Right Cmd + V | 4 secondes → 0.2s |

**Résultat concret** : 10 min/jour gagnées = **60h économisées/an**

**Installation** : 2 minutes chrono (Mac App Store)

**Prix** : 100% gratuit (V2 actuelle)

## Table of content

---

## Qu'est-ce que rcmd ?

<iframe src="https://lowtechguys.com/static/video/rcmd-stage-manager-h264.mp4"></iframe>

**rcmd** (prononcé "are-command"), c'est un launcher minimaliste développé par [Low Tech Guys](https://lowtechguys.com/) qui repense complètement la façon de switcher entre applications sur macOS.

### Le concept en 3 mots

**Right Command + Lettre = App**

C'est tout. Pas de menu. Pas d'interface. Juste tes doigts, ton clavier, et la vitesse de l'éclair.

![](https://res.cloudinary.com/dlkn3lxkk/image/upload/v1765129755/brandonviscacom/rcmd_mac_12-06_at_14.57.27_2x_faon2a.webp)
### Pourquoi c'est génial ?

✅ **Muscle memory parfaite** : Ton cerveau associe chaque app à sa première lettre
✅ **Zéro latence** : Pas d'overlay, pas d'animation, switch instantané
✅ **Gratuit et open source** : Pas de paywall, pas de subscription bullshit
✅ **Léger** : ~5 Mo de RAM, invisible en arrière-plan
✅ **Compatible Apple Silicon** : Optimisé M1/M2/M3/M4

### Les chiffres qui parlent

- **+50 000 téléchargements** sur le Mac App Store
- **Note 5/5** 
- **Développement actif** (dernière update : novembre 2024)

---

## Installation de rcmd

🔔 **Actualité importante (novembre 2024)**

rcmd est actuellement **gratuit en version 2** via le Mac App Store. Bonne nouvelle : le développeur [a annoncé sur Reddit](https://www.reddit.com/r/macapps/comments/1n5wcct/the_rcmd_app_switcher_will_be_free_until_v3_is/) que **la V2 restera gratuite jusqu'à la sortie de la V3**.

**Ce qui change avec la V3** :
- 🚀 **Sortie hors Mac App Store** (plus de contrôle pour le dev)
- 🍺 **Installation via Homebrew** (plus simple pour nous)
- 💰 **Passage au payant** (prix non annoncé)

💡 **Mon conseil** : Installe la V2 **maintenant** pour profiter de la gratuité et te familiariser avec l'outil. Quand la V3 sortira, tu pourras décider si tu veux upgrader ou rester sur la V2 gratuite.

⚠️ **Timing** : La V2 reste **gratuite jusqu'à la V3**, donc c'est le moment idéal pour tester sans pression.

---

### Installation (V2 actuelle - gratuite)

1. **Télécharge rcmd** : [lowtechguys.com/rcmd](https://lowtechguys.com/rcmd/)
2. L'installation s'effectue (à l'heure où j'écris cet article) uniquement via le Mac App Store. Tu cliques : ça s'installe, c'est d'une simplicité enfantine.  
3. Tu peux ensuite lancer l'application via Raycast si tu l'as déjà configuré, ou directement depuis le Launchpad.

![](https://res.cloudinary.com/dlkn3lxkk/image/upload/v1765129755/brandonviscacom/rcmd_mac_12-06_at_15.34.38_2x_vc5glm.webp)

💡 **Astuce** : Épingle rcmd dans la barre de menu ou configure-le pour démarrer automatiquement au login (dans les préférences).

---

## Configuration essentielle en 5 minutes

### Première utilisation : Le tour du propriétaire

Au premier lancement, rcmd te demande :

1. **Accessibilité** : Autoriser dans Réglages Système > Confidentialité
2. **Touche de déclenchement** : Par défaut = Right Command (⌘ droite)
3. **Comportement** : Choisir comment gérer les apps multiples avec même lettre

![](https://res.cloudinary.com/dlkn3lxkk/image/upload/v1765129755/brandonviscacom/rcmd_mac_12-06_at_15.35.20_2x_dei4fd.webp)

![](https://res.cloudinary.com/dlkn3lxkk/image/upload/v1765129755/brandonviscacom/rcmd_mac_12-06_at_15.35.50_2x_yy9djs.webp)
### Réglages de base recommandés

```
✅ Trigger Key : Right Command (par défaut)
✅ Cycle behavior : Enabled (pour apps avec même lettre)
✅ Launch at login : Enabled
✅ Show in menu bar : Disabled (minimalisme FTW)
```

**Pourquoi Right Command ?**
- Ta main droite est déjà sur les lettres
- Aucun conflit avec les raccourcis système existants
- Muscle memory plus naturelle que Left Command

💡 **Claviers externes ?** Si ton clavier n'a pas de Right Command distinct, tu peux changer la trigger key dans les settings (Control, Option, etc.)

---

## Utilisation : Les bases en 3 exemples

### Exemple 1 : Switcher vers une app

Tu veux ouvrir **Safari** ?

```
Right Command + S = Safari se lance/devient active
```

Simple, rapide, efficace.

### Exemple 2 : Apps avec même première lettre

Tu as **Safari**, **Spotify** et **Slack** ?

Première pression : Right Command + S → Safari
Deuxième pression : Right Command + S → Spotify  
Troisième pression : Right Command + S → Slack

**Cycle automatique** entre les apps qui commencent par la même lettre.

### Exemple 3 : Assigner une lettre custom

Tu veux que **Music.app** s'ouvre avec Right Command + U au lieu de M ?

1. Active Music.app
2. Presse Right Command + Right Option + U
3. C'est fait ! Désormais, Right Command + U = Music


---

## Fonctionnalités avancées (pour aller plus loin)

### 1. Window switcher intégré

**Problème** : rcmd switch entre apps, mais pas entre fenêtres de la même app.

**Solution macOS native** :

```
Cmd + ` (backtick) = Switch entre fenêtres de l'app active
```

Combine les deux :
- Right Command + S = Safari
- Puis Cmd + ` pour passer d'un onglet Safari à un autre

### 2. Blacklist des apps

Tu ne veux pas que certaines apps soient accessibles via rcmd ?

Dans les settings → **Excluded Apps** → Ajoute les apps à ignorer

**Cas d'usage** : Exclure les apps que tu n'utilises jamais mais qui tournent en arrière-plan.

### 3. Raccourcis pour Launchpad et Spotlight

rcmd peut aussi lancer :
- **Launchpad** avec une lettre custom
- **Spotlight** (bien que ça soit redondant avec Cmd+Space)

Via commande Terminal pour Launchpad :

```bash
killall rcmd
defaults write com.lowtechguys.rcmd appKeyAssignments -dict-add "com.apple.launchpad.launcher" "L"
open -a rcmd
```

Maintenant Right Command + L = Launchpad.

### 4. Intégration avec d'autres outils macOS

rcmd se combine parfaitement avec :

- **[[raycast-macos-outil-productivite-ultime|Raycast]]** : Raycast pour les commandes, rcmd pour le switch d'apps
- **[[ice-gestionnaire-barre-menu-macos|Ice]]** : Garde ta barre de menu propre pendant que rcmd tourne en arrière-plan
- **[[iterm2-guide-configuration-macos-2025|iTerm2]]** : Right Command + I = iTerm2 instantané

💡 **Mon workflow perso** :
- Right Command + lettre = Switch apps (rcmd)
- Cmd + Space = Lancer des actions (Raycast)
- Cmd + ` = Switch fenêtres même app

---

## rcmd vs les alternatives : Le match sans pitié

### rcmd vs Cmd+Tab (macOS natif)

| Critère | rcmd | Cmd+Tab |
|---------|------|---------|
| **Vitesse** | ⚡ Instantané | 🐌 3-4 Tab parfois |
| **Précision** | 🎯 Touche dédiée par app | 🎲 Ordre chronologique |
| **Muscle memory** | ✅ Lettre = toujours même app | ❌ Position change constamment |
| **Visuel** | 🚫 Aucune UI (minimaliste) | 👁️ Overlay obligatoire |
| **Prix** | 💰 Gratuit | 💰 Gratuit |

**Verdict** : rcmd gagne haut la main sur la vitesse et la prévisibilité.

---

### rcmd vs Raycast / Alfred

| Critère | rcmd | Raycast | Alfred |
|---------|------|---------|--------|
| **Focus** | Switch apps uniquement | Launcher complet | Launcher + workflows |
| **Simplicité** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Latence** | 0 ms | ~50 ms | ~50 ms |
| **Prix** | Gratuit | Gratuit (Pro = 96$/an) | Gratuit (Powerpack = 59€) |
| **Courbe apprentissage** | 2 min | 1-2 jours | 1 semaine |

**Verdict** : rcmd est **complémentaire** à Raycast/Alfred. 

**Usage idéal** :
- **rcmd** pour switcher entre apps (muscle memory)
- **Raycast** pour lancer des commandes, snippets, extensions

Perso, j'utilise les deux en parallèle. Chacun excelle dans son domaine.

---

### rcmd vs AltTab

**AltTab** est une autre alternative open source qui améliore Cmd+Tab.

| Critère | rcmd | AltTab |
|---------|------|--------|
| **Approche** | Touche dédiée par app | Cmd+Tab amélioré |
| **Prévisualisation fenêtres** | ❌ | ✅ (avec thumbnails) |
| **Vitesse** | ⚡ Plus rapide | 🐌 Légèrement plus lent |
| **Simplicité** | Plus simple | Plus de features |

**Verdict** : Si tu veux juste **switcher vite**, prends rcmd. Si tu veux **voir** tes fenêtres avant de switcher, prends AltTab.

---

## Cas d'usage concrets (comment je gagne 10 min/jour)

### Workflow 1 : Développeur

```
Right Command + I = iTerm2 (terminal)
Right Command + V = VS Code (éditeur)
Right Command + S = Safari (docs/Stack Overflow)
Right Command + N = Notion (notes)
Right Command + P = Postman (API testing)
```

**Avant rcmd** : Cmd+Tab x4 = 4 secondes  
**Avec rcmd** : Right Command + lettre = 0.2 seconde

**Gain sur 8h de dev** : ~10 minutes/jour

---

### Workflow 2 : Rédaction d'articles (mon cas)

```
Right Command + O = Obsidian (rédaction markdown)
Right Command + S = Safari (recherche web)
Right Command + F = Firefox (vérif rendu)
Right Command + I = iTerm2 (déploiement)
Right Command + M = Music (concentration)
```

**Résultat** : Je ne quitte plus mon clavier. Zéro friction cognitive.

---

### Workflow 3 : Admin système

```
Right Command + I = iTerm2 (SSH serveurs)
Right Command + L = LocalWP (tests WordPress local)
Right Command + S = Safari (docs techniques)
Right Command + N = Notion (runbooks)
Right Command + U = Uptime Kuma (monitoring)
```

**Effet** : Réactivité accrue pour les incidents. Pas de temps perdu à chercher la bonne app.

---

## Troubleshooting : Les pièges à éviter

### Problème 1 : Right Command ne fonctionne pas

**Symptômes** : Rien ne se passe quand tu appuies sur Right Command + lettre.

**Causes possibles** :
1. Ton clavier externe envoie le mauvais keycode
2. Tu as mappé Right Command à autre chose dans Réglages Système

**Solution** :

1. **Vérifier les keycodes** avec l'app [KeyCodes](https://files.alinpanaitiu.com/KeyCodes.zip)
2. **Changer la trigger key** dans les settings rcmd (essaye Right Option ou Right Control)

![Vérification keycodes - PLACEHOLDER SCREENSHOT]
*Légende : App KeyCodes pour diagnostiquer le problème*

---

### Problème 2 : Conflit avec Raycast/Alfred

**Symptôme** : rcmd et Raycast se marchent dessus sur certaines touches.

**Solution** :

1. Dans Raycast : Utilise Cmd+Space (pas Right Command)
2. Dans rcmd : Utilise Right Command uniquement
3. **Aucun conflit** = usage complémentaire optimal

---

### Problème 3 : Une app ne se lance pas

**Symptôme** : Right Command + S ne fait rien, alors que Safari est installé.

**Causes** :
1. Safari n'est pas dans `/Applications`
2. Le nom de l'app a changé

**Solution** :

1. Vérifie que l'app est bien dans `/Applications`
2. Assigne manuellement la touche : Ouvre Safari, puis Right Command + Right Option + S

---

### Problème 4 : Licence ne reste pas activée

**Symptôme** : Version payante (si tu as pris Pro) qui demande la licence à chaque redémarrage.

**Solution** :

```bash
# Supprimer les fichiers de licence corrompus
rm -rf "$HOME/Library/Application Support/rcmd/"*
killall rcmd
open -a rcmd
```

Puis réactive avec ta clé de licence.

⚠️ **Note** : La version gratuite n'a pas ce problème (pas de licence).

---

## Alternatives et comparaisons

### Si rcmd ne te convient pas, essaie :

**1. [[raycast-macos-outil-productivite-ultime|Raycast]]** (launcher complet)
- Plus de features (snippets, extensions, AI)
- Courbe d'apprentissage plus longue
- Gratuit avec version Pro

**2. [[alttab-macos-gestion-fenetres-windows]]** (Cmd+Tab amélioré)
- Prévisualisation des fenêtres
- Plus visuel que rcmd
- Gratuit et open source

**3. Contexts** (payant, 10$)
- Switch par fenêtre (pas par app)
- Recherche fuzzy
- Plus complexe

**4. Witch** (payant, 14$)
- Très customisable
- Lourd en features
- Overkill pour la plupart

---

## Conclusion : Faut-il adopter rcmd ?

**La réponse courte : OUI**, si tu veux gagner du temps et réduire la friction cognitive.

**Les 3 raisons d'installer rcmd maintenant** :

1. ✅ **C'est gratuit** (version complète fonctionnelle)
2. ✅ **Ça s'installe en 2 minutes** (Homebrew ou manuel)
3. ✅ **Impact immédiat** sur ta productivité

**Ce que j'aime** :
- Vitesse de l'éclair
- Muscle memory parfaite
- Minimalisme (zéro UI)
- Gratuit et open source

**Ce qui pourrait être mieux** :
- Pas de preview des fenêtres (mais c'est le concept)
- Courbe d'apprentissage de 2-3 jours pour oublier Cmd+Tab
- Pas de switch entre fenêtres d'une même app (utilise Cmd+` pour ça)

**Mon verdict perso** : Je l'utilise **tous les jours depuis 6 mois**, et je ne reviendrais jamais en arrière. Combiné avec [[raycast-macos-outil-productivite-ultime|Raycast]] et [[ice-gestionnaire-barre-menu-macos|Ice]], c'est le trinity productivité macOS.

**Temps d'adaptation** : 2-3 jours pour que tes doigts oublient Cmd+Tab. Après, c'est du velours.

Alors, prêt à switcher à la vitesse de la lumière ? 🚀

---

## 🔗 Articles connexes qui pourraient t'intéresser

- **[[raycast-macos-outil-productivite-ultime|Raycast : L'outil qui transforme macOS en machine de productivité]]** : Complémentaire à rcmd pour les commandes et snippets
- **[[ice-gestionnaire-barre-menu-macos|Ice : Le gestionnaire de barre de menu gratuit pour macOS]]** : Garde ta barre de menu propre pendant que rcmd tourne
- **[[iterm2-guide-configuration-macos-2025|iTerm2 : Guide complet configuration macOS]]** : Optimise ton terminal (que tu vas ouvrir avec Right Command + I)
- **[[installation-homebrew-macos|Installation Homebrew sur macOS]]** : Indispensable pour installer rcmd et plein d'autres outils

---

## 💡 Ressources utiles

- [Site officiel rcmd](https://lowtechguys.com/rcmd/)
- [FAQ officielle rcmd](https://lowtechguys.com/rcmd/#faq)
- [Low Tech Guys (tous leurs outils)](https://lowtechguys.com/)
- [Download direct rcmd](https://lowtechguys.com/rcmd/#download)
