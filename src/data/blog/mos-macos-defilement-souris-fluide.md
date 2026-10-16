---
title: "Mos macOS defilement souris fluide : lissage et inversion scroll"
description: "Mos macos defilement souris fluide : l'app qui lisse et inverse le scroll d'une souris classique sur Mac, par axe et par appli."
pubDatetime: "2026-10-16T11:01:11+02:00"
modDatetime: "2026-10-15T08:00:00.000Z"
author: Brandon Visca
tags:
  - macos
  - homebrew
  - intermediaire
featured: false
draft: false
focusKeyword: mos macos defilement souris fluide
faqs:
  - question: "Mos ralentit-il mon Mac ?"
    answer: "Non, Mos tourne en arrière-plan avec une empreinte CPU et RAM négligeable. C'est un utilitaire de barre de menus, pas un service lourd."
  - question: "Mos fonctionne-t-il avec un trackpad ?"
    answer: "Le trackpad Apple a déjà un défilement fluide natif. Mos cible les souris filaires ou Bluetooth classiques, qui envoient des pas de défilement bruts."
  - question: "Que se passe-t-il si je désinstalle Mos ?"
    answer: "Ta souris revient instantanément au défilement saccadé par défaut de macOS. Aucune trace ni fichier de config ne reste à nettoyer manuellement, à part le cask lui-même."
---
> 💡 **TL;DR**
> - Mos macOS lisse le défilement saccadé d'une souris classique et inverse le sens de scroll, séparément sur les deux axes
> - Gratuit, open source, installation en une ligne via `brew install --cask mos`
> - Réglages par application, remapping de boutons, compatible macOS 10.13 et plus récent

## Mos macOS : le défilement de souris enfin digne de ce nom

Tu branches une souris classique sur ton Mac après des mois de trackpad et tu redécouvres l'horreur : le défilement saute par paliers, comme sur un vieux PC sous Windows XP. Normal, macOS a été pensé pour le trackpad et la Magic Mouse, pas pour une souris filaire à molette crantée.

**Mos** règle ça en interceptant les événements de défilement de ta souris et en les réinterpolant pour obtenir un rendu lisse façon trackpad. Léger, open source, et gratuit. Chez moi, c'est la deuxième app installée après Homebrew sur un Mac neuf.

## Table des matières

## Mos macos defilement souris fluide : pourquoi macOS gère si mal les souris classiques

Le trackpad Apple et la Magic Mouse envoient des événements de défilement à haute fréquence, avec une accélération progressive native. Résultat : un scroll qui glisse.

