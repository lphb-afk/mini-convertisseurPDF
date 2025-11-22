import requests
import threading
import time
import os

# URL de l'API
BASE_URL = "http://127.0.0.1:8000"

# Fichiers de test
sample_pdf = "sample.pdf"
sample_docx = "sample.docx"
sample_png = "sample.png"

def test_conversion(endpoint, file_path, num_requests=50):
    def send_request(i):
        try:
            with open(file_path, 'rb') as f:
                filename = os.path.basename(file_path)
                if file_path.endswith('.png'):
                    content_type = 'image/png'
                elif file_path.endswith('.pdf'):
                    content_type = 'application/pdf'
                elif file_path.endswith('.docx'):
                    content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                else:
                    content_type = 'application/octet-stream'
                files = {'file': (filename, f, content_type)}
                response = requests.post(f"{BASE_URL}/{endpoint}", files=files, timeout=30)
                print(f"Request {i}: {response.status_code}")
        except Exception as e:
            print(f"Request {i} failed: {e}")

    threads = []
    for i in range(num_requests):
        t = threading.Thread(target=send_request, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    print("Test de charge : 50 conversions simultanées")

    # Test Image -> PDF
    print("Test Image -> PDF...")
    test_conversion("image-to-pdf", sample_png, 50)

    # Test PDF -> Word
    print("Test PDF -> Word...")
    test_conversion("pdf-to-word", sample_pdf, 50)

    # Test Word -> PDF
    print("Test Word -> PDF...")
    test_conversion("word-to-pdf", sample_docx, 50)

    print("Tests terminés")