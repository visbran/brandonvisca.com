---
title: "Vanderplanki : sauvegarde email gratuite et multi-plateforme (guide 2026)"
description: Sauvegarde tes emails gratuitement avec Vanderplanki — chiffré, multi-plateforme, open source. Par les créateurs de MailStore. Guide 2026.
pubDatetime: "2025-06-12T19:38:49+02:00"
modDatetime: "2026-04-14T00:00:00+01:00"
author: Brandon Visca
tags:
  - backup
  - linux
  - debutant
featured: false
draft: false
focusKeyword: Vanderplanki
faqs:
  - question: "Vanderplanki supporte-t-il Gmail, Outlook et d'autres fournisseurs ?"
    answer: "Oui. Vanderplanki supporte tous les fournisseurs IMAP standard : Gmail, Outlook, Proton Mail (via bridge), Fastmail, et tout serveur IMAP auto-hébergé (Dovecot, Postfix)."
  - question: "Les emails sauvegardés par Vanderplanki sont-ils chiffrés ?"
    answer: "Oui. Vanderplanki chiffre les sauvegardes avec AES-256 avant de les stocker. Seul ton mot de passe (ou clé) permet de déchiffrer les données — même l'équipe Vanderplanki ne peut pas accéder à tes emails."
  - question: "Peut-on restaurer des emails depuis une sauvegarde Vanderplanki ?"
    answer: "Oui. La restauration se fait depuis l'interface Vanderplanki : tu sélectionnes les emails ou dossiers à restaurer et les réimporter dans n'importe quel compte IMAP compatible."
---
> 💡 **TL;DR**
> - Vanderplanki est un outil gratuit de sauvegarde d'emails, développé par les fondateurs de MailStore — contrairement à son prédécesseur, il tourne sur Windows, macOS **et** Linux
> - Chiffrement Zero Knowledge, format d'archive ouvert, stockage local ou NAS : tes emails restent sous ton contrôle
> - La version gratuite couvre 5 comptes email ; la version payante n'est pour l'instant disponible qu'en zone DACH (Allemagne, Autriche, Suisse)

## Table des matières

Sauvegarder ses emails sans dépendre d'un cloud tiers, c'est le genre de truc qu'on remet à plus tard jusqu'au jour où ça foire. Vanderplanki règle le problème proprement : gratuit, multi-plateforme, chiffré. Et derrière, c'est les créateurs de MailStore qui ont remis le couvert.

## Vanderplanki : quand les pros de l'archivage se remettent au boulot

L'histoire commence par une ironie savoureuse : les fondateurs de MailStore, **la** référence en matière d'archivage d'emails, ont vendu leur bébé à Carbonite (racheté depuis par OpenText). Résultat ? Ils se retrouvent avec une envie furieuse de recréer l'outil parfait, mais cette fois **vraiment** multi-plateforme et gratuit.

**Vanderplanki** (oui, ça sonne comme un village perdu au fin fond de la Scandinavie) est né de cette frustration créative. Et autant le dire tout de suite : c'est du sérieux.

### Les fonctionnalités qui font la différence

**Sources d'emails supportées :**

- Comptes IMAP (Gmail, Yahoo, etc.)
- Fichiers EML et MSG
- Support à venir : Microsoft Cloud (Outlook.com, Office 365)

**Sécurité de niveau enterprise :**

- Chiffrement end-to-end avec principe Zero Knowledge
- Hachage SHA-256 pour l'intégrité des données
- Format d'archive ouvert et documenté

**Stockage flexible :**

- Local (disque dur, SSD)
- NAS et serveurs réseau
- Stockage cloud
- Médias optiques

## Installation et configuration

Vanderplanki tourne sur **Windows, macOS et Linux**. Pour Linux, il est distribué sous forme d'AppImage, ce qui simplifie grandement l'installation.

### Étapes d'installation (Linux)

```bash
# Téléchargement (remplace par la version actuelle depuis le site officiel)
wget https://releases.vanderplanki.com/vanderplanki-desktop-1.0.0.AppImage

# Rendre exécutable
chmod +x vanderplanki-desktop-1.0.0.AppImage

# Lancement
./vanderplanki-desktop-1.0.0.AppImage
```

### Configuration IMAP — exemple Gmail

```text
Serveur IMAP : imap.gmail.com
Port         : 993
Sécurité     : SSL/TLS
Identifiant  : ton.email@gmail.com
Mot de passe : [mot de passe d'application si 2FA activé]
```

> 💡 **Astuce :** depuis juin 2024, Gmail active automatiquement l'accès IMAP. Plus besoin de bidouiller dans les paramètres.

## Version gratuite vs Plus : que choisir ?

### Version Basic (gratuite)

