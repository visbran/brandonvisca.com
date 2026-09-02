---
title: "Maccy macOS : presse-papiers open-source avec historique et recherche"
description: Maccy est un gestionnaire de presse-papiers open-source pour macOS. Historique, recherche rapide, raccourcis clavier. Guide installation.
pubDatetime: "2026-09-02T06:00:00.000Z"
modDatetime: "2026-09-02T06:00:00.000Z"
author: Brandon
tags:
  - macos
  - productivite
  - debutant
  - guide
  - open-source
featured: false
draft: false
focusKeyword: maccy macos
faqs:
  - question: "Maccy est-il gratuit ?"
    answer: "Oui, Maccy est 100% gratuit et open-source sous licence MIT. Aucune version payante, aucun abonnement. Le code source est disponible sur GitHub."
  - question: "Maccy fonctionne-t-il sur Apple Silicon ?"
    answer: "Oui, Maccy est compatible avec les Mac Intel et Apple Silicon (M1, M2, M3, M4). Il est developpe en Swift natif et tres leger."
  - question: "Maccy peut-il stocker des mots de passe ?"
    answer: "Non, et c'est une bonne chose. Maccy ignore par defaut les applications comme 1Password, Bitwarden ou Keychain. Tu peux aussi configurer des exclusions manuelles."
  - question: "Quelle est la difference avec le presse-papiers natif macOS ?"
    answer: "Le presse-papiers natif macOS ne garde que le dernier element copie. Maccy conserve un historique illimite, ajoute une recherche, des raccourcis clavier et des exclusions."
  - question: "Maccy consomme-t-il beaucoup de ressources ?"
    answer: "Non. Maccy pese moins de 10 Mo en RAM au repos. C'est un outil Swift natif qui tourne en arriere-plan sans impacter les performances."
---
> 💡 **TL;DR**
> - Maccy est un gestionnaire de presse-papiers open-source pour macOS, gratuit et developpe en Swift natif
> - Il conserve un historique illimite de tes copies avec une recherche instantanee et des raccourcis clavier personnalisables
> - Installation en 10 secondes via Homebrew, configuration minimaliste, zero impact sur les performances

T'as deja copie un lien, une adresse ou un morceau de code pour te rendre compte 30 secondes plus tard que tu as ecrase le presse-papiers avec un autre copier-coller ? C'est le scenario classique. macOS garde en memoire une seule chose a la fois. Un seul. C'est ridicule en 2026.

Maccy resout ce probleme. C'est un gestionnaire de presse-papiers open-source, gratuit, qui stocke tout ton historique de copies et te permet de retrouver n'importe quel element en quelques frappes. J'utilise Maccy depuis plus de deux ans sur mon MacBook Pro M3. Il tourne en arriere-plan, invisible, et me sauve plusieurs fois par jour. Voici pourquoi tu devrais l'installer aujourd'hui.

## Qu'est-ce que Maccy et pourquoi tu en as besoin

Maccy est un gestionnaire de presse-papiers concu specifiquement pour macOS. Il est developpe en Swift natif par Alex Rodionov, distribue sous licence MIT, et disponible gratuitement sur GitHub. Contrairement aux solutions lourdes ou payantes, Maccy fait une chose et la fait bien : il garde une trace de tout ce que tu copies et te donne un acces rapide a cet historique.

Le presse-papiers natif de macOS est limite. Tu fais Cmd+C, tu colles avec Cmd+V, et c'est tout. Si tu copies un second element, le premier disparait pour toujours. Pas d'historique, pas de recherche, pas de raccourcis avances. C'est comme utiliser un terminal sans historique de commandes : ca fonctionne, mais tu perds du temps a chaque instant.

Avec Maccy, chaque copie est archivee. Tu peux remonter dans le temps, rechercher un texte precis, coller un ancien element sans passer par la souris, et meme exclure certaines applications sensibles. C'est particulierement utile si tu travailles avec du code, des liens, des adresses e-mail ou des references que tu reutilises regulierement.

> **Astuce**
> Maccy pese moins de 10 Mo de RAM au repos. Sur un MacBook Pro M3, je ne vois meme pas la difference. C'est plus leger que la plupart des widgets de la barre de menu.

## Installation : Homebrew ou manuel

Il y a deux facons d'installer Maccy. La premiere est la plus rapide et la plus recommandee.

### Via Homebrew

Si tu as deja Homebrew installe, une seule ligne suffit :

```bash
brew install --cask maccy
```

L'application se telecharge, s'installe dans le dossier Applications et se lance automatiquement. Le tout prend moins de 10 secondes sur une connexion standard. C'est la methode que j'utilise et que je recommande a tout le monde.

> **Astuce**
> Si tu ne connais pas encore Homebrew, c'est le gestionnaire de paquets indispensable pour macOS. J'en parle regulierement dans les guides macOS comme [Ice macOS](/ice-macos-gestionnaire-barre-menu-gratuit-2025/) ou [AltTab macOS](/alttab-macos-gestion-fenetres-windows/), car la plupart des outils productivite s'installent ainsi.

### Via le site officiel

