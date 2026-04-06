# Audit des tags — brandonvisca.com

> Généré le 2026-04-06 — 77 articles analysés

---

## 1. Inventaire complet des tags (par fréquence)

### Tags très fréquents (10+)

| Tag | Occurrences | Catégorie |
|-----|-------------|-----------|
| `guide` | ~45 | Meta |
| `macos` | ~25 | OS |
| `tutoriel` | ~13 | Meta |
| `productivite` | ~12 | Meta |
| `intermediaire` | ~14 | Niveau |
| `debutant` | ~12 | Niveau |
| `linux` | ~16 | OS |
| `avance` | ~11 | Niveau |
| `docker` | ~9 | Tech |
| `securite` | ~9 | Thème |

### Tags fréquents (5–10)

| Tag | Occurrences |
|-----|-------------|
| `auto-hebergement` | 7 |
| `homelab` | 6 |
| `snipeit` | 6 |
| `active-directory` | 6 |
| `homebrew` | 7 |
| `windows` | ~8 |
| `terminal` | 6 |
| `sysadmin` | 7 |
| `powershell` | 5 |
| `nginx` | 5 |
| `itsm` | 5 |
| `low-tech` | 4 |
| `comparatif` | 4 |
| `navigateur` | 4 |

### Tags peu fréquents (2–4)

`wordpress` (3), `microsoft-365` (3), `office365` (3), `email` (3), `backup` (3), `docker-compose` (4), `arc-browser` (3), `windows-server` (4), `devops` (3), `homebrew` (7)

---

## 2. Problèmes identifiés

### 2.1 Tags avec accents (non conformes à la convention kebab-case)

Ces tags ne respectent pas la convention et peuvent créer des URLs problématiques ou des doublons invisibles :

| Tag incorrect | Occurrences | Fichier(s) concerné(s) | Tag correct |
|---------------|-------------|------------------------|-------------|
| `productivité` | 1 | `2025-11-27-rcmd-alternative-cmd-tab-macos.md` | `productivite` |
| `luminosité` | 1 | `2025-11-27-lunar-luminosite-ecrans-externes-macos.md` | luminosité → à supprimer (doublon thématique) |
| `vidéos` | 1 | `2025-11-27-clop-compression-images-videos-macos.md` | `videos` ou supprimer |
| `récupération` | 1 | `2026-03-10-restaurer-vm-hyperv-vhdx-os-corrompu-winpe.md` | `recuperation` |

### 2.2 Doublons / Incohérences

| Tags en conflit | Recommandation |
|-----------------|----------------|
| `microsoft-365` et `office365` | Garder `microsoft-365`, supprimer `office365` |
| `auto-hebergement` et `self-hosting` | Garder `auto-hebergement` (français), supprimer `self-hosting` |
| `homelab` et `auto-hebergement` | Les deux sont légitimes — `homelab` = infrastructure, `auto-hebergement` = services |
| `tutoriel` et `guide` | Fusionner : garder `guide` uniquement |
| `troubleshooting` et `depannage` | Garder `depannage` (français) |
| `productivity` (anglais, omarchy) | Remplacer par `productivite` |

### 2.3 Tags trop spécifiques (utilisés une seule fois, peu utiles SEO)

Ces tags ne génèrent aucun trafic et encombrent la navigation :

`music-decoy`, `warp-terminal`, `iterm2-alternative`, `putty-alternative`, `1password-alternative`, `netflix-alternative`, `plex-alternative`, `google-alternative`, `google-drive-alternative`, `spotlight-alternative`, `handbrake-alternative`, `swappiness`, `s3cmd`, `azure-ad-connect`, `catppuccin`, `timedatectl`, `super-so`, `notion-sites`, `tiling-wm`, `omarchy`, `arc-search`, `sigma-os`, `zen-browser`, `news`, `cwebp`, `web-publishing`, `high-availability`, `outils-systeme`, `low-tech`, `ddc`, `ecrans-externes`, `fuzzy-search`, `spotlight`, `power-users`, `batch-processing`, `video-editing`

### 2.4 Tags "niveaux" (meta-tags non thématiques)

`debutant`, `intermediaire`, `avance` et `guide`/`tutoriel` sont des meta-tags qui polluent la liste de tags visibles. Ils ne correspondent à aucune catégorie de contenu. Recommandation : les conserver pour l'indexation interne mais ne pas les afficher dans la navigation principale.

### 2.5 Tag fourre-tout

`autres` — utilisé dans 8 articles drafts/non catégorisés (`p1515`, `p1569`, `p1593`, `p1602`, `p1636`, `p1622`, `ladybird-browser`, `ldap-filtrage-utilisateurs-snipeit`). À remplacer par les vrais tags thématiques lors de la publication.

---

## 3. Stratégie recommandée (deux niveaux)

