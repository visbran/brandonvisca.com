---
title: "Migrer WordPress en 2025 : All-in-One WP Migration guide complet (+ astuces pro)"
pubDatetime: "2025-02-24T18:51:33+01:00"
author: Brandon Visca
description: "Migrez votre site WordPress facilement avec All-in-One WP Migration. Guide complet : installation, sauvegarde, restauration et optimisation avancée. Mét..."
tags:
  - linux
  - developpement
  - intermediaire
  - wordpress
  - migration
  - guide
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


- [1. Installation du plugin All-in-One WP Migration](#1-installation-du-plugin-all-in-one-wp-migration)
  - [Étapes d’installation](#etapes-dinstallation)
  - [Alternative : installation manuelle](#alternative-installation-manuelle)
- [2. Export de ton site source](#2-export-de-ton-site-source)
  - [Créer ta sauvegarde](#creer-ta-sauvegarde)
  - [Options d’export avancées](#options-dexport-avancees)
- [3. Import sur le nouveau site](#3-import-sur-le-nouveau-site)
  - [Méthodes d’importation](#methodes-dimportation)
  - [Étapes d’importation détaillées](#etapes-dimportation-detaillees)
- [4. Restauration et vérifications](#4-restauration-et-verifications)
  - [Processus de restauration](#processus-de-restauration)
  - [Checklist post-restauration](#checklist-post-restauration)
- [5. Augmenter la limite de taille d’importation](#5-augmenter-la-limite-de-taille-dimportation)
  - [Modification du fichier constants.php](#modification-du-fichier-constants-php)
- [6. Version 6.77 : La dernière qui importe gratuitement](#6-version-6-77-la-derniere-qui-importe-gratuitement)
  - [Comment garder l’import gratuit](#comment-garder-limport-gratuit)
  - [Configuration alternative](#configuration-alternative)
- [Optimisation post-migration](#optimisation-post-migration)
  - [Configuration serveur](#configuration-serveur)
  - [Checklist d’optimisation](#checklist-doptimisation)
- [Sécurité post-migration](#securite-post-migration)
  - [Mesures de sécurité immédiates](#mesures-de-securite-immediates)
- [Erreurs courantes et solutions](#erreurs-courantes-et-solutions)
  - [Problème : Import qui plante](#probleme-import-qui-plante)
  - [Problème : Site cassé après migration](#probleme-site-casse-apres-migration)
  - [Problème : Images qui ne s’affichent pas](#probleme-images-qui-ne-saffichent-pas)
- [Outils complémentaires recommandés](#outils-complementaires-recommandes)
  - [Pour les migrations complexes](#pour-les-migrations-complexes)
  - [Hébergeurs migration-friendly](#hebergeurs-migration-friendly)
- [Conclusion](#conclusion)
- [FAQ](#faq)
  - [Combien de temps prend une migration WordPress ?](#faq-question-1752691631962)
  - [All-in-One WP Migration est-il gratuit ? ](#faq-question-1752691647198)
  - [Que faire si la migration échoue ? ](#faq-question-1752691658343)
  - [Faut-il sauvegarder avant migration ? TOUJOURS.](#faq-question-1752691669734)
  - [Comment migrer un multisite WordPress ?](#faq-question-1752691688150)


![Illustration — Migrer WordPress en 2025](fusion-vid-ppap-bhecjdygjck6c-1.gif)Alors, tu dois migrer ton site WordPress et tu te demandes comment faire ça proprement sans tout péter ? Parfait, tu es au bon endroit ! La migration WordPress, c’est un peu comme déménager : si tu t’y prends mal, tu risques de casser la vaisselle.

**[All-in-One WP Migration](https://brandonvisca.com/wp-content/uploads/2025/10/all-in-one-wp-migration.6.77.zip)** est probablement le plugin le plus populaire pour cette mission. Et on va voir pourquoi : interface simple, processus quasi-automatique, et surtout… ça marche ! Dans ce guide, on va couvrir l’installation, l’export, l’import, et quelques astuces de baroudeur pour éviter les galères classiques.

💡 **Besoin d’un hébergement fiable pour ta migration ?**  
[O2Switch](https://www.o2switch.fr/) – Hébergeur français, support expert, migrations incluses

- - - - - -

1. Installation du plugin All-in-One WP Migration

Première étape : installer ce petit bijou sur ton **site de destination**. Ouais, pas sur l’ancien, sur le nouveau ! C’est logique mais on préfère le préciser.

### Étapes d’installation

1. **Accède à ton dashboard WordPress** (admin de ton nouveau site)
2. **Extensions** → **Ajouter une extension**
3. **Recherche « All-in-One WP Migration »** dans la barre de recherche
4. **Installe et active** le plugin

> ⚠️ **Point important :** Si tu as déjà une version plus récente installée, désactive-la avant d’activer la version 6.77. Les versions récentes ont supprimé la fonction d’import gratuite.

### Alternative : installation manuelle

Si tu veux la version 6.77 spécifiquement (celle qui importe encore gratuitement) :

1. **[Télécharge la version 6.77](https://brandonvisca.com/wp-content/uploads/2025/10/all-in-one-wp-migration.6.77.zip)** depuis l’archive WordPress
2. **Téléverser une extension** → Sélectionne le fichier ZIP
3. **Active** le plugin

- - - - - -

2. Export de ton site source

Maintenant, on s’occupe de l’**ancien site** (celui que tu veux migrer). C’est parti pour l’export !

### Créer ta sauvegarde

1. **Va dans All-in-One WP Migration** → **Export**
2. **Clique sur « Export vers »** → **Fichier**
3. **Attends que l’export se termine** (ça peut prendre du temps selon la taille)
4. **Télécharge le fichier .wpress** généré

> 💡 **Astuce de pro :** Avant de faire ta migration directement en prod (et potentiellement tout péter), teste plutôt ton truc sur un [environnement WordPress local avec LocalWP](https://brandonvisca.com/installer-localwp-wordpress-local/). Tu éviteras les sueurs froides et tu pourras corriger les couacs tranquille.

### Options d’export avancées

Tu peux exclure certains éléments si besoin :

- **Révisions d’articles** (pour alléger)
- **Commentaires spam** (personne n’en veut)
- **Thèmes non utilisés**
- **Plugins désactivés**

- - - - - -

3. Import sur le nouveau site

On passe aux choses sérieuses : l’import sur ton nouveau serveur.

### Méthodes d’importation

**Méthode 1 : Upload direct** (sites &lt; 2MB)

- All-in-One WP Migration → **Import**
- **Drag &amp; Drop** ton fichier .wpress
- Attends et prie les dieux du web

**Méthode 2 : Via URL** (si tu as hébergé ton fichier)

- Upload ton .wpress sur ton hébergement
- Import → **Import depuis** → **URL**
- Colle l’URL de ton fichier

### Étapes d’importation détaillées

1. **Accède au menu All-in-One WP Migration** → **Import**
2. **Sélectionne ton fichier .wpress** (ou colle l’URL)
3. **Lance l’importation** et va boire un café ☕
4. **Confirme l’import** quand le plugin te le demande

- - - - - -

4. Restauration et vérifications

Une fois l’import terminé, c’est pas fini ! Il faut restaurer et vérifier que tout fonctionne.

### Processus de restauration

1. **All-in-One WP Migration** → **Sauvegardes**
2. **Sélectionne ta sauvegarde** récemment importée
3. **Clique sur « Restaurer »** et confirme

> ⚠️ **Attention** : Toutes les données actuelles du site seront remplacées par celles du fichier importé. Assure-toi d’avoir une sauvegarde récente avant de te lancer. Et si jamais ça part en vrille ou que ta base de données fait des siennes, on a un guide qui cartonne pour [réparer une base de données WordPress corrompue](https://brandonvisca.com/wordpress-2-solutions-pour-reparer-une-base-de-donnee-corrompu/).

### Checklist post-restauration

✅ **URLs et liens** : Vérifie que tout pointe bien  
✅ **Images et médias** : Check que tes photos s’affichent  
✅ **Formulaires** : Teste contact, newsletter, etc.  
✅ **Plugins** : Reactive les plugins désactivés  
✅ **Permaliens** : Va dans Réglages → Permaliens → Enregistrer

- - - - - -

5. Augmenter la limite de taille d’importation

Ton site fait plus de 100MB ? (spoiler : c’est le cas de 99% des sites) Il va falloir bidouiller un peu.

### Modification du fichier constants.php

1. **Dashboard** → **Outils** → **Éditeur de fichiers d’extensions**
2. **Sélectionne All-in-One WP Migration**
3. **Ouvre le fichier `constants.php`**
4. **Trouve cette ligne :**

```bash
define( 'AI1WM_MAX_FILE_SIZE', 2 << 28 );

```

define( 'AI1WM_MAX_FILE_SIZE', 2 << 40 );


6. **Enregistre** et teste ton import

> 🚀 **Résultat :** Tu peux maintenant importer des fichiers jusqu’à **2 To** ! Largement de quoi voir venir.

- - - - - -

6. Version 6.77 : La dernière qui importe gratuitement

Petit point important : depuis la version 6.77, les développeurs ont retiré la fonction d’import gratuite des nouvelles versions.

### Comment garder l’import gratuit

Si tu veux garder cette fonctionnalité :

1. **Utilise la version 6.77 maximum**
2. **Désactive les mises à jour auto** du plugin
3. **Configure la limite dans constants.php** comme vu plus haut

### Configuration alternative

Tu peux aussi définir la limite directement dans `constants.php` :

```bash
// =================
// = Max File Size =
// =================
define( 'AI1WM_MAX_FILE_SIZE', 34359738368 ); // 32 Go

```
