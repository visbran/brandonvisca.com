# Rapport d'audit — brandonvisca.com

> Date : 2026-04-06
> Total articles analysés : 77

---

## Résumé exécutif

| Mission | Articles modifiés |
|---------|-------------------|
| Mission 1 — Suppression sections internes | 8 |
| Mission 2 — Correction liens Obsidian | 6 |
| Mission 3 — Ajout Table des matières | 8 |
| Mission 4 — Audit tags | Rapport dans TAGS_AUDIT.md |

---

## Mission 1 — Sections de documentation interne supprimées

Sections supprimées : `## 📊 Paramètres Rank Math SEO`, `## 🔄 Maillage inverse à effectuer`, `## 🔗 Maillage interne`, `## 📝 Articles complémentaires suggérés`

### Fichiers modifiés (8)

1. **`2026-03-10-restaurer-vm-hyperv-vhdx-os-corrompu-winpe.md`**
   - Supprimé : `## 📊 Paramètres Rank Math`, `## 🔗 Maillage interne`, `## 📝 Articles complémentaires suggérés`

2. **`2026-03-10-hyperv-gen1-vs-gen2-quelle-generation-choisir.md`**
   - Supprimé : `## 📊 Paramètres Rank Math`, `## 🔗 Maillage interne`, `## 📝 Articles complémentaires suggérés`

3. **`2026-03-14-partager-mot-de-passe-securise-comparatif.md`**
   - Supprimé : `## 📊 Paramètres Rank Math`, `## 🔄 Maillage inverse suggéré`, `## 📝 Articles complémentaires à créer`

4. **`2025-02-16-android-file-transfer-mac-alternatives-test-2025.md`**
   - Supprimé : `## 📊 Paramètres Rank Math SEO` (incluant catégories/tags WordPress)

5. **`2025-11-27-rcmd-alternative-cmd-tab-macos.md`**
   - Supprimé : `## 📊 Paramètres Rank Math SEO`, `## 🔄 Maillage inverse à effectuer`, `## 📝 Articles complémentaires suggérés`

6. **`2025-11-27-lunar-luminosite-ecrans-externes-macos.md`**
   - Supprimé : `## 📊 Paramètres Rank Math SEO`, `## 🔄 Maillage inverse à effectuer`, `## 📝 Articles complémentaires suggérés`

7. **`2025-11-27-clop-compression-images-videos-macos.md`**
   - Supprimé : `## 📊 Paramètres Rank Math SEO`, `## 🔄 Maillage inverse à effectuer`, `## 📝 Articles complémentaires suggérés`

8. **`2025-11-27-cling-recherche-fuzzy-fichiers-macos.md`**
   - Supprimé : `## 📊 Paramètres Rank Math SEO`, `## 🔄 Maillage inverse à effectuer`

### Sections conservées (contenu légitime)

