# Audit E-E-A-T — brandonvisca.com

> Date : 2026-05-06
> Audit des signaux Experience, Expertise, Authoritativeness, Trustworthiness
> Basé sur : Guidelines Google Quality Rater, Schema.org, et analyse du codebase

---

## Résumé exécutif

| Signal | Score /10 | État | Quick win ? |
|---|---|---|---|
| **Experience (E)** | 7.5/10 | Fort | Non |
| **Expertise (Ex)** | 6.0/10 | Moyen | Oui (CV + certifs) |
| **Authoritativeness (A)** | 5.5/10 | Moyen | Oui (backlinks + liens autorités) |
| **Trustworthiness (T)** | 7.0/10 | Fort | Non |
| **Score E-E-A-T global** | **6.5/10** | — | — |

**Verdict** : Le site a une base E-E-A-T solide grâce à la première personne, la transparence du setup, et la cohérence de l'identité. Les points faibles sont le **manque de credentialing formel** (CV vide, pas de LinkedIn), la **faiblesse des liens vers sources hautement autoritaires** (RFC, docs officielles vs sites de produits), et le **manque de preuves sociales** (témoignages, commentaires, partages).

---

## 1. Experience (E) — 7.5/10

### 1.1 Preuves d'expérience personnelle

| Critère | État | Preuve |
|---|---|---|
| Langage première personne | **Présent** | "J'ai configuré", "Mon homelab", "J'utilise depuis" |
| Détails de setup réel | **Présent** | Proxmox sur ThinkStation P720 + ThinkCentre M720q, Oracle Cloud VM, VLANs |
| Screenshots de configuration | **Partiel** | Présents sur les articles macOS et homelab, mais pas systématiques |
| Dates de mise en production | **Partiel** | Quelques articles mentionnent "depuis 2020" |
| Retours d'échecs | **Présent** | "Guides testés en prod, pas en théorie" — mention des échecs passés |

### 1.2 Articles avec preuves d'expérience fortes

- `auto-hebergement-guide-complet-2025.md` — détaille le setup Proxmox complet
- `docker-debutant-services-auto-heberger.md` — services réellement hébergés listés
- `proxmox-lxc-containers-guide.md` — configuration réelle de containers
- `independance-numerique-2025-guide-complet.md` — checklist personnelle

### 1.3 Articles avec preuves d'expérience faibles

- `ladybird-browser-le-navigateur-web-qui-refuse-de-se-soumettre-a-google-et-tant-mieux.md` — review sans usage prolongé apparent
- `exploration-de-super-so-un-outil-de-site-web-personnalise-pour-notion.md` — découverte, pas d'usage en production

### 1.4 Recommandations

1. **Ajouter un bloc "Mon setup"** en fin d'article pour les guides techniques : "Cette config tourne sur mon Proxmox depuis X mois."
2. **Systématiser les screenshots** de l'interface réelle (pas seulement les screenshots marketing).
3. **Mentionner la durée d'usage** pour les reviews d'apps : "J'utilise Raycast depuis 2023."

---

## 2. Expertise (Ex) — 6.0/10

### 2.1 Credentials et profil professionnel

| Élément | État | Impact |
|---|---|---|
| Page `/about/` | **Détaillée** | Présente l'identité, le setup, la philosophie |
| Page `/cv/` | **Template vide** | CV.md contient des placeholders — **affaiblit fortement le signal** |
| Photo réelle de l'auteur | **Absente** | Emoji avatar uniquement (`👨‍💻`) — pas de vraie photo |
| Bio technique détaillée | **Présente** | "Administrateur Systèmes & Réseaux" implicite via le contenu |
| Certifications mentionnées | **Absentes** | Aucune certification (LPIC, Cisco, AWS, etc.) mentionnée |
| LinkedIn / X / Bluesky | **Absents** | Seul GitHub et email sont listés |

### 2.2 Profil social

| Réseau | Lien | État |
|---|---|---|
| GitHub | `github.com/visbran` | **Actif** |
| Email | `contact@brandonvisca.com` | **Actif** |
| LinkedIn | — | **Manquant** |
| X/Twitter | — | **Manquant** |
| Bluesky | — | **Manquant** |
| Mastodon | — | **Manquant** |

### 2.3 Schema.org Person (enrichissement)

