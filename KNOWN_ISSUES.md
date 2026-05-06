# Known Issues & SEO Scores

> Fichier volatile — mis à jour après chaque audit SEO. Ne pas inclure dans CLAUDE.md.
> Dernier audit : 2026-05-06 — Voir `AUDIT_GLOBAL_2026-05-06.md`
> Dernières corrections : 2026-05-06 (Schema.org P0 + CV)

---

## Issues actives (post-corrections 2026-05-06)

| Issue | Articles / Scope | Priorité | Fix | Rapport détaillé |
|---|---|---|---|---|
| `ogImage_missing` | 79/79 articles | **High** | Ajouter `ogImage` frontmatter | `AUDIT_SEO_2026-05-06.md` |
| `alt_text_missing` | 8 articles / 56 images | **High** | Ajouter texte alternatif | `AUDIT_SEO_2026-05-06.md` |
| `focusKeyword_missing` | 33 articles | Medium | Compléter le frontmatter | `AUDIT_SEO_2026-05-06.md` |
| `faqs_missing` | 37 articles | Medium | Ajouter bloc FAQ | `AUDIT_SEO_2026-05-06.md` |
| `internal_links_missing` | 34 articles | Medium | Ajouter section "Articles connexes" | `AUDIT_SEO_2026-05-06.md` |
| `external_links_missing` | 22 articles | Medium | Ajouter lien vers source autoritative | `AUDIT_SEO_2026-05-06.md` |
| `tags_excess` | ~120 tags uniques | Medium | Consolidation → ~30 tags | `TAGS_STRATEGY_2026-05-06.md` |
| `tags_thin_content` | ~35 pages tag à 1 article | Medium | `noindex` ou fusion | `TAGS_STRATEGY_2026-05-06.md` |
| `affiliate_disclosure_missing` | Articles Amazon | Medium | Ajouter disclosure "lien affilié" | `EEAT_AUDIT_2026-05-06.md` |
| `ga4_not_connected` | Site-wide | Medium | Setup MCP GA4 Data API | `AUDIT_SEO_2026-05-06.md` |
| `omarchy_traffic_drop` | 1 article | High | Mise à jour contenu ou redirect | — |

---

## Issues résolues (2026-05-06)

| Issue | Ancien état | Résolution | Date |
|---|---|---|---|
| `h1_in_body` | 38 articles | **Résolu** — 0 article avec H1 dans le body | 2026-05-06 |
| `heading_structure` | 55 articles | **Résolu** — 0 article avec saut de niveau | 2026-05-06 |
| `schema_publisher_person` | Site-wide | **Résolu** — `publisher` changé en `Organization` avec `logo` | 2026-05-06 |
| `schema_breadcrumb_mismatch` | Site-wide | **Résolu** — `BreadcrumbList` reflète URLs réelles | 2026-05-06 |
| `schema_inLanguage_missing` | Site-wide | **Résolu** — `inLanguage: "fr"` ajouté à Article et WebSite | 2026-05-06 |
| `schema_website_missing_on_posts` | Site-wide | **Résolu** — `WebSite` schema émis sur toutes les pages | 2026-05-06 |
| `schema_author_minimal` | Site-wide | **Résolu** — `author` enrichi avec `jobTitle`, `sameAs`, `knowsAbout` | 2026-05-06 |
| `schema_mainEntityOfPage_missing` | Site-wide | **Résolu** — `mainEntityOfPage` ajouté | 2026-05-06 |
| `schema_image_string` | Site-wide | **Résolu** — `image` converti en `ImageObject` | 2026-05-06 |
| `tags_accents` | ~4 articles | **Résolu** — Tous les tags accents corrigés | 2026-04-09 → 2026-05-06 |
| `cv_empty` | 1 page | **Résolu** — `src/pages/cv.md` rempli avec l'expérience réelle | 2026-05-06 |
| `tags_english` | ~3 articles | **Résolu** — Tous les tags anglais remplacés | 2026-04-09 → 2026-05-06 |
| `ogwebp_missing` | 1 fichier | **Résolu** — `public/og.webp` créé depuis `devosfera-og.webp` | 2026-05-06 |

---

## Scores SEO de référence

| Axe | Max actuel | Max futur (GA4) | Valeur 2026-04-09 | Valeur 2026-05-06 | Δ |
|---|---|---|---|---|---|
| Performance GSC | 65 | 100 | 39/65 | 39/65 | — |
| On-page SEO | 15 | 15 | 9.2/15 | 8.5/15 | −0.7 |
| GEO Citabilité IA | 15 | 15 | 7.9/15 | 9.5/15 | **+1.6** |
| **Score global** | **45** | **65** | **22.1/45** | **24.5/45** | **+2.4** |

GA4 débloque +20 pts (Engagement /20 + Durée /15, théorique max 65). Propriété GA4 existante — setup MCP GA4 Data API à faire.

---

## Quick wins — cette semaine

1. [x] **Schema.org** : corriger `publisher` en `Organization` + `logo`, ajouter `inLanguage`, fix `BreadcrumbList`
2. [ ] **CV** : remplir `src/pages/cv.md` avec l'expérience réelle
3. [x] **Tags** : fusionner `office365`→`microsoft-365`, `tutoriel`→`guide`, `self-hosting`→`auto-hebergement`
4. [ ] **Frontmatter** : compléter `focusKeyword` sur 33 articles
5. [ ] **Images** : ajouter `ogImage` aux top 10 articles + corriger 56 alt text

---

## Backlog GEO (à implémenter)

- Organization standalone JSON-LD sur homepage
- Enhanced Person schema sur `/about/` et `/cv/`
- ProfilePage schema sur `/about/`
- HowTo schema pour les articles tutoriels
- SoftwareApplication + Review schema pour les reviews d'apps
- Liens externes vers sources autoritatives (≥ 1 par article)
- Connexion GA4 MCP Data API

---

## KPIs cibles — prochain audit (2026-06-06)

| KPI | Baseline (mai) | Cible (juin) |
|---|---|---|
| Clics totaux / mois | ~1 800 | 2 500 |
| CTR moyen | 1.6% | 2.0% |
| Articles avec FAQ schema | 42/79 (53%) | 55/79 (70%) |
| Articles avec ogImage | 0/79 (0%) | 15/79 (19%) |
| Articles avec focusKeyword | 46/79 (58%) | 65/79 (82%) |
| Tags uniques | ~120 | ~50 |
| Liens externes / article (moyenne) | 0.8 | 1.2 |
