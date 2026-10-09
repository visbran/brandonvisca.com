---
title: "Stats macOS : moniteur système gratuit dans la barre des menus"
description: "Stats macOS surveille CPU, RAM, disque et réseau dans la barre des menus : gratuit, open source, et alternative crédible à iStat Menus payant."
pubDatetime: "2026-10-09T11:03:56+02:00"
modDatetime: "2026-10-09T08:00:00.000Z"
author: Brandon
tags:
  - macos
  - menu-bar
  - monitoring
  - homebrew
  - debutant
featured: false
draft: false
focusKeyword: stats macos
faqs:
  - question: "Stats macOS consomme combien de ressources en arrière-plan ?"
    answer: "Très peu en configuration par défaut. Les modules Sensors et Bluetooth sont les plus gourmands selon la doc officielle : désactive-les si tu veux économiser batterie et CPU."
  - question: "Stats fonctionne-t-il sur Apple Silicon et les dernières versions de macOS ?"
    answer: "Oui, l'app est native Apple Silicon et suit les versions récentes de macOS. Sur macOS 26, un nouveau réglage de confidentialité peut bloquer l'affichage des icônes si tu ne l'autorises pas explicitement."
  - question: "Que faire si les icônes de Stats n'apparaissent pas dans la barre des menus ?"
    answer: "Va dans Réglages Système puis Barre des menus et vérifie que Stats a l'autorisation d'y afficher ses modules. C'est une protection ajoutée par Apple, pas un bug de l'app."
---
> 💡 **TL;DR**
> - Stats macOS affiche CPU, RAM, disque, réseau et batterie directement dans ta barre des menus, en graphiques ou en texte
> - Gratuit, open source sous licence MIT, développé par exelban sur GitHub, sans compte ni abonnement
> - Installation en une commande : `brew install --cask stats`, alternative sérieuse à iStat Menus qui lui est payant

## Stats macOS : le moniteur système qui vit dans ta barre des menus

Tu veux savoir ce que fait ton Mac sans ouvrir le Moniteur d'activité à chaque fois ? Stats macOS répond à exactement ce besoin. C'est une petite app qui se love dans ta barre des menus et qui affiche en permanence l'état de ton CPU, ta RAM, ton disque, ton réseau, et pas mal d'autres capteurs.

Chez moi, c'est devenu un réflexe. Un coup d'œil en haut de l'écran et je sais si un process part en vrille, si mon disque se remplit, ou si mon Mac bosse plus fort que d'habitude pendant un export vidéo. Pas besoin d'alt-tab vers une app dédiée.

Stats est développé par exelban, hébergé sur GitHub, sous licence MIT. Ça veut dire code source ouvert, lisible par n'importe qui, et zéro télémétrie cachée à surveiller. Bon, on va pas se mentir : pour un outil qui surveille ton système, c'est un argument qui compte.

## Table des matières

## Installation : une commande Homebrew et c'est réglé

Le plus simple, c'est Homebrew. Si tu n'as pas encore installé Homebrew sur ton Mac, c'est l'affaire de deux minutes avec le script officiel. Une fois en place :

```bash
brew install --cask stats
```

Lance l'app depuis Launchpad ou ton dossier Applications. macOS va probablement te demander une confirmation Gatekeeper au premier lancement, puisque l'app vient d'un développeur hors App Store. C'est normal, c'est le prix de la liberté sur un binaire open source non distribué par Apple.

Tu préfères sans Homebrew ? La page GitHub du projet propose un `Stats.dmg` à télécharger directement dans les releases. Tu le montes, tu glisses l'app dans Applications, terminé.

Au premier démarrage, Stats te propose d'activer ou non chaque module. Tu peux tout cocher d'un coup et trier plus tard, c'est ce que je fais systématiquement.

## Les modules disponibles : CPU, RAM, disque, réseau et plus

Stats macOS fonctionne par modules indépendants, chacun avec son icône dans la barre des menus. Tu actives ceux qui t'intéressent, tu désactives le reste :

**CPU** affiche la charge processeur en temps réel, avec graphique mini intégré à l'icône. **Mémoire** fait pareil pour la RAM, avec détail de la pression mémoire si macOS commence à swapper. **Disque** suit l'espace utilisé et la vitesse de lecture/écriture. **Réseau** montre upload et download en direct, pratique pour repérer un process qui sature ta connexion sans prévenir.

Côté capteurs, Stats va plus loin que le Moniteur d'activité natif : température des composants, tension, consommation électrique instantanée sur les Mac qui exposent ces données. Le module **Batterie** suit l'usure et le cycle de charge, utile pour anticiper un remplacement.

Il y a aussi un module **Bluetooth** qui liste les appareils connectés avec leur niveau de batterie, et un module horloge multi-fuseaux si tu bosses avec des équipes ailleurs dans le monde. Le contrôle de ventilateurs existe dans le code mais la doc officielle le signale clairement comme non maintenu : ne compte pas dessus pour piloter la vitesse de tes fans.

