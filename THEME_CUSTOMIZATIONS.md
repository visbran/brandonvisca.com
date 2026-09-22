# Theme Customizations

Tracks every file modified from upstream [0xdres/astro-devosfera](https://github.com/0xdres/astro-devosfera).

Read this file before merging upstream updates — each entry is a potential conflict point.

---

## Modified files

### `src/utils/getPath.ts`

**Reason**: WordPress URLs are `/{slug}/`, not `/posts/{slug}/`. Changed `includeBase` default to `false`.

**Diff**:
```diff
- export function getPath(id, filePath, includeBase = true) {
+ export function getPath(id, filePath, includeBase = false) {
```

**Merge strategy**: Keep our version. Upstream changes to this file need manual review.

---

### `src/pages/` directory structure

**Reason**: Moved `src/pages/posts/` → `src/pages/` to generate URLs at `/{slug}/`.

**Change**: The `[...slug]/index.astro` and `[...page].astro` files that were under `posts/` are now directly under `pages/`.

**Merge strategy**: Upstream changes to page routing need to be applied to the new path.

---

### `src/config.ts`

**Reason**: Site configuration (author, URL, features). Fully replaced with brandonvisca.com values.

**Merge strategy**: On upstream update, check if new config keys were added and port them manually.

---

### `src/constants.ts`

**Reason**: Social links updated for Brandon Visca accounts.

**Merge strategy**: On upstream update, check if new icon imports or link types were added.

---

### `src/pages/about.md`

**Reason**: Content page — CV / à propos.

**Merge strategy**: Upstream rarely touches this. Safe to ignore upstream changes.

---

### `src/styles/custom.css` *(new file)*

**Reason**: Custom CSS overrides added without touching `global.css`.

**Merge strategy**: No conflict risk — this file doesn't exist upstream.

---

## Untouched upstream files

The following files are **not modified** and will merge cleanly:

- Components in `src/components/` **except** those listed in this file (Header, MobileMenu, Card, Footer, Pagination, Breadcrumb, ShareLinks, IntroAudio, IntroAudioCompact)
- Layouts in `src/layouts/` **except** `PostDetails.astro`, `Layout.astro`, `AboutLayout.astro`
- `src/content.config.ts`
- `src/utils/` (except `getPath.ts`)
- `astro.config.ts`
- `src/styles/global.css`, `typography.css`
- `package.json` (update carefully — check for dependency conflicts)

---

### `src/pages/blog/[...page].astro` *(déplacé depuis `src/pages/posts/[...page].astro`)*

**Reason**: URL `/blog/` au lieu de `/posts/` pour éviter le conflit avec `index.astro` et coller aux URLs WordPress.

**Changes**:
- Titre page : `Posts` → `Articles`
- Description hero : anglais → français
- Badge count : `{n} posts` → `{n} articles`

**Merge strategy**: En cas d'update upstream de `src/pages/posts/[...page].astro`, appliquer les diffs manuellement sur ce fichier.

---

### `src/styles/global.css`

**Reason**: Ajout de `@import './custom.css';` en fin de fichier pour le layer de customisation.

**Merge strategy**: Sur update upstream, vérifier que la ligne d'import est toujours présente en dernière position.

---

### `src/layouts/PostDetails.astro`

**Reason**: Corrections Schema.org JSON-LD (audit SEO 2026-05-06).

**Changes**:
- `publisher` changé de `Person` à `Organization` avec `logo` (ImageObject)
- Ajout de `inLanguage: "fr"`, `mainEntityOfPage`, `articleSection`
- `author` Person enrichi avec `jobTitle`, `sameAs`, `knowsAbout`
- `image` converti en `ImageObject` avec `width`/`height`
- `dateModified` toujours émis (fallback sur `datePublished`)
- `BreadcrumbList` corrigé pour matcher les URLs réelles (`/{slug}/`)

**Merge strategy**: Sur update upstream, conserver nos modifications JSON-LD ou fusionner manuellement.

---

### `src/layouts/Layout.astro`

**Reason**: Corrections Schema.org JSON-LD (audit SEO 2026-05-06).

**Changes**:
- `WebSite` schema désormais émis sur **toutes** les pages (y compris articles)
- Ajout de `inLanguage: "fr"`
- Suppression de la propriété `author` non standard sur `WebSite`

**Merge strategy**: Sur update upstream, conserver la logique `webSiteSchema` inconditionnelle.

---

### `src/styles/custom.css` *(nouveau fichier)*

**Reason**: Layer CSS isolé pour les overrides brandonvisca.com — jamais modifié par upstream.

**Merge strategy**: Aucun conflit possible, fichier inexistant upstream.

---

### `src/components/Header.astro`

**Reason**: Ajout d'un lien "CV" dans le menu principal de navigation.

**Changes**:
- Ajout d'un élément `<li>` avec lien vers `/cv` dans la liste de liens desktop (entre "À propos" et "Recherche")

**Merge strategy**: Sur update upstream, conserver le lien CV. Fusionner manuellement si le menu change de structure.

---

### `public/_headers`

**Reason**: Headers HTTP durcis pour Cloudflare Pages (audit sécurité OWASP 2026-05-17).

**Changes**:
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy` : caméra, micro, géo, payment, USB bloqués
- `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`
- `Content-Security-Policy` : `script-src 'self' 'unsafe-inline' 'wasm-unsafe-eval'`
  - `'unsafe-inline'` conservé — approche hash-based abandonnée (minification non-déterministe local ≠ CF Pages)
  - `'wasm-unsafe-eval'` requis par Pagefind (WebAssembly)
  - `frame-src` : YouTube uniquement
  - `media-src` : fluxfm.streamabc.net + lowtechguys.com (player audio + vidéo article)

**Merge strategy**: Fichier inexistant upstream — aucun conflit. À mettre à jour manuellement si nouveaux scripts externes ou iframes ajoutés.

---

### `src/components/MobileMenu.astro`

**Reason**: Ajout d'un lien "CV" dans le menu mobile de navigation.

**Changes**:
- Ajout d'un élément `<a href="/cv">` dans la liste de liens mobile (entre "À propos" et "Archives")
- Ajustement des indices `style="--i:N"` pour les éléments suivants (Archives → 4, Galleries → 5)

**Merge strategy**: Sur update upstream, conserver le lien CV et les indices de délai d'animation.

---

### Passe « quieter » — suppression des effets décoratifs (2026-09-15)

**Reason**: Aligner le thème sur `DESIGN.md` (« Le Carnet de Bord Sysadmin ») : encre unique, repos plat, pas de texte en dégradé, pas de verre décoratif, pas d'animation infinie décorative, pas de halo qui suit la souris.

**Files & changes**:
- `src/pages/index.astro` — titre hero plein (shimmer supprimé), badge terminal sans blur/lueur, point d'état fixe (plus d'`animate-ping`), curseur `▌` conservé + `prefers-reduced-motion`, script glow des cartes supprimé, halo CTA adouci.
- `src/components/Card.astro` — plus de `backdrop-blur`, plus de glow curseur, variantes amber/purple remplacées par l'accent (featured = `border-accent/30 bg-accent/5`).
- `src/components/Header.astro` — logo en couleur pleine, lueur du point actif supprimée, blur du header défilé réduit (12px, sans saturate), CSS mort du logo SVG supprimé, `--muted-foreground` (non défini) remplacé par `color-mix(foreground 65%)`.
- `src/layouts/PostDetails.astro` — titre plein, panneau d'en-tête et chips sans blur, aurora `.post-hero-bg` / `.post-nav-bg` supprimées, marqueur `end` sans lueur.
- `src/pages/blog/[...page].astro`, `src/pages/tags/index.astro`, `src/pages/archives/index.astro` — orbes aurora animés, halos souris (hero, bordures de cartes) et leur JS supprimés, `.glow-text` et libellés d'année en couleur pleine, badges sans blur, empty state sans flottement, lueurs `text-shadow`/`box-shadow` de survol supprimées.
- `src/layouts/AboutLayout.astro` — orbes, halo avatar, anneau rotatif et script souris/ripple supprimés ; anneau avatar statique ; nom en couleur pleine ; badges sans blur.
- `src/components/Footer.astro`, `Pagination.astro`, `Breadcrumb.astro`, `ShareLinks.astro`, `IntroAudio.astro`, `IntroAudioCompact.astro` — blur décoratif, dégradés et lueurs supprimés ; easing à rebond de la pagination remplacé par `cubic-bezier(0.25, 1, 0.5, 1)` ; animation d'onde audio respecte `prefers-reduced-motion`.

**Conservé volontairement** : blur fonctionnel des surfaces flottantes (header collant, player compact du header, menu mobile, modale de recherche, bouton retour en haut), grain et grille de fond, curseur clignotant du badge terminal.

**Merge strategy**: Sur update upstream de ces fichiers, ne pas réintroduire les effets listés ; appliquer les autres diffs manuellement.

---

### Passe « polish » — cohérence FR et défauts locaux (2026-09-15)

**Files & changes**:
- `src/components/Datetime.astro` — import `dayjs/locale/fr` (la locale n'était jamais chargée → mois en anglais), format `D MMM YYYY` en FR (« 15 sept. 2026 »).
- `Header.astro`, `MobileMenu.astro`, `BackToTopButton.astro`, `Pagination.astro`, `SearchModal.astro` (aussi : titre plein, rebond et halos supprimés), `IntroAudio.astro`, `IntroAudioCompact.astro`, `src/scripts/theme.ts`, `PostDetails.astro`, `src/pages/index.astro` — libellés visibles et accessibles traduits (Aller au contenu, Recherche, Mode sombre/clair, Précédent/Suivant, Copier/Copié, Revenir en haut, Page précédente/suivante, Flux RSS, Thème clair/sombre…).
- `src/pages/blog/[...page].astro` — `[&>li]:my-0` sur la grille : les marges des cartes doublaient l'écart vertical.
- `src/pages/index.astro` — compteur `[6/180]` sans espace parasite.
- `Header.astro` — fond du bouton recherche ramené à `muted` 15 % (trop lourd en thème clair).

**Merge strategy**: Conserver les libellés FR et l'import de locale sur update upstream.

---

### Passe « typeset » — vraies graisses, mesure, échelle (2026-09-15)

**Reason**: Wotfard n'était livré qu'en 400 statique : tout le gras du site était synthétisé (faux gras), Sriracha recevait un faux italique, la prose courait sur ~120 caractères par ligne, et 18 tailles arbitraires coexistaient (dont des libellés à 9–11 px).

**Files & changes**:
- `astro.config.ts` — Wotfard remplacée par **Figtree variable 300–900** (OFL, `@fontsource-variable/figtree` 5.3.0, sous-ensembles latin + latin-ext avec `unicodeRange`) ; Cascadia Code supprimée (utilisée seulement par l'ancien logo devosfera, désactivé).
- `src/assets/fonts/` — ajout `figtree-latin-wght-normal.woff2`, `figtree-latin-ext-wght-normal.woff2`, `figtree-OFL.txt`, `og/figtree-latin-{400,600,700,900}-normal.woff` ; suppression `wotfard.woff2`, `wotfard.ttf`, `cascadia-code.woff2`.
- `src/utils/loadGoogleFont.ts` — images OG (Satori) en Figtree statique réelle par graisse (Satori ne lit ni woff2 ni variable).
- `src/layouts/Layout.astro` — `<Font>` Figtree préchargée, Cascadia retirée.
- `src/styles/global.css` — `--font-app` → Figtree ; `font-synthesis: none` ; `em`/`i` Sriracha en `font-style: normal`.
- `src/styles/typography.css` — prose à 17 px dès 640 px ; texte courant limité à 70ch (code, tableaux, images pleine largeur) ; H3 sans italique ; sommaire en 0.8125rem / 0.75rem.
- `PostDetails.astro`, `Footer.astro`, `ShareLinks.astro`, `BackToTopButton.astro` — plancher 12 px, contraste des micro-libellés relevé ; description du footer en Figtree (plus en monospace) ; libellé « top » redondant supprimé.
- `Header`, `IntroAudio`, `IntroAudioCompact`, `MobileMenu`, `SearchModal`, `GalleryEmbed`, `AboutLayout`, pages `archives`, `blog`, `tags`, `galleries` — tailles consolidées sur l'échelle de `DESIGN.md` (0.75 / 0.8125 / 0.875 / 1 / 1.0625 / 1.25 / 1.5 / 2 / 2.75rem).

**Merge strategy**: Sur update upstream, conserver Figtree et l'échelle ; ne pas réintroduire de police mono-graisse utilisée en gras.

---

### Correctif largeur des articles (2026-09-15)

**Reason**: La limite de 70ch ajoutée par la passe typeset laissait ~220 px vides à droite du texte sur desktop, désalignés de l'en-tête d'article pleine largeur.

**Change**: `src/styles/typography.css` — suppression de la limite `max-width: 70ch` sur la prose ; le texte reprend toute la colonne. Taille de prose 17 px conservée.

---

### Passe « audit impeccable » — contraste, focus, décors, perf (2026-09-17)

**Reason**: Audit technique (a11y, perf, responsive, intégrité). 21 cibles sous WCAG AA (texte secondaire entre 1,73:1 et 4,02:1), indicateurs de focus à 2,25:1, modale de recherche sans piège de focus (Tab s'échappait malgré `aria-modal`), 5 animations infinies tournant en permanence dans une modale `visibility: hidden`, halos et orbes décoratifs bannis par `DESIGN.md`, et `sizes` des images d'article calculé sur la largeur intrinsèque (jusqu'à 2880 px) au lieu des 760 px du corps de texte.

**Files & changes**:
- `src/styles/global.css` — nouveau token `--text-soft` (72 % clair / 65 % sombre, seul palier qui tienne 4,5:1 sur le fond le plus clair du site), exposé en `--color-soft` donc en utilitaire `text-soft` ; `::placeholder` repassé dessus (35 % = 1,94:1).
- `Header.astro`, `Breadcrumb.astro`, `Footer.astro`, `Pagination.astro`, `ShareLinks.astro`, `EditPost.astro`, `PostDetails.astro`, `Card.astro`, `Datetime.astro`, `GalleryEmbed.astro`, `GalleryCard.astro`, `SearchModal.astro`, pages `blog`/`archives`/`tags`/`galleries`/`search`, `typography.css` — tous les `text-foreground/40|50|60|65|70` et `opacity: 0.4–0.7` sur du texte remplacés par `text-soft` / `var(--text-soft)`. Les paliers `/75` et `/80` passent AA et sont conservés comme palier d'emphase supérieur.
- `IntroAudio.astro`, `archives/index.astro`, `tags/index.astro` — libellés accent à 0,35–0,55 d'opacité remontés (l'accent n'atteint 4,5:1 qu'à 100 %, 3:1 à 80 % pour le grand texte) ; `.post-day` (1,5 rem/800 = grand texte) passe de 0,35 à 0,70.
- `Header.astro` — indicateur de focus en double anneau (fond + accent plein = 5,70:1 / 5,43:1) au lieu d'un accent à 50 % (2,25:1) ; `aria-label="auto"` remplacé par un libellé d'action.
- `src/scripts/theme.ts` — `<meta name="theme-color">` alimenté depuis le fond calculé, écouté aussi sur `#theme-btn-mobile` ; l'écoute de `prefers-color-scheme` ne suit plus le système si l'utilisateur a choisi explicitement (elle écrasait son choix et l'écrivait dans `localStorage`) ; `initialColorScheme` laissé à `""` (thème du système) **des deux côtés** — voir la note ci-dessous ; libellés de bouton reformulés comme des actions.
- `src/layouts/Layout.astro` — `<meta name="theme-color">` ajouté (le tag n'existait pas : le `querySelector` de `theme.ts` ne trouvait rien). Sa valeur statique vise le thème sombre et le script inline la réécrit dès qu'il connaît le thème retenu, sinon un visiteur en thème clair gardait une barre sombre jusqu'à l'exécution du module.

**Note — `initialColorScheme` : pourquoi `""` et non `"dark"`.** Le module `theme.ts` fait `window.theme?.themeValue ?? getPreferTheme()` : il reprend la valeur **peinte par le script inline** de `Layout.astro`, et son propre `initialColorScheme` ne sert que de repli si `window.theme` est absent. Les deux scripts ne peuvent donc pas « se contredire », et il n'y a pas de flash à corriger. Les figer à `"dark"` a un effet de bord réel : le visiteur dont le système est en clair se voit imposer le thème sombre à la première visite, alors que le site suivait le système jusqu'ici. `""` des deux côtés conserve ce comportement et rend effective l'écoute de `prefers-color-scheme`.
- `src/components/SearchModal.astro` — piège de focus cyclique (Tab/Shift+Tab) et retour du focus au déclencheur ; suppression des 3 orbes `blur(70px)`, des 5 étincelles, de la lueur de bord en `conic-gradient` animé et de la lueur suiveuse de souris — soit 5 animations infinies et 2 `will-change` qui tournaient sur chaque page, la modale restant `visibility: hidden` (seul `display: none` arrête une animation) ; `prefers-reduced-motion` ajouté.
- `src/pages/search.astro` — même retrait (3 orbes animés, lueur suiveuse de souris, lueur de bord) et suppression des deux blocs JS de suivi de souris devenus sans cible.
- `src/pages/*/index.astro` (tags, archives, blog, search, galleries) — `.glow-text` supprimé : `background-clip: text` + `drop-shadow(0 0 25px)` sur les titres, banni par `DESIGN.md`.
- `src/utils/og-templates/post.js` et `site.js` — réécrits sur la palette du site : rack-night `#10131a`, accent `#008fec`, grille fantôme en signature (au lieu de dégradés violet/indigo/rose flous), Figtree, « Par Brandon Visca » en français, plus d'`textShadow`.
- `src/utils/prose-image-sizes.mjs` (nouveau) + `astro.config.ts` — intégration de build qui recadre `sizes="(min-width: Npx) Npx, 100vw"` sur `(min-width: 792px) 760px, 100vw` quand `N` dépasse la largeur du corps de texte. Les plugins rehype s'exécutent avant celui qui produit `sizes`, et les remark ne connaissent pas encore la largeur résolue : la correction se fait donc sur le HTML écrit. 42 images sur 14 pages.
- `astro.config.ts` — filtre sitemap étendu aux galeries désactivées ; `endsWith("/archives")` remplacé par `includes` (les URLs du sitemap portent un slash final, le test ne matchait jamais).
- `IntroAudio.astro` — `wave-bounce` et la barre de progression animés en `transform: scaleY` / `scaleX` (avec `overflow: hidden` et rayon pilule sur la piste) : `height` et `width` déclenchaient une mise en page à chaque frame.
- Rayons alignés sur l'échelle 4/6/8/12/16/24/pilule (0.2/0.35/0.45/0.6/0.625/0.85/1.25 rem et 10 px supprimés) ; halos sans décalage `0 0 Npx` retirés de `MobileMenu`, `typography.css`, `SearchModal`, `blog/[...page]`, `search`, et des piles `box-shadow` de `archives`/`tags`.

**Conservé volontairement**: `git:(main)` (0,55) et `$` (0,35) du badge terminal de `index.astro`, épinglés par `DESIGN.md` ; séparateurs et puces décoratives ; état désactivé de `Pagination` (exempté par WCAG 1.4.3) ; `.shortcuts-sep` (0,3). Deux faux positifs du détecteur à ne pas « corriger » : `codex-grid-background` (la grille fantôme est une signature documentée) et `bounce-easing` sur `wave-bounce` (les keyframes ne dépassent jamais leur cible, seul le nom trompe).

**Merge strategy**: Sur update upstream, conserver le token `--text-soft`, le double anneau de focus, le piège de focus et le retrait des décors ; ne pas réintroduire les orbes, lueurs, étincelles ni le texte en dégradé.

---

### Passe « palette claire » — le fond quitte le sauge (2026-09-17)

**Reason**: Le fond clair `#f2f5ec` (Papier Sauge) était trop peu saturé pour se lire comme un choix : à cette luminosité la teinte verte passe pour du blanc sale, pas pour du papier teinté. Mesuré sur le rendu réel, la teinte ne se distingue qu'à quelques unités RVB du neutre. Le fond adopté est `#f1f4f8` (Papier Calque), un blanc très légèrement bleuté (teinte oklch 255°, chroma 0,006).

**Pourquoi bleu et pas neutre ni chaud** : les fonds de cartes sont lavés à l'accent (`bg-accent/5`, `color-mix(accent 4%)`). Sur un sol vert ou crème, ce lavis bleu refroidit les cartes et crée un clash de température visible ; sur un sol de la même famille de teinte que l'encre, cartes et fond se lisent comme un seul plan. Le neutre absolu `#f6f6f6` a été écarté : c'est le gris de gabarit par défaut, plus générique encore que le sauge.

**Files & changes**:
- `src/styles/global.css` — thème clair : `--background: #f1f4f8`, `--muted: #c3cfdf` (Brume d'Ardoise). Commentaire de `--text-soft` recalculé : sur le nouveau fond, 72 % donne 4,88:1 (AA), 70 % 4,62:1, 65 % 4,00:1 — le seuil de 72 % reste donc imposé par le thème clair.
- `src/layouts/Layout.astro` — `THEME_COLORS.light` et la réécriture de `theme-color` du script inline passent à `#f1f4f8`. Sans ça, la barre système gardait l'ancien vert pendant la première peinture.
- `DESIGN.md` — jetons renommés : `sage-paper` → `tracing-paper` (Papier Calque), `lichen` → `slate-mist` (Brume d'Ardoise) ; prose (Overview, Key Characteristics, section Neutral) mise à jour ; les deux `{colors.lichen}` des composants `card-post` et `code-inline` suivent.
- `.impeccable/design.json` — `extensions.colorMeta` : clés, `displayName`, `canonical` et `tonalRamp` des deux jetons refaits sur la teinte 255/256 ; les littéraux de repli des composants (`var(--muted, …)`, `var(--background, …)`) et le récit suivent, pour que l'artefact ne contredise pas `DESIGN.md`.

**Vérification** (mesurée sur le rendu, pas déduite) : corps 11,08:1, texte secondaire 4,88:1, accent 5,70:1 en clair ; thème sombre inchangé. Aucune autre occurrence des anciennes valeurs dans le dépôt.

**Merge strategy**: Sur update upstream, conserver les valeurs du thème clair. Si upstream ajoute des surfaces teintées à l'accent, vérifier qu'elles restent dans la famille de teinte du fond.

---

### Mesure d'audience Tianji, en first-party (2026-09-22)

**Reason**: Remplacer Google Analytics par l'instance Tianji auto-hébergée (LXC 108), sans exposer Tianji sur Internet. Le navigateur ne parle qu'à `brandonvisca.com/stats/*` ; une Pages Function relaie vers Tianji via un tunnel Cloudflare protégé par un jeton de service Cloudflare Access.

**Files & changes**:
- `src/layouts/Layout.astro` — balise `<script src="/stats/tracker.js">` émise seulement si `PUBLIC_TIANJI_WEBSITE_ID` est défini. `data-domains` limite le suivi aux domaines de production (rien en local ni sur les previews) ; `data-do-not-track` respecte le réglage DNT. Le tracker s'accroche à `history.pushState`, donc les navigations du `ClientRouter` sont comptées sans relancer le script.
- `astro.config.ts` — variable `PUBLIC_TIANJI_WEBSITE_ID` ajoutée au schéma `env` (publique, optionnelle).
- `functions/stats/[[path]].ts` (nouveau, hors thème) — proxy limité à `tracker.js`, `api/website/send` et `api/website/batch` ; tout le reste renvoie 404. Transmet l'IP du visiteur en `x-forwarded-for` pour la géolocalisation, retire `set-cookie`.

- `.github/workflows/deploy.yml` — `PUBLIC_TIANJI_WEBSITE_ID` passé à l'étape de build. Le site est construit par GitHub Actions puis poussé avec `wrangler pages deploy` : les variables d'environnement de Cloudflare Pages ne sont lues qu'à l'exécution de la Function, jamais au build.

**Infra (2026-09-22)** : tunnel Cloudflare vers Tianji sur le LXC 108, nom d'hôte protégé par une application Access en Service Auth. Identifiants et jeton : tableau de bord Cloudflare Zero Trust. Le jeton de service expire au bout d'un an — à renouveler avant le 2027-09-22. Vérifié à la mise en ligne : 403 sans jeton, 200 avec.

**Géolocalisation** : Tianji fait confiance à `cf-connecting-ip` en priorité, or Cloudflare réécrit cet en-tête sur les sous-requêtes d'un Worker — tous les visiteurs atterrissaient aux États-Unis. La Function envoie donc l'IP dans `x-visitor-ip`, et le service `tianji` porte `CLIENT_IP_HEADER=x-visitor-ip` (surcharge systemd `client-ip.conf` sur le LXC). **Si Tianji est réinstallé, remettre cette variable**, sinon les pays redeviennent faux.

**CSP** : aucune modification — le script et les requêtes sont same-origin, couverts par `'self'`.

**Merge strategy**: Sur update upstream, conserver le bloc Tianji du `<head>` et l'entrée du schéma `env`.

---

### Image OG : espace manquant avant le nom de l'auteur (2026-09-22)

**Reason** : les images OG générées affichaient « ParBrandon Visca ». Satori supprime l'espace final
d'un enfant texte quand le suivant est un élément : `"Par "` perdait son espace au rendu.

**Files & changes** :
- `src/utils/og-templates/post.js` — `"Par "` remplacé par `"Par\u00a0"` (espace insécable, conservé
  par Satori). La police est déjà chargée pour ces caractères, rien d'autre à changer.

**Au passage** : l'issue `ogImage_specific` du backlog SEO est sans objet. Chaque article a déjà sa
propre image de partage, générée au build (`/{slug}/index.png` via `generateOgImages.ts`), référencée
par `og:image` **et** `twitter:image`. Aucun article n'a d'`ogImage` personnalisée : 64 ont un champ
vide, 129 n'ont pas le champ. Remplir ce champ remplacerait une image générée et cohérente par une
image figée à maintenir — à réserver à une bannière vraiment travaillée.

**Merge strategy** : sur update upstream, conserver l'espace insécable.
