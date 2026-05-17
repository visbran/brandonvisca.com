---
title: "pfSense 2.8 : télécharger l'ISO, mettre à jour et éviter les pièges (2026)"
description: "Télécharger pfSense 2.8.1, mettre à jour depuis 2.7.x ou installer l'ISO : guide complet avec les pièges FreeBSD 15 à éviter avant de cliquer."
pubDatetime: "2025-06-01T19:41:15+02:00"
modDatetime: "2026-05-17T00:00:00+01:00"
author: Brandon Visca
tags:
  - securite
  - reseau
  - intermediaire
  - guide
featured: false
draft: false
focusKeyword: pfSense 2.8
faqs:
  - question: "Quelles sont les nouveautés de pfSense CE 2.8 ?"
    answer: "Passage à FreeBSD 15.0 (meilleur support matériel), PHP 8.3, OpenVPN 2.6.10, Unbound 1.22, NAT64, Kea DHCP avec HA, nouveau backend PPPoE plus rapide. Corrections de failles XSS, injections et divulgation d'infos dans la WebGUI."
  - question: "Comment télécharger pfSense CE 2.8 ?"
    answer: "Télécharge l'ISO officielle sur netgate.com/downloads. Choisis pfSense CE, version 2.8.1 (dernière stable). L'image est au format ISO/gzip, à flasher avec Balena Etcher ou Rufus sur ta clé USB."
  - question: "Comment mettre à jour pfSense vers la version 2.8 ?"
    answer: "Sauvegarde la config via Diagnostics > Backup & Restore > Download configuration. Ensuite : System > Update > Update Settings, sélectionne la branche CE Latest Stable (2.8.1), clique Update et laisse redémarrer."
  - question: "La mise à jour vers pfSense 2.8 est-elle stable ?"
    answer: "Oui. La 2.8.1 est stable en production. La 2.8.0 avait des bugs sur Dynamic DNS et les interfaces, corrigés dans la 2.8.1 sortie fin 2025. Teste toujours en lab avant production sur des configs complexes."
  - question: "Quels matériels sont compatibles avec pfSense 2.8 ?"
    answer: "Support natif du matériel moderne Intel/AMD 64 bits grâce à FreeBSD 15. Les chipsets Realtek s'en sortent mieux qu'avant. Les cartes Intel NIC (i210, i350) restent le choix recommandé. Vérifie le Hardware Compatibility List Netgate en cas de doute."
