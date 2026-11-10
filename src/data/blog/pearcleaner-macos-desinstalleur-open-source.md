---
title: "Pearcleaner macOS : le désinstalleur open source qui chasse les fichiers orphelins"
description: "Pearcleaner macOS : désinstalleur gratuit et open source qui traque les fichiers orphelins après suppression d'une app, alternative à CleanMyMac."
pubDatetime: "2026-11-10T11:01:44+01:00"
modDatetime: "2026-11-09T08:00:00.000Z"
author: Brandon
tags:
  - macos
  - homebrew
  - stockage
  - debutant
featured: false
draft: false
focusKeyword: pearcleaner macos
faqs:
  - question: "Pearcleaner est-il payant ?"
    answer: "Non, c'est gratuit et open source sous licence Apache 2.0 avec Commons Clause : tu peux l'utiliser, le lire et le compiler toi-même, mais personne ne peut en revendre une version commerciale."
  - question: "Pearcleaner peut-il supprimer des fichiers dont une autre app a encore besoin ?"
    answer: "Il te montre la liste des fichiers associés avant toute suppression, donc tu valides chaque élément. Reste prudent avec les frameworks ou plugins partagés entre plusieurs apps si tu hésites."
  - question: "Pearcleaner est-il encore mis à jour en 2026 ?"
    answer: "Le développement est en pause depuis fin 2025, faute de Mac disponible chez l'auteur. Le projet n'est pas abandonné officiellement, mais aucun nouveau correctif n'est garanti pour l'instant."
---
> 💡 **TL;DR**
> - Pearcleaner macOS désinstalle une app et retrouve ses fichiers orphelins : préférences, caches, logs, supports
> - Gratuit, open source, licence fair-code, s'installe en une commande : `brew install --cask pearcleaner`
> - Développement en pause depuis fin 2025, mais l'app installée fonctionne toujours parfaitement sur macOS 13 à 26

## Pearcleaner macOS : en finir avec les fichiers qui restent après une désinstallation

Tu glisses une app vers la corbeille, tu la vides, et tu crois en avoir fini. Faux. Derrière, il reste des dizaines de fichiers : préférences dans `~/Library/Preferences`, caches dans `~/Library/Caches`, parfois un daemon planqué dans `/Library/LaunchAgents`. Au bout de quelques années d'usage d'un Mac, ça représente plusieurs gigaoctets de poussière numérique que personne ne nettoie jamais.

C'est exactement le problème que **Pearcleaner** règle. Une app macOS, gratuite, open source, qui scanne ton disque pour retrouver tout ce qu'une application a laissé derrière elle, et qui te propose de tout supprimer en un clic. Pas d'abonnement, pas de compte à créer, pas de télémétrie cachée.

## Table des matières

## Pourquoi glisser une app à la corbeille ne suffit jamais

Sur Windows, un désinstalleur fait partie du contrat : chaque logiciel embarque sa propre routine de suppression. Sur macOS, Apple a fait un choix différent : une app est censée être un simple bundle `.app`, et la glisser à la corbeille devrait suffire.

Dans la pratique, ça ne marche que pour les apps les plus sobres. Dès qu'un logiciel installe un agent de lancement, écrit des préférences, télécharge des assets ou pose un plugin système, ces fichiers survivent indéfiniment à la suppression du `.app`. Ils ne consomment pas forcément beaucoup d'espace individuellement, mais ils s'accumulent, encombrent les recherches Spotlight, et parfois entrent en conflit si tu réinstalles plus tard une version plus ancienne du même logiciel.

Pearcleaner macOS attaque ce problème avec une approche simple : avant de supprimer une app, il scanne les emplacements classiques où macOS range les fichiers associés (bundle identifier, nom de l'app, variantes de casse) et te montre tout en une seule liste. Tu coches, tu valides, tout part d'un coup.

## Installer Pearcleaner sur macOS

Le plus rapide passe par Homebrew. Si tu ne l'as pas encore configuré sur ton Mac, mon [guide d'installation Homebrew](/installation-homebrew-macos/) couvre la mise en route en quelques minutes.

```bash
brew install --cask pearcleaner
```

L'app est aussi disponible en téléchargement direct depuis les releases GitHub du projet (compte `alienator88`), si tu préfères éviter Homebrew. L'auteur, Alin Lupascu, est clair sur un point : **le seul site légitime pour télécharger Pearcleaner est `itsalin.com`**. Les autres plateformes de téléchargement qui le référencent ne sont pas affiliées au projet, et certaines proposent carrément des binaires modifiés. Pour une app qui demande un accès complet au disque, ce n'est pas un détail.

