#!/bin/bash
# Compte admin via /setup, puis une vraie conversion (PNG -> JPG) pour peupler l'historique.
set -e
python3 - <<'PY'
import struct, zlib
def png(path, w, h, c1, c2):
    rows = b"".join(b"\x00" + bytes(
        [int(c1[k] + (c2[k] - c1[k]) * y / h) for x in range(w) for k in range(3)]) for y in range(h))
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) \
        + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b"")
    open(path, "wb").write(data)
png("photo-vacances.png", 640, 420, (30, 90, 160), (240, 180, 90))
PY

for i in $(seq 1 30); do curl -sfo /dev/null http://localhost:8099/ && break; sleep 2; done

/opt/shots-venv/bin/python3 - <<'PY'
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8099"

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    pg = ctx.new_page()

    # Premier compte : /setup redirige automatiquement au premier lancement.
    pg.goto(f"{BASE}/", wait_until="networkidle")
    pg.fill("input[name=email]", "demo@example.com")
    pg.fill("input[name=password]", "demo-captures-2026")
    pg.keyboard.press("Enter")
    pg.wait_for_url(lambda u: "/setup" not in u and "/register" not in u and "/login" not in u, timeout=20000)
    pg.wait_for_load_state("networkidle")

    # Upload d'une image de démo puis conversion réelle, pour avoir une ligne "Done" dans l'historique.
    pg.set_input_files("input[name=file]", "photo-vacances.png")
    pg.wait_for_selector("#file-list tr")
    pg.wait_for_selector(".convert_to_group", state="attached", timeout=15000)
    pg.wait_for_timeout(1000)
    pg.click("input[name=convert_to_search]")
    pg.wait_for_selector(".convert_to_popup.flex .convert_to_target button.target", timeout=10000)
    pg.click(".convert_to_popup.flex .convert_to_target button.target >> nth=0")
    pg.wait_for_timeout(1500)
    pg.click("input[type=submit][value=Convert]")
    pg.wait_for_timeout(6000)

    pg.goto(f"{BASE}/history", wait_until="networkidle")
    pg.wait_for_selector("text=Done", timeout=30000)

    ctx.storage_state(path="/opt/shots/auth/convertx-convertisseur-fichiers-auto-heberge.json")
    b.close()
PY
