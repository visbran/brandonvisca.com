---
title: "Migrer WordPress gratuitement avec All-in-One WP Migration : guide 2026"
description: "Migrez WordPress gratuitement avec All-in-One WP Migration v6.77 (téléchargeable). Guide complet : export, import, contourner la limite PHP."
pubDatetime: "2025-02-24T18:51:33+01:00"
modDatetime: "2026-05-17T00:00:00+01:00"
author: Brandon Visca
tags:
  - developpement
  - wordpress
  - sysadmin
  - backup
  - intermediaire
  - guide
featured: false
draft: false
focusKeyword: All-in-One WP Migration
faqs:
  - question: "Combien de temps prend une migration WordPress ?"
    answer: "Selon la taille du site, entre 30 minutes (petit site) et 2 heures (gros site avec base de données massive)."
  - question: "All-in-One WP Migration est-il gratuit ?"
    answer: "La version 6.77 importe gratuitement. Les versions récentes ont retiré cette fonction et demandent une extension payante."
  - question: "Que faire si la migration échoue ?"
    answer: "Vérifie les logs d'erreur, augmente les limites PHP (upload_max_filesize, memory_limit), ou utilise la migration manuelle par FTP."
  - question: "Faut-il sauvegarder avant migration ?"
    answer: "Toujours. Crée une sauvegarde via phpMyAdmin ou le Dashboard WordPress avant de migrer. C'est ton filet de sécurité."
---
> 💡 **TL;DR** : Installe All-in-One WP Migration v6.77 (la dernière version qui importe gratuitement), exporte depuis l'ancien site, importe sur le nouveau. Augmente la limite dans `constants.php` si ton site dépasse 512 MB. [Télécharge directement la v6.77 ici.](/downloads/all-in-one-wp-migration.6.77.zip)

![Illustration — Migrer WordPress en 2026](fusion-vid-ppap-bhecjdygjck6c-1.gif)

Alors, tu dois migrer ton site WordPress et tu te demandes comment faire ça proprement sans tout péter ? Parfait, tu es au bon endroit ! La migration WordPress, c'est un peu comme déménager : si tu t'y prends mal, tu risques de casser la vaisselle.

**[All-in-One WP Migration](/downloads/all-in-one-wp-migration.6.77.zip)** est probablement le plugin le plus populaire pour cette mission. Et on va voir pourquoi : interface simple, processus quasi-automatique, et surtout… ça marche !

## Table des matières

- - - - - -

## 1. Installation du plugin All-in-One WP Migration

Première étape : installer ce petit bijou sur ton **site de destination**. Ouais, pas sur l'ancien, sur le nouveau ! C'est logique mais on préfère le préciser.

### Étapes d'installation

1. **Accède à ton dashboard WordPress** (admin de ton nouveau site)
2. **Extensions** → **Ajouter une extension**
3. **Recherche « All-in-One WP Migration »** dans la barre de recherche
4. **Installe et active** le plugin

> ⚠️ **Point important :** Si tu as déjà une version plus récente installée, désactive-la avant d'activer la version 6.77. Les versions récentes ont supprimé la fonction d'import gratuite.

### Alternative : installation manuelle (version 6.77)

Si tu veux la version 6.77 spécifiquement (celle qui importe encore gratuitement) :

1. **[Télécharge la version 6.77](/downloads/all-in-one-wp-migration.6.77.zip)** directement depuis ce site
2. **Dashboard WordPress** → **Extensions** → **Téléverser une extension**
3. **Sélectionne le fichier ZIP** et active le plugin

- - - - - -

## 2. Export de ton site source

Maintenant, on s'occupe de l'**ancien site** (celui que tu veux migrer). C'est parti pour l'export !

### Créer ta sauvegarde

1. **Va dans le plugin** → **Export**
2. **Clique sur « Export vers »** → **Fichier**
3. **Attends que l'export se termine** (ça peut prendre du temps selon la taille)
4. **Télécharge le fichier .wpress** généré

