---
title: "Itsycal macOS : mini calendrier gratuit dans ta menu bar"
description: "Itsycal macOS : mini calendrier gratuit pour la menu bar. Découvre comment installer, configurer et remplacer l'horloge native en 2 minutes."
pubDatetime: "2026-08-24T06:00:00.000Z"
modDatetime: "2026-08-24T06:00:00.000Z"
author: Brandon
tags:
  - macos
  - productivite
  - debutant
  - calendrier
  - menu-bar
featured: false
draft: false
focusKeyword: itsycal macos
faqs:
  - question: "Itsycal est-il gratuit ?"
    answer: "Oui, Itsycal est totalement gratuit et open-source. Tu peux le télécharger directement depuis le site officiel ou l'installer via Homebrew sans payer un centime."
  - question: "Itsycal remplace-t-il l'horloge macOS ?"
    answer: "Pas exactement. Itsycal s'affiche à côté de l'horloge native dans la menu bar. Cependant, tu peux masquer l'horloge système dans les paramètres de date et heure si tu préfères que seul Itsycal affiche l'heure."
  - question: "Itsycal fonctionne-t-il avec le Calendrier Apple ?"
    answer: "Oui, Itsycal se synchronise automatiquement avec les calendriers configurés sur ton Mac (iCloud, Google, Exchange, etc.). Tu vois tes événements directement dans le popup sans configuration supplémentaire."
  - question: "Comment changer le format de la date affichée dans la menu bar ?"
    answer: "Dans les préférences d'Itsycal, utilise le champ 'Format de la date' avec des tokens comme E pour le jour, M pour le mois, et d pour la date. Par exemple, EEEE d MMMM affiche 'Lundi 24 août'."
ogImage: "" 
---
> 💡 **TL;DR**
>
> - Itsycal est un mini calendrier open-source et gratuit qui vit dans ta menu bar macOS, juste à côté de l'horloge
> - Il affiche un popup rapide avec le calendrier du mois, tes événements, et la date personnalisée, sans quitter ton bureau
> - Installation en deux clics via Homebrew ou le site officiel, configuration en moins d'une minute
> - Parfait complément aux outils de productivité macOS comme [Swish](/swish-macos-gestion-fenetres-gestures/) pour optimiser ton workflow au quotidien

## Table des matières

## Pourquoi l'horloge native de macOS est frustrante

Si tu passes tes journées sur macOS, tu connais ce petit moment d'irritation. Tu veux jeter un coup d'œil rapide à la date du mois prochain, vérifier si tu as un rendez-vous demain matin, ou simplement savoir quel jour on est sans ouvrir l'app Calendrier. Et là, tu cliques sur l'horloge en haut à droite de l'écran... et tu obtiens un widget absolument inutile qui ne montre qu'une horloge analogique miniature et une liste de fuseaux horaires.

Sérieusement, Apple ? En 2026, la menu bar macOS est encore incapable d'afficher un simple calendrier mensuel en un clic. C'est d'autant plus rageant que presque tous les OS concurrents proposent cette fonctionnalité depuis des années. Même Windows 11, avec son calendrier popup intégré, fait mieux sur ce point précis.

La conséquence, c'est que tu te retrouves à ouvrir l'app Calendrier plusieurs fois par jour, à jongler entre les espaces de Mission Control, ou à consulter ton iPhone pour une info qui devrait être accessible en un clic depuis ton Mac. C'est du temps perdu, des changements de contexte inutiles, et une friction quotidienne qui s'accumule.

Heureusement, la communauté macOS est riche en petites utilitaires qui corrigent les défauts de Cupertino. Et dans la catégorie "calendrier menu bar gratuit", il y a un outil qui domine largement le marché depuis des années : Itsycal macOS.

Dans ce guide, je te montre comment installer Itsycal macOS, le configurer, le personnaliser, et surtout pourquoi il est devenu un indispensable de ma menu bar depuis des années.

## Itsycal macOS : ce que c'est exactement

