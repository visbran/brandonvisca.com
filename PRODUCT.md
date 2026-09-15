# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Lecteurs francophones intéressés par l'auto-hébergement, le homelab et l'indépendance numérique, de niveaux mixtes :

- **Débutants** qui veulent quitter Google/SaaS et suivent un tuto pas-à-pas (copier-coller des commandes, vérifier chaque étape).
- **Homelabbers confirmés** (sysadmin, dev) qui cherchent un retour d'expérience terrain, des configs réelles et des comparatifs.

Arrivée dominante : recherche Google ou réponse d'un assistant IA sur une requête précise, atterrissage direct sur un article. Le site doit servir le débutant sans ennuyer le confirmé.

## Product Purpose

Blog tech francophone (brandonvisca.com) publiant des guides concrets, testés en prod sur le homelab de l'auteur : homelab & Proxmox, auto-hébergement (Nextcloud, Jellyfin, Vaultwarden, Immich…), Linux & sécurité, macOS & productivité.

Succès = trafic organique SEO et citabilité par les IA (GPTBot, ClaudeBot, PerplexityBot). Crédibilité personnelle de l'auteur en bénéfice secondaire.

## Positioning

Tutos en français à la fois techniques et accessibles, écrits par quelqu'un qui fait tourner l'infra décrite (Proxmox deux nœuds P720 + M720q, edge Oracle Cloud, VLAN, Caddy, Headscale, Technitium, backups QNAP). « Si j'écris un tuto, c'est que j'ai foiré l'install au moins une fois avant toi. » Ni le ton condescendant des docs officielles, ni le flou des tutos YouTube.

## Operating Context

- Contenu rédigé et maintenu dans le vault Obsidian `/opt/brandon-knowledge/Content/Articles/`, converti vers `src/data/blog/` par un pipeline automatisé (agents Hermes, publication quasi quotidienne).
- Workflow SEO/GEO outillé : `/audit-seo`, `/fix-seo`, Google Search Console MCP, `public/llms.txt` régénéré à chaque article.
- Lecture typique : article long avec blocs de code, captures, FAQ, section « Articles connexes » ; lecteur souvent en train d'exécuter les commandes dans un terminal à côté.

## Capabilities and Constraints

- Astro 6 statique, Tailwind 4, déployé sur Cloudflare Pages (push `main`).
- Fork d'astro-devosfera (lui-même fork d'AstroPaper) : fichiers thème « gelés », toute modif documentée dans `THEME_CUSTOMIZATIONS.md` ; overrides CSS dans `src/styles/custom.css`.
- URLs d'articles à `/{slug}/` (équité SEO héritée de WordPress), redirections dans `public/_redirects`.
- Recherche Pagefind, flux RSS, sitemap, OG images dynamiques, mode clair/sombre, archives, tags.
- Schema JSON-LD `Article`/`Person`/`WebSite`/`BreadcrumbList`, FAQ en frontmatter, `author: Brandon Visca` sur chaque article.
- CSP via `public/_headers` (unsafe-inline, hashes abandonnés).
- Galeries désactivées (`showGalleries: false`).
- ~260 articles, volume en croissance continue : toute surface doit tenir à l'échelle.
- **Non décidé** : forme de la monétisation (newsletter, affiliation, produits) et politique pub/tracking.

## Brand Commitments

- Nom : Brandon Visca, brandonvisca.com. Langue : français.
- Voix : tutoiement, ton direct, humour sysadmin, jamais condescendant, « testé en prod ».
- Identité terminal/homelab conservée comme signature : prompt `~/homelab (main) $` dans le hero, grain, radio lofi d'intro.
- Monétisation prévue à terme (newsletter, affiliation, produits) ; les liens affiliés doivent être divulgués.

## Evidence on Hand

- Articles réels : `src/data/blog/` (~260).
- Page À propos : `src/pages/about.md` ; CV : `src/pages/cv.md`.
- Activités annexes réelles : SaaS pour l'enseignement supérieur (en développement), rédaction technique pour mxtoolbox.eu et ippriv.com.
- GitHub : github.com/visbran.
- OG par défaut : `public/og.webp`.
- **Absents, à ne pas inventer** : témoignages, nombre d'abonnés, chiffres d'audience, logos presse, partenariats.

## Product Principles

1. **L'article est le produit.** Toute surface sert la lecture et l'exécution d'un tuto ; le reste est secondaire.
2. **Découvrable par Google et par les IA.** Structure sémantique, vitesse, URLs stables et signaux E-E-A-T priment sur l'effet.
3. **Deux niveaux, un seul texte.** Guider le débutant pas-à-pas sans ralentir le confirmé qui scanne.
4. **Crédibilité par la preuve terrain.** Montrer l'infra réelle et les erreurs vécues plutôt que des promesses.
5. **Tenir à l'échelle de la publication automatisée.** Aucun design qui exige un travail manuel par article.
