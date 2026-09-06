---
title: Comprendre les blocs location de Nginx et leur impact sur la sécurité
description: "Maîtrisez les blocs location Nginx : types, priorités, regex et implications sécurité. Guide complet avec exemples pratiques pour configurer vos sites."
pubDatetime: "2025-04-15T20:25:29+02:00"
author: Brandon Visca
tags:
  - linux
  - securite
  - avance
  - nginx
  - guide
featured: false
draft: false
focusKeyword: Nginx location sécurité
faqs:
  - question: "Quelle est la priorité entre un bloc location exact (=) et un bloc regex ?"
    answer: "L'ordre de priorité Nginx est : 1) location = (exact), 2) location ^~ (préfixe prioritaire), 3) location ~ ou ~* (regex, premier match gagne), 4) location /prefix (préfixe le plus long). Les blocs = court-circuitent toute évaluation regex."
  - question: "Un bloc location s'applique-t-il récursivement aux sous-dossiers ?"
    answer: "Non par défaut. Un bloc location /api/ s'applique à /api/ et ses sous-chemins (/api/v1/, /api/users/...) mais chaque sous-chemin peut être surchargé par un bloc location plus spécifique."
  - question: "Comment déboguer un bloc location qui ne semble pas s'appliquer ?"
    answer: "Active les logs de debug Nginx (error_log /var/log/nginx/debug.log debug;) et utilise nginx -T pour voir la configuration compilée. L'outil nginx-config-validator permet aussi de tester les règles de matching."
---
> 💡 **TL;DR**
> - Les blocs `location` de Nginx définissent le comportement du serveur selon l'URL demandée
> - Types de location, gestion des priorités et pièges de sécurité courants
> - Bien utilisés ils organisent tes routes ; mal utilisés ils ouvrent des failles

- - - - - -

## Table des matières

Le serveur web **Nginx** est reconnu pour sa performance et sa flexibilité. L’une de ses fonctionnalités clés est la directive location, qui permet de définir le comportement à adopter pour une URL ou un ensemble d’URL.

Bien utilisée, cette directive permet d’organiser proprement ses routes, d’améliorer la sécurité, et de simplifier la maintenance du serveur. Mal utilisée, elle peut introduire des failles de sécurité, provoquer des conflits entre règles, ou casser certaines fonctionnalités.

Dans cet article, nous allons explorer :

- Les différents types de blocs location
- La priorité d’évaluation
- Les expressions régulières et leur usage
- Les erreurs fréquentes
- Les bonnes pratiques à adopter
- - - - - -
## Qu’est-ce qu’un bloc location dans Nginx ?

Un bloc location permet de définir un **comportement spécifique pour une requête HTTP en fonction de son URI**. C'est la brique sur laquelle reposent la plupart des règles de durcissement, des [headers de sécurité](/securiser-nginx-avec-headers-http/) au filtrage d'extensions. Il est souvent utilisé pour :

- Servir des fichiers statiques
- Rediriger vers un script PHP
- Appliquer des règles de sécurité ou des headers
- Déléguer à un proxy (ex: PHP-FPM, Node.js, etc.)

Exemple de base :

```nginx
location /images/ {
    root /var/www/html;
}

```

Cela signifie que toute URL commençant par /images/ sera servie depuis le répertoire /var/www/html/images.
- - - - - -
## Les différents types de blocs location

Nginx propose plusieurs syntaxes de location, chacune avec un comportement et une priorité différente.

### 1. location = /chemin

- Correspondance **exacte**
- Priorité **maximale**
- Pratique pour /favicon.ico, /robots.txt, etc.

Exemple :

```nginx
location = /login {
    return 301 https://secure.monsite.com/login;
}

```

### 2. location /chemin/

- Correspondance **préfixée**
- Le plus **général**
- Priorité **inférieure** aux autres

```nginx
location /admin/ {
    auth_basic "Espace restreint";
}

```

### 3. location ^~ /chemin

- Correspondance **préfixée prioritaire**
- Ignore les expressions régulières si le préfixe correspond

Utile pour **forcément servir des fichiers statiques**, sans qu’une regex interfère.

```nginx
location ^~ /static/ {
    root /var/www/assets;
}

```

### 4. location ~ pattern

- Expression régulière sensible à la **casse**
- Exemple :

```nginx
location ~ \.php$ {
    include fastcgi_params;
    ...
}

```

### 5. location ~* pattern

