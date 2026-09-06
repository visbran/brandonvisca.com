---
title: "Aller plus loin : Permissions-Policy et protection anti-bots sur Nginx"
description: Renforcez la sécurité de vos apps web avec Permissions-Policy Nginx pour restreindre les API navigateur et bloquer les bots malveillants. Guide complet.
pubDatetime: "2025-04-27T17:12:59+02:00"
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
focusKeyword: Nginx Permissions-Policy anti-bot
faqs:
  - question: "Le header Permissions-Policy remplace-t-il l'ancien Feature-Policy ?"
    answer: "Oui. Permissions-Policy est le successeur standardisé de Feature-Policy. La syntaxe a changé (plus de guillemets, nouvelle notation) mais le concept est identique. Feature-Policy est déprécié depuis Chrome 88."
  - question: "Comment bloquer les bots sans affecter les vrais utilisateurs avec Permissions-Policy ?"
    answer: "Permissions-Policy contrôle les APIs navigateur (caméra, micro, géolocalisation), pas le trafic bot. Pour bloquer les bots, combiner fail2ban sur les logs Nginx + règles de rate limiting + Cloudflare Bot Management."
  - question: "Peut-on tester ma Permissions-Policy sans la mettre en production ?"
    answer: "Oui. Dans Chrome DevTools, l'onglet Application > Permissions Policy affiche les permissions autorisées et bloquées sur la page courante. L'extension Security Headers permet aussi d'analyser les headers en temps réel."
---
> 💡 **TL;DR**
> - Après HSTS, CSP et X-Frame-Options, le header Permissions-Policy affine ta sécurité
> - Il restreint les API navigateur (caméra, micro, géolocalisation) accessibles à ton site
> - Plus des protections anti-bots intégrées à Nginx pour limiter les abus

- - - - - -

## Table des matières

- - - - - -
Lorsque vous avez déjà mis en place [les headers classiques](/securiser-nginx-avec-headers-http/) (HSTS, CSP, X-Frame-Options…), il reste encore des moyens d’**affiner votre politique de sécurité**.

Deux approches particulièrement utiles :

1. **Les Permissions-Policy** : pour limiter ce que le navigateur est autorisé à faire (caméra, micro, géolocalisation…)
2. **Le Rate Limiting dans Nginx** : pour bloquer ou ralentir les requêtes abusives, souvent utilisées par des bots ou des scripts malveillants

Ces deux mesures combinées offrent un **contrôle plus précis du comportement client** et **protègent votre serveur contre les abus**.
- - - - - -
## 1. Permissions-Policy : contrôle des capacités navigateur

Anciennement connue sous le nom de Feature-Policy, cette en-tête HTTP permet de **restreindre ou autoriser l’accès aux fonctionnalités sensibles du navigateur**, comme la caméra, le micro, la géolocalisation, etc. Elle complète la [Content-Security-Policy](/content-security-policy-nginx-sans-casser-site/), qui contrôle les ressources chargées là où Permissions-Policy contrôle les APIs utilisées.

### Objectif :

Empêcher les navigateurs d’accéder à des APIs si ce n’est pas nécessaire au bon fonctionnement du site.
- - - - - -
### Exemple de configuration :

```nginx
add_header Permissions-Policy "geolocation=(), microphone=(), camera=(), fullscreen=(self), payment=()" always;

```

### Explication :

- `geolocation=()` → désactive complètement l’accès à l’API de géolocalisation
- `fullscreen=(self)` → autorise le plein écran uniquement depuis le site actuel
- `payment=()` → interdit l’usage de l’API de paiement

Vous pouvez **affiner domaine par domaine**, exemple :

```
camera=(self "https://appli.externe.com")

```
- - - - - -
### Pourquoi l’utiliser ?

- Réduction des risques d’exploitation des APIs navigateur
- Moins de permissions = surface d’attaque plus faible
- Compatible avec les navigateurs modernes (Chrome, Edge, Firefox)
- Permet de **respecter les règles RGPD** en désactivant des fonctions sensibles
- - - - - -
## 2. Rate limiting avec Nginx : la protection anti-bots native

Les attaques par force brute, les scans automatisés ou les abus de formulaire sont **des menaces constantes** pour les serveurs web. Le rate limiting agit en amont, avant même que la requête n’atteigne les [blocs `location` que tu as sécurisés](/nginx-location-bloc-et-securite/). Heureusement, **Nginx dispose de modules intégrés** pour contrôler le débit par IP.
- - - - - -
### Étape 1 : définir une zone de limitation

```nginx
limit_req_zone $binary_remote_addr zone=antibot:10m rate=10r/s;

```

Cette directive :

- Crée une zone appelée `antibot`
- Limite à 10 requêtes par seconde **par IP**
- Utilise jusqu’à 10 Mo de mémoire partagée (peut contenir environ 160 000 IP)
- - - - - -
### Étape 2 : appliquer la règle

```nginx
location / {
    limit_req zone=antibot burst=20 nodelay;
}

```

- `burst=20` : permet une petite tolérance en pic
- `nodelay` : autorise le burst sans ralentissement

💡 Tu peux adapter cette règle pour les zones sensibles uniquement :

```nginx
location /login {
    limit_req zone=antibot burst=5;
}

```
- - - - - -
### Résultat :

Les requêtes excessives sont automatiquement **ralenties** ou **rejetées** avec une réponse HTTP 503 ou 429.
- - - - - -
### Bonus : filtrer certains User-Agent

Pour bloquer certains bots connus :

```nginx
if ($http_user_agent ~* (HTTrack|wget|curl|scanner|sqlmap)) {
    return 403;
}

```

Et si tu veux aller plus loin :

- [fail2ban](https://www.fail2ban.org/wiki/index.php/Main_Page) pour bannir les IP
- [ModSecurity](https://www.modsecurity.org/) pour un WAF plus complet
- - - - - -
## Exemple combiné : sécurité sur un endpoint de formulaire

```nginx
location /contact {
    limit_req zone=antibot burst=3;

    add_header Permissions-Policy "microphone=(), camera=(), payment=(), fullscreen=(self)" always;

    try_files $uri $uri/ /contact/index.php?$args;
}

```
- - - - - -
## Astuces pour ne pas bloquer les vrais utilisateurs

- Adapte `rate` et `burst` aux cas réels : 5 requêtes/seconde suffisent pour un humain.
- Exclue les robots légitimes (Googlebot, Bingbot) si besoin avec une whiteliste.
- Surveille les logs de `limit_req_status` pour analyser les rejets.
- - - - - -
## Conclusion

Ces deux techniques permettent de **passer un cap supplémentaire dans la sécurisation** de votre site :

- Les **Permissions-Policy** vous donnent un contrôle fin sur les capacités du navigateur côté utilisateur
- Le **Rate Limiting** protège votre backend des abus, sans surcoût de performance

Intégrées intelligemment dans Nginx, elles renforcent l’**intégrité, la disponibilité et la confidentialité** de vos services web.
- - - - - -
## Ressources utiles

- [Permissions Policy - MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Permissions_Policy)
- [Rate Limiting in Nginx](https://docs.nginx.com/nginx/admin-guide/security-controls/controlling-access-proxied-http/)
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)
- [Fail2ban - Official Site](https://www.fail2ban.org/wiki/index.php/Main_Page)
