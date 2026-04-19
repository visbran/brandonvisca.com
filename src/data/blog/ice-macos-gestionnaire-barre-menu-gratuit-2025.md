---
title: "Ice macOS : remplace Bartender gratuitement et organise ta barre de menu"
description: Ice macOS remplace Bartender gratuitement. Gère ta barre de menu avec sections, hotkeys et personnalisation visuelle. Guide installation + configuration.
pubDatetime: "2025-09-22T22:25:45+02:00"
modDatetime: 2026-04-19 00:00:00+01:00
author: Brandon Visca
tags:
  - macos
  - productivite
  - barre-menu
  - guide
  - debutant
  - open-source
featured: false
draft: false
focusKeyword: ice macOS
faqs:
  - question: "Ice est-il vraiment gratuit ?"
    answer: "Oui, 100% gratuit et open-source (GPL-3.0). Aucune version payante, aucun abonnement. Code auditable sur GitHub."
  - question: "Ice est-il compatible macOS Sequoia ?"
    answer: "Oui. Ice est compatible macOS 14 Sonoma, 15 Sequoia, et la beta macOS 26 Tahoe. Mises à jour régulières du développeur."
  - question: "Quelle différence entre Ice et Bartender ?"
    answer: "Bartender coûte 20$, Ice est gratuit et open-source. Ice couvre 95% des cas d'usage Bartender avec sections multiples et personnalisation visuelle."
  - question: "Ice ralentit-il macOS ?"
    answer: "Non. Ice est développé en Swift natif, très léger. Aucun impact perceptible sur les performances, même sur MacBook Intel."
  - question: "Ice fonctionne-t-il avec l'encoche du MacBook Pro ?"
    answer: "Oui. La fonctionnalité Ice Bar est spécialement conçue pour gérer l'espace autour de l'encoche du MacBook Pro."
---
> 💡 **TL;DR**
> - Ice macOS remplace Bartender gratuitement : sections cachées, hotkeys, personnalisation visuelle
> - Installation en 30 secondes via Homebrew, compatible macOS 14 Sonoma jusqu'à Sequoia
> - Open-source (GPL-3.0), développé activement par Jordan Baird

---

## Pourquoi ta barre de menu mérite mieux

Si ta **barre de menu macOS** ressemble à une rave party d'icônes, t'es pas seul. Entre les apps de monitoring, les outils de productivité et les utilitaires système, l'interface Apple se transforme vite en bazar numérique.

Le problème est concret : **chaque pixel compte**, surtout sur les MacBook Pro avec leur encoche. Quand ta barre de menu déborde, tu perds du temps à chercher l'icône qui te manque et l'interface devient illisible.

Bartender résolvait ça depuis des années. À 20$ et avec la controverse de 2024 sur son rachat opaque, il a perdu pas mal de fans. Ice arrive en 2025 comme l'alternative évidente : gratuit, open-source, et aussi complet.

## Table des matières

## Ice macOS : ce qui change vraiment

**Ice** est développé par Jordan Baird, un développeur indépendant. Lancé en open-source sous licence GPL-3.0, le projet a pris rapidement de l'ampleur après les polémiques autour de Bartender.

J'utilise Ice au quotidien depuis la version 0.8 sur mon MacBook Pro M3. La progression est régulière et les fonctionnalités s'accumulent sans alourdir l'app.

Ce que Ice fait que le macOS natif ne fait pas :

| Fonctionnalité | macOS natif | Ice macOS |
|---|---|---|
| **Masquer des icônes** | ❌ | ✅ Sections multiples |
| **Révéler au survol/clic** | ❌ | ✅ Configurable |
| **Hotkeys par section** | ❌ | ✅ Illimités |
| **Personnalisation visuelle** | ❌ | ✅ Tint, shadow, border |
| **Ice Bar (encoche)** | ❌ | ✅ Optimisé MacBook Pro |
| **Prix** | Gratuit | Gratuit |

## Installation rapide : 3 méthodes

### Méthode 1 : Homebrew (recommandée)

Si t'as déjà [installé Homebrew](https://brandonvisca.com/installation-homebrew-macos/) :

```bash
brew install --cask jordanbaird-ice
```

Pour vérifier l'installation :

```bash
brew list --cask | grep ice
```

### Méthode 2 : Téléchargement direct (GitHub)

