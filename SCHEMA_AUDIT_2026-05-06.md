# Audit Schema.org / JSON-LD — brandonvisca.com

> Date : 2026-05-06
> Schémas audités : Article, BreadcrumbList, FAQPage, WebSite, SearchAction, Person
> Fichiers analysés : `src/layouts/PostDetails.astro`, `src/layouts/Layout.astro`, `src/components/Breadcrumb.astro`, `src/pages/search.astro`, `src/config.ts`

---

## Résumé exécutif

| Schéma | État | Gaps critiques | Score /10 |
|---|---|---|---|
| **Article** | Présent mais incomplet | Publisher = Person (devrait être Organization), `inLanguage` manquant, `mainEntityOfPage` manquant, `image` en string pas ImageObject | 5/10 |
| **BreadcrumbList** | Présent mais incorrect | Hiérarchie hardcodée `Accueil > Blog > Article` ne correspond pas aux URLs réelles (`/{slug}/`) | 4/10 |
| **FAQPage** | Présent et valide | 42/79 articles actifs — bon taux de couverture | 7/10 |
| **WebSite** | Partiel | Absent sur les pages d'articles (uniquement sur non-articles) | 5/10 |
| **SearchAction** | Présent et fonctionnel | URL template correct (`/search/?q=`) | 9/10 |
| **Person (author)** | Minimal | `sameAs`, `jobTitle`, `image`, `knowsAbout` absents | 4/10 |

**Score global Schema.org : 5.5/10**

**Priorité P0** : Corriger `publisher` en `Organization` avec `logo`, ajouter `inLanguage`, et corriger le `BreadcrumbList`. Ces 3 corrections débloquent l'éligibilité aux rich results Google.

---

## 1. Article Schema (`src/layouts/PostDetails.astro`, lignes 85–108)

### 1.1 Implémentation actuelle

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Titre de l'article",
  "description": "Description",
  "datePublished": "2025-10-13T17:08:33+02:00",
  "dateModified": "2026-04-19T00:00:00+01:00",
  "author": {
    "@type": "Person",
    "name": "Brandon Visca",
    "url": "https://brandonvisca.com/about/"
  },
  "publisher": {
    "@type": "Person",
    "name": "Brandon Visca",
    "url": "https://brandonvisca.com/about/"
  },
  "url": "https://brandonvisca.com/article-slug/",
  "image": "https://brandonvisca.com/article-slug/index.png"
}
```

### 1.2 Gaps identifiés (détail)

| # | Champ / Problème | Sévérité | Raison |
|---|---|---|---|
| 1 | **`publisher` est `Person`** | **Critique** | Google Article rich results exigent un `publisher` de type `Organization` avec un `logo`. Un `Person` comme publisher disqualifie le site. |
| 2 | **`publisher.logo` manquant** | **Critique** | Champ requis par Google pour les rich results Article (minimum 696px de large, 1200px recommandé). |
| 3 | **`inLanguage` manquant** | **Critique** | Le contenu est en français mais Schema.org ne le déclare pas. Impacte le ciblage linguistique des rich results. |
| 4 | **`mainEntityOfPage` manquant** | Haute | Best practice Google — lie explicitement l'Article à sa page WebPage. |
| 5 | **`image` est une string, pas ImageObject`** | Moyenne | Google recommande un `ImageObject` avec `url`, `width`, `height` (min 696px de large). Une string simple est valide mais moins optimale. |
| 6 | **`articleSection` manquant** | Moyenne | Le premier tag de l'article (`tags[0]`) devrait être utilisé ici pour aider Google à catégoriser le contenu. |
| 7 | **`wordCount` manquant** | Faible | Signal secondaire mais recommandé par Schema.org. |
| 8 | **`dateModified` conditionnel** | Faible | Bien que valide, il est préférable de toujours l'émettre (égal à `datePublished` si pas de modif) pour éviter un signal stale. |
| 9 | **`author` Person trop minimal** | Haute | Manque `sameAs` (GitHub, LinkedIn), `jobTitle`, `image` (photo), `knowsAbout`. Affaiblit le signal E-E-A-T. |

### 1.3 Code recommandé (Article)

