---
title: "Filtrage utilisateurs LDAP Snipe-IT : Guide pratique Active Directory 2025"
pubDatetime: "2025-03-02T21:06:25+01:00"
description: "Guide avancé pour filtrer les utilisateurs LDAP dans Snipe-IT connecté à Active Directory. Filtres sécurisés, exclusions par OU, bonnes pratiques 2025."
tags:
  - sysadmin
  - linux
  - avance
  - ldap
  - active-directory
  - snipeit
faqs:
  - question: "Erreur ldap_search(): Search: Bad search filter"
    answer: "La syntaxe du filtre LDAP est invalide. Vérifie les parenthèses, opérateurs (&, |, !), et attributs comme objectCategory, objectClass."
  - question: "Aucun utilisateur retourné après la synchronisation LDAP"
    answer: "Le filtre est correct mais trop restrictif. Teste avec un filtre plus large d'abord : (&(objectCategory=person)(objectClass=user))"
  - question: "Certains utilisateurs sont exclus alors qu'ils ne devraient pas l'être"
    answer: "Révise le filtre sur userAccountControl ou userPrincipalName. L'opérateur ! exclut, pas de demi-mesures."
---

---

## Table des matières