### Niveau 1 — Tags primaires (navigation + SEO) — max 12

Ces tags doivent être les seuls visibles dans la navigation du blog. Choisir 1-2 par article maximum.

| Tag primaire | Thème couvert | Articles actuels |
|--------------|---------------|------------------|
| `homelab` | Infrastructure, serveurs persos, hardware | ~6 |
| `auto-hebergement` | Services auto-hébergés, Docker, Nextcloud | ~7 |
| `linux` | Administration Linux, CLI, serveurs | ~16 |
| `macos` | Apps macOS, productivité Mac | ~25 |
| `windows` | Windows Server, Active Directory, outils | ~8 |
| `docker` | Docker, docker-compose, conteneurs | ~9 |
| `securite` | Sécurité serveur, Nginx, chiffrement | ~9 |
| `reseau` | pfSense, DNS, Pi-hole, réseau | ~3 |
| `productivite` | Outils de productivité, workflow | ~12 |
| `sysadmin` | Administration système, PowerShell, AD | ~7 |
| `developpement` | Dev tools, éditeurs, terminal | ~6 |
| `microsoft-365` | Office 365, Exchange, Teams | ~3 |

### Niveau 2 — Tags secondaires (longue traîne SEO) — max 4 par article

Ces tags sont plus spécifiques, utiles pour le SEO de niche mais pas pour la navigation.

Exemples par cluster :
- Homelab : `proxmox`, `pihole`, `hyper-v`, `vaultwarden`, `jellyfin`, `nextcloud`
- macOS : `homebrew`, `raycast`, `iterm2`, `warp-terminal`, `terminal`
- Sécurité Linux : `nginx`, `hardening`, `ssh`, `headers-http`
- Active Directory : `active-directory`, `powershell`, `ldap`, `snipeit`
- WordPress : `wordpress`, `migration`, `mysql`

---

## 4. Plan de consolidation

### Tags à fusionner

| Tag à supprimer | Tag cible | Action |
|-----------------|-----------|--------|
| `office365` | `microsoft-365` | Remplacer dans tous les articles |
| `self-hosting` | `auto-hebergement` | Remplacer dans auto-hebergement-guide-complet-2025.md |
| `tutoriel` | `guide` | Fusionner (garder `guide`) |
| `troubleshooting` | `depannage` | Remplacer dans wordpress-repair, depannage-raid |
| `productivity` (anglais) | `productivite` | Remplacer dans omarchy |
| `productivité` (avec accent) | `productivite` | Corriger dans rcmd |
| `luminosité` | supprimer | Tag trop spécifique sans valeur SEO |
| `vidéos` | `multimedia` ou supprimer | Corriger dans clop |
| `récupération` | `depannage` | Corriger dans hyper-v-restaurer |
| `autres` | tags thématiques réels | À corriger article par article lors de publication |

### Tags à supprimer (sans remplacement)

Tags inutiles pour le SEO ou la navigation :
- `music-decoy`, `morgen`, `wailbrew`, `alttab`, `ice`, `appcleaner`, `shutter-encoder`, `vanderplanki`, `nebula-sync`, `notion-sites`, `super-so`, `omarchy` → les noms de produits comme tags uniques n'apportent rien
- `high-availability`, `synchronisation` (dans nebula-sync) → trop génériques
- `low-tech` → trop vague, non-standard

---

## 5. Convention future pour l'ajout de tags

### Règles obligatoires

1. **Kebab-case strict, sans accents** : `auto-hebergement` pas `auto-hébergement`, `productivite` pas `productivité`
2. **Français uniquement** pour les tags thématiques visibles (sauf noms propres : `docker`, `nginx`, `hyper-v`)
3. **Maximum 6 tags par article** : 1-2 primaires + max 4 secondaires
4. **Toujours inclure un tag primaire** parmi : `homelab`, `auto-hebergement`, `linux`, `macos`, `windows`, `docker`, `securite`, `reseau`, `productivite`, `sysadmin`, `developpement`, `microsoft-365`
5. **Toujours inclure un niveau** : `debutant`, `intermediaire`, ou `avance`
6. **Ne jamais utiliser `autres`** — toujours trouver le vrai tag thématique

### Gabarit recommandé

```yaml
tags:
  - [tag-primaire-1]       # ex: macos
  - [tag-primaire-2]       # ex: productivite (optionnel)
  - [tag-secondaire-1]     # ex: homebrew
  - [tag-secondaire-2]     # ex: raycast
  - [niveau]               # debutant | intermediaire | avance
  - guide                  # toujours
```

### Exemples corrects

```yaml
# Article sur Homebrew macOS
tags:
  - macos
  - developpement
  - homebrew
  - terminal
  - debutant
  - guide

# Article sécurité Nginx
tags:
  - linux
  - securite
  - nginx
  - headers-http
  - avance
  - guide
```
