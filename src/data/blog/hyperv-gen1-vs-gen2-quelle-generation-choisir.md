---
title: "Hyper-V Gen1 vs Gen2 : laquelle choisir pour ta VM ? (2026)"
description: "Hyper-V Gen1 vs Gen2 : UEFI, Secure Boot, PXE, performances — le comparatif complet pour choisir la bonne génération selon ton OS et ton contexte."
pubDatetime: "2026-03-10T00:00:00+01:00"
author: Brandon Visca
tags:
  - hyper-v
  - windows-server
  - virtualisation
  - sysadmin
  - uefi
  - intermediaire
featured: false
draft: false
focusKeyword: hyper-v gen1 vs gen2
faqs:
  - question: "Peut-on convertir une VM Hyper-V Gen1 en Gen2 ?"
    answer: "Non, la génération est définie à la création et ne peut pas être changée. Pour migrer, il faut créer une nouvelle VM Gen2 et y transférer les données avec robocopy ou un outil de migration."
  - question: "Quels OS ne supportent pas Gen2 ?"
    answer: "Windows 32 bits, Windows Server 2003/2008 sans SP, et certains vieux Linux sans support UEFI ne fonctionnent qu'en Gen1. Pour tout OS moderne, Gen2 est le bon choix."
  - question: "Gen2 est-elle toujours plus rapide que Gen1 ?"
    answer: "Pour le démarrage et l'I/O disque, oui : Gen2 démarre 2-3x plus vite grâce à UEFI. Les performances CPU et réseau sont identiques entre les deux générations."
  - question: "Le Secure Boot Gen2 bloque-t-il les Linux ?"
    answer: "Par défaut oui, si ton Linux n'est pas signé par Microsoft. Solution : désactiver le Secure Boot dans les paramètres de la VM Gen2. Ubuntu et Debian sont signés et démarrent sans modification."
---
# Hyper-V Gen1 vs Gen2 : laquelle choisir pour ta VM ? (2026)

Gen1 ou Gen2 pour ta prochaine VM Hyper-V ? La question revient à chaque création de VM, et la réponse n'est pas toujours évidente — surtout quand on voit que certains OS ne supportent tout simplement pas Gen2.

Spoiler : dans 90% des cas, tu veux Gen2. Mais il y a des exceptions qui méritent qu'on s'y arrête.

Voici le comparatif complet, basé sur ce que j'utilise au quotidien en environnement de production.

---

## Table des matières

## TL;DR

| Critère | Gen1 (BIOS) | Gen2 (UEFI) | Gagnant |
|---|---|---|---|
| Firmware | BIOS legacy | UEFI natif | Gen2 |
| Démarrage | Plus lent | Plus rapide | Gen2 |
| Secure Boot | ❌ Non | ✅ Oui | Gen2 |
| PXE Boot | ✅ Legacy + UEFI | ✅ UEFI seulement | Égalité |
| Taille disque OS max | 2 To (MBR) | 64 To (GPT) | Gen2 |
| Compatibilité OS 32 bits | ✅ Oui | ❌ Non | Gen1 |
| Linux ancien (< RHEL 6) | ✅ Oui | ⚠️ Limité | Gen1 |
| Windows Server 2012+ | ✅ Oui | ✅ Oui | Égalité |
| Conversion possible | ❌ Non | ❌ Non | — |

**Mon choix par défaut : Gen2** pour tout OS moderne (Windows Server 2012+, Ubuntu 14.04+, Debian 8+).

---

## C'est quoi la différence concrète ?

La génération d'une VM Hyper-V, c'est le firmware émulé : **Gen1 simule un BIOS legacy**, **Gen2 émule un firmware UEFI**. C'est fixé à la création de la VM et **non modifiable après** — d'où l'importance de choisir correctement dès le départ.

Gen1 est là depuis Hyper-V 2012. Gen2 est arrivé avec Hyper-V 2012 R2. Les deux coexistent parce que le parc de VMs existantes est souvent mixte.

> ⚠️ **Attention** : impossible de convertir une VM Gen1 en Gen2 (et vice-versa) sans recréer la VM. Si tu choisis mal, tu recommences.

---

## Hyper-V Gen1 : test complet

### ✅ Points forts

- **Compatibilité maximale** : supporte tous les OS y compris les 32 bits, les vieux Linux, FreeBSD, et les OS exotiques
- **PXE boot legacy** : indispensable dans certains environnements de déploiement qui n'ont pas encore migré en UEFI
- **Stabilité éprouvée** : des années de production sans surprise
- **Idéal pour migrations** : si tu P2V une vieille machine physique avec BIOS, rester en Gen1 évite les frictions