Itsycal macOS est une micro-application gratuite développée par Mike S. Elle fait une chose et une seule : afficher un calendrier mensuel compact et tes événements du jour directement dans la menu bar. Quand tu cliques sur son icône, un popup s'ouvre avec une vue en grille du mois en cours, les dates surlignées, et la liste de tes rendez-vous en dessous. Un second clic, et tout disparaît. C'est propre, rapide, et instantanément compréhensible.

Contrairement à beaucoup d'apps de productivité qui tentent de tout faire et finissent par alourdir ton système, Itsycal adopte une philosophie minimaliste. Pas de tableau de bord complexe, pas de notifications intrusives, pas de compte à créer. Juste un calendrier qui est là quand tu en as besoin, et invisible le reste du temps.

L'app **Itsycal macOS** est open-source, distribuée sous licence MIT, et totalement gratuite. Elle est régulièrement mise à jour pour suivre les évolutions de macOS. À l'heure où j'écris ces lignes, elle fonctionne parfaitement sur macOS Sequoia et est compatible avec les puces Apple Silicon (M1/M2/M3/M4) ainsi qu'avec les vieux Mac Intel.

Pour les geeks du chiffre, sache que le projet est écrit en Objective-C et utilise les frameworks natifs d'Apple (Cocoa, EventKit). Résultat : une empreinte mémoire ridicule, un démarrage instantané, et une intégration parfaite avec le système. C'est le genre d'outil que tu installes une fois et que tu oublies, dans le bon sens du terme : il devient tellement naturel que tu ne t'imagines plus travailler sans.

## Installation : Homebrew ou téléchargement direct

Il y a deux façons d'installer **Itsycal macOS** sur ton Mac, et les deux sont aussi simples l'une que l'autre.

### Via Homebrew (recommandé)

Si tu utilises déjà Homebrew, c'est le plus rapide. Ouvre ton Terminal et tape :

```bash
brew install --cask itsycal
```

Homebrew télécharge la dernière version stable, l'installe dans ton dossier Applications, et crée un lien dans la menu bar. Tu n'as rien d'autre à faire.

### Via le site officiel

Si tu n'utilises pas Homebrew ou que tu préfères contrôler manuellement ce que tu installes, rends-toi sur le site officiel d'Itsycal. Télécharge le fichier `.zip`, décompresse-le, glisse l'app dans ton dossier Applications, et double-clique dessus.

Lors du premier lancement, macOS va probablement te demander de confirmer que tu fais confiance à l'application. C'est normal pour une app non signée par l'App Store. Va dans `Paramètres système > Confidentialité et sécurité`, et autorise Itsycal à s'ouvrir.

### Premier démarrage

Au premier lancement, Itsycal s'affiche automatiquement dans la menu bar sous la forme d'une icône ou d'une date. Si tu ne la vois pas immédiatement, vérifie que tu n'as pas trop d'icônes dans la menu bar. Sur un MacBook avec notch, l'espace est limité et macOS masque automatiquement les icônes qui débordent. Dans ce cas, ferme temporairement quelques apps en arrière-plan pour libérer de la place, ou réorganise tes icônes en maintenant la touche `Cmd` enfoncée pendant que tu les fais glisser.

## L'interface : un calendrier dans la menu bar

Clique sur l'icône d'Itsycal dans la menu bar. Ce qui apparaît est un modèle de simplicité : en haut, le mois et l'année avec deux petites flèches pour naviguer vers le mois précédent ou suivant. En dessous, une grille de sept colonnes avec les jours de la semaine. La date du jour est surlignée en rouge. En bas, la liste de tes événements du jour sélectionné, avec l'heure de début et l'heure de fin.

C'est tout. Pas de boutons inutiles, pas de publicités, pas de suggestions d'apps tierces. Juste ton calendrier.

Tu navigues dans le mois avec les flèches ou avec les raccourcis clavier (`Cmd + flèches gauche/droite`). Pour changer d'année, maintiens `Option` enfoncé tout en utilisant les flèches. Pour revenir immédiatement à aujourd'hui, appuie sur `Cmd + T`.