```astro
<script
  slot="head"
  type="application/ld+json"
  is:inline
  set:html={JSON.stringify({
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": title,
    "description": description,
    "datePublished": pubDatetime,
    "dateModified": modDatetime || pubDatetime,
    "inLanguage": "fr",
    "articleSection": tags?.[0] || "Blog",
    "mainEntityOfPage": {
      "@type": "WebPage",
      "@id": canonicalURL || Astro.url.href,
    },
    "author": {
      "@type": "Person",
      "name": author || "Brandon Visca",
      "url": `${Astro.url.origin}/about/`,
      "jobTitle": "Administrateur Systèmes & Réseaux",
      "image": `${Astro.url.origin}/avatar.webp`,
      "sameAs": [
        "https://github.com/visbran",
        "https://www.linkedin.com/in/brandonvisca", // si créé
      ],
      "knowsAbout": [
        "Proxmox VE",
        "Auto-hébergement",
        "Linux",
        "Docker",
        "Sécurité informatique",
        "DevOps",
      ],
    },
    "publisher": {
      "@type": "Organization",
      "name": "Brandon Visca",
      "url": `${Astro.url.origin}/`,
      "logo": {
        "@type": "ImageObject",
        "url": `${Astro.url.origin}/og.webp`,
        "width": 1200,
        "height": 630,
      },
    },
    "url": canonicalURL || Astro.url.href,
    "image": ogImage
      ? {
          "@type": "ImageObject",
          "url": ogImage,
          "width": 1200,
          "height": 630,
        }
      : undefined,
  })}
/>
```

---

## 2. BreadcrumbList Schema (`src/layouts/PostDetails.astro`, lignes 110–137)

### 2.1 Implémentation actuelle

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "position": 1, "name": "Accueil", "item": "https://brandonvisca.com/" },
    { "position": 2, "name": "Blog",    "item": "https://brandonvisca.com/blog/" },
    { "position": 3, "name": "Titre",   "item": "https://brandonvisca.com/article-slug/" }
  ]
}
```

### 2.2 Problème critique : mismatch URL

Les articles du blog ne sont **PAS** sous `/blog/{slug}/`. Ils sont à la racine : `/{slug}/`.

Le JSON-LD affirme que l'article est un enfant de `/blog/`, ce qui est **faux structurellement**. Cela peut être interprété par Google comme du structured data trompeur (misleading structured data).

### 2.3 Mismatch avec le breadcrumb visuel

Le breadcrumb visuel (`src/components/Breadcrumb.astro`) est généré dynamiquement depuis `Astro.url.pathname`. Pour un article à la racine, il affiche :
- `~` (Accueil)
- `{slug}` (current)

Le JSON-LD, lui, affiche toujours `Accueil > Blog > Article`.

### 2.4 Recommandation

**Option A (simple)** : Corriger le BreadcrumbList pour refléter la vraie structure plate :

```json
{
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "position": 1, "name": "Accueil", "item": "https://brandonvisca.com/" },
    { "position": 2, "name": title,     "item": "https://brandonvisca.com/article-slug/" }
  ]
}
```

**Option B (si articles sous /blog/ un jour)** : Conserver la structure actuelle mais modifier les routes Astro pour que les articles soient effectivement sous `/blog/{slug}/` (non recommandé — perte d'URLs existantes).

---

## 3. FAQPage Schema (`src/layouts/PostDetails.astro`, lignes 139–157)

### 3.1 Implémentation actuelle

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Question ?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Réponse texte..."
      }
    }
  ]
}
```

### 3.2 État

| Aspect | Valeur |
|---|---|
| Articles avec FAQ schema | **42 / 79** (53%) |
| Validité syntaxique | **Correcte** |
| Validité sémantique | **Correcte** (Question + Answer bien formés) |
| Markdown dans `text` | **Présent** dans certaines réponses (ex: `[lien](url)`). Google's parser accepte le texte brut mais les liens Markdown seront affichés littéralement. |

### 3.3 Recommandations

1. **Continuer l'expansion** — cibler les articles tutoriels à fort trafic (iTerm2, Oh-My-Zsh, Jellyfin) pour atteindre 70% de couverture.
2. **Nettoyer le Markdown** dans les réponses FAQ si possible (stripper les syntaxes `[]()` ou les convertir en HTML).
3. **Ajouter `@id`** aux Questions pour lier aux ancres de page : `@id: "${canonicalURL}#faq-1"`.

