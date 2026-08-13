---
title: "K3s Docker : Kubernetes léger pour ton homelab"
description: "K3s Docker : déploie Kubernetes léger sur ton homelab en 10 minutes. Installation, kubectl, pods, ingress et migration depuis Docker Compose."
pubDatetime: "2026-08-13T08:00:00.000Z"
modDatetime: "2026-08-13T08:00:00.000Z"
author: Brandon Visca
tags:
  - intermediaire
  - docker
  - kubernetes
  - homelab
  - k3s
featured: false
draft: false
focusKeyword: k3s docker
ogImage: ""
faqs:
  - question: "K3s remplace-t-il Docker ?"
    answer: "Non. K3s utilise containerd comme runtime, mais il peut utiliser les mêmes images Docker. Docker Compose et K3s peuvent coexister sur des machines différentes."
  - question: "Puis-je utiliser K3s sur un seul serveur ?"
    answer: "Oui. Un seul nœud suffit pour commencer. C'est d'ailleurs le cas le plus courant en homelab. Ajouter des workers se fait quand tu as besoin de scalabilité."
  - question: "Quelle différence entre K3s et Kubernetes classique ?"
    answer: "K3s est une distribution allégée : SQLite remplace etcd, containerd remplace Docker, et tous les composants sont dans un seul binaire. C'est Kubernetes conforme, mais plus léger."
  - question: "Comment migrer mes conteneurs Docker Compose vers K3s ?"
    answer: "Les images restent les mêmes. Tu réécris le docker-compose.yml en manifests Kubernetes (Deployment, Service, PVC, Ingress). Les données persistantes s'exportent et s'importent via dump."
---
> 💡 **TL;DR**
> - K3s est une distribution Kubernetes allégée qui tourne sur un Raspberry Pi 4 ou un NUC de 4 Go de RAM
> - Tu gardes tes habitudes Docker : les images restent les mêmes, seul l'orchestrateur change
> - Un seul nœud suffit pour commencer ; ajouter un second prend une commande
> - Traefik est embarqué : tu exposes tes services en HTTPS sans rien installer de plus

## Table des matières

## K3s Docker : qu'est-ce que c'est exactement ?

Rancher a sorti **K3s Docker** en 2019 avec une promesse simple : Kubernetes dans un binaire de moins de 100 Mo. Pas de dizaines de services à installer, pas de etcd séparé, pas de 4 Go de RAM minimum juste pour le plan de contrôle.

K3s remplace les composants lourds de Kubernetes par des alternatives plus légères :

- **SQLite au lieu d'etcd** pour le stockage du cluster (optionnel : tu peux revenir à etcd en multi-nœuds)
- **Flannel embarqué** pour le réseau entre pods, sans CNI à configurer
- **Containerd intégré** comme runtime, pas besoin de Docker daemon séparé
- **Traefik préinstallé** comme ingress controller
- **CoreDNS** pour la résolution DNS interne
- **Metrics-server** pour `kubectl top`

Résultat : tu installes Kubernetes sur un serveur avec 512 Mo de RAM libre. Pas une blague. En homelab, ça change tout. Ton vieux Raspberry Pi 4 ou ton NUC Intel de génération précédente devient un vrai cluster, pas juste une machine qui fait tourner 5 conteneurs en Docker Compose.

Si tu débutes avec les conteneurs, mon guide [Docker pour les débutants](/docker-debutant-services-auto-heberger/) te donne les bases avant de sauter à Kubernetes.

## Pourquoi passer de Docker Compose à K3s ?

Docker Compose reste formidable. Un fichier YAML, une commande, et ton Nextcloud avec sa base PostgreSQL tourne. Mais quand ton homelab grandit, tu rencontres des limites :

**Pas de redémarrage auto sur panne.** Si un conteneur plante, Docker Compose le relance. Si le serveur physique plante, tout s'arrête. Kubernetes reschedule tes pods sur un autre nœud si tu en as plusieurs.

**Pas de rolling update.** Pour mettre à jour une image Docker, tu fais `docker compose pull && docker compose up -d`. Le service est indisponible quelques secondes. Kubernetes fait un rolling update : il démarre la nouvelle version, vérifie la santé, bascule le trafic, puis éteint l'ancienne.

**Pas de scalabilité.** Besoin de deux instances de ton API pour absorber la charge ? Docker Compose ne sait pas faire. Kubernetes oui, avec `kubectl scale deployment/api --replicas=2`.

