---
title: "TwinDesk : un clavier et une souris pour ton Mac, ton PC et ton Android"
description: TwinDesk partage clavier, souris, presse-papiers et fichiers entre Mac, Windows, Linux et Android, sans câble ni compte cloud à créer.
pubDatetime: "2026-11-06T11:00:40+01:00"
modDatetime: "2026-11-05T08:00:00.000Z"
author: Brandon
tags:
  - macos
  - productivite
  - homebrew
  - intermediaire
featured: false
draft: false
focusKeyword: twindesk
faqs:
  - question: "TwinDesk fonctionne-t-il sans réseau Wi-Fi partagé ?"
    answer: "Oui. En plus du Wi-Fi classique, TwinDesk se connecte en Bluetooth, en Wi-Fi Direct, via le partage de connexion du téléphone ou par câble USB, donc même sans box commune entre tes machines."
  - question: "Faut-il créer un compte pour utiliser TwinDesk ?"
    answer: "Non. Le logiciel est local-first : aucun compte, aucun identifiant, aucune donnée qui transite par un serveur tiers. Les appareils se parlent directement entre eux."
  - question: "TwinDesk est-il compatible avec un iPhone ?"
    answer: "Pas pour l'instant. Seul Android (version 10 et supérieure) est pris en charge côté téléphone, l'éditeur ne mentionne aucun support iOS en développement."
---
> 💡 **TL;DR**
> - TwinDesk partage un seul clavier et une seule souris entre Mac, Windows, Linux et Android, gratuit et open source (GPL-3.0)
> - Installation en une commande : `brew install --cask inukaasith/twindesk/twindesk` sur macOS, paquet natif sur Windows et Linux, APK pour Android
> - Presse-papiers, fichiers glissés d'un écran à l'autre et écran étendu en bonus, sans compte ni cloud, même sans Wi-Fi partagé

## TwinDesk : un clavier et une souris pour tout ton setup

T'as un Mac pour le taf, un PC pour jouer, et un téléphone Android qui traîne entre les deux. Trois claviers, trois souris, et le geste débile de te pencher vers l'autre écran chaque fois qu'une notif arrive sur ton téléphone. Chez moi c'était exactement ça jusqu'à ce que je teste TwinDesk.

Le principe tient en une phrase : un seul clavier, une seule souris, le pointeur traverse le bord de l'écran et change de machine comme s'il n'y avait jamais eu de frontière. Gratuit, open source, et surtout activement mis à jour, ce qui n'est pas rien dans cette catégorie d'outils où pas mal de projets finissent à l'abandon.

## Table des matières

## Qu'est-ce que TwinDesk, concrètement

TwinDesk est développé par InukaAsith et publié sous licence GPL-3.0 sur GitHub. Pas de société derrière, pas d'offre payante cachée : le site officiel le dit noir sur blanc, pas de compte, pas d'abonnement, pas de cloud. Les appareils communiquent directement entre eux.

Ce qui distingue TwinDesk d'un simple partage souris-clavier classique :

- **Multi-plateforme large** : macOS 13 et plus, Windows 10/11 (x64 et ARM64), Linux x86_64 sous X11 comme sous Wayland, et Android 10 et plus.
- **Ton téléphone devient un vrai poste de travail** : fichiers, presse-papiers, appels, SMS, notifications et même la caméra accessibles depuis l'ordinateur.
- **Écran étendu** : un vieux laptop ou une tablette peut servir de moniteur additionnel, en miroir ou en extension réelle.
- **Connexion sans réseau partagé** : Bluetooth, Wi-Fi Direct, partage de connexion du téléphone ou câble USB, pour les cas où tes machines ne sont pas sur le même Wi-Fi.
- **Mode Mesh (bêta)** : plusieurs appareils reliés en même temps, pas juste une paire.

Le rythme de sortie donne une bonne idée du sérieux du projet : v2.2.0 le 23 octobre, v2.3.0 le 26, v2.4.0 le 28, puis v2.5.3 début novembre. Une mise à jour quasi hebdomadaire, ce qui change de pas mal d'utilitaires open source qui sortent une version par trimestre, si tout va bien.

## Installer TwinDesk sur macOS, Windows et Linux

Sur Mac, le plus propre passe par Homebrew, mais attention à un détail : le cask n'est pas encore dans le dépôt principal `homebrew/cask`, il faut passer par le tap du projet.

```bash
brew install --cask inukaasith/twindesk/twindesk
```

Une mise à jour future se fait ensuite normalement :

