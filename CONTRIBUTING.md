# 🤝 Guide de Contribution

Merci de votre intérêt pour contribuer au Mini Convertisseur PDF ! Voici comment vous pouvez participer.

## 📋 **Table des Matières**

- [Code de Conduite](#-code-de-conduite)
- [Comment Contribuer](#-comment-contribuer)
- [Configuration de l'Environnement](#️-configuration-de-lenvironnement)
- [Structure du Projet](#️-structure-du-projet)
- [Standards de Code](#-standards-de-code)
- [Tests](#-tests)
- [Documentation](#-documentation)
- [Soumission de PR](#-soumission-de-pr)

## 🌟 **Code de Conduite**

- Soyez respectueux et bienveillant envers tous les contributeurs
- Respectez les opinions différentes
- Acceptez la critique constructrice de manière positive
- Concentrez-vous sur ce qui est meilleur pour la communauté

## 🚀 **Comment Contribuer**

### **🐛 Signaler des Bugs**
- Utilisez le [template de bug report](.github/ISSUE_TEMPLATE/bug_report.md)
- Décrivez clairement le problème
- Fournissez les étapes pour reproduire
- Mentionnez votre environnement (OS, navigateur, etc.)

### **💡 Proposer des Fonctionnalités**
- Utilisez le [template de feature request](.github/ISSUE_TEMPLATE/feature_request.md)
- Expliquez pourquoi cette fonctionnalité serait utile
- Décrivez votre implémentation idéale

### **📝 Améliorer la Documentation**
- Corrections de fautes
- Amélioration des explications
- Traductions
- Exemples supplémentaires

### **🔧 Contributions Techniques**
- Corriger des bugs
- Optimiser les performances
- Ajouter des tests
- Améliorer la sécurité

## ⚙️ **Configuration de l'Environnement**

### **Prérequis**
- Python 3.9+
- Git
- Poppler-utils
- Tesseract-OCR
- LibreOffice (optionnel)

### **Installation**

```bash
# Cloner le repo
git clone https://github.com/votre-username/mini-convertisseurPDF.git
cd mini-convertisseurPDF

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Installer les dépendances système
# macOS
brew install poppler tesseract libreoffice

# Ubuntu/Debian
sudo apt install poppler-utils tesseract-ocr libreoffice

# Lancer l'application
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📁 **Structure du Projet**

```
mini-convertisseurPDF/
├── main.py                 # Application FastAPI principale
├── static/                 # Fichiers statiques
│   ├── index.html         # Page principale
│   ├── styles.css         # Styles CSS
│   └── script.js          # JavaScript
├── requirements.txt       # Dépendances Python
├── .gitignore            # Fichiers ignorés par Git
├── Dockerfile            # Configuration Docker
├── docker-compose.yml    # Configuration Docker Compose
├── README.md             # Documentation principale
├── CONTRIBUTING.md       # Guide de contribution
└── LICENSE              # Licence MIT
```

## 📏 **Standards de Code**

### **Python**
- **PEP 8** : Suivez les conventions de style Python
- **Type hints** : Utilisez-les quand possible
- **Docstrings** : Documentez vos fonctions avec des docstrings

### **JavaScript**
- **ES6+** : Utilisez les fonctionnalités modernes
- ** camelCase** : Pour les variables et fonctions
- **Commentaires** : Documentez les parties complexes

### **CSS**
- **BEM** : Methodology pour les noms de classes
- **Mobile-first** : Responsive design priorité mobile

### **Exemples de Code**

#### Python
```python
async def convert_image_to_pdf(file: UploadFile) -> FileResponse:
    """
    Convert an image file to PDF format.
    
    Args:
        file: UploadFile - The image file to convert
        
    Returns:
        FileResponse: The converted PDF file
        
    Raises:
        HTTPException: If the file format is not supported
    """
    # Validation
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Format non supporté")
    
    # Traitement
    # ... votre code ici
```

#### JavaScript
```javascript
/**
 * Shows progress for file conversion with animated steps
 * @param {HTMLElement} resultDiv - Container element for progress display
 * @param {number} step - Current step (1-4)
 * @param {number} total - Total number of steps
 * @param {string} message - Progress message to display
 */
function showProgress(resultDiv, step = 1, total = 4, message = 'En cours...') {
    // Your implementation here
}
```

## 🧪 **Tests**

### **Lancer les Tests**
```bash
# Tests unitaires (si implémentés)
pytest tests/

# Tests manuels
# Utilisez les fichiers dans le répertoire pour tester
# sample.pdf, sample.png, sample.docx
```

### **Écrire des Tests**
- Tests unitaires pour les fonctions utilitaires
- Tests d'intégration pour les endpoints API
- Tests de performance pour les conversions

## 📖 **Documentation**

### **README.md**
- Maintenez-le à jour avec les nouvelles fonctionnalités
- Ajoutez des exemples d'usage
- Mettez à jour la section "Installation"

### **Code Comments**
- Documentez les algorithmes complexes
- Expliquez les décisions d'architecture
- Utilisez des noms de variables explicites

## 🚀 **Soumission de PR**

### **Processus**
1. **Fork** le projet
2. **Créez** une branche feature (`git checkout -b feature/amazing-feature`)
3. **Commitez** vos changements (`git commit -m 'Add amazing feature'`)
4. **Pushez** la branche (`git push origin feature/amazing-feature`)
5. **Ouvrez** une Pull Request

### **Template de PR**
```markdown
## 📝 Description
Brève description des changements

## 🔍 Type de Changement
- [ ] Bug fix (changement non-breaking qui corrige un problème)
- [ ] New feature (changement non-breaking qui ajoute une fonctionnalité)
- [ ] Breaking change (correction ou fonctionnalité qui casserait l'existant)
- [ ] Documentation update

## 🧪 Tests
- [ ] J'ai testé localement mes changements
- [ ] J'ai ajouté des tests pour mes changements
- [ ] Tous les nouveaux et existants tests passent

## 📋 Checklist
- [ ] Mon code suit les standards du projet
- [ ] J'ai fait une auto-review de mon code
- [ ] J'ai commenté les parties complexes
- [ ] J'ai mis à jour la documentation
- [ ] Mes changements ne génèrent pas de nouveaux warnings
```

### **Critères d'Acceptation**
- ✅ Tests passent
- ✅ Code suit les standards
- ✅ Documentation mise à jour
- ✅ Pas de breaking changes (sauf mention explicite)
- ✅ Description claire des changements

## 📞 **Support**

Si vous avez des questions :
- Ouvrez une [Issue](https://github.com/votre-username/mini-convertisseurPDF/issues)
- Consultez la [Documentation](README.md)
- Regardez les [Discussions](https://github.com/votre-username/mini-convertisseurPDF/discussions)

## 🙏 **Remerciements**

Merci à tous les contributeurs qui aident à améliorer ce projet !

---

**Note** : Ce document peut évoluer. Vérifiez régulièrement les mises à jour.