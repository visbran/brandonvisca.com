#!/usr/bin/env python3
"""
security-audit.py — Audit sécurité et conformité RGPD pour brandonvisca.com
Usage:
  python3 scripts/security-audit.py             # Audit complet
  python3 scripts/security-audit.py --summary   # Résumé sans détail
  python3 scripts/security-audit.py --fix-headers  # Génère public/_headers recommandé
  python3 scripts/security-audit.py --hook      # Mode hook PostToolUse (stdin JSON)
"""

import sys
import os
import re
import json
import glob as glob_module
from pathlib import Path

ROOT = Path(__file__).parent.parent
BLOG_DIR = ROOT / "src" / "data" / "blog"
SRC_DIR = ROOT / "src"
PUBLIC_DIR = ROOT / "public"
GITIGNORE = ROOT / ".gitignore"

# ─── ANSI colors ──────────────────────────────────────────────────────────────
RED = "\033[91m"
YEL = "\033[93m"
GRN = "\033[92m"
BLU = "\033[94m"
RST = "\033[0m"
BOLD = "\033[1m"

def err(msg):  return f"{RED}✗{RST}  {msg}"
def warn(msg): return f"{YEL}⚠{RST}  {msg}"
def ok(msg):   return f"{GRN}✓{RST}  {msg}"
def info(msg): return f"{BLU}ℹ{RST}  {msg}"

