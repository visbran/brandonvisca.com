---
title: "Importer fichiers PST dans Outlook 365 : Guide fiable et rapide (2025)"
pubDatetime: "2025-02-21T10:14:37+01:00"
description: Guide complet pour importer vos fichiers PST dans Outlook 365. 2 méthodes testées + alternative XstReader pour lire vos emails sans Outlook. Solutions g...
tags:
  - microsoft-365
  - sysadmin
  - intermediaire
  - outlook
  - migration
  - guide
---

> **TL;DR** : Microsoft a viré la fonction import PST d’Outlook 365. Spoiler : t’es pas mort pour autant. Deux solutions qui marchent + une astuce gratuite pour lire tes vieux emails sans t’arracher les cheveux.
> 
> 
> - [Le drame en 3 actes](#le-drame-en-3-actes)
> - [Pourquoi Microsoft nous emmerde avec les PST ?](#pourquoi-microsoft-nous-emmerde-avec-les-pst)
> - [Solution 1 : La méthode « oldschool » (ancienne version Outlook)](#solution-1-la-methode-oldschool-ancienne-version-outlook)
>   - [Ce qu’il te faut](#ce-quil-te-faut)
>   - [La procédure qui marche](#la-procedure-qui-marche)
>   - [Quand ça foire (et ça arrive)](#quand-ca-foire-et-ca-arrive)
> - [Solution 2 : XstReader (le plan B qui sauve tout)](#solution-2-xst-reader-le-plan-b-qui-sauve-tout)
>   - [Pourquoi c’est génial](#pourquoi-cest-genial)
>   - [Comment s’en servir (c’est idiot de simplicité)](#comment-sen-servir-cest-idiot-de-simplicite)
> - [FAQ (parce que vous posez toujours les mêmes questions)](#faq-parce-que-vous-posez-toujours-les-memes-questions)
>   - [« Combien de temps ça prend ? »](#combien-de-temps-ca-prend)
>   - [« XstReader c’est vraiment gratuit ? »](#xst-reader-cest-vraiment-gratuit)
>   - [« L’import échoue, je fais quoi ? »](#limport-echoue-je-fais-quoi)
>   - [« Je peux traiter plusieurs PST en même temps ? »](#je-peux-traiter-plusieurs-pst-en-meme-temps)
> - [💀 Les pièges à éviter (appris à mes dépens)](#%F0%9F%92%80-les-pieges-a-eviter-appris-a-mes-depens)
>   - [« Le fichier .pst ne peut pas être ouvert »](#le-fichier-pst-ne-peut-pas-etre-ouvert)
>   - [« Import partiel – la moitié des emails a disparu »](#import-partiel-la-moitie-des-emails-a-disparu)
>   - [« Outlook freeze pendant l’import »](#outlook-freeze-pendant-limport)
> - [Pour aller plus loin (et sécuriser tout ça)](#pour-aller-plus-loin-et-securiser-tout-ca)
> - [Ce qu’il faut retenir](#ce-quil-faut-retenir)
> 
> 

- - - - - -

Le drame en 3 actes
-------------------

**Acte 1** : Tu lances Outlook 365 tout content  
**Acte 2** : Tu cherches « Importer/Exporter » → Introuvable  
**Acte 3** : Tu réalises que tes 10 ans d’emails sont coincés dans un `.pst`

Si tu reconnais ce scénario, bienvenue au club ! Avec 1,3 milliard d’utilisateurs Outlook dans le monde, on est quelques-uns à s’être fait avoir par cette « évolution » de Microsoft.

**La vraie raison ?** Microsoft veut tout pousser dans le cloud Exchange Online. Les fichiers PST, c’est l’ancien monde. Pas rentable, pas contrôlable, pas moderne.

Résultat : tu te retrouves avec tes précieuses archives sur les bras et aucun moyen « officiel » de les récupérer.

**Bonne nouvelle :** Il reste des solutions. On va voir ça.

- - - - - -

Pourquoi Microsoft nous emmerde avec les PST ?
----------------------------------------------

C’est simple : Microsoft gagne plus d’argent avec Exchange Online qu’avec du stockage local.

**Leur logique :**

- PST = stockage local = pas de revenus récurrents
- Exchange Online = abonnement mensuel = $$$
- Bonus : ils contrôlent tes données

**Pour toi, ça veut dire :**

- Plus de menu « Import/Export » dans les nouvelles versions
- Migration forcée vers les boîtes en ligne (payantes)
- Fichiers > 2GB ? Oublie, ça plante

Pour nous, administrateurs système qui devons gérer ces conneries au quotidien, c’est aussi frustrant que de [sécuriser un serveur Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/) avec des utilisateurs qui utilisent « password123 ».

- - - - - -

Solution 1 : La méthode « oldschool » (ancienne version Outlook)
----------------------------------------------------------------

### Ce qu’il te faut

- Outlook 2016-2019 (versions desktop)
- Ou Outlook 365 Desktop d’avant mars 2024
- Un environnement qui n’a pas encore été « migré de force »

**☠️ Attention piège :** Si ton PST est corrompu, tu vas juste planter ton Outlook. Test d’intégrité obligatoire avant (on verra ça plus bas).

### La procédure qui marche

**Étape 1 :** Lance ton Outlook (l’ancien, hein)

**Étape 2 :** Va dans `Fichier` → `Ouvrir et exporter` → `Importer/Exporter`  
*(Si tu vois pas ce menu, c’est que t’as déjà la nouvelle version… passe à la solution 2)*

**Étape 3 :** Sélectionne « Importer à partir d’un autre programme ou fichier »

**Étape 4 :** Choisis « Fichier de données Outlook (.pst) »

**Étape 5 :** Configuration (la partie critique) :

- Trouve ton fichier `.pst`
- **Important :** Coche « Inclure les sous-dossiers » (sinon tu récupères que l’Inbox)
- Option « Remplacer les doublons » → à toi de voir selon tes besoins

**Étape 6 :** Clique sur « Terminer » et va prendre un café

**Durée :** Entre 5 minutes (petit PST) et 30 minutes (gros bordel de 1.5GB).

### Quand ça foire (et ça arrive)

**Import bloqué à 50% ?** → Ton PST fait plus de 2GB. Fais-le maigrir ou découpe-le.

**Outlook plante ?** → Pas assez de RAM ou PST défragmenté. Ferme tout, redémarre, et divise par lots.

Si tu bosses en environnement AD et que ton PST est sur un partage réseau, assure-toi que ton [intégration Ubuntu Active Directory avec SSSD](https://brandonvisca.com/integration-ubuntu-active-directory-sssd/) permet l’accès aux fichiers. Ça peut paraître con, mais j’ai vu des gens galérer 2h là-dessus.

- - - - - -

Solution 2 : XstReader (le plan B qui sauve tout)
-------------------------------------------------

### Pourquoi c’est génial

XstReader, c’est le couteau suisse des PST. Gratuit, portable, et ça marche partout.

**Développé par qui ?** Une équipe d’anciens de Microsoft qui en avaient marre des solutions payantes pourries.

**Les plus :**

- ✅ **100% gratuit** (pas de « version premium » cachée)
- ✅ **Multi-plateforme** : Windows, Linux, macOS
- ✅ **Portable** : tu décompresses, tu lances
- ✅ **Lecture seule** : impossible de péter tes données par accident
- ✅ **Rapide** : même sur des PST de 2GB+

**Les moins :**

- Interface en anglais seulement
- Export limité (pas de conversion massive)
- Nécessite .NET sur Windows

### Comment s’en servir (c’est idiot de simplicité)

**Étape 1 : Téléchargement**

```bash
https://www.xstreader.com/download
# Version portable - pas d'installation

```

