#!/usr/bin/env python3
"""
Tests unitaires complets pour Mini Convertisseur PDF
"""

import pytest
import asyncio
import tempfile
import os
from fastapi.testclient import TestClient
from main import app
from PIL import Image
import io

client = TestClient(app)

class TestMiniConverter:
    """Tests pour l'application Mini Convertisseur PDF"""
    
    def setup_method(self):
        """Setup pour chaque test"""
        # Créer des fichiers de test
        self.test_image = Image.new('RGB', (100, 100), color='red')
        self.test_pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 44 >>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n(Test PDF) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000227 00000 n \ntrailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n304\n%%EOF"
        
        # Sauvegarder temporairement
        self.temp_files = []
    
    def teardown_method(self):
        """Nettoyage après chaque test"""
        for temp_file in self.temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def create_temp_file(self, content, suffix):
        """Créer un fichier temporaire"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(content)
            temp_path = tmp.name
            self.temp_files.append(temp_path)
            return temp_path
    
    def test_health_check(self):
        """Test de vérification de santé"""
        response = client.get("/")
        assert response.status_code == 200
        assert "Mini Convertisseur PDF" in response.text
    
    def test_image_to_pdf_valid_image(self):
        """Test conversion image vers PDF avec image valide"""
        # Créer une image temporaire
        img_bytes = io.BytesIO()
        self.test_image.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        files = {'file': ('test.png', img_bytes, 'image/png')}
        response = client.post('/image-to-pdf', files=files)
        
        assert response.status_code == 200
        assert response.headers['content-type'] == 'application/pdf'
        assert len(response.content) > 0
    
    def test_image_to_pdf_invalid_file_type(self):
        """Test conversion image vers PDF avec type de fichier invalide"""
        files = {'file': ('test.txt', b'invalid content', 'text/plain')}
        response = client.post('/image-to-pdf', files=files)
        
        assert response.status_code == 400
        assert 'non autorisé' in response.json()['detail']
    
    def test_pdf_to_word_valid_pdf(self):
        """Test conversion PDF vers Word avec PDF valide"""
        temp_path = self.create_temp_file(self.test_pdf_content, '.pdf')
        
        with open(temp_path, 'rb') as f:
            files = {'file': ('test.pdf', f, 'application/pdf')}
            response = client.post('/pdf-to-word', files=files)
        
        assert response.status_code == 200
        assert response.headers['content-type'] == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    
    def test_pdf_to_word_invalid_file_type(self):
        """Test conversion PDF vers Word avec type de fichier invalide"""
        files = {'file': ('test.jpg', b'invalid content', 'image/jpeg')}
        response = client.post('/pdf-to-word', files=files)
        
        assert response.status_code == 400
        assert 'non autorisé' in response.json()['detail']
    
    def test_pdf_to_images_valid_pdf(self):
        """Test conversion PDF vers Images avec PDF valide"""
        temp_path = self.create_temp_file(self.test_pdf_content, '.pdf')
        
        with open(temp_path, 'rb') as f:
            files = {'file': ('test.pdf', f, 'application/pdf')}
            response = client.post('/pdf-to-images', files=files)
        
        assert response.status_code == 200
        # Devrait retourner une archive ZIP maintenant
        assert response.headers['content-type'] == 'application/zip'
    
    def test_ocr_pdf_valid_pdf(self):
        """Test OCR PDF avec PDF valide"""
        temp_path = self.create_temp_file(self.test_pdf_content, '.pdf')
        
        with open(temp_path, 'rb') as f:
            files = {'file': ('test.pdf', f, 'application/pdf')}
            response = client.post('/ocr-pdf', files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'ok'
        assert 'text' in data
    
    def test_rate_limiting(self):
        """Test de limitation de débit"""
        # Faire plusieurs requêtes pour déclencher la limitation
        for i in range(11):  # Limite est à 10/minute
            img_bytes = io.BytesIO()
            self.test_image.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            files = {'file': (f'test{i}.png', img_bytes, 'image/png')}
            response = client.post('/image-to-pdf', files=files)
            
            if i < 10:
                assert response.status_code == 200
            else:
                assert response.status_code == 429  # Too Many Requests
    
    def test_file_size_limit(self):
        """Test de limite de taille de fichier"""
        # Créer un fichier plus gros que la limite (30MB)
        large_content = b'x' * (31 * 1024 * 1024)  # 31MB
        
        files = {'file': ('large.png', io.BytesIO(large_content), 'image/png')}
        response = client.post('/image-to-pdf', files=files)
        
        assert response.status_code == 413  # Payload Too Large
    
    def test_invalid_filename(self):
        """Test avec nom de fichier invalide"""
        img_bytes = io.BytesIO()
        self.test_image.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        files = {'file': ('../../../etc/passwd.png', img_bytes, 'image/png')}
        response = client.post('/image-to-pdf', files=files)
        
        assert response.status_code == 400
        assert 'invalide' in response.json()['detail']
    
    def test_security_headers(self):
        """Test des en-têtes de sécurité"""
        response = client.get("/")
        
        # Vérifier la présence des en-têtes de sécurité
        assert 'Content-Security-Policy' in response.headers
        assert 'X-Frame-Options' in response.headers
        assert 'X-Content-Type-Options' in response.headers
        assert 'X-XSS-Protection' in response.headers
        assert 'Strict-Transport-Security' in response.headers
        
        # Vérifier les valeurs
        assert response.headers['X-Frame-Options'] == 'DENY'
        assert response.headers['X-Content-Type-Options'] == 'nosniff'
        assert response.headers['X-XSS-Protection'] == '1; mode=block'

def test_concurrent_requests():
    """Test de requêtes concurrentes"""
    import threading
    import time
    
    results = []
    errors = []
    
    def make_request():
        try:
            img = Image.new('RGB', (50, 50), color='blue')
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            files = {'file': ('concurrent.png', img_bytes, 'image/png')}
            response = client.post('/image-to-pdf', files=files)
            results.append(response.status_code)
        except Exception as e:
            errors.append(str(e))
    
    # Lancer 5 threads simultanément
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=make_request)
        threads.append(thread)
        thread.start()
    
    # Attendre que tous les threads terminent
    for thread in threads:
        thread.join()
    
    # Tous devraient réussir
    assert len(errors) == 0, f"Erreurs: {errors}"
    assert all(status == 200 for status in results), f"Statuts inattendus: {results}"

if __name__ == "__main__":
    # Lancer les tests avec pytest
    pytest.main([__file__, "-v"])