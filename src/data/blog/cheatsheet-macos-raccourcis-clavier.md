---
title: "Cheatsheet macOS : CheatSheet est mort, KeyClu prend le relais"
description: "CheatSheet ne fonctionne plus depuis macOS Sonoma. Voici KeyClu, la cheatsheet macOS gratuite qui affiche les raccourcis de l'app active."
pubDatetime: "2026-09-11T11:02:12+02:00"
modDatetime: "2026-09-11T08:00:00.000Z"
author: Brandon
tags:
  - macos
  - productivite
  - guide
  - debutant
featured: false
draft: false
focusKeyword: cheatsheet macos
faqs:
  - question: "Pourquoi CheatSheet ne s'affiche plus sur mon Mac ?"
    answer: "Parce que l'app est abandonnée. Media Atelier l'annonce noir sur blanc sur sa page officielle : CheatSheet ne fonctionne plus à partir de macOS 14 Sonoma. Le fichier .dmg de la version 1.6.4 renvoie une erreur 404, et le cask Homebrew a été désactivé le 9 novembre 2025 pour cause d'abandon."
  - question: "Quelle alternative gratuite à CheatSheet en 2026 ?"
    answer: "KeyClu, développée par Sergii Tatarenkov, gratuite, en version 0.33 (août 2026). C'est l'une des deux alternatives que le développeur de CheatSheet recommande lui-même, avec KeyCue qui est payante. KeyClu s'installe avec brew install --cask keyclu."
  - question: "KeyClu affiche-t-elle vraiment tous les raccourcis d'une app ?"
    answer: "Non, et son développeur le dit ouvertement : elle peut en rater certains, et parfois en afficher qui ne sont pas réellement actifs. Elle lit la barre de menus, donc tout ce qui n'y figure pas lui échappe, en particulier les raccourcis internes des éditeurs comme VS Code, rangés dans leur propre panneau de préférences."
---
> 💡 **TL;DR**
> - CheatSheet, la cheatsheet macOS culte qui affichait les raccourcis en maintenant ⌘, est abandonnée : elle ne fonctionne plus depuis macOS 14 Sonoma
> - KeyClu la remplace, gratuite, maintenue (v0.33 en août 2026), avec recherche intégrée : `brew install --cask keyclu`
> - L'activation change : deux appuis sur ⌘ puis maintien, au lieu d'un simple maintien

## Cheatsheet macOS : pourquoi ton raccourci ne fait plus rien

Tu maintiens ⌘ dans le Finder, tu attends deux secondes, et il ne se passe rien. Avant, la liste complète des raccourcis de l'app s'affichait en overlay. Aujourd'hui, plus rien.

Ce n'est pas ton Mac, et ce n'est pas ta configuration. L'app qui faisait ça s'appelait CheatSheet, elle était géniale, gratuite, et elle est morte. La bonne nouvelle : son remplaçant est meilleur, toujours gratuit, et son propre développeur te pointe dessus.

## Table des matières

## Ce que faisait CheatSheet, et pourquoi tu la cherches encore

CheatSheet était une app de Media Atelier, sortie en 2012 et restée gratuite toute sa vie. Le principe tenait en une phrase : tu maintiens la touche ⌘ enfoncée pendant environ deux secondes, et un overlay liste tous les raccourcis clavier de l'application au premier plan, groupés par menu.

L'astuce technique était élégante. L'app ne maintenait aucune base de données de raccourcis, elle lisait simplement la barre de menus de l'app active. Un nouveau logiciel sortait, ses raccourcis apparaissaient automatiquement, sans aucune mise à jour côté CheatSheet. Bonus rarement connu : tu pouvais cliquer sur une entrée de la liste pour exécuter la commande, au lieu de taper la combinaison.

Ça explique pourquoi une app de 2012 traîne encore dans autant de listes d'outils macOS indispensables, et pourquoi tant de gens cherchent encore cette cheatsheet macOS en 2026.

