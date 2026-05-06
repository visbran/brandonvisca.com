# Audit Global — brandonvisca.com

> Date : 2026-05-06
> Auditeur : Claude Code (Pipeline SEO)
> Rapports détaillés : `AUDIT_SEO_2026-05-06.md`, `TAGS_STRATEGY_2026-05-06.md`, `EEAT_AUDIT_2026-05-06.md`, `SCHEMA_AUDIT_2026-05-06.md`

---

## Résumé stratégique

Cet audit couvre 5 axes : SEO technique, Tags, E-E-A-T, Schema.org, et Outils d'automatisation. Il s'appuie sur les données Google Search Console (90 jours), un crawl complet du codebase, et une analyse manuelle des 79 articles.

**Score global SEO** : **24.5/45** (Performance 6.5 + On-page 8.5 + GEO 9.5)

**Potentiel de croissance** : +15 à +20 points avec les quick wins identifiés.

---

## 1. SEO Technique — Synthèse

### Ce qui marche bien

- **Base technique solide** : Astro statique, sitemap auto-généré, robots.txt permissif pour les IA, RSS, canonical tags, OG/Twitter Cards, llms.txt complet.
- **Architecture URL** : Slugs plats `/{slug}/` préservent l'équité SEO post-WordPress. Redirects 301 bien configurés.
- **JSON-LD** : Article, BreadcrumbList, FAQPage, WebSite+SearchAction déjà implémentés.
- **Pagefind search** : Index de recherche statique performant.
- **Dynamic OG images** : Génération automatique via Satori.

### Ce qui bloque la croissance

- **CTR faible** : 45 requêtes avec >100 impressions et CTR <3%. Potentiel de +1 200 clics/mois.
- **Aucun `ogImage` dédié** : 0 article sur 79 a un `ogImage` personnalisé.
- **33 articles sans `focusKeyword`** : Champ présent dans le schema mais pas renseigné.
- **37 articles sans FAQ** : Perte de rich snippets.
- **56 images sans alt text** : SEO image + accessibilité.
- **34 articles sans maillage interne** : Perte de PV/session.
- **22 articles sans liens externes** : Signal E-E-A-T affaibli.

### Quick wins SEO (priorité cette semaine)

| # | Action | Effort | Impact |
|---|---|---|---|
| 1 | Ajouter `ogImage` aux top 10 articles | Faible | +CTR social |
| 2 | Compléter `focusKeyword` sur 33 articles | Faible | Meilleur ciblage |
| 3 | Ajouter FAQ aux 10 articles les plus visités | Moyen | Rich snippets |
| 4 | Corriger les 56 images sans alt | Moyen | Image SEO + a11y |

---

## 2. Tags — Synthèse

### Problème

**~120 tags uniques** pour 79 articles. Densité excessive créant du thin content (~35 pages de tag à 1 article).

### Stratégie cible

**12 tags primaires** (navigation) + **~18 tags secondaires** (SEO longue traîne). Réduction de **75%** du nombre de tags.

### Actions clés

| Action | Détail |
|---|---|
| Fusionner doublons | `office365`→`microsoft-365`, `tutoriel`→`guide`, `self-hosting`→`auto-hebergement` |
| Supprimer tags uniques | ~35 tags à 1 occurrence (noms de produits uniques) |
| Filtrer méta-tags | Masquer `guide`, `debutant`, `intermediaire`, `avance` de la grille publique |
| Noindex thin tags | Mettre `noindex` sur les pages de tag à 1 article |
| Optimiser meta tags des pages de tags | Title + description dynamiques par tag |

---

## 3. E-E-A-T — Synthèse

### Score par signal

| Signal | Score | Diagnostic |
|---|---|---|
| **Experience** | 7.5/10 | Fort — setup réel, première personne, preuves |
| **Expertise** | 6.0/10 | Moyen — CV vide, pas de photo, pas de LinkedIn |
| **Authoritativeness** | 5.5/10 | Moyen — manque de liens vers sources institutionnelles |
| **Trustworthiness** | 7.0/10 | Fort — transparence, contact, sécurité technique |

### Actions prioritaires

1. **Remplir le CV** (`src/pages/cv.md`) — impact immédiat sur le signal Expertise
2. **Ajouter une photo réelle** de l'auteur
3. **Créer un profil LinkedIn** et l'ajouter aux socials
4. **Ajouter ≥1 lien autoritatif** (docs officielles, RFC, etc.) aux 22 articles sans lien externe
5. **Ajouter une disclosure** pour les liens affiliés Amazon

---

## 4. Schema.org — Synthèse

### Gaps critiques (P0)

1. **`publisher` est `Person`** → doit être `Organization` avec `logo`
2. **`inLanguage: "fr"` manquant** sur Article et WebSite
3. **BreadcrumbList incorrect** — hardcodé `Accueil > Blog > Article` ne correspond pas aux URLs (`/{slug}/`)
4. **WebSite schema absent** sur les pages d'articles

