---
title: "Importer un fichier PST dans Outlook 365 : 2 méthodes qui marchent (2026)"
description: "Importer un fichier PST dans Outlook 365 : 2 méthodes testées + XstReader gratuit pour lire tes archives sans Outlook. Guide pas à pas 2026."
pubDatetime: "2025-02-21T10:14:37+01:00"
modDatetime: 2026-05-17 00:00:00+01:00
author: Brandon Visca
tags:
  - microsoft-365
  - sysadmin
  - guide
  - intermediaire
featured: false
draft: false
focusKeyword: fichier PST dans Outlook 365
faqs:
  - question: "Peut-on importer un PST dans Outlook 365 sans installer le client lourd (desktop) ?"
    answer: "Non, l'import PST natif nécessite Outlook desktop (Windows ou Mac). Outlook Web (OWA) ne supporte pas l'import PST. Des outils tiers comme XstReader permettent de lire un PST sans Outlook."
  - question: "Quelle est la taille maximale d'un fichier PST supportée par Outlook 365 ?"
    answer: "Outlook 365 supporte les PST jusqu'à 50 Go. Au-delà, l'import peut échouer ou être très lent. La recommandation Microsoft est de scinder les gros PST avant import."
  - question: "Comment lire un fichier PST sans avoir Outlook installé ?"
    answer: "XstReader (gratuit, open source) permet de lire les PST et OST sur Windows et Linux sans Outlook. Il supporte la recherche, l'export en EML et l'affichage des pièces jointes."
---
> 💡 **TL;DR**
> - Microsoft a supprimé l'import PST du nouvel Outlook 365 — mais deux alternatives fonctionnent
> - **Méthode 1** : importer via l'ancien Outlook (2016-2019 ou Outlook 365 classique avant mi-2024)
> - **Méthode 2** : XstReader, outil gratuit open source pour lire et exporter tes PST sans Outlook

## Table des matières

## Le drame en 3 actes

**Acte 1** : Tu lances Outlook 365 tout content.
**Acte 2** : Tu cherches « Importer/Exporter » → Introuvable.
**Acte 3** : Tu réalises que tes 10 ans d'emails sont coincés dans un `.pst`

Si tu reconnais ce scénario, bienvenue au club. Avec plus d'un milliard d'utilisateurs Outlook dans le monde, on est quelques-uns à s'être fait avoir par cette « évolution » de Microsoft.

**La vraie raison ?** Microsoft veut tout pousser dans le cloud Exchange Online. Les fichiers PST, c'est l'ancien monde. Pas rentable, pas contrôlable, pas moderne.

Résultat : tu te retrouves avec tes précieuses archives sur les bras et aucun moyen « officiel » de les récupérer.

**Bonne nouvelle :** Il reste des solutions. On va voir ça.

---

## Pourquoi importer un fichier PST dans Outlook 365 est devenu compliqué

![Interface Outlook 365 import fichier PST tutorial](thedailyshow-7zio8wtexjcgzlq4mm.gif)

C'est simple : Microsoft gagne plus d'argent avec Exchange Online qu'avec du stockage local.

**Leur logique :**

- PST = stockage local = pas de revenus récurrents
- Exchange Online = abonnement mensuel = $$$
- Bonus : ils contrôlent tes données

**Pour toi, ça veut dire :**

- Plus de menu « Import/Export » dans le nouvel Outlook pour Windows (disponible depuis fin 2023)
- Migration forcée vers les boîtes en ligne (payantes)
- Fichiers > 2 GB ? Oublie, ça plante

Pour nous, administrateurs système qui devons gérer ces conneries au quotidien, c'est aussi frustrant que de [sécuriser un serveur Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/) avec des utilisateurs qui utilisent « password123 ».

---

## Solution 1 : La méthode oldschool (ancien Outlook)

### Ce qu'il te faut

- Outlook 2016, 2019 ou 2021 (versions desktop classiques)
- Ou Outlook 365 Desktop en version « classique » (pas le nouvel Outlook)
- Un environnement qui n'a pas encore été migré de force vers le nouvel Outlook