**Pas de secrets natifs.** Tu colles tes mots de passe en clair dans le `.env` ? Kubernetes a des Secrets chiffrés au repos, intégrés au cluster.

Ce n'est pas pour autant que Docker Compose devient obsolète. Il reste parfait pour des stacks simples sur un seul serveur. Si ton [homelab tourne déjà avec quelques services en Docker](/docker-debutant-services-auto-heberger/), tu n'es pas obligé de tout migrer. K3s cohabite très bien avec Docker : tu peux faire tourner K3s sur une machine et garder Docker Compose sur une autre.

## Prérequis matériels et logiciels

K3s est indulgent, mais il faut quand même un minimum :

- Un serveur sous Linux (Debian 12, Ubuntu 22.04/24.04, ou Alpine pour les téméraires)
- 1 Go de RAM minimum (2 Go recommandés pour être à l'aise)
- 1 cœur CPU (2 recommandés)
- Un accès SSH avec une clé
- Un utilisateur non-root avec `sudo`
- Les ports 6443 (API Kubernetes), 10250 (Kubelet), 2379/2380 (etcd en HA), 8472/udp (Flannel VXLAN)

Pour un cluster de 3 nœuds (1 master + 2 workers), un trio de Raspberry Pi 4 avec 4 Go de RAM chacun suffit amplement. C'est d'ailleurs la config la plus populaire dans les homelabs francophones qui adoptent **K3s Docker**.

## Installation en une ligne

Rancher a optimisé l'installateur au point où une seule commande suffit :

```bash
curl -sfL https://get.k3s.io | sh -
```

Après 30 à 60 secondes, Kubernetes est opérationnel. Tu peux vérifier :

```bash
sudo kubectl get nodes
```

Tu devrais voir ton serveur en statut `Ready`. C'est tout. Pas de kubeadm, pas de certificats à générer manuellement, pas de réseau à configurer.

Pour éviter de taper `sudo` à chaque commande kubectl, ajoute ton utilisateur au groupe et copie le kubeconfig :

```bash
sudo usermod -aG k3s $USER
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $USER:$USER ~/.kube/config
chmod 600 ~/.kube/config
export KUBECONFIG=~/.kube/config
```

Reconnecte-toi en SSH pour que le groupe prenne effet, puis teste :

```bash
kubectl get nodes
```

## Installation de kubectl

K3s installe déjà kubectl sur le serveur, mais si tu veux piloter ton cluster depuis ta machine locale (ton laptop), installe le client officiel :

**macOS :**
```bash
brew install kubectl
```

**Linux :**
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

Puis copie le fichier `~/.kube/config` du serveur vers ta machine locale, dans `~/.kube/config`.

## Ton premier déploiement : Nginx

Kubernetes pense en ressources déclaratives. Tu décris l'état désiré, le control plane s'occupe de le réaliser. Voici le manifeste minimal pour faire tourner Nginx :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-demo
  labels:
    app: nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:alpine
          ports:
            - containerPort: 80
```

Applique-le :

```bash
kubectl apply -f nginx-deployment.yaml
```

Vérifie que le pod tourne :

```bash
kubectl get pods
```

Pour accéder à Nginx depuis l'extérieur, tu as besoin d'un Service. Kubernetes sépare la logique de calcul (Deployment/Pod) de la logique réseau (Service) :

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: LoadBalancer
```

Applique-le aussi :

```bash
kubectl apply -f nginx-service.yaml
```

Avec K3s, le type `LoadBalancer` est géré automatiquement par Klipper, un load balancer léger intégré. Tu obtiens une IP externe sans MetalLB ou autre joyeuseté à configurer.

## Les images Docker dans K3s

Voici la bonne nouvelle : **toutes tes images Docker fonctionnent telles quelles**. K3s Docker utilise containerd comme runtime, qui parle le même langage OCI que Docker. Tu peux utiliser n'importe quelle image Docker Hub, GitHub Container Registry, ou ta registry privée.

Si tu as une image locale que tu as construite avec `docker build`, tu dois la rendre visible à containerd. Deux méthodes :

**1. Push vers une registry** (recommandé en production) :

```bash
docker tag mon-app:latest registry.tondomaine.fr/mon-app:latest
docker push registry.tondomaine.fr/mon-app:latest
```

Puis référence-la dans ton manifeste avec `image: registry.tondomaine.fr/mon-app:latest`.

**2. Import local** (pratique pour les tests) :

```bash
docker save mon-app:latest > mon-app.tar
sudo k3s ctr images import mon-app.tar
```

Attention : containerd n'utilise pas le cache d'images Docker. Les images que tu as en local avec `docker images` ne sont pas visibles par K3s. Il faut explicitement les importer ou les pull depuis une registry.

## Ingress avec Traefik (déjà embarqué)

K3s installe Traefik par défaut comme ingress controller. Tu n'as rien à faire pour l'HTTPS : ajoute un certificat et une règle d'ingress, et le tour est joué.

Voici un exemple complet pour exposer Nginx en HTTPS avec Let's Encrypt :

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nginx-ingress
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: websecure
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  rules:
    - host: nginx.tondomaine.fr
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: nginx-service
                port:
                  number: 80
  tls:
    - hosts:
        - nginx.tondomaine.fr
      secretName: nginx-tls
```

Applique-le :

```bash
kubectl apply -f nginx-ingress.yaml
```

Tu remarqueras que c'est très proche de la logique [Traefik en Docker Compose](/traefik-reverse-proxy-docker/). Les labels Docker deviennent des annotations Kubernetes, mais le concept est identique : un reverse proxy qui découvre automatiquement tes services et gère le HTTPS.

Si tu utilises déjà Traefik avec Docker, la transition vers **K3s Docker** est quasi transparente. Les mêmes concepts de routers, services et middlewares s'appliquent.

## Stockage persistant avec les PersistentVolumes

Contrairement à Docker Compose où tu montes un volume local avec `./data:/var/lib/postgresql/data`, Kubernetes abstrait le stockage via les PersistentVolumes (PV) et PersistentVolumeClaims (PVC).

K3s configure automatiquement un `local-path-provisioner` qui crée des volumes locaux sur le disque du nœud. C'est parfait pour un homelab mono-nœud.

Exemple pour PostgreSQL :

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:16-alpine
          env:
            - name: POSTGRES_USER
              value: "monuser"
            - name: POSTGRES_PASSWORD
              value: "monmotdepasse"
            - name: POSTGRES_DB
              value: "mondb"
          ports:
            - containerPort: 5432
          volumeMounts:
            - name: postgres-storage
              mountPath: /var/lib/postgresql/data
      volumes:
        - name: postgres-storage
          persistentVolumeClaim:
            claimName: postgres-pvc
```

Le PVC demande 5 Go. Le `local-path-provisioner` crée automatiquement un répertoire sur le disque et le monte dans le conteneur. Tu n'as pas à gérer les chemins à la main.

## Multi-nœuds : ajouter un worker

C'est là que Kubernetes devient intéressant. Ton premier nœud est le master. Pour ajouter un worker, récupère le token sur le master :

```bash
sudo cat /var/lib/rancher/k3s/server/node-token
```

Sur le nouveau serveur, exécute :

```bash
curl -sfL https://get.k3s.io | K3S_URL=https://IP_DU_MASTER:6443 K3S_TOKEN=TON_TOKEN sh -
```

En 30 secondes, le nouveau nœud apparaît dans `kubectl get nodes`. Kubernetes peut désormais répartir tes pods entre les deux machines. Si un nœud tombe, les pods sont reschedulés sur l'autre (pour les deployments avec `replicas > 1`).

Pour un homelab, deux nœuds suffisent pour apprendre et tester la haute disponibilité. Trois nœuds sont recommandés pour l'etcd en mode HA, mais ce n'est pas obligatoire avec SQLite.

## Monitoring basique avec kubectl top

K3s embarque le metrics-server. Tu peux surveiller la consommation de tes pods sans installer Prometheus :

```bash
kubectl top nodes
kubectl top pods
kubectl top pods --all-namespaces
```

Pour aller plus loin, installe le stack Prometheus + Grafana avec Helm :

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack
```

Mais honnêtement, pour un homelab modeste, `kubectl top` + un dashboard comme [Beszel](/beszel-monitoring-docker/) en parallèle suffisent largement.

## Mise à jour de K3s

Rancher gère les mises à jour simplement. Pour upgrader K3s :

```bash
sudo /usr/local/bin/k3s-killall.sh
curl -sfL https://get.k3s.io | sh -
```

Ou utilise l'outil officiel `k3sup` pour des clusters plus complexes. Pour un homelab mono-nœud, la réinstallation par-dessus fonctionne sans perte de données (les PV locaux sont conservés).

## Automatiser avec Ansible

Si tu as plusieurs nœuds, tu ne veux pas te connecter en SSH à chacun pour lancer la mise à jour. C'est là qu'Ansible entre en jeu. Tu peux automatiser l'installation de K3s, le déploiement des manifests et les mises à jour depuis un seul playbook.

Si Ansible est nouveau pour toi, mon guide [Ansible 101 pour homelab](/ansible-101-homelab-yaml/) explique comment écrire des playbooks qui installent Docker, déploient des stacks et configurent SSH. Le même principe s'applique à K3s : un inventaire, un playbook, exécution sur tous les nœuds en parallèle.

Exemple de tâche Ansible pour installer K3s sur tous les nœuds :

```yaml
- name: Installer K3s
  hosts: k3s_cluster
  become: yes
  tasks:
    - name: Télécharger et installer K3s
      shell: |
        curl -sfL https://get.k3s.io | sh -
      args:
        creates: /usr/local/bin/k3s

    - name: Attendre que le nœud soit Ready
      shell: kubectl get nodes
      register: nodes
      until: "'Ready' in nodes.stdout"
      retries: 10
      delay: 5
```

## Migration progressive depuis Docker Compose

Tu n'es pas obligé de tout migrer d'un coup. Voici une stratégie réaliste :

1. Garde tes stacks Docker Compose existantes sur ton serveur principal
2. Installe K3s sur une nouvelle machine (ou une VM)
3. Déploie un ou deux services neufs sur K3s pour apprendre
4. Migre les services un par un en réécrivant leurs `docker-compose.yml` en manifests Kubernetes
5. Quand tu es à l'aise, bascule tout sur K3s et garde Docker Compose comme backup

Les concepts se traduisent facilement :

| Docker Compose | Kubernetes |
|---|---|
| `docker-compose.yml` | Manifestes YAML (`deployment.yaml`, `service.yaml`) |
| `services:` | `Deployment` |
| `ports:` | `Service` de type `LoadBalancer` ou `NodePort` |
| `volumes:` | `PersistentVolumeClaim` |
| `networks:` | Géré automatiquement par CNI (Flannel) |
| `environment:` | `ConfigMap` ou variables d'env directes |
| `secrets:` | `Secret` Kubernetes |
| `restart: always` | `restartPolicy: Always` (défaut dans Deployment) |

Pour les services stateless (pas de base de données locale), la migration est quasi mécanique. Pour les bases de données, exporte le dump, recrée le PVC sous K3s, importe le dump.

## Quand ne PAS utiliser K3s

K3s n'est pas la solution universelle. Reste sur Docker Compose si :

- Tu n'as qu'un seul serveur et moins de 10 services. La complexité de Kubernetes n'est pas justifiée.
- Tu dois partager des fichiers entre conteneurs via des bind mounts simples. Kubernetes abstrait le stockage, c'est plus verbeux pour des cas basiques.
- Ton équipe ne connaît pas Kubernetes et n'a pas le temps d'apprendre.
- Tu fais du développement local itératif. `docker compose up` est plus rapide que `kubectl apply + wait + logs`.

Kubernetes devient pertinent quand tu as plusieurs machines, besoin de HA, de scalabilité, ou que tu veux apprendre un standard industriel. Pour un homelab personnel modeste, c'est aussi un terrain de jeu formidable.

## Conclusion

K3s abaisse drastiquement la barrière d'entrée à Kubernetes. En une ligne de commande, tu obtiens un cluster fonctionnel avec réseau, ingress et stockage persistant. Tes images Docker restent utilisables telles quelles. Tu peux commencer sur un seul nœud et ajouter des workers quand tu veux.

Le passage de Docker Compose à Kubernetes n'est pas une révolution, c'est une évolution. Les concepts sont les mêmes : conteneurs, réseaux, volumes, reverse proxy. Seule la syntaxe et l'orchestrateur changent. Et une fois que tu as goût à `kubectl rollout status` et aux rolling updates sans coupure, retourner à Docker Compose pour une infrastructure complexe devient difficile.

K3s est le meilleur compromis entre la puissance de Kubernetes et la simplicité d'un homelab auto-hébergé. Installe-le ce weekend, déploie un Nginx, et constate par toi-même que Kubernetes n'est pas réservé aux équipes DevOps des grandes entreprises.
