---
title: "Content-Security-Policy : Protéger votre site sans bloquer vos utilisateurs"
pubDatetime: "2025-04-15T20:03:49+02:00"
author: Brandon Visca
description: "Configurez une Content-Security-Policy Nginx pour bloquer les attaques XSS sans casser votre site. Guide complet directive par directive avec exemples."
tags:
  - linux
  - securite
  - nginx
  - avance
  - guide
  - csp
---


- [Qu’est-ce qu’une Content-Security-Policy (CSP) ?](#quest-ce-quune-content-security-policy-csp)
- [Pourquoi mettre en place une CSP ?](#pourquoi-mettre-en-place-une-csp)
- [Exemple d’attaque sans CSP](#exemple-dattaque-sans-csp)
- [Intégrer une CSP dans Nginx](#integrer-une-csp-dans-nginx)
- [Une configuration CSP souple et sécurisée](#une-configuration-csp-souple-et-securisee)
  - [Détails des directives :](#details-des-directives)
- [CSP et environnement frontend moderne](#csp-et-environnement-frontend-moderne)
- [Astuce : mode report-only pour tester sans casser](#astuce-mode-report-only-pour-tester-sans-casser)
- [Où ajouter la CSP dans Nginx ?](#ou-ajouter-la-csp-dans-nginx)
- [Conseils pratiques](#conseils-pratiques)
- [Tester votre configuration](#tester-votre-configuration)
- [Cas réel : CSP dans un contexte scolaire (site avec sous-répertoires)](#cas-reel-csp-dans-un-contexte-scolaire-site-avec-sous-repertoires)
- [En résumé](#en-resume)
- [Ressources utiles](#ressources-utiles)


La **Content-Security-Policy** (CSP) est l’un des outils les plus puissants de la sécurité web moderne. Pourtant, elle est aussi l’une des plus redoutées. Mal configurée, elle peut casser des fonctionnalités critiques de votre site. Bien configurée, elle offre une **protection redoutable contre les attaques XSS, les injections de scripts et les chargements externes non maîtrisés**.

Dans cet article, nous allons explorer pas à pas :

- Ce qu’est la Content-Security-Policy
- Comment la configurer dans Nginx
- Comment éviter de bloquer le bon fonctionnement du site
- Et comment la tester et l’ajuster en toute sécurité

- - - - - -

Qu’est-ce qu’une Content-Security-Policy (CSP) ?

La CSP est un **header HTTP** qui indique au navigateur **quelles ressources il est autorisé à charger** (scripts, styles, images, etc.) et depuis quelles sources.

Son objectif principal : **empêcher l’exécution de contenu non prévu** dans la page, comme un script malveillant injecté par un attaquant (attaque XSS).

Prenons un exemple simple :

```bash
Content-Security-Policy: default-src 'self'

```

<script>alert('Vous avez été piraté');</script>


Sans CSP, le navigateur l’exécutera. Avec une bonne politique, il le bloquera purement et simplement.

- - - - - -

Intégrer une CSP dans Nginx

Dans Nginx, la CSP se configure via une directive `add_header` dans votre bloc `server {}` ou `location {}`.

Exemple basique :

```bash
add_header Content-Security-Policy "default-src 'self'" always;

```

add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https:; style-src 'self' 'unsafe-inline' https:; img-src 'self' data: https:; font-src 'self' https: data:; connect-src 'self' https:; frame-ancestors 'self';" always;


#### Détails des directives :

- `default-src 'self'` : autorise uniquement les ressources locales par défaut
- `script-src` : autorise JS inline (si nécessaire) + sources HTTPS
- `style-src` : idem pour les feuilles CSS
- `img-src` : autorise les images locales, en base64 (`data:`) et via CDN
- `font-src` : autorise les polices locales + Google Fonts
- `connect-src` : autorise les connexions Ajax/Fetch/WebSocket
- `frame-ancestors 'self'` : empêche l’intégration dans une iframe par un autre domaine

💡 Tu peux **affiner chaque directive** selon les besoins de ton site.

- - - - - -

CSP et environnement frontend moderne

Si tu utilises un framework comme Vue, React, Angular ou un CMS comme WordPress, il faut adapter la CSP :

- **WordPress + Elementor** : attention à `unsafe-inline` pour les styles et scripts dans les shortcodes.
- **React / Vue avec Webpack** : éviter `unsafe-eval` si possible.
- **CDN (Bootstrap, jQuery)** : autorise `https:` dans `script-src` et `style-src`.

Exemple spécifique WordPress avec CDN :

```bash
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://code.jquery.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com;" always;

```

add_header Content-Security-Policy-Report-Only "default-src 'self'; script-src 'self' https:;" always;


Couple ça avec une plateforme de monitoring CSP comme :

- [https://report-uri.com](https://report-uri.com/)
- [https://csp-evaluator.withgoogle.com](https://csp-evaluator.withgoogle.com/)

- - - - - -

Où ajouter la CSP dans Nginx ?

Toujours dans le bloc `server {}` ou directement dans un `location` si tu veux l’appliquer uniquement sur des zones sensibles (`/admin`, `/login`, etc.)

**Important :** ajoute `always` pour que le header soit appliqué même sur les pages 404/500.

- - - - - -

Conseils pratiques

- 🔁 Teste ta CSP sur un environnement de staging avant production
- ✅ Utilise `report-only` pour analyser sans casse
- 🔍 Inspecte les erreurs CSP dans la console développeur de ton navigateur
- 🧪 Utilise `csp-evaluator` pour voir les failles potentielles
- ❌ Évite `unsafe-inline` et `unsafe-eval` si ton frontend le permet
- 🧩 Ne bloque jamais `img-src data:` si tu utilises des images en base64 (ex. avatars dans WordPress)

- - - - - -

Tester votre configuration

Voici les meilleurs outils pour valider ta politique CSP :

- [https://securityheaders.com](https://securityheaders.com/)
- [https://observatory.mozilla.org](https://observatory.mozilla.org/)
- [https://csp-evaluator.withgoogle.com](https://csp-evaluator.withgoogle.com/)

Avec une CSP bien configurée, ton site obtiendra facilement un score **A ou A+** sur ces plateformes.

- - - - - -

Cas réel : CSP dans un contexte scolaire (site avec sous-répertoires)

Si tu héberges des applications ou sites étudiants dans des sous-répertoires (`/tata`, `/toto`, etc.), tu peux appliquer une CSP globale dans un bloc avec regex :

```bash
location ~ ^/([a-z0-9-]+)(/.*)?$ {
    root /home/app/htdocs;
    try_files $uri $uri/ /$1/index.php?$args;

    add_header Content-Security-Policy "default-src 'self'; script-src 'self' https:;" always;
}

```

## Articles connexes

- [Limiter les risques sur Nginx : fichiers sensibles, uploads,](/proteger-nginx-fichiers-sensibles-et-uploads/)
- [Comment renforcer la sécurité de Nginx avec les headers HTTP](/securiser-nginx-avec-headers-http/)
