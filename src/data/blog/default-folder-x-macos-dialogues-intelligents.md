---
title: "Default Folder X macOS : les boîtes de dialogue Ouvrir/Enregistrer enfin intelligentes"
description: "Default Folder X macOS transforme les boîtes de dialogue Ouvrir et Enregistrer en outils puissants. Favoris, aperçu, historique : guide complet."
pubDatetime: "2026-09-09T11:02:11+02:00"
modDatetime: "2026-09-08T08:00:00.000Z"
author: Brandon
tags:
  - debutant
  - macos
  - productivite
  - guide
featured: false
draft: false
focusKeyword: default folder x macos
faqs:
  - question: "Default Folder X ralentit-il les boîtes de dialogue macOS ?"
    answer: "Non, l'overhead est imperceptible. Default Folder X s'injecte via une extension système légère et n'ajoute aucun délai visible à l'ouverture des dialogues Ouvrir et Enregistrer."
  - question: "Default Folder X fonctionne-t-il avec toutes les apps macOS ?"
    answer: "La plupart des apps natives et tierces sont supportées. Certaines apps Electron ou fortement sandboxées peuvent être partiellement incompatibles, mais les cas problématiques sont rares."
  - question: "Combien coûte Default Folder X et y a-t-il une version d'essai ?"
    answer: "Default Folder X est vendu 39,95 $ en licence simple, 34,95 $ à partir de deux licences. Une version d'essai gratuite de 30 jours est disponible sur le site officiel de St. Clair Software."
---
> 💡 **TL;DR**
> - Default Folder X ajoute des favoris par app, un historique de dossiers segmenté et un aperçu intégré dans chaque boîte de dialogue Ouvrir/Enregistrer
> - Tu accèdes d'un clic aux fenêtres Finder ouvertes, tu fais des recherches Spotlight depuis un dialogue sans quitter ton workflow
> - 39,95 $ en licence permanente, essai gratuit 30 jours sur stclairsoft.com

## Default Folder X macOS : pourquoi les dialogues natifs sont une punition

Chaque fois que tu enregistres un fichier dans une app macOS, t'as droit à la même boîte de dialogue minimaliste depuis des années. L'app décide d'un dossier de départ aléatoire, tu dois naviguer depuis là, sans aperçu, sans favoris spécifiques à l'app, sans raccourci vers le dossier que tu utilisais il y a 30 secondes dans une autre fenêtre.

Apple a ajouté une barre latérale aux dialogues, mais elle est rigide et identique pour toutes les apps. Si tu travailles dans Affinity Photo sur un projet graphique le matin et dans Final Cut l'après-midi, les deux apps t'affichent les mêmes favoris génériques qui ne correspondent à aucun de tes deux contextes de travail. La navigation devient une répétition d'aller-retours inutiles dans l'arborescence.

C'est précisément le trou qu'a bouché **Default Folder X macOS** de St. Clair Software, une app qui existe depuis la fin des années 90 et qui tient le coup parce qu'elle résout un vrai problème qu'Apple n'a jamais daigné corriger. Elle ne remplace pas les boîtes de dialogue natives : elle se greffe dessus et les rend intelligentes.

## Table des matières

## Ce que Default Folder X change concrètement

Default Folder X s'injecte dans les dialogues système via une extension et leur ajoute une couche de contenu dans la barre latérale. Dès que tu déclenches un Cmd+S ou un Ouvrir dans n'importe quelle app, tu vois apparaître :

- Tes **dossiers favoris** configurés dans Default Folder X, accessibles en un clic
- Les **dossiers récents pour cette app spécifiquement**, séparés des autres apps
- Les **fenêtres Finder actuellement ouvertes** sur ton bureau

Ce troisième point est le plus percutant. Tu as un projet ouvert dans une fenêtre Finder sur `~/Projets/Site/assets/`. Tu bascules dans Preview pour enregistrer une capture retouchée. Normalement, tu renavigues jusqu'au bon dossier depuis zéro. Avec Default Folder X macOS, cette fenêtre Finder apparaît directement dans la barre latérale du dialogue. Un clic, tu es dedans. La navigation prend moins d'une seconde.

L'app ajoute aussi un bouton dans la barre de titre du dialogue, qui ouvre un menu rapide vers tes favoris globaux et tes dossiers récents toutes apps confondues, pratique pour les cas où tu veux accéder à quelque chose hors de l'historique par app.

## Installation et première configuration de Default Folder X

Default Folder X n'est pas disponible sur l'App Store : les permissions système nécessaires dépassent les contraintes du sandbox d'Apple. Tu le télécharges directement sur stclairsoft.com. Une version d'essai de 30 jours est disponible sans carte bancaire requise.

