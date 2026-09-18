---
title: "SideNotes macOS : notes rapides qui glissent depuis le bord de l'écran"
description: "SideNotes macOS range tes notes sur le bord de l'écran, accessibles en un clic sans quitter ton app active. Installation, prix et astuces."
pubDatetime: "2026-09-16T11:01:12+02:00"
modDatetime: "2026-09-15T08:00:00.000Z"
author: Brandon
tags:
  - macos
  - productivite
  - homebrew
  - guide
  - intermediaire
featured: false
draft: false
focusKeyword: sidenotes macos
faqs:
  - question: "SideNotes macOS est-il gratuit ?"
    answer: "Non. C'est un achat unique à 19,99 dollars sur le Mac App Store ou en direct, ou un accès via l'abonnement Setapp si tu es déjà client."
  - question: "SideNotes macOS synchronise-t-il entre plusieurs Mac ?"
    answer: "Oui, via iCloud. Tes notes, dossiers et codes couleur se retrouvent identiques sur tous tes appareils connectés au même compte Apple."
  - question: "Existe-t-il une alternative gratuite à SideNotes macOS ?"
    answer: "Oui, Memos en auto-hébergement Docker fait le même métier de bloc-notes rapide, sans licence à payer mais avec un serveur à maintenir toi-même."
---
> 💡 **TL;DR**
> - SideNotes macOS range tes notes, tâches et snippets sur le bord de l'écran, accessibles en un clic sans jamais quitter l'app où tu travailles
> - Formatage Markdown, dossiers, codes couleur, épinglage, sync iCloud, intégration Shortcuts et AppleScript
> - Achat unique à 19,99 dollars (App Store, direct ou Setapp), `brew install --cask sidenotes` pour l'installer en une ligne

## SideNotes macOS résout un problème précis : où tu mets tes pense-bêtes

Tu bosses, tu as une idée, un lien à garder, une tâche qu'il ne faut pas oublier. Tu ouvres Notes, tu switches d'app, tu perds le fil de ce que tu faisais avant. Cinq minutes plus tard t'as complètement zappé pourquoi tu avais ouvert Notes.

**SideNotes macOS** part de ce constat. C'est un éditeur made by Apptorium qui vit sur le bord de ton écran, en dehors du flux normal des fenêtres. Tu glisses depuis le bord, tu notes, tu relâches, ta note reste planquée le temps qu'elle serve. Zéro changement de contexte, zéro fenêtre en plus dans ton Mission Control.

## Table des matières

## Installation de SideNotes macOS

Trois chemins possibles, choisis selon ta situation :

```bash
brew install --cask sidenotes
```