Au premier lancement, Pearcleaner macOS te demande deux autorisations dans Réglages Système, section Confidentialité et sécurité.

## Les permissions à accorder, et pourquoi elles comptent

⚠️ **Accès complet au disque (Full Disk Access).** Sans cette permission, Pearcleaner ne peut lire que les dossiers accessibles par défaut à une app sandboxée, ce qui exclut une bonne partie des caches système et des logs. Accorde-la, sinon la recherche de fichiers orphelins renvoie des résultats incomplets et tu gardes des restes sans le savoir.

**Un composant d'aide privilégié (helper).** Certaines actions, comme supprimer un daemon dans `/Library/LaunchDaemons` ou retirer un plugin système, nécessitent les droits root. Pearcleaner installe un petit helper signé pour ces cas précis, avec une demande de mot de passe au moment de l'action, exactement comme le ferait un installeur `.pkg` classique.

✅ Vérification rapide après l'installation : désinstalle une app que tu n'utilises plus (pas une app système, évidemment), regarde si Pearcleaner te propose une liste de fichiers associés avant la suppression. Si la liste est vide alors que tu sais que l'app a des préférences, retourne vérifier la case Full Disk Access.

## Ce que Pearcleaner sait faire au-delà du nettoyage de base

La désinstallation avec recherche de fichiers orphelins reste le cœur du projet, mais la liste de fonctions a beaucoup grossi au fil des versions (la dernière stable visible est la 5.4.3) :

- **Extension Finder** : un clic droit sur une app dans le Finder propose directement « Désinstaller avec Pearcleaner », sans ouvrir l'app principale.
- **Gestionnaire Homebrew intégré** : tu vois et gères tes formules et casks installés sans repasser par le terminal, pratique si tu préfères une interface pour ce genre de ménage.
- **App Lipo** : un outil pour retirer l'architecture Intel inutile des binaires universels sur un Mac Apple Silicon, histoire de regagner quelques centaines de mégaoctets par app.
- **Gestionnaires PKG, plugins et services** : une vue centralisée des installeurs `.pkg`, des plugins système et des services lancés au démarrage, trois catégories de fichiers invisibles autrement.
- **Sentinel Monitor** : une surveillance en arrière-plan qui déclenche automatiquement une recherche de fichiers orphelins dès que tu glisses une app à la corbeille, sans avoir à ouvrir Pearcleaner à chaque fois.
- **Support CLI et liens profonds** : pratique si tu veux déclencher une désinstallation depuis un script ou un raccourci Shortcuts.
- **Recherche de fichiers générale**, avec sensibilité réglable et inclusion ou exclusion de dossiers spécifiques. Si tu veux un outil encore plus rapide dédié uniquement à la recherche de fichiers au quotidien, j'utilise [Cling pour la recherche fuzzy](/cling-recherche-fuzzy-fichiers-macos/) en complément, les deux ne se recouvrent pas vraiment.

Pour un outil gratuit, c'est beaucoup plus que ce que propose la concurrence payante sur ce créneau précis.

## Pearcleaner face à AppCleaner et CleanMyMac

Trois outils se disputent le même usage, avec des philosophies différentes :

**AppCleaner** (FreeMacSoft) est le plus ancien et le plus minimaliste des trois. Gratuit, stable depuis des années, il fait une seule chose : glisser une app dans sa fenêtre, voir la liste de fichiers associés, supprimer. Pas d'extension Finder, pas de gestion Homebrew, pas de recherche de fichiers orphelins après coup si tu as déjà supprimé l'app ailleurs.

**CleanMyMac** (MacPaw) va dans l'autre sens : interface très soignée, nettoyage système complet, scan de malware, optimisation au démarrage. C'est aussi un logiciel payant par abonnement, avec une version d'essai limitée. Si tu cherches une alternative gratuite à CleanMyMac pour le seul besoin de désinstallation propre, c'est précisément le créneau que Pearcleaner occupe.

**Pearcleaner** se positionne entre les deux : plus complet qu'AppCleaner (recherche orpheline après coup, extension Finder, gestion Homebrew), sans jamais devenir payant ni pousser vers un abonnement. Le compromis, c'est une interface un peu moins polie que CleanMyMac et une courbe d'apprentissage légèrement plus raide la première fois que tu ouvres les gestionnaires PKG et plugins.