```bash
# Via Homebrew si tu gères tes apps en ligne de commande
brew install --cask default-folder-x
```

Au premier lancement, macOS te demande de valider l'extension système dans `Réglages Système > Confidentialité et sécurité`. Sur les versions récentes de macOS, un redémarrage peut être nécessaire. C'est attendu : Default Folder X doit s'accrocher au niveau des dialogues système pour fonctionner.

### Configuration initiale recommandée

Ouvre les préférences via l'icône Default Folder X dans la menu bar et commence par les **Favoris**. Glisse depuis le Finder les dossiers que tu utilises vraiment : projets actifs, dossier Desktop, zones d'export. Ces favoris seront accessibles depuis n'importe quel dialogue sur n'importe quelle app.

Configure ensuite le **comportement par application**. Default Folder X peut rouvrir systématiquement dans le dernier dossier utilisé pour chaque app. Sketch se souvient du dossier de ton dernier asset. Terminal s'ouvre là où tu étais la dernière fois. Tu ne reconfigures plus à chaque session.

## Favoris et dossiers récents segmentés par application

La feature centrale de Default Folder X macOS, c'est la segmentation de l'historique de navigation par application. macOS mémorise les "dossiers récents" de façon globale, ce qui produit une liste mélangeant tous tes contextes de travail. Default Folder X garde une liste distincte pour chaque app.

Concrètement : tu travailles dans Acorn sur des assets graphiques et dans Logic Pro sur des samples audio. Chaque app a sa propre liste de dossiers récents. Quand tu enregistres depuis Acorn, tu vois tes dossiers graphiques. Depuis Logic Pro, tu vois tes dossiers audio. Le mélange disparaît, la navigation devient prédictible.

⚠️ Cette liste se construit progressivement sur quelques jours d'utilisation normale. Les premières 48 heures, elle sera maigre. Au bout d'une semaine, l'app connaît tes patterns de navigation et commence à faire vraiment gagner du temps.

## L'aperçu de fichiers intégré dans les dialogues

Default Folder X ajoute un aperçu de fichiers directement dans les boîtes de dialogue Ouvrir. Quand tu sélectionnes un fichier dans le dialogue, un aperçu miniature s'affiche à côté : images, PDFs, documents, et selon ta version macOS, vidéos et fichiers audio.

Pour un workflow graphique, c'est particulièrement utile. Tu dois retrouver le bon JPG parmi 50 exports dans un dossier ? Tu cliques sur chaque fichier et tu vois l'aperçu sans sortir du dialogue, sans ouvrir Preview, sans alt-tab. La sélection qui prenait 2 minutes prend 20 secondes.

L'aperçu se configure dans les préférences : taille, types de fichiers prévisualisés, et désactivation sélective. Si tu travailles sur un dossier avec des fichiers RAW de plusieurs gigaoctets, tu peux désactiver l'aperçu pour ces types pour éviter le moindre ralentissement lors de la navigation.

## Spotlight et tags directement dans les dialogues

Default Folder X intègre une recherche Spotlight dans les boîtes de dialogue. Cmd+F dans un dialogue ouvre une zone de recherche qui interroge le dossier courant et ses sous-dossiers. Tu trouves tes fichiers sans ouvrir une fenêtre Finder séparée.

Tu restes dans ton app, dans ton workflow. Tu cherches, tu trouves, tu ouvres ou tu enregistres. Pas de fenêtre supplémentaire à gérer, pas de split d'attention.

L'intégration des **tags Finder** fonctionne dans le même esprit. Si tu utilises les tags macOS pour catégoriser tes fichiers, tu filtres par tag depuis la barre latérale du dialogue. Les fichiers tagués "En cours" ou "À livrer" s'affichent instantanément, sans naviguer dans l'arborescence. C'est particulièrement puissant couplé avec un workflow de tags rigoureux dans Finder.

## Accès aux fenêtres Finder ouvertes

La barre latérale des dialogues inclut une section "Finder Windows" qui liste toutes tes fenêtres Finder actuellement ouvertes. Un clic sur une entrée navigue le dialogue directement vers ce dossier.

Pour un workflow multi-app, c'est l'intégration la plus percutante de Default Folder X. T'as un Finder pointant sur `~/Projets/Client/exports/`. Tu travailles dans Photoshop. Tu enregistres un fichier. Tu cliques sur la fenêtre Finder dans le dialogue. Tu es dans le bon dossier. Pas de navigation, pas de raccourci à mémoriser, juste un clic sur ce que tu vois déjà à l'écran.

