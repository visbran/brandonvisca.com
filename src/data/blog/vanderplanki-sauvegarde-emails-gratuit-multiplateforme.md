---
title: "Vanderplanki : L'Outil Gratuit qui Va Révolutionner Vos Sauvegardes Email (Enfin du Multi-plateforme !)"
pubDatetime: "2025-06-12T19:38:49+02:00"
author: Brandon Visca
description: "Vanderplanki : outil gratuit de sauvegarde d'emails multiplateforme par les créateurs de MailStore. Chiffré, open source. Guide complet d'installation."
tags:
  - macos
  - windows
  - linux
  - debutant
  - guide
  - backup
---


- [Vanderplanki : Quand les Pros de l’Archivage se Remettent au Boulot](#vanderplanki-quand-les-pros-de-l-archivage-se-remettent-au-boulot)
  - [🔧 Les Fonctionnalités qui Font la Différence](#%F0%9F%94%A7-les-fonctionnalites-qui-font-la-difference)
- [Installation et Configuration : Plus Simple qu’un Café du Matin 🍵](#installation-et-configuration-plus-simple-quun-cafe-du-matin)
  - [Prérequis Système](#prerequis-systeme)
  - [Étapes d’Installation](#etapes-d-installation)
  - [Configuration Initiale](#configuration-initiale)
  - [Configuration IMAP : L’Example Gmail](#configuration-imap-l-example-gmail)
- [Version Gratuite vs Plus : Que Choisir ?](#version-gratuite-vs-plus-que-choisir)
  - [Version Basic (Gratuite)](#version-basic-gratuite)
  - [Version Plus (Payante – Non disponible en France)](#version-plus-payante-non-disponible-en-france)
- [Bonnes Pratiques pour un Archivage Réussi](#bonnes-pratiques-pour-un-archivage-reussi)
  - [Stratégie de Stockage 3-2-1](#strategie-de-stockage-3-2-1)
  - [Optimisation des Performances](#optimisation-des-performances)
  - [Automatisation avec Cron](#automatisation-avec-cron)
- [Cas d’Usage : Quand Vanderplanki Devient Indispensable](#cas-d-usage-quand-vanderplanki-devient-indispensable)
  - [Le Freelance Organisé](#le-freelance-organise)
  - [L’Admin Système Prévoyant](#l-admin-systeme-prevoyant)
  - [Le Paranoïaque de la Vie Privée (à Juste Titre)](#le-paranoiaque-de-la-vie-privee-a-juste-titre)
- [Limites et Points d’Attention](#limites-et-points-d-attention)
  - [Ce qui Pourrait Vous Gêner](#ce-qui-pourrait-vous-gener)
  - [Comparaison avec MailStore Home](#comparaison-avec-mail-store-home)
- [Dépannage : Les Galères Classiques](#depannage-les-galeres-classiques)
  - [« Impossible de se connecter à IMAP »](#impossible-de-se-connecter-a-imap)
  - [« Archive corrompu »](#archive-corrompu)
  - [« Synchronisation lente »](#synchronisation-lente)
- [Verdict : Une Alternative Crédible ?](#verdict-une-alternative-credible)
- [Pour Aller Plus Loin](#pour-aller-plus-loin)


Vous cherchez une solution fiable pour sauvegarder vos emails sans dépendre d’un service cloud ? Vanderplanki pourrait bien être la perle rare que vous attendiez. Développé par les créateurs de MailStore, cet outil gratuit et open source promet de révolutionner la sauvegarde d’emails personnels.

Vanderplanki : Quand les Pros de l’Archivage se Remettent au Boulot

![Illustration 1 — Vanderplanki](mail-ijx5h0iafcbym.gif)L’histoire commence par une ironie savoureuse : les fondateurs de MailStore, **la** référence en matière d’archivage d’emails, ont vendu leur bébé à Carbonite (racheté depuis par OpenText). Résultat ? Ils se retrouvent avec une envie furieuse de recréer l’outil parfait, mais cette fois **vraiment** multi-plateforme et gratuit.

**Vanderplanki** (oui, ça sonne comme un village perdu au fin fond de la Scandinavie) est né de cette frustration créative. Et autant le dire tout de suite : c’est du sérieux.

### 🔧 **Les Fonctionnalités qui Font la Différence**

**Sources d’emails supportées :**

- Comptes IMAP (Gmail, Yahoo, etc.)
- Fichiers EML et MSG
- Support à venir : Microsoft Cloud (Outlook.com, Office 365)

**Sécurité de niveau enterprise :**

- Chiffrement end-to-end avec principe Zero Knowledge
- Hachage SHA-256 pour l’intégrité des données
- Format d’archive ouvert et documenté

**Stockage flexible :**

- Local (disque dur, SSD)
- NAS et serveurs réseau
- Stockage cloud
- Médias optiques

Installation et Configuration : Plus Simple qu’un Café du Matin 🍵

![Capture d'écran — Les Fonctionnalités qui Font la Différence](excited-yes-nicolas-cage-rrvzuoxldfe8m.gif)### Prérequis Système

Vanderplanki tourne sur **Windows, macOS et Linux**. Pour Linux, il est distribué sous forme d’AppImage, ce qui simplifie grandement l’installation.

### Étapes d’Installation

```bash
# Téléchargement (remplacez par la version actuelle)
wget https://releases.vanderplanki.com/vanderplanki-desktop-1.0.0.AppImage

# Rendre exécutable
chmod +x vanderplanki-desktop-1.0.0.AppImage

# Lancement
./vanderplanki-desktop-1.0.0.AppImage

```

Serveur IMAP : imap.gmail.com
Port : 993
Sécurité : SSL/TLS
Nom d'utilisateur : votre.email@gmail.com
Mot de passe : [Mot de passe d'application si 2FA activé]


<strong>💡 À savoir :</strong> Depuis juin 2024, Gmail active automatiquement l'accès IMAP. Plus besoin de bidouiller dans les paramètres !

Version Gratuite vs Plus : Que Choisir ?

### Version Basic (Gratuite)

- Jusqu’à **5 comptes email**
- Archivage de fichiers illimité
- Tous les emplacements de stockage
- Support communautaire

### Version Plus (Payante – Non disponible en France)

- Comptes email illimités
- Archives multiples
- Connexions cloud étendues
- Support prioritaire

<strong>🇫🇷 Statut France :</strong> Actuellement, Vanderplanki n'est officiellement disponible qu'en Allemagne, Autriche et Suisse. La version payante n'est donc pas accessible depuis la France, mais la version gratuite fonctionne parfaitement.

Bonnes Pratiques pour un Archivage Réussi

### Stratégie de Stockage 3-2-1

Appliquez la règle d’or de la sauvegarde :

- **3** copies de vos données
- **2** supports différents
- **1** copie hors site

```bash
# Example de configuration multi-emplacements
/home/user/vanderplanki-archive/     # Local SSD
/mnt/nas/email-backup/               # NAS local
/mnt/cloud/vanderplanki/             # Cloud mount

```

# Synchronisation quotidienne à 2h du matin
0 2 * * * /home/user/vanderplanki-desktop.AppImage --sync-all --headless


Cas d’Usage : Quand Vanderplanki Devient Indispensable

### Le Freelance Organisé

*« J’ai 15 ans d’emails clients éparpillés sur 4 comptes différents. Vanderplanki m’a permis de tout centraliser avec une recherche ultra-rapide. »*

### L’Admin Système Prévoyant

*« Avec la version gratuite, je sauvegarde les comptes email critiques de notre PME. Le format ouvert me rassure pour la pérennité. »*

### Le Paranoïaque de la Vie Privée (à Juste Titre)

*« Zero Knowledge + stockage local = mes emails restent vraiment privés. Même les développeurs ne peuvent pas y accéder. »*

Limites et Points d’Attention

### Ce qui Pourrait Vous Gêner

❌ **Pas de support Exchange direct** (contournement via IMAP possible)  
❌ **Interface en anglais/allemand uniquement**  
❌ **Pas de version web** (desktop only)  
❌ **Géolocalisation limitée** (officiellement DACH uniquement)

### Comparaison avec MailStore Home

Fonctionnalité | Vanderplanki | MailStore Home | **Multi-plateforme** | ✅ Win/Mac/Linux | ❌ Windows uniquement | **Format ouvert** | ✅ Documenté | ❌ Propriétaire | **Usage commercial** | ✅ Autorisé | ❌ Payant | **Maturité** | ⚠️ Récent | ✅ 15+ ans | 

Dépannage : Les Galères Classiques

### « Impossible de se connecter à IMAP »

```bash
# Vérification des ports
telnet imap.gmail.com 993
# Si ça fonctionne, c'est un problème d'authentification

```

## Articles connexes

- [LocalWP : Ton lab WordPress en 5 min (guide complet 2025 + m](/installer-localwp-wordpress-local/)
- [Arc Browser abandonné : 7 alternatives épurées pour retrouve](/arc-browser-alternatives-navigateur-epure-2025/)
