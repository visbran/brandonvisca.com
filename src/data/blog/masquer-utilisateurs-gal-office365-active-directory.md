---
title: "Masquer des utilisateurs de la GAL Office 365 + Active Directory : Guide complet"
description: Masquez des utilisateurs de la GAL Office 365 synchronisés depuis Active Directory sans les supprimer. Méthode PowerShell et console Exchange Admin Centre.
pubDatetime: "2025-08-01T21:17:07+02:00"
author: Brandon Visca
tags:
  - microsoft-365
  - sysadmin
  - avance
  - active-directory
  - powershell
  - guide
featured: false
draft: false
focusKeyword: masquer utilisateurs GAL Office 365
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
> 💡 **TL;DR**
> - Masquer des utilisateurs de la GAL Office 365 synchronisés depuis Active Directory local
> - Sans étendre le schéma AD (l'attribut `msExchHideFromAddressLists` manque en hybride)
> - Solution testée avec Azure AD Connect

- - - - - -

## Table des matières

Ah, la fameuse Liste d’Adresses Globale (GAL) d’Office 365… Tu sais, cette liste interminable où tous les utilisateurs de ton organisation s’affichent fièrement, même ceux que tu préférerais planquer dans un placard virtuel ?

Si tu gères un environnement hybride avec Active Directory local et Office 365, tu as sûrement déjà pesté contre l’absence de l’attribut `msExchHideFromAddressLists` dans ton AD. Heureusement, il existe une solution élégante qui évite de foutre en l’air ton schéma Active Directory.

**Spoiler** : On va bidouiller Azure AD Connect avec style, sans tout casser.
- - - - - -- - - - - -
## Le problème qui fait mal aux cheveux

Dans un monde parfait, masquer un utilisateur de la GAL c’est simple comme bonjour quand tu as un compte cloud :

```powershell
# La méthode de feignant pour les comptes cloud
Set-Mailbox -Identity user@domain.com -HiddenFromAddressListsEnabled $true

```

**Mais alors**, que faire quand tes utilisateurs viennent d’un Active Directory local via Azure AD Connect ?

![giphy](https://media0.giphy.com/media/tfVJZMEbl93awAR0V4/giphy.gif)

Tu te retrouves avec une erreur qui te dit poliment d’aller voir ailleurs si tu y es, parce que l’attribut `msExchHideFromAddressLists` n’existe pas dans ton schéma AD.

### 💡 À savoir

Le problème vient du fait qu’Azure AD Connect synchronise les attributs depuis ton AD local vers Azure AD. Si l’attribut n’existe pas côté local, pas de miracle côté cloud.
- - - - - -
Ce type de manipulation suppose un Active Directory sain. Si le tien traîne des rôles mal répartis, commencer par [le transfert des rôles FSMO](/activedirectory-transfere-des-roles-fsmo/).

- - - - - -

## Pourquoi pas d’extension de schéma ?

Tu pourrais être tenté d’étendre ton schéma Active Directory pour Exchange. Techniquement, c’est faisable. **Pratiquement**, c’est comme utiliser un lance-flammes pour allumer une bougie :

- ✅ Ça marche
- ❌ C’est overkill
- ❌ Ça ajoute une tonne d’attributs que tu n’utiliseras jamais
- ❌ C’est irréversible
- ❌ Ça peut foutre la zone dans ton AD

Bref, on va éviter.
- - - - - -
## La solution : msDS-cloudExtensionAttribute

Les `msDS-cloudExtensionAttribute` sont apparues avec Windows Server 2012, et c’est exactement ce qu’il nous faut. Ces attributs offrent 20 slots (de 1 à 20) pour ce genre de bidouilles.

**Pourquoi pas `showInAddressBook` ?** Parce que cet attribut cherche le format DN (Distinguished Name) d’un objet, et c’est pas du tout ce qu’on veut ici.

### 🚨 Erreur fréquente

Ne confonds pas `msDS-cloudExtensionAttributeX` avec les `extensionAttributeX` classiques. Les premiers sont spécialement conçus pour la synchronisation cloud.
- - - - - -
## Étape 1 : Configuration d’Azure AD Connect

Première étape : dire à Azure AD Connect qu’il doit s’occuper de notre nouvel attribut.

**Ouvre le Service de Synchronisation Azure AD Connect** sur ton serveur.

1. Navigue vers l’onglet **Connecteurs**
2. Sélectionne ton **Active Directory** (pas celui en `.onmicrosoft.com`)
3. Clique sur **Propriétés**
4. En haut à droite, clique sur **Show All**
5. Scroll down et trouve **msDS-CloudExtensionAttribute1**
6. Coche la case et valide

```
💡 Tu peux utiliser n'importe quel numéro de 1 à 20,
   assure-toi juste de pas utiliser un slot déjà occupé.

```

**Redémarre le service de synchronisation** après cette modif.
- - - - - -
## Étape 2 : Règle de synchronisation personnalisée

Maintenant, on va créer une règle qui dit à Azure AD Connect : *« Si tu vois `HideFromGAL` dans `msDS-CloudExtensionAttribute1`, alors tu mets `msExchHideFromAddressLists` à `True`. »*

**Ouvre l’Éditeur de règles de synchronisation Azure AD Connect**

Clique sur **Ajouter une nouvelle règle** (assure-toi que la direction est **Inbound**)

### Configuration de la règle :

| Champ | Valeur |
| --- | --- |
| **Nom** | `HideFromGAL` |
| **Description** | `Si msDS-CloudExtensionAttribute1 = HideFromGAL, masquer de la GAL` |
| **Système connecté** | `Ton domaine Active Directory` |
| **Type d’objet du système connecté** | `utilisateur` |
| **Type d’objet Metaverse** | `personne` |
| **Type de lien** | `Join` |
| **Précédence** | `50` |

### Transformation :

- **Type de flux** : `Expression`
- **Attribut cible** : `msExchHideFromAddressLists`
- **Source** :

```
IIF(IsPresent([msDS-cloudExtensionAttribute1]),IIF([msDS-cloudExtensionAttribute1]="HideFromGAL",True,False),NULL)

```

### 🔍 Explication de la formule

Cette expression dit : « Si l’attribut `msDS-cloudExtensionAttribute1` est présent ET égal à `HideFromGAL`, alors retourne `True`, sinon `False`. S’il n’est pas présent, retourne `NULL`. »
- - - - - -
## Étape 3 : Synchronisation initiale

Maintenant qu’on a tout configuré, on lance la synchronisation pour appliquer notre nouvelle règle.

**Ouvre PowerShell en tant qu’administrateur** sur ton serveur Azure AD Connect :

```powershell
Start-ADSyncSyncCycle -PolicyType Initial

```

Cette commande va prendre un moment. Va te faire un café, ça va être long.

### ⚠️ Point d’attention

La synchronisation initiale peut prendre plusieurs heures selon la taille de ton AD. C’est normal, respire.
- - - - - -
## Étape 4 : Masquer un utilisateur depuis AD

Maintenant, le moment de vérité : masquer un utilisateur.

**Ouvre Active Directory Users and Computers**

1. Trouve l’utilisateur à masquer
2. Clic droit → **Propriétés**
3. Va dans l’onglet **Éditeur d’attributs**
4. Trouve `msDS-cloudExtensionAttribute1`
5. Entre la valeur **`HideFromGAL`** (attention à la casse !)
6. Valide

### 🚨 Tu ne vois pas l’onglet Éditeur d’attributs ?

Dans ADUC, va dans **View** → **Advanced Features** pour activer l’affichage avancé.
- - - - - -
Une synchronisation d’annuaire fiable suppose des horloges alignées : voir [synchroniser le temps sur un domaine Active Directory](/ntp-active-directory-synchroniser-domaines/).

- - - - - -

## Étape 5 : Validation et vérification

**Retourne dans le Service de Synchronisation Azure AD Connect**

1. Va dans l’onglet **Opérations**
2. Lance une synchronisation Delta si elle ne s’est pas déclenchée automatiquement
3. Vérifie l’export vers ton connecteur `domain.onmicrosoft.com`
4. Tu devrais voir 1 mise à jour
5. Clique sur l’utilisateur modifié → **Propriétés**
6. Vérifie que `msExchHideFromAddressLists` est bien défini sur `true`

**Test final** : Connecte-toi à Outlook ou OWA et vérifie que l’utilisateur n’apparaît plus dans la GAL.
- - - - - -
Côté postes Linux du parc, l’intégration à ce même annuaire passe par [SSSD sur Ubuntu](/connecter-les-systemes-ubuntu-a-active-directory-en-utilisant-sssd/).

- - - - - -

## Bonus : Automatisation PowerShell

Si tu as plusieurs utilisateurs à masquer, voici un script pour automatiser le processus :

```powershell
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

```

### 🔧 Pour lancer une sync Delta à distance :

```powershell
# Depuis un autre serveur (remplace SERVEUR-AZUREAD par ton serveur AD Connect)
Invoke-Command -ComputerName "SERVEUR-AZUREAD" -ScriptBlock {
    Start-ADSyncSyncCycle -PolicyType Delta
}

```
- - - - - -
## FAQ : Les galères classiques

### Ma règle de synchronisation ne fonctionne pas !

Vérifie que :
Le service Azure AD Connect Sync est redémarré
Ta règle a bien une précédence unique (pas de conflit)
L’utilisateur existe bien dans ton AD local
Tu as bien lancé une synchronisation après avoir créé la règle

### L’utilisateur apparaît toujours dans la GAL

Patience, jeune padawan. Il peut y avoir jusqu’à 2h de délai pour que les changements se propagent dans Exchange Online. Si ça persiste :
Vérifie dans le centre d’administration Exchange Online
Force une synchronisation complète : `Start-ADSyncSyncCycle -PolicyType Initial`

### Je peux utiliser un autre attribut que msDS-cloudExtensionAttribute1 ?

Absolument ! Tu as 20 slots disponibles (`msDS-cloudExtensionAttribute1` à `msDS-cloudExtensionAttribute20`). Choisis un slot libre et adapte ta règle de synchronisation.

### Ça marche avec les groupes aussi ?

Théoriquement oui, mais les groupes de distribution ont leurs propres attributs. Pour un groupe, utilise plutôt :
Set-DistributionGroup -Identity « groupe@domain.com » -HiddenFromAddressListsEnabled $true
- - - - - -
## Pour aller plus loin

Cette technique t’ouvre plein de possibilités pour personnaliser la synchronisation Azure AD Connect. Tu peux maintenant :

- **Automatiser la gestion des licences** en fonction d’attributs personnalisés
- **Contrôler l’affichage des utilisateurs** dans différents annuaires
- **Créer des règles métier** complexes pour la synchronisation

### Articles connexes qui peuvent t’intéresser :

- **[Connecter Ubuntu à Active Directory avec SSSD](https://brandonvisca.com/connecter-les-systemes-ubuntu-a-active-directory-en-utilisant-sssd/)** : Pour intégrer tes serveurs Linux à ton domaine AD
- **[Transférer les rôles FSMO Active Directory](https://brandonvisca.com/activedirectory-transfere-des-roles-fsmo/)** : Indispensable quand tu gères plusieurs contrôleurs de domaine

### 🎯 Prochaine étape

Maintenant que tu maîtrises la GAL, l’étape suivante consiste à automatiser la gestion des groupes de distribution en PowerShell, puis à câbler le tout sur ta procédure de départ : un script qui masque le compte, coupe les accès et archive la boîte, en une passe.
- - - - - -
**Et voilà !** Tu as maintenant une solution propre, réversible et qui ne va pas foutre en l’air ton Active Directory. Cette méthode résistera aux mises à jour d’Azure AD Connect, contrairement à certaines bidouilles qu’on peut trouver sur des forums douteux.
