---
title: "NetBox Docker : la source de vérité de ton réseau (IPAM/DCIM)"
description: "NetBox Docker : installe l'IPAM/DCIM open source avec Docker Compose et fais-en la source de vérité unique de ton réseau et ton inventaire."
pubDatetime: "2026-11-21T11:00:55+01:00"
modDatetime: "2026-11-20T08:00:00.000Z"
author: Brandon
tags:
  - reseau
  - docker
  - automation
  - intermediaire
featured: false
draft: false
focusKeyword: netbox docker
faqs:
  - question: "NetBox est-il vraiment gratuit en self-hosted ?"
    answer: "Oui, l'édition communautaire est open source sous licence Apache 2.0, sans limite de devices ni d'utilisateurs. Les offres payantes ajoutent de l'hébergement managé et du support, pas des fonctionnalités cachées."
  - question: "Faut-il une grosse machine pour faire tourner NetBox en Docker ?"
    answer: "Non. Un conteneur NetBox avec PostgreSQL et Redis tient sur une petite VM avec 1 à 2 vCPU et 2 Go de RAM pour un homelab ou une PME. La charge grossit avec le nombre d'objets, pas avec le trafic réseau."
  - question: "Comment migrer mon inventaire existant (Excel, Visio) vers NetBox ?"
    answer: "Par l'API REST ou des scripts Python avec pynetbox : tu importes sites, devices et préfixes IP par lot plutôt qu'à la main, ce qui évite les erreurs de saisie sur des centaines de lignes."
---
> 💡 **TL;DR**
> - NetBox Docker documente ton réseau entier (sites, racks, devices, câbles, IP, VLAN) dans une base unique interrogeable par API
> - Déploiement via le dépôt officiel netbox-community/netbox-docker : `docker compose up -d`, accès sur le port 8000
> - Gratuit et open source (Apache 2.0), base PostgreSQL + Redis, devient vite la source de vérité pour ton automatisation réseau

## NetBox Docker : la source de vérité qui manquait à ton réseau

Tu as un fichier Excel qui recense tes VLAN. Un Visio périmé pour le plan de ton rack. Un fichier texte planqué dans un coin pour tes plages IP. Et évidemment, aucun des trois n'est à jour depuis six mois. Bon, on va pas se mentir, c'est le schéma classique de 90% des réseaux en PME et en homelab.

**NetBox** règle ce problème en centralisant tout ça dans une seule base de données, avec une interface web et une API REST. C'est devenu le standard de facto pour la documentation réseau et l'automatisation chez les gens qui gèrent plus de dix switchs. Et la bonne nouvelle, c'est que NetBox Docker se déploie en quelques minutes grâce au dépôt officiel maintenu par la communauté.

## Table des matières

## DCIM et IPAM : ce que NetBox documente vraiment

NetBox a été créé à l'origine par Jeremy Stretch pour les besoins internes de DigitalOcean, avant de devenir un projet open source à part entière. Le projet est aujourd'hui stewarded par **NetBox Labs**, qui vend des offres cloud et entreprise payantes, mais le cœur du logiciel reste sous licence **Apache 2.0** et entièrement gratuit en self-hosted, sans limite de devices.

NetBox repose sur deux modules principaux.

### DCIM : l'inventaire physique

Le module DCIM (Data Center Infrastructure Management) documente tout ce qui se touche :

- **Sites et locations** : datacenters, salles serveurs, étages de bureau
- **Racks** : position U, profondeur, fabricant
- **Devices** : serveurs, switchs, routeurs, firewalls, avec leur modèle exact
- **Câbles et ports** : qui est branché où, physiquement
- **Alimentation** : PDU, circuits électriques, consommation

### IPAM : la gestion d'adresses IP

Le module IPAM (IP Address Management) suit tout ce qui ne se touche pas :

- **Préfixes et agrégats** : tes plages IP, publiques et privées
- **Adresses IP** : attribuées, réservées, libres
- **VLAN** : identifiants, descriptions, sites associés
- **VRF** : séparation logique des tables de routage
- **ASN** : pour ceux qui font du BGP, même en interne

La force de NetBox, c'est que DCIM et IPAM sont liés. Une IP n'est pas juste une ligne dans un tableau, elle est rattachée à une interface, qui est rattachée à un device, qui est rattaché à un rack, qui est rattaché à un site. Tu casses une seule brique, tu remontes toute la chaîne pour comprendre l'impact.

## Installer NetBox avec Docker Compose

