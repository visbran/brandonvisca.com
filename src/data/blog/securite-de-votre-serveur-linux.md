---
title: "Sécurité de votre serveur linux : Comment durcir un serveur sous linux ?"
pubDatetime: "2024-06-10T19:29:00+02:00"
description: "Dans ce guide pratique où nous allons renforcer ensemble la sécurité de votre serveur Linux. De l'installation de votre système à l'application des dern..."
tags:
  - linux
  - securite
  - avance
  - sysadmin
  - guide
  - hardening
faqs:
  - question: "Qu'est-ce que le durcissement d'un serveur sous Linux ?"
    answer: "C'est l'ensemble des mesures de sécurité appliquées à un serveur pour minimiser les vulnérabilités : SSH durci, firewall, fail2ban, sysctl renforcés."
  - question: "Comment désactiver la connexion SSH en tant que root et modifier le port ?"
    answer: "Édite /etc/ssh/sshd_config : définis PermitRootLogin no et change le port 22 par un numéro personnalisé."
  - question: "Comment limiter l'accès à su uniquement au groupe admin ?"
    answer: "Crée un groupe admin et utilise dpkg-statoverride pour restreindre l'accès à /bin/su uniquement à ce groupe."
  - question: "Qu'est-ce que DenyHosts et Fail2Ban ?"
    answer: "DenyHosts et Fail2Ban sont des outils qui analysent les logs et bannissent automatiquement les IPs des attaques SSH et autres tentatives malveillantes."
---

Dans ce guide pratique où nous allons renforcer ensemble la sécurité de votre serveur Linux. De l’installation de votre système à l’application des dernières mesures de sécurité, nous allons passer par toutes les étapes nécessaires pour rendre votre serveur aussi sûr que possible.

  
Assurez-vous de dimensionner en fonction des ressources disponibles, du nombre d’utilisateurs susceptibles de se connecter et de la taille des adhésions aux groupes.

Cette optimisation s’inscrit dans une démarche plus globale de gestion des ressources système — au même titre que la [configuration du swap Linux](https://brandonvisca.com/guide-swap-linux-configuration-optimisation/) qui permet d’éviter les dysfonctionnements en cas de saturation mémoire.

---

## Table des matières

Sommaire :
---