### Gaps haute priorité (P1)

5. `mainEntityOfPage` manquant
6. `author` Person trop minimal (pas de `sameAs`, `jobTitle`, `image`)
7. `image` en string au lieu de `ImageObject` avec width/height
8. Aucun JSON-LD sur `/about/` et `/cv/`

### Schémas recommandés (P2-P3)

- Organization standalone
- Enhanced Person sur `/about/`
- ProfilePage sur `/about/`
- HowTo pour les tutoriels
- SoftwareApplication + Review pour les reviews d'apps

---

## 5. Outils de productivité (CI/CD) — Livrables

### Workflows GitHub Actions créés

| Workflow | Fichier | Déclencheur | Action |
|---|---|---|---|
| **PR Audit** | `.github/workflows/pr-audit.yml` | PR sur `main` | Lint, build, check liens, audit frontmatter |
| **Tag Validation** | `.github/workflows/tag-check.yml` | Push/PR modifiant `src/data/blog/` | Vérifie kebab-case, accents, max 6 tags, tag primaire |
| **Regen llms.txt** | `.github/workflows/llms-txt.yml` | Push modifiant articles | Régénère `public/llms.txt` depuis les frontmatter |
| **Deploy + Smoke** | `.github/workflows/deploy.yml` (modifié) | Push sur `main` | Déploiement + tests HTTP homepage, sitemap, robots.txt, llms.txt |

### Scripts créés

| Script | Fichier | Usage |
|---|---|---|
| **PR Audit** | `scripts/pr-audit.mjs` | Vérifie H1, alt text, frontmatter incomplet, tags |
| **Tag Check** | `scripts/tag-check.mjs` | Validation globale des tags sur tous les articles |
| **Generate llms.txt** | `scripts/generate-llms-txt.mjs` | Génère `llms.txt` structuré |
| **Pre-publish Check** | `scripts/pre-publish-check.py` | Vérification article par article avant publication |

---

## 6. Matrice priorité Effort / Impact

```
          Impact élevé              Impact moyen
         ┌────────────────────┬────────────────────┐
Effort   │ 1. Remplir le CV   │ 5. Enrichir schema │
faible   │ 2. Corriger publisher│   Person          │
         │    Organization    │ 6. Ajouter FAQ    │
         │ 3. Ajouter inLanguage│    top 10 articles│
         │ 4. Fix BreadcrumbList│                   │
         ├────────────────────┼────────────────────┤
Effort   │ 7. Ajouter ogImage │ 9. Ajouter HowTo  │
moyen    │    top 10 articles │    schema         │
         │ 8. Maillage interne│ 10. Link building │
         │    34 articles     │    stratégique    │
         ├────────────────────┼────────────────────┤
Effort   │ 11. Connecter GA4  │ 13. Profil LinkedIn│
élevé    │ 12. Consolidation  │ 14. Guest posts   │
         │    tags (~120→30)  │                    │
         └────────────────────┴────────────────────┘
```

**Ordre recommandé d'exécution** : 2 → 3 → 4 → 1 → 8 → 7 → 6 → 5 → 13 → 12 → 11 → 9 → 10 → 14

---

## 7. Calendrier de mise en oeuvre

### Semaine 1 (6–12 mai 2026)
- [ ] Corriger schema.org (publisher Organization, inLanguage, BreadcrumbList)
- [ ] Remplir `src/pages/cv.md`
- [ ] Ajouter photo réelle de l'auteur
- [ ] Compléter `focusKeyword` sur 33 articles
- [ ] Ajouter `ogImage` aux top 10 articles

### Semaine 2 (13–19 mai)
- [ ] Ajouter sections "Articles connexes" aux 34 articles sans maillage
- [ ] Ajouter FAQ aux 10 articles les plus visités
- [ ] Corriger les 56 images sans alt text
- [ ] Ajouter disclosure affilié Amazon

### Semaine 3 (20–26 mai)
- [ ] Fusion des tags doublons (office365, tutoriel, self-hosting)
- [ ] Suppression des ~35 tags uniques
- [ ] Filtrer méta-tags de la grille `/tags/`
- [ ] Noindex sur les pages de tags à 1 article

### Semaine 4 (27 mai–2 juin)
- [ ] Connecter GA4 (MCP Data API)
- [ ] Ajouter liens externes autoritaires aux 22 articles
- [ ] Créer profil LinkedIn + l'ajouter aux socials
- [ ] Enrichir `author` Person (sameAs, jobTitle, image)

### Mois 2 (juin)
- [ ] Implémenter Organization standalone JSON-LD
- [ ] Ajouter Person schema sur `/about/`
- [ ] Tester HowTo schema sur 3 articles tutoriels
- [ ] Lancer stratégie link building (StackOverflow, Reddit)

