---
title: "Ubuntu Active Directory SSSD : intègre tes machines Linux en 5 étapes"
description: "Ubuntu Active Directory SSSD : installe, configure Kerberos et rejoins ton domaine en quelques commandes. Testé sur Ubuntu 22.04 et 24.04."
pubDatetime: "2024-06-13T11:40:02+02:00"
modDatetime: 2026-05-17 00:00:00+02:00
author: Brandon Visca
tags:
  - linux
  - sysadmin
  - avance
  - active-directory
  - ubuntu
  - guide
featured: false
draft: false
focusKeyword: Ubuntu Active Directory SSSD
faqs:
  - question: "Comment dépanner les problèmes de SSSD ?"
    answer: "Lance systemctl status sssd et journalctl -u sssd pour voir les erreurs. Les causes fréquentes : DNS mal pointé vers le DC, certificats Kerberos expirés, permissions sur sssd.conf (doit être 600)."
  - question: "Puis-je utiliser SSSD avec d'autres distributions Linux ?"
    answer: "Oui, SSSD fonctionne sur Debian, RedHat, CentOS, Rocky Linux. Les commandes d'installation diffèrent (dnf install sssd au lieu d'apt), la config SSSD reste identique."
  - question: "Comment créer automatiquement les répertoires personnels des utilisateurs AD ?"
    answer: "Active oddjob-mkhomedir avec pam-auth-update --enable mkhomedir. Le home dir est créé à la première connexion. Crée les répertoires parents manuellement si tu uses le format /home/%d/%u."
---
> 💡 **TL;DR** : Intègre Ubuntu à Active Directory via SSSD en 5 étapes : installe realmd + sssd-ad, configure le DNS vers ton DC, `realm join`, ajuste sssd.conf et krb5.conf, active mkhomedir. Authentification centralisée opérationnelle en 15 min.

Tu as un parc mixte Windows/Linux et tu veux que tes utilisateurs se connectent avec leurs credentials AD ? La combo **Ubuntu Active Directory SSSD** via realmd, c'est la solution standard. Ça s'intègre proprement avec Kerberos, ça gère le cache hors ligne, et ça évite de devoir maintenir des comptes locaux sur chaque machine.

J'ai déployé ça sur une quinzaine de postes Ubuntu 22.04 et 24.04 rejoignant un domaine Windows Server 2019. Voilà ce qui marche. Si ton AD n'est pas encore en place, commence par [transférer tes rôles FSMO](/activedirectory-transfere-des-roles-fsmo/) correctement avant d'intégrer des clients Linux.

## Table des matières

---

## Étape 1 — Installer les paquets

Installe les outils nécessaires :

```bash
sudo apt update
sudo apt install realmd sssd-ad sssd-tools libnss-sss libpam-sss adcli samba-common-bin oddjob oddjob-mkhomedir packagekit
```

- **realmd** → découverte et jonction au domaine
- **sssd-ad** → fournisseur AD pour SSSD
- **adcli** → opérations bas niveau sur AD
- **oddjob-mkhomedir** → création automatique des home dirs

Active SSSD au démarrage :

```bash
sudo systemctl enable sssd
sudo systemctl start sssd
```

---

## Étape 2 — Pointer le DNS vers ton contrôleur de domaine

SSSD a besoin de résoudre ton domaine AD. Pointe le DNS vers ton DC :

```bash
sudo nano /etc/resolv.conf
```

Ajoute :

```text
nameserver <IP_DE_TON_DC>
```

> ⚠️ **Attention** : `/etc/resolv.conf` peut être écrasé par NetworkManager ou systemd-resolved. Sur Ubuntu 22.04+, préfère configurer le DNS via `nmcli` ou l'interface réseau Netplan pour que le changement survive aux redémarrages.

Vérifie que tu résous bien le domaine :

```bash
sudo realm discover domain.tld
```

Tu dois voir les infos du domaine AD en retour.

---

## Étape 3 — Rejoindre le domaine

```bash
sudo realm join -v --user=Administrator domain.tld
```

`realm` crée automatiquement l'objet computer dans AD et génère un ticket Kerberos. Le `-v` affiche le détail si ça bloque.

---

## Étape 4 — Configurer SSSD

### sssd.conf

Sauvegarde la config générée par realm puis édite :

```bash
sudo cp /etc/sssd/sssd.conf /etc/sssd/sssd.conf.bak
sudo nano /etc/sssd/sssd.conf
```

> ⚠️ **Ne redémarre jamais SSSD avec une config cassée** : si sssd.conf est invalide, ton système ne pourra plus authentifier et tu devras passer par le mode recovery. Valide toujours avant de redémarrer.

Config de base :

