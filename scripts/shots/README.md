# Captures d'écran automatisées

Les captures des articles sont prises par le LXC `shots` (109, `192.168.50.9`), qui est sur le LAN et
joint donc les services du homelab sans qu'ils soient exposés.

## Prendre les captures d'un article

```bash
pnpm shots <slug>          # lit scripts/shots/<slug>.yml
pnpm shots <slug> --force  # refait même les images déjà présentes
```

Le script envoie le YAML au conteneur, lance `shot-scraper multi --retina`, rapatrie les PNG,
les convertit en WebP 1600 px et les range dans `src/data/blog/`, nommées `<slug>-<n>.webp`.

## Instance jetable plutôt que ta production (recommandé)

La plupart des articles sont des tutoriels : le lecteur doit voir l'interface **telle qu'il la
découvrira après l'installation**, pas ta prod. Trois fichiers, les deux derniers optionnels :

| Fichier | Rôle |
|---|---|
| `<slug>.yml` | les captures (format shot-scraper) |
| `<slug>.compose.yml` | instance jetable, démarrée avant et **détruite après** (`down -v`) |
| `<slug>.setup.sh` | tourne sur le runner une fois l'instance up : attendre, créer le compte admin, injecter des données de démo |

Avantages : aucun compte à gérer par outil, aucune donnée personnelle à masquer, captures
reproductibles (image épinglée), et fidèles au tutoriel. Exemple complet :
`dozzle-docker-visionneuse-logs-web.*`.

Bonnes pratiques :

- `container_name:` explicite pour chaque service — les noms générés par Compose apparaissent dans
  certaines interfaces et trahissent l'infra.
- Le projet Compose s'appelle `demo` : lisible dans les UI, mais **une seule recette à la fois**.
- `--keep` laisse l'instance en vie pour mettre une recette au point ; à détruire ensuite à la main.
- Les ports publiés sont locaux au runner : les captures pointent sur `http://localhost:<port>`.

**Le compte dédié sur un service de prod ne se justifie que** si l'article montre des données réelles
accumulées (statistiques Tianji, bibliothèque Immich). Sinon, instance jetable.

## Écrire une recette

Un fichier par article : `scripts/shots/<slug>.yml`.

```yaml
- output: tianji-dashboard.png
  url: http://192.168.50.8:12345/dashboard
  width: 1440
  wait_for: document.querySelectorAll('.echarts-for-react').length > 0
  alt: "Tableau de bord Tianji affichant les visites des 7 derniers jours"
  javascript: |
    // masquer ce qui ne doit pas être publié
    document.querySelectorAll('[data-email]').forEach(e => e.textContent = 'demo@example.com');
```

Clés utiles (doc complète : <https://shot-scraper.datasette.io/en/stable/multi.html>) :

| Clé | Usage |
|---|---|
| `url`, `output` | obligatoires |
| `width`, `height` | fenêtre ; sans `height`, la page entière est capturée |
| `selector`, `selectors`, `padding` | cadrer sur un élément plutôt que la page |
| `wait`, `wait_for` | attendre un délai ou une condition JS (graphiques, chargement) |
| `javascript` | exécuter du JS avant la capture (masquage, thème, faux jeu de données) |
| `alt` | **spécifique à ce dépôt** : le texte alternatif recopié dans le Markdown |

## Services authentifiés

Les sessions vivent sur le conteneur, dans `/opt/shots/auth/<service>.json`, jamais dans le dépôt.
Pour Tianji : `/opt/shots/tianji_login.py` relit `/etc/shots/tianji.env` et régénère la session.
Ajouter `auth: tianji` dans une entrée YAML pour l'utiliser.

## Avant de publier une capture

Le conteneur photographie **tes** services : vérifie toujours l'image avant de la committer
(adresses IP publiques, e-mails, noms de machines, jetons visibles dans une URL).
Le bloc `javascript:` sert à masquer ces éléments à la source.