### ✗ Points faibles

- **Démarrage plus lent** : le POST BIOS émulé rajoute quelques secondes inutiles
- **Pas de Secure Boot** : pas de protection contre les bootkits
- **Limité à 2 To pour le disque OS** (MBR) — un vrai problème sur des VMs très chargées
- **Pas de démarrage réseau HTTPS** : le PXE legacy ne supporte pas les déploiements sécurisés modernes
- **Contrôleurs IDE émulés** : les disques IDE sont plus lents que SCSI virtuel

### 💰 Coût réel

Aucun coût direct, mais le coût caché c'est le temps : si ton WSUS ou ton système de déploiement évolue vers du full-UEFI, tes VMs Gen1 devront être recréées.

### 🎯 Cas d'usage idéal

- OS 32 bits (Windows Server 2003, vieux Linux)
- Déploiement PXE dans un environnement legacy
- Migration P2V depuis une machine BIOS
- FreeBSD, Solaris, OS non-mainstream

---

## Hyper-V Gen2 : test complet

### ✅ Points forts

- **Démarrage UEFI natif** : plus rapide, sans le POST BIOS inutile
- **Secure Boot** : protection contre les bootkits et les rootkits au démarrage — important en production
- **Disques SCSI virtuel uniquement** : meilleures performances I/O, plus simple à gérer
- **Taille disque OS jusqu'à 64 To** (GPT) : plus de limite MBR
- **Démarrage réseau HTTPS** : compatible avec les déploiements WDS/MDT modernes
- **TPM virtuel (vTPM)** : obligatoire pour Windows 11 et certaines fonctionnalités BitLocker
- **Shielded VMs** : si tu utilises Guarded Host, Gen2 est obligatoire

### ✗ Points faibles

- **Pas de support 32 bits** : si ton OS n'est pas 64 bits, c'est mort
- **Certains Linux anciens galèrent** : RHEL/CentOS 6 et antérieurs, Debian 7 et antérieurs nécessitent des ajustements
- **PXE limité au mode UEFI** : si ton infra de déploiement est full-legacy, problème
- **Secure Boot parfois contraignant** : certains drivers ou bootloaders non signés bloquent au démarrage

### 💰 Coût réel

Zéro coût supplémentaire. Gen2 est disponible sur le même Hyper-V que Gen1.

Le seul "coût" : s'assurer que ton OS est compatible et que ton infrastructure de déploiement supporte UEFI PXE si tu en as besoin.

### 🎯 Cas d'usage idéal

- Windows Server 2012 R2 et versions ultérieures
- Windows 10/11 et versions ultérieures
- Ubuntu 14.04+, Debian 8+, RHEL/CentOS 7+
- Toute VM de production moderne
- Environnements avec Secure Boot obligatoire
- VMs nécessitant un vTPM (BitLocker, Windows 11)

---

## Le verdict : qui pour qui ?

### Choisis Gen2 si :
- Ton OS est Windows Server 2012 R2 ou plus récent
- Ton OS est un Linux 64 bits moderne (Ubuntu 14.04+, Debian 8+, RHEL 7+)
- Tu veux Secure Boot activé
- Tu as besoin d'un disque OS > 2 To
- Tu déploies Windows 11 (vTPM obligatoire)
- Tu pars de zéro sur une infra propre

