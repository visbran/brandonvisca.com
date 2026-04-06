---
title: "Aller plus loin : Permissions-Policy et protection anti-bots sur Nginx"
pubDatetime: "2025-04-27T17:12:59+02:00"
description: "Découvrez comment renforcer la sécurité de vos applications web grâce aux politiques Permissions-Policy pour restreindre les API navigateur, et comment ..."
tags:
  - linux
  - securite
  - avance
  - nginx
  - guide
  - headers
---

-----------
## Table des matières


- [Objectif :](#objectif)
- [Exemple de configuration :](#exemple-de-configuration)
- [Explication :](#explication)
- [Pourquoi l’utiliser ?](#pourquoi-lutiliser)
- [Étape 1 : définir une zone de limitation](#etape-1-definir-une-zone-de-limitation)
- [Étape 2 : appliquer la règle](#etape-2-appliquer-la-regle)
- [Résultat :](#resultat)
- [Bonus : filtrer certains User-Agent](#bonus-filtrer-certains-user-agent)


### Introduction

Lorsque vous avez déjà mis en place les headers classiques (HSTS, CSP, X-Frame-Options…), il reste encore des moyens d’**affiner votre politique de sécurité**.

Deux approches particulièrement utiles :

1. **Les Permissions-Policy** : pour limiter ce que le navigateur est autorisé à faire (caméra, micro, géolocalisation…)
2. **Le Rate Limiting dans Nginx** : pour bloquer ou ralentir les requêtes abusives, souvent utilisées par des bots ou des scripts malveillants

Ces deux mesures combinées offrent un **contrôle plus précis du comportement client** et **protègent votre serveur contre les abus**.

- - - - - -

1. Permissions-Policy : contrôle des capacités navigateur
---------------------------------------------------------

Anciennement connue sous le nom de Feature-Policy, cette en-tête HTTP permet de **restreindre ou autoriser l’accès aux fonctionnalités sensibles du navigateur**, comme la caméra, le micro, la géolocalisation, etc.

### Objectif :

Empêcher les navigateurs d’accéder à des APIs si ce n’est pas nécessaire au bon fonctionnement du site.

- - - - - -

### Exemple de configuration :

```bash
add_header Permissions-Policy "geolocation=(), microphone=(), camera=(), fullscreen=(self), payment=()" always;

```

camera=(self "https://appli.externe.com")


- - - - - -

### Pourquoi l’utiliser ?

- Réduction des risques d’exploitation des APIs navigateur
- Moins de permissions = surface d’attaque plus faible
- Compatible avec les navigateurs modernes (Chrome, Edge, Firefox)
- Permet de **respecter les règles RGPD** en désactivant des fonctions sensibles

- - - - - -

2. Rate limiting avec Nginx : la protection anti-bots native
------------------------------------------------------------

Les attaques par force brute, les scans automatisés ou les abus de formulaire sont **des menaces constantes** pour les serveurs web. Heureusement, **Nginx dispose de modules intégrés** pour contrôler le débit par IP.

- - - - - -

### Étape 1 : définir une zone de limitation

```bash
limit_req_zone $binary_remote_addr zone=antibot:10m rate=10r/s;

```

location / {
    limit_req zone=antibot burst=20 nodelay;
}


- `burst=20` : permet une petite tolérance en pic
- `nodelay` : autorise le burst sans ralentissement

💡 Tu peux adapter cette règle pour les zones sensibles uniquement :

```bash
location /login {
    limit_req zone=antibot burst=5;
}

```

if ($http_user_agent ~* (HTTrack|wget|curl|scanner|sqlmap)) {
    return 403;
}


Et si tu veux aller plus loin :

- [fail2ban](https://www.fail2ban.org/wiki/index.php/Main_Page) pour bannir les IP
- [ModSecurity](https://www.modsecurity.org/) pour un WAF plus complet

- - - - - -

Exemple combiné : sécurité sur un endpoint de formulaire
--------------------------------------------------------

```bash
location /contact {
    limit_req zone=antibot burst=3;

    add_header Permissions-Policy "microphone=(), camera=(), payment=(), fullscreen=(self)" always;

    try_files $uri $uri/ /contact/index.php?$args;
}

```

