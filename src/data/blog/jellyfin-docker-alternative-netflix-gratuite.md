---
title: "Jellyfin avec Docker : Ton Netflix Gratuit en 30 Min (Économise 378€/an)"
pubDatetime: "2025-10-26T20:59:01+01:00"
description: "Installe Jellyfin avec Docker en 20 min. Alternative Netflix auto-hébergée, économise 378€/an. Guide 2025 complet + transcoding 4K."
tags:
  - docker
  - auto-hebergement
  - homelab
  - linux
  - guide
  - intermediaire
---

## Table des matières

🎯 TL;DR
---

Tu paies Netflix + Disney+ + Prime Video = **378€/an** pour regarder des films ? Spoiler : tu peux héberger **ton propre Netflix avec Jellyfin** pour 0€ supplémentaire si tu as déjà un serveur (ou 4€/mois sur VPS).

**Ce que tu vas apprendre :**

- Installer Jellyfin avec Docker en 20 minutes chrono
- Organiser ta bibliothèque films/séries automatiquement (metadata, posters, sous-titres)
- Streamer sur TV, mobile, tablette, navigateur
- Transcoding 4K en temps réel (si ton serveur suit)
- Économiser 378€/an minimum en virant tes abonnements streaming
- Inviter famille/amis avec comptes séparés

**Prérequis :**

- Un serveur Linux (VPS, Raspberry Pi 4/5, vieux PC, NAS)
- 2 Go RAM minimum, 4 Go recommandé (8 Go pour transcoding 4K)
- Docker installé
- Espace disque selon ta collection (500 Go = ~200 films HD)
- 30 minutes de ton temps

---

Pourquoi Jellyfin > Netflix (et Plex, et Emby)
---

### Le calcul économique qui fait mal

**Abonnements streaming en 2025 :**

- Netflix Standard : 13,49€/mois = **162€/an**
- Disney+ Premium : 10,99€/mois = **132€/an**
- Prime Video : 6,99€/mois = **84€/an**
- Canal+ : 24,99€/mois = **300€/an** (si fan de sport/séries)

💰 **Total famille moyenne : 378-678€/an**

**Jellyfin auto-hébergé :**

- Serveur (si VPS) : 4-8€/mois = **48-96€/an**
- Électricité (Raspberry Pi) : **~10€/an**
- Contenu : **variable** (achats VOD, Blu-ray d’occasion, bibliothèque municipale…)

💰 **Économie réaliste sur 5 ans : 1 500-3 000€**

Et encore, si tu réutilises ton serveur Nextcloud ou un vieux PC, c’est **quasi gratuit**.

---

### Jellyfin vs Plex vs Emby : Le match

| Critère | Jellyfin | Plex | Emby |
|---|---|---|---|
| **Prix** | 🟢 Gratuit à vie | 🟡 Gratuit (limité) ou 5€/mois | 🟡 Gratuit (limité) ou 5€/mois |
| **Open source** | 🟢 100% | 🔴 Propriétaire | 🟡 Partiellement |
| **Vie privée** | 🟢 Aucune télémétrie | 🔴 Compte Plex obligatoire | 🟡 Compte optionnel |
| **Transcoding** | 🟢 Illimité | 🟡 Limité sans Plex Pass | 🟢 Illimité |
| **Apps mobiles** | 🟢 Gratuites | 🔴 5€ une fois | 🟡 Freemium |
| **Interface** | 🟡 Correcte | 🟢 Excellente | 🟢 Très bonne |
| **Plugins** | 🟢 Large choix | 🟡 Restreints | 🟡 Moyens |
| **Communauté FR** | 🟢 Active | 🟢 Très active | 🟡 Moyenne |

**Verdict :**

- **Tu veux gratuit + privé + sans limites** → **Jellyfin** ✅
- **Tu veux la meilleure interface** → Plex (mais tu paies)
- **Tu veux un mix** → Emby

💡 **Mon avis perso** : Jellyfin fait 95% du job de Plex gratuitement. L’interface est moins léchée mais tu t’y fais en 2 jours. Et surtout, **tes données restent chez toi**.

---

Jellyfin c’est quoi exactement ?
---

**En une phrase :** Un serveur multimédia qui transforme ta collection de films/séries en **Netflix personnel**.

**Ce que ça fait :**  
✅ Récupère automatiquement les **posters, synopsis, notes** (via TMDB/TVDB)  
✅ Organise ta bibliothèque par **films, séries, musique, photos**  
✅ **Transcode à la volée** (ton film 4K devient 720p si ton mobile est en 4G)  
✅ **Sous-titres automatiques** (recherche et téléchargement intégrés)  
✅ **Comptes utilisateurs** séparés (Papa voit pas les dessins animés des enfants)  
✅ **Reprise lecture** multi-appareils (tu commences sur TV, tu finis sur tablette)  
✅ **Apps dédiées** Android TV, Fire TV, Roku, iOS, Android, Web…

**Ce que ça fait PAS :**  
❌ Télécharger du contenu à ta place (c’est pas son job)  
❌ Gérer les DRM (pas de Netflix/Prime rippé)  
❌ Remplacer ta box TV (c’est complémentaire)

---
