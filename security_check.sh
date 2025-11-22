#!/bin/bash

# Script de vérification de sécurité automatique
# À exécuter régulièrement (hebdomadaire recommandé)

echo "=== Vérification de sécurité - $(date) ==="

# Activer l'environnement virtuel
source venv/bin/activate

echo "1. Mise à jour des dépendances..."
pip install --upgrade -r requirements.txt

echo "2. Audit des vulnérabilités..."
pip-audit

echo "3. Analyse de sécurité du code..."
bandit main.py create_samples.py test_load.py test_platform.py

echo "=== Fin de la vérification ==="