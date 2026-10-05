---
title: "OpenWrt firmware : le routeur open-source pour ton homelab"
description: Installer OpenWrt firmware sur ton routeur, passer à apk en 25.12, comparer avec pfSense et éviter les pièges classiques avant de flasher ton homelab.
pubDatetime: "2026-10-05T11:09:49+02:00"
modDatetime: "2026-10-04T08:00:00.000Z"
author: Brandon
tags:
  - reseau
  - wireguard
  - intermediaire
featured: false
draft: false
focusKeyword: openwrt
faqs:
  - question: "OpenWrt peut-il remplacer pfSense sur un mini PC x86 ?"
    answer: "Oui, OpenWrt tourne très bien sur x86. Mais si ton besoin est un pare-feu complet avec une interface pensée pour ça, pfSense reste plus confortable. OpenWrt brille surtout sur le Wi-Fi et les cartes réseau exotiques."
  - question: "Est-ce que je perds ma configuration en passant de 24.10 à 25.12 ?"
    answer: "Dans la plupart des cas non, sysupgrade tente de migrer ta config. Fais quand même une sauvegarde avant. Un passage direct depuis la 23.05 n'est pas supporté officiellement."
  - question: "Pourquoi mes commandes opkg ne marchent plus depuis la 25.12 ?"
    answer: "Depuis la 25.12, opkg est remplacé par apk, le gestionnaire de paquets Alpine. La plupart des noms de paquets ne changent pas, et le projet publie un aide-mémoire opkg vers apk."
---
> 💡 **TL;DR**
> - OpenWrt est un firmware Linux libre pour routeurs et équipements embarqués, installable sur un routeur compatible ou sur un mini PC x86
> - La branche stable courante est la 25.12, avec la version 25.12.5 publiée le 1er juillet 2026 selon le site officiel
> - Depuis la 25.12, le gestionnaire de paquets change : opkg laisse la place à apk, et une sauvegarde de config reste indispensable avant tout flash

Ton routeur d'opérateur fait le job, jusqu'au jour où tu veux un DNS qui filtre, un VPN qui tient la route ou un Wi-Fi qui ne s'effondre pas au deuxième étage. Là, tu tombes sur OpenWrt. Et tu te rends compte qu'un routeur, c'est juste un ordinateur Linux avec des ports réseau, sauf qu'on t'a enfermé dans une interface web de 2009.

OpenWrt te rend la main. Un vrai système Linux, un shell, un gestionnaire de paquets, et une interface web (LuCI) pour ceux qui ne veulent pas tout éditer à la main. Dans cet article, on voit ce que c'est, en quoi ça se compare à pfSense, comment choisir son matériel, comment installer et mettre à jour, et les pièges à éviter.

## Table des matières

## OpenWrt, c'est quoi au juste

OpenWrt est une distribution Linux open-source pensée pour les équipements embarqués, en particulier les routeurs. Le projet se présente lui-même comme un système d'exploitation Linux destiné aux appareils embarqués, et c'est exactement ce qu'il est : un remplaçant du firmware que le constructeur a glissé dans ta box.

Concrètement, tu gagnes trois choses. D'abord, un noyau et des paquets à jour, sans attendre que le fabricant daigne publier un correctif. Ensuite, un contrôle fin sur le routage, le pare-feu, le Wi-Fi et les VPN. Enfin, un écosystème de paquets qui te permet d'ajouter un serveur WireGuard, un client DNS ou un agent de supervision sans rien compiler.

La branche stable courante s'appelle 25.12. Le site officiel annonce la version 25.12.5 comme dernière publiée, sortie le 1er juillet 2026. Les images pour chaque cible sont disponibles sur le téléchargeur officiel, et le sélecteur de firmware permet de générer une image adaptée à ton modèle.

## OpenWrt contre pfSense : le vrai comparatif

