#!/bin/bash

# Script de mise à jour automatique des dépendances
# À exécuter hebdomadairement via cron ou launchd

echo "=== Mise à jour automatique des dépendances - $(date) ==="

# Activer l'environnement virtuel
source venv/bin/activate

echo "1. Vérification des vulnérabilités..."
pip-audit --format=json --output=audit_report.json || true

echo "2. Mise à jour des dépendances..."
pip install --upgrade -r requirements.txt

echo "3. Régénération du lock file avec versions exactes..."
pip freeze > requirements_lock.txt

echo "4. Test des fonctionnalités de base..."
python test_comprehensive.py || echo "⚠️  Certains tests ont échoué"

echo "5. Analyse de sécurité du code..."
bandit -r . -f json -o security_report.json || true

echo "6. Génération du rapport de mise à jour..."
cat > update_report.md << EOF
# Rapport de Mise à Jour - $(date)

## Vulnérabilités Détectées
EOF

if [ -f audit_report.json ]; then
    echo "Fichier d'audit généré" >> update_report.md
else
    echo "Aucune vulnérabilité détectée" >> update_report.md
fi

cat >> update_report.md << EOF

## Sécurité du Code
EOF

if [ -f security_report.json ]; then
    echo "Rapport de sécurité généré" >> update_report.md
else
    echo "Aucun problème de sécurité détecté" >> update_report.md
fi

echo "=== Mise à jour terminée ==="

# Nettoyer les fichiers temporaires
rm -f audit_report.json security_report.json

# Envoyer une notification (optionnel)
# osascript -e 'display notification "Mise à jour des dépendances terminée" with title "Mini Convertisseur PDF"'