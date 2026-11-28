#!/bin/bash
# Installation non interactive d'iTop (setup/unattended-install), avec données de
# démonstration, puis connexion pour enregistrer la session de shot-scraper.
set -euo pipefail

for i in $(seq 1 60); do
  curl -sf -o /dev/null http://localhost:8080/ && break
  sleep 2
done

docker exec -u www-data -i itop-shots sh -c 'cat > /tmp/fresh-install.xml' <<'XMLEOF'
<?xml version="1.0" encoding="UTF-8"?>
<installation>
  <mode>install</mode>
  <optional_steps>
    <log-parameters>1</log-parameters>
    <migrate-before>1</migrate-before>
    <migrate-after>1</migrate-after>
    <copy>1</copy>
  </optional_steps>
  <source_dir>datamodels/2.x/</source_dir>
  <datamodel_version>3.3.0</datamodel_version>
  <extensions_dir>extensions</extensions_dir>
  <target_env>production</target_env>
  <workspace_dir></workspace_dir>
  <database>
    <server>db</server>
    <user>itop</user>
    <pwd>changeme_itop</pwd>
    <name>itop</name>
    <db_tls_enabled></db_tls_enabled>
    <db_tls_ca></db_tls_ca>
    <prefix></prefix>
  </database>
  <url>http://localhost:8080/</url>
  <graphviz_path>/usr/bin/dot</graphviz_path>
  <admin_account>
    <user>admin</user>
    <pwd>changeme_admin</pwd>
    <language>FR FR</language>
  </admin_account>
  <language>FR FR</language>
  <selected_modules type="array">
    <item>itop-structure</item>
    <item>itop-profiles-itil</item>
    <item>authent-local</item>
    <item>itop-config</item>
    <item>itop-config-mgmt</item>
    <item>itop-datacenter-mgmt</item>
    <item>itop-storage-mgmt</item>
    <item>itop-virtualization-mgmt</item>
    <item>itop-endusers-devices</item>
    <item>itop-service-mgmt</item>
    <item>itop-container-mgmt</item>
    <item>itop-request-mgmt-itil</item>
    <item>itop-incident-mgmt-itil</item>
    <item>itop-problem-mgmt</item>
    <item>itop-change-mgmt-itil</item>
    <item>itop-knownerror-mgmt</item>
    <item>itop-tickets</item>
    <item>itop-welcome-itil</item>
    <item>itop-full-itil</item>
    <item>itop-portal</item>
    <item>itop-portal-base</item>
    <item>itop-faq-light</item>
    <item>itop-sla-computation</item>
    <item>itop-attachments</item>
    <item>itop-flow-map</item>
    <item>itop-backup</item>
    <item>itop-files-information</item>
    <item>itop-ui-copypaste</item>
    <item>itop-attribute-class-set</item>
    <item>itop-attribute-encrypted-password</item>
    <item>itop-themes-compat</item>
    <item>itop-bridge-cmdb-ticket</item>
    <item>itop-bridge-cmdb-services</item>
    <item>itop-bridge-datacenter-mgmt-services</item>
    <item>itop-bridge-storage-mgmt-services</item>
    <item>itop-bridge-virtualization-mgmt-services</item>
    <item>itop-bridge-virtualization-storage</item>
    <item>itop-bridge-endusers-devices-services</item>
    <item>combodo-db-tools</item>
    <item>combodo-attributes-visual-beautifier</item>
    <item>combodo-data-feature-removal</item>
    <item>combodo-my-account</item>
    <item>combodo-my-account-user-info</item>
    <item>combodo-password-expiration</item>
  </selected_modules>
  <selected_extensions type="array">
  </selected_extensions>
  <sample_data>1</sample_data>
  <old_addon></old_addon>
  <options type="array"/>
  <mysql_bindir></mysql_bindir>
  <selected_modules type="array">
    <item>itop-structure</item>
    <item>itop-profiles-itil</item>
    <item>authent-local</item>
    <item>itop-config</item>
    <item>itop-config-mgmt</item>
    <item>itop-datacenter-mgmt</item>
    <item>itop-storage-mgmt</item>
    <item>itop-virtualization-mgmt</item>
    <item>itop-endusers-devices</item>
    <item>itop-service-mgmt</item>
    <item>itop-container-mgmt</item>
    <item>itop-request-mgmt-itil</item>
    <item>itop-incident-mgmt-itil</item>
    <item>itop-problem-mgmt</item>
    <item>itop-change-mgmt-itil</item>
    <item>itop-knownerror-mgmt</item>
    <item>itop-tickets</item>
    <item>itop-welcome-itil</item>
    <item>itop-full-itil</item>
    <item>itop-portal</item>
    <item>itop-portal-base</item>
    <item>itop-faq-light</item>
    <item>itop-sla-computation</item>
    <item>itop-attachments</item>
    <item>itop-flow-map</item>
    <item>itop-backup</item>
    <item>itop-files-information</item>
    <item>itop-ui-copypaste</item>
    <item>itop-attribute-class-set</item>
    <item>itop-attribute-encrypted-password</item>
    <item>itop-themes-compat</item>
    <item>itop-bridge-cmdb-ticket</item>
    <item>itop-bridge-cmdb-services</item>
    <item>itop-bridge-datacenter-mgmt-services</item>
    <item>itop-bridge-storage-mgmt-services</item>
    <item>itop-bridge-virtualization-mgmt-services</item>
    <item>itop-bridge-virtualization-storage</item>
    <item>itop-bridge-endusers-devices-services</item>
    <item>combodo-db-tools</item>
    <item>combodo-attributes-visual-beautifier</item>
    <item>combodo-data-feature-removal</item>
    <item>combodo-my-account</item>
    <item>combodo-my-account-user-info</item>
    <item>combodo-password-expiration</item>
  </selected_modules>
  <selected_extensions type="array">
  </selected_extensions>
  <use_symbolic_links>off</use_symbolic_links>
</installation>
XMLEOF

echo "--- extensions disponibles ---"
docker exec itop-shots find /var/www/html/extensions -maxdepth 1 2>&1
echo "--- datamodels/2.x ---"
docker exec itop-shots find /var/www/html/datamodels/2.x -maxdepth 1 2>&1

docker exec -u www-data -w /var/www/html itop-shots \
  php setup/unattended-install/unattended-install.php --param-file=/tmp/fresh-install.xml

/opt/shots-venv/bin/python3 - <<'PY'
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={"width": 1440, "height": 900}); pg = ctx.new_page()
    pg.goto("http://localhost:8080/pages/UI.php", wait_until="networkidle")
    f = pg.locator("input:visible").all(); f[0].fill("admin"); f[1].fill("changeme_admin")
    pg.keyboard.press("Enter")
    pg.wait_for_url(lambda u: "login" not in u, timeout=20000)
    pg.wait_for_timeout(2000)
    ctx.storage_state(path="/opt/shots/auth/itop-docker-cmdb-gestion-parc.json")
    b.close()
PY
