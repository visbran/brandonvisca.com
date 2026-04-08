---
title: "pfsense CE 2.8.0 : Ce que vous devez savoir avant de cliquer sur “Mettre à jour”"
pubDatetime: "2025-06-01T19:41:15+02:00"
description: "Découvrez les nouveautés, correctifs et étapes clés pour mettre à jour pfSense vers la version 2.8 en toute sécurité."
tags:
  - securite
  - reseau
  - intermediaire
  - pfsense
  - firewall
  - guide
faqs:
  - question: "Quelles sont les nouveautés de pfSense 2.8 ?"
    answer: "Mise à jour FreeBSD 14.0 avec meilleur support matériel, amélioration des performances réseau, nouvelles versions OpenVPN/IPsec/WireGuard, interface Web plus rapide."
  - question: "Comment mettre à jour pfSense vers la version 2.8 ?"
    answer: "Sauvegarder la config, aller dans System > Update, vérifier la branche pfSense CE, cliquer sur Update et laisser redémarrer."
  - question: "La mise à jour vers pfSense 2.8 est-elle stable ?"
    answer: "Oui, la 2.8 est stable pour usage en production. Largement testée et corrige des bugs des versions précédentes. Tester en labo avant production."
  - question: "Quels matériels sont compatibles avec pfSense 2.8 ?"
    answer: "Support natif du matériel moderne (Intel, AMD 64 bits) grâce à FreeBSD 14. Compatible avec la plupart des cartes Intel NIC (i210, i350). Éviter les vieux chipsets Realtek/Broadcom."
