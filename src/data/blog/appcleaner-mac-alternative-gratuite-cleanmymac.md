---
title: "AppCleaner Mac : l'alternative gratuite à CleanMyMac (2026)"
description: "AppCleaner Mac supprime tes apps avec tous leurs fichiers cachés, gratuitement. L'alternative légère à CleanMyMac (40€/an), testée sur mon propre Mac."
pubDatetime: "2025-11-18T17:39:28+01:00"
modDatetime: "2026-06-22T00:00:00+01:00"
author: Brandon Visca
tags:
  - appcleaner
  - macos
  - homebrew
  - nettoyage
  - productivite
  - debutant
featured: false
draft: false
focusKeyword: AppCleaner Mac
faqs:
  - question: "AppCleaner est-il vraiment 100% gratuit ?"
    answer: "Oui. AppCleaner est totalement gratuit, sans version payante ni achat intégré. Le développeur accepte les dons, mais aucune fonctionnalité n'est verrouillée."
  - question: "AppCleaner fonctionne-t-il sur les dernières versions de macOS ?"
    answer: "Oui. AppCleaner est maintenu et tourne sur macOS Sonoma et Sequoia. Il faut juste lui accorder l'accès complet au disque dans les Réglages Système."
  - question: "AppCleaner ou CleanMyMac, lequel choisir ?"
    answer: "AppCleaner si tu veux juste désinstaller proprement, sans payer. CleanMyMac (40€/an) ajoute du monitoring et de l'optimisation système, souvent superflus."
  - question: "Comment installer AppCleaner avec Homebrew ?"
    answer: "Une seule commande : brew install --cask appcleaner. C'est la méthode la plus rapide si Homebrew est déjà installé sur ton Mac."
---
> 💡 **TL;DR**
> - macOS ne supprime que le bundle d'une app : config, caches et logs restent sur ton SSD
> - AppCleaner les détecte et les vire en un glisser-déposer, gratuitement (vs 40€/an pour CleanMyMac)
> - SmartDelete automatise le tout : tu glisses l'app à la Corbeille, AppCleaner nettoie le reste

Tu viens de désinstaller une app sur ton Mac en la glissant dans la Corbeille ? Spoiler : elle a laissé des traces partout. Des fichiers de config dans `~/Library`, des caches, des préférences oubliées dans `Application Support`. Résultat ? Ton SSD se remplit de déchets invisibles.

**AppCleaner** résout ce problème une bonne fois pour toutes. Et contrairement à CleanMyMac qui te coûte 40€/an, cet utilitaire est **100% gratuit**.

Dans ce guide, je te montre comment l'installer, configurer SmartDelete pour automatiser le nettoyage, et récupérer plusieurs gigaoctets d'espace disque que tu croyais perdus.

## Table des matières

## Pourquoi macOS ne sait pas désinstaller proprement

Apple a conçu un système d'installation simple : tu glisses une app dans `/Applications`, tu la lances, ça marche. Mais à la désinstallation, macOS ne fait **que supprimer le bundle principal** de l'application.

Tous les fichiers associés restent en place :

- **Préférences système** : `~/Library/Preferences/com.app.plist`
- **Données utilisateur** : `~/Library/Application Support/NomApp/`
- **Caches** : `~/Library/Caches/com.app/`
- **Logs** : `~/Library/Logs/`
- **LaunchAgents** : `~/Library/LaunchAgents/` (processus en arrière-plan)

Sur mon Mac, j'ai récupéré **18 Go** de fichiers orphelins avec AppCleaner après 2 ans d'utilisation. Pas mal pour un utilitaire gratuit.

## AppCleaner Mac vs les alternatives

Voici un comparatif rapide pour situer AppCleaner face à ses concurrents :

