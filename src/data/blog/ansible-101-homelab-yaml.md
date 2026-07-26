---
title: "Ansible homelab 101 : automatise ton infrastructure en YAML"
description: "Guide Ansible homelab pour débutants : automatise ton infrastructure en YAML avec playbooks, inventaires, rôles et exemples prêts à copier."
pubDatetime: "2026-07-26T08:00:00.000Z"
modDatetime: "2026-07-26T08:00:00.000Z"
author: Brandon Visca
tags:
  - linux
  - auto-hebergement
  - ansible
  - intermediaire
featured: false
draft: false
focusKeyword: ansible homelab
faqs:
  - question: "Ansible ou Docker Compose, faut-il choisir ?"
    answer: "Non. Ansible orchestre les machines (install, config, déploiement), Docker Compose gère les conteneurs. La plupart des homelabs utilisent les deux : Ansible installe Docker puis déploie les stacks Compose."
  - question: "Ansible a-t-il besoin d'un agent sur les serveurs distants ?"
    answer: "Non. Ansible est agentless : il utilise SSH et Python déjà présents sur la cible. Rien à installer du côté serveur."
  - question: "Puis-je utiliser Ansible sur un Raspberry Pi ou un NAS ?"
    answer: "Oui, tant que SSH est actif et Python installé. Les playbooks peuvent même déployer Docker sur ARM pour adapter les images à l'architecture."
  - question: "Quelle est la différence entre un playbook et un rôle Ansible ?"
    answer: "Un playbook est un scénario d'automatisation (liste de tâches sur des hôtes). Un rôle est un package réutilisable de tâches, variables et templates pour une fonction précise (ex : installer Docker)."
ogImage: ""
---
> 💡 **TL;DR**
> - Ansible est un outil d'automatisation agentless qui te permet de configurer, déployer et maintenir tes serveurs via des fichiers YAML lisibles
> - Tu décris l'état désiré de ton infrastructure dans un playbook, Ansible s'occupe de le réaliser sur tes machines via SSH
> - Parfait pour homelab : installe Docker, configure SSH, déploie des stacks, tout en un seul fichier versionnable avec `git`

## Pourquoi Ansible dans ton homelab ?

Tu as monté un [serveur auto-hébergé avec Docker](/docker-debutant-services-auto-heberger/). Tu fais tourner une vingtaine de services. Et puis un jour tu dois :

- Changer le port SSH sur tes 4 VMs
- Mettre à jour les certificats SSL partout
- Déployer une nouvelle stack sur ton VPS et ton NUC en même temps
- Refaire ta config de zéro après un crash disque

À la main, c'est répétitif, source d'erreurs et insupportable. Ansible résout ça en te permettant d'écrire une fois, d'exécuter partout.

Contrairement à d'autres outils d'automatisation, Ansible est **agentless** : pas besoin d'installer quoi que ce soit sur tes serveurs. Il se connecte en SSH et exécute des tâches directement. C'est léger, rapide à mettre en place et parfaitement adapté à un homelab modeste.

## Table des matières

## Ce que tu dois savoir avant de commencer

Ansible utilise trois concepts simples :

- **L'inventaire** (`inventory.ini` ou `inventory.yml`) : la liste de tes machines
- **Les playbooks** (`*.yml`) : les scénarios d'automatisation
- **Les rôles** : des modules réutilisables pour organiser tes playbooks

Le langage de description est le **YAML**. Pas de code complexe, pas de DSL obscur. Tu décris l'état désiré, Ansible s'occupe du reste.

### Prérequis

- Une machine de contrôle (ton laptop, un desktop, un VPS) sous Linux, macOS ou WSL
- Python 3 et `pip` installés
- Accès SSH à tes machines cibles avec une clé (pas de mot de passe)
- Un minimum de droits `sudo` sur les machines distantes

## Installation d'Ansible

Sur ta machine de contrôle :

```bash
# Debian / Ubuntu
sudo apt update && sudo apt install -y ansible sshpass

# macOS (avec Homebrew)
brew install ansible

# Vérifier l'installation
ansible --version
```

La version 2.15+ est recommandée pour bénéficier des dernières fonctionnalités et collections.

## Ton premier inventaire