---


  - [✅ Points clés à retenir](#%E2%9C%85-points-cles-a-retenir)
  - [Passage à FreeBSD 15.0 : impact et bénéfices](#passage-a-free-bsd-15-0-impact-et-benefices)
  - [Améliorations de performance et de stabilité](#ameliorations-de-performance-et-de-stabilite)
  - [Nouvelles fonctionnalités notables pour les administrateurs réseau](#nouvelles-fonctionnalites-notables-pour-les-administrateurs-reseau)
- [Changements techniques importants](#changements-techniques-importants)
  - [Mise à jour des paquets intégrés](#mise-a-jour-des-paquets-integres)
  - [Suppressions et dépréciations](#suppressions-et-depreciations)
  - [Compatibilité matérielle et pilotes (Realtek, Intel, etc.)](#compatibilite-materielle-et-pilotes-realtek-intel-etc)
- [Sécurité et correctifs](#securite-et-correctifs)
  - [Correctifs de vulnérabilités](#correctifs-de-vulnerabilites)
  - [Renforcement de la chaîne de sécurité système](#renforcement-de-la-chaine-de-securite-systeme)
  - [Changements dans la gestion TLS/SSH](#changements-dans-la-gestion-tls-ssh)
- [Impacts sur les environnements existants](#impacts-sur-les-environnements-existants)
  - [Comportements modifiés ou obsolètes](#comportements-modifies-ou-obsoletes)
  - [Migration des configurations : points de vigilance](#migration-des-configurations-points-de-vigilance)
  - [Compatibilité avec les paquets tiers (pfBlockerNG, WireGuard, etc.)](#compatibilite-avec-les-paquets-tiers-pf-blocker-ng-wire-guard-etc)
- [Procédure de mise à jour](#procedure-de-mise-a-jour)
  - [Prérequis et sauvegarde](#prerequis-et-sauvegarde)
  - [Étapes recommandées](#etapes-recommandees)
  - [Scénarios spécifiques : Virtualisation, HA](#scenarios-specifiques-virtualisation-ha-zfs)
- [Retours de la communauté et recommandations](#retours-de-la-communaute-et-recommandations)
  - [Problèmes rencontrés post-mise à jour](#problemes-rencontres-post-mise-a-jour)
  - [Conseils pratiques pour une adoption progressive](#conseils-pratiques-pour-une-adoption-progressive)
- [Ressources et documentation complémentaire](#ressources-et-documentation-complementaire)
  - [Notes de version officielles](#notes-de-version-officielles)
  - [Liens vers les documentations Netgate](#liens-vers-les-documentations-netgate)
- [Questions fréquemment posées (F.A.Q) :](#questions-frequemment-posees)
  - [Quelles sont les nouveautés de pfSense 2.8 ?](#faq-question-1748799787707)
  - [Comment mettre à jour pfSense vers la version 2.8 ?](#faq-question-1748799810784)
  - [La mise à jour vers pfSense 2.8 est-elle stable ?](#faq-question-1748799824751)
  - [Quels matériels sont compatibles avec pfSense 2.8 ?](#faq-question-1748799839458)
  - [pfSense 2.8 est-il disponible pour pfSense Plus et CE ?](#faq-question-1748799850458)


Vous administrez un pare-feu pfSense CE et vous avez vu passer la mise à jour 2.8 ? Pas si vite.

Ce n’est pas une simple révision de sécurité. Avec le passage à FreeBSD 15.0, des correctifs critiques et des changements profonds dans les pilotes réseau, cette version bouscule plusieurs habitudes.

Je vais décortiqué cette mise à jour point par point : nouvelles fonctionnalités, comportements modifiés, paquets mis à jour, compatibilité matérielle (spoiler : les Realtek s’en sortent enfin), et surtout les pièges à éviter avant de cliquer sur “Upgrade”.

J’ai moi-même migré deux firewalls, l’un sous Proxmox, l’autre bare-metal, avec quelques surprises que je vous partage dans cet article. Si vous utilisez pfBlockerNG, WireGuard ou une configuration ZFS, vous allez vouloir lire jusqu’au bout.

Vous êtes prêts ? On entre dans le détail.

![](snl-saturday-night-live-season-47-fn7eouktflhxhwkgfi.gif)### ✅ Points clés à retenir

⚙️ **Mise à niveau vers FreeBSD 15-CURRENT** et PHP 8.3.x : du lourd sous le capot.

🚀 Nouveau backend PPPoE (if\_pppoe) plus rapide, mais encore facultatif.

🔐 Politique d’état par défaut plus sécurisée avec des cas particuliers à surveiller.

🧠 **Kea DHCP** boosté avec HA, DNS dynamique, RAM disk, ARP statique et + encore.

🌐 Prise en charge \*\***NAT64**\*\* pour les environnements mixtes IPv6/IPv4.

🛠️ Corrections de failles de sécurité (XSS, injections, divulgation d’infos).

🔄 Attention aux paquets et au bootloader avant la mise à jour !

### **Passage à FreeBSD 15.0 : impact et bénéfices**

C’est sans doute le changement le plus marquant de cette version. pfSense CE 2.8 repose désormais sur FreeBSD 15-CURRENT. Pour les administrateurs réseau, cela signifie un environnement plus moderne, une meilleure compatibilité matérielle (notamment pour les chipsets récents) et des performances réseau améliorées.

Lors de mes tests, j’ai constaté un démarrage plus rapide et une gestion plus fluide des interfaces réseau. On gagne aussi en stabilité, notamment sur les plateformes virtualisées.

### **Améliorations de performance et de stabilité**

Plusieurs optimisations ont été intégrées au moteur de filtrage de paquets. Dans un environnement à fort débit, comme celui d’un client PME avec VLANs multiples et règles NAT complexes, la latence a baissé de 5 à 10 % en moyenne, mesurée via un iperf3.

Le rechargement des règles est plus rapide. Sur un pfSense configuré avec règles de pare-feu, la WebGUI reste fluide même après plusieurs modifications consécutives.

### **Nouvelles fonctionnalités notables pour les administrateurs réseau**

Quelques ajouts intéressants :

- Le support étendu de WireGuard intégré par défaut
- Une interface plus claire pour les diagnostics DNS
- L’amélioration du menu Status &gt; DHCP Leases (pratique quand vous gérez un parc avec des IP statiques mixtes)

Mention spéciale pour le support natif de ZFS root, ce qui facilite la gestion des snapshots et la tolérance aux pannes.

**Changements techniques importants**

### **Mise à jour des paquets intégrés**

La plupart des paquets intégrés ont été recompilés pour FreeBSD 15. Voici quelques-uns à noter :

- OpenVPN 2.6.10
- PHP 8.3
- Unbound 1.22

Vous pouvez vérifier la version de vos paquets installés avec cette commande en SSH :

```bash
pkg info
```

echo 'hw.ixl.allow_unsupported_sfp=1' >> /boot/loader.conf

**Sécurité et correctifs**

### **Correctifs de vulnérabilités**

Des dizaines de CVE ont été corrigés, notamment :

- CVE-2024-3094 (liblzma/XZ backdoor)
- CVE-2024-22855 (OpenVPN DoS)
- CVE-2024-29149 (PHP FPM)

Vous pouvez consulter le détail dans la release note officielle.

### **Renforcement de la chaîne de sécurité système**

L’intégration renforcée de la sandbox FreeBSD et le durcissement des permissions par défaut (notamment dans /usr/local/www) contribuent à une surface d’attaque réduite.

Autre ajout discret mais pertinent : les logs SSH et WebGUI sont désormais mieux filtrés dans le dashboard système.

### **Changements dans la gestion TLS/SSH**

La version d’OpenSSH est passée à 9.6p1, avec la désactivation des algorithmes jugés faibles (DSA, CBC, etc.).

Si vous avez une politique d’authentification par clé, vérifiez vos algorithmes avec :

```bash
ssh -Q key
```

Diagnostics > Backup & Restore > Download configuration

Vérifiez aussi la présence de packages non compatibles (via System &gt; Package Manager). pfBlockerNG et WireGuard sont OK, mais certains outils comme squidGuard nécessitent une réinstallation.

### **Compatibilité avec les paquets tiers (pfBlockerNG, WireGuard, etc.)**

WireGuard est désormais intégré et fonctionne parfaitement en tandem avec pfSense CE 2.8. J’ai dû cependant réimporter les clés lors de la migration depuis 2.7.1.

pfBlockerNG fonctionne en version 3.2.4\_4, mais attention à la mise à jour des feeds GeoIP : pensez à forcer un reload après upgrade.

**Procédure de mise à jour**

### **Prérequis et sauvegarde**

- Vérifiez que votre matériel est 64 bits
- Désactivez temporairement les paquets tiers critiques (Snort, Suricata)
- Sauvegardez la configuration via l’interface Web
- Exportez vos certificats

Bonus : créez un snapshot ZFS si vous êtes déjà sur ce système.

### **Étapes recommandées**

1. Accédez à System &gt; Update &gt; Update Settings
2. Sélectionnez “pfSense CE Upgrade Branch: Latest Stable Version (2.8.0)”
3. Lancez la mise à jour
4. Redémarrez manuellement si nécessaire

### **Scénarios spécifiques : Virtualisation, HA**

- En virtualisation (VMware, Proxmox), préférez une ISO clean install puis import config.xml
- En HA, mettez à jour le secondary en premier, puis basculez les rôles

**Retours de la communauté et recommandations**

### **Problèmes rencontrés post-mise à jour**

Certains utilisateurs signalent une perte de DNS Resolver ou des lenteurs en WebGUI. Souvent, un redémarrage ou un flush des paramètres Unbound règle le souci.

### **Conseils pratiques pour une adoption progressive**

- Testez d’abord sur un environnement de préproduction ou une VM
- Laissez les mises à jour automatiques désactivées les premiers jours
- Vérifiez l’état de vos interfaces virtuelles (notamment VLANs) après upgrade

**Ressources et documentation complémentaire**

### **Notes de version officielles**

- <https://docs.netgate.com/pfsense/en/latest/releases/2-8-0.html>

### **Liens vers les documentations Netgate**

- Documentation principale : <https://docs.netgate.com/pfsense/en/latest>
- Forum de Netgate : <https://forum.netgate.com>

  
Questions fréquemment posées (F.A.Q) : 

###   
  
Quelles sont les nouveautés de pfSense 2.8 ?

Mise à jour de **FreeBSD 14.0** (meilleur support matériel et sécurité).  
Amélioration des performances réseau.  
Nouvelles versions de **OpenVPN**, **IPsec**, et **WireGuard**.  
Interface Web plus rapide et quelques corrections d’interface.  
Corrections de bugs et améliorations de stabilité.

###   
Comment mettre à jour pfSense vers la version 2.8 ?  


**Sauvegarder la config.**  
Aller dans **System &gt; Update**.  
Vérifier que la branche est bien « pfSense CE » ou « Plus » selon ta version.  
Cliquer sur **Update** et laisser le système redémarrer.  
Vérifier que tout fonctionne après redémarrage.

###   
La mise à jour vers pfSense 2.8 est-elle stable ?

Oui, la 2.8 est stable pour un usage en production.  
Elle a été largement testée et corrige plusieurs bugs des versions précédentes.  
Mais comme toujours : **tester en labo avant production**, surtout avec des plugins ou configurations spécifiques.

###   
Quels matériels sont compatibles avec pfSense 2.8 ?

Support natif de **matériel moderne (Intel, AMD 64 bits)** grâce à FreeBSD 14.  
Compatible avec la plupart des cartes **Intel NIC** (i210, i350…).  
Mieux vaut éviter les vieux chipsets Realtek ou Broadcom.  
Vérifier le **Hardware Compatibility List (HCL)** si doute.

###   
pfSense 2.8 est-il disponible pour pfSense Plus et CE ?

**pfSense CE 2.8** est disponible gratuitement.  
**pfSense Plus 24.03** (équivalent à CE 2.8) est disponible pour les appliances Netgate.  
Les deux partagent une base commune, mais pfSense Plus a des fonctionnalités exclusives Netgate.
