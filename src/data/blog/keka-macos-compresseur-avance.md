---
title: "Keka macOS : compresseur avancé gratuit (7z, split, chiffrement AES)"
description: "Keka macOS : l'archiveur gratuit et open source qui gère 7z, zip chiffré AES-256, split de fichiers et plus de 30 formats en glisser-déposer."
pubDatetime: "2026-09-18T11:01:11+02:00"
modDatetime: "2026-09-17T08:00:00.000Z"
author: Brandon
tags:
  - macos
  - homebrew
  - guide
  - avance
featured: false
draft: false
focusKeyword: keka macos
faqs:
  - question: "Keka macOS est-il vraiment gratuit ?"
    answer: "Oui, le téléchargement direct depuis keka.io et l'installation via Homebrew sont gratuits. Seule la version du Mac App Store est payante, environ 6,49 dollars, et c'est juste un moyen de soutenir le développeur puisqu'elle n'ajoute aucune fonctionnalité."
  - question: "Keka peut-il ouvrir une archive RAR protégée par mot de passe ?"
    answer: "Keka extrait le RAR sans souci et te demande le mot de passe si l'archive en a un. Par contre il ne crée pas de RAR en sortie, ce format reste propriétaire et Keka ne fait que le lire."
  - question: "Le chiffrement AES-256 de Keka est-il compatible avec 7-Zip sous Windows ou Linux ?"
    answer: "Oui, une archive 7z chiffrée en AES-256 avec Keka s'ouvre sans problème avec 7-Zip sur Windows ou p7zip sous Linux, tant que la personne en face connaît le mot de passe."
