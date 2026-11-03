#!/bin/bash
# Instance jetable : voir triliumnext-knowledge-base-auto-heberge.compose.yml
set -e

for i in $(seq 1 30); do
  curl -sf http://localhost:8097/ >/dev/null && break
  sleep 2
done

PASSWORD="demo-captures-2026"

# Premier lancement (définition du mot de passe du compte unique) puis connexion,
# et sauvegarde de la session pour shot-scraper.
/opt/shots-venv/bin/python3 - <<PY
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    pg = ctx.new_page()
    import sys
    pg.goto("http://localhost:8097/", wait_until="networkidle")
    pg.wait_for_timeout(1500)

    def debug(tag):
        print(f"DEBUG[{tag}] url=", pg.url, file=sys.stderr)
        print(f"DEBUG[{tag}] buttons=", pg.locator("button").all_text_contents(), file=sys.stderr)
        print(f"DEBUG[{tag}] inputs=", [pg.locator("input").nth(i).get_attribute("type") for i in range(pg.locator("input").count())], file=sys.stderr)
        print(f"DEBUG[{tag}] body=", pg.locator("body").inner_text()[:1500], file=sys.stderr)

    debug("1-lang")
    pg.get_by_role("button", name="Continue").first.click()
    pg.wait_for_timeout(1500)
    debug("2-after-continue")

    # Écran de choix : "New knowledge base" / "Connect to an existing server" / ...
    pg.get_by_text("New knowledge base", exact=True).first.click()
    pg.wait_for_timeout(1500)
    debug("3-after-new-kb")

    # "With demo content" / "Empty" : on part vide, les notes de démo sont injectées par ETAPI.
    pg.get_by_text("Empty", exact=True).first.click()
    # Écran de chargement "Preparing your knowledge base" avant le formulaire de mot de passe.
    pg.wait_for_selector('input[type="password"]', timeout=30000)
    debug("3b-after-empty")
    next_btn = pg.get_by_role("button", name="Continue")
    if next_btn.count():
        next_btn.first.click()
        pg.wait_for_timeout(1500)
        debug("3c-after-continue2")

    pw_fields = pg.locator('input[type="password"]')
    if pw_fields.count() >= 2:
        pw_fields.nth(0).fill("$PASSWORD")
        pw_fields.nth(1).fill("$PASSWORD")
        pg.get_by_role("button").last.click()
        pg.wait_for_timeout(3000)
        debug("4-after-password")

    # Écran de connexion (mot de passe seul) après la création du compte.
    pw_fields = pg.locator('input[type="password"]')
    if pw_fields.count() == 1:
        pw_fields.first.fill("$PASSWORD")
        login_btn = pg.get_by_role("button", name="Log in")
        if login_btn.count():
            login_btn.first.click()
        else:
            pg.keyboard.press("Enter")
        pg.wait_for_timeout(3000)
        debug("5-after-login")

    ctx.storage_state(path="/opt/shots/auth/triliumnext-knowledge-base-auto-heberge.json")
    b.close()
PY

