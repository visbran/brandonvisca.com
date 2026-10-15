---
title: "Iperf3 : mesurer le débit réel de ton réseau homelab"
description: "Iperf3 teste le débit réel entre deux machines du homelab : installation, mode serveur/client, UDP, Docker et lecture des résultats."
pubDatetime: "2026-10-15T11:01:11+02:00"
modDatetime: "2026-10-14T08:00:00.000Z"
author: Brandon Visca
tags:
  - reseau
  - vpn
  - tailscale
  - intermediaire
featured: false
draft: false
focusKeyword: iperf3
faqs:
  - question: "Quel port iperf3 utilise-t-il et faut-il l'ouvrir sur le firewall ?"
    answer: "Le port par défaut est 5201, en TCP et en UDP. Sur un LAN interne, inutile d'ouvrir quoi que ce soit côté WAN : ouvre juste le port entre les deux machines concernées si un firewall local filtre déjà le trafic."
  - question: "iperf3 donne un chiffre différent de mon test Speedtest, c'est normal ?"
    answer: "Oui. Speedtest mesure ta connexion internet via un serveur distant et beaucoup d'overhead HTTPS. iperf3 mesure le débit brut entre deux machines précises, souvent sur ton LAN, donc les deux chiffres ne répondent pas à la même question."
  - question: "Peut-on tester le débit d'un tunnel VPN avec iperf3 ?"
    answer: "Oui, c'est l'un des usages les plus utiles. Lance le serveur iperf3 derrière le VPN et le client à travers le tunnel : tu obtiens le débit réel une fois le chiffrement et l'encapsulation pris en compte, pas le débit théorique de la ligne."
---
> 💡 **TL;DR**
> - Iperf3 mesure le débit réel entre deux machines, en TCP ou UDP, sans dépendre d'un service tiers comme Speedtest
> - Mode serveur sur une machine (`iperf3 -s`), mode client sur l'autre (`iperf3 -c IP`), résultat en quelques secondes
> - Utile pour valider un lien WiFi, un VPN Tailscale ou Headscale, ou un switch qui ne tient pas la charge annoncée

Tu viens de poser un switch 2.5 Gb/s dans ton homelab et tu veux savoir si le câble tient vraiment la promesse. Ou alors ton transfert vers le NAS plafonne à 40 Mo/s et tu cherches si le problème vient du réseau ou du disque. Dans les deux cas, un copier-coller de fichier te donne un chiffre pollué par le disque, le système de fichiers et le cache. iperf3 retire tout ça et mesure uniquement le tuyau réseau entre deux machines.

## Table des matières

## Qu'est-ce qu'iperf3 exactement