Prefere-tu le telechargement manuel ? Rend-toi sur le site officiel de Maccy ou sur la page GitHub du projet. Telecharge le fichier .dmg, ouvre-le, et glisse l'application dans ton dossier Applications. C'est aussi simple.

Apres l'installation, Maccy te demande quelques permissions : Accessibility et Screen Recording. Ne panique pas. La permission Accessibility permet a Maccy de simuler les combinaisons de touches pour coller un element selectionne. La permission Screen Recording est necessaire pour capturer les images du presse-papiers. Aucune donnée n'est envoyee sur Internet. Le code est open-source, tu peux l'auditer toi-meme si tu es paranoiaque.

## Utilisation au quotidien

Des que Maccy est lance, il commence a enregistrer chaque element que tu copies. Tu remarqueras une petite icone en forme de ciseaux dans ta barre de menu. C'est l'interface principale.

Pour acceder a ton historique, tu as deux options. Tu peux cliquer sur l'icone de la barre de menu, ou tu peux utiliser le raccourci clavier par defaut : Maj+Cmd+V. Une fenetre flottante apparait avec la liste de tes derniers elements copies. Navigue avec les fleches du clavier, appuye sur Entree, et l'element est colle a l'endroit ou se trouve ton curseur.

> **Astuce**
> Appuie sur Echap pour fermer la fenetre Maccy sans coller. C'est pratique quand tu ouvres l'historique par erreur ou que tu changes d'avis.

Chaque element de l'historique affiche un apercu du texte ou de l'image. Les images sont representees par une miniature. Les textes longs sont tronques mais completement disponibles au moment du collage. Tu peux aussi voir la date et l'heure de la copie, ce qui aide a retrouver un element meme si tu as oublie son contenu exact.

Par defaut, Maccy conserve 200 elements dans l'historique. Tu peux augmenter cette limite dans les preferences ou laisser l'historique croitre indefiniment. Sur mon setup, je garde 500 elements. Ca represente plusieurs jours de travail sans jamais perdre une information.

## Les fonctionnalites qui changent tout

Maccy n'est pas qu'un simple historique. Il embarque plusieurs fonctionnalites qui le transforment en outil productivite indispensable.

### Historique illimite

Le coeur de Maccy, c'est son historique. Chaque copie est stockee avec un horodatage. Tu peux remonter des heures, des jours, voire des semaines en arriere pour retrouver un element. J'ai deja sauve un article de blog entier grace a Maccy apres avoir ferme une fenetre sans sauvegarder. Le texte etait encore dans l'historique.

Tu peux configurer la taille maximale de l'historique dans les preferences. 200 est le defaut, mais tu peux monter a 999 ou desactiver la limite. Attention : si tu copies beaucoup d'images, l'historique prend de la place sur le disque. Pour du texte pur, c'est negligeable.

> **Astuce**
> Active l'option "Delete on paste" si tu veux qu'un element disparaisse de l'historique apres l'avoir colle. C'est utile pour les mots de passe temporaires ou les informations sensibles.

### Recherche instantanee

C'est la fonctionnalite que j'utilise le plus. Quand tu ouvres la fenetre Maccy, tu peux directement taper du texte pour filtrer l'historique. Pas besoin de cliquer dans un champ de recherche, Maccy capture tes frappes des l'ouverture.

Tape un mot-cle, un fragment de phrase, ou meme quelques lettres. L'historique se filtre en temps reel. Appuye sur Entree pour coller le premier resultat, ou utilise les fleches pour en choisir un autre. C'est radical pour retrouver un lien que tu as copie il y a trois jours sans avoir a scroller des dizaines d'elements.

La recherche est insensible a la casse et fonctionne aussi bien sur le texte que sur les noms de fichiers images. C'est rapide, fluide, et ca fonctionne meme avec des historiques de plusieurs centaines d'elements.

### Raccourcis clavier

Maccy est concu pour les utilisateurs de clavier. Le raccourci par defaut est Maj+Cmd+V, mais tu peux le changer dans les preferences. Moi, je l'ai garde. Il est intuitif : Cmd+V pour le dernier element, Maj+Cmd+V pour l'historique complet.

Une fois la fenetre ouverte, tu navigues avec les fleches Haut et Bas. Entree colle l'element selectionne. Echap ferme la fenetre. Tu peux aussi utiliser Cmd+1, Cmd+2, etc., pour coller directement l'un des 9 premiers elements sans meme naviguer. C'est bluffant de rapidite quand tu as des elements recurrents en tete de liste.

> **Astuce**
> Pince l'element que tu utilises le plus souvent. Il restera en haut de la liste et ne sera jamais pousse par les nouvelles copies. C'est parfait pour une adresse e-mail professionnelle ou un lien de reunion recurrent.

### Preferences et personnalisation

Maccy est minimaliste, mais il offre suffisamment d'options pour s'adapter a ton workflow. Dans les preferences, tu peux :

