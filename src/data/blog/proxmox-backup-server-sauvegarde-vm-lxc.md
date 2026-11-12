---
title: "Proxmox Backup Server : sauvegardes dédupliquées de tes VM et LXC"
description: Proxmox Backup Server déduplique et chiffre tes sauvegardes de VM et LXC. Installation, datastore, planification et restauration, guide complet.
pubDatetime: "2026-11-07T11:01:44+01:00"
modDatetime: "2026-11-06T08:00:00.000Z"
author: Brandon
tags:
  - homelab
  - sauvegarde
  - stockage
  - intermediaire
featured: false
draft: false
focusKeyword: proxmox backup server
faqs:
  - question: "Proxmox Backup Server consomme combien de RAM ?"
    answer: "Compte 4 Gio pour le système et les démons, plus environ 1 Gio par To de stockage de sauvegarde géré. En dessous, les jobs de garbage collection ralentissent fort."
  - question: "Peut-on sauvegarder vers PBS depuis plusieurs hôtes Proxmox VE ?"
    answer: "Oui, un seul PBS centralise les sauvegardes de tous tes nœuds Proxmox VE. C'est justement l'intérêt : un datastore partagé, une déduplication qui profite à tout le cluster."
  - question: "Que se passe-t-il si le disque du datastore PBS tombe en panne ?"
    answer: "Tu perds toutes tes sauvegardes dessus, donc ta seule copie de secours. PBS sait répliquer un datastore vers un second PBS ou vers S3 : configure-le avant d'en avoir besoin, pas après."
---
> 💡 **TL;DR**
> - Proxmox Backup Server centralise les sauvegardes de tes VM et LXC avec déduplication par blocs, incrémental au niveau bloc, et chiffrement client-side optionnel
> - Installation en 10 minutes via ISO dédiée ou paquet `proxmox-backup-server` sur Debian, connexion à Proxmox VE en 3 clics
> - Gratuit et open source, planification par jobs, vérification automatique et restauration fichier par fichier sans redémarrer la VM

## Proxmox Backup Server, la pièce qui manquait à ton homelab

Tu as un cluster Proxmox VE qui tourne bien, des VM et des LXC qui tiennent la route, et puis un jour un disque claque ou une mise à jour foire une conteneur. Tu te retournes vers tes sauvegardes et tu découvres qu'elles sont soit absentes, soit stockées en vrac sur un NFS sans dédup, soit si lentes à restaurer que tu rages pendant une heure. Chez moi, c'était exactement ce scénario avant que je migre vers **Proxmox Backup Server** (PBS).

PBS, c'est l'outil officiel de Proxmox Server Solutions GmbH pour centraliser et dédupliquer les sauvegardes de ton infra Proxmox VE. Pas un plugin, pas un hack avec `vzdump` et un script cron maison : un vrai serveur de sauvegarde avec son datastore, ses jobs planifiés, sa vérification d'intégrité et son chiffrement. Et il est gratuit, open source, sans fonctionnalité bridée derrière un abonnement.

## Table des matières

## Pourquoi PBS change la donne par rapport à vzdump seul

Proxmox VE sait déjà faire des sauvegardes basiques avec `vzdump`, en dumpant chaque VM ou LXC vers un stockage NFS, CIFS ou un disque local. Ça fonctionne, mais ça a trois défauts qui deviennent vite douloureux :

- **Pas de déduplication** : chaque sauvegarde complète réécrit la quasi-totalité des données, même si 95 % du disque n'a pas changé depuis la veille.
- **Pas d'incrémental réel** : tu es coincé entre des sauvegardes complètes qui bouffent l'espace et des sauvegardes différentielles fragiles.
- **Restauration lente** : récupérer un fichier isolé dans un dump complet veut dire restaurer toute la VM, puis monter le disque, puis chercher.

PBS résout les trois en travaillant au niveau du bloc. Chaque sauvegarde découpe les disques virtuels en chunks, calcule leur empreinte, et ne stocke que les chunks qu'il n'a jamais vus. Résultat : la première sauvegarde complète prend de la place, toutes les suivantes sont quasi instantanées et minuscules en delta réel, même si Proxmox VE affiche à chaque fois une sauvegarde « complète » côté utilisateur.