Si tu utilises [Bunch macOS](/bunch-macos-lancer-contextes/) pour lancer des contextes de travail complets avec des apps et des fenêtres Finder préconfigurées, Default Folder X capte automatiquement les fenêtres ouvertes par Bunch. Ton switch de contexte inclut désormais aussi la navigation dans les dialogues : les dossiers du contexte sont immédiatement accessibles depuis chaque app du bundle.

## Règles par application et comportements avancés

Default Folder X permet de définir des règles précises pour chaque app. Dans les préférences, onglet Applications, tu configures :

- **Dernier dossier utilisé** : le dialogue rouvre là où tu t'es arrêté la dernière fois dans cette app
- **Dossier fixe** : certaines apps enregistrent toujours au même endroit, pas besoin de mémorisation dynamique
- **Désactivation complète** : pour les apps qui gèrent leurs propres dialogues ou dont tu ne veux pas modifier le comportement

Tu peux aussi créer des exceptions depuis le dialogue lui-même via Option+clic sur le menu Default Folder X, sans passer par les préférences.

Pour ceux qui utilisent [Hammerspoon macOS](/hammerspoon-macos-scripting-lua/) pour l'automatisation avancée des fenêtres et des raccourcis système, Default Folder X et Hammerspoon opèrent dans des couches différentes et se complètent sans s'interférer. Hammerspoon gère le placement des fenêtres et les actions clavier globales. Default Folder X gère les dialogues fichiers. Ensemble, ils couvrent deux axes d'automatisation que macOS laisse ouverts.

## Intégration dans le Finder

Default Folder X ajoute des fonctions optionnelles dans les fenêtres Finder elles-mêmes. Une barre d'outils dans le Finder te permet d'ajouter le dossier courant aux favoris Default Folder X en un clic, de copier le chemin complet dans le presse-papier, ou d'afficher les infos détaillées d'un fichier sélectionné sans passer par Cmd+I.

Cette intégration est optionnelle et activable dans les préférences. Elle complète le comportement dans les dialogues plutôt que de le dupliquer. Depuis le Finder, tu prépares ta liste de favoris. Dans les dialogues, tu en bénéficies.

Default Folder X s'inscrit dans la même philosophie que [Dato macOS](/dato-macos-calendrier-intelligent/) ou [BetterDisplay macOS hidpi](/betterdisplay-macos-hidpi-ddc/) : une app qui cible un angle précis de l'interface macOS laissé en friche par Apple et qui l'améliore sans alourdir le reste du système. Rien de superflu, tout au service d'une friction éliminée.

## Astuces de workflow quotidien

**Glisser-déposer vers les favoris dans un dialogue** : depuis un dialogue Ouvrir, tu peux glisser un fichier et le déposer sur un dossier favori dans la barre latérale pour le déplacer directement. Default Folder X gère l'opération de déplacement sans sortir du dialogue.

**Raccourcis clavier vers les favoris** : dans les préférences, chaque favori peut se voir assigner un raccourci clavier Cmd+Option+[chiffre]. Depuis n'importe quel dialogue, tu sautes instantanément vers le dossier voulu. Idéal si tu jonglles entre 3 ou 4 projets actifs en parallèle.

**Synchronisation des préférences** : Default Folder X stocke ses préférences dans un fichier standard. Pointe vers un dossier iCloud Drive ou une solution de sync de ton choix dans les préférences et retrouve ta configuration identique sur tous tes Macs.

**Option+double-clic sur un dossier dans un dialogue** : ouvre ce dossier dans une nouvelle fenêtre Finder sans fermer le dialogue. Pratique pour vérifier le contenu complet d'un dossier de destination avant d'y enregistrer un fichier, quand l'aperçu seul ne suffit pas.

**Réinitialiser l'historique par app** : si une app change de projet et que l'historique de dossiers devient obsolète, tu peux effacer l'historique pour une app spécifique depuis les préférences sans toucher aux autres. L'historique repart de zéro pour cette app uniquement.

## Conclusion

Default Folder X macOS résout un problème vieux comme macOS lui-même : des boîtes de dialogue Ouvrir et Enregistrer trop rigides pour un workflow sérieux. Favoris par application, dossiers récents segmentés, aperçu intégré, accès direct aux fenêtres Finder ouvertes, Spotlight dans les dialogues. Pas de révolution graphique, juste un trou comblé qu'Apple ne comblera probablement jamais parce que les dialogues système ne sont pas une priorité grand public.

À 39,95 $ en licence permanente avec des mises à jour gratuites sur la version majeure en cours, c'est un investissement justifié si tu passes ta journée à ouvrir et enregistrer des fichiers dans des dizaines d'apps différentes. L'essai de 30 jours est là pour te convaincre avant d'engager les sous. Après une semaine, revenir aux dialogues natifs sera difficile.
