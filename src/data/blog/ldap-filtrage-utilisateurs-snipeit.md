---
title: "Filtrage utilisateurs LDAP Snipe-IT : Guide pratique Active Directory 2025"
pubDatetime: "2025-03-02T21:06:25+01:00"
description: "Guide avancé pour filtrer les utilisateurs LDAP dans Snipe-IT connecté à Active Directory. Filtres sécurisés, exclusions par OU, bonnes pratiques 2025."
tags:
  - autres
---

--------
## Table des matières


- [1️⃣ Prérequis](#1-%EF%B8%8F-prerequis)
- [2️⃣ Objectif du filtre LDAP](#2-%EF%B8%8F-objectif-du-filtre-ldap)
- [🔐 Bonnes pratiques de sécurité pour le filtrage LDAP](#%F0%9F%94%90-bonnes-pratiques-de-securite-pour-le-filtrage-ldap)
  - [Cas d’usage avancés du filtrage LDAP](#cas-dusage-avances-du-filtrage-ldap)
- [3️⃣ Syntaxe du filtrage utilisateurs LDAP Snipe-IT](#3-%EF%B8%8F-syntaxe-du-filtre-ldap)
  - [🔍 Explication du filtre](#%F0%9F%94%8D-explication-du-filtre)
- [4️⃣ Tester le filtre LDAP](#4-%EF%B8%8F-tester-le-filtre-ldap)
  - [Commande ldapsearch pour tester](#commande-ldapsearch-pour-tester)
- [5️⃣ Configuration dans Snipe-IT](#5-%EF%B8%8F-configuration-dans-snipe-it)
- [6️⃣ Problèmes fréquents et solutions](#6-%EF%B8%8F-problemes-frequents-et-solutions)
  - [❌ Erreur ldap\_search(): Search: Bad search filter](#faq-question-1753108122614)
  - [❌ Aucun utilisateur retourné](#faq-question-1753108142726)
  - [❌ Certains utilisateurs sont exclus alors qu’ils ne devraient pas l’être](#faq-question-1753108163800)
- [7️⃣ Conclusion](#7-%EF%B8%8F-conclusion)

------------

Le filtrage utilisateurs LDAP Snipe-IT est crucial lors de l’intégration avec Active Directory.

L’intégration de Snipe-IT avec un annuaire LDAP permet d’automatiser la gestion des accès, mais il est essentiel de bien configurer les filtres LDAP pour exclure certaines unités organisationnelles (OU) ou utilisateurs spécifiques.

Pourquoi ? Parce qu’importer tous les comptes de votre annuaire, c’est la  
garantie de créer un beau bazar dans votre ITAM.

1️⃣ Prérequis
-------------

Avant de commencer, assurez-vous d’avoir :

- Un serveur LDAP/Active Directory accessible depuis Snipe-IT.
- Les identifiants d’un compte ayant les permissions suffisantes pour interroger l’AD.
- Snipe-IT correctement configuré avec la connexion LDAP active.

2️⃣ Objectif du filtre LDAP
---------------------------

Un bon filtrage utilisateurs LDAP Snipe-IT vous permettra de :

- Synchroniser uniquement les **utilisateurs actifs**.
- **Exclure** les comptes désactivés.
- Ne récupérer que les utilisateurs appartenant à certains groupes.
- **Exclure les utilisateurs** dont l’adresse `userPrincipalName` se termine par un domaine spécifique (ex. `@exemple.ad`).

🔐 Bonnes pratiques de sécurité pour le filtrage LDAP
----------------------------------------------------

Le filtrage utilisateurs LDAP Snipe-IT ne se limite pas à exclure des comptes. C’est aussi une question de sécurité cruciale pour votre infrastructure.

**Erreurs de sécurité courantes :**

- Utiliser un compte administrateur pour la liaison LDAP (gros risque !)
- Ne pas tester les filtres avant la mise en production
- Oublier de monitorer les logs de synchronisation

**Recommandations expertes :**

- Créez un compte de service dédié avec permissions minimales
- Testez toujours vos filtres avec `ldapsearch` avant application
- Activez les logs détaillés pendant la phase de test
- Documentez vos filtres pour faciliter la maintenance

### **Cas d’usage avancés du filtrage LDAP**

Voici des exemples concrets de filtrage utilisateurs LDAP Snipe-IT :

```bash
&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2))(!(ou=<em>Externe</em>))(memberOf=CN=IT-Assets,OU=GROUPS,DC=exemple,DC=ad)
```

&(objectCategory=person)(objectClass=user)
(!(userAccountControl:1.2.840.113556.1.4.803:=2))
(!(userPrincipalName=*@exemple.ad))
(|(memberof=CN=Groupe1,OU=GROUPS,DC=exemple,DC=ad)
  (memberof=CN=Groupe2,OU=GROUPS,DC=exemple,DC=ad)
  (memberof=CN=Groupe3,OU=GROUPS,DC=exemple,DC=ad))


### 🔍 **Explication du filtre**

- &( … ) : Combine plusieurs conditions avec un **ET logique**.
- (objectCategory=person) : Sélectionne uniquement les utilisateurs et pas les groupes ou ordinateurs.
- (objectClass=user) : Garantit que seuls les comptes utilisateurs sont pris en compte.
- (!(userAccountControl:1.2.840.113556.1.4.803:=2)) : **Exclut les comptes désactivés**.
- (!(userPrincipalName=\*@exemple.ad)) : **Exclut les utilisateurs dont l’UPN finit par `@exemple.ad`**.
- (|(memberof=CN=Groupe1,OU=GROUPS,DC=exemple,DC=ad)… ) : Ne synchronise que les utilisateurs appartenant à au moins un des groupes spécifiés.

4️⃣ Tester le filtre LDAP
-------------------------

Avant d’ajouter le filtre dans Snipe-IT, testez-le avec **[ldapsearch](https://docs.ldap.com/ldap-sdk/docs/tool-usages/ldapsearch.html)** sous Linux ou via l’outil LDAP Admin sous Windows.

### **Commande `<a href="https://cyberinstitut.fr/utiliser-ldapsearch-guide-debutants/">ldapsearch</a>` pour tester**

```bash
ldapsearch -x -h AD_SERVER -D "cn=Utilisateur,dc=exemple,dc=ad" -W -b "dc=exemple,dc=ad" \
  "(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2))(!(userPrincipalName=*@exemple.ad)))"

```