1. Va sur [GitHub Releases](https://github.com/jordanbaird/Ice/releases)
2. Télécharge `Ice.zip` (dernière version)
3. Décompresse et glisse dans `/Applications`

### Méthode 3 : Site officiel

Téléchargement direct sur [icemenubar.app](https://icemenubar.app/).

> ⚠️ **Gatekeeper** : Au premier lancement, macOS va bloquer l'app. Va dans **Réglages > Confidentialité et sécurité** pour l'autoriser. C'est le comportement normal pour toute app hors App Store.

## Configuration essentielle en 5 minutes

### Première connexion

Lance Ice. L'app demande quelques permissions :

1. **Accessibilité** : pour manipuler les icônes
2. **Enregistrement d'écran** (optionnel) : pour les fonctionnalités de prévisualisation
3. **Automatisation** : pour les interactions système

Accorde les trois. Sans Accessibilité, Ice ne peut pas faire grand-chose.

### Configuration de base

1. **Crée ta première section cachée** : clic droit sur une icône → `Move to Hidden Section`
2. **Configure l'affichage** dans `Ice Settings` :
   - `Show on Hover` : révèle les icônes au survol
   - `Show on Click` : affichage sur clic
   - `Auto-hide delay` : délai de masquage (3-5 secondes recommandé)
3. **Définis un raccourci global** pour révéler/masquer rapidement

## Fonctionnalités avancées

### 1. Sections multiples

Ice organise ta barre en trois zones distinctes :

- **Section visible** : apps essentielles toujours affichées
- **Section cachée** : apps secondaires révélées à la demande
- **Section Always Hidden** : apps rarement utilisées, jamais visibles sauf en mode gestion

Tu peux glisser-déposer les icônes entre sections directement dans la barre de menu en maintenant `⌘`.

### 2. Personnalisation visuelle

Ouvre `Ice Settings > Menu Bar Appearance` pour customiser l'apparence de ta barre :

- **Tinting** : couleur de fond ou dégradé
- **Shadow** : ombre sous la barre
- **Border** : bordures autour de la barre
- **Shape** : coins arrondis ou barre séparée du reste de l'écran

Le résultat peut être spectaculaire sur un setup bien calibré. J'ai opté pour un léger tint sombre avec coins arrondis sur mon setup. Résultat : une cohérence visuelle que le macOS natif n'offre pas.

### 3. Hotkeys intelligents

Ice supporte plusieurs raccourcis claviers configurables :

```text
⌘ + `       → Toggle section principale (affiche/masque)
⌃ + ⌘ + I   → Recherche Ice
⌥ + Clic    → Réorganisation rapide des icônes
⌘ + ⇧ + M   → Masquer/Afficher tout
```

Définis tes propres raccourcis dans **Ice Settings > Hotkeys**. Évite les conflits avec les raccourcis système (`⌘+Espace` est pris par Spotlight/Raycast).

### 4. Ice Bar pour MacBook Pro

Si t'as un MacBook Pro avec encoche, la fonctionnalité **Ice Bar** est ta meilleure amie. Elle crée une barre secondaire qui optimise l'espace de chaque côté de l'encoche.

Active dans **Ice Settings > Ice Bar** → `Enable Ice Bar`.

L'encoche disparaît visuellement dans la mise en page. Les icônes s'organisent proprement des deux côtés sans chevauchement.

### 5. Gestion intelligente

Ice propose quelques comportements automatiques pratiques :

- **Auto-rehide** : masque automatiquement les icônes après X secondes d'inactivité
- **Show on fullscreen exit** : révèle toutes les icônes quand tu sors du plein écran
- **Menu bar tint match** : synchronise la couleur de la barre avec ton fond d'écran

Tout ça dans **Ice Settings > General**.

## Comparaison : Ice vs Bartender vs Hidden Bar

| Critère | Ice | Bartender 5 | Hidden Bar |
|---|---|---|---|
| **Prix** | Gratuit | 20$ | Gratuit |
| **Open-source** | ✅ GPL-3.0 | ❌ | ❌ |
| **Sections multiples** | ✅ 3 sections | ✅ | ❌ 1 seule |
| **Personnalisation visuelle** | ✅ | ✅ | ❌ |
| **Hotkeys** | ✅ | ✅ | Basique |
| **Ice Bar (encoche)** | ✅ | ❌ | ❌ |
| **Compatibilité Sequoia** | ✅ | ✅ | ⚠️ Partiel |
| **Développement actif** | ✅ | ✅ | ⚠️ Lent |

Hidden Bar est trop limité pour un usage sérieux. Bartender est solide mais payant, et la controverse du rachat en 2024 a refroidi beaucoup d'utilisateurs. Ice est aujourd'hui la meilleure option par défaut.

## Tips pour optimiser ton workflow

### 1. Organisation par contexte

Ne cache pas au hasard. Organise tes sections par fréquence d'utilisation :
- **Visible** : horloge, WiFi, batterie, app active
- **Cachée** : Raycast, AltTab, outils dev
- **Always Hidden** : Bluetooth, AirDrop, tout ce que tu n'utilises jamais

### 2. Raccourcis optimaux

Un seul raccourci suffit pour 80% des usages : `⌘+\`` pour toggle. Garde les mains sur le clavier, évite la souris pour accéder à la barre cachée.

### 3. Automatisation avec Shortcuts

Combine Ice avec l'app Raccourcis macOS pour des workflows contextuels :

- **Mode Focus** : masque tout sauf l'essentiel via un raccourci
- **Mode Dev** : affiche uniquement les outils de développement
- **Mode Présentation** : interface ultra-épurée pour les démos

### 4. Intégration avec ton setup

Si t'utilises [iTerm2](https://brandonvisca.com/iterm2-guide-configuration-macos-2025/) et [Oh My Zsh](https://brandonvisca.com/installation-oh-my-zsh-powerlevel10k-guide-complet/), Ice complète bien l'environnement. Et si tu cherches à nettoyer aussi les apps installées, [AppCleaner](https://brandonvisca.com/appcleaner-mac-alternative-gratuite-cleanmymac/) fait ça gratuitement.

## Troubleshooting

### Ice ne démarre pas

**Fix** : **Réglages > Confidentialité et sécurité** → vérifie que la permission Accessibilité est accordée. Si déjà accordée, révoque et réaccorde.

### Les icônes disparaissent sans raison

**Fix** : Redémarre Ice (`⌘+Q` depuis la barre de menu, puis relance). Si le problème persiste, désactive `Auto-rehide` temporairement pour isoler le problème.

### Incompatibilité avec Bartender

**Fix** : Tu peux pas utiliser Bartender et Ice simultanément : ils se conflictent. Désinstalle Bartender avant d'utiliser Ice.

### Performances dégradées

**Fix** : Réduis le nombre d'apps en section « toujours visible ». Plus t'as d'icônes actives à surveiller, plus Ice sollicite les ressources.

## Conclusion

Ice macOS, c'est l'outil que la communauté attendait après les polémiques Bartender. Gratuit, open-source, actif, et fonctionnellement équivalent à ce que tu payais 20$ avant.

Installe-le maintenant via Homebrew, passe 5 minutes à configurer tes sections, et ta barre de menu ne ressemblera plus jamais à un bazar.

## FAQ Ice macOS

**Ice est-il vraiment gratuit ?**

Oui, 100% gratuit et open-source (GPL-3.0). Aucune version Pro, aucun abonnement. Le développeur accepte des dons sur GitHub mais l'app est entièrement fonctionnelle sans payer.

**Ice est-il compatible macOS Sequoia ?**

Oui. Ice supporte macOS 14 Sonoma, 15 Sequoia, et est testé sur la beta macOS 26 Tahoe. Les mises à jour suivent les nouvelles versions macOS rapidement.

**Quelle différence entre Ice et Bartender ?**

Bartender coûte 20$ et a connu une controverse lors de son rachat en 2024. Ice est gratuit, open-source, et couvre 95% des cas d'usage Bartender avec en plus la fonctionnalité Ice Bar pour l'encoche.

**Ice ralentit-il macOS ?**

Non. Ice est développé en Swift natif, très léger. Aucun impact perceptible sur les performances, même sur les vieux MacBook Intel.

**Puis-je utiliser Ice avec l'encoche du MacBook Pro ?**

Oui. La fonctionnalité Ice Bar est spécialement conçue pour optimiser l'espace autour de l'encoche. Ni Hidden Bar ni les autres alternatives gratuites ne proposent ça.

---

## Pour aller plus loin

- [AltTab macOS : remplace le ⌘+Tab avec des previews de fenêtres](https://brandonvisca.com/alttab-macos-gestion-fenetres-windows/)
- [AppCleaner : désinstaller proprement les apps sur Mac](https://brandonvisca.com/appcleaner-mac-alternative-gratuite-cleanmymac/)
- [Installation Homebrew sur macOS](https://brandonvisca.com/installation-homebrew-macos/)
