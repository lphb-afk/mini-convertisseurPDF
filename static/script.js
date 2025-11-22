// Fonction pour scroller vers les convertisseurs
function scrollToConverters() {
    console.log('Bouton cliqué!'); // Debug
    
    // Méthode 1: scrollIntoView
    const convertersSection = document.getElementById('converters');
    if (convertersSection) {
        console.log('Section trouvée:', convertersSection); // Debug
        convertersSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
        console.log('Scroll déclenché');
        return;
    }
    
    // Méthode 2: scrollTo (fallback)
    console.log('Méthode scrollIntoView échouée, utilisation de scrollTo');
    const elements = document.querySelectorAll('.converters');
    if (elements.length > 0) {
        elements[0].scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
        return;
    }
    
    // Méthode 3: scrollTo avec position fixe
    console.log('Utilisation de scrollTo avec position fixe');
    window.scrollTo({
        top: window.innerHeight,
        behavior: 'smooth'
    });
    
    console.error('Toutes les méthodes de scroll ont échoué!');
}

// Fonction pour copier le texte OCR
function copyToClipboard() {
    const textarea = document.getElementById('ocr-textarea');
    textarea.select();
    document.execCommand('copy');
    alert('Texte copié dans le presse-papiers !');
}

// Fonction pour afficher les erreurs proprement
function showError(resultDiv, error) {
    console.log('Erreur complète:', error); // Debug
    let errorMessage = 'Erreur inconnue';
    
    if (typeof error === 'string') {
        errorMessage = error;
    } else if (error && typeof error === 'object') {
        // Essayer plusieurs propriétés possibles
        errorMessage = error.detail || error.message || error.error || 
                      JSON.stringify(error) || 'Erreur de traitement';
    }
    
    console.log('Message d\'erreur extrait:', errorMessage); // Debug
    resultDiv.innerHTML = `<div class="result error">❌ ${errorMessage}</div>`;
}