Sauf que Media Atelier a arrêté les frais. Sur sa page officielle, l'éditeur écrit sobrement que **CheatSheet a été abandonnée parce qu'elle ne fonctionne plus avec macOS 14 Sonoma et les versions suivantes**. Je suis allé vérifier trois choses avant de l'écrire ici, parce qu'un éditeur qui range un produit laisse en général des traces ailleurs :

- L'URL officielle `mediaatelier.com/CheatSheet/` renvoie une redirection 301 vers GrandTotal, le logiciel de facturation de l'éditeur. Le produit a quitté le site.
- Le fichier `CheatSheet_1.6.4.dmg` répond en HTTP 404. Il n'y a plus rien à télécharger.
- Le cask Homebrew `cheatsheet` a été marqué déprécié le 9 novembre 2024, puis désactivé le 9 novembre 2025, avec le motif `discontinued`.

⚠️ Méfie-toi des sites de téléchargement tiers (Softonic, FileHippo, SourceForge et compagnie) qui proposent encore l'installeur. Tu récupères un binaire non signé par l'éditeur, abandonné, qui de toute façon ne fonctionnera pas sur ton macOS. Ce n'est pas le genre de risque qui vaut le coup pour une app de raccourcis clavier.

## KeyClu, la cheatsheet macOS qui a repris le flambeau

Media Atelier ne laisse pas ses utilisateurs dans le vide : la page d'abandon recommande deux remplaçants, KeyCue (payante) et KeyClu (gratuite). Commence par la gratuite, elle suffit dans la majorité des cas.

KeyClu est développée par Sergii Tatarenkov. Version 0.33 en août 2026, donc activement maintenue, compatible macOS 11 Big Sur et supérieur, en natif Apple Silicon comme Intel.

Le principe reste identique à CheatSheet : elle surveille quelle app a le focus et affiche ses raccourcis. Le geste d'activation, lui, change et c'est le point qui déroute tout le monde au premier essai.

**Appuie deux fois sur ⌘, et maintiens la touche au second appui.** Pas un simple maintien comme avant. Ce double appui évite de déclencher l'overlay par accident chaque fois que tu réfléchis trois secondes avec le doigt posé sur la touche Commande.

## Installer KeyClu en une commande

Le plus rapide passe par Homebrew. Si tu ne l'as pas encore configuré, mon [guide d'installation Homebrew sur macOS](/installation-homebrew-macos/) couvre la mise en route complète en quelques minutes.

```bash
brew install --cask keyclu
```

Sinon, l'archive est téléchargeable directement depuis les releases GitHub du projet, avec une installation classique par glisser-déposer dans le dossier Applications.

Au premier lancement, KeyClu réclame l'autorisation **Accessibilité** dans Réglages Système, section Confidentialité et sécurité. Ce n'est pas négociable : sans cette permission, l'app ne peut pas savoir quelle application est au premier plan, ni lire sa barre de menus. C'est exactement le même besoin que CheatSheet en son temps.

Elle demande aussi, de façon optionnelle, l'accès au Centre de notifications pour te signaler ses mises à jour. Tu peux refuser sans rien casser.

✅ Vérification en dix secondes : ouvre le Finder, appuie deux fois sur ⌘ en maintenant le second appui. Si la cheatsheet macOS du Finder s'affiche, tout est en place. Si rien ne bouge, retourne vérifier la case Accessibilité, c'est la cause dans la quasi-totalité des cas.

## Ce que KeyClu fait mieux que CheatSheet

Le remplacement n'est pas une régression, plutôt l'inverse. KeyClu apporte des choses que l'originale n'a jamais eues :

