---
title: "NTP Active Directory : synchroniser tes domaines Windows"
description: "Guide ntp active directory : synchronise tes domaines Windows avec NTP, w32time, config PDC Emulator, GPO temps et dépannage Kerberos."
pubDatetime: "2026-07-02T08:00:00.000Z"
modDatetime: "2026-07-04T14:00:00.000Z"
author: Brandon Visca
tags:
  - windows
  - intermediaire
  - reseau
  - active-directory
  - ntp
featured: false
draft: false
focusKeyword: ntp active directory
---
> 💡 **TL;DR**
> - Active Directory dépend d'un temps synchrone : Kerberos plante si le décalage dépasse 5 minutes
> - Le PDC Emulator est la source NTP de référence pour toute la forêt
> - Tu configures w32time sur le DC, tu vérifies avec `w32tm /monitor`, et tu laisses NT5DS gérer les clients
> - Pour tes machines Linux jointes au domaine, pointe Chrony vers ton DC pour éviter les décalages Kerberos

## Table des matières

## Pourquoi le temps est critique dans Active Directory

Dans une forêt Windows, le temps n'est pas une préférence. C'est un protocole de sécurité. Kerberos, qui gère l'authentification entre utilisateurs, postes et contrôleurs de domaine, tolère un écart maximum de 5 minutes entre deux machines. Au-delà, les tickets sont rejetés. Les utilisateurs ne peuvent plus ouvrir de session, les partages réseau deviennent inaccessibles, et la réplication entre DCs échoue silencieusement.

Sans NTP fiable, tu te retrouves avec des logs horodatés à des heures différentes sur chaque serveur. Quand tu dois tracer une intrusion ou debugger une réplication, c'est l'enfer. Le problème ne se voit pas immédiatement, mais quand il éclate, il paralyse tout.

Active Directory repose donc sur une hiérarchie de temps stricte pour la synchro NTP active directory. Chaque poste et serveur membre doit suivre son DC. Chaque DC doit suivre le PDC Emulator du domaine racine. Et ce PDC Emulator doit pointer vers une source de temps externe fiable. Si un maillon lâche, toute la chaîne dérive.

## L'architecture NTP dans une forêt AD

La synchro temps dans AD ne fonctionne pas en mode peer-to-peer. Elle est hiérarchique et imposée par le domaine.

Les clients Windows et les serveurs membres se synchronisent automatiquement avec leur contrôleur de domaine le plus proche via le service Windows Time (`w32time`). Ce mécanisme interne s'appelle `NT5DS`. Les DCs eux-mêmes remontent au PDC Emulator de leur domaine. Enfin, le PDC Emulator du domaine racine de la forêt remonte vers une source NTP externe. C'est le seul endroit où tu configures un serveur NTP public.

Si tu as plusieurs domaines enfants, le PDC de chaque enfant remonte au PDC du domaine parent, jusqu'à la racine. C'est propre, prévisible, et ça évite que chaque DC aille chercher son temps n'importe où sur Internet.

Dans ce contexte, [configurer un serveur NTP dédié avec Chrony](/chrony-docker-serveur-ntp-homelab/) fait sens pour tes machines Linux et tes équipements réseau. Mais pour la partie Windows, tu laisses `w32time` gérer la hiérarchie AD. Le serveur Chrony devient juste la source externe du PDC Emulator si tu n'utilises pas les pools NTP publics directement.

## Identifier ton PDC Emulator

Avant de configurer quoi que ce soit, trouve le DC qui détient le rôle PDC Emulator. C'est lui le maître de l'horloge pour tout le domaine.

Dans une invite de commandes admin sur n'importe quel contrôleur de domaine :

```powershell
netdom query fsmo
```

Le résultat liste les cinq rôles FSMO. Note le nom du serveur pour la ligne `PDC`. C'est sur cette machine que tu vas configurer la source NTP externe. Si tu ne sais pas encore comment gérer ces rôles, j'ai un guide sur le [transfert des rôles FSMO](/activedirectory-transfere-des-roles-fsmo/) qui explique la procédure pas à pas.

## Configurer NTP Active Directory sur le PDC Emulator

Par défaut, Windows Server synchronise avec `time.windows.com`. Ce n'est pas idéal : la latence est variable et la fiabilité n'est pas garantie. Tu veux pointer vers des pools NTP publics robustes.

### 1. Arrêter le service w32time

```powershell
Stop-Service w32time
```

### 2. Configurer les serveurs NTP sources

```powershell
w32tm /config /manualpeerlist:"0.pool.ntp.org 1.pool.ntp.org 2.pool.ntp.org" /syncfromflags:manual /reliable:yes /update
```

`manualpeerlist` définit les sources externes. `/reliable:yes` marque ce serveur comme source de temps fiable pour les clients qui lui remontent. C'est indispensable pour que les DCs enfants et les postes acceptent sa synchro.

### 3. Redémarrer et resynchroniser

```powershell
Start-Service w32time
w32tm /resync /force
```

Si tu préfères utiliser des serveurs régionaux, remplace `pool.ntp.org` par `fr.pool.ntp.org` ou `europe.pool.ntp.org`. L'important est d'en indiquer au moins trois pour avoir de la redondance.

### 4. Vérifier que le PDC est bien configuré comme serveur NTP

```powershell
w32tm /query /configuration | findstr "Type"
```

Tu dois voir `Type: NTP` (ou `NT5DS` sur les DCs non-PDC). Sur le PDC, `NTP` indique qu'il utilise une source externe.

## Vérifier la synchronisation sur les contrôleurs de domaine

Une fois la config appliquée, contrôle que la synchro est active et que les décalages restent raisonnables.

### Statut local