- Jusqu'à **5 comptes email**
- Archivage de fichiers illimité
- Tous les emplacements de stockage
- Support communautaire

### Version Plus (payante — non disponible en France)

- Comptes email illimités
- Archives multiples
- Connexions cloud étendues
- Support prioritaire

> ⚠️ **Attention :** Vanderplanki n'est officiellement disponible qu'en Allemagne, Autriche et Suisse. La version payante n'est donc pas accessible depuis la France, mais la version gratuite fonctionne parfaitement.

## Bonnes pratiques pour un archivage réussi

### Stratégie 3-2-1

Applique la règle d'or de la sauvegarde :

- **3** copies de tes données
- **2** supports différents
- **1** copie hors site

```bash
# Exemple de configuration multi-emplacements
/home/user/vanderplanki-archive/     # SSD local
/mnt/nas/email-backup/               # NAS local
/mnt/cloud/vanderplanki/             # Cloud monté localement
```

### Automatisation avec cron

```bash
# Synchronisation quotidienne à 2h du matin
0 2 * * * /home/user/vanderplanki-desktop.AppImage --sync-all --headless
```

## Cas d'usage : quand Vanderplanki devient indispensable

**Le freelance organisé :** 15 ans d'emails clients éparpillés sur 4 comptes différents. Vanderplanki centralise tout avec une recherche rapide.

**L'admin système prévoyant :** avec la version gratuite, tu sauvegardes les comptes email critiques d'une PME. Le format ouvert garantit la pérennité.

**Le paranoïaque de la vie privée (à juste titre) :** Zero Knowledge + stockage local = tes emails restent vraiment privés. Même les développeurs ne peuvent pas y accéder.

## Limites et points d'attention

❌ **Pas de support Exchange direct** (contournement via IMAP possible)
❌ **Interface en anglais/allemand uniquement**
❌ **Pas de version web** (desktop only)
❌ **Géolocalisation limitée** (officiellement DACH uniquement)

### Vanderplanki vs MailStore Home

| Fonctionnalité | Vanderplanki | MailStore Home |
|---|---|---|
| Multi-plateforme | ✅ Win/Mac/Linux | ❌ Windows uniquement |
| Format ouvert | ✅ Documenté | ❌ Propriétaire |
| Usage commercial | ✅ Autorisé | ❌ Payant |
| Maturité | ⚠️ Récent | ✅ 15+ ans |

## Dépannage : les galères classiques

### « Impossible de se connecter à IMAP »

```bash
# Vérification des ports
telnet imap.gmail.com 993
# Si ça fonctionne, c'est un problème d'authentification
```

Pour Gmail avec 2FA activé, génère un [mot de passe d'application](https://myaccount.google.com/apppasswords) dédié — le mot de passe principal ne fonctionnera pas.

### « Archive corrompue »

Si Vanderplanki signale une archive corrompue, utilise l'outil de vérification intégré (menu `Archive > Vérifier l'intégrité`). Les hachages SHA-256 permettent de détecter toute altération.

### « Synchronisation lente »

Divise par compte email et réduis la plage de dates initiale. Une première synchronisation de 10 ans d'emails prend du temps. C'est normal.

## Conclusion

Vanderplanki est une alternative sérieuse à MailStore Home pour quiconque tourne sur macOS ou Linux. Le format d'archive ouvert et le chiffrement Zero Knowledge en font un choix défendable pour les paranoïaques de la souveraineté des données.

L'outil est encore jeune, l'interface reste en anglais/allemand, et la disponibilité géographique est limitée. Mais ça fonctionne. Si tu jonglais jusqu'ici avec des scripts `mbsync` bricolés ou des exports MBOX à la main, c'est clairement un upgrade.

Télécharge Vanderplanki sur [vanderplanki.com](https://vanderplanki.com) et commence avec tes 5 comptes gratuits.

## Pour aller plus loin

- [Import PST / Outlook 365 — guide complet](/import-pst-outlook-365-guide-complet/)
- [Site officiel Vanderplanki](https://vanderplanki.com) — téléchargement et documentation
- [Dépôt GitHub MailStore](https://github.com/mailstore) — contexte historique du projet

## Articles connexes

- [Auto-hébergement : Le guide ultime 2025 pour reprendre contrôle de vos données](/auto-hebergement-guide-complet-2025/)
- [Comment définir le fuseau horaire et synchroniser l'heure du serveur sous Linux](/comment-modifier-heure-du-serveur-sous-linux/)
- [Docker pour les débutants : 10 services essentiels à auto-héberger en 2025](/docker-debutant-services-auto-heberger/)
- [S3cmd : synchronise et sauvegarde vers Amazon S3 gratuitement (guide 2026)](/gerer-fichiers-amazon-s3-avec-s3cmd/)
