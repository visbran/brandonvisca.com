---
title: "Active Directory : Transfère des rôles FSMO"
pubDatetime: "2025-03-31T17:34:29+02:00"
author: Brandon Visca
description: Les rôles FSMO sont 5 fonctions importantes dans un réseau Windows. Un seul contrôleur de domaine peut avoir un ou plusieurs de ces rôles.
focusKeyword: "transfert rôles FSMO"
tags:
  - active-directory
  - windows-server
  - guide
  - sysadmin
  - avance
faqs:
  - question: "Peut-on transférer les rôles FSMO sans redémarrer le serveur ?"
    answer: "Oui. Le transfert FSMO via ntdsutil ou PowerShell s'effectue à chaud, sans redémarrage du contrôleur de domaine source ni cible."
  - question: "Que se passe-t-il si le DC portant les rôles FSMO tombe définitivement ?"
    answer: "Il faut alors procéder à une saisie forcée (seize) des rôles depuis ntdsutil. Cette opération est irréversible — l'ancien DC ne peut plus rejoindre le domaine ensuite."
  - question: "Combien de contrôleurs de domaine faut-il avant de redistribuer les rôles FSMO ?"
    answer: "Au minimum 2 DC. Microsoft recommande de répartir les 5 rôles sur 2 DC : PDC Emulator + RID Master + Infrastructure Master sur le DC principal, Schema Master + Domain Naming Master sur le second."
---


Les rôles FSMO sont 5 fonctions importantes dans un réseau Windows. Un seul contrôleur de domaine peut avoir un ou plusieurs de ces rôles. On peut déplacer ces rôles entre les contrôleurs de domaine de deux façons :

Pour plus de détails sur chaque rôle, consultez la [documentation Microsoft sur les rôles FSMO](https://learn.microsoft.com/fr-fr/windows-server/identity/ad-ds/plan/understanding-active-directory-operations-masters-roles).

1. Avec l’interface graphique de Windows Server
2. Avec la commande **ntdsutil**

Si le serveur qui a les rôles ne fonctionne plus, on doit forcer le transfert. On appelle ça un **seizing de rôles FSMO**. On utilise l’outil **ntdsutil** pour le faire.

**Exemple** : Le domaine « **brandonvisca.local** » a deux contrôleurs de domaine sous **Windows Server 201**6 : **AD1** et **AD2**. AD1 a tous les rôles mais ne fonctionne plus. Nous allons donc transférer les rôles à AD2.

## Table des matières

## Se connecter au contrôleur de domaine

Sur le serveur qui va recevoir les rôles, ouvrez une Invite de commandes et tapez :

```powershell
ntdsutil
roles
```


Puis, utilisez la commande « **connections** » pour vous connecter au contrôleur de domaine :

```powershell
connections
connect to serveur DC2
seize naming master
```

Confirmez en cliquant sur **Oui** .

Un résumé s’affiche pour vérifier que AD2 a bien le nouveau rôle.

## Transférer le rôle Maître RID

Pour le Maître RID (ou **RID master**), tapez :

```bash
seize RID master
seize PDC
seize schema master
seize infrastructure master
```

Après avoir transféré tous les rôles, tapez deux fois « **q** » pour quitter.
## Vérification

Pour vérifier que AD2 a bien tous les rôles, utilisez cette commande dans l’**Invite de commandes** (remplacez « brandonvisca.local » par votre nom de domaine) :

```bash
netdom query /domain:brandonvisca.local fsmo
```

## Articles connexes

- [Masquer des utilisateurs de la GAL Office 365 + Active Direc](/masquer-utilisateurs-gal-office365-active-directory/)
- [Connecter les systèmes Ubuntu à Active Directory en utilisan](/connecter-les-systemes-ubuntu-a-active-directory-en-utilisant-sssd/)
