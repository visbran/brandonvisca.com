#!/bin/bash
# Attendre que Dozzle réponde, puis générer quelques logs à afficher.
for i in $(seq 1 30); do
  curl -sf http://localhost:8081/ >/dev/null && break
  sleep 2
done
docker exec web-frontend sh -c 'for i in $(seq 1 12); do wget -q -O /dev/null http://localhost/; done' 2>/dev/null || true
docker exec cache-redis sh -c 'redis-cli set demo ok >/dev/null; redis-cli get demo >/dev/null' 2>/dev/null || true
sleep 3
