---
title: "NetworkManager CLI : configurer le réseau comme un pro"
description: "Maîtrise NetworkManager CLI (nmcli) pour configurer ton réseau Linux : connexions, Wi-Fi, bonding, DNS, sans passer par une interface graphique."
pubDatetime: "2026-10-25T11:02:12+01:00"
modDatetime: "2026-10-24T08:00:00.000Z"
author: Brandon
tags:
  - linux
  - dns
  - terminal
  - intermediaire
featured: false
draft: false
focusKeyword: networkmanager cli
faqs:
  - question: "Nmcli peut-il tout faire sans toucher aux fichiers de NetworkManager ?"
    answer: "Oui, nmcli pilote directement le démon NetworkManager via D-Bus et écrit lui-même les profils de connexion. Tu n'as jamais besoin d'éditer un fichier à la main, sauf pour du dépannage fin."
  - question: "Que se passe-t-il si Netplan et NetworkManager gèrent la même interface ?"
    answer: "Les deux vont se disputer la configuration : adresses qui changent, DNS écrasé, comportements difficiles à reproduire. Laisse toujours une interface donnée à un seul gestionnaire."
  - question: "NetworkManager consomme-t-il des ressources sur un serveur sans interface graphique ?"
    answer: "Non, c'est un démon léger pensé pour tourner aussi bien sur un serveur headless que sur un poste de bureau. L'empreinte mémoire reste minime face à ce qu'il automatise."
---
> 💡 **TL;DR**
> - NetworkManager CLI (nmcli) pilote connexions, Wi-Fi et DNS depuis le terminal, sans dépendre d'une interface graphique
> - Syntaxe par objets (`general`, `device`, `connection`) : tu listes, tu ajoutes, tu modifies, tu actives
> - Coexiste avec Netplan sur Ubuntu : comprendre qui pilote quoi évite les conflits DNS et IP qui changent tout seuls

## NetworkManager CLI : piloter ton réseau Linux sans souris

T'as déjà configuré une IP statique à la main en éditant un fichier dont tu savais pas s'il serait relu au prochain boot ? Moi oui, et c'est le genre de moment où tu te dis qu'il doit exister mieux. La réponse s'appelle NetworkManager CLI, plus connu sous son nom de commande, `nmcli`.

NetworkManager est le gestionnaire réseau standard sous Linux, maintenu dans le projet freedesktop.org. Il tourne en démon, parle D-Bus, et sert de couche d'abstraction entre toi et les interfaces réseau du noyau. Sur Fedora et RHEL, c'est l'outil par défaut depuis longtemps. Sur Ubuntu Desktop, il a aussi pris cette place. Sur Ubuntu Server et Debian, c'est souvent systemd-networkd piloté par Netplan qui fait le travail, NetworkManager restant disponible en option. Bref, tu le croises partout, sous une forme ou une autre.

Le truc, c'est que la plupart des tutos te montrent l'interface graphique. Chez moi, sur un serveur sans bureau, ça ne sert à rien. `nmcli` fait tout ce que fait l'interface graphique, en scriptable, en reproductible, et sans jamais lâcher le terminal.

## Table des matières

## Les bases de NetworkManager CLI : objets et commandes

`nmcli` s'organise autour d'objets. Chaque commande commence par l'un d'eux, et c'est ce qui rend la syntaxe prévisible une fois que tu l'as en tête :

- `general` : état global du démon, nom d'hôte, connectivité
- `networking` : activation ou coupure complète du réseau
- `device` : les interfaces physiques ou virtuelles (eth0, wlan0, docker0...)
- `connection` : les profils de configuration, qu'ils soient actifs ou pas
- `radio` : l'état Wi-Fi ou WWAN au niveau matériel

Pour voir où tu en es, deux commandes suffisent au quotidien :

```bash
nmcli general status
nmcli device status
```

La première te donne la connectivité globale et si le démon tourne. La seconde liste chaque interface avec son état (`connected`, `disconnected`, `unmanaged`) et le profil actif associé. C'est souvent la première chose que je tape en me connectant à un serveur que je ne connais pas encore.

Pour aller plus loin sur une interface précise :

```bash
nmcli device show eth0
nmcli connection show
nmcli connection show --active
```

