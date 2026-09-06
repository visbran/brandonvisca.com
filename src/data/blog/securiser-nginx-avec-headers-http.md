---
title: Comment renforcer la sécurité de Nginx avec les headers HTTP essentiels
description: "Sécurisez Nginx avec les headers HTTP OWASP : HSTS, X-Frame-Options, CSP, Referrer-Policy. Guide complet avec configurations testées et explications."
pubDatetime: "2025-04-06T11:33:55+02:00"
author: Brandon Visca
tags:
  - linux
  - securite
  - avance
  - nginx
  - guide
  - hardening
featured: false
draft: false
focusKeyword: sécuriser Nginx headers HTTP
faqs:
  - question: "Ces headers HTTP causent-ils des problèmes avec WordPress ou Prestashop ?"
    answer: "Certains oui. X-Frame-Options: DENY bloque les iframes, à remplacer par SAMEORIGIN pour les back-offices. Le header CSP est celui qui casse le plus souvent les plugins tiers : déployer en Report-Only d'abord."
  - question: "Faut-il appliquer ces headers sur tous les virtual hosts Nginx ?"
    answer: "Recommandé. Place les headers dans un fichier snippet (/etc/nginx/snippets/security-headers.conf) et inclus-le dans chaque virtual host avec include snippets/security-headers.conf;. Cela évite la duplication."
  - question: "Comment vérifier que mes headers HTTP sont bien actifs sur mon site ?"
    answer: "Utilise securityheaders.com (scan gratuit) ou curl -I https://ton-site.com pour voir tous les headers de réponse. Tu peux aussi inspecter l'onglet Réseau de Chrome DevTools sur n'importe quelle page."
---
> 💡 **TL;DR**
> - Sécuriser Nginx avec les headers HTTP recommandés par l'OWASP
> - Protection contre XSS, clickjacking et vol de session
> - Exemples de configuration concrets et bonnes pratiques

- - - - - -

## Table des matières

La sécurité web est aujourd’hui un enjeu fondamental. Face à la montée des attaques (XSS, clickjacking, vol de session…), les administrateurs système doivent renforcer la protection de leurs serveurs. Dans ce contexte, les **headers HTTP de sécurité** représentent une première ligne de défense simple, rapide à mettre en place et très efficace.

Dans cet article, nous allons découvrir comment sécuriser un serveur **Nginx** grâce aux en-têtes recommandés par l’**OWASP**. Nous détaillerons également leur fonctionnement, leur impact sur le comportement du navigateur, et leur intégration propre dans la configuration du serveur.

## Pourquoi les headers HTTP sont importants

Chaque fois que votre serveur web répond à une requête, il envoie des métadonnées HTTP. Certains de ces en-têtes peuvent guider le comportement du navigateur et restreindre certaines fonctionnalités sensibles, comme l’exécution de scripts, l’affichage en iframe ou encore la détection automatique du type de contenu.

En configurant correctement ces headers, vous réduisez la surface d’attaque de votre site sans modifier une seule ligne de code côté frontend.

## Les headers de sécurité recommandés par l’OWASP

### 1. Strict-Transport-Security (HSTS)

Ce header indique au navigateur qu’il doit toujours utiliser HTTPS pour se connecter à votre site. Il empêche également les attaques de type « downgrade » où un attaquant forcerait l’utilisateur à passer par HTTP.

Exemple à ajouter dans Nginx :

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

```

- `max-age=31536000` correspond à une durée d’un an.
- `includeSubDomains` applique la règle à tous les sous-domaines.

### 2. X-Frame-Options

Ce header bloque l’affichage de votre site dans une iframe, ce qui empêche les attaques de type clickjacking.

Exemple :

```nginx
add_header X-Frame-Options "SAMEORIGIN";

```

Vous pouvez aussi utiliser `DENY` pour interdire toutes les iframes, ou `ALLOW-FROM` (déprécié).

### 3. X-Content-Type-Options

Ce header empêche le navigateur de deviner le type MIME d’un fichier et d’exécuter du code inattendu.

Exemple :

```nginx
add_header X-Content-Type-Options "nosniff";

```

### 4. Referrer-Policy

Contrôle les informations du champ « Referer » pour éviter les fuites de données lors de la navigation entre sites.

Exemple :

```nginx
add_header Referrer-Policy "strict-origin-when-cross-origin";

