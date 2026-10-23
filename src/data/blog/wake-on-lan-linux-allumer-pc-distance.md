---
title: "Wake-on-LAN Linux : allumer tes machines à distance"
description: Configure le Wake-on-LAN Linux avec ethtool, systemd et NetworkManager pour allumer un PC ou un serveur sans bouger du canapé.
pubDatetime: "2026-10-23T11:02:11+02:00"
modDatetime: "2026-10-22T08:00:00.000Z"
author: Brandon
tags:
  - linux
  - ssh
  - automation
  - intermediaire
featured: false
draft: false
focusKeyword: wake-on-lan linux
faqs:
  - question: "Le Wake-on-LAN marche-t-il après un arrêt complet, pas juste en veille ?"
    answer: "Oui si l'alimentation reste en mode veille électrique (ACPI S5) et que l'option ErP/EuP du BIOS est désactivée. Avec ErP activé, la carte réseau est coupée à l'arrêt et aucun magic packet ne peut la réveiller."
  - question: "Le Wake-on-LAN fonctionne-t-il en Wi-Fi ?"
    answer: "Rarement et mal. Le standard vise l'Ethernet filaire. L'équivalent Wi-Fi (WoWLAN) existe sur certaines puces mais le support Linux est inégal, mieux vaut un câble sur la machine à réveiller."
  - question: "Peut-on réveiller un PC depuis internet, hors du réseau local ?"
    answer: "Le magic packet est un broadcast local, il ne traverse pas internet tel quel. Il faut soit un VPN (Tailscale, WireGuard) qui te ramène sur le LAN, soit une redirection de port UDP vers l'adresse de broadcast du sous-réseau."
---
> 💡 **TL;DR**
> - Le Wake-on-LAN Linux repose sur un magic packet UDP envoyé à l'adresse MAC de la carte réseau : `ethtool -s eth0 wol g` l'active, `wakeonlan` ou `etherwake` l'envoie
> - Le réglage ne survit pas toujours à un reboot : un service systemd ou `nmcli ethernet.wake-on-lan magic` le rend permanent
> - Pour réveiller une machine hors du LAN, il faut un VPN (Tailscale, WireGuard) ou une redirection de port vers le broadcast du sous-réseau, jamais un simple port forward vers l'IP

## Wake-on-LAN Linux : réveiller une machine sans bouger du canapé

Tu as un NAS, un serveur de sauvegarde ou une tour de jeu qui dort la plupart du temps et que tu dois allumer deux fois par semaine. Trois solutions : te lever, laisser tourner 24/7 et payer l'électricité, ou envoyer un paquet réseau depuis ton canapé pour que la machine se réveille toute seule. La troisième, c'est le Wake-on-LAN.

Chez moi, c'est le serveur de sauvegarde qui reste éteint sauf pendant la fenêtre de sync nocturne. Un cron sur mon serveur principal envoie le magic packet, la machine boote, fait son travail, et un script d'extinction la rendort. Zéro intervention manuelle, zéro consommation inutile le reste du temps.

Le Wake-on-LAN Linux demande trois choses qui doivent toutes être vraies en même temps : la carte réseau doit supporter et avoir le WoL activé, le BIOS doit laisser l'alimentation en veille électrique, et un outil doit envoyer le bon paquet au bon moment. Si un seul des trois manque, rien ne se passe, et c'est souvent le plus énervant à diagnostiquer.

## Table des matières

## Comment fonctionne le Wake-on-LAN

Le principe du Wake-on-LAN Linux tient en une phrase : quand une machine est éteinte mais toujours alimentée, sa carte réseau reste sous tension réduite et écoute le trafic qui passe. Si elle reçoit un paquet spécifique contenant son adresse MAC répétée seize fois, précédée de six octets `FF`, elle déclenche l'allumage de la carte mère. Ce paquet s'appelle le magic packet, et c'est littéralement tout ce qu'il y a à savoir sur le protocole.

Ce magic packet voyage en UDP, en général sur le port 9 (parfois 7), et il est envoyé en broadcast sur le réseau local : pas besoin de connaître l'IP de la machine éteinte puisqu'elle n'en a justement pas tant qu'elle dort. Seule l'adresse MAC compte, ce qui veut dire qu'il faut la noter une fois pour toutes avant d'éteindre la machine (`ip link show` pendant qu'elle tourne encore).

Deux conditions matérielles, hors de portée de Linux :

