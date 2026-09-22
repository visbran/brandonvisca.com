#!/bin/bash
# Prépare une instance Tianji jetable pour les captures de l'article :
# compte de démo, un site, et 7 jours de visites synthétiques.
set -e
BASE="http://localhost:12346"

echo "· attente du démarrage de Tianji"
for i in $(seq 1 60); do
  curl -sf -o /dev/null "$BASE/" && break
  sleep 3
done

echo "· compte de démo + session"
/opt/shots/login.py "$BASE" demo demo1234 /opt/shots/auth/tianji-demo.json --register

echo "· site + 7 jours de visites synthétiques"
docker exec -i tianji-db psql -U tianji -d tianji -v ON_ERROR_STOP=1 <<'SQL'
-- Le site, rattaché au workspace du compte de démo
INSERT INTO "Website" (id, "workspaceId", name, domain, "createdAt", "updatedAt")
SELECT 'demo-website-0001', u."currentWorkspaceId", 'mon-blog.fr', 'mon-blog.fr', now() - interval '30 days', now()
FROM "User" u WHERE u.username = 'demo'
ON CONFLICT (id) DO NOTHING;

-- ~420 sessions réparties sur 7 jours, avec un creux la nuit
INSERT INTO "WebsiteSession" (id, "websiteId", hostname, browser, os, device, screen, language, country, city, "createdAt")
SELECT
  gen_random_uuid(), 'demo-website-0001', 'mon-blog.fr',
  (ARRAY['chrome','firefox','safari','edge'])[1 + floor(random()*4)],
  (ARRAY['Linux','Windows 11','macOS','Android','iOS'])[1 + floor(random()*5)],
  (ARRAY['desktop','desktop','mobile','laptop'])[1 + floor(random()*4)],
  (ARRAY['1920x1080','2560x1440','390x844','1440x900'])[1 + floor(random()*4)],
  (ARRAY['fr-FR','fr-FR','fr-BE','en-US'])[1 + floor(random()*4)],
  (ARRAY['FR','FR','FR','BE','CH','CA'])[1 + floor(random()*6)],
  (ARRAY['Paris','Lyon','Marseille','Bruxelles','Genève','Montréal'])[1 + floor(random()*6)],
  now() - (random() * interval '7 days')
FROM generate_series(1, 420);

-- 2 à 5 pages vues par session (1 seule = rebond, et un dashboard à 100 % de rebond fait mauvais effet)
INSERT INTO "WebsiteEvent" (id, "websiteId", "sessionId", "urlPath", "referrerDomain", "pageTitle", "eventType", "createdAt")
SELECT
  left(md5(random()::text || clock_timestamp()::text), 30),
  'demo-website-0001', s.id,
  (ARRAY['/','/docker-debutant/','/auto-hebergement-guide/','/nginx-reverse-proxy/','/blog/','/a-propos/'])[1 + floor(random()*6)],
  (ARRAY['google.com','google.com','news.ycombinator.com','reddit.com',''])[1 + floor(random()*5)],
  (ARRAY['Accueil','Docker pour débutants','Guide auto-hébergement','Nginx en reverse proxy','Blog','À propos'])[1 + floor(random()*6)],
  1,
  s."createdAt" + (random() * interval '6 minutes')
FROM "WebsiteSession" s, generate_series(1, 2 + floor(random()*4)::int)
WHERE s."websiteId" = 'demo-website-0001';
SQL

echo "· données prêtes"
sleep 2