Tu vas forcément te poser la question, parce que tout homelab qui se respecte a déjà eu son petit débat pfSense contre autre chose. On a déjà parlé de pfSense dans [mon article sur la mise à jour vers la 2.8](/mise-a-jour-pfsense-2-8-nouveautes-installation/), donc je ne reviens pas sur les détails. Ici, on compare les philosophies.

pfSense repose sur FreeBSD et se présente comme un pare-feu complet. Il est pensé pour être installé sur du matériel dédié, avec une interface qui couvre pare-feu, VPN, IDS et IPS sans que tu aies à assembler les morceaux. En contrepartie, il demande une machine un peu plus solide que ce que peut offrir un petit routeur de salon.

OpenWrt, lui, est pensé pour les équipements à ressources limitées et pour le Wi-Fi. Comme c'est du Linux, la prise en charge matérielle est souvent plus large, notamment pour les cartes réseau ou les puces Wi-Fi moins courantes. Sur x86, les deux fonctionnent très bien. La vraie question est donc celle-ci :

- Tu veux un pare-feu complet, avec une interface pensée pour ça et une doc très rodée : pfSense
- Tu veux un routeur, un point d'accès Wi-Fi ou un équipement avec une carte exotique : OpenWrt
- Tu veux un petit serveur qui fait routeur, VPN et Wi-Fi sur un seul boîtier : les deux se défendent, mais OpenWrt est plus léger à faire tourner
- Tu veux un outil qui se paramètre surtout en ligne de commande : OpenWrt, sans hésiter

Le bon choix dépend donc surtout de ce que tu attends de la box : un pare-feu qui fait tout, ou un système Linux qu'on peut plier dans tous les sens. Les deux ne s'excluent pas, et rien ne t'empêche de combiner un pare-feu dédié avec des points d'accès OpenWrt.

## Matériel : bien choisir avant de flasher

Avant d'installer quoi que ce soit, vérifie que ton matériel est supporté. Le moyen le plus fiable reste la table de matériel officielle (Table of Hardware) et le sélecteur de firmware, qui ne propose que les cibles réellement compatibles avec ta version. Ne te fie pas aux forums de 2019, ils ne reflètent plus l'état actuel.

Pour un routeur de salon, regarde la mémoire flash et la RAM, mais surtout le chipset Wi-Fi. Pour un mini PC x86 sous OpenWrt, c'est plus simple : il suffit d'avoir deux interfaces réseau et un CPU compatible, puis de prendre l'image correspondante. C'est d'ailleurs la voie que je recommande si tu veux du routage sérieux avec de la marge.

⚠️ Attention, certains modèles changent de nom d'interface en 25.12. Le Bananapi BPI-R4, par exemple, voit ses ports renommés (eth1 devient sfp-lan ou lan4, eth2 devient sfp-wan). Si tu as des règles de pare-feu codées en dur sur les anciens noms, elles tomberont en silence. Relis ta config après la migration.

## Installation : sysupgrade, ASU ou image brute

Pour le premier flash, tu pars souvent du firmware constructeur. Il faut alors utiliser l'image dite factory, qui passe par l'interface d'origine. Une fois OpenWrt en place, tu passes sur les images sysupgrade, qui conservent la configuration.

Pour OpenWrt, la méthode la plus simple reste le sélecteur de firmware. Tu choisis la version 25.12.5, ton modèle, puis les paquets que tu veux ajouter dès le départ, comme les outils WireGuard ou un client DNS. Le site génère une image sur mesure, à télécharger puis à flasher.

Depuis LuCI, tu passes par le menu d'administration pour le flash, avec l'option de conserver la configuration. Depuis le terminal, tu peux utiliser sysupgrade directement :

```
sysupgrade -v openwrt-25.12.5-<cible>-sysupgrade.bin
```

Le nom du fichier dépend de ta cible, donc remplace-le par celui que tu as téléchargé. L'option -v affiche le détail du processus. N'utilise l'option -n que si tu veux repartir d'une config vierge, parce qu'elle efface tout.

