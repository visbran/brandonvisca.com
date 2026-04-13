---
title: "Réparer WordPress : 2 solutions pour une base de données corrompue"
description: "Réparer WordPress après une corruption de base de données : 2 méthodes éprouvées, testées en prod, pour restaurer votre site en moins de 10 minutes."
pubDatetime: "2024-07-16T19:50:34+02:00"
modDatetime: "2026-04-13T00:00:00+01:00"
author: Brandon Visca
tags:
  - developpement
  - wordpress
  - mysql
  - avance
  - guide
featured: false
draft: false
focusKeyword: réparer wordpress
---
## Table des matières

Ton site WordPress affiche "Erreur lors de la connexion à la base de données" au pire moment. Pas de panique. Une base MySQL corrompue, ça arrive : crash serveur, mise à jour ratée, coupure de courant en pleine écriture.

J'ai eu le cas sur un site client en production : voilà les deux méthodes que j'utilise pour réparer WordPress rapidement.

> 💡 **TL;DR**
> - Une base de données corrompue = site inaccessible, pages blanches, erreurs SQL
> - Solution 1 : l'outil de réparation intégré WordPress (1 ligne dans `wp-config.php`)
> - Solution 2 : `REPAIR TABLE` via phpMyAdmin pour les cas résistants

## Identifier les symptômes

Avant de toucher quoi que ce soit, identifie ce que tu as vraiment :

- **"Erreur lors de la connexion à la base de données"** → mauvais credentials ou base corrompue
- **Page blanche** → erreur PHP ou table corrompue
- **"Une ou plusieurs tables de la base de données sont endommagées"** → WordPress te le dit clairement
- **Requêtes lentes, timeouts** → tables fragmentées

Si tu vois l'erreur de connexion, commence par vérifier tes credentials dans `wp-config.php` avant de partir sur une réparation. Ce serait bête de passer 20 minutes à réparer une base qui n'a rien.

## Solution 1 : l'outil de réparation intégré WordPress

WordPress embarque un outil de réparation natif, désactivé par défaut pour des raisons de sécurité. Une ligne suffit à l'activer.

Ouvre `wp-config.php` et ajoute ça avant la ligne `/* That's all, stop editing! */` :

```php
define('WP_ALLOW_REPAIR', true);
```

Ensuite, accède à cette URL dans ton navigateur :

```text
https://ton-site.com/wp-admin/maint/repair.php
```

Tu arrives sur une page avec deux options :

- **Réparer la base de données** : corrige les tables corrompues
- **Réparer et optimiser la base de données** : corrige + défragmente

Lance "Réparer et optimiser" si ton site est en production depuis un moment. Ça prend 1 à 2 minutes selon la taille de ta base.

> ⚠️ **Important** : une fois la réparation terminée, **supprime** la ligne `WP_ALLOW_REPAIR` de ton `wp-config.php`. Cette page est accessible sans authentification : n'importe qui peut lancer une réparation si tu laisses ça actif.

## Activer le mode débogage

Si l'outil intégré ne suffit pas ou que tu veux comprendre ce qui se passe exactement, active le débogage pour voir les erreurs SQL brutes.

Dans `wp-config.php` :

```php
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false);
```

Les erreurs s'écrivent dans `wp-content/debug.log`. Ouvre ce fichier : tu verras exactement quelle(s) table(s) pose(nt) problème.

Une fois le diagnostic fait, désactive `WP_DEBUG` avant de remettre le site en production.

## Solution 2 : réparer WordPress via phpMyAdmin

Si l'outil intégré échoue ou que tu préfères intervenir directement, phpMyAdmin te donne un accès direct aux tables MySQL.

1. Connecte-toi à phpMyAdmin (via ton panel d'hébergement ou directement sur `localhost/phpmyadmin`)
2. Sélectionne la base de données de ton WordPress
3. Coche les tables à réparer (ou tout sélectionner avec "Tout cocher")
4. Dans le menu déroulant en bas, choisis **"Réparer la table"**

phpMyAdmin va lancer `REPAIR TABLE` sur chaque table sélectionnée. Tu verras le statut ligne par ligne : `OK` si ça passe, un message d'erreur sinon.

En CLI MySQL, c'est équivalent à :

```sql
REPAIR TABLE wp_options;
REPAIR TABLE wp_posts;
```

Si une table retourne une erreur persistante, essaie `CHECK TABLE nom_table` pour un diagnostic plus fin avant de tenter une restauration.

## Restaurer une sauvegarde

Si les deux méthodes précédentes ne suffisent pas, la table est peut-être trop corrompue pour être réparée. C'est le moment de restaurer depuis une sauvegarde.

La procédure dépend de ton hébergement :

- **cPanel** : Backup Wizard ou Softaculous → restauration base de données
- **Plesk** : Gestionnaire de sauvegardes WordPress
- **VPS/serveur dédié** : `mysql -u user -p database < backup.sql`

Si tu n'as pas de sauvegarde... c'est la leçon la plus douloureuse de l'admin sys. La section suivante est pour toi.

> ✅ **Bonne pratique** : si tu anticipes une migration complète en même temps, le [guide All-in-One WP Migration](/migration-wordpress-all-in-one-guide-2025/) couvre le transfert base + fichiers de A à Z, avec les pièges à éviter.

## Prévenir les problèmes futurs

Une corruption de base ne s'anticipe pas, mais ses conséquences si.

**Sauvegardes automatiques :**

- Plugin [UpdraftPlus](https://wordpress.org/plugins/updraftplus/) pour des sauvegardes quotidiennes vers Dropbox, Google Drive ou S3
- Sauvegardes côté hébergeur en complément (pas à la place)

**Optimisation régulière :**

- Plugin WP-Optimize pour défragmenter les tables et purger les révisions
- `mysqlcheck --optimize --all-databases` en cron si tu gères ton serveur directement

**Surveille tes logs :**

Un crash MySQL laisse des traces dans `/var/log/mysql/error.log`. Vaut mieux le voir venir qu'attendre que le site tombe.

Et si tu veux tester des manipulations risquées sans toucher la prod, [LocalWP](/installer-localwp-wordpress-local/) te permet de monter un WordPress local en 5 minutes, idéal pour valider une procédure de restauration avant d'en avoir besoin pour de vrai.

## Conclusion

Pour réparer WordPress après une corruption de base, commence toujours par l'outil intégré : rapide, sans risque, ça règle 80% des cas. Si ça bloque, phpMyAdmin te donne un contrôle plus fin table par table.

Dans les deux cas : active le débogage pour comprendre ce qui se passe réellement, et pense à désactiver `WP_ALLOW_REPAIR` dès que c'est réparé. Et si t'as pas de sauvegardes, c'est le bon moment pour mettre UpdraftPlus en place.

## Articles connexes

- [LocalWP : Ton lab WordPress en 5 min (guide complet 2025 + migration prod)](/installer-localwp-wordpress-local/)
- [Migrer WordPress en 2025 : All-in-One WP Migration guide complet (+ astuces pro)](/migration-wordpress-all-in-one-guide-2025/)