// Fonction pour afficher la progression avec étapes
function showProgress(resultDiv, step = 1, total = 4, message = 'En cours...') {
    const steps = [
        { name: 'Upload', text: 'Téléchargement du fichier' },
        { name: 'Process', text: 'Traitement du document' },
        { name: 'Convert', text: 'Conversion en cours' },
        { name: 'Complete', text: 'Finalisation' }
    ];
    
    let stepClass = '';
    for (let i = 0; i < total; i++) {
        if (i + 1 < step) stepClass = 'completed';
        else if (i + 1 === step) stepClass = 'active';
        else stepClass = '';
        
        steps[i].class = stepClass;
    }
    
    const progressPercent = Math.round((step / total) * 100);
    
    resultDiv.innerHTML = `
        <div class="progress-container">
            <div class="progress-bar" style="width: ${progressPercent}%"></div>
            <div class="progress-text">${message}</div>
            <div class="progress-steps">
                ${steps.map((stepData, index) => `
                    <div class="progress-step ${stepData.class}">
                        <div class="step-icon">
                            ${stepData.class === 'completed' ? '✓' : index + 1}
                        </div>
                        <div>${stepData.name}</div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

// Gestion des conversions
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM chargé, script initialisé');
    
    // Vérifier que les éléments existent
    const ctaButton = document.getElementById('cta-button');
    const convertersSection = document.getElementById('converters');
    
    console.log('Bouton CTA trouvé:', !!ctaButton);
    console.log('Section converters trouvée:', !!convertersSection);
    
    if (ctaButton) {
        ctaButton.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Event click déclenché!');
            scrollToConverters();
        });
        console.log('Event listener ajouté au bouton');
    } else {
        console.error('Bouton CTA non trouvé');
    }
    
    // Image vers PDF
    document.getElementById('image-to-pdf-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const resultDiv = document.getElementById('image-to-pdf-result');
        
        showProgress(resultDiv, 1, 4, 'Téléchargement de votre image...');
        
        try {
            showProgress(resultDiv, 2, 4, 'Préparation de l\'image...');
            const response = await fetch('/image-to-pdf', {
                method: 'POST',
                body: formData
            });
            
            showProgress(resultDiv, 3, 4, 'Conversion en PDF...');
            
            if (response.ok) {
                showProgress(resultDiv, 4, 4, 'Finalisation du PDF...');
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'output.pdf';
                a.click();
                window.URL.revokeObjectURL(url);
                resultDiv.innerHTML = '<div class="result success">✅ Conversion réussie ! Votre PDF est prêt.</div>';
            } else {
                const error = await response.json();
                showError(resultDiv, error);
            }
        } catch (error) {
            showError(resultDiv, error.message || 'Erreur de connexion.');
        }
    });
    
    // PDF vers Word
    document.getElementById('pdf-to-word-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const resultDiv = document.getElementById('pdf-to-word-result');
        
        showProgress(resultDiv, 1, 4, 'Analyse de votre PDF...');
        
        try {
            showProgress(resultDiv, 2, 4, 'Extraction du texte...');
            const response = await fetch('/pdf-to-word', {
                method: 'POST',
                body: formData
            });
            
            showProgress(resultDiv, 3, 4, 'Création du document Word...');
            
            if (response.ok) {
                showProgress(resultDiv, 4, 4, 'Finalisation du fichier DOCX...');
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'output.docx';
                a.click();
                window.URL.revokeObjectURL(url);
                resultDiv.innerHTML = '<div class="result success">✅ Document Word prêt ! Téléchargement en cours.</div>';
            } else {
                const error = await response.json();
                showError(resultDiv, error);
            }
        } catch (error) {
            showError(resultDiv, error.message || 'Erreur de connexion.');
        }
    });
    
    // Word vers PDF
    document.getElementById('word-to-pdf-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const resultDiv = document.getElementById('word-to-pdf-result');
        
        showProgress(resultDiv, 1, 4, 'Ouverture du document Word...');
        
        try {
            showProgress(resultDiv, 2, 4, 'Analyse du contenu...');
            const response = await fetch('/word-to-pdf', {
                method: 'POST',
                body: formData
            });
            
            showProgress(resultDiv, 3, 4, 'Génération du PDF...');
            
            if (response.ok) {
                showProgress(resultDiv, 4, 4, 'Optimisation du fichier...');
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'output.pdf';
                a.click();
                window.URL.revokeObjectURL(url);
                resultDiv.innerHTML = '<div class="result success">✅ PDF généré avec succès !</div>';
            } else {
                const error = await response.json();
                showError(resultDiv, error);
            }
        } catch (error) {
            showError(resultDiv, error.message || 'Erreur de connexion.');
        }
    });
    
    // PDF vers Images
    document.getElementById('pdf-to-images-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const resultDiv = document.getElementById('pdf-to-images-result');
        
        showProgress(resultDiv, 1, 4, 'Rendu des pages PDF...');
        
        try {
            showProgress(resultDiv, 2, 4, 'Extraction des images haute qualité...');
            const response = await fetch('/pdf-to-images', {
                method: 'POST',
                body: formData
            });
            
            showProgress(resultDiv, 3, 4, 'Création de l\'archive ZIP...');
            
            if (response.ok) {
                showProgress(resultDiv, 4, 4, 'Préparation du téléchargement...');
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'pdf_images.zip';
                a.click();
                window.URL.revokeObjectURL(url);
                resultDiv.innerHTML = '<div class="result success">✅ Images extraites ! Archive ZIP prête.</div>';
            } else {
                const error = await response.json();
                showError(resultDiv, error);
            }
        } catch (error) {
            showError(resultDiv, error.message || 'Erreur de connexion.');
        }
    });
    
    // OCR PDF
    document.getElementById('ocr-pdf-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const resultDiv = document.getElementById('ocr-pdf-result');
        const textarea = document.getElementById('ocr-textarea');
        const copyBtn = document.getElementById('copy-btn');
        
        showProgress(resultDiv, 1, 4, 'Préparation du PDF pour OCR...');
        
        try {
            showProgress(resultDiv, 2, 4, 'Extraction du texte avec intelligence artificielle...');
            const response = await fetch('/ocr-pdf', {
                method: 'POST',
                body: formData
            });
            
            showProgress(resultDiv, 3, 4, 'Analyse et structuration du texte...');
            
            if (response.ok) {
                showProgress(resultDiv, 4, 4, 'Finalisation de l\'extraction...');
                const data = await response.json();
                textarea.value = data.text;
                textarea.style.display = 'block';
                copyBtn.style.display = 'block';
                resultDiv.innerHTML = '<div class="result success">✅ Texte extrait avec succès ! Prêt à copier.</div>';
            } else {
                const error = await response.json();
                showError(resultDiv, error);
            }
        } catch (error) {
            showError(resultDiv, error.message || 'Erreur de connexion.');
        }
    });
});

// Exporter la fonction globalement pour onclick
window.scrollToConverters = scrollToConverters;
window.copyToClipboard = copyToClipboard;
