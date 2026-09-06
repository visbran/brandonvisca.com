---
title: "Content-Security-Policy : Protéger votre site sans bloquer vos utilisateurs"
description: Configurez une Content-Security-Policy Nginx pour bloquer les attaques XSS sans casser votre site. Guide complet directive par directive avec exemples.
pubDatetime: "2025-04-15T20:03:49+02:00"
author: Brandon Visca
tags:
  - linux
  - securite
  - nginx
  - avance
  - guide
featured: false
draft: false
focusKeyword: Content-Security-Policy Nginx
faqs:
  - question: "Comment tester une CSP sans risquer de casser le site en production ?"
    answer: "Utilise d'abord le header Content-Security-Policy-Report-Only avec une URL report-uri. Le navigateur signale les violations sans bloquer quoi que ce soit, ce qui te permet d'ajuster la politique avant de l'activer."
  - question: "Ma CSP bloque Google Analytics ou Google Tag Manager, que faire ?"
    answer: "Ajoute les domaines Google aux directives script-src et connect-src : 'https://www.googletagmanager.com' et 'https://www.google-analytics.com'. Pour GTM, le nonce-based CSP est la solution la plus propre."
  - question: "Une CSP protège-t-elle contre toutes les attaques XSS ?"
    answer: "Non, la CSP est une couche de défense supplémentaire, pas une solution complète. Elle réduit fortement l'impact d'une XSS en empêchant l'exécution de scripts non autorisés, mais ne remplace pas la validation des entrées."
---
> 💡 **TL;DR**
> - La Content-Security-Policy est l'un des headers les plus puissants contre les attaques XSS
> - Mal configurée, elle bloque tes propres scripts et casse le site
> - Ce guide montre comment la configurer dans Nginx pas à pas, sans casser le frontend

- - - - - -

## Table des matières

La **Content-Security-Policy** (CSP) est l’un des outils les plus puissants de la sécurité web moderne. Pourtant, elle est aussi l’une des plus redoutées. Mal configurée, elle peut casser des fonctionnalités critiques de votre site. Bien configurée, elle offre une **protection redoutable contre les attaques XSS, les injections de scripts et les chargements externes non maîtrisés**.

Dans cet article, nous allons explorer pas à pas :

- Ce qu’est la Content-Security-Policy
- Comment la configurer dans Nginx
- Comment éviter de bloquer le bon fonctionnement du site
- Et comment la tester et l’ajuster en toute sécurité
- - - - - -
## Qu’est-ce qu’une Content-Security-Policy (CSP) ?

La CSP est un **header HTTP** qui indique au navigateur **quelles ressources il est autorisé à charger** (scripts, styles, images, etc.) et depuis quelles sources.

Son objectif principal : **empêcher l’exécution de contenu non prévu** dans la page, comme un script malveillant injecté par un attaquant (attaque XSS).

Prenons un exemple simple :

```
Content-Security-Policy: default-src 'self'

```

Cette directive interdit au navigateur de charger des ressources (scripts, images, etc.) depuis des domaines autres que le vôtre.
- - - - - -
## Pourquoi mettre en place une CSP ?

Voici quelques bénéfices clés :

