---
title: "Masquer des utilisateurs de la GAL Office 365 + Active Directory : Guide complet"
pubDatetime: "2025-08-01T21:17:07+02:00"
author: Brandon Visca
description: "Masquez des utilisateurs de la GAL Office 365 synchronisés depuis Active Directory sans les supprimer. Méthode PowerShell et console Exchange Admin Centre."
tags:
  - microsoft-365
  - sysadmin
  - avance
  - active-directory
  - powershell
  - guide
faqs:
  - question: "Ma règle de synchronisation ne fonctionne pas !"
    answer: "Vérifie que l'attribut msDS-cloudExtensionAttribute1 est bien configuré dans SSSD et que la formule IIF est correcte."
  - question: "L'utilisateur apparaît toujours dans la GAL"
    answer: "Attends que la synchro Delta soit complète (peut prendre plusieurs minutes). Teste aussi avec un autre utilisateur pour vérifier."
  - question: "Je peux utiliser un autre attribut que msDS-cloudExtensionAttribute1 ?"
    answer: "Oui, utilise msDS-cloudExtensionAttribute2 à 15, mais reste cohérent dans ta formule de synchronisation."
  - question: "Ça marche avec les groupes aussi ?"
    answer: "Oui, la même logique s'applique aux groupes Distribution avec l'attribut msExchHideFromAddressLists."
---

Ah, la fameuse Liste d’Adresses Globale (GAL) d’Office 365… Tu sais, cette liste interminable où tous les utilisateurs de ton organisation s’affichent fièrement, même ceux que tu préférerais planquer dans un placard virtuel ?

Si tu gères un environnement hybride avec Active Directory local et Office 365, tu as sûrement déjà pesté contre l’absence de l’attribut `msExchHideFromAddressLists` dans ton AD. Heureusement, il existe une solution élégante qui évite de foutre en l’air ton schéma Active Directory.

**Spoiler** : On va bidouiller Azure AD Connect avec style, sans tout casser.

- - - - - -


  - [💡 À savoir](#%F0%9F%92%A1-a-savoir)
- [Pourquoi pas d’extension de schéma ?](#pourquoi-pas-dextension-de-schema)
- [La solution : msDS-cloudExtensionAttribute](#la-solution-ms-ds-cloud-extension-attribute)
  - [🚨 Erreur fréquente](#%F0%9F%9A%A8-erreur-frequente)
- [Étape 1 : Configuration d’Azure AD Connect](#etape-1-configuration-d-azure-ad-connect)
- [Étape 2 : Règle de synchronisation personnalisée](#etape-2-regle-de-synchronisation-personnalisee)
  - [Configuration de la règle :](#configuration-de-la-regle)
  - [Transformation :](#transformation)
  - [🔍 Explication de la formule](#%F0%9F%94%8D-explication-de-la-formule)
- [Étape 3 : Synchronisation initiale](#etape-3-synchronisation-initiale)
  - [⚠️ Point d’attention](#%E2%9A%A0%EF%B8%8F-point-dattention)
- [Étape 4 : Masquer un utilisateur depuis AD](#etape-4-masquer-un-utilisateur-depuis-ad)
  - [🚨 Tu ne vois pas l’onglet Éditeur d’attributs ?](#%F0%9F%9A%A8-tu-ne-vois-pas-longlet-editeur-dattributs)
- [Étape 5 : Validation et vérification](#etape-5-validation-et-verification)
- [Bonus : Automatisation PowerShell](#bonus-automatisation-power-shell-bonus-automatisation)
  - [🔧 Pour lancer une sync Delta à distance :](#%F0%9F%94%A7-pour-lancer-une-sync-delta-a-distance)
- [FAQ : Les galères classiques](#faq-les-galeres-classiques)
  - [Ma règle de synchronisation ne fonctionne pas !](#faq-question-1760987652385)
  - [L’utilisateur apparaît toujours dans la GAL](#faq-question-1760987674274)
  - [Je peux utiliser un autre attribut que msDS-cloudExtensionAttribute1 ?](#faq-question-1760987690969)
  - [Ça marche avec les groupes aussi ?](#faq-question-1760987723847)
- [Pour aller plus loin](#pour-aller-plus-loin)
  - [Articles connexes qui peuvent t’intéresser :](#articles-connexes-qui-peuvent-tinteresser)
  - [🎯 Prochaine étape](#%F0%9F%8E%AF-prochaine-etape)


Le problème qui fait mal aux cheveux

Dans un monde parfait, masquer un utilisateur de la GAL c’est simple comme bonjour quand tu as un compte cloud :

```bash
# La méthode de feignant pour les comptes cloud
Set-Mailbox -Identity user@domain.com -HiddenFromAddressListsEnabled $true

```

IIF(IsPresent([msDS-cloudExtensionAttribute1]),IIF([msDS-cloudExtensionAttribute1]="HideFromGAL",True,False),NULL)


### 🔍 Explication de la formule

Cette expression dit : « Si l’attribut `msDS-cloudExtensionAttribute1` est présent ET égal à `HideFromGAL`, alors retourne `True`, sinon `False`. S’il n’est pas présent, retourne `NULL`. »

- - - - - -

Étape 3 : Synchronisation initiale 

Maintenant qu’on a tout configuré, on lance la synchronisation pour appliquer notre nouvelle règle.

**Ouvre PowerShell en tant qu’administrateur** sur ton serveur Azure AD Connect :

```bash
Start-ADSyncSyncCycle -PolicyType Initial

```

# Script pour masquer plusieurs utilisateurs de la GAL
# À exécuter sur un contrôleur de domaine

$UsersToHide = @(
    "user1@domain.com",
    "user2@domain.com",
    "serviceaccount@domain.com"
)

foreach ($User in $UsersToHide) {
    try {
        $ADUser = Get-ADUser -Filter "UserPrincipalName -eq '$User'" -Properties msDS-cloudExtensionAttribute1
        
        if ($ADUser) {
            Set-ADUser $ADUser -Replace @{'msDS-cloudExtensionAttribute1'='HideFromGAL'}
            Write-Host "✅ $User configuré pour être masqué de la GAL" -ForegroundColor Green
        } else {
            Write-Host "❌ Utilisateur $User introuvable" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "❌ Erreur avec $User : $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n🔄 N'oublie pas de lancer une synchronisation Delta !" -ForegroundColor Yellow


### 🔧 Pour lancer une sync Delta à distance :

```bash
# Depuis un autre serveur (remplace SERVEUR-AZUREAD par ton serveur AD Connect)
Invoke-Command -ComputerName "SERVEUR-AZUREAD" -ScriptBlock {
    Start-ADSyncSyncCycle -PolicyType Delta
}

```

## Articles connexes

- [Connecter les systèmes Ubuntu à Active Directory en utilisan](/connecter-les-systemes-ubuntu-a-active-directory-en-utilisant-sssd/)
- [Active Directory : Transfère des rôles FSMO](/activedirectory-transfere-des-roles-fsmo/)
