---
title: "Stirling-PDF Docker : remplace SmallPDF et Adobe par du self-hosted open-source"
description: "Stirling-PDF Docker : auto-héberge ton éditeur PDF open-source. Fusionne, convertis, signe — sans payer un centime à Adobe ou SmallPDF."
pubDatetime: "2026-05-29T10:00:00.000Z"
modDatetime: "2026-05-31T00:00:00.000Z"
author: Brandon Visca
tags:
  - docker
  - auto-hebergement
  - productivite
  - intermediaire
  - pdf
featured: false
draft: false
focusKeyword: stirling-pdf docker
faqs:
  - question: "Est-ce que mes PDF restent stockés sur le serveur ?"
    answer: "Non. Stirling-PDF traite les fichiers en local et ne les conserve pas par défaut. Aucun tracking, aucun cloud externe."
  - question: "Ça fonctionne sans connexion internet ?"
    answer: "Oui, totalement. Seuls le module OCR et la conversion Office nécessitent un premier téléchargement de modèles ou LibreOffice. Après ça, tout est offline."
  - question: "Plusieurs utilisateurs peuvent-ils utiliser la même instance ?"
    answer: "Oui. En activant SECURITY_ENABLELOGIN=true, tu crées un compte admin et tu peux ajouter d’autres comptes depuis l’interface."
  - question: "Quelle est la différence avec LibreOffice ?"
    answer: "Stirling-PDF est une interface web dédiée aux manipulations PDF. Il utilise parfois LibreOffice en arrière-plan pour certaines conversions, mais il est beaucoup plus simple et rapide pour les tâches courantes (fusion, split, OCR, signature)."
timezone: Europe/Paris
---
> 💡 **TL;DR** — Ce qu'il faut retenir :
> - Stirling-PDF est un éditeur PDF open-source auto-hébergé (~73 000 stars GitHub).
> - Il remplace SmallPDF (~84€/an) et Adobe Acrobat (~180€/an) gratuitement.
> - Docker Compose en 5 minutes : mergé, split, OCR, conversion, signature.
> - Active le login et mets-le derrière Traefik avant de l'exposer sur Internet.

Combien tu lâches par an pour éditer des PDF ? Petit calcul rapide : SmallPDF Pro c’est ~84€/an, Adobe Acrobat Online s’approche allègrement des 180€/an. Et dans les deux cas, tes fichiers passent par leurs serveurs, avec le tracking et les comptes à la clé.

Spoiler : il existe une solution open-source qui fait tout ça — et bien plus — sans dépenser un sou.

## Stirling-PDF Docker : l'outil open-source qui te sert du PDF sur un plateau

Stirling-PDF, c'est **l'outil web open-source #1 sur GitHub** pour manipuler des PDF. On parle de près de 73 000 stars, un projet maintenu par la communauté (Stirling-Tools), sous licence MIT. Pas de compte obligatoire, pas de limite de pages, pas de watermark imposé.

Tu l'héberges chez toi sur un VPS ou un serveur perso via Docker. **Stirling-PDF Docker** devient alors ton éditeur PDF personnel : tes documents ne quittent jamais ton infrastructure. Zéro tracking, zéro analytics tiers, zéro surprise.

C'est la réponse parfaite à *"j'ai besoin de merger deux PDF rapidement sans ouvrir un compte chez un service en ligne"*.

## Comparatif rapide : Stirling-PDF vs SmallPDF vs Adobe Acrobat Online

| Critère | Stirling-PDF | SmallPDF Pro | Adobe Acrobat Online |
|---|---|---|---|
| Prix | 0€ | ~84€/an | ~180€/an |
| Hébergement | Auto-hébergé | Cloud (US) | Cloud (US) |
| Tracking / pubs | Aucun | Oui | Oui |
| Compte requis | Non | Oui | Oui |
| OCR intégré | Oui (Tesseract) | Oui | Oui |
| Conversion Office | Oui (LibreOffice) | Oui | Oui |
| Signature PDF | Oui | Oui | Oui |
| Limite de taille | Tu décides | 5–100 Mo | 100 Mo |
| Open-source | ✅ MIT | ❌ Non | ❌ Non |

Mon avis perso : à moins que ton entreprise impose Adobe pour des raisons de conformité très strictes, il n'y a aucune raison de payer pour ce que Stirling-PDF fait gratuitement et mieux.

## Tout ce qu'il fait (et c'est beaucoup)

Stirling-PDF embarge une dizaine d'outils PDF dans une seule interface web. Tu peux :

- **Fusionner** plusieurs PDF en un seul
- **Diviser** un PDF par pages ou en extraits
- **Pivoter** et réorganiser les pages
- **Compresser** un PDF pour réduire sa taille sans perdre en qualité
- **OCR** : extraire le texte d'un scan via Tesseract (FR inclus)
- **Convertir** : PDF ↔ Word, Excel, PowerPoint, image (PNG, JPG), HTML
- **Signer** électroniquement un PDF
- **Ajouter un filigrane** (watermark)
- **Caviarder** (redaction) des zones sensibles
- **Numéroter** les pages automatiquement
- **Extraire les images** d'un PDF
- **Aplatir les formulaires** (flatten forms) pour bloquer les champs

Bref, tout ce que tu faisais sur SmallPDF, mais sur ton propre serveur. Avec un GUI propre et responsive.

## Prérequis

Tu as besoin de trois choses, pas une de plus :