## Configuration : graphiques, icônes et placement

Chaque module se configure indépendamment. Clic droit sur une icône, tu choisis entre affichage graphique (mini courbe qui défile), icône simple, ou valeur chiffrée brute. J'utilise le graphique pour CPU et réseau, et la valeur chiffrée pour la RAM : question de goût, teste les deux.

Tu peux aussi combiner plusieurs métriques dans un seul widget pour économiser de la place, ce qui compte vite si ton écran est déjà chargé d'icônes tierces. D'ailleurs, si ta barre des menus commence à ressembler à un capharnaüm, [One Switch macOS](/one-switch-macos-panneau-controle/) te permet de regrouper les bascules système courantes dans un seul panneau au lieu d'empiler les icônes une par une, un bon complément à Stats plutôt qu'un concurrent.

Pour réordonner les icônes entre elles, maintiens Cmd et fais glisser. macOS gère lui-même cet ordre, pas l'app : ne cherche pas une option dans les préférences de Stats, elle n'existe pas parce que ce n'est pas de son ressort.

Sur macOS 26, Apple a ajouté un réglage de confidentialité dédié à la barre des menus. Si une icône Stats disparaît après une mise à jour système, va dans Réglages Système, section Barre des menus, et vérifie l'autorisation de l'app. C'est un comportement Apple, pas un bug de Stats.

## Stats vs iStat Menus : lequel choisir

iStat Menus est la référence historique du genre : moniteur système payant, interface très soignée, support officiel, et une réputation bien établie chez les utilisateurs macOS depuis des années. Stats couvre une bonne partie des mêmes besoins, gratuitement, en open source.

La vraie question c'est ton usage. Si tu veux un outil qui fait le job sans sortir la carte bleue, que tu es à l'aise avec un projet communautaire maintenu sur GitHub, et que tu n'as pas besoin de support officiel réactif, Stats coche toutes les cases. Si tu veux un produit commercial poli dans les moindres détails, avec des widgets plus riches et un historique de développement continu financé par les ventes, iStat Menus reste une option sérieuse.

Perso, j'ai basculé sur Stats il y a un moment et je n'ai pas regretté. Les modules essentiels, CPU, RAM, réseau, disque, batterie, sont tous là, stables, et je n'ai jamais eu besoin d'ouvrir mon porte-monnaie pour surveiller mon propre Mac.

## Dépannage : icônes manquantes et consommation

Deux soucis reviennent le plus souvent avec Stats macOS. Le premier, des icônes qui n'apparaissent pas : vérifie d'abord le réglage de confidentialité de la barre des menus mentionné plus haut, puis relance l'app depuis Applications si ça persiste.

Le second, une sensation de ralentissement. La doc officielle du projet est honnête là-dessus : les modules Sensors et Bluetooth sont les plus gourmands en énergie. Si tu es sur batterie et que chaque pourcent compte, désactive-les et garde juste CPU, RAM, réseau et disque. Tu perds le détail des capteurs thermiques, tu gagnes en autonomie.

Si une icône reste bloquée ou affiche des valeurs incohérentes après une mise à jour macOS, un redémarrage complet de l'app (quitter puis relancer, pas juste fermer la fenêtre) règle la grande majorité des cas. C'est un comportement classique des apps de barre des menus qui gardent un état en mémoire.

## Stats dans ton setup macOS : les compléments qui vont bien avec

Stats macOS ne vit pas seul dans ta barre des menus, et c'est tant mieux. Si tu bosses avec plusieurs navigateurs selon le contexte, perso ou pro, [Velja macOS](/velja-macos-choisir-navigateur/) te laisse choisir lequel ouvrir pour chaque lien, directement depuis la barre des menus elle aussi.

Pour le MacBook avec notch, [Boring Notch](/boring-notch-macbook-dynamic-island/) transforme cet espace soi-disant perdu en zone utile façon Dynamic Island, une autre manière de récupérer de la place visuelle plutôt que d'empiler des icônes.

Et si tu veux élargir ta collection d'outils macOS gratuits au-delà du monitoring système, j'ai fait un tour complet dans [10 outils macOS gratuits que j'utilise](/10-outils-low-tech-macos-guide-complet/), avec d'autres apps légères et sans abonnement dans le même esprit que Stats.

## Conclusion

Stats macOS fait une seule chose et la fait bien : te montrer ce qui se passe sous le capot de ton Mac, sans friction, sans facture mensuelle, sans télémétrie cachée. Pour un admin sys ou un dev qui veut garder un œil sur ses ressources pendant qu'il bosse, c'est exactement le genre d'outil qu'on installe une fois et qu'on oublie, jusqu'au jour où il te sauve en repérant un process qui dérape.

Une commande Homebrew, cinq minutes de configuration des modules qui t'intéressent, et ta barre des menus devient un vrai tableau de bord système. Spoiler : ça va marcher du premier coup.
