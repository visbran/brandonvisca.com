---
title: "Enregistreur d'écran open source : ScreenKite, OpenScreen, Cap et Recordly comparés (tous multiplateformes)"
description: "Comparatif ScreenKite, OpenScreen, Cap et Recordly : enregistreur d'écran open source, licence, prix et installation sur Mac, Windows et Linux."
pubDatetime: "2026-11-27T11:01:24+01:00"
modDatetime: "2026-11-26T08:00:00.000Z"
author: Brandon
tags:
  - macos
  - productivite
  - multimedia
  - homebrew
  - intermediaire
featured: false
draft: false
focusKeyword: "enregistreur d'écran open source"
faqs:
  - question: "ScreenKite est-il vraiment open source ?"
    answer: "Non. Le site ne publie aucun code source et le dépôt GitHub de l'éditeur ne contient que des releases Windows, pas le logiciel. C'est un outil propriétaire freemium, pas un enregistreur d'écran open source."
  - question: "Cap fonctionne-t-il sans payer et sans compte cloud ?"
    answer: "Oui. Le plan gratuit enregistre et monte en local sans limite, en Studio Mode complet. Seul le partage de lien cloud est plafonné à 25 liens par mois de 5 minutes."
  - question: "Recordly et OpenScreen, c'est le même projet ?"
    answer: "Non, mais ils partagent une origine. Recordly a démarré comme fork d'OpenScreen avant de diverger sur plus de 80% du code, notamment pour son moteur d'auto-zoom."
---
> 💡 **TL;DR**
> - ScreenKite n'est pas open source : c'est un outil propriétaire payant au-delà du filigrane, malgré son nom qui traîne dans toutes les listes « enregistreur d'écran open source »
> - OpenScreen (MIT) et Cap (AGPLv3) sont les deux vrais enregistreurs d'écran open source multiplateformes, avec self-hosting disponible côté Cap
> - Recordly (AGPL) mise tout sur l'auto-zoom automatique, au prix d'un code qui a diverge de plus de 80% depuis son fork d'OpenScreen

## Enregistreur d'écran open source : le tri avant le comparatif

Tu cherches un enregistreur d'écran open source et tu tombes sur ScreenKite dans toutes les comparaisons. Logique, l'éditeur publie lui-même des articles de blog qui le positionnent face à des outils open source. Sauf que ScreenKite n'en est pas un. Bon, on va pas se mentir, c'est le genre de détail qui change toute la discussion.

J'ai vérifié les quatre outils un par un avant d'écrire cette ligne : la page officielle, le dépôt GitHub quand il existe, et le statut du cask Homebrew quand il y en a un. La vraie question c'est de savoir lequel de ces outils respecte vraiment le critère que tu cherches, et lequel coche juste la case marketing.

## Table des matières

## ScreenKite : le signal d'alarme avant de comparer quoi que ce soit

ScreenKite se présente comme un enregistreur d'écran et éditeur vidéo IA pour macOS, avec une version Windows distribuée sur le Microsoft Store. La page officielle ne mentionne à aucun moment un code source ouvert. Elle parle d'un développeur indépendant, « Mike », d'un outil gratuit avec filigrane à l'export, et d'un passage Pro à 49,99 $ en achat unique pour un Mac (un an de mises à jour incluses), ou d'une Founders Edition à 139,99 $ pour trois Macs avec mises à jour à vie.

J'ai été voir l'organisation GitHub de ScreenKite pour être sûr. Deux dépôts publics : des releases Windows compilées, sans licence affichée, et une liste de ressources sur le montage vidéo par IA qui n'a rien à voir avec le logiciel lui-même. Aucune trace du code source de l'application. C'est un outil fermé, point.

⚠️ Ce qui brouille les pistes, c'est que ScreenKite publie sur son propre blog des comparatifs face à des enregistreurs d'écran open source, avec des titres du genre « enregistreurs d'écran open source comparés ». C'est une stratégie de contenu qui marche : l'outil remonte dans les recherches à côté de ses concurrents libres, sans jamais revendiquer lui-même l'étiquette open source. Si ton critère de départ est la licence, ScreenKite sort du jeu avant même la première colonne du tableau.

