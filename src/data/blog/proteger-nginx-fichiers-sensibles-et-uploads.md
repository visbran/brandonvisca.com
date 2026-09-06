---
title: "Limiter les risques sur Nginx : fichiers sensibles, uploads, méthodes HTTP"
description: "Renforcez la sécurité Nginx en bloquant les fichiers sensibles et l'exécution de scripts dans les répertoires d'upload. Configurations prêtes à copier."
pubDatetime: "2025-04-15T20:18:39+02:00"
author: Brandon Visca
tags:
  - linux
  - securite
  - avance
  - nginx
  - guide
featured: false
draft: false
focusKeyword: sécuriser Nginx uploads
faqs:
  - question: "Faut-il recharger Nginx après chaque modification de configuration ?"
    answer: "Oui. Utilise nginx -t pour valider la syntaxe, puis systemctl reload nginx (ou nginx -s reload) pour appliquer sans coupure de service. Le reload est graceful : les connexions actives ne sont pas interrompues."
  - question: "Comment vérifier qu'un fichier sensible (.env, .git) est bien bloqué par Nginx ?"
    answer: "Teste avec curl -I https://ton-site.com/.env. La réponse doit être 403 Forbidden ou 404 Not Found, jamais 200. Utilise aussi nikto -h ton-site.com pour un scan automatique des fichiers exposés."
  - question: "Mon répertoire uploads autorise-t-il l'exécution PHP par défaut sur Nginx ?"
    answer: "Avec Nginx seul : non, Nginx ne traite pas PHP sans configuration explicite (fastcgi_pass). Mais si php-fpm est configuré globalement, les scripts dans uploads/ peuvent être exécutés, il faut donc bloquer explicitement l'exécution dans ce dossier."
---
> 💡 **TL;DR**
> - La sécurité Nginx commence dans la config, pas seulement avec les headers ou le pare-feu
> - Bloquer l'accès aux fichiers sensibles et interdire l'exécution de scripts dans les dossiers d'uploads
> - Limiter les méthodes HTTP aux seules actions légitimes

- - - - - -

## Table des matières

- - - - - -
La sécurité d’un site web ne repose pas uniquement sur des headers ou un pare-feu. Elle commence aussi par des **mesures préventives dans la configuration du serveur web**.

Dans cet article, nous allons aborder 3 axes cruciaux pour protéger votre application via **Nginx** :

1. L’interdiction d’accès aux **fichiers sensibles** (ex. : .env, .git, .htaccess)
2. La **désactivation de l’exécution PHP dans les répertoires d’upload**
3. La restriction des **méthodes HTTP** (seulement GET et POST autorisés)

Ces pratiques sont simples à mettre en place, mais trop souvent oubliées. Et pourtant, elles peuvent faire la différence entre un site sécurisé et un site compromis. Elles reposent toutes sur [les blocs `location`](/nginx-location-bloc-et-securite/), dont l'ordre de priorité décide de la règle qui l'emporte.
- - - - - -
## 1. Interdire l’accès aux fichiers sensibles

Certains fichiers générés par vos outils ou frameworks ne doivent **jamais être accessibles via le navigateur**. C'est le pendant côté système de fichiers de ce que font [les headers de sécurité](/securiser-nginx-avec-headers-http/) côté navigateur :

- .env (variables sensibles, mots de passe)
- .git (historique du code)
- .htaccess, .htpasswd
- .DS_Store, Thumbs.db, etc.
- Fichiers de config internes : .idea, .vscode, .svn, .project

**Objectif** : Empêcher qu’un utilisateur accède à ces fichiers avec une simple URL du type https://monsite.com/.env.

#### Configuration Nginx recommandée :

```nginx
location ~ /\.(ht|git|env|svn|project|idea|DS_Store|vscode) {
    deny all;
    access_log off;
    log_not_found off;
}

```

🔒 Ce bloc :

- Interdit totalement l’accès
- Désactive les logs d’erreur (discrétion)
- Fonctionne sur toutes les variantes (.git, .env, .gitignore, etc.)

✅ Tu peux le placer dans ton bloc server {} ou dans un include partagé entre tes vhosts.
- - - - - -
## 2. Bloquer l’exécution de scripts dans /uploads