### Mois 3 (juillet)
- [ ] Implémenter SoftwareApplication schema sur 3 reviews
- [ ] Guest posts sur blogs tech francophones
- [ ] Audit de suivi (comparer KPIs vs baseline du 6 mai)

---

## 8. KPIs de suivi

| KPI | Baseline (mai 2026) | Cible (juillet 2026) | Méthode |
|---|---|---|---|
| Clics totaux / mois (GSC) | ~1 800 | 3 500 | Requête GSC mensuelle |
| CTR moyen | 1.6% | 2.5% | Requête GSC mensuelle |
| Articles avec FAQ schema | 42/79 (53%) | 60/79 (76%) | Comptage frontmatter |
| Articles avec ogImage | 0/79 (0%) | 30/79 (38%) | Comptage frontmatter |
| Articles avec focusKeyword | 46/79 (58%) | 79/79 (100%) | Comptage frontmatter |
| Tags uniques | ~120 | ~30 | `scripts/tag-check.mjs` |
| Pages de tag thin content | ~35 | <5 | Audit manuel |
| Liens externes / article (moyenne) | 0.8 | 1.5 | `scripts/pr-audit.mjs` |
| Rich results actifs (FAQ) | Inconnu | 15+ articles | GSC Enhancements |
| Score E-E-A-T perçu | 6.5/10 | 8.0/10 | Audit qualitatif |
| Score Schema.org | 5.5/10 | 8.5/10 | Audit technique |

---

## 9. Risques et blocages identifiés

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Perte de trafic sur articles iTerm2 / Oh-My-Zsh (baisse mensuelle) | Élevée | Haute | Mettre à jour `modDatetime`, ajouter contenu frais, screenshots récents |
| Pénalité thin content sur pages de tags | Moyenne | Moyenne | Noindex + consolidation rapide |
| Conflit avec upstream theme (fork AstroPaper) | Moyenne | Faible | Documenter toutes les modifications dans `THEME_CUSTOMIZATIONS.md` |
| Temps de build Cloudflare Pages (timeout) | Faible | Moyenne | `build:cf` skip `astro check` — déjà en place |

---

## 10. Documents produits lors de cet audit

| Document | Contenu | Lien interne |
|---|---|---|
| **AUDIT_SEO_2026-05-06.md** | Données GSC, on-page, technique, plan d'action SEO | `[AUDIT_SEO_2026-05-06.md](AUDIT_SEO_2026-05-06.md)` |
| **TAGS_STRATEGY_2026-05-06.md** | Inventaire tags, plan de consolidation, stratégie 2 niveaux | `[TAGS_STRATEGY_2026-05-06.md](TAGS_STRATEGY_2026-05-06.md)` |
| **EEAT_AUDIT_2026-05-06.md** | Matrice E-E-A-T, scoring par signal, plan d'action | `[EEAT_AUDIT_2026-05-06.md](EEAT_AUDIT_2026-05-06.md)` |
| **SCHEMA_AUDIT_2026-05-06.md** | Gaps JSON-LD, code recommandé, matrice priorité | `[SCHEMA_AUDIT_2026-05-06.md](SCHEMA_AUDIT_2026-05-06.md)` |
| **AUDIT_GLOBAL_2026-05-06.md** | Ce document — synthèse stratégique et roadmap | `[AUDIT_GLOBAL_2026-05-06.md](AUDIT_GLOBAL_2026-05-06.md)` |

---

## 11. Mise à jour de KNOWN_ISSUES.md

Les issues suivantes de `KNOWN_ISSUES.md` (2026-04-09) sont **résolues** :

- `h1_in_body` : 38 articles → **0 article** (résolu)
- `heading_structure` : 55 articles → **0 article** (résolu)
- `schema_jsonld` : Marqué comme "manquant" alors qu'il est **présent** — la documentation était obsolète

Les issues suivantes restent **actives** :

- `GA4 non connecté` — toujours à faire
- `Omarchy article (-87% clics)` — nécessite une mise à jour de contenu

Nouvelles issues à ajouter :

- `ogImage_missing` : 79/79 articles sans `ogImage` dédié
- `alt_text_missing` : 56 images sans alt text
- `external_links_missing` : 22 articles sans lien externe
- `internal_links_missing` : 34 articles sans section Articles connexes
- `tags_excess` : ~120 tags uniques, consolidation nécessaire
- `schema_publisher_person` : publisher doit être Organization
- `schema_breadcrumb_mismatch` : BreadcrumbList ne correspond pas aux URLs
- `cv_empty` : CV page est un template vide
- `affiliate_disclosure_missing` : Pas de disclosure pour les liens Amazon

---

> **Prochain audit recommandé** : 2026-06-06 (dans 1 mois) pour mesurer l'impact des corrections appliquées.