> ⚠️ **Attention** : si ton PST est corrompu, tu vas planter Outlook. Teste l'intégrité avant avec `scanpst.exe` (voir la section Pièges plus bas).

### La procédure qui marche

**Étape 1 :** Lance ton Outlook classique.

**Étape 2 :** Va dans `Fichier` → `Ouvrir et exporter` → `Importer/Exporter`.
*(Si tu vois pas ce menu, t'as déjà le nouvel Outlook → passe à la Solution 2)*

**Étape 3 :** Sélectionne « Importer à partir d'un autre programme ou fichier ».

**Étape 4 :** Choisis « Fichier de données Outlook (.pst) ».

**Étape 5 :** Configuration (la partie critique) :
- Trouve ton fichier `.pst`
- **Coche « Inclure les sous-dossiers »**. Sinon tu récupères que l'Inbox
- Option « Remplacer les doublons » → à toi de voir selon tes besoins

**Étape 6 :** Clique « Terminer » et va prendre un café.

**Durée :** Entre 5 min (PST léger) et 30-45 min pour un fichier de 1.5 GB.

### Quand ça foire (et ça arrive)

**Import bloqué à 50% ?** → Ton PST dépasse 2 GB. Coupe-le en plusieurs fichiers plus petits ou utilise un outil de split PST.

**Outlook plante ?** → Pas assez de RAM ou PST fragmenté. Ferme tout, redémarre, divise par lots.

Si tu bosses en environnement AD et que ton PST est sur un partage réseau, assure-toi que ton [intégration Ubuntu Active Directory avec SSSD](https://brandonvisca.com/connecter-les-systemes-ubuntu-a-active-directory-en-utilisant-sssd/) permet l'accès aux fichiers. Ça peut paraître con, mais j'ai vu des gens galérer 2h là-dessus.

---

## Solution 2 : XstReader (le plan B qui sauve tout)

### Pourquoi c'est bien

XstReader, c'est le couteau suisse des PST. Gratuit, open source, et ça marche partout.

**Les plus :**

- ✅ **100% gratuit** (open source, aucune version premium)
- ✅ **Multi-plateforme** : Windows, Linux, macOS
- ✅ **Portable** : tu décompresses, tu lances
- ✅ **Lecture seule** : impossible de péter tes données par accident
- ✅ **Rapide** : même sur des PST de 2 GB+

**Les moins :**

- Interface en anglais seulement
- Export limité (pas de conversion massive vers un autre format)
- Nécessite .NET 6+ sur Windows

### Comment s'en servir

**Étape 1 : Télécharge XstReader**

Projet open source disponible sur GitHub :

```text
https://github.com/iluvadev/XstReader/releases
```

Télécharge la dernière release pour ton OS (portable, pas d'installateur). Tu décompresses et tu lances.

**Étape 2 : Ouvre ton PST**

Lance `XstReader.exe` → `File` → `Open` → sélectionne ton `.pst`.

**Étape 3 : Navigue et exporte**

L'arborescence de tes dossiers apparaît à gauche. Tu peux :
- Lire chaque email directement dans l'interface
- Exporter un dossier entier en `.eml` via clic droit → `Export`
- Chercher dans tous tes emails via la barre de recherche

> 💡 **Astuce** : XstReader gère aussi les fichiers `.ost` (boîtes Exchange locales). Pratique si tu as d'autres archives à dépoussiérer.

---

## FAQ

### Combien de temps ça prend ?

Ça dépend de la taille du PST et de la méthode :

| Taille PST | Méthode oldschool | XstReader |
|------------|-------------------|-----------|
| < 200 Mo | 2-5 min | Immédiat |
| 200 Mo – 1 GB | 10-20 min | 1-3 min |
| 1-2 GB | 20-45 min | 5-10 min |
| > 2 GB | Risqué (peut planter) | Fonctionne |

En environnement réseau, ajoute 30-50% de temps selon la latence.

### XstReader c'est vraiment gratuit ?

Oui. Open source sur GitHub. Aucune version premium, aucun compte requis.

### L'import échoue, je fais quoi ?

Commence par tester l'intégrité de ton PST avec `scanpst.exe` (Inbox Repair Tool, inclus dans Office) :

```text
C:\Program Files\Microsoft Office\root\Office16\SCANPST.EXE
```

Lance-le, pointe sur ton `.pst`, et laisse-le réparer. Ensuite retry l'import.

### Je peux traiter plusieurs PST en même temps ?

Avec la méthode oldschool : non, Outlook gère un import à la fois.
Avec XstReader : oui, ouvre plusieurs instances en parallèle.

---

## Les pièges à éviter

### « Le fichier .pst ne peut pas être ouvert »

**Cause :** PST corrompu ou verrouillé par un autre process.

**Fix :**
1. Vérifie qu'Outlook est bien fermé (y compris dans la tray)
2. Lance `scanpst.exe` sur le fichier
3. Si ça persiste → ouvre avec XstReader (mode lecture seule, moins exigeant)

### « Import partiel — la moitié des emails a disparu »

**Cause :** Case « Inclure les sous-dossiers » non cochée à l'étape 5.

**Fix :** Relance l'import, cette fois avec la case cochée. Outlook proposera de gérer les doublons.

### « Outlook freeze pendant l'import »

**Cause :** PST > 2 GB, mémoire insuffisante, ou antivirus qui scanne en temps réel.

**Fix :**
- Désactive temporairement l'antivirus pendant l'import
- Divise le PST en plusieurs fichiers < 1.5 GB
- Ferme toutes les autres apps avant de lancer

---

## Conclusion

Si tu dois importer un fichier PST dans Outlook 365, voilà le topo :

- **T'as encore l'ancien Outlook** (2016-2021 ou 365 classique) : utilise la méthode import native. Rapide, fiable, sans outil tiers.
- **T'as le nouvel Outlook** (la version avec l'interface simplifiée) : impossible en natif. XstReader est ta meilleure option.
- **Tu veux juste lire tes vieux emails sans importer** : XstReader directement, sans même ouvrir Outlook.

J'ai utilisé les deux méthodes en prod. La méthode oldschool reste la plus propre quand elle est disponible. XstReader sauve la mise quand elle ne l'est plus. Et si tu veux aller plus loin dans la protection de tes emails, j'ai un guide sur [Vanderplanki pour sauvegarder tes emails gratuitement](https://brandonvisca.com/vanderplanki-sauvegarde-emails-gratuit-multiplateforme/).

---

## Pour aller plus loin

- [Documentation Microsoft — Importer les emails et les contacts](https://support.microsoft.com/fr-fr/office/importer-les-e-mails-les-contacts-et-le-calendrier-outlook-71f8ef5a-80d8-4dbb-b9a7-4d73b4a09e46)
- [XstReader sur GitHub](https://github.com/iluvadev/XstReader/releases)
- [Exchange Online — bloquer les transferts automatiques d'emails](https://brandonvisca.com/exchange-online-bloquer-transferts-automatiques-emails/)
- [Vanderplanki : sauvegarde emails gratuit multiplateforme](https://brandonvisca.com/vanderplanki-sauvegarde-emails-gratuit-multiplateforme/)

## Articles connexes

- [Exchange Online : bloquer les transferts email automatiques avec PowerShell (2026)](/exchange-online-bloquer-transferts-automatiques-emails/)
- [Migrer WordPress gratuitement avec All-in-One WP Migration : guide 2026](/migration-wordpress-all-in-one-guide-2025/)
- [Pourquoi j&rsquo;ai quitté Google (et comment tu peux faire pareil en 2025)](/quitter-google-auto-hebergement/)
- [Sendme CLI : Transfert Fichiers P2P en 2 Commandes (Alternative scp Moderne)](/sendme-cli-transfert-fichiers-p2p-terminal/)