## Installation : ISO dédiée ou paquet sur Debian

Deux chemins officiels, selon que tu dédies une machine à PBS ou que tu l'ajoutes à un Debian existant.

### Option 1 : l'ISO officielle (recommandée)

Télécharge l'ISO hybride de Proxmox Backup Server depuis le site officiel, grave-la sur une clé USB, et boote dessus. L'installateur propose trois modes (graphique, console, terminal série) et gère pour toi le partitionnement en ext4, xfs ou ZFS, le réseau, et l'installation des paquets. C'est le chemin le plus simple si tu as une machine ou une VM dédiée.

### Option 2 : paquet sur un Debian existant

Si tu préfères greffer PBS sur un Debian déjà en place, configure le dépôt Proxmox puis installe le paquet minimal :

```bash
echo "deb http://download.proxmox.com/debian/pbs trixie pbs-no-subscription" > /etc/apt/sources.list.d/pbs.list
wget https://enterprise.proxmox.com/debian/proxmox-release-trixie.gpg -O /etc/apt/trusted.gpg.d/proxmox-release-trixie.gpg
apt update
apt install proxmox-backup-server -y
```

Ce paquet minimal conserve le kernel Debian existant. Si tu veux le support ZFS complet et le kernel Proxmox, installe plutôt la meta-package `proxmox-backup` à la place. Adapte le nom de la distribution dans le dépôt (`trixie`, `bookworm`...) à ta version de Debian.

⚠️ Après une installation fraîche, mets immédiatement à jour les paquets (`apt update && apt dist-upgrade`) avant de créer ton premier datastore. Les notes de version de chaque ISO insistent là-dessus.

### Configuration matérielle à prévoir

Pour un usage de production, compte un CPU 64 bits à 4 cœurs minimum, 4 Gio de RAM pour le système plus environ 1 Gio par To de stockage géré, et au moins 32 Gio pour le disque système, idéalement sur du RAID matériel à cache protégé par batterie ou sur du ZFS redondant (les deux ne se combinent pas : ZFS ne tolère pas un contrôleur RAID matériel en dessous). Pour le stockage des sauvegardes elles-mêmes, privilégie du SSD d'entreprise pour les IOPS aléatoires ; si tu restes sur des HDD, un device de métadonnées ZFS en miroir change vraiment la vie en performance.

## Créer le datastore

Une fois PBS installé, connecte-toi à son interface web sur `https://ip-du-serveur:8007`. Premier réflexe : créer un datastore, qui est l'équivalent d'un dossier de stockage dédié où PBS range ses chunks dédupliqués.

Dans **Datastore > Add Datastore**, donne-lui un nom, un chemin (idéalement un montage dédié, pas la racine du système), et laisse la case **GC Schedule** activée. La garbage collection (GC) est le processus qui nettoie périodiquement les chunks qui ne sont plus référencés par aucune sauvegarde : sans elle, ton datastore grossit indéfiniment même quand tu supprimes de vieilles sauvegardes.

```
Name: datastore-principal
Path: /mnt/pbs-storage
GC Schedule: daily
```

💡 Si tu as de la place sur plusieurs disques, PBS gère le stockage amovible et les volumes ZFS nativement : un deuxième datastore sur un disque externe fait une excellente copie froide, hors ligne la majorité du temps.

## Connecter Proxmox VE à PBS

Côté serveur Proxmox VE (le cluster qui héberge tes VM et LXC), va dans **Datacenter > Storage > Add > Proxmox Backup Server**. Renseigne l'adresse IP ou le nom d'hôte de ton serveur PBS, le nom du datastore créé précédemment, et les identifiants d'un utilisateur PBS dédié (ne pas utiliser `root@pam` pour ça, crée un utilisateur avec juste les droits `DatastoreBackup` et `DatastoreReader`).

Une fois le stockage ajouté, il apparaît directement dans la liste des cibles disponibles quand tu configures une sauvegarde sur une VM ou un LXC, exactement comme un NFS ou un disque local, sauf que celui-ci déduplique.

## Planifier les jobs de sauvegarde

Dans **Datacenter > Backup**, crée un job planifié qui cible soit un nœud entier, soit une sélection de VM et LXC. Les champs importants :

