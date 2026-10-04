#!/bin/bash
# Fichiers de démo, puis connexion pour enregistrer la session de shot-scraper.
set -e
mkdir -p files/Documents/Factures files/Photos/Vacances-2026 files/Projets/homelab files/Sauvegardes
python3 - <<'PY'
import struct, zlib, os
def png(path, w, h, c1, c2):
    rows = b"".join(b"\x00" + bytes(
        [int(c1[k] + (c2[k] - c1[k]) * y / h) for x in range(w) for k in range(3)]) for y in range(h))
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) \
        + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b"")
    open(path, "wb").write(data)
cols = [((30,90,160),(240,180,90)), ((20,120,90),(200,230,160)), ((90,40,120),(240,120,140)), ((10,40,70),(120,190,230))]
for i, (a, b) in enumerate(cols, 1):
    png(f"files/Photos/Vacances-2026/plage-{i:02d}.png", 640, 420, a, b)
docs = {
    "files/Documents/Factures/facture-2026-09-electricite.pdf": 180_000,
    "files/Documents/Factures/facture-2026-09-internet.pdf": 95_000,
    "files/Documents/contrat-location.pdf": 420_000,
    "files/Projets/homelab/docker-compose.yml": 2_400,
    "files/Projets/homelab/notes-reseau.md": 6_100,
    "files/Sauvegardes/vaultwarden-2026-10-01.tar.gz": 12_000_000,
    "files/Sauvegardes/nextcloud-db-2026-10-01.sql.gz": 48_000_000,
}
for p, n in docs.items():
    with open(p, "wb") as f: f.write(os.urandom(n))
open("files/Documents/liste-courses.txt", "w").write("Lait\nPain\nCafé\n")
PY
chown -R 1000:1000 files
for i in $(seq 1 30); do curl -sf -o /dev/null http://localhost:8090/health && break; sleep 2; done
/opt/shots-venv/bin/python3 - <<'PY'
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": 1440, "height": 900}); pg = ctx.new_page()
    pg.goto("http://localhost:8090/login", wait_until="networkidle")
    f = pg.locator("input:visible").all(); f[0].fill("admin"); f[1].fill("demo-captures-2026")
    pg.keyboard.press("Enter"); pg.wait_for_url(lambda u: "/login" not in u, timeout=20000)
    pg.wait_for_timeout(1500)
    ack = pg.get_by_text("Acknowledge")
    if ack.count(): ack.first.click(); pg.wait_for_timeout(800)
    ctx.storage_state(path="/opt/shots/auth/filebrowser-quantum.json"); b.close()
PY
