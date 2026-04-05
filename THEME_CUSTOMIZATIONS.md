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

- All components in `src/components/`
- All layouts in `src/layouts/`
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

### `src/styles/custom.css` *(nouveau fichier)*

**Reason**: Layer CSS isolé pour les overrides brandonvisca.com — jamais modifié par upstream.

**Merge strategy**: Aucun conflit possible, fichier inexistant upstream.
