---
title: "Velja macOS : choisis quel navigateur ouvrir pour chaque lien"
description: Velja macOS route chaque lien vers le bon navigateur, par domaine, appli source ou profil, avec nettoyage automatique du tracking.
pubDatetime: "2026-09-14T11:01:11+02:00"
modDatetime: "2026-09-13T08:00:00.000Z"
author: Brandon
tags:
  - macos
  - productivite
  - intermediaire
featured: false
draft: false
focusKeyword: velja macos
faqs:
  - question: "Velja macOS est-il gratuit ?"
    answer: "Non. Velja coûte environ 8 dollars sur le Mac App Store. Un essai gratuit complet est disponible en téléchargement direct depuis le site de l'éditeur avant d'acheter."
  - question: "Faut-il désinstaller Safari ou Chrome pour utiliser Velja macOS ?"
    answer: "Non, aucun navigateur n'est supprimé. Tu désignes Velja comme navigateur par défaut dans les réglages système, et il se contente de rediriger chaque lien vers le vrai navigateur choisi."
  - question: "Velja macOS fonctionne-t-il avec les profils Chrome ou Edge ?"
    answer: "Oui. Velja détecte les profils Chrome, Edge, Brave et les autres navigateurs basés sur Chromium, et tu peux créer une règle qui ouvre un lien précis dans un profil précis."
---
> 💡 **TL;DR**
> - Velja macOS s'installe à la place de ton navigateur par défaut et redirige chaque lien vers le bon navigateur, la bonne appli ou le bon profil, selon des règles par domaine ou par appli source
> - Compatible Chrome, Edge, Brave, Firefox et leurs profils, avec nettoyage automatique des paramètres de tracking dans les URLs
> - Développé par Sindre Sorhus, environ 8 dollars sur le Mac App Store (essai gratuit disponible en direct), nécessite macOS 26 ou plus récent

## Velja macOS : pourquoi ton Mac a besoin d'un routeur de liens

Tu cliques sur un lien dans Slack. Ça ouvre Safari. Sauf que ce lien, tu voulais l'ouvrir dans Chrome, parce que c'est là qu'est ton compte pro avec toutes tes extensions. Résultat : tu copies l'URL, tu la recolles dans Chrome, tu perds dix secondes. Multiplie ça par vingt fois par jour et t'as compris le problème.

macOS ne connaît qu'un seul navigateur par défaut. Un seul, pour tous les liens, peu importe d'où ils viennent. C'est absurde quand tu jongles entre un compte perso sur Firefox, un compte boîte sur Chrome, et un navigateur dédié à la crypto ou aux tests que tu ne veux surtout pas mélanger avec le reste.

C'est exactement ce que corrige Velja macOS. L'app se place entre le clic et l'ouverture du lien, regarde d'où vient l'URL et où elle pointe, puis décide (ou te demande) quel navigateur doit s'en charger. Développée par Sindre Sorhus, une référence chez les développeurs macOS pour ses petits utilitaires bien pensés, elle fait exactement une chose et la fait bien.

## Table des matières

## Installer Velja macOS

Pas de `brew install --cask` ici. Contrairement à beaucoup d'outils que je couvre sur ce blog, Velja macOS n'a pas de cask Homebrew : Sindre Sorhus la distribue uniquement via son propre site, en essai gratuit complet à télécharger, et via le Mac App Store pour l'achat définitif.

Deux chemins possibles :

- Télécharger l'essai depuis [sindresorhus.com/velja](https://sindresorhus.com/velja) pour tester toutes les fonctionnalités sans limite de temps, avec des rappels d'achat une fois lancée
- Acheter directement sur le Mac App Store si t'es déjà convaincu

L'app nécessite macOS 26 ou une version plus récente. Si tu tournes encore sur un système plus ancien, tu devras d'abord mettre à jour macOS avant même de pouvoir l'installer.

Une fois lancée, Velja tourne en arrière-plan avec une icône dans la barre de menu. C'est elle qui affiche le navigateur actuellement défini par défaut et qui te donne un accès rapide aux réglages.

## Configurer Velja macOS comme navigateur par défaut

Voilà l'étape que tout le monde oublie et qui bloque la moitié des utilisateurs au premier lancement : Velja macOS ne fait rien tant qu'il n'est pas défini comme navigateur par défaut du système.

Va dans **Réglages Système** > **Bureau et Dock**, descends jusqu'à **Navigateur web par défaut**, et sélectionne Velja dans la liste. C'est contre-intuitif : tu ne remplaces pas ton navigateur habituel, tu remplaces le rôle de « standard de macOS » par Velja, qui lui-même redispatche vers le vrai navigateur choisi.

⚠️ Sans cette étape, tous tes liens continueront de s'ouvrir dans l'ancien navigateur par défaut, et Velja restera une icône inutile dans ta barre de menu.

Une fois ce réglage fait, teste avec un lien depuis Mail ou Messages. Une petite fenêtre de Velja macOS doit apparaître, te proposant le choix du navigateur si aucune règle ne s'applique encore.

## Créer des règles par domaine et par application

C'est le cœur de l'outil. Sans règles, Velja te demande à chaque clic, ce qui devient vite lourd. Avec des règles, tout devient automatique.

Une règle Velja combine plusieurs critères :

- **Le domaine du lien** : `github.com` toujours dans Chrome, `notion.so` toujours dans le navigateur perso
- **L'application source** : un lien cliqué depuis Slack part sur un navigateur, le même lien cliqué depuis Mail part sur un autre
- **Le chemin de l'URL** : tu peux descendre jusqu'au sous-dossier pour affiner encore

