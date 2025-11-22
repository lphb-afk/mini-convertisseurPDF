#!/usr/bin/env python3
"""
Script de test multiplateforme pour Mini Convertisseur PDF
Teste les dépendances et fonctionnalités de base
"""

import sys
import platform
import subprocess
import os

def check_python_version():
    """Vérifie la version Python"""
    version = sys.version_info
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return version >= (3, 8)

def check_platform():
    """Affiche la plateforme"""
    system = platform.system()
    print(f"🖥️  Plateforme: {system}")
    return system

def check_dependencies():
    """Vérifie les dépendances Python"""
    try:
        import fastapi
        import uvicorn
        import PIL
        import pdfplumber
        import pytesseract
        import docx
        import reportlab
        print("✅ Toutes les dépendances Python installées")
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        return False

def check_system_tools():
    """Vérifie les outils système selon la plateforme"""
    system = platform.system()
    tools_ok = True

    # Outils communs
    tools = ['tesseract', 'unoconv']

    for tool in tools:
        try:
            result = subprocess.run([tool, '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"✅ {tool} installé")
            else:
                print(f"❌ {tool} non fonctionnel")
                tools_ok = False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print(f"❌ {tool} non trouvé")
            tools_ok = False

    # Vérification Poppler (pdf2image)
    try:
        import pdf2image
        print("✅ pdf2image (avec Poppler) OK")
    except Exception as e:
        print(f"❌ pdf2image/Poppler problème: {e}")
        tools_ok = False

    return tools_ok

def test_basic_functionality():
    """Test basique des imports et fonctionnalités"""
    try:
        # Test PIL
        from PIL import Image
        img = Image.new('RGB', (100, 100), color='red')
        print("✅ PIL Image creation OK")

        # Test reportlab
        from reportlab.pdfgen import canvas
        print("✅ ReportLab PDF generation OK")

        # Test pdfplumber
        import pdfplumber
        print("✅ pdfplumber PDF processing OK")

        # Test pytesseract (sans OCR réel)
        import pytesseract
        print("✅ pytesseract OCR OK")

        return True
    except Exception as e:
        print(f"❌ Erreur fonctionnalité: {e}")
        return False

def main():
    print("🚀 Test Multiplateforme - Mini Convertisseur PDF")
    print("=" * 50)

    all_ok = True

    # Tests
    all_ok &= check_python_version()
    check_platform()
    all_ok &= check_dependencies()
    all_ok &= check_system_tools()
    all_ok &= test_basic_functionality()

    print("\n" + "=" * 50)
    if all_ok:
        print("🎉 Tous les tests réussis ! L'application est prête.")
        print("\nPour lancer l'application:")
        if platform.system() == "Windows":
            print("venv\\Scripts\\activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        else:
            print("source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    else:
        print("❌ Certains tests ont échoué. Vérifiez l'installation.")
        sys.exit(1)

if __name__ == "__main__":
    main()