Crée un fichier `inventory.ini` qui liste tes machines. Tu peux les organiser par groupes :

```ini
[homelab]
192.168.1.10 ansible_user=admin
192.168.1.11 ansible_user=admin

[vps]
srv-exemple.net ansible_user=debian

[all:vars]
ansible_python_interpreter=/usr/bin/python3
ansible_ssh_private_key_file=~/.ssh/id_rsa_homelab
```

Teste la connexion à tes machines :

```bash
ansible all -i inventory.ini -m ping
```

Si tout est vert, tu es prêt à automatiser.

## Ton premier playbook Ansible homelab : configurer SSH et les mises à jour

Crée `setup-base.yml` :

```yaml
---
- name: Configuration de base des serveurs homelab
  hosts: homelab
  become: yes
  tasks:
    - name: Mise à jour des paquets
      apt:
        update_cache: yes
        upgrade: dist
      tags: [update]

    - name: Installation des outils essentiels
      apt:
        name:
          - curl
          - git
          - htop
          - vim
          - fail2ban
        state: present

    - name: Désactivation de la connexion root par SSH
      lineinfile:
        path: /etc/ssh/sshd_config
        regexp: '^PermitRootLogin'
        line: 'PermitRootLogin no'
        state: present
      notify: Redémarrer SSH

    - name: Interdiction de l'authentification par mot de passe
      lineinfile:
        path: /etc/ssh/sshd_config
        regexp: '^PasswordAuthentication'
        line: 'PasswordAuthentication no'
        state: present
      notify: Redémarrer SSH

  handlers:
    - name: Redémarrer SSH
      service:
        name: ssh
        state: restarted
```

Exécute-le avec :

```bash
ansible-playbook -i inventory.ini setup-base.yml
```

En quelques lignes, tu viens de :
- Mettre à jour tous tes serveurs
- Installer tes outils préférés
- Durcir la configuration SSH