Le schema `Person` dans `PostDetails.astro` ne contient que `name` et `url`. Il manque :
- `jobTitle`
- `image` (photo réelle)
- `sameAs` (liens sociaux)
- `knowsAbout` (domaines d'expertise)
- `worksFor` (lien vers Organization)
- `alumniOf` (formations)

### 2.4 Recommandations

| Priorité | Action | Effort | Impact |
|---|---|---|---|
| **P0** | **Remplir `src/pages/cv.md`** avec l'expérience réelle | Moyen | Élevé |
| **P0** | **Ajouter une photo réelle** dans `public/` et l'utiliser dans `about.md` | Faible | Élevé |
| **P1** | **Créer un profil LinkedIn** et l'ajouter dans `src/constants.ts` | Moyen | Élevé |
| **P1** | **Enrichir le schema `Person`** avec `jobTitle`, `image`, `sameAs`, `knowsAbout` | Faible | Moyen |
| **P2** | **Mentionner les certifications/formations** dans le CV et l'about | Faible | Moyen |
| **P2** | **Ajouter X/Bluesky** si actifs | Faible | Faible |

---

## 3. Authoritativeness (A) — 5.5/10

### 3.1 Liens vers sources autoritatives

**Analyse des liens externes sur 79 articles :**

| Type de source | Exemples | Fréquence | Autorité |
|---|---|---|---|
| GitHub repos | `github.com/...` | Très fréquent | Moyenne-Haute |
| Documentation produit | `raycast.com`, `manual.raycast.com` | Fréquent | Moyenne |
| Man pages officielles | `kernel.org`, `freedesktop.org` | Occasionnel | Haute |
| Scripts officiels | `get.docker.com` | Occasionnel | Haute |
| Amazon affiliés | `amzn.to/...` | Rare | Faible (pas autoritaire) |
| Reddit communautaire | `reddit.com/r/...` | Rare | Faible |

**Problème** : Très peu d'articles citent des sources **institutionnelles** de très haute autorité :
- RFC (IETF)
- Documentation Microsoft Learn / Docs
- Documentation AWS/GCP/Azure officielle
- OWASP, NIST, CIS Benchmarks
- W3C, WHATWG

**22 articles n'ont aucun lien externe** (voir `AUDIT_SEO_2026-05-06.md`).

### 3.2 Backlinks entrants (via GSC)

GSC ne fournit pas directement les backlinks. Cependant, le trafic provenant de requêtes branded (`brandonvisca`, `visbran`) est faible, ce qui suggère un **link building limité**.

### 3.3 Citations et mentions

| Élément | État |
|---|---|
| Citations dans d'autres sites | Inconnu — pas de tracking |
| Guest posts | Aucun identifié |
| Podcasts / interviews | Aucun identifié |
| Communautés modérées / réponses | GitHub uniquement |

### 3.4 Recommandations

| Priorité | Action | Exemple |
|---|---|---|
| **P1** | **Ajouter ≥ 1 lien vers source hautement autoritative** par article | `docs.docker.com`, `learn.microsoft.com`, `tools.ietf.org/html/rfc...` |
| **P1** | **Ajouter des liens vers man pages** pour les commandes Linux | `man7.org/linux/man-pages/man8/ip.8.html` |
| **P2** | **Citer les RFC** pour les articles réseau/sécurité | RFC 791 (IP), RFC 6749 (OAuth) |
| **P2** | **Citer OWASP / NIST** pour les articles sécurité | OWASP Top 10, CIS Benchmarks |
| **P3** | **Stratégie de link building** : répondre sur Reddit/StackOverflow avec liens contextuels | — |

---

## 4. Trustworthiness (T) — 7.0/10

### 4.1 Transparence de l'identité

| Élément | État |
|---|---|
| Nom réel | **Brandon Visca** — présent partout |
| Email de contact | **contact@brandonvisca.com** — présent |
| Page `/about/` | **Détaillée** avec setup réel |
| Politique de confidentialité | **À vérifier** — page `privacy.md` ou `confidentialite.md` ? |
| Mentions légales | **À vérifier** |

### 4.2 Liens affiliés et disclosures

| Élément | État | Problème |
|---|---|---|
| Liens Amazon (`amzn.to`) | **Présents** dans quelques articles hardware | Pas de **disclosure visible** ("lien affilié") |
| Liens sponsorisés | Non identifiés | — |
| Autres affiliés | Non identifiés | — |

> **Risque** : L'absence de disclosure pour les liens affiliés est une violation des guidelines FTC (US) et peut impacter la confiance Google.

### 4.3 Sécurité technique

| Élément | État |
|---|---|
| HTTPS | **Actif** (Cloudflare Pages) |
| HSTS | **Présent** (`public/_headers`) |
| CSP | **Présent** |
| X-Frame-Options | **Présent** |
| Referrer-Policy | **Présent** |
| Permissions-Policy | **Présent** |

### 4.4 Recommandations

| Priorité | Action | Effort |
|---|---|---|
| **P1** | **Ajouter une disclosure affilié** près des liens Amazon | Faible |
| **P1** | **Créer / vérifier la page politique de confidentialité** | Faible |
| **P1** | **Créer / vérifier la page mentions légales** | Faible |
| **P2** | **Ajouter une page `/transparence/`** listant tous les liens affiliés et sponsors | Moyen |
| **P3** | **Ajouter un "Dernière vérification"** sur les articles techniques avec date | Faible |

---

## 5. Matrice E-E-A-T par article (échantillon)

| Article | E | Ex | A | T | Note |
|---|---|---|---|---|---|
| iTerm2 guide | 7 | 7 | 6 | 8 | Fort — screenshots, config perso |
| Oh-My-Zsh guide | 7 | 7 | 5 | 8 | Fort — mais liens externes limités |
| Arc Browser | 6 | 6 | 5 | 7 | Moyen — review, pas d'usage long terme clair |
| Proxmox LXC guide | 9 | 7 | 7 | 8 | Très fort — setup réel, preuves |
| Omarchy Linux | 5 | 5 | 4 | 7 | Faible — review rapide, peu de preuves |
| Auto-hébergement complet | 9 | 7 | 7 | 8 | Très fort — détails du setup réel |
| Snipe-IT vs GLPI | 7 | 7 | 6 | 7 | Fort — comparatif structuré |
| Nginx sécurité | 6 | 7 | 7 | 8 | Fort — mais pourrait citer RFC/OWASP |
| Raycast extensions | 7 | 7 | 5 | 8 | Fort — usage réel apparent |
| Jellyfin Docker | 7 | 7 | 6 | 8 | Fort — service auto-hébergé |

---

## 6. Plan d'action E-E-A-T

### Court terme (cette semaine)

1. **Remplir le CV** (`src/pages/cv.md`) avec l'expérience professionnelle réelle
2. **Ajouter une disclosure** "Liens affiliés" sur les articles concernés
3. **Vérifier/créer** les pages légales (confidentialité, mentions légales)
4. **Enrichir le schema `Person`** dans `PostDetails.astro` (voir `SCHEMA_AUDIT_2026-05-06.md`)

### Moyen terme (ce mois)

5. **Ajouter une photo réelle** de l'auteur (`public/avatar.webp` ou similaire)
6. **Créer un profil LinkedIn** et l'ajouter aux réseaux sociaux
7. **Ajouter ≥ 1 lien autoritatif** (docs officielles, RFC, etc.) aux 22 articles sans lien externe
8. **Systématiser les mentions de setup** : "Testé sur Proxmox 8.2 / Debian 12"

### Long terme (ce trimestre)

9. **Stratégie de link building** : réponses StackOverflow, Reddit, HackerNews avec liens contextuels
10. **Guest posts** sur des blogs techniques francophones (Le Journal du Hacker, LinuxFr, etc.)
11. **Ajouter des témoignages / retours** des lecteurs si disponibles
12. **Créer une page `/transparence/`** listant affiliations et méthodologie

---

## 7. Suivi des métriques E-E-A-T

| KPI | Méthode de mesure | Fréquence |
|---|---|---|
| Score E-E-A-T perçu | Audit qualitatif manuel | Mensuel |
| Nombre de liens externes / article | Script d'analyse | Mensuel |
| Nombre d'articles avec source autoritative | Script d'analyse | Mensuel |
| Mentions branded (`brandonvisca`, `visbran`) dans GSC | Requête GSC | Mensuel |
| Nombre de rich results (FAQ, Article) | GSC > Enhancement | Mensuel |
| Backlinks entrants (domaines référents) | GSC > Links (si dispo) | Mensuel |

> Prochain audit E-E-A-T recommandé : 2026-06-06.
