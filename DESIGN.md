---
name: Brandon Visca
description: Blog tech francophone sur le homelab, l'auto-hébergement et l'indépendance numérique.
colors:
  console-blue: "#1158d1"
  console-blue-night: "#008fec"
  sage-paper: "#f2f5ec"
  graphite-ink: "#353538"
  lichen: "#bbc789"
  blueprint-line: "#7cadff"
  rack-night: "#10131a"
  chalk-white: "#f6f7f8"
  slate-well: "#212f3f"
  signal-line: "#2264e3"
typography:
  display:
    fontFamily: "Figtree, sans-serif"
    fontSize: "clamp(3rem, 8vw, 4.5rem)"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.025em"
  headline:
    fontFamily: "Figtree, sans-serif"
    fontSize: "clamp(1.875rem, 5vw, 2.75rem)"
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "-0.025em"
  title:
    fontFamily: "Figtree, sans-serif"
    fontSize: "1.125rem"
    fontWeight: 600
    lineHeight: 1.55
  body:
    fontFamily: "Figtree, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.75
  heading-lg:
    fontFamily: "Figtree, sans-serif"
    fontSize: "2rem"
    fontWeight: 700
    lineHeight: 1.2
  heading-md:
    fontFamily: "Figtree, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 700
    lineHeight: 1.3
  heading-sm:
    fontFamily: "Figtree, sans-serif"
    fontSize: "1.25rem"
    fontWeight: 600
    lineHeight: 1.35
  body-ui:
    fontFamily: "Figtree, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
  ui:
    fontFamily: "Figtree, sans-serif"
    fontSize: "0.8125rem"
    fontWeight: 500
    lineHeight: 1.4
  micro:
    fontFamily: "Cartograph CF, monospace"
    fontSize: "0.75rem"
    fontWeight: 400
    lineHeight: 1.3
  note:
    fontFamily: "Sriracha, cursive"
    fontSize: "1.05rem"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Figtree, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: "0.1em"
  mono:
    fontFamily: "Cartograph CF, monospace"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.6
rounded:
  sm: "4px"
  md: "6px"
  lg: "8px"
  xl: "12px"
  2xl: "16px"
  3xl: "24px"
  full: "9999px"
spacing:
  gutter: "16px"
  card: "20px"
  section: "24px"
  panel-y: "48px"
  panel-x: "40px"
components:
  button-cta:
    backgroundColor: "{colors.console-blue}"
    textColor: "{colors.console-blue}"
    typography: "{typography.title}"
    rounded: "{rounded.xl}"
    padding: "16px 32px"
  nav-link:
    textColor: "{colors.graphite-ink}"
    rounded: "{rounded.lg}"
    padding: "6px 12px"
  nav-link-active:
    textColor: "{colors.console-blue}"
    rounded: "{rounded.lg}"
    padding: "6px 12px"
  card-post:
    backgroundColor: "{colors.lichen}"
    textColor: "{colors.graphite-ink}"
    rounded: "{rounded.2xl}"
    padding: "{spacing.card}"
  tag-badge:
    backgroundColor: "{colors.console-blue}"
    textColor: "{colors.console-blue}"
    typography: "{typography.mono}"
    rounded: "{rounded.full}"
    padding: "2px 10px"
  code-inline:
    backgroundColor: "{colors.lichen}"
    textColor: "{colors.graphite-ink}"
    typography: "{typography.mono}"
    rounded: "{rounded.md}"
    padding: "2px 6px"
  blockquote-note:
    backgroundColor: "{colors.console-blue}"
    textColor: "{colors.graphite-ink}"
    typography: "{typography.note}"
    rounded: "{rounded.xl}"
    padding: "16px 20px 16px 24px"
  terminal-badge:
    textColor: "{colors.console-blue}"
    typography: "{typography.mono}"
    rounded: "{rounded.full}"
    padding: "6px 16px 6px 12px"
---

# Design System: Brandon Visca

## Overview

