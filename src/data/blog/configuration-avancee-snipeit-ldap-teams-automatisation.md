---
title: "Configuration avancée SnipeIT : LDAP, automatisation et notifications (guide 2025)"
pubDatetime: "2025-10-13T16:05:41+02:00"
description: "Configuration avancée SnipeIT : intégration Active Directory LDAP, scan réseau automatique, libre-service, notifications Teams et sécurité. Guide comple..."
tags:
  - linux
  - sysadmin
  - avance
  - snipeit
  - ldap
  - automatisation
---

-----------
## Table des matières


  - [Installation SnipeIT fonctionnelle](#installation-snipe-it-fonctionnelle)
  - [Accès Active Directory (pour LDAP)](#acces-active-directory-pour-ldap)
  - [Serveur sécurisé](#serveur-securise)
- [Intégration Active Directory LDAP](#integration-active-directory-ldap)
  - [Pourquoi intégrer AD avec SnipeIT ?](#pourquoi-integrer-ad-avec-snipe-it)
  - [Configuration LDAP dans SnipeIT](#configuration-ldap-dans-snipe-it)
      - [1. Paramètres serveur LDAP](#1-parametres-serveur-ldap)
      - [2. Filtres LDAP](#2-filtres-ldap)
      - [3. Mapping des champs](#3-mapping-des-champs)
      - [4. Tester la connexion LDAP](#4-tester-la-connexion-ldap)
  - [Synchronisation manuelle LDAP](#synchronisation-manuelle-ldap)
  - [Automatiser la sync LDAP (cron)](#automatiser-la-sync-ldap-cron)
  - [Troubleshooting LDAP](#troubleshooting-ldap)
- [Scanner automatiquement le parc avec Nmap](#scanner-automatiquement-le-parc-avec-nmap)
  - [Principe du scan automatique](#principe-du-scan-automatique)
  - [Installation de Nmap](#installation-de-nmap)
  - [Script de scan réseau basique](#script-de-scan-reseau-basique)
  - [Script Python pour traiter les résultats](#script-python-pour-traiter-les-resultats)
  - [Génération de la clé API SnipeIT](#generation-de-la-cle-api-snipe-it)
  - [Rendre les scripts exécutables](#rendre-les-scripts-executables)
  - [Tester le scan](#tester-le-scan)
  - [Automatiser le scan (cron)](#automatiser-le-scan-cron)
- [Configuration du portail libre-service](#configuration-du-portail-libre-service)
  - [Activer le libre-service](#activer-le-libre-service)
  - [Configuration des permissions](#configuration-des-permissions)
  - [Assigner les utilisateurs au groupe](#assigner-les-utilisateurs-au-groupe)
  - [Activer les demandes d’assets](#activer-les-demandes-dassets)
- [Sécurité avancée SnipeIT](#securite-avancee-snipe-it)
  - [1. HTTPS obligatoire (SSL/TLS)](#1-https-obligatoire-ssl-tls)
  - [2. Authentification à deux facteurs (2FA)](#2-authentification-a-deux-facteurs-2-fa)
  - [3. Chiffrement des custom fields sensibles](#3-chiffrement-des-custom-fields-sensibles)
  - [4. Audit logs](#4-audit-logs)
  - [5. Restreindre l’accès par IP](#5-restreindre-lacces-par-ip)
  - [6. Désactiver la création de compte](#6-desactiver-la-creation-de-compte)
- [Notifications Teams et Email](#notifications-teams-et-email)
  - [Configuration Email (SMTP)](#configuration-email-smtp)
  - [Configuration Teams (Webhooks)](#configuration-teams-webhooks)
      - [Créer un workflow Teams](#creer-un-workflow-teams)
      - [Configurer SnipeIT](#configurer-snipe-it)
      - [Format des notifications](#format-des-notifications)
  - [Personnaliser les notifications](#personnaliser-les-notifications)
- [Automatisation et API](#automatisation-et-api)
  - [Utiliser l’API REST SnipeIT](#utiliser-l-api-rest-snipe-it)
      - [Lister tous les assets](#lister-tous-les-assets)
      - [Créer un asset](#creer-un-asset)
      - [Assigner un asset à un utilisateur](#assigner-un-asset-a-un-utilisateur)
  - [Scripts d’automatisation utiles](#scripts-dautomatisation-utiles)
      - [Import CSV automatique](#import-csv-automatique)
- [Conclusion : configuration avancée SnipeIT maîtrisée](#conclusion-configuration-avancee-snipe-it-maitrisee)


Dans ce guide de **configuration avancée SnipeIT**, on va couvrir tout ce qui fait la différence entre « j’ai installé un outil » et « j’ai un système ITSM professionnel ». Intégration Active Directory pour ne plus saisir les utilisateurs à la main, scan automatique du réseau pour découvrir les assets, notifications Teams pour que toute l’équipe soit au courant, et sécurité béton pour dormir tranquille.

Cette **configuration SnipeIT avancée** est ce qui manque à 90% des installations que je vois. Allez, on transforme ton SnipeIT en Formule 1.

- - - - - -

Prérequis configuration avancée SnipeIT
---------------------------------------

Avant d’attaquer cette **configuration SnipeIT avancée**, assure-toi d’avoir :

### Installation SnipeIT fonctionnelle

Si c’est pas déjà fait, suis mon [guide d’installation SnipeIT Ubuntu complet](https://brandonvisca.com/installation-snipeit-ubuntu-guide-complet/). On part du principe que tu as un SnipeIT qui tourne et que tu peux te connecter en admin.

### Accès Active Directory (pour LDAP)

- Compte de service AD avec droits de lecture
- Accès LDAP sur le port 389 ou 636 (LDAPS)
- Base DN de ton Active Directory

### Serveur sécurisé

Si ton serveur ressemble encore à une passoire, va lire mon guide sur [la sécurisation Linux](https://brandonvisca.com/securite-de-votre-serveur-linux/). Sérieusement.

**À savoir :** Cette **configuration avancée SnipeIT** va manipuler des comptes utilisateurs et des données sensibles. La sécurité, c’est pas une option.

- - - - - -

Intégration Active Directory LDAP
---------------------------------

La **configuration SnipeIT LDAP** est probablement LA fonctionnalité la plus demandée en entreprise. Fini la saisie manuelle des utilisateurs, bonjour la synchronisation automatique avec ton Active Directory.

### Pourquoi intégrer AD avec SnipeIT ?

**Avantages :**

- ✅ Sync automatique des utilisateurs AD → SnipeIT
- ✅ Login avec les credentials AD (Single Sign-On)
- ✅ Mise à jour auto des infos utilisateurs (nom, email, département)
- ✅ Désactivation auto des comptes supprimés dans AD
- ✅ Assignation d’assets basée sur l’organigramme AD

**Sans LDAP**, tu dois :

- Créer chaque utilisateur manuellement dans SnipeIT
- Mettre à jour les infos quand quelqu’un change de poste
- Désactiver les comptes des personnes qui partent

Bref, un boulot de dingue. Avec LDAP, tout ça se fait automatiquement.

### Configuration LDAP dans SnipeIT

Connecte-toi en admin dans SnipeIT, puis va dans **Settings > LDAP/AD**.

#### 1. Paramètres serveur LDAP

```bash
# Configuration type pour Active Directory Windows

LDAP Server: ldap://ton-dc.entreprise.local
# ou ldaps://ton-dc.entreprise.local (recommandé, port 636 avec SSL)

Port: 389 (ou 636 pour LDAPS)

Base Bind DN: OU=Users,DC=entreprise,DC=local
# Remplace par ta structure AD

LDAP Bind Username: CN=snipeit-service,OU=ServiceAccounts,DC=entreprise,DC=local
# Compte de service AD créé spécialement

LDAP Bind Password: MotDePasseUltraSecure123!

```

# Filtre basique : tous les utilisateurs actifs
(&(objectClass=user)(sAMAccountType=805306368)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))

# Filtre : uniquement les membres d'un groupe spécifique
(&(objectClass=user)(memberOf=CN=SnipeIT-Users,OU=Groups,DC=entreprise,DC=local))

# Filtre : utilisateurs d'une OU spécifique
(&(objectClass=user)(distinguishedName=*,OU=IT-Department,DC=entreprise,DC=local))

# Filtre : exclure les comptes de service
(&(objectClass=user)(!(description=Service Account)))


**Explication du filtre standard :**

- `objectClass=user` : objets de type utilisateur
- `sAMAccountType=805306368` : comptes utilisateurs normaux (pas machines)
- `!(userAccountControl:1.2.840.113556.1.4.803:=2)` : exclure les comptes désactivés

#### 3. Mapping des champs

SnipeIT doit savoir où trouver les infos dans AD.

```bash
Username Field: samaccountname
# Nom d'utilisateur AD (ex: jdupont)

First Name: givenname
# Prénom

Last Name: sn
# Nom de famille

Email: mail
# Email

Employee Number: employeenumber
# Matricule (si présent dans AD)

Department: department
# Département

```

sudo tail -f /var/log/apache2/snipeit-error.log


Souvent, c’est un problème de syntaxe dans le Base DN ou le filtre LDAP.

### Synchronisation manuelle LDAP

Une fois configuré, tu peux sync manuellement :

**Via l’interface web :**

- Va dans **People > LDAP**
- Clique sur **« Synchronize »**
- Attends que ça finisse (peut prendre plusieurs minutes pour un gros AD)

**Via CLI (recommandé pour automatiser) :**

```bash
cd /var/www/snipe-it
sudo -u www-data php artisan snipeit:ldap-sync --summary

```

# Sync avec assignation automatique à un site
sudo -u www-data php artisan snipeit:ldap-sync --location="Paris HQ" --summary

# Sync avec location_id
sudo -u www-data php artisan snipeit:ldap-sync --location_id=1 --summary


### Automatiser la sync LDAP (cron)

Créer un cron pour synchroniser tous les jours à 2h du matin :

```bash
# Édite le crontab de www-data
sudo crontab -u www-data -e

# Ajoute cette ligne :
0 2 * * * /usr/bin/php /var/www/snipe-it/artisan snipeit:ldap-sync --summary >> /var/log/snipeit-ldap-sync.log 2>&1

```

# Test manuel depuis le serveur
ldapsearch -x -H ldap://ton-dc.entreprise.local -D "CN=snipeit-service,OU=ServiceAccounts,DC=entreprise,DC=local" -W -b "OU=Users,DC=entreprise,DC=local" "(objectClass=user)"


Si cette commande ne retourne rien, ton filtre ou ton Base DN est incorrect.

**Problème : Les utilisateurs ne peuvent pas se connecter**

- Vérifie que la case « Active Directory » est cochée dans les settings LDAP
- Vérifie que l’Auth Query est correct : `samaccountname=`
- Vérifie que les utilisateurs existent bien dans SnipeIT après la sync

- - - - - -

Scanner automatiquement le parc avec Nmap
-----------------------------------------

SnipeIT n’a **pas de découverte réseau native**. C’est son plus gros point faible face à GLPI (je l’explique dans mon [comparatif SnipeIT vs GLPI](https://brandonvisca.com/snipeit-vs-glpi-comparatif-itsm-inventaire-it/)). Mais on va pallier ça avec des scripts maison.

### Principe du scan automatique

L’idée : utiliser **Nmap** pour scanner le réseau, extraire les infos des machines (IP, MAC, OS, hostname), et créer/mettre à jour les assets dans SnipeIT via l’API.

**Workflow :**

1. Nmap scanne une plage IP
2. Script Python/Bash extrait les données
3. Script interroge l’API SnipeIT
4. Si l’asset existe (même MAC) → mise à jour
5. Si l’asset n’existe pas → création

### Installation de Nmap

```bash
sudo apt install nmap -y

```

#!/bin/bash
# Script de scan réseau pour SnipeIT
# Brandon Visca - brandonvisca.com

# Configuration
NETWORK="192.168.1.0/24"  # Ton réseau à scanner
OUTPUT_FILE="/tmp/nmap-scan-$(date +%Y%m%d).xml"
API_KEY="ton-api-key-snipeit"
SNIPEIT_URL="https://inventory.entreprise.com"

# Scan Nmap (-sn = ping scan, -O = OS detection, -oX = output XML)
echo "Scanning network $NETWORK..."
sudo nmap -sn -O --osscan-guess $NETWORK -oX $OUTPUT_FILE

echo "Scan complete. Results in $OUTPUT_FILE"
echo "Processing results..."

# Appel du script Python pour traiter les résultats
python3 /usr/local/bin/process-nmap-results.py $OUTPUT_FILE

echo "Done!"


### Script Python pour traiter les résultats

Créer `/usr/local/bin/process-nmap-results.py` :

```bash
#!/usr/bin/env python3
"""
Script de traitement des résultats Nmap pour SnipeIT
Auteur: Brandon Visca - brandonvisca.com
"""

import xml.etree.ElementTree as ET
import requests
import sys

# Configuration
SNIPEIT_URL = "https://inventory.entreprise.com/api/v1"
API_KEY = "ton-api-key-snipeit"
DEFAULT_STATUS_ID = 2  # ID du statut "Ready to Deploy" dans SnipeIT
DEFAULT_MODEL_ID = 1   # ID du modèle par défaut

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def parse_nmap_xml(xml_file):
    """Parse le fichier XML Nmap et extrait les hosts"""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    hosts = []
    for host in root.findall('host'):
        # Ignore les hosts down
        if host.find('status').get('state') != 'up':
            continue
            
        host_data = {}
        
        # IP Address
        address = host.find('address[@addrtype="ipv4"]')
        if address is not None:
            host_data['ip'] = address.get('addr')
        
        # MAC Address
        mac = host.find('address[@addrtype="mac"]')
        if mac is not None:
            host_data['mac'] = mac.get('addr')
            host_data['vendor'] = mac.get('vendor', 'Unknown')
        
        # Hostname
        hostnames = host.find('hostnames')
        if hostnames is not None:
            hostname = hostnames.find('hostname')
            if hostname is not None:
                host_data['hostname'] = hostname.get('name')
        
        # OS Detection (si disponible)
        os = host.find('.//osmatch')
        if os is not None:
            host_data['os'] = os.get('name')
        
        if host_data:
            hosts.append(host_data)
    
    return hosts

def check_asset_exists(mac_address):
    """Vérifie si un asset avec cette MAC existe déjà"""
    # Recherche par custom field _snipeit_mac_address_1
    response = requests.get(
        f"{SNIPEIT_URL}/hardware",
        headers=headers,
        params={"search": mac_address}
    )
    
    if response.status_code == 200:
        data = response.json()
        if data['total'] > 0:
            return data['rows'][0]['id']
    return None

def create_or_update_asset(host_data):
    """Crée ou met à jour un asset dans SnipeIT"""
    mac = host_data.get('mac')
    if not mac:
        print(f"⚠️  Skipping host without MAC: {host_data.get('ip')}")
        return
    
    # Vérifie si l'asset existe
    asset_id = check_asset_exists(mac)
    
    # Prépare les données
    asset_payload = {
        "name": host_data.get('hostname', f"Device-{mac.replace(':', '')}"),
        "status_id": DEFAULT_STATUS_ID,
        "model_id": DEFAULT_MODEL_ID,
        "_snipeit_mac_address_1": mac,
        "notes": f"Auto-discovered via Nmap scan\nIP: {host_data.get('ip')}\nVendor: {host_data.get('vendor', 'Unknown')}\nOS: {host_data.get('os', 'Unknown')}"
    }
    
    if asset_id:
        # Mise à jour de l'asset existant
        response = requests.patch(
            f"{SNIPEIT_URL}/hardware/{asset_id}",
            headers=headers,
            json=asset_payload
        )
        if response.status_code == 200:
            print(f"✅ Updated: {host_data.get('hostname', mac)} ({host_data.get('ip')})")
        else:
            print(f"❌ Failed to update {mac}: {response.text}")
    else:
        # Création d'un nouvel asset
        response = requests.post(
            f"{SNIPEIT_URL}/hardware",
            headers=headers,
            json=asset_payload
        )
        if response.status_code == 200:
            print(f"✅ Created: {host_data.get('hostname', mac)} ({host_data.get('ip')})")
        else:
            print(f"❌ Failed to create {mac}: {response.text}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 process-nmap-results.py <nmap-xml-file>")
        sys.exit(1)
    
    xml_file = sys.argv[1]
    print(f"📡 Processing Nmap results from {xml_file}...")
    
    hosts = parse_nmap_xml(xml_file)
    print(f"🔍 Found {len(hosts)} active hosts")
    
    for host in hosts:
        create_or_update_asset(host)
    
    print(f"\n✨ Processing complete!")

if __name__ == "__main__":
    main()

```

sudo chmod +x /usr/local/bin/snipeit-network-scan.sh
sudo chmod +x /usr/local/bin/process-nmap-results.py

# Installer les dépendances Python
sudo apt install python3-pip -y
pip3 install requests


### Tester le scan

```bash
sudo /usr/local/bin/snipeit-network-scan.sh

```

Scanning network 192.168.1.0/24...
Scan complete. Results in /tmp/nmap-scan-20251010.xml
Processing results...
🔍 Found 45 active hosts
✅ Created: PC-COMPTA-01 (192.168.1.15)
✅ Updated: SERVER-WEB (192.168.1.100)
...
✨ Processing complete!


### Automatiser le scan (cron)

Scan tous les jours à 3h du matin :

```bash
sudo crontab -e

# Ajoute :
0 3 * * * /usr/local/bin/snipeit-network-scan.sh >> /var/log/snipeit-network-scan.log 2>&1

```

sudo apt install certbot python3-certbot-apache -y
sudo certbot --apache -d inventory.entreprise.com


Certbot configure Apache automatiquement avec SSL.

**Forcer HTTPS dans SnipeIT :**

```bash
# Dans /var/www/snipe-it/.env
APP_URL=https://inventory.entreprise.com

```

# Dans /etc/apache2/sites-available/snipe-it.conf
<Directory /var/www/snipe-it/public>
    Require ip 192.168.1.0/24
    Require ip 10.0.0.0/8
</Directory>


Redémarre Apache :

```bash
sudo systemctl restart apache2

```

Driver: SMTP
SMTP Host: smtp.gmail.com
SMTP Port: 587
Encryption: TLS
SMTP Username: alerts@entreprise.com
SMTP Password: mot-de-passe-application
From Address: noreply-snipeit@entreprise.com
From Name: SnipeIT Inventory


**Exemple avec Office 365 :**

```bash
Driver: SMTP
SMTP Host: smtp.office365.com
SMTP Port: 587
Encryption: TLS
SMTP Username: alerts@entreprise.com
SMTP Password: mot-de-passe

```

Microsoft Teams Webhook URL: [colle l'URL du workflow]
Microsoft Teams Channel: #it-assets


**Test :** Clique **« Test Microsoft Teams Integration »**

Tu dois voir un message dans Teams du type :

```bash
Test message from SnipeIT
This is a test of your Microsoft Teams integration.

```

📦 Asset Checked Out
MacBook Pro 16" (Serial: C02XL4J8MD6T)
Assigned to: Jean Dupont
By: Marie Martin
Notes: Remplacement laptop défectueux


### Personnaliser les notifications

**Settings > Notifications**

Tu peux activer/désactiver chaque type de notification individuellement :

✅ Send emails on checkout
✅ Send emails on checkin
✅ Send Teams notifications on checkout
❌ Send Teams notifications on checkin (trop de spam)
✅ Send license expiration reminders (30 days before)
✅ Send warranty expiration reminders (60 days before)


**Bonnes pratiques :**

- N’active QUE les notifications utiles (sinon spam)
- Pour Teams, limite aux événements importants (checkout/requests)
- Pour Email, envoie les résumés quotidiens plutôt qu’en temps réel

- - - - - -

Automatisation et API
---------------------

> 👉 Si tu gères un parc Windows, jette un œil à [SnipeAgent](https://brandonvisca.com/snipeagent-automatiser-inventaire-windows-snipeit/), un agent qui remplit automatiquement ton inventaire Snipe-IT à partir des machines Windows du réseau. Ça complète parfaitement l’automatisation via l’API.

### Utiliser l’API REST SnipeIT

SnipeIT a une API REST complète. Documentation : `https://ton-snipeit.com/api/docs`

**Exemples d’utilisation :**

#### Lister tous les assets

```bash
curl -X GET "https://inventory.entreprise.com/api/v1/hardware" \
  -H "Authorization: Bearer TON-API-KEY" \
  -H "Accept: application/json"

```

curl -X POST "https://inventory.entreprise.com/api/v1/hardware" \
  -H "Authorization: Bearer TON-API-KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MacBook Pro Jean",
    "model_id": 3,
    "status_id": 2,
    "serial": "C02XL4J8MD6T",
    "asset_tag": "MBP-2024-042"
  }'


#### Assigner un asset à un utilisateur

```bash
curl -X POST "https://inventory.entreprise.com/api/v1/hardware/42/checkout" \
  -H "Authorization: Bearer TON-API-KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "assigned_user": 15,
    "checkout_at": "2025-10-10",
    "note": "Nouvel arrivant"
  }'

```

import csv
import requests

API_KEY = "ton-api-key"
SNIPEIT_URL = "https://inventory.entreprise.com/api/v1"

with open('new-assets.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        payload = {
            "name": row['name'],
            "serial": row['serial'],
            "model_id": int(row['model_id']),
            "status_id": 2
        }
        
        response = requests.post(
            f"{SNIPEIT_URL}/hardware",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json=payload
        )
        
        if response.status_code == 200:
            print(f"✅ Created: {row['name']}")
        else:
            print(f"❌ Failed: {row['name']} - {response.text}")


- - - - - -

Conclusion : configuration avancée SnipeIT maîtrisée
----------------------------------------------------

Voilà, tu as maintenant une **configuration SnipeIT avancée** de niveau professionnel. Plus besoin de saisir les utilisateurs à la main, plus besoin de scanner manuellement le réseau, et toute ton équipe est notifiée en temps réel via Teams.

**Récap de cette configuration avancée SnipeIT :** ✅ Intégration Active Directory LDAP (sync auto des users)  
✅ Scan réseau automatique avec Nmap (découverte des assets)  
✅ Portail libre-service (users autonomes)  
✅ Sécurité renforcée (2FA, HTTPS, audit logs)  
✅ Notifications Teams + Email configurées  
✅ Automatisation via API et scripts

Ton **SnipeIT** est maintenant au niveau d’un CMDB professionnel. Il ne te reste plus qu’à maintenir tout ça (sauvegardes régulières, mises à jour mensuelles) et à l’enrichir au fil du temps.

**Et maintenant ?**

Si tu veux aller encore plus loin, les prochains sujets à explorer :

- **Nginx + reverse proxy + SSL** (setup production avancé)
- **Monitoring SnipeIT avec Zabbix/Nagios**
- **Intégration avec ton système de ticketing** (osTicket, Zammad)
- **Rapports personnalisés avancés**

En attendant, si ton terminal ressemble encore à celui de Windows 95, fais un tour sur mon guide [Oh My Zsh + Powerlevel10k](https://brandonvisca.com/installation-oh-my-zsh-powerlevel10k-guide-complet/). Un vrai ninja a des outils qui claquent.

**💬 Questions sur la configuration avancée SnipeIT ?** Balance ton cas d’usage en commentaire, j’adore les défis techniques !
