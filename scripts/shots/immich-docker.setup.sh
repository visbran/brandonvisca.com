#!/bin/bash
# Prépare une instance Immich jetable pour les captures de l'article :
# compte admin de démo, onboarding passé, une vingtaine de photos libres
# (picsum.photos, licence Unsplash) étalées sur plusieurs mois.
set -e
BASE="http://localhost:2283"
API="$BASE/api"
AUTH_FILE=/opt/shots/auth/immich-demo.json
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

echo "· attente du démarrage d'Immich"
for i in $(seq 1 100); do
  curl -sf -o /dev/null "$API/server/ping" && break
  sleep 3
done
curl -sf -o /dev/null "$API/server/ping" || { echo "Immich ne répond pas"; exit 1; }

echo "· compte admin de démo"
curl -sf -X POST "$API/auth/admin-sign-up" -H 'Content-Type: application/json' \
  -d '{"email":"admin@exemple.fr","password":"demo1234","name":"Brandon"}' >/dev/null

TOKEN=$(curl -sf -X POST "$API/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"admin@exemple.fr","password":"demo1234"}' \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["accessToken"])')
H="Authorization: Bearer $TOKEN"

echo "· onboarding marqué comme fait"
curl -s -o /dev/null -X PUT "$API/users/me/onboarding" -H "$H" -H 'Content-Type: application/json' -d '{"isOnboarded":true}' || true
curl -s -o /dev/null -X POST "$API/system-metadata/admin-onboarding" -H "$H" -H 'Content-Type: application/json' -d '{"isOnboarded":true}' || true

echo "· clé API d'exemple (seul son nom apparaît dans la liste)"
curl -sf -o /dev/null -X POST "$API/api-keys" -H "$H" -H 'Content-Type: application/json' \
  -d '{"name":"immich-go","permissions":["all"]}'

echo "· photos de démo"
i=0
for id in 10 11 15 16 17 18 28 29 37 42 43 49 54 57 58 64 65 76 82 84 88 96 100 101; do
  i=$((i+1))
  f="$WORK/photo-$id.jpg"
  curl -sfL "https://picsum.photos/id/$id/1600/1067" -o "$f"
  # Dates étalées sur ~8 mois pour une timeline crédible
  d=$(date -u -d "-$((i * 10)) days 14:$((i % 60)):00" +%Y-%m-%dT%H:%M:%S.000Z)
  curl -sf -X POST "$API/assets" -H "$H" \
    -F "assetData=@$f" -F "deviceAssetId=demo-$id" -F "deviceId=demo" \
    -F "fileCreatedAt=$d" -F "fileModifiedAt=$d" >/dev/null \
    || { echo "upload refusé pour $id :"; curl -s -X POST "$API/assets" -H "$H" \
         -F "assetData=@$f" -F "deviceAssetId=demo-$id-b" -F "deviceId=demo" \
         -F "fileCreatedAt=$d" -F "fileModifiedAt=$d"; echo; exit 1; }
done

echo "· session navigateur pour shot-scraper"
/opt/shots-venv/bin/python3 - "$AUTH_FILE" <<'PY'
import sys
from playwright.sync_api import sync_playwright
out = sys.argv[1]
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto("http://localhost:2283/auth/login", wait_until="networkidle")
    page.fill("#email", "admin@exemple.fr")
    page.fill("#password", "demo1234")
    page.click("button[type=submit]")
    page.wait_for_url(lambda u: "/auth/" not in u, timeout=20000)
    page.wait_for_load_state("networkidle")
    ctx.storage_state(path=out)
    b.close()
PY

echo "· attente de la génération des vignettes"
sleep 25
echo "· données prêtes"
