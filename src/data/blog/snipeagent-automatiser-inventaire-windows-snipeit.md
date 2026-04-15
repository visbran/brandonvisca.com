---
title: "SnipeAgent : Automatiser l'inventaire Windows sans Excel ni galères"
description: "Automatise ton inventaire Windows avec SnipeAgent et Snipe-IT. Guide complet : installation, déploiement GPO, automatisation et dépannage. Fini Excel !"
pubDatetime: "2025-10-13T16:49:19+02:00"
modDatetime: "2026-04-15T00:00:00+01:00"
author: Brandon Visca
tags:
  - snipeit
  - snipeagent
  - windows
  - active-directory
  - powershell
  - intermediaire
featured: false
draft: false
focusKeyword: SnipeAgent
---
> 💡 **TL;DR**
> - SnipeAgent automatise l'inventaire Windows en alimentant Snipe-IT via son API
> - L'installeur MSI se déploie en masse via GPO sur tout un parc Active Directory
> - Une tâche planifiée au démarrage suffit pour maintenir l'inventaire à jour en continu

Installation, configuration, déploiement GPO — tout ce qu'il faut pour que SnipeAgent s'occupe de ton inventaire Windows à ta place. Admin sys junior ou homelab à la maison, même combat.

## Table des matières

## Pourquoi automatiser l'inventaire avec SnipeAgent ?

Si tu as déjà essayé de maintenir un inventaire IT à jour manuellement, tu connais la chanson : un PC qui change de bureau, une MAC address qui dérive, un numéro de série mal noté… Et ton Excel devient une fiction plus qu'un inventaire.

**SnipeAgent résout ce problème** en créant automatiquement des fiches d'actifs dans Snipe-IT avec toutes les infos importantes :

