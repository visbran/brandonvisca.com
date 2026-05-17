---
title: "Raycast macOS : Guide complet 2026 — Extensions, AI et Snippets"
description: "Découvrez Raycast macOS, le launcher gratuit qui remplace Spotlight. Extensions, AI, snippets : gagnez 2h par jour. Guide complet 2026."
pubDatetime: "2025-10-13T15:20:28+02:00"
modDatetime: 2026-05-17 00:00:00+01:00
author: Brandon Visca
tags:
  - raycast
  - macos
  - productivite
  - guide
  - debutant
featured: false
draft: false
focusKeyword: Raycast macOS
---
> 💡 **TL;DR**
> - Raycast est un launcher macOS **gratuit** qui remplace Spotlight — clipboard history, snippets, window management inclus
> - Installe en 2 minutes via `brew install --cask raycast` ou depuis raycast.com
> - La version gratuite couvre 90% des besoins — le Pro (96$/an) ajoute l'IA et le Cloud Sync

## Table des matières

## Introduction : Pourquoi Spotlight ne suffit plus

![Raycast macOS](CleanShot-2025-10-13-at-15.04.53@2x.webp)

Soyons honnêtes deux secondes : **Spotlight, c'était cool en 2010**. Mais en 2026, ouvrir une app ou chercher un fichier, c'est le strict minimum. Si tu bosses sur Mac et que tu passes encore 50% de ton temps à cliquer dans le Dock ou à fouiller dans le Finder, on a un problème.

T'as déjà calculé combien de temps tu perds par jour à :

- Chercher un fichier noyé dans tes dossiers
- Copier une URL que t'as écrasée 3 secondes après
- Basculer entre 12 fenêtres ouvertes pour trouver la bonne
- Retaper « cordialement, » pour la 47ème fois cette semaine

Spoiler : **c'est beaucoup trop**.

C'est là que **Raycast macOS** débarque. Un launcher gratuit, ultra-puissant, extensible à l'infini, qui transforme ton Mac en véritable **machine de guerre productive**. Et le meilleur ? Tu vas te demander comment t'as fait pour vivre sans.

---

## Raycast macOS : qu'est-ce que c'est ?

![Clavier avec option de téléchargement](CleanShot-2025-10-13-at-15.07.57@2x.webp)

Imagine Spotlight. Maintenant imagine qu'on lui donne des **stéroïdes**, une **API extensible**, un **store d'extensions**, de l'**IA intégrée**, et qu'on le rende **100x plus rapide**. Voilà Raycast.

Concrètement, c'est un **launcher** (comme Alfred ou Spotlight), mais qui va **bien plus loin** :

- ⌨️ **Contrôle tout au clavier** : apps, fichiers, actions, services web
- 🧩 **Extensions gratuites** : GitHub, Docker, Notion, Slack, Jira, Spotify…
- 🤖 **IA intégrée** : ChatGPT, Claude, Gemini directement dans la barre de recherche
- 📋 **Clipboard History** : historique de tous tes copier-coller (avec recherche)
- 🪟 **Window Management** : redimensionne tes fenêtres en une touche
- ⚡ **Snippets** : templates réutilisables pour emails, code, réponses types
- 🔗 **Quicklinks** : ouvre tes sites favoris en 3 lettres

Et tout ça, c'est **gratuit**. Oui, tu as bien lu.

---

## Installation et premiers pas

### Étape 1 : Télécharge Raycast