- Empêche les **scripts injectés** (XSS) d’être exécutés
- Bloque les **ressources non autorisées** (ex. CDN tiers non validés)
- Évite les **attaques de type data exfiltration** (ex. chargement d’images depuis un domaine pirate pour récupérer des infos)
- Protège les utilisateurs avec un niveau de sécurité élevé
- ✅ Recommandé par l’[OWASP](https://owasp.org/www-project-secure-headers/) et Mozilla
- - - - - -
## Exemple d’attaque sans CSP

Un champ de commentaire non protégé peut permettre à un utilisateur malveillant d’injecter :

```
<script>alert('Vous avez été piraté');</script>

```

Sans CSP, le navigateur l’exécutera. Avec une bonne politique, il le bloquera purement et simplement.
- - - - - -
## Intégrer une CSP dans Nginx

Dans Nginx, la CSP se configure via une directive `add_header` dans votre bloc `server {}` ou `location {}`. Si le fonctionnement des blocs `location` ne vous est pas familier, [ce guide sur les blocs location](/nginx-location-bloc-et-securite/) explique leur ordre de priorité, qui décide quel header s'applique où.

Exemple basique :

```nginx
add_header Content-Security-Policy "default-src 'self'" always;

```

Mais en pratique, cela cassera tous vos scripts, styles et ressources provenant de CDNs externes (Bootstrap, jQuery, Google Fonts…).
- - - - - -
## Une configuration CSP souple et sécurisée

Voici une configuration **équilibrée** qui couvre la majorité des sites modernes sans tout bloquer :

```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https:; style-src 'self' 'unsafe-inline' https:; img-src 'self' data: https:; font-src 'self' https: data:; connect-src 'self' https:; frame-ancestors 'self';" always;

```

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
## CSP et environnement frontend moderne

Si tu utilises un framework comme Vue, React, Angular ou un CMS comme WordPress, il faut adapter la CSP :

- **WordPress + Elementor** : attention à `unsafe-inline` pour les styles et scripts dans les shortcodes.
- **React / Vue avec Webpack** : éviter `unsafe-eval` si possible.
- **CDN (Bootstrap, jQuery)** : autorise `https:` dans `script-src` et `style-src`.

Exemple spécifique WordPress avec CDN :

```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://code.jquery.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com;" always;

```
- - - - - -
## Astuce : mode `report-only` pour tester sans casser

Avant d’activer ta politique CSP, tu peux la tester en mode `report-only`. Cela permet de voir les violations sans bloquer les ressources :

```nginx
add_header Content-Security-Policy-Report-Only "default-src 'self'; script-src 'self' https:;" always;

```

Couple ça avec une plateforme de monitoring CSP comme :

- [https://report-uri.com](https://report-uri.com/)
- [https://csp-evaluator.withgoogle.com](https://csp-evaluator.withgoogle.com/)
- - - - - -
## Où ajouter la CSP dans Nginx ?

Toujours dans le bloc `server {}` ou directement dans un `location` si tu veux l’appliquer uniquement sur des zones sensibles (`/admin`, `/login`, etc.). La CSP arrive rarement seule : elle se pose en général en même temps que [les autres headers de sécurité](/securiser-nginx-avec-headers-http/).

**Important :** ajoute `always` pour que le header soit appliqué même sur les pages 404/500.

Une CSP bien réglée bloque l'exécution de scripts injectés, mais elle n'empêche pas de servir un fichier qui n'aurait jamais dû être exposé. Pour ce volet, voir [protéger les fichiers sensibles et les uploads](/proteger-nginx-fichiers-sensibles-et-uploads/).
- - - - - -
## Conseils pratiques

- 🔁 Teste ta CSP sur un environnement de staging avant production
- ✅ Utilise `report-only` pour analyser sans casse
- 🔍 Inspecte les erreurs CSP dans la console développeur de ton navigateur
- 🧪 Utilise `csp-evaluator` pour voir les failles potentielles
- ❌ Évite `unsafe-inline` et `unsafe-eval` si ton frontend le permet
- 🧩 Ne bloque jamais `img-src data:` si tu utilises des images en base64 (ex. avatars dans WordPress)
- - - - - -
## Tester votre configuration

Voici les meilleurs outils pour valider ta politique CSP :

- [https://securityheaders.com](https://securityheaders.com/)
- [https://observatory.mozilla.org](https://observatory.mozilla.org/)
- [https://csp-evaluator.withgoogle.com](https://csp-evaluator.withgoogle.com/)

Avec une CSP bien configurée, ton site obtiendra facilement un score **A ou A+** sur ces plateformes.
- - - - - -
## Cas réel : CSP dans un contexte scolaire (site avec sous-répertoires)

Si tu héberges des applications ou sites étudiants dans des sous-répertoires (`/tata`, `/toto`, etc.), tu peux appliquer une CSP globale dans un bloc avec regex :

```nginx
location ~ ^/([a-z0-9-]+)(/.*)?$ {
    root /home/app/htdocs;
    try_files $uri $uri/ /$1/index.php?$args;

    add_header Content-Security-Policy "default-src 'self'; script-src 'self' https:;" always;
}

```
- - - - - -
## En résumé

- ✅ La Content-Security-Policy protège contre les attaques XSS et injections
- ⚙️ Elle se configure facilement dans Nginx avec `add_header`
- 🎯 Elle peut être testée en mode `report-only` pour éviter de casser ton site
- 🔒 Elle est recommandée par tous les standards modernes (OWASP, Mozilla, Google)
- 💡 Elle doit être **adaptée à ton environnement technique**
- - - - - -
## Ressources utiles

- Documentation MDN CSP : <https://developer.mozilla.org/fr/docs/Web/HTTP/CSP>
- Google CSP Evaluator : [https://csp-evaluator.withgoogle.com](https://csp-evaluator.withgoogle.com/)
- OWASP Secure Headers : <https://owasp.org/www-project-secure-headers/>
- Report URI : [https://report-uri.com](https://report-uri.com/)
- SecurityHeaders.com : [https://securityheaders.com](https://securityheaders.com/)
