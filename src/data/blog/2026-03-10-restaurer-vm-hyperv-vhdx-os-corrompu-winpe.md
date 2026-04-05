---
title: "VM Hyper-V irrécupérable ? Restaure l'OS sans réinstaller (2026)"
pubDatetime: "2026-03-10T00:00:00+00:00"
description: "Export-VM qui échoue, sauvegardes VSS bloquées, DISM instable : ta VM Hyper-V est logiquement corrompue. Voici la procédure complète pour reconstruire u..."
tags:
  - hyper-v
  - windows-server
  - vhdx
  - winpe
  - sysadmin
  - récupération
draft: true
---

# VM Hyper-V irrécupérable ? Restaure l'OS sans réinstaller (2026)

T'as une VM Hyper-V qui démarre encore, mais `Export-VM` plante, les sauvegardes VSS refusent de partir et DISM te regarde avec des yeux vides. La VM tourne, mais elle est cassée de l'intérieur.

Bonne nouvelle : c'est récupérable. Sans réinstaller Windows Server. Sans perdre tes données.

La technique : créer un nouveau VHDX OS sain, y copier l'ancien OS en offline via WinPE, puis reconstruire le boot UEFI de zéro. Ça prend 45 minutes et une bonne tasse de café.

---

## 📋 Prérequis

- **VM arrêtée** (pas en veille, arrêtée proprement)
- **ISO Windows Server 2022** disponible sur l'hôte Hyper-V
- **Copie de sauvegarde** des VHDX existants (même si corrompus — au cas où)
- **Accès console Hyper-V** sur l'hôte
- VM en **Génération 2 (UEFI)** — cette procédure est spécifique Gen2

> ⚠️ **Attention** : La corruption est *logique*, pas physique. Le VHDX démarre, mais l'intégrité du système de fichiers Windows est compromise. Cette procédure ne convient pas si le disque physique sous-jacent est mort.

---

## 🧩 Ce qui se passe vraiment

Ton disque OS actuel a des structures Windows corrompues (registre, CBS, BCD...). Windows démarre par miracle, mais VSS ne peut pas prendre de snapshot propre, donc export et sauvegarde échouent.

Le plan d'attaque :

1. Créer un nouveau VHDX OS vierge (structure saine)
2. Démarrer sur l'ISO WinPE
3. Copier tout l'ancien OS vers le nouveau disque en mode offline
4. Reconstruire le boot UEFI sur le nouveau disque
5. Redémarrer et valider

Le disque DATA n'est pas touché. Il reste connecté pendant toute l'opération.

---

## 1️⃣ Créer le nouveau disque OS (sur l'hôte Hyper-V)

```powershell
New-VHD -Path "F:\Hyper-V\Disks\SRV-XXX_OS_NEW.vhdx" -SizeBytes 80GB -Dynamic
```

> 💡 **Astuce** : Utilise `_OS_NEW` dans le nom pour te souvenir que c'est le nouveau. Tu le renommeras à la fin une fois que tout fonctionne.

---

## 2️⃣ Reconfigurer la VM

- **Déconnecter** l'ancien disque OS (ne pas supprimer)
- **Connecter** le nouveau VHDX vierge
- **Laisser** le disque DATA connecté
- **Monter l'ISO Windows Server 2022** dans le lecteur DVD

**Ordre de boot firmware (CRITIQUE pour Gen2) :**
1. DVD (ISO Windows)
2. Disque dur

> ⚠️ **Attention** : Secure Boot doit rester sur **"Microsoft Windows"** pour une VM Gen2 Windows Server.

---

## 3️⃣ Démarrer en WinPE

Lance la VM et connecte-toi via la console Hyper-V. Sur l'écran d'installation Windows Server :

```
Réparer l'ordinateur → Dépannage → Options avancées → Invite de commandes
```

Tu es maintenant dans **WinPE**.

---

## 4️⃣ Initialiser le nouveau disque (DiskPart)

```cmd
diskpart
list disk
select disk X    ← le nouveau disque (vide, 80 Go)
clean
convert gpt

create partition efi size=100
format quick fs=fat32 label=EFI
assign letter=S

create partition msr size=16

create partition primary
format quick fs=ntfs label=OS
assign letter=F

exit
```

> 🔍 **À savoir** : Identifie le bon disque avec `list disk` — le nouveau est celui qui affiche 0 Mo utilisés.

---

## 5️⃣ Assigner une lettre à l'ancien disque OS

```cmd
diskpart
list disk
select disk Y    ← l'ancien disque OS
list partition
select partition Z    ← la partition principale NTFS
assign letter=D
exit
```

Vérifie que c'est le bon :

```cmd
dir D:\
```

Tu dois voir : `Windows`, `Program Files`, `Users`. Si t'as ça, t'es sur le bon disque.

