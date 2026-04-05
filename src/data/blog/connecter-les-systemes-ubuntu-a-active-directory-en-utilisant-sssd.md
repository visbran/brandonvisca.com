---
title: Connecter les systèmes Ubuntu à Active Directory en utilisant SSSD
pubDatetime: "2024-06-13T11:40:02+02:00"
description: Apprenez à connecter les systèmes Ubuntu à Active Directory en utilisant SSSD pour une authentification centralisée et une gestion des utilisateurs. Sui...
tags:
  - linux
  - ubuntu
  - active-directory
  - sssd
  - authentification
  - tutoriel
  - avance
  - sysadmin
---

Introduction
============

L’intégration des systèmes Ubuntu à Windows Active Directory (AD) peut simplifier l’authentification des utilisateurs et la gestion des identités sur un réseau. Ce guide détaille comment utiliser le System Security Services Daemon (SSSD) pour connecter efficacement les hôtes Linux à un domaine Active Directory.

----------
## Table des matières


  - [Pourquoi intégrer Ubuntu avec Active Directory ?](#pourquoi-integrer-ubuntu-avec-active-directory)
  - [Préparer votre système Ubuntu](#preparer-votre-systeme-ubuntu)
      - [Installer les paquets nécessaires](#installer-les-paquets-necessaires)
      - [Configurer DNS](#configurer-dns)
      - [Activer et démarrer SSSD](#activer-et-demarrer-sssd)
      - [Découvrir et rejoindre le domaine](#decouvrir-et-rejoindre-le-domaine)
  - [Configurer SSSD](#configurer-sssd)
      - [Modifier la configuration de SSSD](#modifier-la-configuration-de-sssd)
      - [Configurer Kerberos](#configurer-kerberos)
  - [Création automatique du répertoire personnel](#creation-automatique-du-repertoire-personnel)
  - [Tester notre configuration](#tester-notre-configuration)
      - [Configurer PAM et NSS](#configurer-pam-et-nss)
  - [Configuration avancée](#configuration-avancee)
      - [Gérer plusieurs Active Directories](#gerer-plusieurs-active-directories)
      - [Gérer les permissions des utilisateurs](#gerer-les-permissions-des-utilisateurs)
  - [Questions fréquemment posées](#questions-frequemment-posees)
      - [Comment dépanner les problèmes de SSSD ?](#faq-question-1754323710489)
      - [Puis-je utiliser SSSD avec d’autres distributions Linux ?](#faq-question-1754323721895)
      - [Comment assurer la création des répertoires personnels pour les utilisateurs AD ?](#faq-question-1754323741584)
  - [Conclusion](#conclusion)

------------------------------------------------

L’intégration avec Active Directory fournit un fournisseur d’identité centralisé pour l’authentification réseau, rendant la gestion des utilisateurs plus sécurisée et efficace. Elle simplifie les connexions des utilisateurs et le contrôle d’accès sur plusieurs systèmes, réduisant ainsi la charge administrative.

Préparer votre système Ubuntu
-----------------------------

### Installer les paquets nécessaires

Commencez par installer les paquets requis sur votre système Ubuntu. La commande suivante installe `realmd`, `sssd`, et d’autres outils essentiels :

```bash
sudo apt update
sudo apt install realmd sssd-ad sssd-tools libnss-sss libpam-sss adcli samba-common-bin oddjob oddjob-mkhomedir packagekit

```

sudo nano /etc/resolv.conf


Ajoutez l’IP de votre serveur DNS AD :

```bash
nameserver <AD_DNS_IP>

```

sudo systemctl enable sssd
sudo systemctl start sssd


### Découvrir et rejoindre le domaine

Utilisez la commande `realm` pour découvrir et rejoindre le domaine AD. Remplacez `domain.tld` par le nom de votre domaine réel :

```bash
sudo realm discover domain.tld
sudo realm join -v --user=Administrator domain.tld

```

sudo cp /etc/sssd/sssd.conf /etc/sssd/sssd.conf.bak
sudo nano /etc/sssd/sssd.conf


Utilisez la configuration suivante comme modèle, en remplaçant `domain.tld` par votre domaine AD :

```bash
[sssd]
domains = domain.tld
config_file_version = 2
services = nss, pam

[domain/domain.tld]
id_provider = ad
auth_provider = ad
chpass_provider = ad
access_provider = ad
ldap_id_mapping = True
krb5_realm = DOMAIN.TLD
realmd_tags = manages-system joined-with-samba
cache_credentials = True
default_shell = /bin/bash
fallback_homedir = /home/%u@%d
use_fully_qualified_names = True
ldap_schema = ad

```

sudo nano /etc/krb5.conf


Ajoutez ou modifiez les lignes suivantes :

```bash
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

sudo pam-auth-update --enable mkhomedir



Tester notre configuration
--------------------------

Vous devriez maintenant être en mesure de récupérer des informations sur les utilisateurs de l’AD. Dans cet exemple, `John DOE` est un utilisateur de l’AD :

```bash
$ getent passwd john@ad1.domain.tld
john@ad1.domain.tld:*:1725801106:1725800513:John Smith:/home/john@ad1.domain.tld:/bin/bash


```

$ groups john@ad1.domain.tld
john@ad1.domain.tld : utilisateurs du domaine@ad1.domain.tld it@ad1.domain.tld



### Configurer PAM et NSS

Modifiez les fichiers de configuration PAM et NSS pour intégrer SSSD :

```bash
sudo nano /etc/nsswitch.conf

```

passwd:     compat sss
group:      compat sss
shadow:     compat sss


Configurez PAM pour utiliser SSSD :

```bash
sudo pam-auth-update

```

sudo realm permit -g "groupe@domain.tld"
sudo realm deny --all


Sauvegardez et modifiez le fichier de configuration. Si vous n’avez pas un sssd.conf fonctionnel, ne redémarrez pas car votre système ne démarrera pas ou ne se connectera pas lorsque SSSD est cassé, et vous devrez peut-être utiliser le mode de récupération.

```bash
cp /etc/sssd/sssd.conf /etc/sssd/sssd.back.20230101
nano /etc/sssd/sssd.conf
```

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

Vous pouvez utiliser la configuration ci-dessus, en remplaçant domain.tld par votre propre domaine. Laissez-moi vous guider à travers certaines des modifications.

```bash
default_domain_suffix = domain.tld
```

login myaduser@domain.tld

Lorsque nous définissons *default*domain*suffix* à domain.tld, cela ajoute automatiquement le domaine en suffixe à toutes les connexions, ce qui facilite la tâche des utilisateurs finaux.

```bash
login myaduser
```

default_shell = /bin/bash
fallback_homedir = /home/%d/%u

L’emplacement du répertoire d’accueil %d/%u assure que les comptes d’utilisateurs ayant des sAMAccountNames chevauchants dans différents domaines ne se heurtent pas (jdoe@finance.domain.tld est peu probable qu’il soit le même jdoe@hr.domain.tld).

Le %d sera remplacé par le domaine de l’utilisateur lors de la connexion. %u est le nom d’utilisateur, probablement l’attribut sAMAccountName. En utilisant l’exemple ci-dessus, un utilisateur se connectera à /home/finance.domain.tld/jdoe tandis que l’autre utilisera /home/hr.domain.tld/jdoe.

Avec le %u@%d par défaut, nous avons remarqué que certains programmes ou utilisateurs ne gèrent pas bien le symbole @. Vous devez créer manuellement le répertoire parent pour chaque domaine, car oddjob-mkhomedir ne gère pas la création de répertoires parents.

```bash
mkdir /home/finance.domain.tld /home/rh.domain.tld
```

ad_gpo_access_control = disabled

En désactivant GPO, par défaut, personne ne pourra se connecter. Pour permettre à *quiconque possède une accréditation AD active* de se connecter (non recommandé) :

```bash
realm permit --all
```

realm deny --all
realm permit user@domain.tld
realm permit -g group@domain.tld

L’ensemble de configurations suivant est principalement destiné à des domaines plus grands :

```bash
enumerate = False
ignore_group_members = True
```

[nss]
memcache_size_passwd = 200
memcache_size_group = 200
memcache_size_initgroups = 50

Les utilisateurs qui terminent une connexion auront toujours leurs informations mises en cache localement. La section NSS agrandit le cache RAM par défaut à 200 MB, de sorte que les requêtes sont rapides et n’ont pas besoin de toucher le disque à chaque fois qu’un appel [*getent*](https://man7.org/linux/man-pages/man1/getent.1.html) est effectué.

Assurez-vous de dimensionner en fonction des ressources disponibles, du nombre d’utilisateurs susceptibles de se connecter et de la taille des adhésions aux groupes.

Une fois toutes les modifications effectuées, redémarrez sssd. Cette commande ne devrait rien retourner, si tout va bien.

```bash
systemctl restart sssd
```

systemctl status sssd
journalctl -u sssd

Questions fréquemment posées
----------------------------

### Comment dépanner les problèmes de SSSD ?

Vérifiez le statut du service SSSD et les journaux pour le dépannage :

sudo systemctl status sssd  
sudo journalctl -u sssd

### Puis-je utiliser SSSD avec d’autres distributions Linux ?

Oui, [SSSD est compatible avec diverses distributions Linux](https://ubuntu.com/server/docs/how-to-set-up-sssd-with-active-directory), y compris Debian et RedHat. Les commandes d’installation peuvent légèrement différer.

### Comment assurer la création des répertoires personnels pour les utilisateurs AD ?

Configurez `oddjob-mkhomedir` pour créer automatiquement les répertoires personnels lors de la connexion :

sudo pam-auth-update –enable mkhomedir

Conclusion
----------

L’intégration des systèmes Ubuntu avec Active Directory en utilisant SSSD améliore la sécurité et simplifie la gestion des utilisateurs.

En suivant les étapes décrites dans ce guide, vous pouvez connecter efficacement vos hôtes Linux à un domaine AD et gérer les connexions utilisateur sans problème.

Pour des étapes plus détaillées sur [comment joindre des hôtes Linux à un domaine Active Directory](https://blog.netwrix.com/2022/11/01/join-linux-hosts-to-active-directory-domain/) ou [connecter Linux à Active Directory en utilisant SSSD](https://4sysops.com/archives/connect-linux-to-active-directory-using-sssd), consultez les ressources supplémentaires disponibles en ligne.

Pour ceux utilisant des systèmes Ubuntu, des guides spécifiques tels que [Comment connecter Ubuntu à AD en utilisant SSSD](https://help.ubuntu.com/community/ActiveDirectoryWinbindHowto) offrent des instructions ciblées.

Pour plus de détails techniques et d’exemples, consultez [Comment utiliser Active Directory comme fournisseur d’identité pour SSSD](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/windows_integration_guide/sssd-ad) et [Joindre une VM Linux à Active Directory](https://www.starwindsoftware.com/blog/join-a-linux-vm-to-active-directory-using-sssd).