L'ordre des règles compte. Velja évalue de haut en bas et applique la première qui correspond. Range tes règles les plus spécifiques en premier, et une règle générique en dernier filet de sécurité.

✅ Astuce concrète : si tu géres un homelab, crée une règle qui envoie systématiquement les liens `*.ton-domaine.local` ou tes interfaces d'admin (Proxmox, Portainer, pfSense) vers un profil dédié, séparé de ta navigation perso. Ça évite les sessions qui se mélangent et les cookies qui traînent au mauvais endroit.

## Profils de navigateur : Chrome, Edge, Brave, Firefox

Velja macOS ne se contente pas de choisir entre navigateurs, il descend au niveau du profil. Si tu as plusieurs profils Chrome (un perso, un pro, un client), tu peux créer une règle qui ouvre un lien précis dans le profil précis, sans jamais passer par le sélecteur de profil natif de Chrome qui te fait perdre du temps.

Ça marche avec Chrome, Edge, Brave et les autres navigateurs basés sur Chromium. Firefox est également supporté, avec ses propres profils si tu les utilises.

C'est particulièrement pratique pour les freelances et les consultants qui jonglent entre plusieurs comptes Google Workspace ou Microsoft 365 sur des profils séparés. Un lien reçu par mail d'un client s'ouvre automatiquement dans le bon profil, sans que tu aies à vérifier lequel est actif.

## Automatiser Velja macOS avec Raccourcis

Velja macOS expose un schéma d'URL personnalisé et s'intègre dans l'app Raccourcis de macOS. Tu peux donc déclencher l'ouverture d'un lien dans un navigateur précis depuis un raccourci que tu construis toi-même, ou l'appeler depuis un script.

Pour ceux qui veulent aller plus loin dans l'automatisation système, mon article sur [Hammerspoon macOS : scripting Lua ultra-puissant pour automatiser tout](/hammerspoon-macos-scripting-lua/) montre comment scripter des comportements bien plus larges que le simple routage de liens, si Velja te donne le goût de l'automatisation.

Autre fonctionnalité utile de Velja macOS : le nettoyage automatique des paramètres de tracking dans les URLs. L'app reconnaît plus de 200 paramètres de suivi courants (`utm_source`, `fbclid`, et compagnie) et les retire avant d'ouvrir le lien. Tu gagnes en confidentialité sans rien faire de plus, et tes URLs partagées restent propres.

Si ton usage penche plutôt vers des contextes de travail complets à basculer d'un coup (navigateur, apps, disposition de fenêtres), regarde aussi [Bunch macOS : lance des contextes complets en un clic](/bunch-macos-lancer-contextes/) : combiné à des règles Velja bien pensées, tu changes de mode de travail en un raccourci, navigateur inclus.

## Velja macOS vs les alternatives

Le marché du routeur de liens macOS n'est pas immense, mais quelques noms reviennent souvent :

- **Choosy** : le pionnier historique, fonctionnel mais à l'interface vieillissante, moins actif en développement
- **Finicky** : gratuit et open source, mais configuré entièrement en JavaScript dans un fichier texte, réservé aux devs à l'aise avec ce format
- **Velja macOS** : interface native, réglages visuels sans toucher à un fichier de config, profils Chromium et Firefox gérés nativement, développement actif

Si tu veux zéro configuration texte et une interface propre, Velja macOS l'emporte. Si tu préfères tout piloter en JSON versionné dans un dotfiles, Finicky reste une option gratuite valable.

Pour la gestion rapide de réglages système complémentaires (Wi-Fi, Bluetooth, Do Not Disturb), j'utilise à côté [One Switch macOS : panneau de contrôle rapide en un clic](/one-switch-macos-panneau-controle/), qui vit dans la même barre de menu que Velja sans jamais entrer en conflit.

Si ton besoin est différent, c'est-à-dire un navigateur auto-hébergé accessible depuis n'importe où plutôt qu'un routeur local, regarde plutôt [Alcove Docker : navigateur web auto-hébergé pour homelab](/alcove-navigateur-auto-heberge/). Ce n'est pas un concurrent de Velja, c'est un complément pour un usage homelab bien différent.

## Limites et points de vigilance

Quelques réserves avant de foncer :

- **Prix** : environ 8 dollars, pas de version gratuite illimitée, seulement un essai
- **macOS 26 minimum** : les Mac tournant sur un système plus ancien sont exclus
- **Pas de version Windows ou Linux** : Velja macOS reste un outil exclusivement Apple
- **Un temps d'apprentissage** : la logique de règles par priorité demande un peu de tâtonnement au début, surtout si tu as beaucoup de domaines à router

Rien de rédhibitoire, mais si tu n'ouvres jamais de liens depuis plusieurs profils ou navigateurs, l'app n'apportera pas grand-chose à ton quotidien.

## Conclusion

Velja macOS règle un problème que macOS refuse de résoudre depuis toujours : un seul navigateur par défaut pour des usages qui, eux, sont multiples. Une fois les règles posées, tu ne repenses plus jamais au bon navigateur à ouvrir, ça se fait tout seul.

Pour 8 dollars et un essai gratuit sans engagement, ça vaut clairement le test si tu jongles entre plusieurs comptes ou plusieurs profils. Installe l'essai, configure trois ou quatre règles pour tes domaines les plus utilisés, et regarde si l'habitude s'installe. Chez moi, elle a mis une semaine à devenir invisible, et c'est exactement ce qu'on attend d'un bon outil système.