`device show` déballe tout ce que NetworkManager sait sur cette carte : IP, passerelle, DNS, MAC, vitesse du lien. `connection show` liste tous les profils enregistrés, actifs ou non, alors que `--active` ne garde que ceux réellement appliqués. La distinction compte : un profil peut exister sans jamais avoir été activé.

Petit bonus pour les scripts : ajoute `-t` (terse) pour un format sans en-tête ni alignement, pensé pour être parsé par `awk` ou `cut`. `-p` fait l'inverse et rend la sortie plus lisible pour un humain.

## Configurer une IP statique avec nmcli

Passons au vrai sujet : fixer une IP sans toucher un fichier à la main. On crée un profil dédié plutôt que de modifier celui qui existe, ça garde une trace propre de ce que tu as changé et pourquoi :

```bash
nmcli connection add con-name lan-static ifname eth0 type ethernet \
  ipv4.method manual ipv4.addresses 192.168.1.50/24 \
  ipv4.gateway 192.168.1.1 ipv4.dns "1.1.1.1 9.9.9.9"
```

Chaque paire `clé valeur` configure un attribut du profil. `ipv4.method manual` indique qu'on ne veut pas de DHCP, `ipv4.addresses` prend l'IP au format CIDR, et `ipv4.dns` accepte une liste de résolveurs séparés par un espace, entre guillemets.

Le profil est créé mais pas forcément actif. Pour l'appliquer :

```bash
nmcli connection up lan-static
```

Si tu dois ajuster un paramètre plus tard, pas besoin de tout recréer :

```bash
nmcli connection modify lan-static ipv4.addresses 192.168.1.60/24
nmcli connection up lan-static
```

`modify` change le profil enregistré, mais ne touche pas la connexion en cours tant que tu ne refais pas `up` (ou `nmcli connection reload` suivi d'un redémarrage de l'interface). C'est voulu : ça évite qu'une faute de frappe te coupe l'accès SSH en plein milieu d'une modification. Si tu bosses à distance, teste toujours sur une session que tu peux rouvrir, ou garde un accès console de secours.

## DHCP, Wi-Fi et connexions multiples

Revenir en DHCP, c'est la commande inverse de ce qu'on vient de faire :

```bash
nmcli connection modify lan-static ipv4.method auto
nmcli connection up lan-static
```

Pour le Wi-Fi, NetworkManager CLI gère la découverte et la connexion sans jamais sortir du terminal :

```bash
nmcli device wifi list
nmcli device wifi connect "MonReseau" password "motdepasse"
```

La commande `connect` crée automatiquement un profil nommé d'après le SSID. Tu peux ensuite le retrouver avec `connection show` et le modifier comme n'importe quel autre, par exemple pour forcer une IP fixe sur un réseau Wi-Fi au lieu du DHCP par défaut.

Sur une machine avec plusieurs interfaces (un serveur avec deux cartes réseau, une pour le LAN et une pour une DMZ par exemple), NetworkManager CLI te laisse garder plusieurs profils et jouer sur la priorité :

```bash
nmcli connection modify lan-static connection.autoconnect yes
nmcli connection modify lan-static connection.autoconnect-priority 10
```

Plus la priorité est élevée, plus tôt NetworkManager tentera d'activer ce profil au démarrage. Pratique quand une interface doit systématiquement passer avant l'autre, typiquement l'interface de management sur un hyperviseur.

## NetworkManager vs Netplan : qui pilote quoi

Sur Ubuntu, la question revient souvent : est-ce que je configure via `nmcli` ou via Netplan ? La réponse dépend de qui a la main sur l'interface. Netplan est une couche de configuration déclarative qui génère la config d'un backend, soit `systemd-networkd`, soit NetworkManager lui-même. Si tu as un doute sur la syntaxe YAML de ce côté, j'ai détaillé tout ça dans [Netplan Linux : configurer le réseau en YAML simplement](/netplan-linux-configurer-reseau-yaml/).

Le piège classique : modifier une interface avec `nmcli` alors qu'elle est aussi déclarée dans un fichier Netplan avec `renderer: networkd`. Les deux gestionnaires se marchent sur les pieds, l'IP change toute seule au redémarrage, le DNS repart sur l'ancienne valeur. La règle à retenir est simple : une interface, un seul gestionnaire. Si Netplan déclare `renderer: NetworkManager`, alors `nmcli` est légitime. Sinon, laisse Netplan tranquille et édite le YAML.

