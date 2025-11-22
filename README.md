# 🚀 Mini Convertisseur PDF

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Security](https://img.shields.io/badge/Security-Grade_A-brightgreen.svg)

**Application web moderne pour convertir vos documents PDF et images avec une interface intuitive**

[✨ Démo Live](#-démo) • [🚀 Installation](#-installation) • [📖 Documentation](#-documentation) • [🔧 Développement](#-développement)

</div>

## ✨ Fonctionnalités

| Conversion | Description | Statut |
|------------|-------------|---------|
| 🖼️ **Image → PDF** | Convertit PNG, JPG, GIF, BMP, TIFF en PDF haute qualité | ✅ **Opérationnel** |
| 📄 **PDF → Word** | Extrait le texte d'un PDF vers un document Word (DOCX) | ✅ **Opérationnel** |
| 📝 **Word → PDF** | Convertit DOCX/DOC en PDF avec mise en forme | ✅ **Opérationnel** |
| 🖼️ **PDF → Images** | Convertit chaque page PDF en image PNG haute résolution | ✅ **Opérationnel** |
| 🔍 **OCR PDF** | Extrait le texte des PDFs scannés avec Tesseract | ✅ **Opérationnel** |

### 🎯 **Fonctionnalités Avancées**
- ⚡ **Interface moderne** avec barre de progression en temps réel
- 🔒 **Sécurité renforcée** - Validation complète des fichiers
- 📱 **Responsive Design** - Fonctionne sur mobile et desktop
- 🚀 **Haute Performance** - Traitement optimisé des conversions
- 🎨 **UX Premium** - Animations fluides et feedback visuel

## 🛡️ Sécurité & Qualité

| Aspect | Description | Statut |
|--------|-------------|---------|
| **🔍 Validation** | Types de fichiers, tailles (max 30MB), contenu | ✅ **Sécurisé** |
| **⏱️ Performance** | Timeouts, gestion des erreurs, async | ✅ **Optimisé** |
| **🔒 Protection** | CSP, HSTS, X-Frame-Options, Rate limiting | ✅ **Grade A** |
| **🧹 Nettoyage** | Suppression automatique des fichiers temporaires | ✅ **Automatique** |
| **📋 Conformité** | Validation Pydantic, messages d'erreur sécurisés | ✅ **Conforme** |

### 🔐 **Mesures de Sécurité Avancées**
- **Rate Limiting** : 10 requêtes/minute par IP
- **HTTPS Obligatoire** : Certificats SSL/TLS automatiques
- **Validation Stricte** : Tous les fichiers vérifiés avant traitement
- **Isolation** : Fichiers temporaires isolés et supprimés
- **Headers Sécurisés** : CSP, HSTS, X-Frame-Options, etc.

## Installation

### macOS

```bash
# Dépendances système
brew install poppler tesseract libreoffice unoconv

# Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Linux (Ubuntu/Debian)

```bash
# Dépendances système
sudo apt update
sudo apt install poppler-utils tesseract-ocr libreoffice unoconv

# Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows

```cmd
rem Dépendances système (télécharger et installer)
rem - Poppler: https://blog.alivate.com.au/poppler-windows/
rem - Tesseract: https://github.com/tesseract-ocr/tesseract
rem - LibreOffice: https://www.libreoffice.org/

rem Python
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Lancement

```bash
# macOS/Linux
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Windows
venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Ouvrez http://localhost:8000 dans votre navigateur.

## Architecture

- **Backend** : FastAPI (Python)
- **Frontend** : HTML/CSS/JavaScript vanilla
- **OCR** : Tesseract
- **PDF Processing** : pypdf, pdf2image, reportlab
- **Office Documents** : python-docx, docx2pdf, LibreOffice

## Production

### Configuration recommandée

#### Sécurité réseau et serveur

- **HTTPS obligatoire** : Let's Encrypt (certbot), Nginx ou Caddy
- **Redirection automatique** : HTTP → HTTPS
- **Ports ouverts uniquement** :
  - 443 (HTTPS)
  - 80 (redirection certbot)
  - 22 (SSH uniquement avec clé privée, pas de mot de passe)
- **Firewall** : UFW ou iptables
  ```bash
  ufw allow 443
  ufw allow 80
  ufw deny 22  # ou ufw allow from YOUR_IP to any port 22
  ```
- **Reverse Proxy** : Nginx avec FastAPI derrière (pas d'accès direct)
- **Rate Limiting** : Nginx rate limiting automatique

#### Serveur et déploiement

- **Serveur ASGI** : Gunicorn + Uvicorn workers
- **Reverse Proxy** : Nginx avec rate limiting et SSL
- **HTTPS** : Let's Encrypt (certbot)
- **CDN/WAF** : Cloudflare gratuit pour protection DDoS et caching
- **Blocage IPs** : Fail2Ban pour analyse des logs et bannissement automatique

### Configuration de sécurité

#### Firewall (UFW)
```bash
# Installation
sudo apt install ufw

# Configuration
sudo ufw allow 443
sudo ufw allow 80
sudo ufw deny 22  # ou sudo ufw allow from YOUR_IP to any port 22
sudo ufw --force enable
```

#### Nginx avec SSL et rate limiting
```nginx
# /etc/nginx/sites-available/mini-convertisseur

# Redirection HTTP vers HTTPS
server {
    listen 80;
    server_name votre-domaine.com;
    return 301 https://$server_name$request_uri;
}

# Serveur HTTPS
server {
    listen 443 ssl http2;
    server_name votre-domaine.com;

    # SSL Let's Encrypt
    ssl_certificate /etc/letsencrypt/live/votre-domaine.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/votre-domaine.com/privkey.pem;

    # Sécurité SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/m;
    limit_req zone=api burst=20 nodelay;

    # Blocage bots et scanners
    if ($http_user_agent ~* "badbot|scanner|sqlmap|nmap") {
        return 403;
    }

    # Protection contre les attaques communes
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts de sécurité
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }

    # Logs pour Fail2Ban
    access_log /var/log/nginx/mini-convertisseur.access.log;
    error_log /var/log/nginx/mini-convertisseur.error.log;
}
```

# Configuration Fail2Ban (jail.local)
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 86400

[nginx-ddos]
enabled = true
port = http,https
filter = nginx-ddos
logpath = /var/log/nginx/mini-convertisseur.access.log
maxretry = 3
bantime = 86400
findtime = 600
```

### Sécurité API FastAPI

#### Configuration production
```python
# Dans main.py
app = FastAPI(
    title="Mini Convertisseur PDF",
    docs_url=None,  # Désactive /docs en production
    redoc_url=None  # Désactive /redoc en production
)
```

#### En-têtes de sécurité
- `Content-Security-Policy` : Contrôle des sources de contenu
- `Strict-Transport-Security` : Force HTTPS
- `X-Frame-Options: DENY` : Empêche le clickjacking
- `X-Content-Type-Options: nosniff` : Empêche le MIME sniffing
- `X-XSS-Protection` : Protection XSS (legacy)

#### Bonnes pratiques
- ✅ Validation Pydantic sur toutes les entrées
- ✅ Messages d'erreur neutres (pas d'infos internes)
- ✅ Rate limiting (SlowAPI + Nginx)
- ✅ Pas d'utilisation d'eval/exec
- ✅ Timeouts appropriés
- ✅ Validation des types MIME et tailles de fichiers

### Sécurité des données et clés

#### Variables d'environnement
```bash
# Copiez le fichier exemple
cp .env.example .env

# Permissions sécurisées
chmod 600 .env
```

#### Permissions fichiers
```bash
# Clés privées et certificats
chmod 600 key.pem cert.pem

# Fichiers de configuration sensibles
chmod 600 .env

# Fichiers d'application
chmod 644 *.py *.html *.css *.js
chmod 755 *.sh

# Répertoire venv (protégé)
chmod 700 venv/
```

#### Sauvegardes chiffrées
```bash
# Sauvegarde chiffrée avec GPG
tar czf - . | gpg -c > backup-$(date +%Y%m%d).tar.gz.gpg

# Restauration
gpg -d backup-20250101.tar.gz.gpg | tar xzf -
```

#### Rotation des clés
- Changez les clés JWT/API tous les 90 jours
- Utilisez des mots de passe forts (20+ caractères)
- Stockez les clés dans un gestionnaire de secrets (Vault, AWS Secrets Manager)

### Lancement en production

```bash
# Développement (avec rechargement)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production (sans rechargement pour sécurité)
uvicorn main:app --host 127.0.0.1 --port 8000

# Avec Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000

# Avec systemd
sudo systemctl enable mini-convertisseur
sudo systemctl start mini-convertisseur
```

### Cloudflare

1. Créez un compte gratuit sur cloudflare.com
2. Ajoutez votre domaine
3. Configurez les règles WAF pour bloquer les attaques communes
4. Activez le caching pour les ressources statiques

## Sécurité du développement

### Outils de sécurité

- **pip-audit** : Vérification des vulnérabilités dans les dépendances
- **Bandit** : Analyse statique de sécurité du code Python

### Exécution automatique

Utilisez le script `security_check.sh` pour exécuter automatiquement toutes les vérifications :

```bash
# Exécution manuelle
./security_check.sh

# Planification hebdomadaire avec cron (macOS/Linux)
crontab -e
# Ajouter : 0 2 * * 1 /path/to/mini-convertisseurPDF/security_check.sh

# Ou avec launchd sur macOS (recommandé)
# ✅ Configuré : com.security-check.plist copié vers ~/Library/LaunchAgents/ et chargé
# Le script s'exécute automatiquement tous les lundis à 2h du matin
```

**Contenu du script :**
- Mise à jour des dépendances
- Audit des vulnérabilités (pip-audit)
- Analyse de sécurité du code (Bandit)

### Tests de sécurité

#### OWASP ZAP (scanner de vulnérabilités web)
```bash
# Installation (macOS avec Homebrew)
brew install owasp-zap

# Lancement en mode GUI
zap.sh

# Scan automatisé
zap.sh -cmd -autorun /path/to/zap-script.yaml
```

#### Tests de charge
```bash
# Apache Bench (installé par défaut sur macOS/Linux)
ab -n 1000 -c 10 https://localhost/

# K6 (installation)
brew install k6

# Test de charge avec le script fourni
k6 run load_test.js

# Test personnalisé
k6 run --vus 10 --duration 30s - < load_test.js
```

#### Vérification TLS/SSL
```bash
# SSL Labs (en ligne)
# Allez sur https://www.ssllabs.com/ssltest/

# Test local avec openssl
openssl s_client -connect localhost:443 -servername localhost

# Test des certificats
openssl x509 -in cert.pem -text -noout
```

### Mises à jour manuelles

```bash
# Installation des outils
pip install pip-audit bandit

# Vérifications individuelles
pip-audit
bandit main.py create_samples.py test_load.py test_platform.py
pip install --upgrade -r requirements.txt
```

## Licence

MIT