> 💡 **Astuce de pro :** Avant de faire ta migration directement en prod (et potentiellement tout péter), teste plutôt ton truc sur un [environnement WordPress local avec LocalWP](https://brandonvisca.com/installer-localwp-wordpress-local/). Tu éviteras les sueurs froides et tu pourras corriger les couacs tranquille.

### Options d'export avancées

Tu peux exclure certains éléments si besoin :

- **Révisions d'articles** (pour alléger)
- **Commentaires spam** (personne n'en veut)
- **Thèmes non utilisés**
- **Plugins désactivés**

- - - - - -

## 3. Import sur le nouveau site

On passe aux choses sérieuses : l'import sur ton nouveau serveur.

### Méthodes d'importation

**Méthode 1 : Upload direct** (sites < 512 MB)

- Le plugin → **Import**
- **Drag & Drop** ton fichier .wpress
- Attends et prie les dieux du web

**Méthode 2 : Via URL** (si tu as hébergé ton fichier)

- Upload ton .wpress sur ton hébergement
- Import → **Import depuis** → **URL**
- Colle l'URL de ton fichier

### Étapes d'importation détaillées

1. **Accède à l'interface Import du plugin**
2. **Sélectionne ton fichier .wpress** (ou colle l'URL)
3. **Lance l'importation** et va boire un café ☕
4. **Confirme l'import** quand le plugin te le demande

- - - - - -

## 4. Restauration et vérifications

Une fois l'import terminé, c'est pas fini ! Il faut restaurer et vérifier que tout fonctionne.

### Processus de restauration

1. **Le plugin** → **Sauvegardes**
2. **Sélectionne ta sauvegarde** récemment importée
3. **Clique sur « Restaurer »** et confirme

> ⚠️ **Attention** : Toutes les données actuelles du site seront remplacées par celles du fichier importé. Assure-toi d'avoir une sauvegarde récente avant de te lancer. Et si jamais ça part en vrille ou que ta base de données fait des siennes, on a un guide qui cartonne pour [réparer une base de données WordPress corrompue](https://brandonvisca.com/wordpress-2-solutions-pour-reparer-une-base-de-donnee-corrompu/).

### Checklist post-restauration

✅ **URLs et liens** : Vérifie que tout pointe bien  
✅ **Images et médias** : Check que tes photos s'affichent  
✅ **Formulaires** : Teste contact, newsletter, etc.  
✅ **Plugins** : Reactive les plugins désactivés  
✅ **Permaliens** : Va dans Réglages → Permaliens → Enregistrer

- - - - - -

## 5. Augmenter la limite de taille d'importation

Ton site fait plus de 512 MB ? (spoiler : c'est le cas de la plupart des sites) Il va falloir bidouiller un peu.

### Modification du fichier constants.php

J'utilise cette méthode sur tous mes projets clients depuis 2023. Elle fonctionne sur toutes les versions de WordPress récentes.

1. **Dashboard** → **Outils** → **Éditeur de fichiers d'extensions**
2. **Sélectionne All-in-One WP Migration** dans la liste
3. **Ouvre le fichier `constants.php`**
4. **Trouve cette ligne :**

```php
define( 'AI1WM_MAX_FILE_SIZE', 2 << 28 );
```

5. **Remplace-la par :**

```php
define( 'AI1WM_MAX_FILE_SIZE', 2 << 40 );
```

6. **Enregistre** et teste ton import

> 🚀 **Résultat :** Tu peux maintenant importer des fichiers jusqu'à **2 To** ! Largement de quoi voir venir.

Tu peux aussi définir une valeur fixe si tu préfères quelque chose de plus lisible :

```php
// =================
// = Max File Size =
// =================
define( 'AI1WM_MAX_FILE_SIZE', 34359738368 ); // 32 Go
```

- - - - - -

## 6. Version 6.77 : la dernière qui importe gratuitement

Petit point important : depuis la version 6.77, les développeurs ont retiré la fonction d'import gratuite des nouvelles versions. La raison ? Monétiser via leur extension payante.

### Comment garder l'import gratuit

1. **Utilise la version 6.77 maximum** → [Téléchargement direct ici](/downloads/all-in-one-wp-migration.6.77.zip)
2. **Désactive les mises à jour automatiques** du plugin (Extensions → cherche All-in-One → désactive les MAJ auto)
3. **Configure la limite dans constants.php** comme vu en section 5

- - - - - -

## Conclusion

All-in-One WP Migration reste LA référence pour migrer WordPress sans prise de tête. La clé : garde la v6.77, bloque les mises à jour auto, et ajuste la limite dans `constants.php`. Tu peux migrer n'importe quel site en moins d'une heure. Si tu bosses souvent avec WordPress, jette un œil au guide pour [réparer une base de données corrompue](https://brandonvisca.com/wordpress-2-solutions-pour-reparer-une-base-de-donnee-corrompu/). C'est le genre d'article qu'on est content d'avoir lu avant d'en avoir besoin.

## Pour aller plus loin

- [Installer WordPress en local avec LocalWP](https://brandonvisca.com/installer-localwp-wordpress-local/)
- [WordPress : réparer une base de données corrompue](https://brandonvisca.com/wordpress-2-solutions-pour-reparer-une-base-de-donnee-corrompu/)
- [Documentation officielle All-in-One WP Migration](https://help.servmask.com/knowledgebase/introduction/)

## Articles connexes

- [Réparer WordPress : 2 solutions pour une base de données corrompue](/wordpress-2-solutions-pour-reparer-une-base-de-donnee-corrompu/)
- [Importer un fichier PST dans Outlook 365 : 2 méthodes qui marchent (2026)](/import-pst-outlook-365-guide-complet/)
- [Ladybird Browser : Le navigateur web qui refuse de se soumettre à Google (et tant mieux)](/ladybird-browser-le-navigateur-web-qui-refuse-de-se-soumettre-a-google-et-tant-mieux/)
- [Pourquoi j&rsquo;ai quitté Google (et comment tu peux faire pareil en 2025)](/quitter-google-auto-hebergement/)