Il existe aussi ASU (Attended Sysupgrade), intégré à LuCI par défaut, qui télécharge et construit l'image côté serveur. Et sur les équipements avec suffisamment de stockage, l'outil en ligne de commande owut est aussi présent par défaut. Il offre plus de diagnostic, ce qui est utile quand une mise à jour se passe mal.

## Passer de 24.10 à 25.12 sans casser ton réseau

C'est la partie qui fait mal si tu ne la lis pas. Depuis la 25.12, OpenWrt remplace opkg par apk, le gestionnaire de paquets d'Alpine. Le fork d'opkg utilisé par le projet n'est plus maintenu, donc la bascule était inévitable. La bonne nouvelle, c'est que la plupart des noms de paquets ne changent pas. Seule une petite poignée bouge, et le projet publie un aide-mémoire opkg vers apk pour les correspondances.

Les commandes de base sont simples. Pour mettre à jour la liste des paquets puis le système :

```
apk update
apk upgrade
```

Pour chercher un paquet avant de l'installer, la commande de recherche d'apk prend la place de ton ancien réflexe opkg. Si tu tapes encore opkg dans tes scripts, ils vont échouer. Fais le ménage dans tes automatisations avant la migration, pas après.

Sur le passage de la 24.10 à la 25.12, sysupgrade tente de migrer la configuration, et la plupart des réglages restent identiques ou sont convertis proprement. Je te conseille quand même de faire une sauvegarde complète depuis LuCI avant de toucher à quoi que ce soit. En revanche, un saut direct depuis la 23.05 n'est pas supporté officiellement, donc passe d'abord par la 24.10.

Un détail qui surprend : la documentation de la 25.12 demande de régler le loglevel du cron sur 7 pour conserver une journalisation normale. Si tes logs de tâches planifiées disparaissent après la mise à jour, c'est probablement là qu'il faut regarder.

## Dépannage : les pièges classiques

Le piège numéro un, c'est le flash sans sauvegarde. Un sysupgrade qui ne conserve pas la configuration te renvoie à zéro, et si tu avais un accès distant configuré, tu peux te retrouver enfermé dehors. Avant chaque flash, exporte ta config, et garde un accès de secours (câble sur le LAN, ou console série si ton matériel en a une).

Le deuxième piège concerne le réseau d'OpenWrt. Si le WAN ou le LAN ont été renommés par la migration, ton routeur démarre mais n'a plus les bons ports dans les bonnes zones. Vérifie les interfaces et les zones de pare-feu juste après le redémarrage, pas une semaine plus tard quand tu cherches pourquoi Internet est lent.

Le troisième piège, c'est le mode de secours. OpenWrt dispose d'un mode failsafe qui démarre sans la configuration utilisateur. C'est le filet de sécurité quand tu as cassé un réglage sur une machine distante, et il vaut mieux savoir où il se trouve avant d'en avoir besoin.

✅ Liste de contrôle avant flash : sauvegarde de la config, image téléchargée depuis le sélecteur pour ta version, vérification des noms d'interfaces, accès de secours prêt. Quatre points, deux minutes, et tu évites la plupart des mauvaises surprises.

## Conclusion

OpenWrt n'est pas un remplaçant universel de pfSense, et il n'a pas vocation à l'être. C'est un firmware libre qui transforme un routeur ou un mini PC en outil réseau souple, avec une prise en charge matérielle large et un écosystème de paquets qui grandit à chaque version.

Si tu gardes en tête le piège de la bascule vers apk, la sauvegarde avant flash et la vérification des interfaces, la migration se passe généralement sans drame. Et si tu veux brancher ton routeur sur le reste du homelab, regarde du côté de [Unbound en Docker](/unbound-docker-dns-recursif/) pour le DNS récursif ou de [SNMPd](/snmpd-docker-monitorer-reseau/) pour la supervision.