iperf3 est un outil en ligne de commande développé par ESnet et le Lawrence Berkeley National Laboratory, publié sous licence BSD à trois clauses. Le site officiel est [software.es.net/iperf](https://software.es.net/iperf), le code source vit sur [GitHub chez esnet/iperf](https://github.com/esnet/iperf). Dernière version stable au moment où j'écris : 3.22, sortie fin septembre 2026.

iperf3 fonctionne toujours en duo : une machine joue le serveur et attend une connexion, une autre joue le client et envoie du trafic généré pour saturer le lien. Le résultat donne un débit en bits par seconde, dans le sens que tu choisis, sans toucher au disque ni passer par un service web externe.

Chez moi, c'est le premier outil que je lance dès qu'un transfert me semble lent. Il répond en quelques secondes à la seule question qui compte : le réseau est-il le coupable, oui ou non.

## Installer iperf3 sur Linux, macOS et Windows

Sur la quasi-totalité des distributions, iperf3 est packagé et à jour :

```bash
# Debian, Ubuntu
sudo apt install iperf3

# Fedora, RHEL, Rocky
sudo dnf install iperf3

# Arch Linux
sudo pacman -S iperf3
```

Sur macOS, le paquet passe par Homebrew :

```bash
brew install iperf3
```

Sur Windows, iperf3 n'a pas de build officiel de l'équipe ESnet : les binaires circulent via des mainteneurs tiers. Le plus simple reste souvent une VM Linux ou WSL2, qui donne accès à la même commande que sur un vrai serveur Linux.

Si tu préfères éviter d'installer un paquet supplémentaire sur une machine, l'image Docker `networkstatic/iperf3` fait le travail sans rien persister sur l'hôte.

## Lancer un premier test iperf3 entre deux machines

Sur la machine qui va recevoir le trafic, démarre le serveur :

```bash
iperf3 -s
```

iperf3 écoute sur le port 5201 par défaut et affiche chaque connexion entrante dans le terminal. Laisse cette fenêtre ouverte.

Sur la seconde machine, lance le client en pointant vers l'IP du serveur :

```bash
iperf3 -c 192.168.1.50
```

Après dix secondes de test par défaut, tu obtiens un résumé avec le débit moyen mesuré, dans les deux colonnes "sender" et "receiver". Sur un lien gigabit propre, attends-toi à voir un chiffre proche de 940 Mbits/sec : le gigabit théorique ne tient jamais compte de l'overhead Ethernet et TCP.

💡 Ajoute `-t 30` pour allonger le test à 30 secondes si tu veux lisser les variations, utile sur du WiFi où le débit bouge beaucoup seconde par seconde.

## Tester en UDP et dans les deux sens

Le mode par défaut d'iperf3 teste en TCP, qui ralentit dès qu'un paquet se perd pour attendre un accusé de réception. Pour voir le débit brut sans ce frein, bascule en UDP :

```bash
iperf3 -c 192.168.1.50 -u -b 1G
```

Le `-b 1G` fixe le débit cible que le client va tenter d'envoyer : en UDP, iperf3 ne ralentit pas automatiquement, donc sans cette limite tu risques de saturer le lien et de perdre des paquets juste pour voir le chiffre monter artificiellement. Le rapport final en UDP indique en plus le pourcentage de perte de paquets et le jitter, deux infos absentes du mode TCP.

Pour tester le sens inverse, du serveur vers le client, ajoute `-R` (reverse) :

```bash
iperf3 -c 192.168.1.50 -R
```

Utile sur une connexion asymétrique, ou pour vérifier qu'une carte réseau encaisse aussi bien en émission qu'en réception.

⚠️ Sur une liaison WiFi, lance toujours le test dans les deux sens. J'ai déjà eu un adaptateur USB qui tenait 300 Mbits/sec en réception et s'effondrait à 80 en émission, un défaut que seul le mode `-R` révèle.

## Utiliser iperf3 en conteneur Docker

Si tu ne veux pas polluer un hôte avec un paquet de plus, l'image `networkstatic/iperf3` évite l'installation. Côté serveur :

```bash
docker run -d --name iperf3-server --restart unless-stopped -p 5201:5201/tcp -p 5201:5201/udp networkstatic/iperf3 -s
```

Côté client, cible l'IP de l'hôte qui porte le conteneur serveur :

```bash
docker run --rm networkstatic/iperf3 -c 192.168.1.50
```

Pratique pour tester le débit réel entre deux hôtes Proxmox ou deux VM, sans installer quoi que ce soit en dur sur le système hôte. Le conteneur se supprime tout seul une fois le test client terminé grâce à `--rm`.

## Mesurer le débit à travers un VPN ou un tunnel

C'est l'usage qui revient le plus souvent chez les gens qui gèrent un homelab accessible de l'extérieur. Un [tunnel Tailscale ou Headscale auto-hébergé](/headscale-docker-tailscale-self-hosted/) ajoute du chiffrement et de l'encapsulation, donc le débit réel chute toujours un peu par rapport au débit brut de la ligne.

La méthode : lance le serveur iperf3 sur la machine distante, à l'intérieur du tunnel, puis le client en ciblant l'IP virtuelle attribuée par le VPN plutôt que l'IP LAN classique.

```bash
iperf3 -c 100.64.0.5
```

Si le résultat est nettement plus bas que le débit mesuré en direct sur le LAN, le chiffrement ou le routage du tunnel devient le facteur limitant, pas ta connexion internet. Le même réflexe marche pour vérifier un conteneur qui sort par un [VPN comme Gluetun](/gluetun-docker-vpn-conteneurs/) : tu compares le débit obtenu depuis le conteneur routé avec celui obtenu en direct depuis l'hôte, et l'écart te dit combien le VPN te coûte réellement en performance.

## Diagnostiquer un routeur ou un switch sous-performant

Un routeur [OpenWrt](/openwrt-firmware-routeur-homelab/) ou un boîtier [pfSense](/mise-a-jour-pfsense-2-8-nouveautes-installation/) annonce souvent un débit théorique sur sa fiche produit qui ne correspond à rien en usage réel, surtout si le routage passe par du NAT ou un pare-feu avec inspection profonde activée.

Place un serveur iperf3 d'un côté du routeur, un client de l'autre, et compare avec un test fait directement entre les deux machines reliées par un câble, sans passer par le routeur. Si l'écart dépasse 10 à 15 %, le routeur limite réellement le débit, souvent parce que le CPU sature sur le NAT ou sur des règles de pare-feu trop lourdes.

✅ Fais ce test avant et après chaque changement de configuration réseau notable (nouvelle règle de pare-feu, QoS activée, VLAN ajouté). C'est le seul moyen de savoir si un changement a vraiment un coût, plutôt que de le supposer.

## Lire et interpréter les résultats iperf3

Un rapport iperf3 typique ressemble à ceci :

```
[ ID] Interval           Transfer     Bitrate
[  5]   0.00-10.00  sec  1.09 GBytes   940 Mbits/sec                  sender
[  5]   0.00-10.00  sec  1.09 GBytes   937 Mbits/sec                  receiver
```

La ligne "sender" donne ce que la machine émettrice a réellement poussé, la ligne "receiver" ce que l'autre bout a effectivement reçu. Un écart important entre les deux signale une perte de paquets ou de la retransmission TCP, à creuser côté câblage ou côté carte réseau avant de blâmer le switch.

En UDP, cherche en plus la ligne "Jitter" et le pourcentage de perte : au-delà de 1 à 2 % de perte, de la visioconférence ou un flux audio en souffrira, même si le débit affiché paraît correct.

## Dépannage courant avec iperf3

**Le client n'arrive pas à se connecter.** Vérifie que le serveur iperf3 tourne toujours, et qu'aucun firewall local ne bloque le port 5201 entre les deux machines. Un `telnet IP_SERVEUR 5201` rapide confirme si le port répond avant même de relancer iperf3.

**Le débit mesuré chute fortement au fil du test.** Signe fréquent d'un câble réseau abîmé ou d'une carte qui chauffe et renégocie sa vitesse de liaison. Vérifie la vitesse négociée côté switch avant de remettre en cause iperf3 lui-même.

**Le résultat en UDP affiche 0 % de perte mais un débit ridicule.** Le `-b` est probablement réglé trop bas. En UDP, iperf3 n'essaie jamais de dépasser le débit cible que tu lui donnes : relance avec une valeur plus proche du débit réel attendu sur ce lien.

## Conclusion

iperf3 règle en deux commandes une question qui prend souvent des heures à trancher à tâtons : le réseau est-il vraiment le problème. Mode serveur d'un côté, mode client de l'autre, et un chiffre fiable en quelques secondes, sans dépendre d'un service en ligne ni d'un transfert de fichier pollué par le disque.

La prochaine fois qu'un transfert te semble lent dans ton homelab, avant de changer de câble ou de réinstaller un pilote, lance iperf3 des deux côtés du doute. Tu sauras en moins d'une minute si c'est le réseau, ou autre chose.
