# Configuration de Production SSL pour Mini Convertisseur PDF

## Étapes pour Configurer SSL en Production

### 1. Certificats Let's Encrypt (Recommandé)

```bash
# Installer certbot
sudo apt install certbot python3-certbot-nginx  # Ubuntu/Debian
brew install certbot  # macOS

# Obtenir un certificat
sudo certbot --nginx -d votre-domaine.com

# Renouvellement automatique
sudo crontab -e
# Ajouter : 0 12 * * * /usr/bin/certbot renew --quiet
```

### 2. Configuration Nginx SSL

Créez `/etc/nginx/sites-available/mini-convertisseur` :

```nginx
server {
    listen 80;
    server_name votre-domaine.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name votre-domaine.com;

    # Certificats SSL Let's Encrypt
    ssl_certificate /etc/letsencrypt/live/votre-domaine.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/votre-domaine.com/privkey.pem;

    # Configuration SSL sécurisée
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # En-têtes de sécurité
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/m;
    limit_req zone=api burst=20 nodelay;

    # Protection contre les bots malveillants
    if ($http_user_agent ~* "badbot|scanner|sqlmap|nmap|nikto|dirb|dirbuster|w3af") {
        return 403;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts de sécurité
        proxy_connect_timeout 30s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Taille max des fichiers uploadés
        client_max_body_size 30M;
    }

    # Logs pour surveillance
    access_log /var/log/nginx/mini-convertisseur.access.log;
    error_log /var/log/nginx/mini-convertisseur.error.log;
}
```

### 3. Activation

```bash
# Créer le lien symbolique
sudo ln -s /etc/nginx/sites-available/mini-convertisseur /etc/nginx/sites-enabled/

# Tester la configuration
sudo nginx -t

# Redémarrer Nginx
sudo systemctl reload nginx
```

### 4. Configuration Firewall

```bash
# UFW (Ubuntu/Debian)
sudo ufw allow 443/tcp
sudo ufw allow 80/tcp
sudo ufw deny 22/tcp  # ou restrict SSH

# Ou iptables
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j DROP
```

### 5. Variables d'Environnement Production

Créez `.env` :

```bash
# Production
DEBUG=False
SECRET_KEY=votre-cle-secrete-tres-longue-et-aleatoire
ALLOWED_HOSTS=votre-domaine.com
MAX_FILE_SIZE_MB=30
TIER=premium

# Base de données (si utilisée)
DATABASE_URL=postgresql://user:password@localhost/dbname

# Email (notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=votre-email@gmail.com
SMTP_PASSWORD=votre-mot-de-passe-app
```

### 6. Service Systemd

Créez `/etc/systemd/system/mini-convertisseur.service` :

```ini
[Unit]
Description=Mini Convertisseur PDF
After=network.target

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/app
Environment=PATH=/path/to/your/app/venv/bin
ExecStart=/path/to/your/app/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Activation :
```bash
sudo systemctl daemon-reload
sudo systemctl enable mini-convertisseur
sudo systemctl start mini-convertisseur
```

### 7. Surveillance et Logs

```bash
# Logs Nginx
sudo tail -f /var/log/nginx/mini-convertisseur.access.log

# Logs Application
sudo tail -f /var/log/mini-convertisseur/app.log

# État du service
sudo systemctl status mini-convertisseur
```

### 8. Sauvegarde

```bash
# Script de sauvegarde quotidienne
#!/bin/bash
DATE=$(date +%Y%m%d)
tar czf /backups/mini-convertisseur-$DATE.tar.gz \
    /path/to/your/app \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc'

# Upload vers cloud storage (AWS S3, etc.)
aws s3 cp /backups/mini-convertisseur-$DATE.tar.gz s3://votre-bucket/backups/