Oublie l'installation native avec son virtualenv Python, sa configuration PostgreSQL à la main et ses dépendances système. Le dépôt officiel **netbox-community/netbox-docker** fournit tout ce qu'il faut pour un déploiement NetBox Docker propre, isolé, et reproductible d'une machine à l'autre.

### Prérequis

Avant de lancer quoi que ce soit, vérifie que tu as :

- Docker 20.10.10 minimum et Docker Compose 1.28.0 minimum
- Au moins 2 Go de RAM disponibles (NetBox + PostgreSQL + Redis + Redis Cache tournent en parallèle)
- Un port 8000 libre, ou prévu pour être redirigé derrière un reverse proxy

Si tu débutes avec les conteneurs, mon article sur [Gluetun Docker](/gluetun-docker-vpn-conteneurs/) couvre déjà les bases du réseau Docker que tu vas retrouver ici, notamment la gestion des volumes persistants.

### Cloner le dépôt et lancer les conteneurs

```bash
git clone -b release https://github.com/netbox-community/netbox-docker.git
cd netbox-docker
cp docker-compose.override.yml.example docker-compose.override.yml
docker compose pull
docker compose up -d
```

Le premier démarrage prend quelques minutes : NetBox applique ses migrations de base de données et collecte ses fichiers statiques. Surveille les logs avec :

```bash
docker compose logs -f netbox
```

Une fois le message indiquant que le serveur écoute apparaît, NetBox Docker est accessible sur `http://ton-ip:8000/`.

### Créer ton compte administrateur

Deux options pour le compte admin. La manuelle, à chaque fois :

```bash
docker compose exec netbox /opt/netbox/netbox/manage.py createsuperuser
```

Ou l'automatique, en définissant les variables dans `docker-compose.override.yml` pour que le compte soit créé dès le premier lancement, pratique si tu reconstruis ton environnement de test souvent :

```yaml
services:
  netbox:
    environment:
      SUPERUSER_NAME: admin
      SUPERUSER_EMAIL: admin@tondomaine.local
      SUPERUSER_PASSWORD: change-moi-immediatement
```

> ⚠️ **Important** : ces variables ne créent le compte qu'au premier lancement, sur une base vide. Si tu changes le mot de passe après coup, ça ne touchera pas un compte déjà existant.

## Premiers pas : sites, devices, IP et VLAN

Une fois connecté, résiste à l'envie de tout remplir d'un coup. L'ordre logique qui évite de tout reprendre depuis le début :

1. Crée un **site** (ton datacenter, ta salle serveur, ton appartement si c'est un homelab)
2. Ajoute les **racks** si tu veux du détail physique, sinon passe directement aux devices
3. Déclare tes **device types** (modèle de switch, de serveur) une seule fois, réutilisables ensuite
4. Crée les **devices** réels et rattache-les à leur rack et leur site
5. Attribue les **interfaces** sur chaque device
6. Crée tes **préfixes IP** et tes **VLAN**, puis assigne les adresses aux interfaces

Cette hiérarchie, c'est ce qui fait que NetBox n'est pas juste un tableur glorifié. Un switch que tu documentes correctement te permet ensuite de savoir en deux clics quelle IP est câblée sur quel port, dans quelle salle, sur quel circuit électrique.

💡 Si tu héberges déjà des services réseau comme un serveur DNS avec [Unbound](/unbound-docker-dns-recursif/) ou un bloqueur de pub [Pi-hole](/pihole-v6-docker-bloqueur-pubs-reseau/), c'est le moment de les ajouter comme devices virtuels dans NetBox, avec leurs IP réservées. Tu sauras toujours où chercher en cas de conflit d'adresse.

## Documenter un réseau existant sans tout casser

Le vrai défi, c'est rarement l'installation. C'est de faire rentrer un réseau qui existe déjà depuis des années dans NetBox sans y passer trois semaines à temps plein.

Quelques règles qui m'ont fait gagner du temps :

- **Commence par l'IPAM, pas le DCIM.** Importer tes plages IP et tes VLAN est plus rapide que de redessiner chaque rack, et ça donne déjà de la valeur immédiatement : plus de conflit d'adressage surprise.
- **Importe par lot, pas device par device.** NetBox accepte des imports CSV directement depuis l'interface pour les sites, devices, préfixes et IP. Prépare un fichier plutôt que de cliquer cinquante fois.
- **Utilise l'API pour les gros volumes.** Avec `pynetbox`, un script Python de trente lignes qui boucle sur ton inventaire existant (export d'un switch core, fichier Excel, whatever) va plus vite que n'importe quel import manuel.
- **Tolère l'incomplet au début.** Une IP sans description vaut mieux qu'une IP absente. Tu enrichiras les fiches plus tard, l'important c'est d'avoir une base de départ fiable.