# Jeu de notes de démo via l'API ETAPI, pour que l'arborescence ne soit pas vide.
# (diagnostic de la structure de l'arbre, avant de câbler la navigation dans le yml)
TOKEN=$(curl -sf -X POST http://localhost:8097/etapi/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"password\":\"$PASSWORD\"}" | python3 -c "import sys,json;print(json.load(sys.stdin)['authToken'])")

create_note() {
  curl -sf -X POST http://localhost:8097/etapi/create-note \
    -H "Authorization: $TOKEN" -H "Content-Type: application/json" \
    -d "{\"parentNoteId\":\"$1\",\"title\":\"$2\",\"type\":\"text\",\"content\":\"$3\"}" \
    | python3 -c "import sys,json;print(json.load(sys.stdin)['note']['noteId'])"
}

add_label() {
  curl -sf -X POST http://localhost:8097/etapi/attributes \
    -H "Authorization: $TOKEN" -H "Content-Type: application/json" \
    -d "{\"noteId\":\"$1\",\"type\":\"label\",\"name\":\"$2\",\"value\":\"$3\"}" >/dev/null
}

HOMELAB=$(create_note root "Homelab" "<p>Documentation d'infrastructure du homelab.</p>")
create_note root "Dev" "<p>Notes de developpement.</p>" >/dev/null
create_note root "Admin perso" "<p>Administratif personnel.</p>" >/dev/null
VEILLE=$(create_note root "Veille" "<p>Veille technique.</p>")

DOCKER_NOTE=$(create_note "$HOMELAB" "Stack Docker" "<p>Services conteneurises du homelab : images, ports, volumes.</p>")
add_label "$DOCKER_NOTE" techno docker

PROXMOX=$(create_note "$HOMELAB" "Serveur Proxmox" "<p>Version : 8.2<br>Date de deploiement : 2026-03-01<br>Procedure de restauration : voir sauvegarde PBS.</p>")
add_label "$PROXMOX" techno proxmox

RUNBOOK=$(create_note "$HOMELAB" "Runbook : disque plein" "<h2>Symptome</h2><p>Alerte espace disque sous 10 pourcent.</p><h2>Cause</h2><p>Logs Docker non rotates depuis plusieurs semaines.</p><h2>Solution</h2><p>docker system prune -af --volumes</p><h2>Verification</h2><p>df -h</p>")
add_label "$RUNBOOK" statut adopte

create_note "$VEILLE" "A tester : Paperless-ngx" "<p>Outil de GED auto-heberge a tester pour les documents scannes.</p>" >/dev/null

sleep 2

# La navigation par clic JS brut dans shots.yml n'est pas fiable (fancytree n'a pas fini de
# s'hydrater quand le JS s'exécute). On résout ici les vraies URL des notes avec de vrais
# clics Playwright (qui attendent que l'élément soit actionnable), puis on les fige dans
# shots.yml : shot-scraper n'a plus qu'à charger une URL directe, sans cliquer.
HASHES=$(/opt/shots-venv/bin/python3 - <<'PY'
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1440, "height": 900},
                         storage_state="/opt/shots/auth/triliumnext-knowledge-base-auto-heberge.json")
    pg = ctx.new_page()
    pg.goto("http://localhost:8097/", wait_until="networkidle")
    pg.wait_for_timeout(1500)

    pg.locator(".fancytree-title", has_text="Homelab").first.click()
    pg.wait_for_timeout(1500)

    pg.locator("a.note-book-title", has_text="Stack Docker").first.click()
    pg.wait_for_timeout(1500)
    print("DOCKER_HASH=" + pg.url.split("#", 1)[1])

    pg.locator(".fancytree-title", has_text="Homelab").first.click()
    pg.wait_for_timeout(1500)
    pg.locator("a.note-book-title", has_text="Runbook : disque plein").first.click()
    pg.wait_for_timeout(1500)
    print("RUNBOOK_HASH=" + pg.url.split("#", 1)[1])

    # TriliumNext persiste la dernière note active côté compte : sans ce retour explicite,
    # la capture "accueil" (qui visite juste "/") rouvrirait le Runbook au lieu de la racine.
    pg.goto("http://localhost:8097/", wait_until="networkidle")
    pg.wait_for_timeout(1000)
    pg.get_by_text("root", exact=True).first.click()
    pg.wait_for_timeout(1000)
    homelab_title = pg.locator(".fancytree-title", has_text="Homelab").first
    expander = homelab_title.locator("xpath=..").locator(".fancytree-expander")
    if expander.count():
        expander.first.click()
    pg.wait_for_timeout(1000)

    b.close()
PY
)
echo "$HASHES" >&2
DOCKER_HASH=$(echo "$HASHES" | grep '^DOCKER_HASH=' | cut -d= -f2-)
RUNBOOK_HASH=$(echo "$HASHES" | grep '^RUNBOOK_HASH=' | cut -d= -f2-)
test -n "$DOCKER_HASH" || { echo "ÉCHEC : DOCKER_HASH vide" >&2; exit 1; }
test -n "$RUNBOOK_HASH" || { echo "ÉCHEC : RUNBOOK_HASH vide" >&2; exit 1; }
sed -i "s#__DOCKER_URL__#${DOCKER_HASH}#" shots.yml
sed -i "s#__RUNBOOK_URL__#${RUNBOOK_HASH}#" shots.yml