**Creative North Star: "Le Carnet de Bord Sysadmin"**

Le site se lit comme le journal de terrain de quelqu'un qui administre vraiment son rack. Le corps de texte est un sans-serif chaleureux et arrondi (Figtree), justifié avec césure comme une page imprimée. Les notes en marge, les citations et les sous-titres passent à la main levée (Sriracha), comme griffonnés au stylo. Les commandes, les étiquettes et le prompt `~/homelab git:(main) $` sont en monospace (Cartograph CF). Trois écritures, trois rôles : ce que j'explique, ce que je note, ce que je tape.

Le support est un papier légèrement teinté, vert sauge en clair et bleu nuit de salle serveur en sombre, recouvert d'un grain fin et d'une grille de 50 px à peine visible qui s'efface vers le bas de la page. Une seule encre de couleur, le Bleu Console, sert aux liens, aux puces, aux focus et aux signaux d'état. La densité est modérée : colonne unique de 56 à 64 rem, cartes empilées, beaucoup d'air autour des titres.

Le système hérite du thème astro-devosfera. Ses effets décoratifs (verre dépoli, orbes aurora animés, halos qui suivent la souris, titres à reflet ou en dégradé, variantes amber/purple) ont été retirés le 2026-09-15 : ils ne servaient pas le carnet. Les Don'ts empêchent leur retour.

**Key Characteristics:**
- Trois voix typographiques à rôle strict : exposé (Figtree), annotation (Sriracha), machine (Cartograph).
- Une seule couleur d'accent, déclinée en opacités via `color-mix`, jamais une deuxième teinte.
- Papier teinté + grain + grille fantôme comme matière de fond.
- Signature terminal : badge prompt avec curseur clignotant et point d'état fixe.
- Deux thèmes complets (clair sauge, sombre rack) pilotés par `data-theme`.

## Colors

Palette à encre unique : un bleu de terminal posé sur un papier teinté, tout le reste est une opacité de ces deux pôles.