- **Storage** : le stockage PBS créé plus haut
- **Schedule** : l'heure et la fréquence, en syntaxe calendrier type `02:30` ou `mon..fri 03:00`
- **Retention** : combien de sauvegardes garder par jour, semaine, mois, année
- **Mode** : `snapshot` pour une sauvegarde à chaud sans coupure de service (recommandé pour les VM avec QEMU guest agent), `suspend` ou `stop` si le snapshot n'est pas supporté

La rétention mérite réflexion. PBS applique les règles `keep-daily`, `keep-weekly`, `keep-monthly` au moment du prune, qui tourne après chaque sauvegarde réussie ou sur un planning séparé. Une configuration raisonnable pour un homelab : 7 quotidiennes, 4 hebdomadaires, 6 mensuelles.

```
keep-daily: 7
keep-weekly: 4
keep-monthly: 6
```

## Chiffrement client-side : protéger même une cible non fiable

PBS propose un chiffrement AES-256 appliqué côté client, avant que les données quittent la machine sauvegardée. C'est pertinent si ton PBS tourne chez un tiers, sur un VPS loué, ou simplement si tu veux une couche de protection même en cas de compromission du serveur de sauvegarde lui-même.

Génère une clé de chiffrement depuis l'interface Proxmox VE ou en CLI, et attache-la au job de sauvegarde. Le point critique à retenir : **PBS ne peut pas déchiffrer tes données sans cette clé**. Si tu la perds, tes sauvegardes chiffrées sont inutilisables, point final. Sauvegarde cette clé ailleurs, sur un gestionnaire de mots de passe ou un support physique, pas uniquement sur la machine que tu sauvegardes.

✅ Le chiffrement n'empêche pas la déduplication : PBS déduplique les chunks chiffrés de la même façon que les chunks en clair, tant qu'ils proviennent de la même clé.

## Vérification et intégrité

Un job de sauvegarde qui réussit ne garantit pas que les données sont restaurables. PBS propose des **jobs de vérification** planifiables, qui relisent les chunks du datastore et comparent leurs empreintes pour détecter la corruption silencieuse (bit rot, erreur disque).

Configure-le dans **Datastore > Verify Jobs**, avec une fréquence hebdomadaire sur un homelab suffit largement. Si une vérification échoue sur une sauvegarde précise, PBS la marque et tu sais immédiatement laquelle re-faire plutôt que de le découvrir le jour où tu en as besoin.

## Restauration : fichier isolé ou VM complète

C'est là que PBS prend vraiment son sens par rapport à un dump brut. Depuis l'interface Proxmox VE, un clic sur une sauvegarde propose deux chemins :

1. **Restauration complète** : reconstruit la VM ou le LXC tel qu'il était, sur le même nœud ou un autre.
2. **File Restore** : monte la sauvegarde en lecture seule et te laisse naviguer dans l'arborescence du disque pour récupérer un fichier précis, sans toucher à la VM en production. Pratique quand quelqu'un a supprimé un fichier de config par erreur et que tu n'as aucune envie de restaurer toute la machine pour ça.

Le File Restore fonctionne aussi bien sur des disques ext4, xfs que sur des volumes LVM ou ZFS à l'intérieur de la VM sauvegardée, PBS sachant interpréter ces systèmes de fichiers directement depuis l'image dédupliquée.

## Réplication : ne pas mettre tous les œufs dans le même datastore

Un datastore PBS unique reste un point de défaillance unique. Si le serveur ou le disque qui l'héberge tombe, tu perds ta seule copie de secours en même temps que la donnée originale. PBS répond à ça avec des **jobs de synchronisation** (sync jobs), qui répliquent un datastore vers un second serveur PBS, local ou distant, y compris en mode push chiffré.

Pour une protection hors site, c'est aussi l'occasion de regarder du côté d'une destination cloud compatible S3 : le principe de synchroniser des blocs dédupliqués vers un stockage objet distant rejoint ce que je décris dans mon guide sur [S3cmd pour synchroniser et sauvegarder vers Amazon S3 gratuitement](/gerer-fichiers-amazon-s3-avec-s3cmd/), avec l'avantage que PBS gère nativement la dédup avant l'envoi plutôt que de synchroniser des fichiers bruts.

