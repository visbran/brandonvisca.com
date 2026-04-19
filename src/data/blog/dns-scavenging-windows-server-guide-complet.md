---
title: "DNS Scavenging Windows Server : automatiser le nettoyage DNS"
description: Configure le DNS Scavenging Windows Server pour nettoyer automatiquement les enregistrements obsolètes. Scripts PowerShell et bonnes pratiques inclus.
pubDatetime: "2025-07-13T22:45:43+02:00"
modDatetime: 2026-04-19 00:00:00+01:00
author: Brandon Visca
tags:
  - sysadmin
  - windows-server
  - dns
  - powershell
  - guide
  - intermediaire
featured: false
draft: false
focusKeyword: DNS Scavenging Windows Server
faqs:
  - question: "Le DNS Scavenging peut-il supprimer des enregistrements statiques ?"
    answer: "Non. Le scavenging ne touche que les enregistrements dynamiques (créés via DHCP ou ddns). Les enregistrements statiques sont intouchables."
  - question: "Quels intervalles recommander pour No-Refresh et Refresh ?"
    answer: "7 jours chacun pour un environnement standard. Tes baux DHCP doivent dépasser 14 jours (No-Refresh + Refresh) pour éviter de supprimer des enregistrements encore actifs."
  - question: "Faut-il redémarrer le service DNS après configuration ?"
    answer: "Non. Les changements de configuration du scavenging sont pris en compte sans redémarrage du service DNS."
  - question: "Peut-on activer le scavenging sur plusieurs serveurs DNS ?"
    answer: "Oui, mais configure-le d'abord sur un seul serveur pour tester. Une fois validé, déploie sur les autres. Attention à la réplication AD — un seul serveur effectue réellement le scavenging par zone."
  - question: "Comment confirmer que le scavenging a bien supprimé des enregistrements ?"
    answer: "Filtre les Event ID 1541 dans le journal DNS Server (Get-WinEvent) ou lance Get-DnsServerScavenging pour voir la date du dernier passage."
---
> 💡 **TL;DR**
> - Le DNS Scavenging supprime automatiquement les enregistrements DNS obsolètes via deux intervalles : No-Refresh + Refresh
> - Active-le en PowerShell avec `Set-DnsServerScavenging` et `Set-DnsServerZoneAging` : 3 commandes suffisent
> - Synchronise toujours tes intervalles avec la durée de bail DHCP pour éviter les suppressions intempestives

---

## Pourquoi ton DNS mérite un bon ménage

Spoiler : si tu administres un réseau Windows avec DHCP, ton serveur DNS accumule probablement des enregistrements obsolètes. Résultat ? Des conflits de noms, des résolutions foireuses et des utilisateurs qui viennent te voir avec des mines d'enterrement.

Le **DNS Scavenging Windows Server** est la fonctionnalité qui fait le ménage automatiquement. Et contrairement à ton bureau, ça marche vraiment.

Dans mon labo Windows Server 2022 avec 200+ postes en DHCP dynamique, je laissais tourner sans scavenging. Après 6 mois : 400+ enregistrements fantômes pour des machines éteintes depuis longtemps. Activé le scavenging un vendredi soir, 300 enregistrements nettoyés au lundi matin. Depuis, c'est automatique.

## Table des matières

## Comment fonctionne le DNS Scavenging

Le processus repose sur deux intervalles configurables :

- **No-Refresh Interval** : période pendant laquelle les mises à jour d'un enregistrement ne sont pas acceptées (évite la charge serveur)
- **Refresh Interval** : période pendant laquelle l'enregistrement doit se signaler avant d'être marqué comme obsolète

Une fois les deux périodes écoulées sans activité, l'enregistrement devient éligible au scavenging et peut être supprimé automatiquement.

**En clair** : si un enregistrement n'a pas donné signe de vie pendant `No-Refresh + Refresh`, il dégage.

Le scavenging ne touche **jamais** les enregistrements statiques. Uniquement les enregistrements dynamiques créés par DHCP ou ddns.

