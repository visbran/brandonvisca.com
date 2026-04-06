# brandonvisca.com

Source code of [brandonvisca.com](https://brandonvisca.com) — a French blog about self-hosting, homelab, and digital independence. Built with [Astro](https://astro.build) on top of the [astro-devosfera](https://github.com/0xdres/astro-devosfera) fork of [AstroPaper](https://github.com/satnaing/astro-paper).

> **Note:** This is a personal blog. Feel free to fork and adapt it for your own use — delete the articles in `src/data/blog/` and edit `src/config.ts` to get started.

---

## Stack

| Layer | Tool |
| :--- | :--- |
| Framework | Astro 6 |
| Styling | Tailwind CSS 4 |
| Search | Pagefind (static index) |
| Deployment | Cloudflare Pages (direct upload) |
| Content | Markdown + MDX |

---

## Features

- Terminal-style hero with animated prompt and blinking cursor
- Global backdrop: grid, cursor glow, noise texture (configurable)
- Glassmorphism on navbar, cards, and modals
- Full-text search via `⌘K` / `Ctrl+K` (Pagefind)
- Image galleries with native lightbox and `<GalleryEmbed>` component
- FAQPage JSON-LD structured data (schema.org)
- Strict HTTP security headers (CSP, HSTS, X-Frame-Options…)
- Light / dark mode, RSS feed, sitemap, dynamic OG images

---

## Commands

```bash
pnpm install     # Install dependencies
pnpm dev         # Dev server → http://localhost:4321
pnpm build       # Type-check + build + generate Pagefind index
pnpm preview     # Preview production build
pnpm lint        # ESLint
pnpm format      # Prettier (write)
```

> Pagefind search only works after a full build — run `pnpm build && pnpm preview` to test locally.

---

## Configuration

All site-level settings live in `src/config.ts` (title, author, feature toggles, limits).  
Social links and share links are in `src/constants.ts`.

### Feature toggles in `src/config.ts`

| Key | Description |
| :--- | :--- |
| `backdropEffects.cursorGlow` / `grain` | Background visual effects |
| `showGalleries` | Enable/disable gallery section |
| `introAudio` | Audio player in hero |
| `heroTerminalPrompt` | Animated prompt text |
| `showArchives` | Enable archives page |

---

## Content

### Blog posts

Create `.md` or `.mdx` files in `src/data/blog/` with this frontmatter:

```yaml
---
title: "Post title"
description: "Meta description, 120-155 chars"
pubDatetime: 2026-01-15T10:00:00+02:00
tags:
  - homelab
  - docker
featured: false
draft: false
faqs:               # optional — generates FAQPage JSON-LD
  - question: "..."
    answer: "..."
---
```

### Image galleries

Create a folder in `src/data/galleries/<slug>/` with an `index.md` (metadata) and image files. Use numeric prefixes (`01-`, `02-`) to control order.

---

## Deployment

Content is kept out of this repo and deployed via Cloudflare Pages direct upload:

```bash
pnpm build
wrangler pages deploy dist --project-name brandonvisca-com
```

---

## Security

HTTP security headers are defined in `public/_headers` (processed by Cloudflare Pages at the CDN edge). A `security.txt` is available at `/.well-known/security.txt`.

---

## Credits

- [AstroPaper](https://github.com/satnaing/astro-paper) by [Sat Naing](https://satnaing.dev) — MIT
- [astro-devosfera](https://github.com/0xdres/astro-devosfera) by [0xdres](https://github.com/0xdres) — upstream fork
