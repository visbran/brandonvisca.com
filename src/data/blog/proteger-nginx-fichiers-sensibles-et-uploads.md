---
title: "Limiter les risques sur Nginx : fichiers sensibles, uploads, méthodes HTTP"
pubDatetime: "2025-04-15T20:18:39+02:00"
description: "Apprenez à renforcer la sécurité de vos serveurs Nginx en bloquant l’accès aux fichiers sensibles, en interdisant l’exécution de scripts dans les répert..."
tags:
  - linux
  - securite
  - avance
  - nginx
  - guide
  - protection
---

--------
## Table des matières


- [1. Interdire l’accès aux fichiers sensibles](#1-interdire-lacces-aux-fichiers-sensibles)
  - [Configuration Nginx recommandée :](#configuration-nginx-recommandee)
- [2. Bloquer l’exécution de scripts dans /uploads](#2-bloquer-lexecution-de-scripts-dans-uploads)
  - [Objectif : autoriser l’upload de fichiers… mais jamais leur exécution](#objectif-autoriser-lupload-de-fichiers-mais-jamais-leur-execution)
  - [Configuration Nginx :](#configuration-nginx)
- [3. Limiter les méthodes HTTP autorisées](#3-limiter-les-methodes-http-autorisees)
  - [Exemple de faille :](#exemple-de-faille)
  - [Solution : restreindre aux méthodes nécessaires](#solution-restreindre-aux-methodes-necessaires)
  - [Exemple concret :](#exemple-concret)
- [Checklist à appliquer](#checklist-a-appliquer)
- [En résumé](#en-resume)
- [Ressources utiles](#ressources-utiles)


Introduction
------------

La sécurité d’un site web ne repose pas uniquement sur des headers ou un pare-feu. Elle commence aussi par des **mesures préventives dans la configuration du serveur web**.

Dans cet article, nous allons aborder 3 axes cruciaux pour protéger votre application via **Nginx** :

1. L’interdiction d’accès aux **fichiers sensibles** (ex. : .env, .git, .htaccess)
2. La **désactivation de l’exécution PHP dans les répertoires d’upload**
3. La restriction des **méthodes HTTP** (seulement GET et POST autorisés)

Ces pratiques sont simples à mettre en place, mais trop souvent oubliées. Et pourtant, elles peuvent faire la différence entre un site sécurisé et un site compromis.

- - - - - -

1. Interdire l’accès aux fichiers sensibles
-------------------------------------------

Certains fichiers générés par vos outils ou frameworks ne doivent **jamais être accessibles via le navigateur** :

- .env (variables sensibles, mots de passe)
- .git (historique du code)
- .htaccess, .htpasswd
- .DS\_Store, Thumbs.db, etc.
- Fichiers de config internes : .idea, .vscode, .svn, .project

**Objectif** : Empêcher qu’un utilisateur accède à ces fichiers avec une simple URL du type https://monsite.com/.env.

#### Configuration Nginx recommandée :

```bash
location ~ /\.(ht|git|env|svn|project|idea|DS_Store|vscode) {
    deny all;
    access_log off;
    log_not_found off;
}

```

location ~* ^/uploads/.*\.php$ {
    deny all;
}


Tu peux élargir à d’autres extensions dangereuses :

```bash
location ~* ^/uploads/.*\.(php|phar|phtml|pl|py|cgi)$ {
    deny all;
}

```

limit_except GET POST {
    deny all;
}


Ce bloc :

- Refuse toute requête autre que GET ou POST
- Peut être appliqué globalement ou sur certains location

#### Exemple concret :

```bash
location /api/ {
    limit_except GET POST {
        deny all;
    }

    proxy_pass http://backend-api;
}

```

curl -X DELETE https://monsite.com/


Si tu reçois une réponse `405 Not Allowed`, c’est bon signe. Sinon… corrige vite !

- - - - - -

### Bonus : interdire les requêtes sur des chemins “pièges”

Certains bots scannent le web à la recherche de fichiers mal configurés. Tu peux les bloquer préventivement :

```bash
location ~* /(composer\.json|composer\.lock|package\.json|wp-config\.php|php\.ini)$ {
    deny all;
}

```

