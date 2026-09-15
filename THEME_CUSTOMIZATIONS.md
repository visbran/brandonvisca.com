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