Le popup se ferme automatiquement dès que tu cliques ailleurs sur l'écran, ce qui respecte le flux naturel de travail. Tu veux une info, tu cliques, tu la vois, tu cliques ailleurs, tu reprends ta tâche. Aucune friction.

La liste des événements en bas du popup est synchronisée en temps réel avec le Calendrier Apple. Si tu ajoutes, modifies ou supprimes un événement dans l'app Calendrier, le changement se reflète immédiatement dans Itsycal. Pas besoin de redémarrer quoi que ce soit.

## Personnaliser l'affichage de la date

L'un des gros atouts d'Itsycal, c'est la personnalisation du texte affiché dans la menu bar. Par défaut, l'app montre juste une icône ou la date du jour. Mais tu peux aller beaucoup plus loin.

Ouvre les préférences d'Itsycal (`Cmd + ,` quand le popup est ouvert). Dans le champ "Format de la date", tu peux utiliser des tokens de formatage qui suivent la syntaxe Unicode Date Format. Quelques exemples pratiques :

- `EEEE d MMMM` affiche : "Lundi 24 août"
- `d MMM` affiche : "24 août"
- `EEE d` affiche : "Lun 24"
- `HH:mm` affiche l'heure au format 24h
- `h:mm a` affiche l'heure au format 12h avec AM/PM

Tu peux même combiner date et heure : `EEE d MMM • HH:mm` donne "Lun 24 août • 14:30". C'est particulièrement utile si tu veux remplacer complètement l'horloge native de macOS par Itsycal. Dans ce cas, va dans `Paramètres système > Centre de contrôle > Heure et date`, décoche "Afficher l'heure dans la barre des menus", et laisse Itsycal prendre le relais.

Il y a aussi une option pour choisir quel jour commence la semaine (lundi ou dimanche), afficher ou masquer les numéros de semaine, et ajuster la taille de la police du calendrier. Ces petits réglages permettent d'adapter l'app exactement à ta façon de lire le temps.

## Synchronisation avec tes calendriers

Itsycal ne stocke aucune donnée de calendrier par lui-même. Il lit directement les calendriers configurés dans l'app Calendrier de macOS via l'API EventKit. Cela signifie que si tu utilises iCloud, Google Calendar, Microsoft Exchange, Outlook, Fastmail, ou n'importe quel autre service configuré dans l'app Calendrier native, Itsycal les verra tous automatiquement.

Dans les préférences, tu peux choisir quels calendriers afficher dans le popup. Pratique si tu as un calendrier pro et un calendrier perso, et que tu ne veux voir que l'un des deux dans la menu bar. Tu peux aussi activer ou désactiver l'affichage des événements passés, ce qui évite d'encombrer la vue si tu as un historique chargé.

Cette intégration native avec EventKit garantit aussi que tes données restent sur ta machine. Itsycal ne communique avec aucun serveur externe, ne collecte aucune statistique, et ne te demande jamais de créer un compte. C'est un point de sécurité et de confidentialité important, surtout à une époque où même une simple app de météo revend tes données de localisation.

## Les raccourcis clavier

Itsycal supporte quelques raccourcis clavier bien pensés qui te permettent de naviguer sans sortir les mains du clavier :