✅ **Astuce** : NetBox propose un module "Change Logging" qui trace chaque modification avec l'utilisateur et la date. Si plusieurs personnes alimentent la base en même temps, tu sauras toujours qui a touché quoi, utile le jour où une IP attribuée deux fois casse un service en production.

## Connecter NetBox à ton automatisation réseau

C'est là que NetBox Docker arrête d'être une simple documentation et devient un vrai outil d'infra. Deux intégrations reviennent tout le temps.

**Ansible dynamic inventory.** La collection officielle `netbox.netbox` interroge l'API NetBox pour générer ton inventaire Ansible à la volée. Plus de fichier `hosts` à maintenir à la main : tu ajoutes un device dans NetBox, il apparaît dans ton prochain playbook.

**Terraform / scripts custom.** Le provider NetBox pour Terraform permet de déclarer tes ressources réseau en IaC et de les synchroniser avec NetBox comme état de référence. Pour des besoins plus spécifiques, l'API REST et GraphQL couvrent à peu près tout ce que l'interface web permet de faire à la main.

NetBox expose aussi des **webhooks** : chaque création, modification ou suppression d'objet peut déclencher un appel HTTP vers un système tiers. Pratique pour notifier un chat d'équipe, synchroniser un outil de ticketing, ou déclencher un pipeline de configuration automatique dès qu'un device change de statut.

Si tu gères aussi des tunnels ou du VPN mesh entre tes sites, documenter l'architecture dans NetBox avant de la déployer avec un outil comme [Headscale](/headscale-docker-tailscale-self-hosted/) t'évite de réinventer ton plan d'adressage à chaque nouveau site.

## Sauvegarder, sécuriser et dépanner ton instance

**Sauvegarde.** Toute la donnée qui compte vit dans PostgreSQL. Un simple `pg_dump` planifié suffit :

```bash
docker compose exec postgres sh -c 'pg_dump -U netbox netbox' > netbox-backup.sql
```

Pense aussi au volume des fichiers média (images, pièces jointes de devices) si tu en uploades.

**Sécurité.** NetBox Docker n'est pas pensé pour être exposé directement sur internet sur le port 8000. Mets un reverse proxy devant, avec HTTPS, comme je le détaille dans mon article sur [Cloudflare Tunnel](/cloudflare-tunnel-docker-homelab/) si tu veux l'exposer sans ouvrir de port chez toi. Change aussi la valeur par défaut d'`ALLOWED_HOSTS` dans ta configuration pour qu'elle corresponde à ton nom de domaine réel.

**Dépannage courant :**

| Symptôme | Cause probable | Solution |
|---|---|---|
| 502 Bad Gateway derrière un reverse proxy | NetBox pas encore prêt | Attends la fin des migrations, vérifie `docker compose logs netbox` |
| Erreur `ALLOWED_HOSTS` | Nom de domaine non déclaré | Ajoute ton domaine dans la variable `ALLOWED_HOSTS` |
| Compte admin introuvable | Variables SUPERUSER ignorées | Elles ne s'appliquent qu'au premier lancement sur base vide |
| Lenteur à l'interface | Redis cache absent ou mal configuré | Vérifie que les services `redis` et `redis-cache` tournent bien |
| Import CSV qui échoue | Colonnes mal nommées | Télécharge le gabarit CSV proposé par l'interface avant de remplir |

Pour garder une horloge cohérente entre NetBox et le reste de ton infra, notamment pour que les dates du Change Logging soient fiables, un serveur NTP correctement synchronisé comme [Chrony](/chrony-docker-serveur-ntp-homelab/) évite les décalages agaçants dans les historiques.

## Conclusion

NetBox Docker n'est pas magique : il ne découvre pas ton réseau à ta place, tu dois quand même rentrer la donnée. Mais une fois que c'est fait, tu passes d'un tas de fichiers épars et jamais à jour à une base unique, interrogeable, versionnée dans son historique, et branchable à n'importe quel outil d'automatisation.

Le vrai gain arrive après quelques semaines d'usage : quand tu cherches une IP libre, quand tu dois justifier un câblage, quand un nouveau dans l'équipe doit comprendre l'architecture sans te déranger. À ce moment-là, NetBox Docker devient la source de vérité que ton réseau aurait dû avoir depuis le début.

Mon conseil : commence petit. Un site, quelques devices, tes plages IP principales. Tu étofferas au fil de l'eau, et tu ne reviendras jamais à Excel.
