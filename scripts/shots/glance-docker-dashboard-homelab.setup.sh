#!/bin/bash
# Attendre que Glance réponde, puis laisser le temps aux widgets Docker et monitor
# d'interroger le socket Docker et les services de démo.
for i in $(seq 1 30); do
  curl -sf http://localhost:8080/ >/dev/null && break
  sleep 2
done
sleep 6