```bash
brew upgrade --cask twindesk
```

Si tu préfères le `.dmg` manuel, deux builds existent selon ta puce : `TwinDesk-2.5.3-arm64.dmg` pour Apple Silicon, `TwinDesk-2.5.3-x64_Intel.dmg` pour Intel.

⚠️ L'application n'est pas signée par un certificat développeur payant. macOS va probablement afficher un message « application endommagée » au premier lancement. La solution officielle, documentée par le projet lui-même :

```bash
xattr -dr com.apple.quarantine /Applications/TwinDesk.app
```

Sur Windows, télécharge `TwinDesk-Setup-2.5.3.exe` (ou la variante `-arm64` sur les machines ARM). Windows SmartScreen va aussi grogner au premier lancement, normal pour un installeur non signé par une autorité payante : clique sur « informations complémentaires » puis « exécuter quand même ».

Sur Linux, trois formats au choix selon ta distro :

```bash
# AppImage, universel
chmod +x TwinDesk-2.5.3-x86_64.AppImage
./TwinDesk-2.5.3-x86_64.AppImage

# Debian/Ubuntu
sudo dpkg -i TwinDesk-2.5.3-amd64.deb

# Arch Linux
sudo pacman -U twindesk-bin-2.5.3-1-x86_64.pkg.tar.zst
```

NixOS est aussi couvert directement, sans installation préalable :

```bash
nix run github:InukaAsith/TwinDesk
```

Pour les trois systèmes, l'app demande les permissions d'accessibilité ou d'enregistrement d'écran au premier lancement. C'est elle qui doit voir où est ton pointeur et simuler les frappes clavier sur l'autre machine, donc ce n'est pas négociable. Si tu oublies régulièrement où se cache cette permission dans les préférences macOS, [One Switch](/one-switch-macos-panneau-controle/) te donne un accès direct à ce genre de réglages sans fouiller dans les Réglages Système à chaque fois.

## Connecter ton Android en quelques clics

Le téléphone Android se comporte comme un pair à part entière, pas comme un simple écran distant. Dès l'installation de l'APK, le presse-papiers, les fichiers et les notifications remontent sans réglage supplémentaire.

Pour le contrôle souris/clavier et le miroir d'écran, il faut en revanche activer une fois le débogage sans fil (Android 11 et plus), dans les options développeur du téléphone. C'est la même autorisation que celle utilisée par Android Studio, rien de propre à TwinDesk.

Deux APK sont proposés : la version standard, et une version « full » qui ajoute l'accès aux appels, aux SMS et à l'accessibilité système. Cette seconde version nécessite de désactiver temporairement Play Protect lors de l'installation, Google n'aimant pas les APK distribués hors Play Store.

✅ Vérification rapide : installe l'APK, ouvre TwinDesk sur ton ordinateur, scanne le QR code ou saisis le code d'appairage affiché. Si le presse-papiers se synchronise dans les deux sens en moins de cinq secondes, l'appairage est bon.

## Les fonctionnalités qui comptent vraiment au quotidien

Passé l'installation, ce sont les détails du jour le jour qui font la différence entre un gadget et un outil qu'on garde.

### Souris et clavier qui traversent les écrans

Tu positionnes virtuellement tes écrans les uns par rapport aux autres dans les réglages (le Mac à gauche, le PC à droite, par exemple), et le pointeur passe d'une machine à l'autre en franchissant le bord correspondant. Le clavier suit automatiquement, sans raccourci à mémoriser pour « basculer ».

Pour la sensation au quotidien, le pointeur reste fluide d'une machine à l'autre, mais si ta souris a tendance à sauter ou à mal gérer le défilement une fois sur le Mac, le réglage par défaut de macOS n'aide pas vraiment : [Mos](/mos-macos-defilement-souris-fluide/) lisse ce défilement et t'évite cette sensation de souris qui rame juste après avoir traversé l'écran.

### Presse-papiers et fichiers partagés

Le copier-coller fonctionne pour le texte comme pour les images, jusqu'à 10 Mo par élément. Pour les fichiers plus lourds ou les dossiers entiers, deux méthodes : le glisser-déposer au bord de l'écran, ou le raccourci dédié ⌃⌥C pour copier et ⌃⌥V pour coller (Ctrl+Alt sous Windows et Linux).

