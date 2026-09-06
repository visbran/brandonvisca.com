---
title: "Filtrage utilisateurs LDAP Snipe-IT : Guide pratique Active Directory 2025"
description: Guide avancé pour filtrer les utilisateurs LDAP dans Snipe-IT connecté à Active Directory. Filtres sécurisés, exclusions par OU, bonnes pratiques 2025.
pubDatetime: "2025-03-02T21:06:25+01:00"
author: Brandon Visca
tags:
  - sysadmin
  - linux
  - avance
  - ldap
  - active-directory
  - snipeit
featured: false
draft: false
focusKeyword: filtrage LDAP Snipe-IT
faqs:
  - question: "Erreur ldap_search(): Search: Bad search filter"
    answer: "La syntaxe du filtre LDAP est invalide. Vérifie les parenthèses, opérateurs (&, |, !), et attributs comme objectCategory, objectClass."
  - question: "Aucun utilisateur retourné après la synchronisation LDAP"
    answer: "Le filtre est correct mais trop restrictif. Teste avec un filtre plus large d'abord : (&(objectCategory=person)(objectClass=user))"
  - question: "Certains utilisateurs sont exclus alors qu'ils ne devraient pas l'être"
    answer: "Révise le filtre sur userAccountControl ou userPrincipalName. L'opérateur ! exclut, pas de demi-mesures."
---
> 💡 **TL;DR**
> - Filtrer les utilisateurs LDAP importés dans Snipe-IT depuis Active Directory
> - Filtres sécurisés et exclusions par OU pour ne synchroniser que les bons comptes
> - Cas d'usage avancés et bonnes pratiques 2025

- - - - - -

## Table des matières

Le filtrage utilisateurs LDAP Snipe-IT est crucial lors de l’intégration avec Active Directory.

L’intégration de Snipe-IT avec un annuaire LDAP permet d’automatiser la gestion des accès, mais il est essentiel de bien configurer les filtres LDAP pour exclure certaines unités organisationnelles (OU) ou utilisateurs spécifiques.

Pourquoi ? Parce qu’importer tous les comptes de votre annuaire, c’est la
garantie de créer un beau bazar dans votre ITAM.

## 1️⃣ Prérequis

Ce guide suppose une instance Snipe-IT déjà en place. Sinon, commencer par [l’installation de Snipe-IT sur Ubuntu](/installation-snipeit-ubuntu-guide-complet/).

Avant de commencer, assurez-vous d’avoir :

- Un serveur LDAP/Active Directory accessible depuis Snipe-IT.
- Les identifiants d’un compte ayant les permissions suffisantes pour interroger l’AD.
- Snipe-IT correctement configuré avec la connexion LDAP active.

## 2️⃣ Objectif du filtre LDAP

Un bon filtrage utilisateurs LDAP Snipe-IT vous permettra de :

- Synchroniser uniquement les **utilisateurs actifs**.
- **Exclure** les comptes désactivés.
- Ne récupérer que les utilisateurs appartenant à certains groupes.
- **Exclure les utilisateurs** dont l’adresse `userPrincipalName` se termine par un domaine spécifique (ex. `@exemple.ad`).

## 🔐 Bonnes pratiques de sécurité pour le filtrage LDAP

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

```
&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2))(!(ou=<em>Externe</em>))(memberOf=CN=IT-Assets,OU=GROUPS,DC=exemple,DC=ad)
```

## 3️⃣ Syntaxe du filtrage utilisateurs LDAP Snipe-IT

Voici un filtre LDAP fonctionnel pour Snipe-IT :

```
&(objectCategory=person)(objectClass=user)
(!(userAccountControl:1.2.840.113556.1.4.803:=2))
(!(userPrincipalName=*@exemple.ad))
(|(memberof=CN=Groupe1,OU=GROUPS,DC=exemple,DC=ad)
  (memberof=CN=Groupe2,OU=GROUPS,DC=exemple,DC=ad)
  (memberof=CN=Groupe3,OU=GROUPS,DC=exemple,DC=ad))

```