Si tu veux approfondir le durcissement SSH, j'ai détaillé d'autres astuces dans mon article sur [l'hardening Linux](/hardening-linux-10-commandes/).

## Installer Docker avec Ansible

Voici un playbook qui installe Docker et Docker Compose sur tes machines, prêt à déployer tes stacks :

```yaml
---
- name: Installation de Docker sur les serveurs
  hosts: homelab
  become: yes
  tasks:
    - name: Installation des dépendances
      apt:
        name:
          - apt-transport-https
          - ca-certificates
          - curl
          - gnupg
          - lsb-release
        state: present

    - name: Ajout de la clé GPG officielle Docker
      apt_key:
        url: https://download.docker.com/linux/debian/gpg
        state: present

    - name: Ajout du dépôt Docker
      apt_repository:
        repo: "deb [arch=amd64] https://download.docker.com/linux/debian {{ ansible_distribution_release }} stable"
        state: present

    - name: Installation de Docker Engine et Docker Compose
      apt:
        name:
          - docker-ce
          - docker-ce-cli
          - containerd.io
          - docker-compose-plugin
        state: present
        update_cache: yes

    - name: Ajout de l'utilisateur au groupe docker
      user:
        name: "{{ ansible_user }}"
        groups: docker
        append: yes

    - name: Vérification que Docker est actif
      service:
        name: docker
        state: started
        enabled: yes
```

Exécute avec `ansible-playbook -i inventory.ini install-docker.yml` et tes serveurs sont prêts à recevoir des conteneurs.

## Déployer des stacks Docker avec Ansible

Ansible ne fait pas qu'installer : il peut aussi gérer les fichiers et lancer les services. Exemple avec un déploiement de [Proxmox VE Helper Scripts](/proxmox-ve-helper-scripts-community/) ou d'un [dashboard Homer](/homer-dashboard-docker-homelab/) :

```yaml
---
- name: Déploiement du dashboard Homer
  hosts: homelab
  become: yes
  vars:
    homer_dir: /opt/homer
  tasks:
    - name: Création du répertoire Homer
      file:
        path: "{{ homer_dir }}"
        state: directory
        mode: '0755'

    - name: Déploiement du docker-compose.yml
      copy:
        dest: "{{ homer_dir }}/docker-compose.yml"
        content: |
          version: "3.8"
          services:
            homer:
              image: b4bz/homer:latest
              container_name: homer
              volumes:
                - ./assets:/www/assets
              ports:
                - "8080:8080"
              restart: unless-stopped

    - name: Lancement de la stack Homer
      community.docker.docker_compose_v2:
        project_src: "{{ homer_dir }}"
        state: present
```

> **Note :** Le module `community.docker.docker_compose_v2` nécessite la collection Docker : `ansible-galaxy collection install community.docker`

Ansible peut aussi déployer des templates Jinja2 pour générer des configs personnalisées (`nginx.conf`, `.env`, etc.) avant de lancer les conteneurs.

## Organiser avec des rôles

Quand tes playbooks grossissent, tu les découpe en **rôles**. Un rôle est un dossier structuré avec des tâches, des variables, des templates et des handlers.

Structure typique :

```text
roles/
└── docker/
    ├── tasks/
    │   └── main.yml
    ├── handlers/
    │   └── main.yml
    ├── templates/
    │   └── docker-daemon.json.j2
    └── vars/
        └── main.yml
```

Ton playbook devient alors ultra lisible :

```yaml
---
- name: Setup complet du serveur
  hosts: homelab
  become: yes
  roles:
    - base
    - docker
    - monitoring
```

Chaque rôle gère une responsabilité unique. Tu peux les partager entre projets, les publier sur Ansible Galaxy ou les versionner dans un repo Git dédié.

## Astuces pratiques pour ton homelab

### Exécuter sur une seule machine

```bash
ansible-playbook -i inventory.ini setup.yml --limit 192.168.1.10
```

### Mode test (dry-run)

```bash
ansible-playbook -i inventory.ini setup.yml --check --diff
```

### Récupérer des infos sur tes machines

```bash
ansible homelab -i inventory.ini -m setup | less
```

Cela te donne toutes les variables facts (architecture, distribution, RAM, interfaces réseau) exploitables dans tes playbooks via `{{ ansible_architecture }}` ou `{{ ansible_distribution }}`.

### Variables d'environnement et secrets

Ne mets jamais de mots de passe en clair dans tes playbooks. Utilise **Ansible Vault** :

```bash
ansible-vault create secrets.yml
```

Puis charge les variables dans ton playbook :

```yaml
vars_files:
  - secrets.yml
```

Exécute avec :

```bash
ansible-playbook -i inventory.ini setup.yml --ask-vault-pass
```

### Tags pour exécuter partiellement

Ajoute des tags à tes tâches pour ne lancer que ce qui t'intéresse :

```bash
ansible-playbook -i inventory.ini setup.yml --tags docker
```

C'est idéal quand tu veux juste mettre à jour une stack sans refaire toute la config système.

## Ansible vs les alternatives

| Outil | Avantage | Inconvénient |
|-------|----------|--------------|
| **Ansible** | Agentless, YAML simple, très documenté | Peut être lent sur des milliers de machines |
| **Terraform** | Excellent pour le provisionnement cloud (VM, réseau) | Moins adapté à la configuration système |
| **Nix / NixOS** | Reproductibilité totale, rollback intégré | Courbe d'apprentissage abrupte |
| **Bash scripts** | Direct, pas de dépendance | Difficile à maintenir, pas idempotent |

Pour un homelab, Ansible est le meilleur compromis. Si un jour tu provisionnes des VMs dans le cloud, couplé avec Terraform il devient redoutable.

## Conclusion

Ansible transforme ton homelab d'un tas de serveurs gérés à la main en une infrastructure déclarative, reproductible et versionnable. Tu écris ce que tu veux, tu lances une commande, et tes machines se mettent en conformité toutes seules.

Commence avec un playbook simple qui met à jour tes paquets et configure SSH. Puis ajoute l'installation de Docker, le déploiement de tes stacks, et enfin des rôles structurés. En quelques semaines, tu auras une infrastructure que tu pourras reconstruire de zéro en 10 minutes.

L'automatisation n'est pas un luxe réservé aux grandes entreprises. Dans ton homelab, c'est ce qui te permet de tester, casser, et recommencer sans angoisse. Et ça commence aujourd'hui avec un fichier YAML.