Pense aussi à ton plan de secours plus large : si tu sauvegardes des boîtes mail en plus de tes VM, j'ai un guide dédié sur [Vanderplanki pour la sauvegarde email gratuite et multi-plateforme](/vanderplanki-sauvegarde-emails-gratuit-multiplateforme/), complémentaire à PBS qui lui se concentre sur les disques virtuels.

## Namespaces : organiser un gros datastore

Si tu gères plusieurs clients, environnements, ou simplement beaucoup de VM, les **namespaces** de PBS permettent de cloisonner logiquement un même datastore physique. Chaque namespace a sa propre arborescence de sauvegardes, ses propres permissions, et peut être synchronisé indépendamment vers un autre PBS. C'est l'équivalent d'un sous-dossier avec droits d'accès dédiés, utile dès que plus d'une personne touche à l'infra.

## Gestion des bandes LTO : pour aller plus loin

PBS sait aussi piloter des lecteurs de bande LTO directement, avec gestion des pools de médias, inventaire automatique et restauration depuis bande. C'est clairement orienté vers un usage pro ou un gros homelab avec archivage à froid longue durée, pas le premier réflexe pour une infra de quelques VM. Mentionné ici pour que tu saches que l'option existe si ton volume de données grossit au point de justifier un support hors ligne durable.

## Cas d'usage concret : un cluster Proxmox VE à trois nœuds

Pour fixer les idées, voici une configuration typique que je recommande pour un homelab avec plusieurs nœuds Proxmox VE :

- Un PBS dédié sur une petite machine ou VM séparée, avec un datastore sur un volume ZFS redondant
- Un job de sauvegarde quotidien à 02h00 en mode `snapshot` sur l'ensemble des VM et LXC du cluster
- Rétention 7 quotidiennes / 4 hebdomadaires / 6 mensuelles
- Un job de vérification hebdomadaire le dimanche
- Un sync job mensuel vers un second datastore sur un NAS distant ou un stockage S3

Cette combinaison couvre l'essentiel : récupération rapide d'une erreur récente (quotidiennes), marge pour remonter plus loin dans le temps (mensuelles), et une copie hors site en cas de sinistre matériel complet.

Pendant que tu es dans la configuration réseau de ton infra, vérifie aussi que l'heure est bien synchronisée entre PBS et tes nœuds Proxmox VE : un décalage d'horloge fausse les timestamps de rétention et peut provoquer des purges inattendues. Mon guide sur [comment définir le fuseau horaire et synchroniser l'heure sous Linux](/comment-modifier-heure-du-serveur-sous-linux/) couvre exactement ce point.

## Limites à connaître avant de se lancer

PBS n'est pas magique sur tous les plans :

- **Pas de sauvegarde applicative fine** : PBS sauvegarde des disques virtuels entiers, pas des bases de données ligne par ligne. Pour une cohérence applicative parfaite (base SQL en particulier), combine-le avec un dump applicatif planifié en complément.
- **Dépendant du guest agent pour le mode snapshot propre** : sans QEMU guest agent installé dans la VM, le snapshot à chaud peut geler brièvement les IO, ce qui reste généralement sans conséquence mais vaut d'être su.
- **Un seul serveur = un seul point de défaillance** : déjà évoqué plus haut, mais ça vaut la répétition. Prévois une réplication dès le départ, pas après l'incident.

💡 À lire aussi : [Kopia Docker : sauvegardes chiffrées et dédupliquées avec interface web](/kopia-docker-sauvegarde-chiffree/), dans la même veine que cet article.

## Conclusion

Proxmox Backup Server transforme la sauvegarde de ton cluster d'une tâche redoutée en une routine presque invisible. La déduplication fait fondre l'espace disque utilisé, le chiffrement client-side rassure même sur une cible distante, et le File Restore évite de restaurer une VM complète pour un fichier oublié. Si ton homelab Proxmox VE tourne encore avec des dumps bruts sur un NFS, c'est probablement le prochain morceau d'infra à migrer. L'installation prend moins de temps que la lecture de cet article, et la tranquillité d'esprit qui suit vaut largement l'effort.