- **L'alimentation doit rester en veille ACPI S5** (soft-off) et non coupée physiquement. Un onduleur ou une multiprise avec interrupteur mécanique en aval tue le Wake-on-LAN, logique.
- **L'option ErP/EuP du BIOS** (parfois nommée "Deep Sleep" ou "EuP 2013") doit être désactivée. Elle vise à réduire la conso en veille à quasi zéro en coupant aussi l'alimentation de la carte réseau, ce qui rend le réveil impossible par définition.

## Activer le Wake-on-LAN sur la carte réseau avec ethtool

Une fois le BIOS en ordre, la partie logicielle du Wake-on-LAN Linux commence par vérifier ce que la carte annonce supporter :

```bash
sudo ethtool eth0 | grep -A1 "Wake-on"
```

Tu dois voir une ligne `Supports Wake-on: ...` listant les lettres disponibles (`g` pour magic packet, `d` pour désactivé, etc.) et une ligne `Wake-on: d` si c'est actuellement coupé. Pour activer le magic packet :

```bash
sudo ethtool -s eth0 wol g
```

Remplace `eth0` par le nom réel de ton interface (`ip a` pour le retrouver, souvent `enpXsY` sur une install récente). Si `ethtool` répond que la carte ne supporte pas `g`, inutile d'aller plus loin ailleurs : c'est une limite matérielle ou du chipset, pas un réglage à chercher dans systemd.

> ⚠️ Ce réglage ne survit pas au reboot sur la plupart des distributions. Il revient à `d` à chaque démarrage tant que rien ne le réapplique automatiquement, c'est la cause numéro un de « ça marchait hier et plus aujourd'hui ».

## Rendre le réglage permanent

Deux façons de faire tenir le réglage du Wake-on-LAN Linux après un reboot, selon ce qui gère ton réseau.

**Avec systemd, un service oneshot** qui rejoue la commande à chaque boot :

```ini
# /etc/systemd/system/wol.service
[Unit]
Description=Active le Wake-on-LAN sur eth0
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/sbin/ethtool -s eth0 wol g

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now wol.service
```

**Avec NetworkManager**, pas besoin de service séparé, la propriété se porte directement sur la connexion :

```bash
nmcli connection show
nmcli connection modify "Wired connection 1" 802-3-ethernet.wake-on-lan magic
nmcli connection up "Wired connection 1"
```

La valeur `magic` correspond au mode `g` d'ethtool. `nmcli connection modify "Wired connection 1" 802-3-ethernet.wake-on-lan ignore` désactive le réglage si besoin. Si tu gères tes interfaces en YAML plutôt qu'avec NetworkManager, direction mon [guide Netplan](/netplan-linux-configurer-reseau-yaml/), l'activation du WoL s'y fait séparément via systemd puisque Netplan lui-même ne porte pas cette option.

Après reboot, vérifie que `ethtool eth0` affiche bien `Wake-on: g` et pas `Wake-on: d`. Si ça retombe à `d` malgré le service activé, un pilote ou un gestionnaire de power management (TLP, powertop) peut réécrire le réglage après coup : regarde dans leurs configs si une ligne `WOL_DISABLE` ou équivalent existe.

## Envoyer le magic packet : wakeonlan et etherwake

Côté machine qui envoie le réveil, le Wake-on-LAN Linux se résume à deux outils qui suffisent largement. Le plus simple, **`wakeonlan`**, un script packagé sur quasiment toutes les distributions :

```bash
sudo apt install wakeonlan   # Debian/Ubuntu
wakeonlan AA:BB:CC:DD:EE:FF
```

Il construit le magic packet et l'envoie en broadcast sur `255.255.255.255` par défaut. Si ton réseau est segmenté en VLAN ou que le broadcast global ne passe pas, précise l'adresse de broadcast du sous-réseau :

```bash
wakeonlan -i 192.168.1.255 AA:BB:CC:DD:EE:FF
```

L'autre option, **`etherwake`** (parfois listé comme `ether-wake` selon la distribution), cible directement une interface plutôt qu'une IP de broadcast, pratique sur une machine avec plusieurs cartes réseau :

```bash
sudo apt install etherwake
sudo etherwake -i eth0 AA:BB:CC:DD:EE:FF
```

Les deux font le même paquet au final, le choix est surtout une question d'habitude ou de ce qui est déjà packagé sur ta distribution. Pour automatiser le réveil quotidien d'un serveur de sauvegarde, un cron suffit :

```bash
# crontab -e
0 2 * * * /usr/bin/wakeonlan AA:BB:CC:DD:EE:FF
```