Si le terminal n'est vraiment pas ta tasse de thé pour ce genre de réglages, sache qu'il existe une alternative web complète qui expose les mêmes réglages dans un navigateur : j'en parle dans [Cockpit Docker : interface web d'administration Linux moderne](/cockpit-docker-interface-web-administration/). C'est souvent un bon compromis pour une équipe qui ne veut pas former tout le monde au CLI.

## Dépannage : logs, service et erreurs fréquentes

Quand une connexion refuse de monter sous NetworkManager CLI, commence toujours par le service lui-même :

```bash
systemctl status NetworkManager
journalctl -u NetworkManager -n 50 --no-pager
```

Le journal donne presque toujours la raison exacte : conflit d'adresse, échec DHCP, interface marquée `unmanaged` parce qu'un autre outil la gère déjà. Cette dernière cause est fréquente sur les machines qui ont un fichier dans `/etc/network/interfaces` ou une règle udev héritée d'une ancienne installation.

Un profil qui existe mais refuse de s'activer mérite un œil sur son état détaillé :

```bash
nmcli -f GENERAL.STATE connection show lan-static
nmcli device show eth0 | grep -i state
```

Dans les cas les plus coincés, redémarrer juste le service suffit à repartir sur une base saine, sans toucher à la config :

```bash
sudo systemctl restart NetworkManager
```

Un peu comme quand tu dépannes un montage RAID qui refuse de se remonter en mode de secours, la méthode est la même : lire le journal avant de toucher à quoi que ce soit, isoler la couche fautive, et ne corriger qu'elle. Si ce genre de diagnostic par étapes t'intéresse côté stockage, j'ai un cas détaillé dans [Dépannage des problèmes de montage de matrices RAID (mdadm) en mode de secours Linux](/depannage-montage-partition-raid-linux-mode-secours/).

Enfin, si après toute modification rien ne semble pris en compte, vérifie que le profil est bien marqué pour démarrer automatiquement (`connection.autoconnect yes`) et que l'interface n'est pas en `unmanaged` dans `nmcli device status`. Ces deux oublis expliquent la majorité des "ça marche pas" après un `up` qui a pourtant renvoyé un succès.

## Cas concrets pour ton homelab

Sur mon homelab, NetworkManager CLI me sert surtout pour des VMs et des conteneurs qui ont besoin d'une IP fixe prévisible, sans dépendre d'un bail DHCP qui peut changer après un redémarrage du routeur. Un serveur qui héberge un service NTP en est un bon exemple : si son adresse bouge, tous les clients qui pointent vers lui perdent la synchro. J'ai justement un serveur monté avec Chrony pour ce rôle, détaillé dans [Chrony Docker : serveur NTP précis pour ton homelab](/chrony-docker-serveur-ntp-homelab/), et son IP est fixée exactement comme montré plus haut.

Autre cas fréquent : une VM avec deux interfaces, une pour le trafic normal et une dédiée à l'administration, branchée sur un VLAN séparé derrière un routeur OpenWrt. Si ton router tourne sous ce firmware, c'est côté routeur que tu gères les VLAN et le DHCP, et côté machine que `nmcli` prend le relais pour fixer l'IP sur la bonne interface. J'en parle dans [OpenWrt firmware : le routeur open-source pour ton homelab](/openwrt-firmware-routeur-homelab/), qui complète bien ce qu'on vient de voir ici.

Dernier conseil pratique : documente tes profils `nmcli` quelque part en dehors de la machine. `nmcli connection show` te dira ce qui existe, mais pas pourquoi tu l'as configuré ainsi. Un simple fichier texte avec la commande exacte utilisée pour chaque serveur t'évite de redevenir archéologue le jour où tu dois reconstruire une VM à l'identique.

## Conclusion

NetworkManager CLI n'est pas plus compliqué que l'interface graphique, juste plus direct. Une fois que tu as intégré la logique objet-puis-action (`device`, `connection`, `general`), la plupart des tâches réseau se résument à deux ou trois commandes copiables d'un serveur à l'autre. Teste les commandes de ce guide sur une VM avant de les rejouer en prod, garde toujours un accès console de secours quand tu touches une interface à distance, et vérifie qui gère réellement l'interface avant de la modifier si Netplan est dans la boucle. Le reste, c'est de la pratique.