---

## 4. WebSite + SearchAction Schema (`src/layouts/Layout.astro`, lignes 37–58)

### 4.1 Implémentation actuelle

Le `WebSite` schema est **conditionnellement absent** sur les pages d'articles :

```astro
const structuredData = !pubDatetime ? { /* WebSite schema */ } : null;
```

Quand `pubDatetime` est présent (tous les articles), `structuredData` vaut `null`.

### 4.2 Gaps

| # | Problème | Sévérité |
|---|---|---|
| 1 | **WebSite absent sur les articles** | Haute |
| 2 | **`inLanguage` manquant** | Moyenne |
| 3 | **`author` sur WebSite** — propriété non standard pour ce type | Faible (inoffensif) |

### 4.3 Impact

L'absence de `WebSite` schema sur les articles empêche Google d'associer systématiquement toutes les pages à la même entité de site. Cela réduit l'éligibilité à la **Sitelinks Search Box**.

### 4.4 Code recommandé

Déplacer le WebSite schema **hors de la condition** `!pubDatetime` :

```astro
// WebSite schema — toujours émis, indépendamment du type de page
const webSiteSchema = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": SITE.title,
  "url": SITE.website,
  "description": SITE.desc,
  "inLanguage": "fr",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": `${SITE.website}search/?q={search_term_string}`,
    },
    "query-input": "required name=search_term_string",
  },
};
```

Puis l'émettre dans le `<head>` de **toutes** les pages :

```astro
<script type="application/ld+json" is:inline set:html={JSON.stringify(webSiteSchema)} />
```

### 4.5 SearchAction

| Aspect | État |
|---|---|
| URL template | `https://brandonvisca.com/search/?q={search_term_string}` |
| Page de recherche | `src/pages/search.astro` — lit `?q=` et charge Pagefind |
| Fonctionnel | **Oui** |

---

## 5. Schémas manquants recommandés

### 5.1 Organization Schema (Critique)

**Statut** : Absent.

**Où ajouter** :
- Dans `Article` comme `publisher` (voir section 1.3)
- En tant que bloc JSON-LD standalone sur toutes les pages (homepage, about)

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://brandonvisca.com/#organization",
  "name": "Brandon Visca",
  "url": "https://brandonvisca.com/",
  "logo": {
    "@type": "ImageObject",
    "url": "https://brandonvisca.com/og.webp",
    "width": 1200,
    "height": 630
  },
  "sameAs": [
    "https://github.com/visbran",
    "https://www.linkedin.com/in/brandonvisca"
  ]
}
```

### 5.2 Enhanced Person Schema sur /about/ et /cv/ (Haute)

**Statut** : `AboutLayout.astro` n'émet **aucun** JSON-LD.

**Recommandation** : Ajouter un bloc `Person` riche sur la page `/about/` :

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Brandon Visca",
  "url": "https://brandonvisca.com/about/",
  "image": "https://brandonvisca.com/avatar.webp",
  "jobTitle": "Administrateur Systèmes & Réseaux",
  "worksFor": { "@id": "https://brandonvisca.com/#organization" },
  "sameAs": [
    "https://github.com/visbran",
    "https://www.linkedin.com/in/brandonvisca"
  ],
  "knowsAbout": [
    "Proxmox VE",
    "Auto-hébergement",
    "Linux",
    "Docker",
    "Sécurité informatique",
    "DevOps"
  ]
}
```

### 5.3 ProfilePage Schema sur /about/ (Moyenne)

Google supporte le type `ProfilePage` pour les pages personnelles :

```json
{
  "@context": "https://schema.org",
  "@type": "ProfilePage",
  "mainEntity": {
    "@type": "Person",
    "name": "Brandon Visca",
    ...
  }
}
```

### 5.4 HowTo Schema pour les tutoriels (Moyenne)

Articles éligibles : iTerm2, Oh-My-Zsh, Docker débutant, Proxmox LXC, Nginx sécurité, etc.

**Nécessite** : ajouter `howToSteps` au frontmatter ou parser la structure des headings.

### 5.5 SoftwareApplication + Review Schema (Moyenne)