### Primary
- **Bleu Console** (#1158d1, thème clair) : liens au survol, soulignement des liens de prose (40 % au repos, 100 % au survol), puces de liste, point actif de la navigation, contour de focus en pointillé, prompt du badge terminal, sélection de texte (75 %).
- **Bleu Console de nuit** (#008fec, thème sombre) : même rôle, éclairci pour garder le contraste sur fond rack.

### Neutral
- **Papier Sauge** (#f2f5ec) : fond de page en thème clair. Le vert très léger évite le blanc clinique.
- **Encre Graphite** (#353538) : texte principal en clair, titres compris.
- **Lichen** (#bbc789) : token `muted` en clair. Utilisé presque uniquement à 5-15 % pour les fonds de cartes, de chips et de code inline, et pour la barre de défilement.
- **Trait de Plan** (#7cadff) : token `border` en clair, presque toujours à 15-40 % d'opacité (cartes, séparateurs, tableaux).
- **Nuit de Rack** (#10131a) : fond de page en thème sombre.
- **Blanc Craie** (#f6f7f8) : texte principal en sombre.
- **Puits Ardoise** (#212f3f) : token `muted` en sombre.
- **Trait Signal** (#2264e3) : token `border` en sombre.

### Named Rules
**La Règle de l'Encre Unique.** Toute couleur d'interface dérive de `--accent`, `--foreground`, `--muted`, `--border` ou `--background` via opacité ou `color-mix`. Aucune teinte Tailwind nommée (amber, purple, green hors diff de code) sur une nouvelle surface.

**La Règle du Trait Dilué.** `--border` n'est jamais appliqué à 100 % sur un conteneur : 15 à 40 % au repos, l'accent à 30-40 % au survol.

## Typography

**Display Font:** Figtree (fallback sans-serif)
**Body Font:** Figtree (fallback sans-serif)
**Annotation Font:** Sriracha (fallback cursive)
**Label/Mono Font:** Cartograph CF (fallback monospace)

**Character:** Un sans-serif géométrique et ouvert (Figtree, variable 300–900, OFL, auto-hébergé) pour tout ce qui est expliqué, contrarié par une écriture manuscrite pour ce qui est commenté et un monospace à ligatures pour ce qui est exécuté. Le contraste entre les trois est la personnalité du site.

### Hierarchy
- **Display** (700, 3rem → 4.5rem, 1.1, tracking serré) : titre du hero de la page d'accueil uniquement.
- **Headline** (700, 1.875rem → 2.75rem, 1.25, tracking serré) : H1 d'article, centré dans le panneau d'en-tête.
- **Title** (600, 1.125rem, 1.55) : titres des cartes d'articles, libellé du bouton CTA.
- **Body** (400, 1.0625rem dès 640 px, 1rem en dessous, 1.75) : prose d'article via `@tailwindcss/typography`. Texte courant limité à 70ch ; blocs de code, tableaux et paragraphes d'images gardent toute la colonne. Justifié avec `hyphens: auto` au-delà de 640 px, aligné à gauche en dessous.
- **Heading lg / md / sm** (700 / 700 / 600 ; 2rem / 1.5rem / 1.25rem) : titres de pages secondaires, libellés d'année, chiffres des archives et des tags.
- **Body UI** (400, 1rem, 1.6) : texte hors prose (titres de listes d'archives, noms de tags, descriptions d'états vides).
- **UI** (500, 0.8125rem) : boutons secondaires, badges de hero, descriptions compactes.
- **Note** (400, Sriracha, 1.05rem) : H3 de prose, `em` et `i`, citations en bloc. L'italique du site *est* Sriracha.
- **Label** (700, 0.875rem, 0.1em, capitales) : en-têtes de section de l'accueil (« À la une », « Récents »).
- **Mono** (400, Cartograph, 0.875rem) : code inline et blocs, badges de tags, sommaire, badge terminal.
- **Micro** (Cartograph, 0.75rem, capitales espacées selon le contexte) : marqueurs « end », « Précédent/Suivant », compteurs `[6/180]`, copyright. Plancher absolu : rien sous 12 px.

### Named Rules
**La Règle des Trois Écritures.** Figtree explique, Sriracha annote, Cartograph exécute. Ne jamais mettre du code en Sriracha, ni un paragraphe entier en Cartograph, ni un titre d'article en Sriracha.

**La Règle des Graisses Réelles.** Seules les graisses présentes dans un fichier s'affichent (`font-synthesis: none`). Figtree porte toute la hiérarchie en graisse ; Sriracha et Cartograph restent en 400, sans faux gras ni faux italique.

**La Règle de l'Italique Manuscrit.** Tout `em` bascule en Sriracha. Réserver l'emphase aux vraies apartés, sinon la page devient un cahier de brouillon.

## Layout

Colonne unique centrée, `max-width` 56rem (64rem à partir de 1280 px), gouttière latérale de 16 px. Pas de grille multi-colonnes hormis la paire « À la une » (2 colonnes dès 640 px) et la navigation précédent/suivant en bas d'article (2 colonnes).

Rythme vertical : sections de l'accueil séparées par 24 px, en-têtes de section suivis d'un filet horizontal qui prend l'espace restant, hero à 40-56 px en haut et 56-80 px en bas. L'en-tête d'article est un panneau centré (24-40 px de padding horizontal, 32-48 px vertical) suivi de la prose à 32 px.

Le header est collant ; transparent au repos, il reçoit un fond à 80 % et un flou en défilant. Sur mobile (< 640 px) la navigation passe dans un menu burger animé. Les ancres ont `scroll-margin-block: 5rem` pour ne pas passer sous le header.

## Elevation & Depth

Hybride : la profondeur vient d'abord du tonal (fonds `muted` à 5-10 %, bordures diluées), puis d'ombres teintées d'accent qui n'apparaissent qu'en réponse à un état (survol, focus). Au repos, les surfaces sont quasi plates. Le fond de page porte une profondeur atmosphérique : grille fantôme masquée en dégradé et grain en `overlay` à 9 %.

### Shadow Vocabulary
- **Halo de survol de carte** (`box-shadow: 0 10px 15px -3px color-mix(in srgb, var(--accent) 10%, transparent)`) : carte d'article survolée ou focalisée, avec translation de -2 px.
- **Halo CTA** (`box-shadow: 0 10px 15px -3px color-mix(in srgb, var(--accent) 15%, transparent)`) : bouton « Voir tous les articles » au survol.
- **Header défilé** (`box-shadow: 0 4px 30px rgba(0,0,0,0.05)`) : header collant après défilement.

### Named Rules
**La Règle du Repos Plat.** Aucune ombre au repos. L'ombre est une réponse à l'interaction, et elle prend la teinte de l'accent, jamais du noir pur (sauf header).

## Shapes

Coins franchement arrondis qui grandissent avec la taille du conteneur : 4 px pour les touches `kbd` et les surlignages de recherche, 6 px pour le code inline, 8 px pour les liens de navigation, chips et images de prose, 12 px pour le CTA et les citations (côté droit seulement, le côté gauche étant la barre d'accent de 3 px), 16 px pour cartes, sommaire et résultats de recherche, 24 px pour le panneau d'en-tête d'article. Pilules complètes pour les tags et le badge terminal. Les bordures sont fines (1 px) et diluées ; les tags de l'index utilisent un soulignement pointillé de 2 px comme un trait de crayon.

## Components

### Buttons
Rares et affirmés : un seul vrai bouton d'appel par page.
- **Shape:** coins doux (12 px).
- **CTA (« Voir tous les articles »):** fond Bleu Console à 10 %, bordure à 20 %, texte Bleu Console en gras, padding 16 px × 32 px, pleine largeur sur mobile.
- **Hover / Focus:** bordure et fond montent (60 % / 15 %), halo CTA, translation -2 px, flèche qui glisse de 4 px vers la droite. Focus : contour pointillé 2 px Bleu Console.
- **Icon buttons (thème, recherche):** carrés de 32 px, coins 8 px, fond accent à 8 % au survol. Le bouton recherche porte une touche `⌘K` à bordure inférieure épaissie.

### Chips
- **Tag d'article:** pilule, fond accent 5 %, bordure accent 20 %, Cartograph 12 px, `#` préfixé à 50 % d'opacité. Survol : fond 10 %, bordure 40 %.
- **Méta (auteur, date):** coins 8 px, fond `muted` 10 %, bordure 25 %, icône trait accent à 70 %.
- **Tag de l'index:** pas de fond, soulignement pointillé 2 px, icône `#`, remonte de 2 px au survol.

### Cards / Containers
- **Corner Style:** 16 px.
- **Background:** `muted` à 10 %, accent à 5 % au survol.
- **Shadow Strategy:** Repos Plat, halo de survol de carte (voir Elevation).
- **Border:** `border` à 25 %, accent à 40 % au survol.
- **Internal Padding:** 16 px, 20 px dès 640 px.
- **Comportement:** toute la carte est cliquable via un pseudo-élément étendu ; titre qui passe en accent ; description tronquée à 2 lignes à 75 % d'opacité.
- **À la une:** même carte, ton renforcé (bordure accent 30 %, fond accent 5 %). Pas d'autre teinte.

### Navigation
- **Style:** liens Figtree 14 px medium, padding 6 × 12 px, coins 8 px.
- **Hover:** texte accent, fond accent 8 %.
- **Active:** texte accent + point plein de 5,6 px centré sous le lien.
- **Mobile:** burger à trois traits animés dans un carré de 40 px, menu plein écran.
- **Logo:** nom « Brandon Visca » en texte plein, couleur encre.

### Prose de tutoriel
- **Liens:** soulignement dessiné en `background-image` de 1 px (accent 40 %), épaissi à 2 px et plein au survol.
- **Code inline:** Cartograph 14 px, fond `muted` 15 %, coins 6 px.
- **Blocs de code:** Shiki bi-thème, bordure 1 px, lignes `diff add/remove` sur fond vert/rouge à 20 %, lignes surlignées ardoise 20 %.
- **Citations:** barre gauche accent 3 px, fond accent 5 %, Sriracha 1.05rem, coins droits 12 px.
- **Images:** centrées, bordure 1 px, coins 8 px, 760 px et 80vh maximum.
- **Sommaire (`details`):** carte 16 px sans fond, icône liste en masque SVG, chevron qui pivote, liens Cartograph 13 px avec puce ronde accent.

### Badge Terminal (signature)
Pilule Cartograph en haut du hero : point d'état fixe en accent, prompt `~/homelab` en accent gras, `git:(main)` à 55 %, `$` à 35 %, curseur `▌` qui clignote en `step-end` toutes les 1,1 s (coupé sous `prefers-reduced-motion`). Fond accent 4 % mêlé au papier, contour simple dilué, aucun flou ni lueur. C'est la seule animation continue du site. C'est l'élément d'identité le plus fort du site.

### Marqueur de fin d'article
Filets horizontaux en dégradé qui convergent vers un point accent à 50 % et le mot `end` en Cartograph micro capitales. Clôt la prose comme une ligne de log.

## Do's and Don'ts

### Do:
- **Do** dériver toute nouvelle couleur des cinq tokens CSS (`--background`, `--foreground`, `--accent`, `--muted`, `--border`) par opacité ou `color-mix`, et vérifier les deux thèmes.
- **Do** respecter la Règle des Trois Écritures : Figtree pour l'exposé, Sriracha pour l'annotation, Cartograph pour tout ce qui se tape ou s'étiquette.
- **Do** garder les bordures diluées (15-40 %) et les ombres teintées d'accent, uniquement sur état.
- **Do** réutiliser le vocabulaire terminal (prompt, compteur `[n/total]`, marqueur `end`, `kbd`) pour les nouveaux éléments de navigation ou d'état.
- **Do** placer les overrides dans `src/styles/custom.css` et consigner toute modif de fichier thème dans `THEME_CUSTOMIZATIONS.md`.
- **Do** fournir un focus visible en pointillé 2 px accent sur tout élément interactif.
- **Do** garder le texte courant des articles à 70ch maximum et n'utiliser que les tailles de l'échelle typographique (frontmatter).
- **Do** exporter toute nouvelle graisse Figtree utilisée par les images OG dans `src/assets/fonts/og/` (Satori ne lit ni woff2 ni police variable).

### Don't:
- **Don't** utiliser le verre dépoli (`backdrop-filter`) comme décor. Réservé aux surfaces qui flottent au-dessus du contenu défilant : header collant, player compact, menu mobile, modale de recherche, bouton retour en haut.
- **Don't** mettre de texte en dégradé (`background-clip: text`), animé ou non. Titres, logo et libellés sont en couleur pleine.
- **Don't** réintroduire de teinte hors tokens (amber, purple…) pour distinguer une variante : jouer sur l'opacité de l'accent.
- **Don't** ajouter de halo qui suit le curseur, d'orbe aurora, de lueur à décalage nul (`0 0 Npx`) ni d'animation infinie décorative.
- **Don't** référencer `--muted-foreground` : la variable n'existe pas. Texte secondaire = `color-mix(in srgb, var(--foreground) 65%, transparent)`.
- **Don't** utiliser d'easing à rebond (`cubic-bezier(0.34, 1.56, …)`) : préférer `cubic-bezier(0.25, 1, 0.5, 1)`.
- **Don't** descendre sous 12 px (0.75rem), ni poser un paragraphe entier en Cartograph (le monospace est réservé au code et aux étiquettes).
- **Don't** mettre de H1 dans le corps d'un article : le panneau d'en-tête génère déjà le titre.
- **Don't** justifier le texte sous 640 px (rivières) ni désactiver la césure au-dessus.