- `Cmd + T` : retourner à aujourd'hui
- `Cmd + flèche gauche/droite` : mois précédent / suivant
- `Option + flèche gauche/droite` : année précédente / suivante
- `Espace` : ouvrir/fermer le popup (si Itsycal est l'app active)

Ces raccourcis sont modestes, mais ils s'intègrent parfaitement dans un workflow déjà optimisé. Si tu es du genre à utiliser [Amethyst](/amethyst-macos-tiling-window-manager/) ou [Yabai](/yabai-macos-tiling-avance/) pour gérer tes fenêtres avec le clavier, tu apprécieras cette cohérence. C'est tout l'esprit de macOS : des outils légers qui communiquent bien entre eux et qui respectent la même logique d'interaction.

Et si tu veux aller encore plus loin dans l'automatisation de ta menu bar, jette un œil à [Boring.Notch](/boring-notch-macbook-dynamic-island/). Cet outil transforme la notch de ton MacBook en un hub d'informations utiles. Couplé avec Itsycal pour la gestion du temps, tu obtiens une menu bar véritablement fonctionnelle et informée.

## Itsycal comparé aux alternatives

Le marché des calendriers menu bar sur macOS n'est pas énorme, mais il existe quelques alternatives qui méritent d'être mentionnées.

**Dato** est probablement l'alternative la plus proche. C'est un calendrier menu bar payant (environ 5 dollars) avec une interface plus moderne, des rappels intégrés, et des options de personnalisation avancées. Si tu veux absolument un look plus "Apple Design 2026", Dato est solide. Mais Itsycal fait 90 % du travail gratuitement, et la différence de prix n'est pas justifiée pour un usage standard.

**Calendar 366** est une autre option payante, plus orientée vers la gestion complète des événements avec édition inline. C'est un bon outil, mais c'est overkill si tu cherches juste un calendrier en lecture rapide.

**MeetingBar** est une alternative intéressante si tu passes ta journée en visioconférence. Il affiche ton prochain meeting directement dans la menu bar avec un bouton pour rejoindre Zoom/Teams/Meet en un clic. Ce n'est pas exactement la même cible qu'Itsycal, mais ça peut compléter l'expérience.

Pour la grande majorité des utilisateurs, Itsycal reste le choix par défaut. Il est gratuit, open-source, léger, fiable depuis des années, et il fait exactement ce qu'on lui demande sans artifice. Dans un monde où les apps deviennent de plus en plus lourdes et dépendantes de l'abonnement SaaS, Itsycal est une bouffée d'air frais.

## Quelques astuces avancées

Même si Itsycal se veut simple, il cache quelques réglages sympathiques pour les utilisateurs exigeants.

Si tu masques l'horloge système et que tu utilises Itsycal pour afficher l'heure, pense à activer l'option "Clignotement des deux-points" dans les préférences. Ça reproduit fidèlement le comportement de l'horloge native macOS et ça te permet de voir d'un coup d'œil si l'app est bien en cours d'exécution.

Tu peux aussi décider que Itsycal démarre automatiquement à l'ouverture de session. Dans les préférences système de macOS, ajoute Itsycal à la liste des éléments de connexion. Comme ça, dès que tu allumes ton Mac, ta menu bar est prête.

Pour les utilisateurs de plusieurs moniteurs, sache qu'Itsycal s'affiche par défaut sur la menu bar de l'écran principal. Si tu travailles souvent sur un écran externe, il peut être judicieux de régler cet écran comme écran principal dans `Paramètres système > Affichages > Organiser` pour garder Itsycal dans ton champ de vision.

Enfin, si tu utilises des apps qui masquent aussi la menu bar (comme certains modes plein écran), Itsycal disparaîtra avec le reste des icônes. C'est le comportement normal de macOS, pas un bug de l'app.

## Conclusion

Itsycal est l'exemple parfait d'un utilitaire macOS bien pensé. Il identifie un problème simple mais quotidien, l'absence de calendrier dans la menu bar, et le résout avec une élégance rare. L'installation se compte en secondes, la configuration est intuitive, et l'impact sur la productivité est immédiat. Tu arrêtes d'ouvrir l'app Calendrier pour un simple coup d'œil, tu réduis les changements de contexte, et tu gardes une vue claire sur ton temps sans quitter ton bureau.

Si tu cherches un moyen rapide et gratuit d'améliorer ton workflow macOS, Itsycal devrait être la prochaine chose que tu installes. C'est le genre d'outil que tu recommandes à tous tes collègues développeurs, et que tu regrettes de ne pas avoir découvert plus tôt. macOS reste un système incroyablement puissant, mais ce sont souvent ces petites apps communautaires qui le rendent vraiment complet.