1. **Docker et Docker Compose** sur ton serveur
2. **Un VPS ou un serveur** avec au moins 2 Go de RAM (4 Go recommandés si tu veux l'OCR + conversion Office)
3. **Un sous-domaine** (si tu veux l'exposer en HTTPS avec Traefik ou Nginx Proxy Manager)

Résultat : en 5 minutes, t'as un éditeur PDF opérationnel accessible depuis n'importe quel navigateur. Stirling-PDF Docker tourne partout, même sur un Raspberry Pi si tu privilégies la version `ultra-lite`.

## Docker Compose : le fichier complet

Crée un dossier `/opt/stirling-pdf` et place ce `compose.yaml` dedans :

```yaml
services:
  stirling-pdf:
    image: frooodle/s-pdf:latest
    container_name: stirling-pdf
    restart: unless-stopped
    ports:
      - "8080:8080"
    volumes:
      - ./data:/usr/share/tessdata:rw
      - ./configs:/configs:rw
      - ./logs:/logs:rw
    environment:
      - SYSTEM_DEFAULTLOCALE=fr-FR
      - SECURITY_ENABLELOGIN=true
      - UI_APPNAME=Stirling-PDF
      - UI_APPNAMENAVBAR=Stirling-PDF
      - SYSTEM_MAXFILESIZE=100
      - METRICS_ENABLED=true
```

Puis lance :

```bash
cd /opt/stirling-pdf && docker compose up -d
```

Ça télécharge l'image (~1 Go), monte les volumes locaux et démarre le service sur le port 8080.

> 💡 **Astuce** : `frooodle/s-pdf:latest` est l'image officielle. Elle existe aussi en `latest-ultra-lite` (légère, sans OCR/Office) et en version fixe (ex. `2.11.0-ultra-lite`). Pour un usage domestique complet, `latest` est le meilleur compromis.

## Configuration post-install

Une fois démarré, rends-toi sur `http://IP_DU_SERVEUR:8080`.

**Activer la langue française :**
Va dans l’icône **Settings** en haut à droite, change la **Language** en **Français**. Tout bascule immédiatement.

**Activer la sécurité (obligatoire si exposé sur Internet) :**
1. Dans **Settings > Security**, active **Enable Login**
2. Crée un premier compte — il sera automatiquement administrateur
3. Redémarre le conteneur pour que `SECURITY_ENABLELOGIN=true` soit pleinement actif :
   ```bash
   docker compose restart
   ```

Ton instance est maintenant protégée par un login. Tu peux ajouter d’autres comptes utilisateurs depuis le panneau d’administration si besoin.

> ⚠️ **Important** : ne laisse jamais Stirling-PDF face à Internet sans authentification. Même s’il ne stocke pas les fichiers, un service de conversion PDF ouvert au monde est une porte d’entrée pour les abus.

## Reverse proxy avec Traefik

Si tu utilises déjà [Traefik v3](/traefik-reverse-proxy-docker/) dans ton stack, ajoute ces labels au service :

```yaml
services:
  stirling-pdf:
    image: frooodle/s-pdf:latest
    container_name: stirling-pdf
    restart: unless-stopped
    volumes:
      - ./data:/usr/share/tessdata:rw
      - ./configs:/configs:rw
      - ./logs:/logs:rw
    environment:
      - SYSTEM_DEFAULTLOCALE=fr-FR
      - SECURITY_ENABLELOGIN=true
      - UI_APPNAME=Stirling-PDF
    networks:
      - proxy
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.stirling-pdf.rule=Host(`pdf.tondomaine.com`)"
      - "traefik.http.routers.stirling-pdf.entrypoints=websecure"
      - "traefik.http.routers.stirling-pdf.tls.certresolver=letsencrypt"
      - "traefik.http.services.stirling-pdf.loadbalancer.server.port=8080"

networks:
  proxy:
    external: true
```

Remplace `pdf.tondomaine.com` par ton sous-domaine. Traefik gère le certificat Let's Encrypt tout seul. Tu n’as plus qu’à pointer ton DNS vers ton serveur.

> 💡 Si tu préfères Nginx Proxy Manager, j’ai aussi fait un guide complet : [Nginx Proxy Manager : reverse proxy en 5 min avec Docker](/nginx-proxy-manager-docker-guide/).

## FAQ

### Est-ce que mes PDF restent stockés sur le serveur ?

Non. Stirling-PDF traite les fichiers en local et ne les conserve pas par défaut. Aucun tracking, aucun cloud externe. Tes documents restent tes documents.

### Ça fonctionne sans connexion internet ?

Oui, totalement. Seuls le module OCR et la conversion Office nécessitent un premier téléchargement de modèles ou LibreOffice. Après ça, tout est offline.

### Plusieurs utilisateurs peuvent-ils utiliser la même instance ?

Oui. En activant `SECURITY_ENABLELOGIN=true`, tu crées un compte admin et tu peux ajouter d’autres comptes depuis l’interface.

### Quelle est la différence avec LibreOffice ?

Stirling-PDF est une interface web dédiée aux manipulations PDF. Il utilise parfois LibreOffice en arrière-plan pour certaines conversions, mais il est beaucoup plus simple et rapide pour les tâches courantes (fusion, split, OCR, signature).

## TL;DR

- Stirling-PDF est un éditeur PDF open-source hébergé chez toi
- Il remplace SmallPDF (~84€/an) et Adobe Acrobat (~180€/an) gratuitement
- Docker Compose à copier-coller, 5 min de setup
- Active le login et mets-le derrière Traefik avant de l’exposer
- ~73 000 stars GitHub, communauté active, zéro tracking

## Articles connexes

- [Traefik v3 : le reverse proxy Docker qui gère le HTTPS tout seul](/traefik-reverse-proxy-docker/)
- [Nginx Proxy Manager : reverse proxy en 5 min avec Docker](/nginx-proxy-manager-docker-guide/)
- [Beszel : Monitoring auto-hébergé ultra-léger pour ton homelab](/beszel-monitoring-docker/)