Articles éligibles : Raycast, Arc Browser, Jellyfin, Vaultwarden, Snipe-IT, etc.

**Nécessite** : ajouter `softwareReviewed` au frontmatter.

---

## 6. Content Schema — extensions recommandées (`src/content.config.ts`)

Pour supporter les nouveaux schémas, le frontmatter pourrait être étendu :

```typescript
howToSteps: z.array(z.object({
  name: z.string(),
  text: z.string(),
  image: image().optional(),
})).optional(),

softwareReviewed: z.object({
  name: z.string(),
  category: z.string(),
  price: z.number().default(0),
  rating: z.number().min(1).max(5).optional(),
  os: z.string().optional(),
}).optional(),
```

---

## 7. Matrice de priorité

| Priorité | Action | Fichier(s) | Impact | Difficulté |
|---|---|---|---|---|
| **P0 — Critique** | Changer `publisher` en `Organization` + ajouter `logo` | `PostDetails.astro` | Rich results Article | Facile |
| **P0 — Critique** | Ajouter `inLanguage: "fr"` à Article | `PostDetails.astro` | Ciblage langue | Facile |
| **P0 — Critique** | Corriger BreadcrumbList pour matcher les URLs réelles | `PostDetails.astro` | Pas de pénalité SD | Facile |
| **P1 — Haute** | Émettre WebSite schema sur **toutes** les pages | `Layout.astro` | Sitelinks Search Box | Facile |
| **P1 — Haute** | Ajouter `mainEntityOfPage` à Article | `PostDetails.astro` | Best practice | Facile |
| **P1 — Haute** | Ajouter Person schema sur `/about/` | `AboutLayout.astro` ou page | E-E-A-T | Moyen |
| **P2 — Moyenne** | Enrichir `author` Person avec `sameAs`, `jobTitle`, `image` | `PostDetails.astro` | E-E-A-T | Moyen |
| **P2 — Moyenne** | Convertir `image` en `ImageObject` avec width/height | `PostDetails.astro` | Rich result image | Moyen |
| **P2 — Moyenne** | Ajouter Organization standalone | `Layout.astro` | Entity linking | Facile |
| **P3 — Faible** | Ajouter `articleSection` (tag primaire) | `PostDetails.astro` | Categorization | Facile |
| **P3 — Faible** | Ajouter `wordCount` | `PostDetails.astro` | Signal mineur | Moyen |
| **P3 — Faible** | Ajouter `ProfilePage` sur `/about/` | `AboutLayout.astro` | Personnal | Facile |
| **P3 — Faible** | Implémenter `HowTo` schema | Content + layout | How-to snippets | Complexe |
| **P3 — Faible** | Implémenter `SoftwareApplication` schema | Content + layout | App snippets | Complexe |

---

## 8. Vérification et tests recommandés

1. **Google Rich Results Test** : https://search.google.com/test/rich-results
   - Tester 3–5 URLs d'articles représentatifs
   - Vérifier l'éligibilité Article, FAQ, Breadcrumb

2. **Schema.org Validator** : https://validator.schema.org/
   - Tester la validité syntaxique de tous les blocs JSON-LD

3. **GSC > Enhancements** :
   - Surveiller le nombre d'articles avec FAQ rich result actif
   - Surveiller les erreurs de structured data

4. **MCP GSC `query_by_search_appearance`** :
   - Vérifier si des articles apparaissent en "FAQ" ou "Article" rich results

---

## 9. Références rapides

**Fichiers audités :**
- `src/layouts/PostDetails.astro` — Article, BreadcrumbList, FAQPage
- `src/layouts/Layout.astro` — WebSite + SearchAction
- `src/layouts/AboutLayout.astro` — Aucun JSON-LD
- `src/components/Breadcrumb.astro` — Breadcrumb visuel
- `src/config.ts` — Configuration site
- `src/content.config.ts` — Schema frontmatter
- `src/pages/search.astro` — Validation SearchAction URL

**Articles avec FAQ schema actif :** 42 / 79 (53%)
**SearchAction :** Fonctionnel
**og:locale :** `fr_FR` (correct)
**SITE.lang :** `"fr"` (à utiliser pour `inLanguage`)
