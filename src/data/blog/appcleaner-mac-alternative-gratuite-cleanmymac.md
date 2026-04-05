---
title: "AppCleaner Mac : Alternative Gratuite à CleanMyMac (Guide Complet 2025)"
pubDatetime: "2025-11-18T17:39:28+01:00"
description: AppCleaner Mac supprime complètement tes apps avec tous leurs fichiers
tags:
  - appcleaner
  - macos
  - homebrew
  - nettoyage
  - productivite
  - guide
  - debutant
---

TL;DR
-----

Tu viens de désinstaller une app sur ton Mac en la glissant dans la Corbeille ? Spoiler : elle a laissé des traces partout. Des fichiers de config dans `~/Library`, des caches dans `/tmp`, des préférences oubliées dans `Application Support`. Résultat ? Ton SSD se remplit de déchets invisibles.

**AppCleaner Mac** résout ce problème une bonne fois pour toutes. Et contrairement à CleanMyMac qui te coûte 40€/an, cet utilitaire est **100% gratuit**.

Dans ce guide, je te montre comment installer AppCleaner Mac, configurer SmartDelete pour automatiser le nettoyage, et récupérer plusieurs gigaoctets d’espace disque que tu croyais perdus.

- - - - - -

Pourquoi macOS ne sait pas désinstaller proprement
--------------------------------------------------

Apple a conçu un système d’installation simple : tu glisses une app dans `/Applications`, tu la lances, ça marche. Mais à la désinstallation, macOS ne fait **que supprimer le bundle principal** de l’application.

Tous les fichiers associés restent en place :

- **Préférences système** : `~/Library/Preferences/com.app.plist`
- **Données utilisateur** : `~/Library/Application Support/NomApp/`
- **Caches** : `~/Library/Caches/com.app/`
- **Logs** : `~/Library/Logs/`
- **LaunchAgents** : `~/Library/LaunchAgents/` (processus en arrière-plan)

Sur une installation standard, j’ai récupéré **18 Go** de fichiers orphelins avec AppCleaner Mac après 2 ans d’utilisation. Pas mal pour un utilitaire gratuit.

- - - - - -

----------
## Table des matières


