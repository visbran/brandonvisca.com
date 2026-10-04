#!/bin/bash
# Fichiers de démo dans le dossier partagé (monté sur /w), puis attente du service.
set -e
mkdir -p files/photos/vacances-2026 files/documents files/musique files/depot
python3 - <<'PY'
import struct, zlib, os
def png(path, w, h, c1, c2):
    rows = b"".join(b"\x00" + bytes(
        [int(c1[k] + (c2[k] - c1[k]) * y / h) for x in range(w) for k in range(3)]) for y in range(h))
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    open(path, "wb").write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                           + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b""))
cols = [((30,90,160),(240,180,90)), ((20,120,90),(200,230,160)), ((90,40,120),(240,120,140)),
        ((10,40,70),(120,190,230)), ((150,60,30),(250,210,120)), ((40,40,40),(200,200,210))]
for i, (a, b) in enumerate(cols, 1):
    png(f"files/photos/vacances-2026/plage-{i:02d}.png", 640, 420, a, b)
for p, n in {"files/documents/contrat-location.pdf": 420_000, "files/documents/facture-internet-2026-09.pdf": 95_000,
             "files/musique/playlist-ete.m3u": 900}.items():
    with open(p, "wb") as f: f.write(os.urandom(n))
PY
chown -R 1000:1000 files
for i in $(seq 1 40); do curl -sf -o /dev/null "http://localhost:3923/?reset=/._" && break; sleep 2; done
# Laisse l'indexeur passer et génère les miniatures avant les captures
sleep 4
for i in 01 02 03 04 05 06; do curl -s -o /dev/null "http://localhost:3923/photos/vacances-2026/plage-$i.png?th=w&pw=demo-captures-2026"; done
sleep 2