💡 Ce raccourci n'est pas le plus intuitif à retenir au début. Si tu as l'habitude d'ouvrir une cheatsheet de raccourcis dès que tu changes d'app, [l'alternative qui a remplacé CheatSheet](/cheatsheet-macos-raccourcis-clavier/) t'évite de revenir sur cet article à chaque fois que tu oublies la combinaison.

### Écran étendu et Mesh

Une machine peut servir d'écran supplémentaire à une autre, en miroir ou en extension réelle avec sa propre résolution. C'est pratique pour recycler un vieux laptop ou une tablette Android comme second moniteur de dépannage. Si tu pousses ce genre de montage avec un vrai écran externe plutôt qu'un laptop recyclé, la gestion fine des résolutions et du DDC côté [BetterDisplay](/betterdisplay-macos-hidpi-ddc/) reste complémentaire, TwinDesk gère le partage clavier-souris, pas le pilotage avancé de l'écran lui-même.

Le mode Mesh, encore en bêta, relie plusieurs appareils simultanément plutôt qu'une simple paire. Utile si ton setup dépasse les deux écrans, mais attends-toi à quelques aspérités tant que la fonctionnalité n'est pas stabilisée.

### Le téléphone comme télécommande et webcam

Au-delà du contrôle clavier-souris, le téléphone peut servir de pavé tactile, de manette de jeu, et sa caméra devient utilisable comme webcam dans Zoom, Teams ou Meet. Pratique si ta webcam intégrée est à des années-lumière de celle de ton téléphone, ce qui est le cas sur pas mal de laptops d'entrée de gamme.

## TwinDesk face à Deskflow, Barrier et Synergy

Si tu cherches un partage clavier-souris en ligne de commande, tu es sûrement déjà tombé sur Deskflow, Barrier, ou l'ancêtre Synergy. Deskflow est aujourd'hui le projet le plus actif de cette lignée : fork maintenu de Barrier (lui-même dérivé de Synergy), compatible avec les trois, et doté du chiffrement TLS par défaut.

La vraie différence ne se joue pas sur le clavier-souris, où les deux font le travail correctement. Elle se joue sur tout ce qui l'entoure :

- Deskflow vise strictement Windows, macOS et Linux, sans volet Android.
- TwinDesk intègre le téléphone comme un pair complet : fichiers, presse-papiers, SMS, appels, caméra.
- Deskflow suppose un réseau local partagé entre les machines. TwinDesk ajoute Bluetooth, Wi-Fi Direct, partage de connexion et USB pour les cas où ce réseau commun n'existe pas.
- Deskflow ne propose pas d'écran étendu. TwinDesk si, même si l'implémentation reste plus jeune et moins mature.

Si ton usage se limite à deux PC fixes sur le même switch, Deskflow fait le job avec une base de code plus ancienne et plus éprouvée. Si l'Android fait partie de l'équation ou que tes machines changent souvent de réseau, TwinDesk couvre un terrain que Deskflow ne vise pas.

## Limites et points de vigilance

TwinDesk n'est pas exempt de défauts, et autant les connaître avant de l'adopter en usage quotidien.

- **Pas d'iPhone.** Seul Android est pris en charge côté téléphone, aucune mention d'un support iOS à venir sur le site officiel.
- **Binaires non signés.** Attends-toi au message Gatekeeper sur Mac et SmartScreen sur Windows à chaque nouvelle version installée manuellement, le correctif `xattr` du dessus reste valable.
- **Extension d'écran limitée sous Linux avec NVIDIA.** La documentation du projet est explicite : la fonctionnalité d'écran étendu via X11 ne fonctionne pas avec le pilote propriétaire NVIDIA.
- **Mesh en bêta.** Le mode multi-appareils simultané est jeune, à tester avant de t'y fier pour un setup de travail critique.
- **Un projet encore jeune porté par un développeur principal.** Le rythme de sortie est rassurant, mais la dépendance à un seul mainteneur reste un facteur à surveiller sur la durée, comme pour n'importe quel outil open source récent.

Rien de rédhibitoire, mais ce sont exactement les points que je vérifierais avant de baser un poste de travail professionnel entier dessus plutôt que de le garder en complément.

## Conclusion

TwinDesk fait ce que son nom promet : transformer deux ou trois appareils disparates en un seul poste de travail, sans jongler entre claviers. Le fait qu'il couvre Android comme un vrai pair, et pas comme un gadget annexe, le distingue clairement de Deskflow et consorts.

Si ton quotidien mélange Mac, PC et Android, l'installation vaut clairement les cinq minutes que ça prend. Commence par la paire Mac-PC, ajoute le téléphone ensuite, et juge sur deux semaines d'usage réel avant de décider si ça remplace ou complète ton setup actuel.
