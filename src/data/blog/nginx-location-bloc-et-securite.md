---
title: Comprendre les blocs location de Nginx et leur impact sur la sécurité
pubDatetime: "2025-04-15T20:25:29+02:00"
description: "Découvrez le fonctionnement des blocs location dans Nginx, leurs types, la gestion des priorités, et les implications en matière de sécurité et de bonne..."
tags:
  - nginx
  - securite
  - location-bloc
  - configuration
  - linux
  - web-server
  - tutoriel
  - avance
---

--------
## Table des matières


- [Qu’est-ce qu’un bloc location dans Nginx ?](#quest-ce-quun-bloc-location-dans-nginx)
- [Les différents types de blocs location](#les-differents-types-de-blocs-location)
  - [1. location = /chemin](#1-location-chemin)
  - [2. location /chemin/](#2-location-chemin)
  - [3. location ^~ /chemin](#3-location-chemin)
  - [4. location ~ pattern](#4-location-pattern)
  - [5. location ~\* pattern](#5-location-pattern)
- [Priorité des blocs location](#priorite-des-blocs-location)
- [Exemples d’utilisation avancée](#exemples-dutilisation-avancee)
  - [Mutualiser plusieurs utilisateurs avec une regex](#mutualiser-plusieurs-utilisateurs-avec-une-regex)
  - [Séparer les extensions](#separer-les-extensions)
- [Erreurs fréquentes à éviter](#erreurs-frequentes-a-eviter)
  - [❌ Mauvaise priorité](#%E2%9D%8C-mauvaise-priorite)
  - [❌ Mauvais usage de alias vs root](#%E2%9D%8C-mauvais-usage-de-alias-vs-root)
- [Bonnes pratiques](#bonnes-pratiques)
- [Sécurité : ce que les blocs location peuvent protéger](#securite-ce-que-les-blocs-location-peuvent-proteger)
- [En résumé](#en-resume)
- [Ressources complémentaires](#ressources-complementaires)

------------

Le serveur web **Nginx** est reconnu pour sa performance et sa flexibilité. L’une de ses fonctionnalités clés est la directive location, qui permet de définir le comportement à adopter pour une URL ou un ensemble d’URL.

Bien utilisée, cette directive permet d’organiser proprement ses routes, d’améliorer la sécurité, et de simplifier la maintenance du serveur. Mal utilisée, elle peut introduire des failles de sécurité, provoquer des conflits entre règles, ou casser certaines fonctionnalités.

Dans cet article, nous allons explorer :

- Les différents types de blocs location
- La priorité d’évaluation
- Les expressions régulières et leur usage
- Les erreurs fréquentes
- Les bonnes pratiques à adopter

- - - - - -

Qu’est-ce qu’un bloc location dans Nginx ?
------------------------------------------

Un bloc location permet de définir un **comportement spécifique pour une requête HTTP en fonction de son URI**. Il est souvent utilisé pour :

- Servir des fichiers statiques
- Rediriger vers un script PHP
- Appliquer des règles de sécurité ou des headers
- Déléguer à un proxy (ex: PHP-FPM, Node.js, etc.)

Exemple de base :

```bash
location /images/ {
    root /var/www/html;
}

```

location = /login {
    return 301 https://secure.monsite.com/login;
}


### 2. location /chemin/

- Correspondance **préfixée**
- Le plus **général**
- Priorité **inférieure** aux autres

```bash
location /admin/ {
    auth_basic "Espace restreint";
}

```

location ^~ /static/ {
    root /var/www/assets;
}


### 4. location ~ pattern

- Expression régulière sensible à la **casse**
- Exemple :

```bash
location ~ \.php$ {
    include fastcgi_params;
    ...
}

```

location ~* \.(jpg|jpeg|png|gif|ico)$ {
    expires 7d;
    access_log off;
}


- - - - - -

Priorité des blocs location
---------------------------

Voici **l’ordre d’évaluation** des blocs location :

1. `location = /uri` (exact)
2. `location ^~ /prefix`
3. `location ~ /regex` ou `~*`
4. `location /prefix` (générique)

Nginx applique le **premier bloc qui correspond** dans l’ordre ci-dessus.

Cela signifie que si plusieurs location peuvent correspondre à une requête, **le bloc exact ou prioritaire sera appliqué** même si une regex plus spécifique pourrait convenir.

- - - - - -

Exemples d’utilisation avancée
------------------------------

### Mutualiser plusieurs utilisateurs avec une regex

Imaginons un site éducatif avec un sous-dossier par utilisateur : /tamere, /tonpere, /tasoeur, etc.

Plutôt que de créer un bloc pour chacun, on utilise :

```bash
location ~ ^/([a-z0-9-]+)(/.*)?$ {
    root /home/app/htdocs;
    try_files $uri $uri/ /$1/index.php?$args;
}

```

location ~ \.php$ {
    fastcgi_pass 127.0.0.1:9000;
    include fastcgi_params;
}


Et pour éviter que des .php soient exécutés dans un répertoire public (ex. /uploads/) :

```bash
location ~* ^/uploads/.*\.php$ {
    deny all;
}

```

location ~ \.php$ { ... }
location /admin/ { return 403; }  ← Ignoré si /admin/index.php


✅ Solution : utiliser ^~ pour donner la priorité :

```bash
location ^~ /admin/ { return 403; }

```

location /images/ {
    alias /data/photos/;
    # Accède à /images/photo.jpg → /data/photos/photo.jpg
}


root, lui, **ajoute** le chemin après l’URI.

- - - - - -

Bonnes pratiques
----------------

- Préfère les **location ^~** pour les fichiers statiques
- Utilise **try\_files** pour la gestion des erreurs 404
- Centralise les blocs PHP dans un include commun
- Regroupe les **location ~\*** pour les extensions statiques (CSS, JS, fonts…)
- Bloque l’accès aux fichiers sensibles :

```bash
location ~ /\.(ht|git|env|svn|project|idea) {
    deny all;
}

```

location /admin/ {
    add_header X-Frame-Options "DENY";
    add_header Content-Security-Policy "default-src 'none';";
}


- - - - - -

En résumé
---------

- Les blocs location permettent de router et sécuriser les requêtes dans Nginx
- Leur ordre d’évaluation est capital pour éviter les conflits
- Les expressions régulières permettent de factoriser et gérer dynamiquement les chemins
- Une bonne structuration évite les erreurs critiques et renforce la sécurité globale de l’application

- - - - - -

Ressources complémentaires
--------------------------

- Documentation Nginx officielle : [https://nginx.org/en/docs/http/ngx\_http\_core\_module.html#location](https://nginx.org/en/docs/http/ngx_http_core_module.html#location)
- OWASP Secure Headers Project : <https://owasp.org/www-project-secure-headers/>
- Tutoriel Nginx regex et `location` : <https://www.digitalocean.com/community/tutorials/understanding-nginx-location-blocks>