### 🔍 **Explication du filtre**

- &( … ) : Combine plusieurs conditions avec un **ET logique**.
- (objectCategory=person) : Sélectionne uniquement les utilisateurs et pas les groupes ou ordinateurs.
- (objectClass=user) : Garantit que seuls les comptes utilisateurs sont pris en compte.
- (!(userAccountControl:1.2.840.113556.1.4.803:=2)) : **Exclut les comptes désactivés**.
- (!(userPrincipalName=*@exemple.ad)) : **Exclut les utilisateurs dont l’UPN finit par `@exemple.ad`**.
- (|(memberof=CN=Groupe1,OU=GROUPS,DC=exemple,DC=ad)… ) : Ne synchronise que les utilisateurs appartenant à au moins un des groupes spécifiés.

## 4️⃣ Tester le filtre LDAP

Avant d’ajouter le filtre dans Snipe-IT, testez-le avec **[ldapsearch](https://docs.ldap.com/ldap-sdk/docs/tool-usages/ldapsearch.html)** sous Linux ou via l’outil LDAP Admin sous Windows.

### **Commande `ldapsearch` pour tester**

```bash
ldapsearch -x -h AD_SERVER -D "cn=Utilisateur,dc=exemple,dc=ad" -W -b "dc=exemple,dc=ad" \
  "(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2))(!(userPrincipalName=*@exemple.ad)))"

```

Si la requête retourne bien les utilisateurs attendus, vous pouvez la copier-coller dans Snipe-IT. Côté poste client, la même logique d’annuaire s’applique quand on veut [connecter des systèmes Ubuntu à Active Directory avec SSSD](/connecter-les-systemes-ubuntu-a-active-directory-en-utilisant-sssd/).

## 5️⃣ Configuration dans Snipe-IT

Le filtre n’est qu’une brique de l’intégration annuaire : la synchronisation planifiée et les notifications sont traitées dans la [configuration avancée de Snipe-IT](/configuration-avancee-snipeit-ldap-teams-automatisation/).

1. **Accédez à l’interface d’administration** de Snipe-IT.
2. Allez dans **Paramètres > LDAP**.
3. Ajoutez votre filtre LDAP dans le champ correspondant.
4. Enregistrez et **testez la connexion**.
5. Vérifiez que seuls les utilisateurs souhaités sont importés.

## 6️⃣ Problèmes fréquents et solutions

Ces erreurs de filtrage utilisateurs LDAP sont fréquentes lors de l’intégration
Snipe-IT avec Active Directory…

### ❌ **Erreur `ldap_search(): Search: Bad search filter`**

✔ **Solution** : Vérifiez la syntaxe du filtre. LDAP ne supporte pas `*` dans certains champs, notamment `userPrincipalName`. Testez le filtre avec `ldapsearch` avant de l’ajouter à Snipe-IT.

### ❌ **Aucun utilisateur retourné**

✔ **Solution** : Vérifiez que la Base DN dans Snipe-IT correspond bien à votre structure AD (`OU=Users,DC=exemple,DC=ad`).

### ❌ **Certains utilisateurs sont exclus alors qu’ils ne devraient pas l’être**

✔ **Solution** : Assurez-vous que les groupes mentionnés dans `memberof` sont corrects et que les utilisateurs en font bien partie.

## 7️⃣ Conclusion

Avec ce guide de filtrage utilisateurs LDAP, Snipe-IT ne synchronise que les
comptes pertinents de votre Active Directory tout en excluant ceux dont l’adresse `userPrincipalName` ne correspond pas aux critères définis. Cela améliore la sécurité et évite d’importer des comptes non pertinents. Avec cette configuration de filtrage utilisateurs LDAP Snipe-IT, vous maîtrisez parfaitement la synchronisation avec Active Directory.

**Besoin d’un ajustement spécifique ?** Testez d’abord avec `ldapsearch` pour éviter toute erreur avant d’appliquer les modifications à Snipe-IT ! 🚀