- Nom de la machine (hostname)
- Numéro de série unique
- Adresse MAC
- Marque et modèle (selon ce que Windows remonte)
- Localisation géographique (configurée dans l'agent)
- Garantie et statut (si tu les renseignes)

L'agent tourne en tâche planifiée, au démarrage ou à intervalle régulier. Tu le déploies une fois via GPO, et ensuite il fait le boulot tout seul. Parfait pour les environnements avec beaucoup de postes ou pour ton homelab si tu aimes savoir ce qui tourne où.

💡 **Bon à savoir** : SnipeAgent remplit automatiquement l'inventaire que tu auras déjà configuré dans ton installation Snipe-IT. Si tu n'as pas encore installé Snipe-IT, commence par lire mon [guide d'installation SnipeIT Ubuntu complet](https://brandonvisca.com/installation-snipeit-ubuntu-guide-complet/) avant de revenir ici.

---

## Prérequis : prépare ton environnement

Avant d'installer SnipeAgent, assure-toi d'avoir :

### Côté serveur Snipe-IT

- Une instance Snipe-IT fonctionnelle (auto-hébergée ou SaaS)
- Un utilisateur API avec les permissions minimales : **lecture + ajout** d'actifs (jamais de droits admin complets pour un agent !)
- Une clé API générée depuis ton compte Snipe-IT (`Paramètres > API Keys`)

Si ta configuration Snipe-IT est encore basique, jette un œil à mon article sur la [configuration avancée SnipeIT](https://brandonvisca.com/configuration-avancee-snipeit-ldap-teams-automatisation/) qui couvre notamment la création d'utilisateurs API sécurisés.

### Côté machines Windows

- Windows 10+ (en pratique, on est en 2026, tu as au moins du Windows 10, j'espère)
- Droits administrateur pour installer l'agent
- Accès réseau vers ton serveur Snipe-IT (HTTPS recommandé, évidemment)

⚠️ **Erreur fréquente** : Si ton Snipe-IT n'est pas en HTTPS, l'agent peut avoir des problèmes de connexion selon la config réseau. Sécurise ton serveur avant de déployer en prod.

---

## Installation de SnipeAgent sur Windows

SnipeAgent est distribué sous forme d'**installeur MSI**, donc c'est ultra simple à déployer, même en masse via GPO si tu bosses en environnement Active Directory.

### Étape 1 : Télécharge l'installeur

Rends-toi sur la page GitHub du projet : 👉 <https://github.com/ReticentRobot/SnipeAgent/releases>

Télécharge le fichier `.msi` de la dernière version stable. Au moment où j'écris ces lignes, c'est la version **1.x.x** (vérifie toujours la version la plus récente sur GitHub).

### Étape 2 : Installe l'agent

Lance l'installeur. Par défaut, il installe SnipeAgent dans :

```text
C:\Program Files (x86)\Snipe-IT\SnipeAgent\
```

### Étape 3 : Configure l'agent

Ouvre le fichier de configuration :

```text
C:\Program Files (x86)\Snipe-IT\SnipeAgent\SnipeAgent.exe.config
```

Tu dois renseigner **au minimum** ces paramètres critiques (dans mon homelab, c'est l'URL interne de mon instance Snipe-IT — ça marche nickel tant que le `BaseURI` est exact) :

```xml
<configuration>
  <appSettings>
    <add key="BaseURI" value="https://inventory.ton-domaine.com" />
    <add key="APIKey" value="ta-clé-api-ici" />
    <add key="Company" value="MaSociété" />
    <add key="Location" value="Bureau Paris" />
  </appSettings>
</configuration>
```

---

## Lancement de l'agent : deux approches

### Option 1 : Exécution manuelle (test)

Pour valider ta configuration avant de l'automatiser, exécute l'agent manuellement depuis un terminal administrateur :

```bat
cd "C:\Program Files (x86)\Snipe-IT\SnipeAgent\"
SnipeAgent.exe
```

L'agent va :

1. Se connecter à l'API Snipe-IT
2. Vérifier si un actif existe déjà pour cette machine (basé sur le numéro de série)
3. Créer ou mettre à jour la fiche d'actif

Si tout se passe bien, tu verras un message de confirmation. Direction ton interface Snipe-IT pour vérifier que la machine est bien apparue dans ton inventaire.

Tu peux aussi lancer l'agent en mode interactif pour avoir un retour visuel :

```bat
SnipeAgent.exe /interactive
```

### Option 2 : Automatisation via tâche planifiée (recommandé)

Pour automatiser, crée une **tâche planifiée Windows** (Task Scheduler) qui exécute l'agent :

- **Au démarrage de la machine** (avec un délai de 1 à 2 minutes pour laisser le réseau s'initialiser)
- **Tous les jours à heure fixe** (par exemple à 8h00 pour capturer les nouvelles machines)

Voici comment créer la tâche planifiée en PowerShell :

```powershell
$action = New-ScheduledTaskAction -Execute "C:\Program Files (x86)\Snipe-IT\SnipeAgent\SnipeAgent.exe"
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RunOnlyIfNetworkAvailable
Register-ScheduledTask -TaskName "SnipeAgent Inventory" -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest
```

---

## Dépannage : quand SnipeAgent ne veut pas coopérer

### Erreur : « Unauthorized » ou « 403 Forbidden »

→ Ta clé API est incorrecte ou les permissions sont insuffisantes. Vérifie dans Snipe-IT que l'utilisateur API a bien les droits de créer des actifs.

### L'agent ne trouve pas le serveur Snipe-IT

→ Vérifie ton `BaseURI`. Il doit pointer vers la **racine** de ton instance Snipe-IT (avec `/api` si nécessaire selon ta config). Teste l'URL dans un navigateur pour vérifier qu'elle répond.

### Les infos remontées sont incomplètes ou fausses

→ SnipeAgent récupère ce que Windows lui donne. Si ton PC est un clone ou un portable sans BIOS correctement configuré, les infos peuvent être vides. Tu peux compléter manuellement dans Snipe-IT ou ajuster ton fichier config pour forcer certaines valeurs.

### L'agent ne tourne pas au démarrage

→ Vérifie que la tâche planifiée est bien créée et active. Regarde les logs dans l'Observateur d'événements Windows (`Journaux Windows > Application`) pour identifier l'erreur.

---

## Alternatives et évolutions : comment aller plus loin

SnipeAgent est parfait pour les parcs Windows, mais si tu as un environnement hétérogène (Linux, macOS, équipements réseau), tu vas devoir compléter avec d'autres outils :

- **SNMP** pour les switches, routeurs, imprimantes
- **Scripts Python/Bash** pour les serveurs Linux (tu peux utiliser l'API Snipe-IT que j'ai documentée dans mon article sur la [configuration avancée SnipeIT](https://brandonvisca.com/configuration-avancee-snipeit-ldap-teams-automatisation/))
- **Jamf** ou équivalent pour les Mac (si t'as du budget)

Snipe-IT supporte l'import CSV, donc tu peux aussi scripter des collectes d'infos et les importer en masse. L'important c'est d'avoir **une source de vérité unique** pour ton inventaire.

Si tu veux aller encore plus loin dans l'automatisation de ton infrastructure Windows, fonce sur les **GPO avancées** et le scripting PowerShell. C'est le combo gagnant pour gérer un parc proprement.

---

## Conclusion : un inventaire qui se gère tout seul

SnipeAgent, c'est la solution pour arrêter de courir après ton inventaire IT. Une fois configuré, l'agent tourne en silence, remplit ta base Snipe-IT, et tu peux enfin te concentrer sur des trucs plus intéressants que compter des numéros de série.

Si t'es admin système ou que tu gères un homelab, cet outil va te faire gagner un temps fou. Et si t'es en entreprise, c'est la base d'une gestion de parc propre et auditable.

**Prochaine étape ?** Si tu n'as pas encore Snipe-IT d'installé, commence par mon [guide d'installation SnipeIT Ubuntu](https://brandonvisca.com/installation-snipeit-ubuntu-guide-complet/), puis reviens déployer SnipeAgent sur tes machines. Et si ton Snipe-IT est déjà en place mais encore basique, passe au niveau supérieur avec mon article sur la [configuration avancée SnipeIT](https://brandonvisca.com/configuration-avancee-snipeit-ldap-teams-automatisation/) (intégration LDAP, notifications Teams, API, etc.).

Spoiler : c'est satisfaisant de voir son inventaire se remplir tout seul.

---

## Pour aller plus loin

- [SnipeAgent sur GitHub](https://github.com/ReticentRobot/SnipeAgent) – Le repo officiel avec releases et doc
- [Snipe-IT Documentation](https://snipe-it.readme.io/) – Pour configurer ton serveur d'inventaire
- [Configuration avancée SnipeIT](https://brandonvisca.com/configuration-avancee-snipeit-ldap-teams-automatisation/) – LDAP, Teams, API et sécurité