Si tu gères déjà ton Mac avec des outils gratuits et légers plutôt que des suites payantes, Pearcleaner rejoint naturellement la logique derrière [10 outils macOS gratuits que j'utilise](/10-outils-low-tech-macos-guide-complet/) : faire une chose précise, bien, sans abonnement caché.

## Licence fair-code et statut "en pause" : ce qu'il faut savoir avant d'installer

Deux points méritent d'être dits clairement avant que tu investisses du temps à configurer Pearcleaner.

**La licence n'est pas une licence open source classique.** Pearcleaner est distribué sous Apache 2.0 avec une clause additionnelle, la Commons Clause. Concrètement : tu peux utiliser le logiciel librement, lire le code, le modifier pour ton usage personnel, et même contribuer des correctifs au projet. Ce que tu ne peux pas faire, c'est vendre une version commerciale de Pearcleaner ou d'un dérivé. C'est ce que le projet appelle lui-même « fair-code », une licence pensée pour empêcher qu'une boîte récupère le travail gratuit d'un développeur solo et le revende sous un autre nom.

**Le développement est officiellement en pause depuis fin 2025.** L'auteur, Alin Lupascu, l'écrit sans détour sur le dépôt GitHub : il n'a plus de Mac disponible pour compiler, tester et publier de nouvelles versions. Les réponses aux issues, le travail sur les fonctionnalités et la revue des pull requests sont suspendus pour une durée indéterminée. Le projet n'est pas annoncé comme abandonné, juste gelé.

⚠️ Ce que ça change concrètement pour toi : la version 5.4.3 que tu installes aujourd'hui fonctionne et continuera de fonctionner, elle couvre macOS 13 Ventura jusqu'à 26 Tahoe. Mais si une future version de macOS casse une fonctionnalité précise (un changement de chemin système, une API Apple modifiée), ne compte pas sur un correctif rapide. C'est un peu la même situation que j'ai documentée pour [CheatSheet, mise en pause puis remplacée par KeyClu](/cheatsheet-macos-raccourcis-clavier/) : une app en pause n'est pas forcément morte, mais elle ne te protège plus des imprévus.

## Mes astuces d'usage et limites rencontrées

Après plusieurs mois d'usage sur mon Mac principal, quelques points qui méritent d'être su avant de foncer :

- **Lance un premier scan complet avant de désinstaller quoi que ce soit.** Pearcleaner peut lister les fichiers orphelins déjà présents sur ton disque, issus d'apps supprimées il y a des mois sans ce genre d'outil. La première passe révèle souvent plusieurs gigaoctets oubliés.
- **Vérifie toujours la liste avant de valider**, surtout pour les apps qui partagent des composants (plugins Adobe, frameworks de développement, runtimes partagés). Pearcleaner fait de son mieux pour isoler ce qui appartient vraiment à l'app ciblée, mais une correspondance de nom approximative reste possible.
- **Le Sentinel Monitor change vraiment l'usage au quotidien.** Une fois activé, tu n'as plus besoin de penser à ouvrir Pearcleaner : il réagit dès que tu vides la corbeille après avoir glissé une app dedans.
- **Les gestionnaires PKG et plugins demandent un peu de prudence.** Ce sont des zones plus techniques que le reste de l'interface, pensées pour des utilisateurs qui savent déjà ce qu'ils regardent. Si un nom ne te dit rien, laisse-le tranquille plutôt que de cliquer au hasard.

Côté comparaison d'écosystème, si tu cherches d'autres utilitaires macOS gratuits et légers dans le même esprit que Pearcleaner, j'ai aussi écrit sur [One Switch pour un panneau de contrôle rapide](/one-switch-macos-panneau-controle/) et sur [Velja pour choisir quel navigateur ouvre chaque lien](/velja-macos-choisir-navigateur/). Aucun des trois ne demande d'abonnement, et tous les trois remplacent une fonction que macOS gère mal ou pas du tout nativement.

## Conclusion

Pearcleaner macOS fait une chose que ni le Finder ni la corbeille ne font correctement : nettoyer vraiment derrière une app supprimée. Gratuit, open source sous licence fair-code, installable en une commande Homebrew, il couvre un vrai trou dans macOS sans jamais te pousser vers un abonnement comme le ferait CleanMyMac.

Le statut « en pause » du projet depuis fin 2025 n'est pas un drapeau rouge immédiat : la version actuelle fonctionne, couvre toutes les versions récentes de macOS, et la licence garantit que le code reste disponible même si l'auteur ne revient jamais. Installe-le, lance un premier scan complet de ton disque, et prépare-toi à être surpris par la quantité de fichiers orphelins qui traînent déjà chez toi.