---
> 💡 **TL;DR**
> - Keka macOS compresse en 7z, zip, tar et une dizaine d'autres formats, avec chiffrement AES-256 et découpage en volumes pour les gros fichiers
> - Gratuit et open source via [keka.io](https://www.keka.io) ou `brew install --cask keka`, payant seulement sur le Mac App Store (juste pour soutenir le dev)
> - Extraction de plus de 30 formats dont RAR, glisser-déposer natif, et un binaire en ligne de commande pour automatiser tes scripts de sauvegarde

## Keka macOS : l'archiveur qu'il te faut

L'app Archive Utility fournie avec macOS fait le café, mais rien de plus. Elle zippe, elle dézippe, et c'est à peu près tout. Le jour où tu veux un 7z, chiffrer une archive avant de l'envoyer à un client, ou découper un fichier de 8 Go pour le faire tenir sur une clé USB de la préhistoire, tu es coincé.

C'est exactement le trou que comble **Keka macOS**. Un archiveur natif, gratuit, open source, qui gère à peu près tous les formats que tu croiseras dans ta vie d'admin sys ou de dev : 7z, zip avec vrai chiffrement, tar, gzip, et l'extraction de plus de 30 formats différents dont le RAR. Chez moi, il a remplacé The Unarchiver et l'app système le même jour.

## Table des matières

## Installation : Homebrew, App Store ou direct

Trois façons d'installer Keka macOS, et elles ne se valent pas toutes.

La plus propre si tu gères déjà tes apps en ligne de commande :

```bash
brew install --cask keka
```

Ça installe la version 1.6.7 (au moment où j'écris ces lignes), directement depuis les releases GitHub du projet. Compatible dès macOS 10.10, donc aucune excuse si tu es encore sur un Mac Intel un peu ancien.

Sinon, direct depuis [keka.io](https://www.keka.io), un `.dmg` classique à glisser dans `/Applications`. Gratuit, identique à la version Homebrew, mise à jour manuelle.

Troisième option, le Mac App Store, à environ 6,49 dollars. Zéro différence fonctionnelle avec la version gratuite. Tu paies juste pour la mise à jour automatique via l'App Store et pour filer un peu d'argent au développeur, aonez, qui maintient le projet en solo sur [GitHub](https://github.com/aonez/Keka) sous licence GPL. Si Keka te sert tous les jours, c'est un bon geste.

Au premier lancement, configure Keka comme extracteur par défaut dans ses préférences si tu veux qu'un double-clic sur n'importe quelle archive l'ouvre directement, plutôt que l'app système.

## Formats supportés et chiffrement AES-256

Là où Archive Utility te propose zip et basta, Keka macOS crée des archives dans une bonne dizaine de formats : 7Z, ZIP, TAR, GZIP, BZIP2, XZ, LZIP, DMG, ISO, en plus de formats plus exotiques comme Brotli ou Zstandard pour les cas de compression pointus.

Côté extraction, c'est encore plus large : plus de 30 formats reconnus, RAR compris. Tu ne peux pas créer de RAR avec Keka (le format reste propriétaire), mais tu peux ouvrir n'importe quelle archive RAR qu'on t'envoie, protégée par mot de passe ou non.

Le vrai argument pour un usage pro, c'est le chiffrement. Keka propose l'AES-256 pour tes archives 7z, et le chiffrement legacy Zip 2.0 pour la compatibilité avec de vieux outils. En pratique :

1. Glisse tes fichiers dans la fenêtre Keka
2. Choisis 7z comme format de sortie
3. Coche le chiffrement et tape un mot de passe
4. Compresse

L'archive résultante est illisible sans le mot de passe, et le chiffrement est compatible avec 7-Zip sur Windows ou p7zip sous Linux. Pratique quand tu dois envoyer un dump de base de données ou une sauvegarde de configs à un collègue, sans passer par un service tiers pour le chiffrement.

⚠️ Le chiffrement Zip 2.0 legacy est là pour la compatibilité, pas pour la sécurité. Si tu veux vraiment protéger un fichier sensible, choisis 7z en AES-256, pas le zip classique.

## Split de fichiers volumineux

Découper une grosse archive en plusieurs morceaux, c'est un besoin qui revient plus souvent qu'on ne le pense : upload sur un service qui plafonne la taille des fichiers, transfert sur une clé USB au format FAT32 limité à 4 Go, ou simplement pour paralléliser un envoi sur plusieurs supports.

Dans Keka macOS, tu actives le split au moment de la compression en définissant une taille de volume (100 Mo, 700 Mo, 4 Go, ou une valeur personnalisée). Tu obtiens une série de fichiers `.7z.001`, `.7z.002`, etc. Pour reconstituer l'archive de l'autre côté, il suffit d'avoir tous les morceaux dans le même dossier et de double-cliquer sur le premier : Keka (ou n'importe quel outil compatible 7z multi-volumes) reconstitue le tout automatiquement.

✅ Astuce homelab : si tu sauvegardes une VM ou un export de conteneur avant de le déplacer sur un NAS avec une limite de taille par fichier, le split 7z te sort de la galère sans passer par des scripts `split` en ligne de commande.

## Keka en ligne de commande et automatisation

Keka macOS installe aussi un binaire utilisable depuis le Terminal, ce qui change tout si tu veux automatiser des sauvegardes plutôt que glisser-déposer à la main. C'est là que Keka dépasse largement l'app système, qui elle n'expose rien en CLI.

Ce binaire s'intègre bien dans un script shell classique : tu déclenches la compression d'un dossier de logs ou de configs à intervalle régulier, avec chiffrement AES-256 si le résultat part vers un stockage externe. Si tu es du genre à automatiser tout ton Mac, ça s'articule très bien avec [Hammerspoon macOS](/hammerspoon-macos-scripting-lua/) : un script Lua qui déclenche une compression chiffrée à heure fixe, puis envoie l'archive sur ton NAS, sans toucher à la souris.

Pour les lancements ponctuels plutôt que planifiés, j'utilise plutôt [Bunch macOS](/bunch-macos-lancer-contextes/) : un contexte « archivage projet » qui ouvre le bon dossier Finder et lance Keka en même temps, histoire de ne pas chercher les fichiers à chaque fois.

## Keka macOS vs les alternatives

The Unarchiver reste correct pour extraire des archives, gratuit, léger, mais il ne crée que du zip en sortie. Zéro chiffrement, zéro 7z, zéro split. Si tu ne fais qu'ouvrir des fichiers reçus, ça suffit. Si tu dois en créer, tu es limité.

BetterZip va plus loin niveau interface, avec un mode aperçu façon Finder très pratique, mais c'est un logiciel payant, autour de 20 dollars, pour des fonctionnalités que Keka couvre déjà gratuitement.

Archive Utility, l'app native de macOS, ne propose ni 7z, ni chiffrement AES sérieux, ni split. Elle fait le strict minimum et c'est très bien pour dézipper une pièce jointe, mais elle n'a rien à faire dans le même match que Keka.

Pour un usage avancé, gratuit et open source, Keka reste devant. Le seul vrai concurrent sérieux serait Keka lui-même en version App Store, pour ceux qui préfèrent payer pour la mise à jour automatique.

## Limites et points de vigilance

Keka n'a pas que des qualités :

- **Pas de création RAR** : logique, le format appartient à RARLAB, mais si ton flux de travail impose du RAR en sortie, il te faut un autre outil.
- **Interface minimaliste** : pas d'aperçu intégré des fichiers dans l'archive comme chez BetterZip. Tu dois extraire pour vérifier le contenu.
- **Documentation en ligne de commande limitée** : le binaire CLI existe mais reste peu documenté officiellement, il faut parfois tester à la main pour trouver la bonne syntaxe.
- **Mise à jour manuelle hors App Store** : la version Homebrew ou directe ne se met pas à jour toute seule, contrairement à la version payante.

Rien de bloquant, mais autant le savoir avant de construire un workflow critique dessus.

## Conclusion

Keka macOS coche toutes les cases d'un bon outil : gratuit, open source, natif, léger, et il fait un travail que l'app système ne sait pas faire. Le chiffrement AES-256 en fait un vrai outil pro pour qui doit envoyer des fichiers sensibles, et le split de fichiers rend service dès que tu bosses avec des supports ou des services limités en taille.

Il rejoint dans ma barre à outils macOS des apps comme [One Switch](/one-switch-macos-panneau-controle/) et [Numi](/numi-macos-calculatrice-textuelle/), toutes gratuites, natives, et sans excuse pour ne pas les installer.

```bash
brew install --cask keka
```

Deux minutes d'installation, et tu ne rouvriras plus jamais Archive Utility.