- Changer le raccourci clavier global
- Modifier la taille maximale de l'historique
- Activer ou desactiver le lancement au demarrage
- Choisir le format de la date affichee
- Activer le mode "Supprimer apres collage" pour des elements sensibles
- Ajuster la hauteur et la largeur de la fenetre flottante
- Choisir si Maccy doit apparaitre dans la barre de menu ou rester completement invisible

J'ai configure Maccy pour demarrer automatiquement, avec une fenetre de taille moyenne et l'historique limite a 500 elements. L'icone dans la barre de menu est desactivee chez moi : je n'utilise que le raccourci clavier. C'est un choix esthetique, mais tout fonctionne aussi bien avec l'icone visible.

### Exclusions et confidentialite

Voici la fonctionnalite qui rassure. Maccy peut ignorer completement certaines applications. Par defaut, il exclut deja les gestionnaires de mots de passe comme 1Password, Bitwarden, Keychain et les applications bancaires. Il ne stockera jamais ce que tu copies dans ces outils.

Tu peux ajouter tes propres exclusions dans les preferences. C'est utile si tu utilises un gestionnaire de mots de passe peu connu ou si tu travailles avec des documents confidentiels dans une application specifique. Maccy te laisse le controle total.

> **Attention**
> N'oublie pas de verifier la liste des exclusions apres l'installation. Meme si Maccy protege les applications connues par defaut, un nouvel outil de securite peut ne pas etre dans la liste. Ajoute-le manuellement pour etre tranquille.

Maccy ne se connecte jamais a Internet. Tout reste local sur ton Mac. Pas de synchronisation cloud, pas de compte utilisateur, pas de collecte de donnees. C'est un point clé pour un outil qui manipule ton presse-papiers. Si tu es sceptique, tu peux bloquer Maccy avec un pare-feu applicatif comme Little Snitch ou Lulu. Il ne se plaindra pas, il n'a rien a envoyer.

## Maccy vs le presse-papiers natif de macOS

Apple a ajoute un historique de presse-papiers dans iOS depuis quelques versions, mais macOS reste a la traine. Le systeme natif ne propose qu'une seule case memoire. Pas d'historique, pas de recherche, pas de raccourci dedie. C'est fonctionnel pour un usage basique, mais des que tu travailles un minimum, c'est insuffisant.

Il existe aussi l'outil Universal Clipboard d'Apple qui synchronise le presse-papiers entre tes appareils. C'est pratique, mais il partage le meme defaut : une seule case memoire. Et il ne fonctionne que si tu es dans l'ecosysteme Apple complet avec iCloud active.

Maccy ne remplace pas Universal Clipboard. Les deux peuvent coexister. Maccy ajoute une couche d'historique et de recherche locale, sans dependre d'iCloud ou d'une connexion Internet. C'est plus fiable, plus rapide, et ca fonctionne meme hors ligne.

Si tu cherches une alternative a Maccy, Paste est la reference payante. Il est elegant, synchronise entre appareils, et offre un design plus travaille. Mais il coute environ 15 euros par an. Maccy fait 95% du job gratuitement, sans abonnement, et avec un code source ouvert. Pour un usage personnel ou professionnel sur un seul Mac, le choix est rapide.

> **Bonne pratique**
> Si tu as plusieurs Mac, Maccy ne synchronise pas entre eux. Utilise une alternative comme Paste ou un gestionnaire de snippets dedie pour les elements que tu partages regulierement entre machines. Garde Maccy pour l'historique local.

## Conclusion

Maccy est l'un de ces outils que tu installes en 10 secondes et qui te font gagner du temps chaque jour. Il est gratuit, open-source, leger, et respecte ta vie privee. Pas de compte a creer, pas de donnees dans le cloud, pas d'interface surchargee. Un raccourci clavier, une fenetre flottante, et tu retrouves tout ce que tu as copie depuis des heures.

Si tu travailles sur macOS, que tu copies du texte, des liens, du code ou des images, Maccy devrait faire partie de ton setup de base. Il est aussi indispensable qu'un bon gestionnaire de fenetres ou une barre de menu organisee. [Ice macOS](/ice-macos-gestionnaire-barre-menu-gratuit-2025/), [AltTab macOS](/alttab-macos-gestion-fenetres-windows/) et Maccy forment chez moi un trio productivite minimaliste et efficace.

Installe-le aujourd'hui via Homebrew ou depuis GitHub. Configure-le en 2 minutes. Oublie-le. Il travaillera en silence et te sauvera la mise au moment ou tu t'y attendras le moins. C'est exactement ce qu'on attend d'un bon outil macOS.

## Pour aller plus loin

- [10 Outils macOS gratuits que j'utilise](/10-outils-low-tech-macos-guide-complet/) : une liste complete de ma suite productivite macOS, avec Maccy, Ice, AltTab et d'autres outils open-source
- [AltTab macOS : gestion de fenetres style Windows](/alttab-macos-gestion-fenetres-windows/) : remplace le Cmd+Tab natif avec des previews visuelles de chaque fenetre, gratuit et open-source
- [Ice macOS : remplace Bartender gratuitement](/ice-macos-gestionnaire-barre-menu-gratuit-2025/) : organise ta barre de menu avec des sections, des hotkeys et une personnalisation complete