```ini
[sssd]
config_file_version = 2
services = nss, pam
domains = domain.tld
default_domain_suffix = domain.tld

[domain/domain.tld]
default_shell = /bin/bash
krb5_store_password_if_offline = True
cache_credentials = True
krb5_realm = DOMAIN.TLD
realmd_tags = manages-system joined-with-adcli
id_provider = ad
ldap_sasl_authid = HOSTNAME$
fallback_homedir = /home/%d/%u
ad_domain = domain.tld
use_fully_qualified_names = True
ldap_id_mapping = True
access_provider = ad
ad_gpo_access_control = disabled
enumerate = False
ignore_group_members = True

[nss]
memcache_size_passwd = 200
memcache_size_group = 200
memcache_size_initgroups = 50
```

Quelques paramètres importants :

**`default_domain_suffix = domain.tld`** — les utilisateurs se connectent avec `jdoe` au lieu de `jdoe@domain.tld`. Plus pratique pour les utilisateurs finaux.

**`fallback_homedir = /home/%d/%u`** — crée `/home/domain.tld/jdoe` au lieu de `/home/jdoe@domain.tld`. Évite les problèmes avec le `@` dans certains programmes. Crée les répertoires parents manuellement :

```bash
mkdir /home/domain.tld
```

**`enumerate = False` + `ignore_group_members = True`** — indispensable sur les grands domaines. Sans ça, SSSD essaie d'énumérer tous les utilisateurs AD au démarrage, et c'est lent.

**`ad_gpo_access_control = disabled`** — désactive le contrôle GPO. Sans ça, personne ne peut se connecter par défaut. Gère les permissions manuellement avec `realm permit`.

La section `[nss]` agrandit le cache RAM à 200 MB — les requêtes `getent` restent rapides sans toucher le disque.

SSSD exige des permissions strictes sur sssd.conf :

```bash
sudo chmod 600 /etc/sssd/sssd.conf
```

### krb5.conf

```bash
sudo nano /etc/krb5.conf
```

```ini
[libdefaults]
    default_realm = DOMAIN.TLD
    dns_lookup_realm = true
    dns_lookup_kdc = true

[realms]
    DOMAIN.TLD = {
        kdc = domain.tld
        admin_server = domain.tld
    }

[domain_realm]
    .domain.tld = DOMAIN.TLD
    domain.tld = DOMAIN.TLD
```

---

## Étape 5 — Activer la création automatique des home dirs

```bash
sudo pam-auth-update --enable mkhomedir
```

Le home dir est créé automatiquement à la première connexion de l'utilisateur AD.

Configure PAM et NSS pour inclure SSSD :

```bash
sudo nano /etc/nsswitch.conf
```

Vérifie que ces lignes sont présentes :

```text
passwd:     compat sss
group:      compat sss
shadow:     compat sss
```

Redémarre SSSD :

```bash
sudo systemctl restart sssd
```

---

## Tester l'intégration

Récupère les infos d'un utilisateur AD :

```bash
getent passwd john@domain.tld
```

Résultat attendu :

```text
john@domain.tld:*:1725801106:1725800513:John Smith:/home/domain.tld/john:/bin/bash
```

Vérifie les groupes :

```bash
groups john@domain.tld
```

---

## Gestion des permissions

Par défaut avec `ad_gpo_access_control = disabled`, tout utilisateur AD valide peut se connecter. Restreins l'accès :

Autoriser un groupe spécifique seulement (tu peux aussi [masquer certains groupes de la GAL](/masquer-utilisateurs-gal-office365-active-directory/) si nécessaire) :

```bash
sudo realm deny --all
sudo realm permit -g "groupe@domain.tld"
```

Autoriser un utilisateur spécifique :

```bash
sudo realm permit user@domain.tld
```

Tout le monde (non recommandé) :

```bash
sudo realm permit --all
```

---

## Dépannage

Vérifie le statut SSSD et les logs :

```bash
sudo systemctl status sssd
sudo journalctl -u sssd
```

**SSSD ne démarre pas** → permissions sssd.conf : doit être `600` et owned par root. Pour durcir davantage l'accès SSH sur ces machines, consulte le [guide de sécurisation des serveurs Linux](/securite-de-votre-serveur-linux/).

**`realm join` échoue** → DNS mal configuré. Vérifie que `realm discover domain.tld` renvoie quelque chose avant de joindre.

**Authentification échoue hors ligne** → vérifie que `cache_credentials = True` est bien dans sssd.conf.

---

## Conclusion

L'intégration **Ubuntu Active Directory SSSD** via realmd fait le job proprement. Une fois la config en place, tes utilisateurs AD se connectent avec leurs credentials habituels, les home dirs se créent tout seuls, et le cache offline garde les sessions actives même si le DC est temporairement inaccessible.

Pour les grands parcs, couple ça avec une GPO d'accès restrictive et des groupes AD dédiés par rôle — évite `realm permit --all` en prod.

---

## Pour aller plus loin

- [Sécurité de votre serveur Linux : durcir un VPS](/securite-de-votre-serveur-linux/)
- [Masquer des utilisateurs de la GAL Office 365 + Active Directory](/masquer-utilisateurs-gal-office365-active-directory/)
- [Transférer les rôles FSMO Active Directory](/activedirectory-transfere-des-roles-fsmo/)