Les dossiers où les utilisateurs peuvent **téléverser des fichiers** sont des zones à haut risque.

Si un pirate réussit à envoyer un fichier .php, il pourrait l’exécuter ensuite en visitant :
https://monsite.com/uploads/malicieux.php

🔥 Cela peut aboutir à une **prise de contrôle complète du serveur** si le script injecté contient une backdoor.

#### Objectif : autoriser l’upload de fichiers… mais **jamais leur exécution**

#### Configuration Nginx :

```nginx
location ~* ^/uploads/.*\.php$ {
    deny all;
}

```

Tu peux élargir à d’autres extensions dangereuses :

```nginx
location ~* ^/uploads/.*\.(php|phar|phtml|pl|py|cgi)$ {
    deny all;
}

```

💡 Conseil : sépare bien tes dossiers d’upload et tes scripts PHP.
- - - - - -
## 3. Limiter les méthodes HTTP autorisées

Par défaut, un serveur web accepte plusieurs méthodes :

- GET (lecture)
- POST (formulaires)
- Mais aussi : PUT, DELETE, TRACE, OPTIONS, PATCH…

🛑 Certaines de ces méthodes sont **dangereuses** si activées inutilement, surtout dans les backends dynamiques.

#### Exemple de faille :

Une API exposée sans restriction peut accepter une requête DELETE non protégée, ce qui peut effacer des données.
- - - - - -
#### Solution : restreindre aux méthodes nécessaires

```nginx
limit_except GET POST {
    deny all;
}

```

Ce bloc :

- Refuse toute requête autre que GET ou POST
- Peut être appliqué globalement ou sur certains location

#### Exemple concret :

```nginx
location /api/ {
    limit_except GET POST {
        deny all;
    }

    proxy_pass http://backend-api;
}

```
- - - - - -
### Astuce : tester avec curl

Pour vérifier si ton serveur accepte d’autres méthodes, utilise cette commande :

```bash
curl -X DELETE https://monsite.com/

```

Si tu reçois une réponse `405 Not Allowed`, c’est bon signe. Sinon… corrige vite !
- - - - - -
### Bonus : interdire les requêtes sur des chemins “pièges”

Certains bots scannent le web à la recherche de fichiers mal configurés. Tu peux les bloquer préventivement :

```nginx
location ~* /(composer\.json|composer\.lock|package\.json|wp-config\.php|php\.ini)$ {
    deny all;
}

```

Et tu peux aussi bloquer les requêtes contenant certains user-agents suspects ou chemins spécifiques.
- - - - - -
Une fois ces trois règles en place, il reste à cadrer ce que le navigateur a le droit de charger : c'est le rôle de la [Content-Security-Policy](/content-security-policy-nginx-sans-casser-site/).

- - - - - -

## Checklist à appliquer

| Vérification | Statut idéal |
| --- | --- |
| Fichiers sensibles inaccessibles | ✅ OK |
| PHP interdit dans les dossiers publics | ✅ OK |
| Seules les méthodes GET/POST actives | ✅ OK |
| Accès REST/API protégé | ✅ OK |
| Logging désactivé sur les interdictions | ✅ OK |
- - - - - -
## En résumé

- Bloquer l’accès aux fichiers sensibles est une **barrière essentielle** contre les fuites d’informations.
- Empêcher l’exécution de fichiers dans /uploads protège contre les **RCE (Remote Code Execution)**.
- Limiter les méthodes HTTP réduit considérablement la **surface d’attaque**.

Ces protections sont simples, légères, et redoutablement efficaces. Ce sont des pratiques recommandées par tous les standards modernes, y compris l’[OWASP](https://owasp.org/www-project-secure-headers/).
- - - - - -
## Ressources utiles

- OWASP Secure Headers : <https://owasp.org/www-project-secure-headers/>
- Nginx Core Module : <https://nginx.org/en/docs/http/ngx_http_core_module.html#location>
- Acunetix Guide - Secure File Uploads : <https://www.acunetix.com/blog/articles/secure-file-upload-best-practices/>
- Cheat sheet des méthodes HTTP : <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods>