```

## Configuration type à intégrer dans Nginx

Voici un exemple complet de bloc Nginx sécurisé :

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

```

Ce bloc est à placer dans votre bloc `server {}` dans Nginx, ou dans un `include` commun si vous gérez plusieurs hôtes virtuels.

## Tester votre configuration

Pour valider que vos headers sont bien envoyés par le serveur, vous pouvez utiliser les outils suivants :

- [https://securityheaders.com](https://securityheaders.com/)
- [https://observatory.mozilla.org](https://observatory.mozilla.org/)

Ces outils analysent vos en-têtes HTTP et vous attribuent une note de sécurité (de F à A+). Avec les headers recommandés ici, vous pouvez facilement atteindre un score de B ou A.

## Headers supplémentaires : Content-Security-Policy (CSP)

Le header `Content-Security-Policy` (CSP) permet de spécifier quelles ressources peuvent être chargées par votre site (images, scripts, styles, etc.). Il s’agit d’un rempart très efficace contre les attaques XSS. C’est le header le plus délicat du lot, au point qu’il mérite son propre guide : [configurer une CSP dans Nginx sans casser le site](/content-security-policy-nginx-sans-casser-site/).

Exemple CSP équilibrée :

```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https:; style-src 'self' 'unsafe-inline' https:;" always;

```

Cette configuration permet :

- De charger les scripts et styles depuis le site lui-même ou via HTTPS.
- De conserver le bon fonctionnement de frameworks frontend (ex. Bootstrap, jQuery, VueJS, etc.).

Plus d’infos : <https://developer.mozilla.org/fr/docs/Web/HTTP/CSP>

## Autre en-tête recommandé : Permissions-Policy

Ce header remplace l’ancien `Feature-Policy`. Il permet de contrôler l’accès aux APIs comme la caméra, la géolocalisation, le micro, etc. Couplé au rate limiting, il constitue l’étape suivante du durcissement, détaillée dans [Permissions-Policy et protection anti-bots sur Nginx](/nginx-permissions-policy-anti-bot/).

Exemple :

```nginx
add_header Permissions-Policy "geolocation=(), camera=(), microphone=(), fullscreen=(self)" always;

```

Plus d’infos : <https://developer.mozilla.org/en-US/docs/Web/HTTP/Permissions_Policy>

## Sécurité et compatibilité : trouver le bon équilibre

Il est essentiel de tester chaque en-tête avant sa mise en production. Une politique trop restrictive peut bloquer des fonctionnalités vitales, notamment sur les sites modernes utilisant des frameworks JS ou des CDN tiers. Les headers ne dispensent d’ailleurs pas de verrouiller le système de fichiers : voir [protéger les fichiers sensibles et les uploads sur Nginx](/proteger-nginx-fichiers-sensibles-et-uploads/).

Quelques conseils :

- Toujours tester sur un environnement de staging.
- Ajuster les directives `script-src`, `style-src`, `img-src` dans la CSP.
- Ajouter `unsafe-inline` uniquement si vraiment nécessaire, avec des commentaires en code pour l’identifier.

## Cas d’usage : mutualisation Nginx pour plusieurs utilisateurs

Dans un contexte éducatif ou multi-utilisateur, on peut mutualiser la sécurité sur plusieurs sous-répertoires grâce aux expressions régulières dans Nginx.

Exemple de bloc :

```nginx
location ~ ^/([a-z0-9-]+)(/.*)?$ {
    root /home/app/htdocs;
    try_files $uri $uri/ /$1/index.php?$args;

    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";
    add_header Referrer-Policy "strict-origin-when-cross-origin";
}

```

Cette méthode est idéale pour sécuriser tous les espaces utilisateurs sans répéter le code pour chaque `location`.

## Conclusion

Les headers HTTP de sécurité sont des outils puissants, simples à mettre en œuvre et très efficaces. Ils renforcent la confiance des navigateurs, limitent les attaques classiques, et améliorent instantanément votre score de sécurité.

En suivant ce guide, vous pouvez :

- Améliorer votre note sur [securityheaders.com](http://securityheaders.com)
- Appliquer les bonnes pratiques [OWASP](http://owasp.org)
- Protéger les utilisateurs finaux sans nuire à l’expérience

Dans le prochain article, nous verrons comment configurer une **[Content-Security-Policy (CSP)](https://brandonvisca.com/content-security-policy-nginx-sans-casser-site/)** efficace sans casser votre frontend.
