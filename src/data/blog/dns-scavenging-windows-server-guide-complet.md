---
title: "DNS Scavenging Windows Server : automatiser le nettoyage DNS"
pubDatetime: "2025-07-13T22:45:43+02:00"
description: Découvre comment configurer le DNS Scavenging sous Windows Server pour automatiser le nettoyage des enregistrements obsolètes. Guide complet avec PowerS...
tags:
  - windows
  - sysadmin
  - intermediaire
  - dns
  - powershell
  - guide
---

-----------
## Table des matières


- [🧩 Comment fonctionne le DNS Scavenging ?](#%F0%9F%A7%A9-comment-fonctionne-le-dns-scavenging)
- [🛡️ Les avantages du DNS Scavenging](#%F0%9F%9B%A1%EF%B8%8F-les-avantages-du-dns-scavenging)
- [⚙️ Configuration du DNS Scavenging](#%E2%9A%99%EF%B8%8F-configuration-du-dns-scavenging)
  - [Prérequis avant de commencer](#prerequis-avant-de-commencer)
  - [Configuration via PowerShell (la méthode de pro)](#configuration-via-power-shell-la-methode-de-pro)
  - [Configuration via l’interface graphique](#configuration-via-linterface-graphique)
  - [Configuration par zone DNS](#configuration-par-zone-dns)
- [🔧 Configuration avancée : les réglages fins](#%F0%9F%94%A7-configuration-avancee-les-reglages-fins)
  - [Synchronisation avec DHCP](#synchronisation-avec-dhcp)
  - [Surveillance et logs](#surveillance-et-logs)
- [🚨 Pièges à éviter (ou comment ne pas tout casser)](#%F0%9F%9A%A8-pieges-a-eviter-ou-comment-ne-pas-tout-casser)
  - [❌ Erreur n°1 : Activer sans tester](#%E2%9D%8C-erreur-n-1-activer-sans-tester)
  - [❌ Erreur n°2 : Mauvaise synchronisation DHCP](#%E2%9D%8C-erreur-n-2-mauvaise-synchronisation-dhcp)
  - [❌ Erreur n°3 : Pas de sauvegarde](#%E2%9D%8C-erreur-n-3-pas-de-sauvegarde)
- [📊 Surveillance et maintenance](#%F0%9F%93%8A-surveillance-et-maintenance)
  - [Vérification périodique](#verification-periodique)
  - [Script de monitoring](#script-de-monitoring)
- [🎯 Bonnes pratiques](#%F0%9F%8E%AF-bonnes-pratiques)
  - [Configuration recommandée pour un environnement standard](#configuration-recommandee-pour-un-environnement-standard)
  - [Pour les environnements critiques](#pour-les-environnements-critiques)
- [🔗 Intégration avec l’écosystème Windows](#%F0%9F%94%97-integration-avec-lecosysteme-windows)
- [Conclusion : DNS propre, admin heureux](#conclusion-dns-propre-admin-heureux)


- - - - - -

Introduction : pourquoi ton DNS mérite un bon ménage
----------------------------------------------------

Spoiler : si tu administres un réseau Windows avec DHCP, ton serveur DNS accumule probablement des enregistrements obsolètes. Résultat ? Des conflits de noms, des résolutions foireuses et des utilisateurs qui viennent te voir avec des mines d’enterrement.

Le **DNS Scavenging** est cette fonctionnalité magique qui fait le ménage automatiquement. Et contrairement à ton bureau, ça marche vraiment.

- - - - - -

🧩 Comment fonctionne le DNS Scavenging ?
----------------------------------------

Le processus repose sur deux concepts principaux :

- **No-Refresh Interval** : Période pendant laquelle les mises à jour d’un enregistrement DNS ne sont pas acceptées pour éviter une charge excessive sur le serveur.
- **Refresh Interval** : Période pendant laquelle l’enregistrement doit être mis à jour avant d’être marqué comme obsolète.

Une fois ces deux périodes écoulées, l’enregistrement devient éligible au **Scavenging** et peut être supprimé automatiquement par le serveur DNS.

**En gros** : si un enregistrement n’a pas donné signe de vie pendant `No-Refresh + Refresh`, il dégage.

- - - - - -

🛡️ Les avantages du DNS Scavenging
----------------------------------

- ✅ **Nettoyage automatique** des anciens enregistrements
- ✅ **Réduction des erreurs de résolution** dues aux enregistrements obsolètes
- ✅ **Optimisation des performances** du serveur DNS
- ✅ **Moins de galères** pour toi (et ça, c’est le plus important)

- - - - - -

⚙️ Configuration du DNS Scavenging
----------------------------------

### Prérequis avant de commencer

**⚠️ IMPORTANT** : Assure-toi que tes serveurs DHCP et DNS sont correctement synchronisés. Sinon, tu risques de supprimer des enregistrements encore actifs.

### Configuration via PowerShell (la méthode de pro)

```bash
# Activer le scavenging sur le serveur
Set-DnsServerScavenging -ScavengingState $true

# Définir les intervalles (en jours)
Set-DnsServerZoneAging -Name "cafe.local" -NoRefreshInterval 7.00:00:00 -RefreshInterval 7.00:00:00

# Démarrer immédiatement le processus de scavenging
Start-DnsServerScavenging

```

# Pour activer le scavenging sur une zone spécifique
Set-DnsServerZoneAging -Name "tondomaine.local" -Aging $true

# Vérifier la configuration
Get-DnsServerZoneAging -Name "tondomaine.local"


- - - - - -

🔧 Configuration avancée : les réglages fins
-------------------------------------------

Pour les environnements complexes avec plusieurs contrôleurs de domaine, assure-toi de bien maîtriser [la gestion des rôles FSMO](https://brandonvisca.com/activedirectory-transfere-des-roles-fsmo/) avant de déployer le scavenging.

### Synchronisation avec DHCP

Si tu utilises DHCP (et tu devrais), synchronise les durées :

```bash
# Durée de bail DHCP : 8 jours
# No-Refresh Interval : 7 jours  
# Refresh Interval : 7 jours
# Total avant suppression : 14 jours

Set-DnsServerZoneAging -Name "tondomaine.local" -NoRefreshInterval 7.00:00:00 -RefreshInterval 7.00:00:00

```

# Activer les logs détaillés
Set-DnsServerDiagnostics -SaveLogsToPersistentStorage $true -EnableLogFileRollover $true

# Vérifier les enregistrements éligibles au scavenging
Get-DnsServerResourceRecord -ZoneName "tondomaine.local" | Where-Object {$_.TimeStamp -lt (Get-Date).AddDays(-14)}


- - - - - -

🚨 Pièges à éviter (ou comment ne pas tout casser)
-------------------------------------------------

### ❌ Erreur n°1 : Activer sans tester

**Le piège** : Activer le scavenging sur toutes les zones d’un coup. **La solution** : Teste d’abord sur une zone de dev ou non-critique.

### ❌ Erreur n°2 : Mauvaise synchronisation DHCP

**Le piège** : Intervalles DNS plus courts que les baux DHCP. **La solution** : `Durée DHCP = No-Refresh + Refresh + marge de sécurité`.

### ❌ Erreur n°3 : Pas de sauvegarde

**Le piège** : « Ça va bien se passer… » **La solution** : Sauvegarde ta zone DNS avant d’activer le scavenging.

```bash
# Export de sauvegarde
dnscmd /zoneexport tondomaine.local tondomaine_backup.txt

```

# Vérifier l'état du scavenging
Get-DnsServerScavenging

# Voir les dernières suppressions
Get-WinEvent -FilterHashtable @{LogName='DNS Server'; ID=1541}

# Statistiques de la zone
Get-DnsServerStatistics


### Script de monitoring

```bash
# Script à lancer en tâche planifiée
$ZoneName = "tondomaine.local"
$Records = Get-DnsServerResourceRecord -ZoneName $ZoneName
$StaleRecords = $Records | Where-Object {$_.TimeStamp -lt (Get-Date).AddDays(-30)}

if ($StaleRecords.Count -gt 100) {
    # Envoyer une alerte
    Write-EventLog -LogName "Application" -Source "DNS Monitoring" -EventId 1001 -Message "Trop d'enregistrements obsolètes détectés : $($StaleRecords.Count)"
}

```