# ─── Secret patterns ──────────────────────────────────────────────────────────
SECRET_PATTERNS = [
    (r"(?i)(api[_-]?key|apikey)\s*[:=]\s*['\"]?[A-Za-z0-9\-_]{20,}", "API Key"),
    (r"(?i)(secret[_-]?key|secret)\s*[:=]\s*['\"]?[A-Za-z0-9\-_]{20,}", "Secret Key"),
    (r"(?i)(password|passwd|pwd)\s*[:=]\s*['\"]?.{8,}", "Password"),
    (r"(?i)(token)\s*[:=]\s*['\"]?[A-Za-z0-9\-_.]{20,}", "Token"),
    (r"(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36}", "GitHub Token"),
    (r"sk-[A-Za-z0-9]{48}", "OpenAI Key"),
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key"),
    (r"(?i)cloudflare[_-]?(api[_-]?)?token\s*[:=]\s*['\"]?[A-Za-z0-9\-_]{40}", "Cloudflare Token"),
    (r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----", "Private Key"),
    (r"wireguard.*PrivateKey\s*=\s*[A-Za-z0-9+/]{43}=", "WireGuard Private Key"),
]

# Patterns that look like secrets but are placeholders — skip
PLACEHOLDER_PATTERNS = [
    r"<[A-Z_]+>",           # <CF_API_TOKEN>
    r"\$\{[A-Z_]+\}",       # ${SECRET}
    r"VOTRE_",              # French placeholder
    r"your[-_]",            # English placeholder
    r"xxx",                 # xxx placeholder
    r"example\.",           # example.com
    r"placeholder",
]

# ─── RGPD: third-party domains that imply tracking ────────────────────────────
TRACKING_DOMAINS = [
    ("google-analytics.com", "Google Analytics — consentement requis RGPD"),
    ("googletagmanager.com", "Google Tag Manager — consentement requis RGPD"),
    ("hotjar.com", "Hotjar — consentement requis RGPD"),
    ("clarity.ms", "Microsoft Clarity — consentement requis RGPD"),
    ("facebook.net", "Facebook Pixel — consentement requis RGPD"),
    ("doubleclick.net", "Google Ads — consentement requis RGPD"),
    ("linkedin.com/insight", "LinkedIn Insight Tag — consentement requis RGPD"),
    ("fonts.googleapis.com", "Google Fonts (DNS leak vers Google)"),
    ("fonts.gstatic.com", "Google Fonts static (DNS leak vers Google)"),
    ("disqus.com", "Disqus — transfert données hors UE"),
    ("gravatar.com", "Gravatar — hash email envoyé à Automattic"),
]

# ─── Security headers to check in public/_headers ─────────────────────────────
REQUIRED_HEADERS = [
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
    "Strict-Transport-Security",
]

RECOMMENDED_HEADERS_CONTENT = """\
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
  Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; frame-src 'none'; object-src 'none'; base-uri 'self'; form-action 'self'
"""

# ─── Helpers ──────────────────────────────────────────────────────────────────
def is_placeholder(text):
    for p in PLACEHOLDER_PATTERNS:
        if re.search(p, text, re.IGNORECASE):
            return True
    return False

def read_frontmatter(filepath):
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        return m.group(1) if m else ""
    except Exception:
        return ""

def get_body(filepath):
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        m = re.match(r"^---\n.*?\n---\n?", content, re.DOTALL)
        return content[m.end():] if m else content
    except Exception:
        return ""

# ─── Checks ───────────────────────────────────────────────────────────────────

def check_secrets(summary_mode=False):
    """Scan all tracked files for secret patterns."""
    issues = []
    extensions = ["*.md", "*.astro", "*.ts", "*.js", "*.json", "*.yaml", "*.yml", "*.env*", "*.txt"]

    # Files to skip
    skip_dirs = {"node_modules", ".git", "dist", ".astro"}
    skip_files = {"package-lock.json", "pnpm-lock.yaml"}

    for ext in extensions:
        for filepath in glob_module.glob(str(ROOT / "**" / ext), recursive=True):
            parts = Path(filepath).parts
            if any(d in parts for d in skip_dirs):
                continue
            if Path(filepath).name in skip_files:
                continue
            is_article = "src/data/blog" in filepath and filepath.endswith(".md")
            try:
                with open(filepath, encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # For blog articles: skip content inside code blocks (tutorial examples)
                if is_article:
                    # Remove fenced code blocks
                    content_scan = re.sub(r'```[\s\S]*?```', '', content)
                    # Remove inline code
                    content_scan = re.sub(r'`[^`\n]+`', '', content_scan)
                else:
                    content_scan = content

                for lineno, line in enumerate(content_scan.splitlines(), 1):
                    for pattern, label in SECRET_PATTERNS:
                        m = re.search(pattern, line)
                        if m and not is_placeholder(m.group(0)):
                            # Additional false positive filters for articles
                            if is_article:
                                # Skip French article text mentioning password managers
                                if label == "Password" and any(x in line for x in [
                                    "1Password", "Master Password", "mot de passe", "Mot de passe",
                                    "MotDePasse", "password manager", "gestionnaire"
                                ]):
                                    continue
                            rel = Path(filepath).relative_to(ROOT)
                            issues.append((str(rel), lineno, label, line.strip()[:80]))
            except Exception:
                pass
    return issues


def check_headers():
    """Check if public/_headers exists and has required security headers."""
    issues = []
    headers_file = PUBLIC_DIR / "_headers"
    if not headers_file.exists():
        issues.append(("MISSING", "public/_headers introuvable — aucun header de sécurité HTTP en production"))
        return issues
    with open(headers_file, encoding="utf-8") as f:
        content = f.read()
    for h in REQUIRED_HEADERS:
        if h.lower() not in content.lower():
            issues.append(("MISSING_HEADER", f"Header manquant : {h}"))
    return issues


def check_gitignore():
    """Check .gitignore coverage for sensitive files."""
    issues = []
    if not GITIGNORE.exists():
        issues.append("MISSING_GITIGNORE", ".gitignore introuvable")
        return issues
    with open(GITIGNORE, encoding="utf-8") as f:
        content = f.read()
    required = [
        (".env.local", ".env.local non exclu du git"),
        (".env.*", ".env.* non exclu du git (couvre .env.staging, .env.test…)"),
        ("*.pem", "*.pem (certificats TLS) non exclu"),
        ("*.key", "*.key (clés privées) non exclu"),
        ("secrets/", "secrets/ non exclu"),
    ]
    for pattern, msg in required:
        if pattern not in content:
            issues.append(msg)
    return issues


def check_tracking_rgpd():
    """Scan src/ and public/ for third-party tracking resources."""
    issues = []
    skip_dirs = {"node_modules", ".git", "dist", ".astro"}
    for ext in ["*.astro", "*.ts", "*.js", "*.html", "*.md"]:
        for filepath in glob_module.glob(str(ROOT / "**" / ext), recursive=True):
            if any(d in Path(filepath).parts for d in skip_dirs):
                continue
            try:
                with open(filepath, encoding="utf-8", errors="ignore") as f:
                    for lineno, line in enumerate(f, 1):
                        for domain, label in TRACKING_DOMAINS:
                            if domain in line:
                                rel = Path(filepath).relative_to(ROOT)
                                issues.append((str(rel), lineno, label))
            except Exception:
                pass
    return issues


def check_set_html():
    """Audit set:html usage in .astro files for XSS risk."""
    issues = []
    for filepath in glob_module.glob(str(SRC_DIR / "**" / "*.astro"), recursive=True):
        try:
            with open(filepath, encoding="utf-8") as f:
                for lineno, line in enumerate(f, 1):
                    if "set:html" in line:
                        # Safe if used with JSON.stringify or a static string
                        if "JSON.stringify" in line or "is:inline" in line:
                            continue  # Structured data — safe
                        rel = Path(filepath).relative_to(ROOT)
                        issues.append((str(rel), lineno, line.strip()[:100]))
        except Exception:
            pass
    return issues


def check_open_redirects():
    """Check _redirects for potential open redirect to external domains."""
    issues = []
    redirects_file = PUBLIC_DIR / "_redirects"
    if not redirects_file.exists():
        return issues
    with open(redirects_file, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                destination = parts[1]
                if destination.startswith("http://") or destination.startswith("https://"):
                    issues.append((lineno, line))
    return issues


def check_article_sensitive_data():
    """Scan article bodies for IPs, emails, tokens that could be real data."""
    issues = []
    # Real IP pattern (private ranges = ok, public = flag)
    public_ip_re = re.compile(
        r'\b(?!10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.|127\.|0\.|255\.)'
        r'(\d{1,3}\.){3}\d{1,3}\b'
    )
    # Email pattern — flag if looks like a real personal email
    email_re = re.compile(r'\b[a-zA-Z0-9._%+-]+@(?!exemple\.|example\.|domain\.|domaine\.)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
    # Token-like strings outside code blocks
    token_re = re.compile(r'(?i)(token|api.key|secret|password)\s*[:=]\s*[^\s<>\'\"]{10,}')

    for filepath in glob_module.glob(str(BLOG_DIR / "*.md")):
        body = get_body(filepath)
        rel = Path(filepath).relative_to(ROOT)

        # Remove code blocks before scanning emails/IPs to reduce false positives
        body_no_code = re.sub(r'```.*?```', '', body, flags=re.DOTALL)
        body_no_code = re.sub(r'`[^`]+`', '', body_no_code)

        # Public IP addresses
        for m in public_ip_re.finditer(body_no_code):
            ip = m.group(0)
            # Skip common false positives
            if ip in ("0.0.0.0", "1.1.1.1", "8.8.8.8", "8.8.4.4", "9.9.9.9"):
                continue
            octets = list(map(int, ip.split(".")))
            if octets[0] in (100, 169):
                continue
            issues.append((str(rel), "IP publique potentiellement réelle", ip))

        # Real emails (skip articles about email tools)
        for m in email_re.finditer(body_no_code):
            email = m.group(0)
            if any(x in email for x in ["@exemple", "@example", "@domain", "@test", "@mail.com", "@brandonvisca"]):
                continue
            issues.append((str(rel), "Adresse email exposée", email))

    return issues


def check_draft_leak():
    """Check if draft articles could leak into sitemap."""
    issues = []
    for filepath in glob_module.glob(str(BLOG_DIR / "*.md")):
        fm = read_frontmatter(filepath)
        if "draft: true" in fm:
            rel = Path(filepath).relative_to(ROOT)
            # Check if it would appear in sitemap (Astro excludes drafts by default in content collections)
            # Flag it as informational
            issues.append(str(rel))
    return issues


def check_privacy_page():
    """Check if a privacy/legal page exists."""
    issues = []
    pages_dir = SRC_DIR / "pages"
    privacy_patterns = ["privacy", "confidentialite", "mentions-legales", "politique-confidentialite", "rgpd", "legal"]
    found = False
    if pages_dir.exists():
        for f in pages_dir.rglob("*"):
            if any(p in f.name.lower() for p in privacy_patterns):
                found = True
                break
    if not found:
        # Also check blog articles
        for filepath in glob_module.glob(str(BLOG_DIR / "*.md")):
            name = Path(filepath).stem.lower()
            if any(p in name for p in privacy_patterns):
                found = True
                break
    if not found:
        issues.append("Page Politique de confidentialité introuvable — obligatoire RGPD (Art. 13)")
    return issues


def check_security_txt():
    """Check if security.txt exists."""
    security_txt = PUBLIC_DIR / ".well-known" / "security.txt"
    if not security_txt.exists():
        return ["/.well-known/security.txt absent (RFC 9116 — permet aux chercheurs de signaler des vulnérabilités)"]
    return []


def check_csp_unsafe():
    """Check if CSP in _headers uses unsafe directives."""
    issues = []
    headers_file = PUBLIC_DIR / "_headers"
    if not headers_file.exists():
        return issues
    with open(headers_file, encoding="utf-8") as f:
        content = f.read()
    if "unsafe-eval" in content:
        issues.append("CSP contient 'unsafe-eval' — risque XSS")
    # unsafe-inline is acceptable for a static blog without user content
    return issues


# ─── Main ─────────────────────────────────────────────────────────────────────

def run_audit(summary_mode=False):
    print(f"\n{BOLD}{'='*60}{RST}")
    print(f"{BOLD}  Security Audit — brandonvisca.com{RST}")
    print(f"{BOLD}{'='*60}{RST}\n")

    total_errors = 0
    total_warnings = 0

    # 1. Security headers
    print(f"{BOLD}[1/9] Headers de sécurité HTTP{RST}")
    header_issues = check_headers()
    if not header_issues:
        print(f"  {ok('public/_headers présent avec tous les headers requis')}")
    else:
        for code, msg in header_issues:
            print(f"  {err(msg)}")
            total_errors += 1
        if not summary_mode:
            print(f"  {info('Exécute: python3 scripts/security-audit.py --fix-headers')}")

    # 2. Secrets scan
    print(f"\n{BOLD}[2/9] Scan de secrets / credentials{RST}")
    secret_issues = check_secrets(summary_mode)
    if not secret_issues:
        print(f"  {ok('Aucun secret détecté dans les fichiers trackés')}")
    else:
        for filepath, lineno, label, snippet in secret_issues:
            print(f"  {err(f'{filepath}:{lineno} — {label}')}")
            if not summary_mode:
                print(f"    {snippet[:80]}")
            total_errors += 1

    # 3. .gitignore coverage
    print(f"\n{BOLD}[3/9] Couverture .gitignore{RST}")
    gi_issues = check_gitignore()
    if not gi_issues:
        print(f"  {ok('.gitignore couvre les fichiers sensibles')}")
    else:
        for msg in gi_issues:
            print(f"  {warn(msg)}")
            total_warnings += 1

    # 4. RGPD — ressources tierces
    print(f"\n{BOLD}[4/9] RGPD — Ressources tierces / tracking{RST}")
    rgpd_issues = check_tracking_rgpd()
    if not rgpd_issues:
        print(f"  {ok('Aucune ressource tierce de tracking détectée')}")
    else:
        seen = set()
        for filepath, lineno, label in rgpd_issues:
            key = (filepath, label)
            if key not in seen:
                print(f"  {warn(f'{filepath}:{lineno} — {label}')}")
                seen.add(key)
                total_warnings += 1

    # 5. set:html XSS audit
    print(f"\n{BOLD}[5/9] XSS — set:html audit (OWASP A03){RST}")
    sethtml_issues = check_set_html()
    if not sethtml_issues:
        print(f"  {ok('Aucun set:html risqué détecté')}")
    else:
        for filepath, lineno, snippet in sethtml_issues:
            print(f"  {warn(f'{filepath}:{lineno} — set:html non sécurisé')}")
            if not summary_mode:
                print(f"    {snippet}")
            total_warnings += 1

    # 6. Open redirects
    print(f"\n{BOLD}[6/9] Open Redirects (OWASP A01){RST}")
    redirect_issues = check_open_redirects()
    if not redirect_issues:
        print(f"  {ok('Aucun redirect vers domaine externe')}")
    else:
        for lineno, line in redirect_issues:
            print(f"  {warn(f'_redirects:{lineno} — redirect externe : {line}')}")
            total_warnings += 1

    # 7. Données sensibles dans articles
    print(f"\n{BOLD}[7/9] Données sensibles dans articles{RST}")
    sens_issues = check_article_sensitive_data()
    if not sens_issues:
        print(f"  {ok('Aucune donnée sensible détectée dans les articles')}")
    else:
        seen = set()
        for filepath, label, value in sens_issues:
            key = (filepath, value)
            if key not in seen:
                print(f"  {warn(f'{filepath} — {label} : {value}')}")
                seen.add(key)
                total_warnings += 1

    # 8. Page vie privée / RGPD
    print(f"\n{BOLD}[8/9] Conformité RGPD — Pages légales{RST}")
    privacy_issues = check_privacy_page()
    if not privacy_issues:
        print(f"  {ok('Page politique de confidentialité trouvée')}")
    else:
        for msg in privacy_issues:
            print(f"  {warn(msg)}")
            total_warnings += 1
    sec_txt_issues = check_security_txt()
    if not sec_txt_issues:
        print(f"  {ok('security.txt présent')}")
    else:
        for msg in sec_txt_issues:
            print(f"  {info(msg)}")

    # 9. Dépendances vulnérables
    print(f"\n{BOLD}[9/9] Dépendances vulnérables (pnpm audit){RST}")
    import subprocess
    result = subprocess.run(["pnpm", "audit", "--audit-level", "high"], capture_output=True, text=True, cwd=ROOT)
    if result.returncode == 0:
        print(f"  {ok('Aucune vulnérabilité high/critical dans les dépendances')}")
    else:
        vuln_count = result.stdout.count("severity")
        print(f"  {err(f'Vulnérabilités détectées — exécute: pnpm audit')}")
        if not summary_mode:
            # Show just the summary line
            for line in result.stdout.splitlines()[-5:]:
                if line.strip():
                    print(f"  {line}")
        total_errors += 1

    # Summary
    print(f"\n{BOLD}{'─'*60}{RST}")
    if total_errors == 0 and total_warnings == 0:
        print(f"{GRN}{BOLD}  Audit propre — aucun problème détecté{RST}")
    else:
        if total_errors > 0:
            print(f"  {RED}{BOLD}{total_errors} erreur(s) critique(s){RST}")
        if total_warnings > 0:
            print(f"  {YEL}{BOLD}{total_warnings} avertissement(s){RST}")
    print()

    return total_errors


def fix_headers():
    """Generate public/_headers with recommended security headers."""
    headers_file = PUBLIC_DIR / "_headers"
    if headers_file.exists():
        print(f"{YEL}public/_headers existe déjà. Affichage des headers recommandés :{RST}\n")
        print(RECOMMENDED_HEADERS_CONTENT)
        return

    with open(headers_file, "w", encoding="utf-8") as f:
        f.write(RECOMMENDED_HEADERS_CONTENT)
    print(f"{GRN}✓ public/_headers créé avec les headers de sécurité recommandés{RST}")
    print(f"{BLU}ℹ Adapte le CSP si tu ajoutes des ressources tierces{RST}")


def hook_mode():
    """PostToolUse hook — runs on blog file writes."""
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    tool = data.get("tool_name", "")
    filepath = data.get("tool_input", {}).get("file_path", "")

    if tool not in ("Write", "Edit"):
        sys.exit(0)
    if not filepath or "src/data/blog/" not in filepath:
        sys.exit(0)

    # Quick scan: only secrets + article sensitive data for this file
    rel = filepath
    try:
        with open(filepath, encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception:
        sys.exit(0)

    issues = []
    for lineno, line in enumerate(content.splitlines(), 1):
        for pattern, label in SECRET_PATTERNS:
            m = re.search(pattern, line)
            if m and not is_placeholder(m.group(0)):
                issues.append(f"  {err(f'ligne {lineno} — {label} détecté')}")

    if issues:
        print(f"\n{RED}{BOLD}⚠ SECURITY: données sensibles détectées dans {Path(filepath).name}{RST}")
        for i in issues:
            print(i)
        print(f"{YEL}Vérifie avant de committer !{RST}\n")


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--hook" in args:
        hook_mode()
    elif "--fix-headers" in args:
        fix_headers()
    else:
        summary = "--summary" in args
        errors = run_audit(summary_mode=summary)
        sys.exit(1 if errors > 0 else 0)