Ça ne veut pas dire que c'est un mauvais outil. L'édition IA et l'intégration macOS sont soignées, d'après ce que décrit l'éditeur. Mais si tu cherches un vrai enregistreur d'écran open source multiplateforme, passe directement aux trois suivants.

## OpenScreen : le MIT qui a repris le flambeau du projet archivé

OpenScreen est un projet communautaire sous licence MIT. Le site officiel le présente explicitement comme la continuation maintenue du projet original créé par Siddharth Vaddem, dont le dépôt d'origine est aujourd'hui archivé. Pas de société éditrice derrière, pas de paywall, pas de palier premium : « no paywalls, no premium tier, no usage caps » selon la page officielle.

Techniquement, c'est une app Electron en TypeScript et Rust qui tourne sur macOS, Windows et Linux. Elle enregistre une fenêtre ou l'écran entier, capture le micro et l'audio système, superpose une webcam en picture-in-picture, et traite tout en local : zooms automatiques, effets de curseur, sous-titres, flou pour masquer les zones sensibles. Rien n'est envoyé ailleurs sauf si tu choisis d'exporter et de partager toi-même.

Installation sur Mac :

```bash
brew install --cask openscreen
```

J'ai vérifié le cask sur le dépôt Homebrew : version 2.4.0, ni `deprecated`, ni `disabled`. Le projet est donc activement maintenu, contrairement à d'autres outils macOS qu'on continue de recommander par habitude alors qu'ils sont morts depuis des mois, comme c'était le cas pour [Cheatsheet macOS : CheatSheet est mort, KeyClu prend le relais](/cheatsheet-macos-raccourcis-clavier/) jusqu'à ce que la communauté reprenne le flambeau.

Sur Windows, le plus simple passe par le Microsoft Store ou par :

```powershell
winget install --source msstore OpenScreen
```

Sur Linux, un paquet `.deb` est fourni :

```bash
sudo apt install ./Openscreen-Linux-*.deb
```

Des variantes `.rpm`, `.pacman`, une AppImage et un flake Nix couvrent le reste des distributions.

## Cap : enregistreur d'écran open source avec cloud optionnel et self-hosting

Cap (cap.so) est le candidat le plus ambitieux côté architecture. Le dépôt `CapSoftware/Cap` est sous licence AGPLv3 pour l'essentiel du code, avec quelques crates de capture caméra et écran sous MIT. Il affiche 25,6k étoiles sur GitHub au moment où j'écris, un signe que le projet dépasse largement le stade du hobby.

Trois modes d'enregistrement : Instant pour aller vite, Studio pour l'édition complète avec export 4K à 60 fps, et Screenshot pour figer une capture au lieu d'une vidéo. C'est ce dernier mode qui répond à qui cherche du « cap.so screenshot mode » : pas un outil à part, juste un bouton de plus dans la même app.

Le plan gratuit ne plafonne ni l'enregistrement ni le montage local. La limite tombe seulement si tu veux générer des liens de partage hébergés : 25 liens par mois, 5 minutes chacun. Pour un usage commercial sans ce plafond, une licence desktop existe à 29 $ par an ou 58 $ en paiement unique sans renouvellement. Cap Pro, à 12 $ par mois (8,16 $ facturé annuellement), ajoute le stockage cloud illimité, les transcriptions automatiques et les espaces d'équipe.

Ce qui distingue vraiment Cap des trois autres, c'est le self-hosting complet du backend cloud. Si tu gères déjà un homelab, l'auto-hébergement se lance en deux commandes :

```bash
git clone https://github.com/CapSoftware/Cap.git
cd Cap
docker compose up -d
```

Tu récupères alors tes propres liens de partage, sur ton propre stockage compatible S3, sans jamais dépendre des serveurs de l'éditeur. C'est le genre de détail qui compte si tu enregistres des démos clients avec des infos sensibles à l'écran. Pense aussi à vérifier ce qui apparaît réellement dans le cadre avant d'enregistrer : si ta fenêtre de travail est perdue au milieu d'un bureau encombré, ranger tes espaces avec [AeroSpace macOS : le tiling façon i3 sans désactiver SIP](/aerospace-macos-tiling-sans-sip/) évite de couper au montage des bouts de notifications ou d'onglets que tu ne voulais pas montrer.

## Recordly : l'auto-zoom qui a divergé d'OpenScreen

