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
