---
title: Comment renforcer la sécurité de Nginx avec les headers HTTP essentiels
pubDatetime: "2025-04-06T11:33:55+02:00"
description: "Apprenez à sécuriser efficacement votre serveur Nginx en configurant les headers HTTP recommandés par l’OWASP. Un guide complet avec exemples pratiques,..."
tags:
  - linux
  - securite
  - avance
  - nginx
  - guide
  - headers
---

---
## Table des matières


- [Pourquoi les headers HTTP sont importants](#pourquoi-les-headers-http-sont-importants)
- [Les headers de sécurité recommandés par l’OWASP](#les-headers-de-securite-recommandes-par-l-owasp)
  - [1. Strict-Transport-Security (HSTS)](#1-strict-transport-security-hsts)
  - [2. X-Frame-Options](#2-x-frame-options)
  - [3. X-Content-Type-Options](#3-x-content-type-options)
  - [4. Referrer-Policy](#4-referrer-policy)
- [Configuration type à intégrer dans Nginx](#configuration-type-a-integrer-dans-nginx)
- [Tester votre configuration](#tester-votre-configuration)
- [Headers supplémentaires : Content-Security-Policy (CSP)](#headers-supplementaires-content-security-policy-csp)
- [Autre en-tête recommandé : Permissions-Policy](#autre-en-tete-recommande-permissions-policy)
- [Sécurité et compatibilité : trouver le bon équilibre](#securite-et-compatibilite-trouver-le-bon-equilibre)
- [Cas d’usage : mutualisation Nginx pour plusieurs utilisateurs](#cas-dusage-mutualisation-nginx-pour-plusieurs-utilisateurs)
- [Conclusion](#conclusion)


La sécurité web est aujourd’hui un enjeu fondamental. Face à la montée des attaques (XSS, clickjacking, vol de session…), les administrateurs système doivent renforcer la protection de leurs serveurs. Dans ce contexte, les **headers HTTP de sécurité** représentent une première ligne de défense simple, rapide à mettre en place et très efficace.

Dans cet article, nous allons découvrir comment sécuriser un serveur **Nginx** grâce aux en-têtes recommandés par l’**OWASP**. Nous détaillerons également leur fonctionnement, leur impact sur le comportement du navigateur, et leur intégration propre dans la configuration du serveur.

### Pourquoi les headers HTTP sont importants

Chaque fois que votre serveur web répond à une requête, il envoie des métadonnées HTTP. Certains de ces en-têtes peuvent guider le comportement du navigateur et restreindre certaines fonctionnalités sensibles, comme l’exécution de scripts, l’affichage en iframe ou encore la détection automatique du type de contenu.

En configurant correctement ces headers, vous réduisez la surface d’attaque de votre site sans modifier une seule ligne de code côté frontend.

### Les headers de sécurité recommandés par l’OWASP

#### 1. Strict-Transport-Security (HSTS)

Ce header indique au navigateur qu’il doit toujours utiliser HTTPS pour se connecter à votre site. Il empêche également les attaques de type « downgrade » où un attaquant forcerait l’utilisateur à passer par HTTP.

Exemple à ajouter dans Nginx :

```bash
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

```

add_header X-Frame-Options "SAMEORIGIN";


Vous pouvez aussi utiliser `DENY` pour interdire toutes les iframes, ou `ALLOW-FROM` (déprécié).

#### 3. X-Content-Type-Options

Ce header empêche le navigateur de deviner le type MIME d’un fichier et d’exécuter du code inattendu.

Exemple :

```bash
add_header X-Content-Type-Options "nosniff";

```

add_header Referrer-Policy "strict-origin-when-cross-origin";


### Configuration type à intégrer dans Nginx

Voici un exemple complet de bloc Nginx sécurisé :

```bash
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

```

add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https:; style-src 'self' 'unsafe-inline' https:;" always;


Cette configuration permet :

- De charger les scripts et styles depuis le site lui-même ou via HTTPS.
- De conserver le bon fonctionnement de frameworks frontend (ex. Bootstrap, jQuery, VueJS, etc.).

Plus d’infos : <https://developer.mozilla.org/fr/docs/Web/HTTP/CSP>

### Autre en-tête recommandé : Permissions-Policy

Ce header remplace l’ancien `Feature-Policy`. Il permet de contrôler l’accès aux APIs comme la caméra, la géolocalisation, le micro, etc.

Exemple :

```bash
add_header Permissions-Policy "geolocation=(), camera=(), microphone=(), fullscreen=(self)" always;

```

location ~ ^/([a-z0-9-]+)(/.*)?$ {
    root /home/app/htdocs;
    try_files $uri $uri/ /$1/index.php?$args;

    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";
    add_header Referrer-Policy "strict-origin-when-cross-origin";
}


Cette méthode est idéale pour sécuriser tous les espaces utilisateurs sans répéter le code pour chaque `location`.

### Conclusion

Les headers HTTP de sécurité sont des outils puissants, simples à mettre en œuvre et très efficaces. Ils renforcent la confiance des navigateurs, limitent les attaques classiques, et améliorent instantanément votre score de sécurité.

En suivant ce guide, vous pouvez :

- Améliorer votre note sur [securityheaders.com](http://securityheaders.com)
- Appliquer les bonnes pratiques [OWASP](http://owasp.org)
- Protéger les utilisateurs finaux sans nuire à l’expérience

Dans le prochain article, nous verrons comment configurer une **[Content-Security-Policy (CSP)](https://brandonvisca.com/content-security-policy-nginx-sans-casser-site/)** efficace sans casser votre frontend.