---
> 💡 **TL;DR** : Télécharge pfSense 2.8.1 (CE) sur [netgate.com](https://www.netgate.com/pfsense-plus-software/how-to-buy#pfsense-ce). Mise à jour depuis 2.7.x : sauvegarde config → System > Update → sélectionne CE 2.8.1 → redémarre. Sous Proxmox, préfère une clean install + import config.xml. WireGuard est intégré nativement — réimporte tes clés si tu migres depuis 2.7.x.

![pfSense CE 2.8 mise à jour](snl-saturday-night-live-season-47-fn7eouktflhxhwkgfi.gif)

Tu administres un pare-feu pfSense et tu as vu passer la mise à jour 2.8 ? Pas si vite.

Ce n'est pas une simple révision de sécurité. Avec le passage à FreeBSD 15.0, des correctifs critiques et des changements profonds dans les pilotes réseau, pfSense 2.8 bouscule plusieurs habitudes. La version 2.8.1, sortie fin 2025, ajoute 19 correctifs supplémentaires sur Dynamic DNS, les interfaces et OpenVPN.

J'ai moi-même migré deux firewalls — l'un sous Proxmox, l'autre bare-metal — avec quelques surprises que je te partage ici. Si tu utilises pfBlockerNG, WireGuard ou une configuration ZFS, tu vas vouloir lire jusqu'au bout.

Les [notes de version officielles pfSense 2.8.0](https://docs.netgate.com/pfsense/en/latest/releases/2-8-0.html) publiées par Netgate restent la référence pour le détail exhaustif.

## Table des matières

- - - - - -

## Nouveautés de pfSense 2.8

### Passage à FreeBSD 15.0

C'est le changement le plus marquant. pfSense 2.8 repose sur FreeBSD 15-CURRENT : environnement plus moderne, meilleure compatibilité matérielle pour les chipsets récents, performances réseau améliorées.

J'ai constaté un démarrage plus rapide et une gestion plus fluide des interfaces réseau — gain de stabilité notable sur les plateformes virtualisées.

Points clés du passage à FreeBSD 15 :

- **PPPoE** : nouveau backend `if_pppoe` plus rapide (encore facultatif)
- **ZFS root natif** : facilite les snapshots avant mise à jour
- **NAT64** : support des environnements mixtes IPv6/IPv4
- **Kea DHCP** boosté : HA, DNS dynamique, RAM disk, ARP statique

### Améliorations de performance

Dans un environnement à fort débit (client PME avec VLANs multiples et règles NAT complexes), la latence a baissé de 5 à 10 % mesurée via iperf3. Le rechargement des règles est plus rapide, la WebGUI reste fluide même après plusieurs modifications consécutives.

### Nouvelles fonctionnalités notables

- WireGuard intégré par défaut (plus besoin du package séparé)
- Interface améliorée pour les diagnostics DNS
- Menu Status > DHCP Leases plus clair pour les parcs avec IP statiques mixtes
- Politique d'état par défaut plus sécurisée (avec cas particuliers à surveiller)

- - - - - -

## Changements techniques importants

### Packages mis à jour

Les paquets intégrés ont été recompilés pour FreeBSD 15 :

- OpenVPN 2.6.10
- PHP 8.3
- Unbound 1.22
- OpenSSH 9.6p1

Pour vérifier les versions de tes packages en SSH :

```bash
pkg info
```

### Compatibilité matérielle et pilotes

Les chipsets Realtek s'en sortent nettement mieux sous FreeBSD 15. Les cartes Intel NIC (i210, i350) restent néanmoins le choix recommandé pour la production.

Si tu as une carte Intel avec SFP non supporté, ajoute ce flag au bootloader :

```bash
echo 'hw.ixl.allow_unsupported_sfp=1' >> /boot/loader.conf
```

### Suppressions et dépréciations

OpenSSH passe à 9.6p1 avec désactivation des algorithmes faibles (DSA, CBC). Si tu as une politique d'authentification par clé, vérifie la compatibilité avant la mise à jour :

```bash
ssh -Q key
```

- - - - - -

## Sécurité et correctifs pfSense 2.8

### CVE corrigés

Parmi les dizaines de CVE traités dans la 2.8.0 :

- CVE-2024-3094 (liblzma/XZ backdoor)
- CVE-2024-22855 (OpenVPN DoS)
- CVE-2024-29149 (PHP FPM)
- Corrections XSS, injections et divulgation d'informations dans la WebGUI

Le détail complet est dans la [release note officielle Netgate](https://docs.netgate.com/pfsense/en/latest/releases/2-8-0.html).

### Renforcement système

- Sandbox FreeBSD renforcée
- Permissions durcies par défaut dans `/usr/local/www`
- Logs SSH et WebGUI mieux filtrés dans le dashboard système

Pour aller plus loin sur la sécurisation de tes services exposés derrière pfSense, le guide [Nginx et les headers HTTP](https://brandonvisca.com/nginx-location-bloc-et-securite/) couvre la couche applicative en complément du firewall.

### Changements TLS/SSH

OpenSSH 9.6p1 désactive les algorithmes faibles (DSA, CBC). Si tu gères des accès SSH vers ton pfSense depuis des clients anciens, vérifie la compatibilité avant de mettre à jour.

- - - - - -

## pfSense 2.8.1 : les correctifs

La 2.8.1 est sortie fin 2025. Elle corrige 19 issues identifiées depuis la 2.8.0, dont 1 haute priorité. Voici ce qui a été patché :

**Operating System** : corrections de stabilité FreeBSD 15, fixes de race conditions au démarrage.

**Dynamic DNS (haute priorité)** : mise à jour qui échouait silencieusement sur certains providers. Comportement corrigé avec logs explicites dans le dashboard.

**Interfaces** : gestion plus robuste des VLANs lors du redémarrage, fix sur les interfaces qui ne remontaient pas après upgrade.

**OpenVPN** : corrections sur la reconnexion automatique des clients et la gestion des certificats expirés.

**Rules/NAT** : fix sur des règles NAT qui disparaissaient dans certaines configurations de basculement HA.

**Dashboard** : corrections d'affichage sur les widgets température et trafic en temps réel.

**System Logs** : amélioration du filtrage et de la rotation des logs système.

**Kea DHCP** : fixes sur la synchronisation HA et la gestion des baux entre nœuds.

> ⚠️ **Si tu es en 2.8.0** : la mise à jour vers 2.8.1 est recommandée, surtout si tu utilises Dynamic DNS ou WireGuard.

- - - - - -

## Procédure de mise à jour

### Prérequis et sauvegarde

Avant de toucher quoi que ce soit :

1. Vérifie que ton matériel est 64 bits
2. Désactive temporairement les paquets tiers critiques (Snort, Suricata)
3. Sauvegarde la configuration : Diagnostics > Backup & Restore > Download configuration
4. Exporte tes certificats
5. Crée un snapshot ZFS si tu es déjà sur ce système de fichiers

> 💡 **Astuce** : Sous Proxmox, fais un snapshot de ta VM avant de lancer la mise à jour. 30 secondes qui peuvent t'éviter des heures de restauration.

### Étapes de mise à jour

1. Accède à **System > Update > Update Settings**
2. Sélectionne : `pfSense CE Upgrade Branch : Latest Stable Version (2.8.1)`
3. Clique sur **Update** et laisse tourner
4. Redémarre manuellement si le firewall ne le fait pas automatiquement
5. Vérifie l'état de tes interfaces, VLANs et règles après redémarrage

### Virtualisation et HA

**Sous Proxmox ou VMware** : préfère une clean install avec l'ISO 2.8.1, puis importe ton `config.xml`. La mise à jour en place fonctionne, mais l'ISO propre évite les surprises sur les pilotes virtuels.

**En configuration HA (CARP)** :
1. Mets à jour le secondary en premier
2. Bascule les rôles
3. Mets à jour l'ancien primary
4. Rebascule si nécessaire

### Compatibilité des packages tiers

- **pfBlockerNG 3.2.4_4** : fonctionnel. Force un reload GeoIP après l'upgrade.
- **WireGuard** : intégré nativement. Tu devras réimporter les clés si tu migres depuis 2.7.x.
- **squidGuard** : nécessite une réinstallation complète.
- **Snort / Suricata** : désactive avant la mise à jour, réinstalle après.

Vérifie tes packages via **System > Package Manager** avant de lancer la mise à jour.

- - - - - -

## Problèmes courants post-mise à jour

### DNS Resolver ne répond plus

Le problème le plus fréquent signalé post-upgrade. Redémarre le service Unbound via **Status > Services**, ou flush les paramètres depuis **Services > DNS Resolver**.

### Lenteurs WebGUI

Un redémarrage complet règle généralement le problème. Si ça persiste, redémarre PHP-FPM en SSH :

```bash
service php-fpm restart
```

### VLANs qui ne remontent pas

Vérifie l'état de tes interfaces virtuelles après l'upgrade : **Interfaces > Interface Assignments**. Les VLANs doivent être listés et actifs. Si ce n'est pas le cas, re-sauvegarde la config d'interface sans modifier et applique.

### Clés WireGuard perdues

Si tu migres depuis une version sans WireGuard natif, tes clés ne sont pas transférées automatiquement. Réimporte-les depuis **VPN > WireGuard**.

Pour les problèmes de configuration SSH post-migration, le guide [sécuriser son serveur Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/) couvre le durcissement qui s'applique aussi au shell pfSense.

Si tu héberges des services derrière ton pfSense, [Vaultwarden avec Docker](https://brandonvisca.com/vaultwarden-docker-gestionnaire-mots-de-passe/) est un bon exemple de service auto-hébergé à protéger derrière ce firewall.

- - - - - -

## Conclusion

pfSense 2.8.1, c'est la version à déployer en 2026. FreeBSD 15.0 sous le capot, WireGuard natif, Kea DHCP avec HA, et 19 correctifs supplémentaires depuis la 2.8.0. Le piège principal : migrer depuis 2.7.x sans sauvegarder les clés WireGuard, ou oublier de forcer le reload pfBlockerNG. Suis la checklist, fais un snapshot si tu es sous Proxmox, et tu t'en sortiras sans accroc. Pour les configs complexes, teste d'abord en lab.

## Pour aller plus loin

- [Notes de version pfSense 2.8.0 — Netgate](https://docs.netgate.com/pfsense/en/latest/releases/2-8-0.html)
- [Documentation principale pfSense — Netgate](https://docs.netgate.com/pfsense/en/latest)
- [Sécuriser son serveur Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/)

## Articles connexes

- [Exchange Online : bloquer les transferts email automatiques avec PowerShell (2026)](/exchange-online-bloquer-transferts-automatiques-emails/)
- [Passkey SSH : remplace tes clés avec SSH ID (2026)](/passkey-ssh-sshid/)
- [Technitium DNS Server : installe ton bloqueur de pubs libre (2026)](/technitium-dns-server/)
- [Vaultwarden avec Docker : Gestionnaire de Mots de Passe Gratuit (Adieu 1Password !)](/vaultwarden-docker-gestionnaire-mots-de-passe/)