| Fonctionnalité              | AppCleaner | CleanMyMac | Hazel           | Méthode manuelle |
|-----------------------------|------------|------------|-----------------|------------------|
| **Prix**                    | Gratuit    | 40€/an     | 42€ (one-time)  | Gratuit          |
| **Détection auto fichiers** | ✅         | ✅         | ✅              | ❌               |
| **SmartDelete**             | ✅         | ✅         | ✅ (règles)     | ❌               |
| **Interface**               | Simple     | Surchargée | Complexe        | Terminal         |
| **Taille**                  | 2 Mo       | 85 Mo      | 25 Mo           | n/a              |

AppCleaner se positionne comme la **solution minimaliste et efficace** : il fait une seule chose, mais il la fait bien.

## Installation d'AppCleaner Mac

### Méthode 1 : téléchargement direct

1. Va sur [freemacsoft.net/appcleaner](https://freemacsoft.net/appcleaner/)
2. Télécharge le fichier `.dmg`
3. Ouvre le DMG et glisse AppCleaner dans `/Applications`
4. Lance l'app, accorde les permissions dans **Réglages Système, Confidentialité et sécurité, Accès complet au disque**

### Méthode 2 : via Homebrew (recommandé)

Si tu utilises déjà Homebrew (le gestionnaire de paquets macOS dont je parle dans mon [guide d'installation Homebrew](https://brandonvisca.com/installation-homebrew-macos/)), c'est encore plus rapide :

```bash
brew install --cask appcleaner
```

## Utiliser AppCleaner au quotidien

### Activer SmartDelete

SmartDelete surveille ta Corbeille en arrière-plan. Dès que tu glisses une app dans la Corbeille, AppCleaner détecte la manœuvre et te propose automatiquement de supprimer les fichiers associés. Plus besoin d'ouvrir l'app à la main.

Pour l'activer : ouvre AppCleaner, va dans **Préférences (⌘,)**, onglet **SmartDelete**, et coche **Enable SmartDelete**. Accorde l'accès complet au disque si macOS le réclame.

### Nettoyer avant une migration

Avant de migrer vers un nouveau Mac avec **Migration Assistant**, utilise AppCleaner pour virer toutes les apps inutiles. Ça réduit la taille de la migration et t'évite de transférer des cochonneries d'un Mac à l'autre.

## Alternatives gratuites à AppCleaner Mac

Si AppCleaner ne te convient pas (ça m'étonnerait), voici d'autres options :

### AppZapper

Interface similaire, mais **payante** (13$). Pas d'avantage notable par rapport à AppCleaner.

### Hazel

Plus orienté **automatisation** que nettoyage pur. 42$ one-time. Overkill si tu veux juste désinstaller des apps.

### Méthode manuelle (Terminal)

Pour les puristes :

```bash
# Rechercher tous les fichiers d'une app
sudo find /Library ~/Library -iname "*NomApp*" 2>/dev/null

# Supprimer manuellement
sudo rm -rf /path/to/files
```

Efficace, mais une erreur de chemin et tu flingues un fichier système. AppCleaner fait la même chose sans le risque.

## Conclusion

AppCleaner, c'est l'utilitaire que tu installes une fois et que tu oublies : il bosse en silence avec SmartDelete et garde ton Mac propre sans abonnement. Pour 2 Mo et zéro euro, difficile de faire mieux que CleanMyMac sur le seul terrain qui compte vraiment, la désinstallation propre.

Si tu équipes un Mac de zéro, enchaîne avec mes [10 extensions Raycast indispensables](https://brandonvisca.com/10-extensions-raycast-indispensables-pour-developpeurs-et-sysadmins/) pour booster ta productivité au clavier.

## Pour aller plus loin

- [Installer Homebrew sur macOS](https://brandonvisca.com/installation-homebrew-macos/) : le gestionnaire de paquets pour installer AppCleaner en une commande
- [10 extensions Raycast indispensables](https://brandonvisca.com/10-extensions-raycast-indispensables-pour-developpeurs-et-sysadmins/) : automatise ton Mac au clavier
- [AltTab : gestion des fenêtres macOS](https://brandonvisca.com/alttab-macos-gestion-fenetres-windows/) : le switcher de fenêtres qui manque à macOS
- [Site officiel AppCleaner](https://freemacsoft.net/appcleaner/) : téléchargement et notes de version
