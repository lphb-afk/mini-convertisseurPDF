# 🚀 Guide de Déploiement - Railway

## 🎯 **Déploiement en 5 minutes sur Railway**

### **Étape 1 : Préparation du repository**
```bash
✅ Repository GitHub créé : https://github.com/lphb-afk/mini-convertisseurPDF
✅ Code source prêt avec FastAPI
✅ Docker configuré
✅ Variables d'environnement définies
```

### **Étape 2 : Déploiement Railway**

#### **2.1 Créer un compte Railway**
1. Aller sur : https://railway.app
2. Cliquer "Login" 
3. Se connecter avec GitHub (recommandé)

#### **2.2 Nouveau projet**
1. Cliquer "New Project"
2. Sélectionner "Deploy from GitHub repo"
3. Chercher et sélectionner : `mini-convertisseurPDF`
4. Cliquer "Deploy Now"

#### **2.3 Configuration automatique**
Railway va automatiquement :
- ✅ Détecter FastAPI dans le code
- ✅ Installer les dépendances depuis `requirements.txt`
- ✅ Configurer le port d'écoute
- ✅ Déployer l'application

### **Étape 3 : Variables d'environnement**

#### **3.1 Ajouter les variables dans Railway :**
1. Aller dans votre projet Railway
2. Cliquer "Variables" dans le menu
3. Ajouter ces variables :

```
MAX_FILE_SIZE_MB=30
TIER=premium
```

#### **3.2 Variables Railway automatiques :**
Railway fournit automatiquement :
- `$PORT` : Port d'écoute (utilisé dans votre app)
- `$RAILWAY_ENVIRONMENT` : Environnement de déploiement

### **Étape 4 : Premier déploiement**

#### **4.1 Déploiement automatique**
- Railway va builder et déployer automatiquement
- Vous verrez les logs en temps réel
- Tiempo estimado : 3-5 minutos

#### **4.2 URL de votre app**
Une fois déployé, Railway vous donne :
- **URL d'exemple** : `https://mini-convertisseur-production-abc123.railway.app`
- **SSL automatique** : HTTPS activé par défaut
- **Domaine personnalisé** : Possible (optionnel)

### **Étape 5 : Test de l'application**

#### **5.1 Tester les endpoints**
```bash
# Test de base
curl https://votre-app.railway.app/

# Test des fonctionnalités
# - Image → PDF
# - PDF → Word  
# - Word → PDF
# - PDF → Images
# - OCR PDF
```

#### **5.2 Interface web**
- Votre interface est accessible à : `https://votre-app.railway.app/`
- Toutes les fonctionnalités sont opérationnelles
- Rate limiting configuré
- Sécurité activée

## 💰 **Coût Railway**

### **Plan gratuit :**
- **$5** de crédits gratuits / mois
- **~150 heures** de calcul
- **~10GB** de bandwidth
- **Suffisant** pour une utilisation personnelle/modérée

### **Plan payant :**
- **$5/mois** minimum
- Usage illimité en heures de calcul
- Support prioritaire

## 🔧 **Configuration avancée (optionnel)**

### **Procfile Railway (auto-généré)**
Railway détecte automatiquement FastAPI et crée :
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### **Si vous voulez personnaliser :**
1. Créer un `Procfile` à la racine :
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT --workers 2
```

### **Variables Railway spécifiques :**
```
MAX_FILE_SIZE_MB=50        # Augmenter la limite si nécessaire
TIER=premium               # Plan premium pour plus de fonctionnalités
RAILWAY_ENVIRONMENT=production
```

## 🚀 **Déploiement pas à pas en images :**

### **Étape 1 : Dashboard Railway**
```
1. Dashboard Railway → "New Project"
2. GitHub OAuth → Autoriser Railway
3. Sélectionner repo → "mini-convertisseurPDF"
4. Deploy → Attendre 3-5 minutes
```

### **Étape 2 : Configuration**
```
1. Projet créé → "Settings" 
2. Variables → Ajouter MAX_FILE_SIZE_MB=30
3. Variables → Ajouter TIER=premium
4. Redéploiement automatique
```

### **Étape 3 : Test**
```
1. Cliquer sur l'URL générée
2. Interface web s'ouvre
3. Tester upload + conversion
4. Fonctionnel ! ✅
```

## 🎯 **Résultat final :**

### **Votre app sera disponible à :**
```
https://mini-convertisseur-production-abc123.railway.app
```

### **Avec toutes les fonctionnalités :**
- ✅ Conversion d'images en PDF
- ✅ Extraction de texte PDF vers Word
- ✅ Conversion Word vers PDF
- ✅ Conversion PDF vers images
- ✅ OCR de PDF scannés
- ✅ Interface web moderne
- ✅ Sécurité et rate limiting
- ✅ HTTPS automatique

## 💡 **Conseils post-déploiement :**

### **Monitoring :**
- Logs disponibles dans Railway Dashboard
- Métriques d'utilisation
- Alertes automatiques

### **Maintenance :**
- Git push → Redéploiement automatique
- Variables modifiables via Dashboard
- Scaling automatique

### **Domaine personnalisé (optionnel) :**
```bash
# Dans Railway Dashboard
Settings → Domains → Add Custom Domain
# Vous avez un vrai nom de domaine professionnel
```

---

**🎉 Votre convertisseur sera en ligne en 5 minutes !**