Une souris filaire ou Bluetooth générique (Logitech, Razer, n'importe quelle souris de bureau) envoie des pas de molette bruts, un cran à la fois. macOS ne les lisse pas, il les affiche tels quels. D'où l'effet saccadé, presque désagréable à l'usage une fois qu'on a connu mieux.

C'est pour ça que mos macos defilement souris fluide revient si souvent en recherche : le problème touche quiconque bascule entre MacBook et poste fixe avec souris externe.

⚠️ Si tu utilises uniquement un trackpad Apple ou une Magic Mouse, Mos n'apporte rien : le défilement est déjà fluide nativement. L'app cible spécifiquement les souris tierces.

## Installation de Mos via Homebrew

Si tu n'as pas encore Homebrew, installe-le d'abord (ça prend deux minutes, c'est la base de tout setup macOS sérieux). Ensuite :

```bash
brew install --cask mos
```

Pour mettre à jour plus tard :

```bash
brew update && brew upgrade --cask mos
```

Sans Homebrew, tu peux récupérer `Mos.app` depuis les Releases du dépôt GitHub `Caldis/Mos` et le glisser dans `/Applications`.

Au premier lancement, macOS te réclame une autorisation d'accessibilité. **Accorde-la** : Mos a besoin de lire et réécrire les événements de défilement en temps réel, c'est le mécanisme même de l'app, pas une demande de permission abusive.

✅ L'app se loge dans la barre de menus. Pas de fenêtre principale à gérer, pas de Dock icon qui pollue ton espace de travail.

## Configurer le défilement fluide

Clique sur l'icône Mos dans la barre de menus, puis ouvre les préférences. Les réglages principaux :

- **Pas minimal** : la granularité du lissage, à ajuster selon ta molette
- **Gain de vitesse** : accélère ou ralentit la vitesse de défilement perçue
- **Durée** : la durée de l'animation d'interpolation, plus long = plus doux mais plus de latence perçue
- **Mode simulé trackpad** : reproduit le comportement d'inertie du trackpad plutôt qu'un simple lissage linéaire

Les axes vertical et horizontal se configurent **séparément**. Tu peux lisser le vertical sans toucher à l'horizontal, ou l'inverse.

## Inverser le sens de défilement par axe

C'est la deuxième fonction qui justifie l'app à elle seule. Si tu viens de Windows ou que tu préfères le sens "naturel" inversé sur un seul axe, Mos te laisse basculer vertical et horizontal indépendamment, dans l'onglet de configuration de chaque appareil.

Pratique si tu as plusieurs souris : une config Logitech, une config générique, chacune avec son propre sens de défilement mémorisé.

## Réglages par application

Mos permet de définir des réglages différents selon l'app au premier plan. Un lissage plus marqué dans un navigateur, désactivé dans un logiciel de montage où tu veux du scroll brut et précis frame par frame, par exemple.

Chaque app hérite des réglages globaux par défaut, tu ne configures que les exceptions dont tu as vraiment besoin. Pas besoin de tout reparamétrer à chaque nouvelle app installée.

💡 Pour désactiver temporairement le lissage sans ouvrir les préférences, Mos propose des touches de fonction dédiées, personnalisables, qui changent de sens ou coupent le lissage à la volée.

## Remapping de boutons et support Logitech

Mos ne se limite pas au scroll. Tu peux remapper des boutons de souris ou de clavier vers des actions système, des raccourcis, le lancement d'une app, un script ou un fichier.

Si tu es sur une souris Logitech avec récepteur Bolt ou Unifying, ou en Bluetooth direct, Mos reconnaît les boutons additionnels via le protocole HID++ de Logitech. Les boutons latéraux ou la molette inclinable deviennent exploitables sans passer par Logi Options+.

C'est un vrai argument pour remplacer Options+, souvent plus lourd et plus intrusif que nécessaire pour juste remapper deux boutons.

## Mos vs les alternatives

- **Logi Options+** : complet si tu es 100% sur du matériel Logitech, mais lourd, avec un service en arrière-plan permanent et une collecte de données que certains refusent. Mos reste minimaliste et open source.
- **Scroll Reverser** : fait l'inversion du scroll, rien de plus. Pas de lissage, pas de réglages par app, pas de remapping de boutons. Mos couvre un périmètre bien plus large pour un poids équivalent.
- **LinearMouse** : projet comparable, open source aussi, avec ses propres forces sur la sensibilité du pointeur. Le choix entre les deux est souvent une question de préférence personnelle plus que de fonctionnalités manquantes.

Si tu cherches à reprendre le contrôle de ta souris sans dépendre d'un fabricant, Mos et [One Switch macOS](/one-switch-macos-panneau-controle/) partagent la même philosophie : des réglages système qu'Apple ne t'expose pas, remis à ta portée dans un panneau simple.

## Cas d'usage concrets

**Poste fixe avec souris filaire** : lissage fort + mode trackpad simulé, pour retrouver une sensation proche du Mac portable sans changer de matériel.

**Montage vidéo ou audio** : lissage désactivé dans l'app concernée, scroll brut pour un défilement précis image par image dans la timeline.

**Multi-souris** : une config douce pour ta souris de bureau, une config neutre pour une souris de secours branchée en dépannage, chacune mémorisée séparément par Mos.

## Limites à connaître

Quelques points de vigilance avant d'installer Mos :

- **Licence non commerciale (CC BY-NC 4.0)** : gratuit pour un usage personnel, mais le projet n'est pas distribué sur le Mac App Store et sa licence encadre explicitement toute republication commerciale.
- **Pas de compatibilité trackpad** : l'app cible les souris, pas le trackpad intégré, déjà géré nativement.
- **Dépendance à l'accessibilité système** : si macOS révoque la permission après une mise à jour majeure (ça arrive), il faut la réaccorder manuellement dans Réglages Système.

## Dépannage : quand mos macos defilement souris fluide ne s'applique pas

Parfois l'app tourne mais le lissage ne se voit pas. Trois causes fréquentes, dans l'ordre à vérifier :

1. **Permission d'accessibilité révoquée.** Une mise à jour majeure de macOS repasse parfois ce réglage à zéro. Ouvre Réglages Système > Confidentialité et sécurité > Accessibilité, et vérifie que Mos est bien activé dans la liste.
2. **Mauvais appareil ciblé.** Si tu as plusieurs souris connectées, Mos applique le profil de l'appareil détecté. Vérifie dans les préférences que c'est bien ta souris active qui est sélectionnée, pas un profil générique resté par défaut.
3. **App en conflit.** Un autre utilitaire de souris (Logi Options+, SteerMouse, un pilote constructeur) peut intercepter les événements avant Mos et l'empêcher d'agir. Ferme l'autre utilitaire et redémarre Mos pour vérifier.

Si rien de tout ça ne marche, quitte complètement Mos (pas juste fermer la fenêtre, quitter depuis la barre de menus), puis relance-le. Ça suffit dans l'immense majorité des cas que j'ai croisés.

## Conclusion

Mos résout un problème précis et irritant : le défilement saccadé d'une souris classique sur macOS. Installation en une commande, configuration fine par axe et par app, remapping de boutons en bonus, le tout en open source et sans service en arrière-plan intrusif.

Si tu alternes entre MacBook et souris externe, ou si tu viens de Windows et que tu veux ton sens de défilement préféré sans compromis, teste Mos. Dix minutes de configuration, et tu ne reviens plus en arrière.

Pour aller plus loin dans la remise en ordre de ton environnement macOS, jette un œil à mon tour d'horizon des [10 outils macOS gratuits que j'utilise](/10-outils-low-tech-macos-guide-complet/), à [BetterDisplay](/betterdisplay-macos-hidpi-ddc/) pour tes écrans externes, et à [Default Folder X](/default-folder-x-macos-dialogues-intelligents/) pour tes boîtes de dialogue Ouvrir/Enregistrer.