Va sur [raycast.com](https://raycast.com/) et clique sur « Download ». C'est un `.dmg` classique, aucun piège.

```bash
# Ou en CLI si t'es du genre à flex avec Homebrew
brew install --cask raycast
```

### Étape 2 : Lance Raycast et configure le raccourci

Au premier lancement, Raycast te demande de remplacer le raccourci Spotlight (⌘ + Espace). **Accepte**. C'est le geste le plus rentable de ta journée.

Si tu préfères garder Spotlight, tu peux définir un raccourci dédié dans **Raycast → Preferences → General → Raycast Hotkey**.

### Étape 3 : Explore les commandes de base

Dès le premier lancement, tape dans la barre :

- `Calculator` → calcul instantané
- `Clipboard History` → tout ton presse-papiers
- `Window Management` → organise tes fenêtres
- `Snippets` → tes modèles de texte

La complétion automatique est redoutablement rapide. Après 2-3 utilisations, Raycast apprend tes habitudes et remonte tes commandes préférées en tête.

---

## Les features qui changent la vie

### Clipboard History : ne perds plus jamais un copier-coller

T'as déjà copié un lien, copié autre chose par-dessus, et perdu le premier ? **Ça n'arrivera plus.**

Raycast garde un historique de tous tes copier-coller : textes, URLs, images, code. Ouvre-le via la commande `Clipboard History` dans Raycast et cherche n'importe quoi dans l'historique.

**Ce que j'utilise le plus :**
- Retrouver une URL copiée il y a 45 minutes
- Réutiliser un snippet de code sans le retaper
- Copier plusieurs éléments à la suite et les coller dans l'ordre

Version gratuite : historique sur 3 mois. Version Pro : illimité.

> 💡 **Astuce** : configure le raccourci Clipboard History sur ⌘ + Shift + V dans **Preferences → Extensions → Clipboard History → Hotkey**. C'est le geste qui sauve le plus de temps au quotidien.

### Window Management : Magnet intégré, gratuit

J'utilisais [Magnet](https://brandonvisca.com/magnet-macos-gestionnaire-fenetres-guide-complet/) avant. Depuis que j'ai Raycast, c'est désinstallé.

**Raccourcis (à configurer dans Preferences → Extensions → Window Management) :**

| Action | Exemple de raccourci |
|--------|---------------------|
| Moitié gauche | Ctrl + Opt + ← |
| Moitié droite | Ctrl + Opt + → |
| Plein écran | Ctrl + Opt + Entrée |
| Quart supérieur gauche | Ctrl + Opt + U |
| Centre (70%) | Ctrl + Opt + C |

Tu peux tout reconfigurer dans **Preferences → Extensions → Window Management**. J'ai gardé les defaults — ils sont suffisamment bien pensés.

### Snippets : arrête de retaper les mêmes trucs

Les Snippets, c'est des **modèles de texte déclenchés par un keyword**. Tu tapes `;mail`, ça se remplace par ton template d'email complet.

**Exemple :**

```text
Keyword: ;mail
Texte:
Bonjour,

J'espère que tu vas bien. Je reviens vers toi concernant...

Cordialement,
Brandon
```

Tape `;mail` n'importe où → le texte se remplace automatiquement.

**Cas d'usage :**
- Emails types
- Commandes CLI fréquentes (`docker ps -a`, `git log --oneline`)
- Réponses support client
- Signatures d'emails

### Quicklinks : tes URLs favorites à portée de doigts

Les Quicklinks, c'est des **bookmarks sous stéroïdes**.

**Exemple :**

```text
Name: GitHub Search
Link: https://github.com/search?q={Query}
Alias: gh
```

Tape `gh raycast` → recherche « raycast » sur GitHub. Le paramètre `{Query}` est remplacé par ce que tu tapes après l'alias.

### Calculator : le seul calculateur qui te comprend

Pas besoin de lancer une app. Tape ton calcul directement dans Raycast :

```text
50 * 12           → 600
15% de 1200       → 180
sqrt(144)         → 12
2^10              → 1024
```

Appuie sur Entrée → le résultat est copié dans ton clipboard. L'historique de tes calculs est sauvegardé.

---

## Les extensions indispensables

![Extensions Raycast Store](CleanShot-2025-10-13-at-15.12.07@2x.webp)

Raycast a un **Store d'extensions** gratuit. Voici les must-have :

| Extension | Utilité | Commande |
|-----------|---------|----------|
| **GitHub** | Voir tes repos, issues, PRs | `gh` |
| **Docker** | Gérer tes containers | `docker` |
| **Brew** | Installer/mettre à jour des apps | `brew search` |
| **Port Manager** | Voir les ports ouverts, kill un process | `port` |
| **Translator** | Traduction instantanée | `translate` |
| **Spotify** | Contrôler la lecture | `spotify` |
| **Color Picker** | Récupérer des couleurs à l'écran | `color` |

**Pour installer une extension :**

1. Tape `store` dans Raycast
2. Cherche l'extension
3. Clique sur « Install »

Pas de compte requis. Pas de paiement. **C'est ça qui est beau.**

**Envie d'aller plus loin ?** 👉 J'ai rédigé un guide complet sur les [10 Extensions Raycast indispensables pour développeurs et sysadmins](https://brandonvisca.com/10-extensions-raycast-indispensables-pour-developpeurs-et-sysadmins/) avec installation détaillée, configuration, et cas d'usage concrets pour chaque extension.

---

## Raycast vs Spotlight vs Alfred : le match sans pitié

| Feature | Spotlight | Alfred | Raycast |
|---------|-----------|--------|---------|
| **Prix** | Gratuit | £34 (Powerpack) | Gratuit |
| **Extensions** | ❌ | ✅ (payant) | ✅ (gratuit) |
| **Clipboard History** | ❌ | ✅ (payant) | ✅ (gratuit) |
| **Window Management** | ❌ | ❌ | ✅ |
| **IA intégrée** | ❌ | ❌ | ✅ (Pro) |
| **Snippets** | ❌ | ✅ (payant) | ✅ (gratuit) |
| **Interface** | Basique | Old school | Moderne |
| **Vitesse** | Correcte | Rapide | Ultra-rapide |

**Verdict :** Si tu débutes, **Raycast écrase tout**. Si t'es un power user d'Alfred depuis 10 ans, tu peux rester sur Alfred (mais teste quand même Raycast, sérieux). J'ai un [comparatif complet Raycast vs Alfred](https://brandonvisca.com/raycast-vs-alfred-spotlight-comparatif-macos/) si tu veux tous les détails.

---

## Version gratuite vs Pro : as-tu vraiment besoin de payer ?

### Version gratuite (0€) :

- Toutes les features de base
- Clipboard History (3 mois max)
- Extensions illimitées
- Window Management
- Snippets
- Quicklinks

### Version Pro (96$/an) :

- **Raycast AI** : ChatGPT, Claude, Gemini dans Raycast
- **Cloud Sync** : sync entre plusieurs Macs
- **Clipboard illimité**
- **Thèmes personnalisés**
- **Traduction AI**

**Mon avis :** La version gratuite est **largement suffisante** pour 90% des utilisateurs. Si tu bosses avec plusieurs Macs ou si tu veux de l'IA intégrée, le Pro peut valoir le coup. Mais ne paie pas si t'en as pas besoin.

---

## Cas d'usage concrets : comment je gagne 2h par jour

Après 18 mois d'utilisation quotidienne, voilà mes 3 workflows qui font la différence.

### Workflow dev

1. ⌘ + Espace → `docker ps` (voir mes containers)
2. ⌘ + Espace → `gh` (voir mes PRs GitHub)
3. ⌘ + Espace → `port 3000` (voir quel process écoute sur le port 3000)

### Rédaction d'articles

1. ⌘ + Espace → `;intro` (snippet pour intro d'article)
2. ⌘ + Shift + V → retrouver une source copiée il y a 1h
3. ⌘ + Espace → `translate` (traduire un terme technique)

### Meetings

1. ⌘ + Espace → `schedule` (voir mon calendrier)
2. ⌘ + Espace → `join meeting` (rejoindre une réunion en 1 clic)

J'estime gagner **~2h par jour** en éliminant les frictions inutiles. C'est une estimation conservative. Les premières semaines après installation, j'ai facilement gagné plus.

---

## Conclusion

Si t'es sur Mac et que tu veux **booster ta productivité sans effort**, installe Raycast macOS. C'est gratuit, c'est rapide, et tu vas te demander comment t'as fait sans.

**Les 3 raisons d'installer Raycast maintenant :**

1. **C'est gratuit** (et meilleur que des tools payants)
2. **Ça s'installe en 2 minutes**
3. **Tu vas gagner un temps fou** dès le premier jour

Il y a une légère courbe d'apprentissage, mais après 2-3 jours d'utilisation, tu ne reviendras jamais en arrière. Je l'ai installé sur tous mes Macs. C'est le premier outil que je configure sur une machine neuve.

---

## Pour aller plus loin

- [Site officiel Raycast](https://raycast.com/)
- [Store d'extensions Raycast](https://raycast.com/store)
- [Documentation officielle Raycast](https://manual.raycast.com/)
- [Raycast vs Alfred : Test après 30 jours](https://brandonvisca.com/raycast-vs-alfred-spotlight-comparatif-macos/)

## Articles connexes

- [Raycast vs Alfred : Test après 30 jours (Verdict 2025)](/raycast-vs-alfred-spotlight-comparatif-macos/)
- [AltTab macOS : Gestion Fenêtres Style Windows (Alternative Gratuite 2026)](/alttab-macos-gestion-fenetres-windows/)
- [Cling : Recherche fuzzy fichiers 10x plus rapide](/cling-recherche-fuzzy-fichiers-macos/)
- [Clop : Compresse tes images et vidéos automatiquement sur macOS (gratuit)](/clop-compression-images-videos-macos/)