Petit détail qui mord : si ce cron tourne sur une machine dont l'heure dérive, le réveil arrive au mauvais moment par rapport au reste de ta chaîne de sauvegarde. Vaut le coup de vérifier que l'heure du serveur qui envoie le paquet est correctement synchronisée, voir mon [guide pour régler l'heure et le fuseau horaire sous Linux](/comment-modifier-heure-du-serveur-sous-linux/) si ce n'est pas déjà fait.

## Réveiller une machine depuis l'extérieur du réseau local

Le piège classique du Wake-on-LAN Linux utilisé à distance : le magic packet est un broadcast, et un broadcast ne sort jamais du réseau local. Rediriger le port UDP 9 de ta box vers l'IP de la machine éteinte ne fonctionnera jamais, puisque cette machine n'a pas d'IP active tant qu'elle dort, et qu'un paquet unicast ne la réveille pas de la même façon qu'un broadcast.

Deux approches qui marchent vraiment :

- **Rediriger vers l'adresse de broadcast du sous-réseau** (`192.168.1.255` par exemple) plutôt que vers une IP de machine. Certaines box et certains routeurs refusent ce type de règle pour des raisons de sécurité, à tester au cas par cas.
- **Passer par un VPN** qui te ramène virtuellement sur le LAN avant d'envoyer le paquet : Tailscale, WireGuard, ou même un simple accès SSH à une machine du réseau qui, elle, est allumée et peut relayer le `wakeonlan` localement.

En pratique, la deuxième option est plus fiable et plus simple à sécuriser. Un `ssh monserveur 'wakeonlan AA:BB:CC:DD:EE:FF'` depuis ton téléphone via Tailscale fait le même travail qu'une app dédiée, sans exposer un port UDP supplémentaire sur ta box.

> ✅ Si tu administres déjà tes serveurs à distance, [Cockpit](/cockpit-docker-interface-web-administration/) peut servir de point d'entrée web pour lancer ce genre de commande sans ouvrir un terminal SSH depuis un appareil qui n'en a pas toujours un sous la main.

## Dépannage : quand le Wake-on-LAN ne répond pas

Dans l'ordre, les causes les plus fréquentes de panne du Wake-on-LAN Linux :

- **Le BIOS a oublié le réglage.** Certaines cartes mères réinitialisent l'option ErP après une coupure de courant ou une mise à jour de firmware. Revérifie-la après chaque intervention physique sur la machine.
- **Le câble est branché sur le mauvais port.** Sur une carte mère avec deux interfaces réseau, seule celle supportée par le chipset principal gère souvent le WoL. L'autre, basée sur un contrôleur annexe, peut ne pas le supporter du tout.
- **Le switch coupe l'alimentation du port en absence de lien actif.** Rare, mais ça existe sur certains switchs administrables avec des profils d'économie d'énergie trop agressifs.
- **Le réglage `ethtool` est retombé à `d`.** Le symptôme classique : ça marchait, puis plus rien après un reboot ou une mise à jour du noyau. Relance la vérification `ethtool eth0 | grep Wake-on` et réapplique le service systemd si besoin.
- **Un pare-feu bloque le broadcast**, surtout si la machine qui envoie le paquet est sur un VLAN différent de celle qui doit se réveiller. Un magic packet ne traverse pas un routeur sans règle explicite.

Si rien de tout ça ne débloque la situation et que la machine héberge un volume RAID critique, pense à avoir sous la main de quoi [dépanner un montage RAID en mode secours](/depannage-montage-partition-raid-linux-mode-secours/) le jour où elle refuse carrément de démarrer, WoL ou pas.

## Conclusion

Le Wake-on-LAN Linux n'a rien de magique une fois qu'on a compris les trois étages : le BIOS qui doit laisser passer l'alimentation, `ethtool` qui active le mode `g` sur la carte, et un outil comme `wakeonlan` ou `etherwake` qui envoie le paquet au bon moment. Le vrai piège, c'est l'oubli du reboot : sans service systemd ou réglage NetworkManager permanent, le réglage saute et tu te retrouves à tout réexpliquer à ta carte réseau depuis le début.

Pour un homelab avec une machine qui dort la majorité du temps, c'est un gain réel : plus besoin de laisser un serveur tourner à vide pour la sauvegarde de 2h du matin, et plus besoin de te lever pour appuyer sur un bouton quand tu as juste besoin d'y accéder cinq minutes depuis l'extérieur.