- Expression régulière **insensible à la casse**
- Très utile pour des extensions :

```nginx
location ~* \.(jpg|jpeg|png|gif|ico)$ {
    expires 7d;
    access_log off;
}

```
- - - - - -
## Priorité des blocs location

Voici **l’ordre d’évaluation** des blocs location :

1. `location = /uri` (exact)
2. `location ^~ /prefix`
3. `location ~ /regex` ou `~*`
4. `location /prefix` (générique)

Nginx applique le **premier bloc qui correspond** dans l’ordre ci-dessus.

Cela signifie que si plusieurs location peuvent correspondre à une requête, **le bloc exact ou prioritaire sera appliqué** même si une regex plus spécifique pourrait convenir.
- - - - - -
## Exemples d’utilisation avancée

### Mutualiser plusieurs utilisateurs avec une regex

Imaginons un site éducatif avec un sous-dossier par utilisateur : /tamere, /tonpere, /tasoeur, etc.

Plutôt que de créer un bloc pour chacun, on utilise :

```nginx
location ~ ^/([a-z0-9-]+)(/.*)?$ {
    root /home/app/htdocs;
    try_files $uri $uri/ /$1/index.php?$args;
}

```

Cette regex :

- Capture le nom du sous-répertoire (`$1`)
- Redirige vers le bon fichier PHP dans le bon répertoire
- Simplifie énormément la configuration

### Séparer les extensions

Pour traiter tous les fichiers .php :

```nginx
location ~ \.php$ {
    fastcgi_pass 127.0.0.1:9000;
    include fastcgi_params;
}

```

Et pour éviter que des .php soient exécutés dans un répertoire public (ex. /uploads/) :

```nginx
location ~* ^/uploads/.*\.php$ {
    deny all;
}

```
- - - - - -
## Erreurs fréquentes à éviter

### ❌ Mauvaise priorité

Avoir un bloc regex qui écrase un bloc statique :

```nginx
location ~ \.php$ { ... }
location /admin/ { return 403; }  ← Ignoré si /admin/index.php

```

✅ Solution : utiliser ^~ pour donner la priorité :

```nginx
location ^~ /admin/ { return 403; }

```

### ❌ Mauvais usage de alias vs root

Si tu utilises alias, n’oublie pas de **retirer le chemin complet de la requête** :

```nginx
location /images/ {
    alias /data/photos/;
    # Accède à /images/photo.jpg → /data/photos/photo.jpg
}

```

root, lui, **ajoute** le chemin après l’URI.
- - - - - -
## Bonnes pratiques

- Préfère les **location ^~** pour les fichiers statiques
- Utilise **try_files** pour la gestion des erreurs 404
- Centralise les blocs PHP dans un include commun
- Regroupe les **location ~*** pour les extensions statiques (CSS, JS, fonts…)
- Bloque l’accès aux fichiers sensibles :

```nginx
location ~ /\.(ht|git|env|svn|project|idea) {
    deny all;
}

```
- - - - - -
## Sécurité : ce que les blocs location peuvent protéger

Chacun de ces points est détaillé dans le guide dédié à la [protection des fichiers sensibles et des uploads](/proteger-nginx-fichiers-sensibles-et-uploads/) :

- Empêcher l’exécution de scripts dans /uploads
- Interdire les extensions .php dans les répertoires publics
- Forcer l’authentification sur des routes spécifiques (/admin/, /api/)
- Ajouter des headers de sécurité sur des zones critiques, [Content-Security-Policy](/content-security-policy-nginx-sans-casser-site/) en tête :

```nginx
location /admin/ {
    add_header X-Frame-Options "DENY";
    add_header Content-Security-Policy "default-src 'none';";
}

```
- - - - - -
## En résumé

- Les blocs location permettent de router et sécuriser les requêtes dans Nginx
- Leur ordre d’évaluation est capital pour éviter les conflits
- Les expressions régulières permettent de factoriser et gérer dynamiquement les chemins
- Une bonne structuration évite les erreurs critiques et renforce la sécurité globale de l’application
- - - - - -
## Ressources complémentaires

- Documentation Nginx officielle : <https://nginx.org/en/docs/http/ngx_http_core_module.html#location>
- OWASP Secure Headers Project : <https://owasp.org/www-project-secure-headers/>
- Tutoriel Nginx regex et `location` : <https://www.digitalocean.com/community/tutorials/understanding-nginx-location-blocks>