## Configurer le DNS Scavenging sur Windows Server

### Prérequis

> ⚠️ **Avant de commencer** : Assure-toi que tes serveurs DHCP et DNS sont synchronisés. Sinon, tu risques de supprimer des enregistrements d'hôtes encore actifs. Sauvegarde ta zone avant d'activer.

Compatible Windows Server 2016, 2019, 2022 et 2025.

### Configuration via PowerShell (recommandé)

```powershell
# 1. Activer le scavenging sur le serveur DNS
Set-DnsServerScavenging -ScavengingState $true -ScavengingInterval 1.00:00:00

# 2. Définir les intervalles sur la zone (en jours)
Set-DnsServerZoneAging -Name "tondomaine.local" `
    -Aging $true `
    -NoRefreshInterval 7.00:00:00 `
    -RefreshInterval 7.00:00:00

# 3. Vérifier la configuration appliquée
Get-DnsServerZoneAging -Name "tondomaine.local"

# 4. Lancer manuellement le premier nettoyage
Start-DnsServerScavenging
```

Pour activer sur toutes les zones d'un coup :

```powershell
Get-DnsServerZone | Where-Object { $_.ZoneType -eq "Primary" } | ForEach-Object {
    Set-DnsServerZoneAging -Name $_.ZoneName -Aging $true `
        -NoRefreshInterval 7.00:00:00 -RefreshInterval 7.00:00:00
}
```

### Configuration via l'interface graphique

1. Ouvre **Gestionnaire DNS** (`dnsmgmt.msc`)
2. Clic droit sur le serveur → **Propriétés** → onglet **Avancé**
3. Coche **Activer le nettoyage automatique des enregistrements obsolètes**
4. Définis l'intervalle de nettoyage (1 jour recommandé)
5. Pour activer sur une zone : clic droit sur la zone → **Propriétés** → onglet **Vieillissement**
6. Coche **Supprimer les enregistrements de ressource obsolètes** et configure les intervalles

### Configuration par zone DNS

Si tu as plusieurs zones avec des besoins différents, gère-les indépendamment :

```powershell
# Zone interne standard
Set-DnsServerZoneAging -Name "corp.local" -Aging $true `
    -NoRefreshInterval 7.00:00:00 -RefreshInterval 7.00:00:00

# Zone DMZ avec intervalles plus courts
Set-DnsServerZoneAging -Name "dmz.local" -Aging $true `
    -NoRefreshInterval 3.00:00:00 -RefreshInterval 3.00:00:00

# Vérifier toutes les zones
Get-DnsServerZone | ForEach-Object {
    Get-DnsServerZoneAging -Name $_.ZoneName
}
```

## Configuration avancée

Pour les environnements avec plusieurs contrôleurs de domaine, maîtrise [la gestion des rôles FSMO](https://brandonvisca.com/activedirectory-transfere-des-roles-fsmo/) avant de déployer le scavenging. Un seul DC effectue réellement le scavenging par zone via la réplication AD.

### Synchronisation avec DHCP

La règle d'or : **durée de bail DHCP > No-Refresh + Refresh**.

```powershell
# Exemple : bail DHCP 8 jours, intervalles DNS 7+7 = 14 jours
# Le bail est renouvelé avant que le DNS ne considère l'enregistrement obsolète

# Configuration cohérente
Set-DnsServerZoneAging -Name "tondomaine.local" `
    -NoRefreshInterval 7.00:00:00 `
    -RefreshInterval 7.00:00:00

# Vérifier la durée de bail DHCP sur le scope
Get-DhcpServerv4Scope | Select-Object ScopeId, LeaseDuration
```

Si ton bail DHCP est à 8 jours et tes intervalles DNS à 7+7 (14 jours), t'es safe : le client renouvelle son bail et met à jour son enregistrement DNS bien avant les 14 jours.

### Surveillance et logs

Active les logs détaillés pour tracer les suppressions :

```powershell
# Activer la journalisation DNS détaillée
Set-DnsServerDiagnostics -SaveLogsToPersistentStorage $true `
    -EnableLogFileRollover $true `
    -MaxMBFileSize 500

# Voir les enregistrements éligibles au scavenging
Get-DnsServerResourceRecord -ZoneName "tondomaine.local" | `
    Where-Object { $_.TimeStamp -lt (Get-Date).AddDays(-14) } | `
    Select-Object HostName, RecordType, TimeStamp

# Vérifier l'état global du scavenging
Get-DnsServerScavenging
```

## Pièges à éviter

### Activer sans tester d'abord

**Le piège** : activer le scavenging sur toutes les zones en production d'un coup.

**Fix** : teste sur une zone de dev ou non-critique pendant 2 semaines. Vérifie qu'aucun enregistrement critique n'a disparu avant de déployer partout.

### Intervalles trop courts vs baux DHCP

**Le piège** : `No-Refresh + Refresh` inférieur à la durée de bail DHCP.

**Fix** : `durée bail DHCP ≤ No-Refresh + Refresh`. Si ton bail est à 3 jours et tes intervalles à 2+2, tu vas supprimer des enregistrements d'hôtes encore actifs.

### Pas de sauvegarde avant activation

**Le piège** : « ça va bien se passer ».

**Fix** : exporte ta zone avant d'activer le scavenging.

```powershell
# Export de la zone DNS
dnscmd /zoneexport tondomaine.local C:\Backup\tondomaine_backup.txt

# Ou via PowerShell (export en fichier zone)
Export-DnsServerZone -Name "tondomaine.local" -FileName "tondomaine_backup.dns"
```

## Surveillance et maintenance

### Vérification périodique

Lance ces commandes en tâche planifiée hebdomadaire pour garder un oeil sur l'état :

```powershell
# État du scavenging (dernière exécution, prochaine planifiée)
Get-DnsServerScavenging

# Voir les dernières suppressions (Event ID 1541)
Get-WinEvent -FilterHashtable @{
    LogName = 'DNS Server'
    Id = 1541
} -MaxEvents 50 | Select-Object TimeCreated, Message

# Statistiques de la zone
Get-DnsServerStatistics -ZoneName "tondomaine.local"
```

### Script de monitoring

À lancer en tâche planifiée pour alerter si trop d'enregistrements obsolètes s'accumulent :

```powershell
$ZoneName = "tondomaine.local"
$Threshold = 100
$Records = Get-DnsServerResourceRecord -ZoneName $ZoneName
$StaleRecords = $Records | Where-Object { $_.TimeStamp -lt (Get-Date).AddDays(-14) }

if ($StaleRecords.Count -gt $Threshold) {
    Write-EventLog -LogName "Application" `
        -Source "DNS Monitoring" `
        -EventId 1001 `
        -EntryType Warning `
        -Message "Enregistrements obsolètes détectés : $($StaleRecords.Count) dans $ZoneName"
    Write-Host "Alerte : $($StaleRecords.Count) enregistrements obsolètes dans $ZoneName"
}
```

## Bonnes pratiques

### Environnement standard

```powershell
# Configuration recommandée pour la majorité des environnements
Set-DnsServerScavenging -ScavengingState $true -ScavengingInterval 1.00:00:00
Set-DnsServerZoneAging -Name "tondomaine.local" `
    -Aging $true `
    -NoRefreshInterval 7.00:00:00 `
    -RefreshInterval 7.00:00:00
# → Total : 14 jours avant suppression, nettoyage quotidien
```

Bail DHCP recommandé : **8 jours minimum** avec cette config.

### Environnements critiques

Pour les infras avec des enregistrements sensibles (serveurs de prod, appliances réseau) :

- **No-Refresh** : 14 jours
- **Refresh** : 14 jours
- **Scavenging Interval** : 7 jours (hebdomadaire)
- Audit manuel mensuel des suppressions via les Event ID 1541
- Exclure explicitement les enregistrements critiques en les passant en statique

```powershell
# Convertir un enregistrement dynamique en statique (protégé du scavenging)
$Record = Get-DnsServerResourceRecord -ZoneName "tondomaine.local" -Name "serveur-critique"
$NewRecord = $Record.Clone()
$NewRecord.TimeToLive = [System.TimeSpan]::FromHours(1)
Set-DnsServerResourceRecord -ZoneName "tondomaine.local" `
    -OldInputObject $Record -NewInputObject $NewRecord
```

## Intégration avec l'écosystème Windows

Le DNS Scavenging interagit avec plusieurs composants de ton infra :

**Active Directory** : les enregistrements AD (SRV, A des DC) sont dynamiques mais critiques. Vérifie qu'ils se renouvellent correctement avant d'activer le scavenging. Un enregistrement DC supprimé par erreur casse l'authentification.

**DHCP** : configure le DHCP pour qu'il enregistre les clients en DNS dynamique (`Set-DhcpServerv4DnsSetting`). Sans ça, les baux DHCP ne mettent pas à jour les timestamps DNS et les enregistrements sont supprimés trop tôt.

**WSUS/SCCM** : les serveurs de gestion ont souvent des enregistrements statiques. Vérifie leur type avant activation.

Si ton infra intègre des machines Linux dans AD, consulte le [guide Ubuntu + Active Directory avec SSSD](https://brandonvisca.com/connecter-les-systemes-ubuntu-a-active-directory-en-utilisant-sssd/). Les machines Linux renouvellent leurs enregistrements DNS différemment des clients Windows : à vérifier avant d'activer le scavenging.

## Conclusion

Le DNS Scavenging Windows Server, c'est 10 minutes de config une fois, et des années sans te battre avec des enregistrements fantômes.

Active-le en PowerShell sur une zone de test cette semaine. Vérifie après 14 jours ce qui a été nettoyé. Si tout est bon, déploie sur le reste. La [documentation Microsoft](https://learn.microsoft.com/en-us/windows-server/networking/dns/deploy/dns-scavenging) couvre les cas edge si tu as une infra complexe. Et si tu gères tes serveurs à distance, [Termius](https://brandonvisca.com/termius-client-ssh-windows-guide-complet/) te donne un accès SSH propre depuis n'importe quel OS.

## FAQ DNS Scavenging Windows Server

**Le DNS Scavenging peut-il supprimer des enregistrements statiques ?**

Non. Le scavenging ne touche que les enregistrements dynamiques créés via DHCP ou ddns. Les enregistrements statiques sont intouchables, peu importe leur ancienneté.

**Quels intervalles recommander pour No-Refresh et Refresh ?**

7 jours chacun pour un environnement standard (14 jours total). Tes baux DHCP doivent dépasser ces 14 jours pour éviter de supprimer des enregistrements d'hôtes encore actifs.

**Faut-il redémarrer le service DNS après configuration ?**

Non. Les changements sont pris en compte sans redémarrage. Tu peux lancer `Start-DnsServerScavenging` immédiatement pour forcer un premier passage manuel.

**Peut-on activer le scavenging sur plusieurs serveurs DNS ?**

Oui, mais en pratique un seul serveur DNS par zone effectue réellement le scavenging (celui qui détient la zone principale). Sur un setup AD multi-DC, configure sur le PDC Emulator en priorité.

**Comment confirmer que le scavenging a bien supprimé des enregistrements ?**

Filtre les Event ID 1541 dans le journal DNS Server ou lance `Get-DnsServerScavenging` pour voir la date du dernier passage et le nombre d'enregistrements supprimés.

---

## Pour aller plus loin

- [Active Directory : transférer les rôles FSMO entre DC](https://brandonvisca.com/activedirectory-transfere-des-roles-fsmo/)
- [Ubuntu + Active Directory avec SSSD : guide complet](https://brandonvisca.com/connecter-les-systemes-ubuntu-a-active-directory-en-utilisant-sssd/)
- [Termius : client SSH moderne pour Windows et macOS](https://brandonvisca.com/termius-client-ssh-windows-guide-complet/)