```powershell
w32tm /query /status
```

Regarde les lignes suivantes :
- `Source` : l'IP ou le nom du serveur NTP externe
- `Last Successful Sync Time` : date et heure de la dernière synchro réussie
- `Stratum` : doit être faible (1 à 4 idéalement), pas 16 qui indique une erreur

### Monitoring de la forêt

```powershell
w32tm /monitor
```

Cette commande interroge tous les DCs du domaine et affiche leur décalage par rapport au PDC Emulator. Si tu vois des écarts supérieurs à quelques secondes, creuse. Un DC avec un offset de plusieurs minutes est symptomatique d'un problème réseau ou d'une config w32time corrompue.

## Propager la synchro aux postes clients

Les machines membres du domaine Windows gèrent leur temps tout seules via le mécanisme NT5DS. Elles se synchronisent avec leur DC au démarrage, puis régulièrement en arrière-plan. Tu n'as normalement rien à faire sur les postes.

Cependant, si tu as des sites distants, des VPNs instables, ou si tu veux forcer un comportement spécifique, tu peux utiliser une GPO.

### GPO : configurer le client Windows Time

1. Ouvre le Group Policy Management Console (`gpmc.msc`)
2. Crée ou édite une GPO liée à ton OU de postes
3. Navigue vers `Computer Configuration > Policies > Administrative Templates > System > Windows Time Service > Time Providers`
4. Active `Configure Windows NTP Client`
5. Définis :
   - `Type` : `NT5DS` (pour les membres du domaine, c'est le défaut et le plus sûr)
   - `NtpServer` : vide ou le nom de ton DC si tu veux forcer
   - `SpecialPollInterval` : 3600 secondes (1 heure)

NT5DS force le poste à respecter la hiérarchie AD. Ne remplace pas ça par `NTP` sur un client membre du domaine, sinon il ignore son DC et va chercher son temps n'importe où.

Pour forcer un poste à resynchroniser immédiatement :

```powershell
w32tm /resync
```

En cas de décalage important, ajoute `/force` pour forcer la correction même si l'écart est brutal.

## Synchroniser tes machines Linux avec Active Directory

Si tu as des serveurs Ubuntu ou Debian joints au domaine via SSSD, ils doivent aussi rester alignés avec le temps AD. Un décalage de plus de 5 minutes bloque l'authentification Kerberos, exactement comme sur Windows.

La méthode la plus simple : pointer Chrony vers ton PDC Emulator ou un DC local. J'explique le déploiement dans mon guide [Chrony Docker : serveur NTP précis pour ton homelab](/chrony-docker-serveur-ntp-homelab/), mais côté client, la config est minimale.

Dans `/etc/chrony/chrony.conf` ou le `docker-compose.yml` de ton conteneur Chrony client :

```text
server 192.168.1.10 iburst
```

Remplace `192.168.1.10` par l'IP de ton PDC Emulator. Puis redémarre Chrony :

```bash
sudo systemctl restart chronyd
sudo chronyc tracking
```

Si tu suis mon guide [Ubuntu Active Directory SSSD](/connecter-les-systemes-ubuntu-a-active-directory-en-utilisant-sssd/), cette étape est le complément obligatoire. Une machine Linux jointe au domaine sans synchro NTP alignée est une machine qui finira par ne plus pouvoir s'authentifier.

## Dépannage des erreurs courantes

### Kerberos échoue avec `KRB_AP_ERR_SKEW (37)`

C'est le classique. Le décalage horaire entre le client et le DC dépasse la tolérance Kerberos. Sur le poste concerné :

```powershell
w32tm /resync /force
```

Sur Linux :

```bash
sudo chronyc makestep
```

Si le problème revient régulièrement, vérifie que la source NTP du PDC Emulator est stable et que le service `w32time` est bien en automatique.

### `w32tm /query /status` indique Stratum 16

Stratum 16 signifie que le service n'a pas réussi à se synchroniser. Causes fréquentes :
- Le pare-feu Windows bloque le port UDP 123 sortant
- Le serveur NTP configuré dans `manualpeerlist` ne répond pas
- Le service n'a pas été redémarré après la config

Vérifie la connectivité NTP :

```powershell
w32tm /stripchart /computer:0.pool.ntp.org /samples:5 /dataonly
```

Si tu n'as aucune réponse, c'est un problème réseau ou de firewall.

### Le DC refuse de se synchroniser après migration

Après un transfert de rôle PDC ou une promotion de DC, `w32time` peut garder une ancienne config en cache. Réinitialise proprement :

```powershell
w32tm /config /update
w32tm /unregister
w32tm /register
Restart-Service w32time
w32tm /resync /force
```

### Les clients Windows affichent une heure incorrecte

Si les postes sont dans des fuseaux horaires différents, vérifie que le paramètre `Time Zone` est bien configuré via GPO (`Computer Configuration > Preferences > Control Panel Settings > Time Zone`). L'heure UTC synchronisée par NTP est identique partout, mais l'affichage local dépend du fuseau.

## Conclusion

La synchronisation temps dans Active Directory n'est pas un détail d'administration. C'est un pilier de la sécurité et de la cohérence du domaine. Un PDC Emulator mal configuré, une source NTP inaccessible, ou un client qui dérive silencieusement, et c'est tout l'écosystème Kerberos qui fragilise.

La règle est simple : le PDC Emulator pointe vers des sources NTP fiables, les DCs remontent au PDC, les clients remontent aux DCs, et tes machines Linux pointent vers le même référentiel. Tu vérifies avec `w32tm /monitor`, tu corriges au premier signe de dérive, et tu ne laisses jamais un décalage atteindre les 5 fatidiques minutes.
