---
title: "OPNsense vs pfSense : quel pare-feu pour ton homelab en 2026"
description: "OPNsense vs pfSense : comparatif complet pour choisir ton pare-feu homelab en 2026, matériel, licences, VPN et facilité de configuration."
pubDatetime: "2026-11-02T11:02:11+01:00"
modDatetime: "2026-11-01T08:00:00.000Z"
author: Brandon
tags:
  - reseau
  - vpn
  - hardening
  - intermediaire
featured: false
draft: false
focusKeyword: opnsense vs pfsense
faqs:
  - question: "OPNsense ou pfSense, lequel tourne le mieux sur du matériel recyclé ?"
    answer: "Les deux fonctionnent avec un CPU dual-core 1 GHz et 4 Go de RAM selon la doc officielle d'OPNsense. Un mini PC ou un boîtier fanless suffit largement pour un trafic domestique."
  - question: "Peut-on migrer une configuration pfSense vers OPNsense sans tout refaire ?"
    answer: "Non, il n'existe pas d'import direct. Les deux partagent un héritage FreeBSD et m0n0wall, mais les formats de configuration ont divergé. Compte sur une reconfiguration manuelle, interface par interface."
  - question: "OPNsense et pfSense sont-ils vraiment gratuits pour un homelab ?"
    answer: "Oui dans les deux cas pour un usage personnel sur ton propre matériel. OPNsense reste open source avec une Business Edition optionnelle payante, pfSense se partage entre l'édition CE communautaire et pfSense Plus, facturée à l'heure sur les images cloud officielles."
---
> 💡 **TL;DR**
> - OPNsense (Deciso, Pays-Bas) et pfSense (Netgate) sortent tous les deux du même ancêtre m0n0wall, mais ont pris des routes différentes depuis
> - OPNsense reste 100% open source avec une Business Edition optionnelle, pfSense se partage entre l'édition CE communautaire et pfSense Plus
> - Les deux tournent sur un mini PC avec 4 Go de RAM : le vrai choix se fait sur l'interface, le rythme des mises à jour et ce que tu veux bricoler

## OPNsense vs pfSense : le match des pare-feux open source pour ton homelab

Chez moi, la question du pare-feu homelab, je me la suis posée trois fois en cinq ans. Changer de box opérateur, segmenter mon VLAN IoT, puis migrer vers un mini PC dédié. Chaque fois, le match OPNsense vs pfSense revenait sur la table, et chaque fois j'ai fini par retester les deux avant de trancher.

Les deux projets sortent du même arbre généalogique : m0n0wall, abandonné en 2015, a donné pfSense côté Netgate et OPNsense côté Deciso, une entreprise néerlandaise qui a forké le projet en 2014 pour en garder le code ouvert. Depuis, les deux ont évolué séparément, avec des choix d'interface, de licence et de rythme de développement assez différents pour que le choix ne soit plus juste une question de goût.

Si tu montes un homelab en 2026 et que tu veux remplacer la box de ton FAI par un vrai pare-feu, voici ce que j'ai retenu des deux côtés, sans parti pris de fanboy.

## Table des matières

## Installation et configuration matérielle

Niveau matériel, OPNsense vs pfSense se jouent quasiment à égalité. OPNsense annonce officiellement un minimum d'un CPU dual-core à 1 GHz et 4 Go de RAM, avec un SSD recommandé plutôt qu'une carte SD pour l'usage quotidien. Pour une VM, compte un cœur, 4 Go de RAM et un disque virtuel d'au moins 8 Go. pfSense vise des besoins comparables : les deux tournent très bien sur un mini PC fanless avec deux ports réseau, le genre de boîtier qu'on trouve d'occasion pour une trentaine d'euros.

L'installation se fait dans les deux cas depuis une clé USB ou une image ISO, avec un assistant texte au premier démarrage qui te demande tes interfaces WAN et LAN. Rien de sorcier, mais prévois un deuxième poste pour suivre la doc pendant l'install. Les deux projets gardent une console en ligne de commande assez austère tant que le réseau n'est pas configuré.