- [Pourquoi macOS ne sait pas désinstaller proprement](#pourquoi-mac-os-ne-sait-pas-desinstaller-proprement)
- [AppCleaner Mac vs les alternatives](#app-cleaner-mac-vs-les-alternatives)
- [Installation d’AppCleaner Mac](#installation-d-app-cleaner-mac)
  - [Méthode 1 : Téléchargement direct](#methode-1-telechargement-direct)
  - [Méthode 2 : Via Homebrew (recommandé)](#methode-2-via-homebrew-recommande)
- [Utilisation basique : désinstaller une app proprement](#utilisation-basique-desinstaller-une-app-proprement)
  - [Méthode par glisser-déposer](#methode-par-glisser-deposer)
  - [Recherche manuelle d’apps installées](#recherche-manuelle-dapps-installees)
- [SmartDelete : automatiser le nettoyage avec AppCleaner Mac](#smart-delete-automatiser-le-nettoyage-avec-app-cleaner-mac)
  - [Activer SmartDelete](#activer-smart-delete)
- [Fonctions avancées d’AppCleaner Mac](#fonctions-avancees-d-app-cleaner-mac)
  - [Nettoyer les widgets et extensions](#nettoyer-les-widgets-et-extensions)
  - [Rechercher manuellement des fichiers résiduels](#rechercher-manuellement-des-fichiers-residuels)
- [Protéger certaines apps de la suppression](#proteger-certaines-apps-de-la-suppression)
- [Erreurs fréquentes avec AppCleaner Mac](#erreurs-frequentes-avec-app-cleaner-mac)
  - [« AppCleaner ne trouve pas tous les fichiers »](#app-cleaner-ne-trouve-pas-tous-les-fichiers)
  - [« L’app ne se supprime pas complètement »](#lapp-ne-se-supprime-pas-completement)
  - [« SmartDelete ne se déclenche pas »](#smart-delete-ne-se-declenche-pas)
- [Pourquoi AppCleaner Mac vaut mieux que CleanMyMac](#pourquoi-app-cleaner-mac-vaut-mieux-que-clean-my-mac)
- [Tips et astuces pour optimiser AppCleaner Mac](#tips-et-astuces-pour-optimiser-app-cleaner-mac)
  - [1. Intégrer AppCleaner dans ton workflow](#1-integrer-app-cleaner-dans-ton-workflow)
  - [2. Automatiser avec des scripts](#2-automatiser-avec-des-scripts)
  - [3. Nettoyer avant une migration](#3-nettoyer-avant-une-migration)
- [Alternatives gratuites à AppCleaner Mac](#alternatives-gratuites-a-app-cleaner-mac)
  - [1. AppZapper](#1-app-zapper)
  - [2. Hazel](#2-hazel)
  - [3. Méthode manuelle (Terminal)](#3-methode-manuelle-terminal)
- [Conclusion : AppCleaner Mac, l’utilitaire que tu installes et que tu oublies](#conclusion-app-cleaner-mac-lutilitaire-que-tu-installes-et-que-tu-oublies)
- [FAQ AppCleaner Mac](#faq-app-cleaner-mac)
  - [AppCleaner est-il vraiment gratuit ? ](#faq-question-1763484533396)
  - [AppCleaner supprime-t-il les malwares ?](#faq-question-1763484542872)
  - [Puis-je récupérer une app supprimée par erreur ?](#faq-question-1763484554405)
  - [AppCleaner fonctionne-t-il sur macOS Sequoia ?](#faq-question-1763484576425)
  - [Quelle différence avec la suppression manuelle ? ](#faq-question-1763484590942)
- [Liens utiles](#liens-utiles)


AppCleaner Mac vs les alternatives
----------------------------------

Voici un comparatif rapide pour situer AppCleaner face à ses concurrents :

| Fonctionnalité | AppCleaner | CleanMyMac | Hazel | Méthode manuelle |
|---|---|---|---|---|
| **Prix** | Gratuit | 40€/an | 42€ (one-time) | Gratuit |
| **Détection auto fichiers** | ✅ | ✅ | ✅ | ❌ |
| **SmartDelete** | ✅ | ✅ | ✅ (règles) | ❌ |
| **Interface** | Simple | Surchargée | Complexe | Terminal |
| **Taille** | 2 Mo | 85 Mo | 25 Mo | — |

AppCleaner Mac se positionne comme la **solution minimaliste et efficace** : il fait une seule chose, mais il la fait bien.

- - - - - -

Installation d’AppCleaner Mac
-----------------------------

### Méthode 1 : Téléchargement direct

1. Va sur [freemacsoft.net/appcleaner](https://freemacsoft.net/appcleaner/)
2. Télécharge le fichier `.dmg`
3. Ouvre le DMG et glisse AppCleaner dans `/Applications`
4. Lance l’app, accorde les permissions dans **Paramètres Système > Confidentialité > Accès complet au disque**

### Méthode 2 : Via Homebrew (recommandé)

Si tu utilises déjà Homebrew (le gestionnaire de paquets macOS dont je parle dans mon [guide d’installation Homebrew](../installation-homebrew-macos/.md)), c’est encore plus rapide :

```bash
brew install --cask appcleaner

```

tell application "AppCleaner"
    activate
    -- Glisse l'app ici via automation
end tell


Perso, je l’utilise dans un script Bash qui nettoie mon Mac tous les mois.

### 3. Nettoyer avant une migration

Avant de migrer vers un nouveau Mac avec **Migration Assistant**, utilise AppCleaner pour virer toutes les apps inutiles. Ça réduit la taille de la migration et t’évite de transférer des cochonneries.

- - - - - -

Alternatives gratuites à AppCleaner Mac
---------------------------------------

Si AppCleaner ne te convient pas (ça m’étonnerait), voici d’autres options :

### 1. AppZapper

Interface similaire, mais **payante** (13$). Pas d’avantage notable par rapport à AppCleaner.

### 2. Hazel

Plus orienté **automatisation** que nettoyage pur. 42$ one-time. Overkill si tu veux juste désinstaller des apps.

### 3. Méthode manuelle (Terminal)

Pour les puristes :

```bash
# Rechercher tous les fichiers d'une app
sudo find /Library ~/Library -iname "*NomApp*" 2>/dev/null

# Supprimer manuellement
sudo rm -rf /path/to/files

```