Les sections suivantes ont été **intentionnellement conservées** car elles contiennent du contenu publié légitime (liens vers d'autres articles du site avec des URLs réelles) :

- `docker-debutant-services-auto-heberger.md` — `### 📚 Articles complémentaires sur ce site` → liens HTML valides
- `auto-hebergement-guide-complet-2025.md` — mention dans le TOC → liens HTML valides
- `installer-localwp-wordpress-local.md` — `**🔗 Articles complémentaires :**` → liens HTML valides
- `independance-numerique-2025-guide-complet.md` — mentions de `Checklist PDF` → contenu légitime de l'article
- `uptimerobot-guide-complet-monitoring-infrastructure.md` — `### Checklist de démarrage` → contenu légitime
- `migration-wordpress-all-in-one-guide-2025.md` — `### Checklist post-restauration` → contenu légitime
- `proteger-nginx-fichiers-sensibles-et-uploads.md` — `Checklist à appliquer` → contenu légitime

---

## Mission 2 — Liens Obsidian corrigés

### Fichiers modifiés (6)

1. **`alttab-macos-gestion-fenetres-windows.md`**
   - Supprimé : `![[nhl-minnesota-wild-welcome-home-ae7si3lopyj8q.gif]]` (image Obsidian orpheline)

2. **`2025-11-27-rcmd-alternative-cmd-tab-macos.md`**
   - 6 wiki-links convertis en texte brut dans les sections corps (intégrations, alternatives, verdict, articles connexes)
   - Wiki-links de la section interne supprimés avec la section (Mission 1)

3. **`2025-11-27-lunar-luminosite-ecrans-externes-macos.md`**
   - 4 wiki-links convertis en texte brut (installation Homebrew, verdict, articles connexes)

4. **`2025-11-27-clop-compression-images-videos-macos.md`**
   - 5 wiki-links convertis en texte brut (Homebrew, WebP références, verdict, articles connexes)

5. **`2025-11-27-cling-recherche-fuzzy-fichiers-macos.md`**
   - 5 wiki-links convertis en texte brut (Homebrew, Raycast comparaison, verdict, articles connexes)

6. **`2026-03-10-restaurer-vm-hyperv-vhdx-os-corrompu-winpe.md`**
   - 1 wiki-link supprimé avec la section Maillage interne

### Règle appliquée

- `[[slug|Texte affiché]]` → `Texte affiché` (texte seul, sans lien)
- `[[slug]]` → `slug` (texte brut)
- `![[image.gif]]` → supprimé (image Obsidian sans équivalent web)

---

## Mission 3 — Table des matières

### Articles avec TOC après audit : 74 / 77

### Articles auxquels le TOC a été ajouté (8)

| Fichier | Sections ## | Position d'insertion |
|---------|-------------|---------------------|
| `2026-03-10-restaurer-vm-hyperv-vhdx-os-corrompu-winpe.md` | 16 | Après intro (avant `## 📋 Prérequis`) |
| `2026-03-10-hyperv-gen1-vs-gen2-quelle-generation-choisir.md` | 9 | Après intro (avant `## TL;DR`) |
| `2026-03-14-partager-mot-de-passe-securise-comparatif.md` | 8 | Après intro (avant `## TL;DR`) |
| `2025-02-16-android-file-transfer-mac-alternatives-test-2025.md` | 10 | Après intro (avant `## 🎯 TL;DR`) |
| `2025-11-27-rcmd-alternative-cmd-tab-macos.md` | 14 | Après intro (avant `## TL;DR`) |
| `2025-11-27-lunar-luminosite-ecrans-externes-macos.md` | 17 | Après intro (avant `## Qu'est-ce que Lunar ?`) |
| `2025-11-27-clop-compression-images-videos-macos.md` | 14 | Après intro (avant `## Qu'est-ce que Clop ?`) |
| `2025-11-27-cling-recherche-fuzzy-fichiers-macos.md` | 15 | Après intro (avant `## TL;DR`) |

### Articles sans TOC (3) — non modifiés

Ces articles n'ont pas été modifiés car le TOC n'est pas nécessaire :

| Fichier | Raison |
|---------|--------|
| `alttab-macos-gestion-fenetres-windows.md` | 1 seule section `##` — article court |
| `p1622.md` | Draft, uniquement des `###` (pas de `##`) |
| `import-pst-outlook-365-guide-complet.md` | TOC manuel existant via blockquote `>` |

---

## Mission 4 — Audit des tags

Voir le fichier détaillé : **`TAGS_AUDIT.md`**

### Statistiques clés

- Total tags uniques : ~120
- Tags primaires recommandés : 12
- Tags avec accents (non conformes) : 4 (`productivité`, `luminosité`, `vidéos`, `récupération`)
- Tags en anglais à remplacer : 3 (`self-hosting`, `troubleshooting`, `productivity`)
- Tags "fourre-tout" à corriger : 8 articles avec tag `autres`

### Actions manuelles recommandées (non appliquées automatiquement)

Les corrections de tags touchent au frontmatter — elles n'ont pas été appliquées automatiquement pour respecter la contrainte de non-modification du frontmatter. À faire manuellement :

1. **`2025-11-27-rcmd-alternative-cmd-tab-macos.md`** : remplacer `productivité` par `productivite`
2. **`2025-11-27-lunar-luminosite-ecrans-externes-macos.md`** : supprimer `luminosité` et `ddc` et `ecrans-externes` (trop spécifiques)
3. **`2025-11-27-clop-compression-images-videos-macos.md`** : remplacer `vidéos` par `multimedia` ou supprimer
4. **`2026-03-10-restaurer-vm-hyperv-vhdx-os-corrompu-winpe.md`** : remplacer `récupération` par `depannage`
5. **`auto-hebergement-guide-complet-2025.md`** : supprimer `self-hosting` (doublon avec `auto-hebergement`)
6. **`omarchy-distribution-linux-arch-hyprland.md`** : remplacer `productivity` par `productivite`
7. **8 articles avec `autres`** : assigner des tags thématiques réels lors de la publication

---

## Statistiques globales

| Métrique | Valeur |
|----------|--------|
| Total articles | 77 |
| Articles publiés (draft: false) | ~50 |
| Articles en draft | ~27 |
| Articles avec TOC | 74 |
| Articles sans TOC | 3 |
| Articles modifiés (mission 1) | 8 |
| Articles modifiés (mission 2) | 6 |
| Articles modifiés (mission 3) | 8 |
| Total articles modifiés (combiné) | 14 (certains dans plusieurs missions) |
| Wiki-links Obsidian supprimés/convertis | ~30 |
| Sections Rank Math supprimées | 8 |
| Tags uniques inventoriés | ~120 |

---

## Problèmes non corrigés automatiquement

### 1. Tags avec accents dans le frontmatter (4 fichiers)

Non modifiés car la contrainte est de ne pas toucher au frontmatter. À corriger manuellement selon le plan de consolidation dans `TAGS_AUDIT.md`.

### 2. Articles avec tag `autres` (8 articles draft)

Les articles `p1515`, `p1569`, `p1593`, `p1602`, `p1636`, `p1622`, `ladybird-browser`, `ldap-filtrage-utilisateurs-snipeit` utilisent le tag fourre-tout `autres`. À corriger lors de leur publication.

### 3. Section "Articles connexes" sans vrais liens (4 articles)

Les articles `rcmd`, `lunar`, `clop`, `cling` ont une section `## 🔗 Articles connexes qui pourraient t'intéresser` avec désormais du texte brut (les wiki-links ont été convertis). Ces sections seraient plus utiles avec de vrais liens Markdown vers les articles publiés. À améliorer manuellement :

```markdown
- **[rcmd : Le raccourci qui tue Cmd+Tab](/rcmd-alternative-cmd-tab-macos/)** : Switch entre apps ultra-rapidement
```

### 4. Double `---` dans lunar

`2025-11-27-lunar-luminosite-ecrans-externes-macos.md` contient un double séparateur `---` en début de fichier (ligne 14 et 24). Non modifié pour ne pas casser la structure, mais à vérifier visuellement.
