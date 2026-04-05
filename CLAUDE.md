# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project context

**brandonvisca.com** — French blog on self-hosting, homelab, and digital independence. Rebuilt in April 2026 after a WordPress data loss incident. All article content lives in the Obsidian vault at `~/Documents/brandon-knowledge/Content/Articles/`.

This is a **fork** of [astro-devosfera](https://github.com/0xdres/astro-devosfera) (itself a fork of AstroPaper). Upstream is tracked as a git remote for future updates.

---

## Commands

```bash
pnpm dev          # Start dev server (http://localhost:4321)
pnpm build        # Type-check + build + generate Pagefind index
pnpm preview      # Preview production build locally
pnpm lint         # ESLint
pnpm format       # Prettier (write)
pnpm format:check # Prettier (check only)
```

> `pnpm build` runs `astro check && astro build && pagefind --site dist`. Pagefind search only works after a full build — run `pnpm build && pnpm preview` to test search locally.

---

## Architecture overview

### Theme fork strategy

This repo is a fork of upstream. To get future theme updates:

```bash
git fetch upstream
git merge upstream/main --no-ff
# Resolve conflicts in THEME_CUSTOMIZATIONS.md to understand what we changed
```

**Two categories of files:**

| Category | Files | Rule |
|---|---|---|
| **Safe to edit freely** | `src/config.ts`, `src/constants.ts`, `src/data/blog/`, `src/data/galleries/`, `src/pages/about.md`, `public/`, `src/styles/custom.css` | These are content/config — no upstream conflict risk |
| **Frozen (theme core)** | Everything else in `src/` | Only modify when strictly necessary. Document every change in `THEME_CUSTOMIZATIONS.md` |

### URL structure

WordPress URLs were `/{slug}/`. The theme default is `/posts/{slug}/`.

**Our choice**: posts live at `/{slug}/` to preserve SEO equity. Route mapping:

| Route | File | Description |
|---|---|---|
| `/{slug}/` | `src/pages/[...slug]/index.astro` | Article individuel |
| `/blog/` | `src/pages/blog/[...page].astro` | Liste paginée (page 1) |
| `/blog/2`, `/blog/3`… | `src/pages/blog/[...page].astro` | Pagination |
| `/` | `src/pages/index.astro` | Homepage |
| `/tags/{tag}/` | `src/pages/tags/` | Articles par tag |
| `/archives/` | `src/pages/archives/` | Archive chronologique |

This required patching `getPath.ts` (default `includeBase=false`) and splitting the theme's `src/pages/posts/` into `src/pages/[...slug]/` + `src/pages/blog/`. See `THEME_CUSTOMIZATIONS.md`.

Cloudflare Pages `public/_redirects` handles any remaining old URL mismatches.

### Content pipeline

```
Vault markdown (~/Documents/brandon-knowledge/Content/Articles/04-Publies/)
    ↓  (frontmatter conversion)
src/data/blog/{slug}.md
    ↓  (Astro content collections)
/{slug}/  (static HTML)
```

### Key files

- `src/config.ts` — all site-level config (title, author, features on/off)
- `src/constants.ts` — social links, share links
- `src/content.config.ts` — Zod schema for blog posts (defines required frontmatter fields)
- `src/data/blog/` — all article markdown files
- `public/_redirects` — Cloudflare Pages 301 redirects (old WP URLs → new URLs)
- `THEME_CUSTOMIZATIONS.md` — diff log of every upstream file we've touched

---

## Blog post frontmatter

Required schema (defined in `src/content.config.ts`):

```yaml
---
title: "Your title here"
description: "Meta description, 120-155 chars"
pubDatetime: 2025-10-22T15:44:27+02:00
modDatetime: 2026-01-10T10:00:00+02:00   # optional, for updated articles
author: Brandon Visca                      # optional, defaults to SITE.author
tags:
  - homelab
  - docker
featured: false                            # optional, shows in hero section
draft: false                               # optional
ogImage: ""                                # optional, defaults to auto-generated OG
canonicalURL: ""                           # optional
---
```

**Tag conventions**: lowercase, kebab-case, French preferred (`auto-hebergement`, `homelab`, `docker`, `macos`, `linux`, `reseau`, `securite`, `windows`).

---

## Importing articles from the vault

Articles live in `~/Documents/brandon-knowledge/Content/Articles/04-Publies/` as markdown with WordPress-style frontmatter. When importing:

1. Copy the file to `src/data/blog/`
2. Convert frontmatter:
   - `date` → `pubDatetime` (keep ISO 8601 format)
   - `status: publish` → remove (no equivalent)
   - `type: post` → remove
   - Add `description` if missing (required)
   - Keep `tags` array as-is (lowercase)
3. Clean up WordPress shortcodes or HTML remnants in the body
4. Run `pnpm build` to validate — Zod will report missing required fields

---

## Customizing the theme safely

### CSS overrides

Add custom CSS in `src/styles/custom.css` (imported at the bottom of `src/styles/global.css`). Use CSS custom properties to override theme tokens — never edit `global.css` or `typography.css` directly.

### Config changes

All visual features are toggled in `src/config.ts`:
- `backdropEffects.cursorGlow` / `grain` — background effects
- `showGalleries` — enable/disable gallery section
- `introAudio` — audio player in hero
- `heroTerminalPrompt` — animated prompt text

### New pages

Add static pages in `src/pages/` as `.astro` or `.md` files. Use `Layout.astro` or `AboutLayout.astro` as the base.

---

## Deployment

**Target**: Cloudflare Pages  
**Trigger**: push to `main` branch  
**Build command**: `pnpm build`  
**Output directory**: `dist`  
**Node version**: 20+

Environment variables needed on Cloudflare Pages:
- `PUBLIC_GOOGLE_SITE_VERIFICATION` — optional, for GSC verification

---

## Redirects (Cloudflare Pages)

File: `public/_redirects`

Format:
```
/old-wordpress-slug/   /new-slug/  301
```

Add a redirect entry for every URL that changed structure between WordPress and this site. Cloudflare Pages processes this file automatically at the CDN edge.