Si ton matériel est vraiment limité, un boîtier embarqué ou un vieux routeur grand public, l'alternative à regarder c'est [OpenWrt firmware](/openwrt-firmware-routeur-homelab/) : plus léger, pensé pour tourner sur des routeurs existants, mais avec moins de fonctionnalités pare-feu avancées qu'OPNsense ou pfSense. Pour une vraie segmentation réseau avec VLAN et règles fines, les deux poids lourds de ce comparatif restent au-dessus.

## Interface et courbe d'apprentissage

C'est là que le match OPNsense vs pfSense se décide le plus souvent. L'interface d'OPNsense a été retravaillée plusieurs fois : menu latéral clair, dashboard personnalisable en widgets, thème sombre natif. pfSense garde une interface plus datée dans l'esprit, des onglets denses, mais qui reste lisible une fois qu'on connaît l'emplacement des menus.

Côté courbe d'apprentissage, aucun des deux n'est vraiment débutant-friendly. Tu dois comprendre les concepts de base : interfaces, règles de pare-feu évaluées dans l'ordre, NAT, alias. Une fois ces notions en tête, la bascule d'un projet à l'autre est rapide, les deux utilisent le même vocabulaire réseau hérité de pf (le pare-feu d'OpenBSD) et de FreeBSD.

Un détail qui compte au quotidien : OPNsense propose un historique de configuration avec rollback en un clic, pratique quand tu casses une règle à 23h un dimanche soir. pfSense a aussi un système de sauvegarde de config, mais moins intégré à l'interface courante.

Sur la doc, les deux s'en sortent bien. docs.opnsense.org est fourni et à jour, le forum Netgate pour pfSense est actif mais plus orienté support commercial que tutoriels pas à pas.

## VPN, DNS et fonctionnalités réseau

Sur la partie VPN, OPNsense vs pfSense proposent globalement le même catalogue : OpenVPN, IPsec, et WireGuard, soit en natif soit via un plugin officiel. Les deux gèrent aussi le multi-WAN, le load balancing et les VLAN sans limite artificielle côté logiciel, uniquement selon ta carte réseau.

Pour la résolution DNS, les deux embarquent Unbound comme résolveur récursif, avec la possibilité de forcer tout le trafic DNS du réseau à passer par le pare-feu. C'est l'endroit idéal pour bloquer les requêtes sortantes vers des résolveurs tiers, et pour brancher un Pi-hole derrière en DNS secondaire. Si tu fais tourner plusieurs instances de Pi-hole pour la redondance, [Nebula-Sync](/nebula-sync-pihole-v6-installation-docker-guide/) te synchronise les listes et les réglages sans y repenser à chaque mise à jour.

Pour le VPN d'accès distant au homelab, les deux savent monter un tunnel site-à-site ou road warrior sans problème. Mais si ton besoin c'est juste relier tes machines entre elles sans gérer de certificats ni de ports à ouvrir, une alternative plus légère existe en complément du pare-feu : [Headscale](/headscale-docker-tailscale-self-hosted/), le serveur Tailscale auto-hébergé, qui fait un mesh VPN en quelques minutes et complète très bien un OPNsense ou un pfSense déjà en place pour le filtrage périmétrique.

Côté IDS/IPS, les deux intègrent Suricata en option, avec des règles communautaires gratuites. Activer l'inspection profonde de paquets sur tout le trafic a un coût CPU réel : sur du matériel modeste, limite-la aux interfaces qui en ont vraiment besoin.

## Licence, prix et éditions : qui reste vraiment gratuit