Recordly (recordly.dev) cible une niche précise : l'alternative gratuite à Screen Studio, un logiciel payant macOS-only à 20 $ par mois (ou 9 $ facturé annuellement). Recordly fait le même pari esthétique, en open source, sous licence AGPL-3.0, et sur trois plateformes au lieu d'une.

Le cœur du produit, c'est l'auto-zoom : le logiciel analyse l'activité du curseur et propose lui-même des zones de zoom là où se passe réellement l'action, façon animation Apple de keynote plutôt que capture brute. S'ajoutent un curseur animé avec flou de mouvement, une bulle webcam qui suit le zoom, des cadres et arrière-plans stylisés, et un éditeur de timeline pour les coupes, les changements de vitesse et les annotations.

Côté moteur, Recordly s'appuie sur ScreenCaptureKit sur macOS, sur Windows Graphics Capture (WGC) sur Windows, et sur Electron pour la version Linux. Fait amusant : le projet est né comme fork d'OpenScreen, avant que les mainteneurs ne divergent sur plus de 80% du code pour construire leur propre moteur d'auto-zoom. Les deux projets partagent une filiation, plus grand-chose en commun dans le détail d'implémentation.

Si ta capture tourne autour d'un déplacement de souris saccadé, l'auto-zoom de Recordly va l'exagérer au pire moment. J'utilise [Mos macOS defilement souris fluide : lissage et inversion scroll](/mos-macos-defilement-souris-fluide/) avant chaque session d'enregistrement de démo, histoire que le zoom automatique ne vienne pas souligner un geste de souris qui saute d'un bord d'écran à l'autre.

## Comparatif enregistreur d'écran open source : quel outil pour quel usage

| Critère | ScreenKite | OpenScreen | Cap | Recordly |
|---|---|---|---|---|
| Open source | Non, propriétaire | Oui, MIT | Oui, AGPLv3 (+ MIT sur des crates) | Oui, AGPL-3.0 |
| Plateformes | macOS, Windows | macOS, Windows, Linux | macOS, Windows, Linux | macOS, Windows, Linux |
| Prix de base | Gratuit avec filigrane, Pro 49,99 $ | Gratuit, sans palier | Gratuit en local, Pro 12 $/mois | Gratuit |
| Self-hosting | Non | Non (tout est local de toute façon) | Oui, via Docker Compose | Non documenté officiellement |
| Point fort | Édition IA intégrée | Zooms auto, sous-titres, flou | CLI, MCP, partage cloud optionnel | Auto-zoom sur l'activité du curseur |

Pour un usage perso sans jamais vouloir dépendre d'un éditeur, OpenScreen est le choix le plus simple : une commande Homebrew, zéro compte à créer, zéro limite cachée. Pour une équipe qui veut partager des liens, héberger ses propres vidéos et garder un historique de démos clients, Cap est le seul des trois à vraiment couvrir ce besoin sans sortir de l'open source. Pour des tutoriels produit où le zoom automatique sur le curseur fait gagner un temps fou au montage, Recordly reste la référence, tant que tu acceptes un projet plus jeune et moins documenté côté self-hosting.

Si tu enregistres depuis un écran externe en résolution custom, les artefacts de mise à l'échelle se voient immédiatement sur la vidéo finale. Mon guide [BetterDisplay macOS hidpi : résolutions custom et contrôle DDC sur écrans externes](/betterdisplay-macos-hidpi-ddc/) règle ce problème avant même d'ouvrir l'enregistreur. Et si tu cherches d'autres outils macOS du même acabit, gratuits et sans compromis sur la confidentialité, j'en liste une dizaine dans [10 Outils macOS gratuits que j'utilise (2026)](/10-outils-low-tech-macos-guide-complet/).

## Conclusion

Le vrai tri, ici, se fait avant la première minute d'enregistrement : ScreenKite n'est pas un enregistreur d'écran open source, quoi que suggère son positionnement marketing. Les trois autres le sont réellement, avec des équilibres différents. OpenScreen pour la simplicité et l'absence totale de palier payant. Cap pour l'équipe qui veut garder la main sur son stockage via le self-hosting. Recordly pour qui veut un rendu léché sans toucher à une timeline pendant des heures.

Spoiler : aucun des trois ne va te décevoir sur la qualité de capture de base. La différence se joue sur ce que tu veux faire après l'enregistrement, pas pendant.