- **Une recherche intégrée.** Tu tapes un mot et l'app surligne le raccourci correspondant. Sur une app qui expose cinquante entrées de menu, ça change tout : c'était la limite la plus pénible de CheatSheet, qui te laissait balayer la liste à l'œil.
- **Le masquage des raccourcis.** Tu peux cacher ceux que tu connais déjà par cœur, ou ceux qui ne te servent jamais. La liste se réduit à ce qui te reste vraiment à apprendre.
- **Des marque-pages.** Tu épingles les raccourcis que tu veux mémoriser en priorité pour qu'ils te sautent aux yeux.
- **Un panneau persistant.** L'overlay peut rester affiché en permanence à côté de ton travail, au lieu de disparaître dès que tu relâches la touche. Pratique pendant les premiers jours sur une app inconnue.
- **Des sources au-delà des menus.** KeyClu sait aussi afficher des raccourcis déclarés ailleurs que dans la barre de menus, notamment tes hotkeys skhd, des gestes, ou des raccourcis enregistrés à la main.

Ce dernier point compte si tu construis ta propre couche de raccourcis. Quand tu automatises ton Mac avec [Hammerspoon et ses scripts Lua](/hammerspoon-macos-scripting-lua/), ou que tu déclenches des contextes entiers avec [Bunch](/bunch-macos-lancer-contextes/), tu finis vite avec des combinaisons personnelles que plus aucun menu ne documente. Les enregistrer manuellement dans KeyClu te donne enfin une référence unique, au lieu d'un fichier de configuration que tu relis en pleine session de travail.

## Les limites, dites par le développeur lui-même

Rare et appréciable : la page officielle de KeyClu liste ses propres angles morts sans les enrober.

**Elle peut rater des raccourcis.** Elle lit la barre de menus, donc tout ce qui n'y figure pas lui échappe. Ça touche surtout les éditeurs et les apps qui gèrent l'essentiel de leur clavier en interne : dans VS Code, la vraie liste vit dans un panneau de préférences maison, pas dans un menu, et KeyClu n'a aucun moyen d'aller la chercher.

**Elle peut en afficher en trop.** Une entrée de menu peut être listée alors qu'elle est grisée ou inopérante dans le contexte du moment.

**Les menus à base d'icônes lui posent problème.** Quand une commande n'a pas de libellé texte, il n'y a pas grand-chose à extraire.

Aucune de ces limites n'est propre à KeyClu, c'est la contrainte de fond de toute cheatsheet macOS qui lit la barre de menus plutôt que de maintenir sa propre base de données. CheatSheet avait exactement les mêmes.

## Et si tu veux la version payante

L'autre alternative recommandée par Media Atelier, c'est KeyCue, éditée par Ergonis, en version 11.2.1. Elle va plus loin que la simple consultation : création de raccourcis personnalisés, écrasement de raccourcis existants, accès direct à des fichiers, dossiers ou sites web depuis une combinaison de touches.

Elle est payante, avec un achat unique en formule Basic et deux formules annuelles au-dessus. Ergonis n'affiche pas ses tarifs sur la page produit, il faut passer par sa page de prix dédiée, donc je ne te donnerai pas un chiffre que je n'ai pas vérifié.

Mon avis : commence par KeyClu. Si après deux semaines la recherche et le panneau persistant te suffisent, tu as réglé le problème pour zéro euro. Le jour où tu veux vraiment fabriquer et gérer tes raccourcis, tu seras de toute façon mieux servi par [Raycast](/raycast-macos-outil-productivite-ultime/) côté lancement d'actions, ou par [rcmd pour basculer entre tes apps avec ⌘ plus une lettre](/rcmd-alternative-cmd-tab-macos/), deux outils qui couvrent des besoins que ni KeyCue ni KeyClu ne visent.

## Conclusion

CheatSheet a rendu de fiers services pendant plus de dix ans, et son abandon depuis Sonoma explique la moitié des « ça ne marche plus chez moi » qu'on lit encore sur les forums. Inutile d'aller chercher un vieil installeur sur un site de téléchargement douteux : il ne se lancera pas.

KeyClu reprend l'idée, ajoute la recherche qui manquait cruellement, et reste gratuite. Une commande Homebrew, une case Accessibilité à cocher, deux appuis sur ⌘, et tu retrouves ta cheatsheet macOS.

Teste-la maintenant sur l'app que tu utilises le plus. Il y a de bonnes chances que tu tombes sur au moins un raccourci que tu attendais depuis des mois sans savoir qu'il existait déjà.