Niveau licence, OPNsense vs pfSense ne jouent plus dans la même catégorie. OPNsense reste sous licence BSD/MIT à deux clauses, intégralement open source, publié par [opnsense.org](https://opnsense.org/) et développé par Deciso aux Pays-Bas. Une Business Edition ajoute des fonctionnalités pro (support, image de virtualisation officielle), sans prix public affiché sur le site, mais le cœur du produit reste gratuit et le code reste consultable.

pfSense, publié par Netgate sur [pfsense.org](https://www.pfsense.org/), se partage en deux éditions. pfSense CE (Community Edition) reste open source et gratuite, mais les correctifs de sécurité et les nouvelles versions y arrivent après pfSense Plus, et plusieurs utilisateurs du forum Netgate remarquent que l'accès public aux sources de développement de CE s'est resserré ces dernières années. pfSense Plus est gratuite pour un usage personnel sur ton propre matériel, mais les images cloud officielles pour AWS et Azure sont facturées à l'heure, à partir de 0,08 dollar selon le site officiel.

Pour un homelab perso qui tourne sur du matériel que tu possèdes déjà, ni l'un ni l'autre ne te coûte un centime à l'installation. La vraie différence se voit sur la durée : OPNsense garde un rythme de publication régulier et entièrement transparent, pendant que l'avenir de pfSense CE dépend des choix de Netgate, qui pousse plutôt vers Plus et son matériel maison.

## Cas d'usage homelab : mon verdict OPNsense vs pfSense

Après avoir fait tourner les deux chez moi pendant plusieurs mois chacun, voici où je mets le curseur. Si tu démarres un homelab et que tu veux une interface agréable, une doc à jour et la certitude que le projet reste ouvert sur la durée, pars sur OPNsense. C'est mon choix actuel sur le pare-feu qui protège mon réseau IoT et mon VLAN invités.

Si tu as déjà un pfSense existant qui tourne bien, ou que tu comptes investir dans du matériel Netgate avec support officiel derrière, pfSense Plus reste un choix cohérent. C'est aussi le cas si ta boîte utilise déjà du matériel Netgate au bureau et que tu veux la même logique à la maison.

Une fois ton pare-feu choisi, la suite logique c'est de vérifier que ta segmentation réseau ne plombe pas le débit. [Iperf3](/iperf3-tester-debit-reseau-homelab/) te donne en deux commandes le débit réel entre deux machines, avant et après avoir activé tes règles de filtrage ou ton IDS. Si tu perds une bonne partie du débit entre deux VLAN sur le même switch, le coupable c'est presque toujours une règle mal placée ou Suricata en mode trop gourmand.

Dernier point pratique : si tu veux exposer un service depuis ton homelab sans ouvrir le moindre port sur ton pare-feu, que ce soit OPNsense ou pfSense, regarde [Cloudflare Tunnel](/cloudflare-tunnel-docker-homelab/). Tu gardes ton pare-feu fermé à double tour côté WAN, et le tunnel sortant s'occupe du reste. Les deux approches sont complémentaires, pas concurrentes : le pare-feu segmente ton réseau interne, le tunnel expose uniquement ce que tu décides d'exposer.

Au final, le match OPNsense vs pfSense se gagne moins sur les fonctionnalités, très proches des deux côtés, que sur la philosophie du projet et ce que tu es prêt à accepter côté licence.

## FAQ rapide

**OPNsense ou pfSense, lequel tourne le mieux sur du matériel recyclé ?**
Les deux fonctionnent avec un CPU dual-core 1 GHz et 4 Go de RAM selon la doc officielle d'OPNsense. Un mini PC ou un boîtier fanless suffit largement pour un trafic domestique.

**Peut-on migrer une configuration pfSense vers OPNsense sans tout refaire ?**
Non, il n'existe pas d'import direct. Les deux partagent un héritage FreeBSD et m0n0wall, mais les formats de configuration ont divergé. Compte sur une reconfiguration manuelle, interface par interface.

**OPNsense et pfSense sont-ils vraiment gratuits pour un homelab ?**
Oui dans les deux cas pour un usage personnel sur ton propre matériel. OPNsense reste open source avec une Business Edition optionnelle payante, pfSense se partage entre l'édition CE communautaire et pfSense Plus, facturée à l'heure sur les images cloud officielles.

## Conclusion

OPNsense vs pfSense, c'est au final un choix entre deux héritiers du même projet qui ont pris des chemins différents. OPNsense mise sur une interface moderne, une transparence totale et un rythme de développement régulier. pfSense mise sur sa base d'utilisateurs historique, son écosystème matériel Netgate, et une édition Plus pensée pour le pro autant que pour le homelab.

Les deux sont largement suffisants pour sécuriser un réseau domestique ou un petit lab, et les deux savent faire du VLAN, du VPN et de l'IDS sans broncher sur un mini PC d'occasion. Teste les deux sur une VM avant de migrer ton réseau de production, tu sauras en une soirée lequel te correspond.