### Choisis Gen1 si :
- Ton OS est 32 bits (pas d'autre choix)
- Tu fais du P2V depuis une machine BIOS et tu veux éviter les complications
- Ton OS est trop ancien pour Gen2 (Windows Server 2003, CentOS 5/6, Debian 7)
- Ton environnement PXE est en legacy uniquement
- Tu utilises FreeBSD ou un OS non-mainstream

> 🔍 **À savoir** : Microsoft recommande officiellement Gen2 pour tous les OS supportés. Gen1 existe pour la compatibilité descendante, pas pour les nouvelles VMs.

---

## Compatibilité OS par génération

| OS | Gen1 | Gen2 |
|---|---|---|
| Windows Server 2025 | ✅ | ✅ |
| Windows Server 2022 | ✅ | ✅ |
| Windows Server 2019 | ✅ | ✅ |
| Windows Server 2016 | ✅ | ✅ |
| Windows Server 2012 R2 | ✅ | ✅ |
| Windows Server 2012 | ✅ | ✅ |
| Windows Server 2008 R2 | ✅ | ❌ |
| Windows Server 2003 | ✅ | ❌ |
| Windows 11 | ✅ | ✅ |
| Windows 10 (64 bits) | ✅ | ✅ |
| Ubuntu 18.04+ | ✅ | ✅ |
| Ubuntu 14.04 - 16.04 | ✅ | ✅ |
| Debian 8+ | ✅ | ✅ |
| RHEL/CentOS 7+ | ✅ | ✅ |
| RHEL/CentOS 6 | ✅ | ⚠️ |
| FreeBSD | ✅ | ❌ |

> 💡 **Astuce** : Si tu as un doute sur la compatibilité Gen2 de ton Linux, démarre en Gen2 sans Secure Boot dans un premier temps. Tu pourras l'activer ensuite une fois l'OS installé et les drivers en place.

---

## Un point sur Secure Boot en Gen2

Secure Boot est activé par défaut sur les VMs Gen2 — et c'est bien. Mais il peut bloquer le démarrage si le bootloader ou le kernel n'est pas signé avec une clé reconnue.

Hyper-V propose 3 templates de Secure Boot selon l'OS :

```powershell
# Windows (défaut)
Set-VMFirmware -VMName "SRV-XXX" -SecureBootTemplate "MicrosoftWindows"

# Linux (Ubuntu, Debian, RHEL)
Set-VMFirmware -VMName "SRV-XXX" -SecureBootTemplate "MicrosoftUEFICertificateAuthority"

# Désactiver Secure Boot (dernier recours)
Set-VMFirmware -VMName "SRV-XXX" -EnableSecureBoot Off
```

> ⚠️ **Attention** : Sur une VM Linux Gen2, utilise toujours le template `MicrosoftUEFICertificateAuthority`. Le template Windows bloquera le démarrage de ton Linux.

---

## FAQ

**Peut-on convertir une VM Gen1 en Gen2 ?**
Non. La génération est figée à la création. Pour passer de Gen1 à Gen2, il faut créer une nouvelle VM Gen2 et migrer le contenu — exactement comme la procédure de [restauration VHDX via WinPE](https://brandonvisca.com/restaurer-vm-hyperv-vhdx-corrompu-winpe/).

**Gen2 est-elle plus performante que Gen1 ?**
Légèrement, surtout au démarrage. En production, la différence de performances I/O est négligeable sur les workloads courants. L'avantage de Gen2 est surtout fonctionnel (Secure Boot, vTPM, disques SCSI) plutôt que purement en termes de vitesse.

**Secure Boot peut-il être activé sur Gen1 ?**
Non. Secure Boot est une fonctionnalité UEFI uniquement, donc réservée aux VMs Gen2.

**Est-ce qu'une VM Gen2 est compatible avec tous les hyperviseurs ?**
Non. Le format VHDX Gen2 est spécifique à Hyper-V. Si tu migres vers VMware ou Proxmox, l'aspect "génération" ne s'applique plus — tu travailleras avec les formats UEFI/BIOS natifs de la plateforme cible.

**Quelle génération pour Windows 11 ?**
Obligatoirement Gen2. Windows 11 nécessite TPM 2.0, et seul le vTPM disponible en Gen2 répond à cette exigence sous Hyper-V.

**Gen1 sera-t-elle dépréciée un jour ?**
Aucune annonce officielle de Microsoft, mais la tendance est clairement vers Gen2. Tous les nouveaux OS et fonctionnalités (vTPM, Shielded VMs) sont Gen2 uniquement. Partir sur du neuf en Gen1 aujourd'hui, c'est s'assurer du travail de migration dans quelques années.

---

## 🎬 Conclusion

**Gen2 est le choix par défaut** pour toute VM tournant sur un OS moderne. Plus rapide au boot, Secure Boot intégré, disques SCSI plus performants et support du vTPM : il n'y a aucune raison de rester sur Gen1 si ton OS le supporte.

Gen1 reste pertinente pour deux cas précis : les OS anciens (32 bits, Windows 2003, vieux Linux) et les migrations P2V depuis des machines BIOS où tu veux minimiser les frictions.

Si tu crées une nouvelle VM aujourd'hui pour Windows Server 2019/2022/2025 ou un Linux récent : **Gen2, sans hésitation**.

Et si tu te retrouves avec une VM Gen2 corrompue, j'ai détaillé [la procédure complète de restauration VHDX via WinPE](https://brandonvisca.com/restaurer-vm-hyperv-vhdx-corrompu-winpe/) — ça peut toujours servir.

---