> ⚠️ **Attention** : Si `dir D:\` affiche du vide ou une erreur, recommence avec une autre partition.

---

## 6️⃣ Copier l'OS en offline (robocopy)

```cmd
robocopy D:\ F:\ /MIR /COPYALL /XJ /R:0 /W:0
```

**Décodage des flags :**
- `/MIR` : miroir complet
- `/COPYALL` : préserve tous les attributs (ACL, timestamps)
- `/XJ` : exclut les jonctions (évite les boucles infinies)
- `/R:0 /W:0` : pas de retry, pas d'attente

**Résultats attendus :**
- ✅ `FAILED : 0` → C'est tout ce qui compte
- ✅ Quelques fichiers skippés → Normal (`pagefile.sys`, `hiberfil.sys`)
- ❌ `FAILED > 0` → Ajoute `/LOG:C:\robocopy.log` pour identifier les fichiers en cause

> 💡 **Astuce** : La copie prend 10-30 minutes selon la taille de l'OS.

---

## 7️⃣ Reconstruire le boot UEFI

```cmd
bcdboot F:\Windows /s S: /f UEFI
```

Message attendu :
```
Les fichiers de démarrage ont bien été créés.
```

> ⚠️ **Attention** : Si la commande échoue sur la partition EFI, vérifie que `S:` est bien formatée en FAT32.

---

## 8️⃣ Préparer le redémarrage

```cmd
exit
```

Puis dans Hyper-V **avant de démarrer** :
1. Éteindre la VM
2. Retirer l'ISO du lecteur DVD
3. Remettre le disque dur en premier dans l'ordre de boot

---

## 9️⃣ Premier démarrage et vérifications

La VM doit démarrer directement sur Windows Server. Une fois connecté, valide l'intégrité :

```cmd
sfc /scannow
dism /online /cleanup-image /checkhealth
```

Résultat attendu pour DISM :
```
Aucun endommagement du magasin de composants n'a été détecté.
```

---

## ✅ Validation finale

**Test Export-VM :**
```powershell
Export-VM -Name "SRV-XXX" -Path "F:\Hyper-V\EXPORT_TEST"
```

**Test sauvegarde VSS :**
Lance une sauvegarde manuelle. Elle doit passer sans checkpoint bloquant.

---

## 🧹 Nettoyage final

1. Supprimer l'ancien VHDX corrompu
2. Renommer : `SRV-XXX_OS_NEW.vhdx` → `SRV-XXX_OS.vhdx`
3. Mettre à jour la documentation de la VM

```powershell
Rename-Item "F:\Hyper-V\Disks\SRV-XXX_OS_NEW.vhdx" "SRV-XXX_OS.vhdx"
```

---

## 🚨 Problèmes courants

**`bcdboot` échoue avec "Impossible d'ouvrir le magasin BCD"**
→ La partition EFI n'est pas FAT32. Reformate-la : `format quick fs=fat32`

**La VM démarre sur l'écran de réparation Windows**
→ Lettres de lecteur incorrectes dans bcdboot. Redémarre en WinPE et relance `bcdboot F:\Windows /s S: /f UEFI` en vérifiant les lettres.

**`sfc /scannow` remonte des erreurs non réparées**
→ Lance `dism /online /cleanup-image /restorehealth` puis relance sfc.

---

## 🎬 Conclusion

Cette procédure est la réponse à "ma VM tourne mais rien ne fonctionne autour". En repartant sur un VHDX OS structurellement sain, tu obtiens un système exportable, sauvegardable et propre pour DISM.

Pas de réinstallation, pas de migration de rôles, pas de reconfiguration. Le disque DATA n'a pas bougé d'un octet.

Si tu te demandes quelle génération de VM Hyper-V choisir pour éviter ce genre de situation dès le départ, consulte [Hyper-V Gen1 vs Gen2 : laquelle choisir ?](https://brandonvisca.com/hyperv-gen1-vs-gen2-quelle-generation-choisir/).

---

## ❓ FAQ

**Est-ce que cette procédure fonctionne sur Hyper-V Gen1 ?**
Non, Gen1 utilise le BIOS legacy. Utilise `bootrec /fixboot` et `bootrec /rebuildbcd` à la place de bcdboot. La partie robocopy reste identique.

**Est-ce que je perds mes données du disque DATA ?**
Non. Le disque DATA n'est jamais touché pendant toute la procédure.

**Pourquoi ne pas simplement réparer Windows avec l'ISO ?**
L'option "Réparer l'ordinateur" ne touche pas la corruption logique du système de fichiers. Repartir sur un VHDX vierge contourne complètement le problème.

**Combien de temps ça prend ?**
45 minutes à 1h30 selon la taille de l'OS. La copie robocopy représente 80% du temps.

---

## 📊 Paramètres Rank Math

**Focus Keyphrase** : restaurer vm hyper-v vhdx corrompu

**Title** : VM Hyper-V irrécupérable ? Restaure l'OS sans réinstaller (2026)
(58 caractères)

**Description** :
Export-VM qui plante, sauvegardes VSS bloquées ? Procédure complète pour reconstruire un VHDX OS sain via WinPE + robocopy + bcdboot, sans réinstaller.
(153 caractères)

**Slug** : restaurer-vm-hyperv-vhdx-corrompu-winpe

---

## 🔗 Maillage interne

- [[2026-03-10-hyperv-gen1-vs-gen2-quelle-generation-choisir]] — cité en conclusion

## 📝 Articles complémentaires suggérés

- "VSS Hyper-V : pourquoi tes sauvegardes échouent (et comment réparer)"
- "Export-VM Hyper-V automatisé : script PowerShell hebdomadaire"
