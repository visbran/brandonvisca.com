# Known Issues & SEO Scores

> Fichier volatile — mis à jour après chaque audit SEO. Ne pas inclure dans CLAUDE.md.
> Dernier audit : 2026-05-06 — Voir `AUDIT_GLOBAL_2026-05-06.md`
> Dernières corrections : 2026-05-17 (audit complet — strings espagnoles constants.ts, schemas JSON-LD CollectionPage + Person)

---

## Issues actives — état réel 2026-05-17

> Réévaluation complète : 82 articles (79 + 3 nouveaux : tianji, immich-docker, adguard-home)

| Issue | Articles / Scope | Priorité | Fix | Rapport détaillé |
|---|---|---|---|---|
| `ogImage_specific` | 0/82 avec ogImage | Medium | Images OG personnalisées par article (fallback `og.webp` actif) | `AUDIT_SEO_2026-05-06.md` |
| `faqs_missing` | **0/82** — tous les articles ont `faqs:` | ~~Medium~~ | ✅ Résolu | — |
| `internal_links_missing` | **0/82** — tous les articles ont "Articles connexes" | ~~Medium~~ | ✅ Résolu 2026-05-17 | — |
| `tags_excess` | 21 tags contenu + 4 meta-tags (cible ~30) | Low | Situation saine, monitoring | `TAGS_STRATEGY_2026-05-06.md` |
| `tags_thin_content` | ~35 pages tag à 1 article | Medium | `noindex` ou fusion | `TAGS_STRATEGY_2026-05-06.md` |
| `affiliate_disclosure_missing` | 2 articles : `s3cmd`, `vaultwarden` | Medium | Ajouter disclosure "lien affilié" | `EEAT_AUDIT_2026-05-06.md` |
| `ga4_not_connected` | Site-wide | Medium | Setup MCP GA4 Data API | `AUDIT_SEO_2026-05-06.md` |

---

## Issues résolues (2026-05-06 + 2026-05-17)

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
| `focusKeyword_missing` | 32 articles | **Résolu** — `focusKeyword` ajouté sur 32 articles manquants | 2026-05-06 |
| `alt_text_missing` | 8 articles / 56 images | **Résolu** — Texte alternatif ajouté sur 58 images | 2026-05-06 |
| `external_links_missing` | 12 articles | **Résolu** — Liens vers sources autoritatives ajoutés | 2026-05-06 |
| `omarchy_traffic_drop` | 1 article | **Résolu** — Réécriture complète v3.8.0 (2 commits) | 2026-05-17 |
| `internal_links_missing` | 51/82 articles | **Résolu** — Section "Articles connexes" ajoutée (script Jaccard) | 2026-05-17 |

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
2. [x] **CV** : remplir `src/pages/cv.md` avec l'expérience réelle
3. [x] **Tags** : fusionner `office365`→`microsoft-365`, `tutoriel`→`guide`, `self-hosting`→`auto-hebergement`
4. [x] **Frontmatter** : compléter `focusKeyword` sur 32 articles
5. [x] **Images** : corriger 58 alt text sur 8 articles
6. [ ] **Liens externes** : tous les articles ont maintenant ≥ 1 lien externe
7. [x] **FAQ** : ajouter FAQ à 3 articles populaires (jellyfin, magnet, snipeit)

---

## Backlog GEO (à implémenter)

- [x] Person schema sur `/about/` — ajouté 2026-05-17
- [x] CollectionPage schema sur `/blog/` — ajouté 2026-05-17
- Organization standalone JSON-LD sur homepage
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
| Articles avec FAQ schema | 45/79 (57%) | 55/79 (70%) |
| Articles avec ogImage (spécifique) | 0/79 (0%) | 15/79 (19%) |
| Articles avec focusKeyword | 79/79 (100%) | 79/79 (100%) |
| Tags uniques | ~116 | ~50 |
| Liens externes / article (moyenne) | 1.0 | 1.2 |