Sinon, le Mac App Store ou le site officiel [apptorium.com/sidenotes](https://www.apptorium.com/sidenotes) proposent le `.dmg` direct. Si t'es déjà abonné à Setapp, l'app y est incluse sans coût additionnel.

Prérequis : macOS 13 ou plus récent, compatible Apple Silicon et Intel. Si Homebrew n'est pas encore sur ta machine, j'ai un guide complet sur [comment installer Homebrew sur macOS](/installation-homebrew-macos/) qui te prend deux minutes.

Au premier lancement, SideNotes macOS te demande de choisir un bord d'écran par défaut (haut, bas, gauche, droite) et te propose d'activer le lancement automatique à la connexion. Accepte, sinon tu vas oublier que l'app existe au bout de trois jours.

## Comment ça marche au quotidien

Le geste de base : tu positionnes ton curseur sur le bord choisi, tu tires légèrement vers l'intérieur, un panneau glisse et affiche tes notes. Tu relâches, il redisparaît. Aucun raccourci obligatoire, même si tu peux en assigner un dans les préférences si tu préfères le clavier à la souris.

Chaque note supporte le Markdown avec un markup qui reste invisible tant que tu n'es pas en train d'éditer la ligne. Tu tapes `**important**`, ça s'affiche en gras, la syntaxe disparaît dès que tu cliques ailleurs. Propre, lisible, sans les astérisques qui traînent partout comme dans un simple fichier texte.

Tu peux plier une note pour ne garder que son titre visible, l'épingler en haut de la liste si elle sert tous les jours, ou la coder par couleur pour repérer d'un coup d'œil le projet auquel elle appartient. Rien d'exotique, mais l'ensemble tient dans un panneau qui ne prend jamais toute la place à l'écran.

## Organisation : dossiers, couleurs, recherche

Passé la dizaine de notes, tu vas vouloir ranger. SideNotes macOS propose des dossiers classiques, imbricables, avec leur propre code couleur. Chez moi, un dossier par client freelance, un dossier « homelab », un dossier « à trier » qui se vide chaque vendredi.

La recherche intégrée filtre en temps réel sur le contenu des notes, pas seulement les titres. Pratique quand tu te souviens d'un bout de commande collé trois semaines plus tôt mais plus du titre que tu lui avais donné.

⚠️ Un point de vigilance : sans organisation régulière, le panneau latéral devient vite un dépotoir. L'app ne force aucune structure, c'est à toi de discipliner tes dossiers.

✅ Astuce qui me sert tous les jours : crée un dossier « scratch » sans code couleur, dédié aux notes jetables de moins d'une heure. Tu vides ce dossier chaque soir, les vraies notes qui méritent de rester finissent dans des dossiers thématiques bien rangés. Ça évite que le tri devienne une corvée hebdomadaire ingérable.

## Automatisation : Shortcuts, AppleScript, API URL

Ce qui distingue SideNotes macOS d'un simple bloc-notes, c'est sa surface d'intégration. Trois portes d'entrée :

- **Apple Shortcuts** : crée une note depuis un raccourci déclenché par un clic, une automatisation Focus, ou une action partagée depuis Safari
- **AppleScript** : pilote la création et la lecture de notes depuis un script existant, utile si t'as déjà une automatisation maison qui journalise des événements
- **API basée sur URL** : ouvre une note précise ou en crée une nouvelle depuis un lien cliquable, pratique dans un second outil qui doit renvoyer vers SideNotes macOS

Exemple concret chez moi : un Shortcut qui capture l'URL de l'onglet Safari actif et la colle dans une note « à lire plus tard », déclenché par un raccourci clavier global. Zéro copier-coller manuel.

Si t'aimes automatiser ton Mac au-delà de la prise de notes, jette un œil à [Bunch macOS pour lancer des contextes complets en un clic](/bunch-macos-lancer-contextes/) ou à [Hammerspoon pour du scripting Lua qui couvre à peu près tout](/hammerspoon-macos-scripting-lua/).

## SideNotes macOS face aux alternatives

**Notes natif d'Apple** : gratuit, synchronisé, mais aucune notion de bord d'écran. Tu dois ouvrir l'app, chercher la bonne note, revenir. SideNotes macOS gagne sur l'accès instantané, Notes gagne sur le prix et l'intégration Apple.

**Numi**, dont j'ai déjà parlé dans mon [guide sur Numi, la calculatrice textuelle macOS](/numi-macos-calculatrice-textuelle/), couvre un besoin voisin mais différent : le calcul rapide, pas la prise de notes libre. Les deux se complètent plutôt qu'ils ne se concurrencent.

**Memos en auto-hébergement Docker** répond au même besoin de capture rapide, mais côté serveur perso plutôt qu'app native. Si tu veux garder tes notes hors du cloud d'un éditeur tiers, mon article sur [Memos Docker, ton bloc-notes auto-hébergé](/memos-docker-notes-auto-heberge/) détaille l'installation complète.

**Boring Notch**, que j'ai couvert dans mon article sur [transformer la notch de ton MacBook en Dynamic Island](/boring-notch-macbook-dynamic-island/), joue sur un autre bord de l'écran mais pour de l'affichage média, pas pour du texte éditable.

## Prix et licence

SideNotes macOS coûte 19,99 dollars en achat unique par version majeure, sans abonnement caché. Trois façons de payer : Mac App Store, achat direct sur le site d'Apptorium, ou accès inclus si tu as déjà un abonnement Setapp actif pour d'autres apps.

Pas de version gratuite limitée à tester avant achat sur le site officiel au moment où j'écris ces lignes. Si tu veux essayer sans engager 20 dollars, l'essai Setapp reste la porte d'entrée la moins risquée.

## Limites et points de vigilance

- **Pas de version gratuite pérenne** : tu paies ou tu passes par Setapp, il n'y a pas de troisième voie confortable
- **Sync limitée à iCloud** : aucune option d'auto-hébergement ou de sync via un autre service si tu veux garder la main sur tes données
- **Courbe d'apprentissage du geste de bord d'écran** : les premiers jours, tu vas cliquer là où il fallait glisser, le temps que le réflexe s'installe
- **Un seul bord actif par défaut** : si tu utilises déjà ce bord d'écran pour un autre outil (Mission Control, une zone de snap de fenêtres), attends-toi à un conflit qu'il faudra arbitrer dans les préférences système avant que tout roule sans accroc

Rien de rédhibitoire, mais autant le savoir avant de sortir la carte bleue plutôt qu'après.

💡 À lire aussi : [Keka macOS : compresseur avancé gratuit (7z, split, chiffrement AES)](/keka-macos-compresseur-avance/), dans la même veine que cet article.

## Conclusion

SideNotes macOS n'invente rien de révolutionnaire, il exécute une idée simple avec un soin réel : des notes toujours à portée de main, jamais dans tes pattes. Si tu captures des idées en continu pendant que tu bosses et que basculer entre fenêtres te sort du rythme, les 19,99 dollars se rentabilisent vite.

Si en revanche tu préfères garder tes notes hors des apps tierces payantes, regarde du côté de Memos en auto-hébergement avant de sortir la carte bleue. Les deux font le job, la différence tient à combien de contrôle tu veux garder sur tes données et combien de temps tu veux passer à maintenir un serveur.
