---
title: Connecter les systèmes Ubuntu à Active Directory en utilisant SSSD
pubDatetime: "2024-06-13T11:40:02+02:00"
description: Apprenez à connecter les systèmes Ubuntu à Active Directory en utilisant SSSD pour une authentification centralisée et une gestion des utilisateurs. Sui...
tags:
  - linux
  - sysadmin
  - avance
  - active-directory
  - ubuntu
  - guide
faqs:
  - question: "Comment dépanner les problèmes de SSSD ?"
    answer: "Vérifie systemctl status sssd et journalctl -u sssd pour les erreurs. Les problèmes courants : DNS mal configuré, certificats Kerberos, ou permissions."
  - question: "Puis-je utiliser SSSD avec d'autres distributions Linux ?"
    answer: "Oui, SSSD est compatible avec Debian, RedHat, CentOS. Les commandes d'installation diffèrent légèrement."
  - question: "Comment assurer la création des répertoires personnels pour les utilisateurs AD ?"
    answer: "Configure oddjob-mkhomedir avec pam-auth-update --enable mkhomedir pour créer automatiquement les home dirs à la première connexion."
---

Introduction
============

L’intégration des systèmes Ubuntu à Windows Active Directory (AD) peut simplifier l’authentification des utilisateurs et la gestion des identités sur un réseau. Ce guide détaille comment utiliser le System Security Services Daemon (SSSD) pour connecter efficacement les hôtes Linux à un domaine Active Directory.

---

## Table des matières

