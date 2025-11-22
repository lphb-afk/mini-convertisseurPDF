from fastapi import FastAPI, UploadFile, BackgroundTasks, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
import io
import asyncio
from docx2pdf import convert
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
from pypdf import PdfReader
import tempfile
import os
import logging
from datetime import datetime
import json

# Configuration tiers
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "30"))  # Default 30MB
TIER = os.getenv("TIER", "premium")  # free or premium

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; object-src 'none';"
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

# Configuration de la journalisation
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Mini Convertisseur PDF", docs_url=None, redoc_url=None)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Restreint en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SecurityHeadersMiddleware)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

# -------- Helper pour supprimer fichier après envoi --------
def remove_file(path):
    if os.path.exists(path):
        os.remove(path)

# -------- Image -> PDF --------
@app.post("/image-to-pdf")
@limiter.limit("10/minute")
async def image_to_pdf(request: Request, file: UploadFile):
    # Log de la requête pour audit
    logger.info(f"Image-to-PDF request - IP: {request.client.host}, File: {file.filename}, Size: {len(await file.read())} bytes")
    await file.seek(0)  # Reset file pointer after reading for size
    # Vérification du type de fichier
    allowed_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']
    allowed_mimes = ['image/png', 'image/jpeg', 'image/gif', 'image/bmp', 'image/tiff']
    if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions) or file.content_type not in allowed_mimes:
        raise HTTPException(status_code=400, detail="Type de fichier non autorisé. Seules les images sont acceptées.")

    # Vérification du nom de fichier
    if ".." in file.filename or "/" in file.filename or "\\" in file.filename:
        raise HTTPException(status_code=400, detail="Nom de fichier invalide.")

    content = await file.read()
    if len(content) > 30 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Fichier trop volumineux. Taille maximale: 30 MB")

    # Vérification du contenu de l'image
    try:
        img = Image.open(io.BytesIO(content))
        img.verify()
    except Exception:
        raise HTTPException(status_code=400, detail="Fichier image invalide.")

    def convert_image_sync():
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.utils import ImageReader

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            c = canvas.Canvas(tmp.name, pagesize=letter)
            img = Image.open(io.BytesIO(content)).convert("RGB")
            # Améliorer la qualité en upscalant et en appliquant un filtre de netteté
            img_width, img_height = img.size
            min_size = 2000  # Taille minimale pour qualité parfaite
            if img_width < min_size or img_height < min_size:
                # Upscaler pour qualité parfaite
                scale_factor = max(min_size / img_width, min_size / img_height)
                new_width = int(img_width * scale_factor)
                new_height = int(img_height * scale_factor)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Appliquer des filtres de netteté avancés
            from PIL import ImageFilter, ImageEnhance
            img = img.filter(ImageFilter.UnsharpMask(radius=1.5, percent=200, threshold=2))
            img = img.filter(ImageFilter.SHARPEN)
            # Améliorer le contraste légèrement
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.1)

            img_width, img_height = img.size
            page_width, page_height = letter
            margin = 50
            max_width = page_width - 2 * margin
            max_height = page_height - 2 * margin

            ratio = min(max_width / img_width, max_height / img_height)
            display_width = img_width * ratio
            display_height = img_height * ratio

            x = (page_width - display_width) / 2
            y = (page_height - display_height) / 2

            c.drawImage(ImageReader(img), x, y, width=display_width, height=display_height, preserveAspectRatio=True)
            c.save()
            return tmp.name

    loop = asyncio.get_event_loop()
    try:
        tmp_path = await asyncio.wait_for(loop.run_in_executor(None, convert_image_sync), timeout=60.0)
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Timeout dépassé. Traitement trop long.")
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur lors du traitement du fichier.")

    task = BackgroundTasks()
    task.add_task(remove_file, tmp_path)
    return FileResponse(tmp_path, filename="output.pdf", media_type="application/pdf",
                        background=task)

# -------- Word -> PDF --------
@app.post("/word-to-pdf")
@limiter.limit("10/minute")
async def word_to_pdf_endpoint(request: Request, file: UploadFile):
    # Vérification du type de fichier
    allowed_extensions = ['.docx', '.doc']
    allowed_mimes = ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword', 'application/octet-stream']
    if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions) or file.content_type not in allowed_mimes:
        raise HTTPException(status_code=400, detail="Type de fichier non autorisé. Seuls les documents Word sont acceptés.")

    # Vérification du nom de fichier
    if ".." in file.filename or "/" in file.filename or "\\" in file.filename:
        raise HTTPException(status_code=400, detail="Nom de fichier invalide.")

    content = await file.read()
    max_size = MAX_FILE_SIZE_MB * 1024 * 1024
    if len(content) > max_size:
        raise HTTPException(status_code=413, detail=f"Fichier trop volumineux. Taille maximale: {MAX_FILE_SIZE_MB} MB")

    def convert_word_sync():
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        output_pdf = tmp_path.replace(".docx", ".pdf")

        # Essayer docx2pdf d'abord
        try:
            convert(tmp_path, output_pdf)
        except SystemExit:
            # Si docx2pdf échoue, essayer avec unoconv (LibreOffice)
            import subprocess  # nosec B404
            try:
                subprocess.run(['unoconv', '-f', 'pdf', '-o', output_pdf, tmp_path], check=True, timeout=60)  # nosec B603 B607
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Si unoconv n'est pas disponible, lever une erreur
                raise Exception("Conversion Word vers PDF impossible. Installez Microsoft Word ou LibreOffice.")

        return tmp_path, output_pdf

    loop = asyncio.get_event_loop()
    try:
        tmp_path, output_pdf = await asyncio.wait_for(loop.run_in_executor(None, convert_word_sync), timeout=60.0)
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Timeout dépassé. Traitement trop long.")
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur lors du traitement du fichier.")

    # Supprimer fichiers temporaires après téléchargement
    task = BackgroundTasks()
    task.add_task(remove_file, tmp_path)
    task.add_task(remove_file, output_pdf)
    return FileResponse(output_pdf, filename="output.pdf", media_type="application/pdf", background=task)

# -------- PDF -> Word (texte simple) --------
@app.post("/pdf-to-word")
@limiter.limit("10/minute")
async def pdf_to_word(request: Request, file: UploadFile):
    # Vérification du type de fichier
    allowed_extensions = ['.pdf']
    allowed_mimes = ['application/pdf']
    if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions) or file.content_type not in allowed_mimes:
        raise HTTPException(status_code=400, detail="Type de fichier non autorisé. Seuls les fichiers PDF sont acceptés.")

    # Vérification du nom de fichier
    if ".." in file.filename or "/" in file.filename or "\\" in file.filename:
        raise HTTPException(status_code=400, detail="Nom de fichier invalide.")

    content = await file.read()
    max_size = MAX_FILE_SIZE_MB * 1024 * 1024
    if len(content) > max_size:
        raise HTTPException(status_code=413, detail=f"Fichier trop volumineux. Taille maximale: {MAX_FILE_SIZE_MB} MB")

    # Vérification du contenu du PDF
    try:
        PdfReader(io.BytesIO(content))
    except Exception:
        raise HTTPException(status_code=400, detail="Fichier PDF invalide.")

    def convert_pdf_to_word_sync():
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
            tmp_docx_path = tmp_docx.name

        # Utiliser pypdf pour extraire le texte
        pdf_reader = PdfReader(io.BytesIO(content))
        from docx import Document
        word_doc = Document()
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                word_doc.add_paragraph(text)
        word_doc.save(tmp_docx_path)
        return tmp_docx_path

    loop = asyncio.get_event_loop()
    try:
        tmp_docx_path = await asyncio.wait_for(loop.run_in_executor(None, convert_pdf_to_word_sync), timeout=60.0)
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Timeout dépassé. Traitement trop long.")
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur lors du traitement du fichier.")

    task = BackgroundTasks()
    task.add_task(remove_file, tmp_docx_path)
    return FileResponse(tmp_docx_path, filename="output.docx", media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        background=task)

# -------- PDF -> Images --------
@app.post("/pdf-to-images")
@limiter.limit("10/minute")
async def pdf_to_images(request: Request, file: UploadFile):
    # Vérification du type de fichier
    allowed_extensions = ['.pdf']
    allowed_mimes = ['application/pdf']
    if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions) or file.content_type not in allowed_mimes:
        raise HTTPException(status_code=400, detail="Type de fichier non autorisé. Seuls les fichiers PDF sont acceptés.")

    # Vérification du nom de fichier
    if ".." in file.filename or "/" in file.filename or "\\" in file.filename:
        raise HTTPException(status_code=400, detail="Nom de fichier invalide.")

    content = await file.read()
    max_size = MAX_FILE_SIZE_MB * 1024 * 1024
    if len(content) > max_size:
        raise HTTPException(status_code=413, detail=f"Fichier trop volumineux. Taille maximale: {MAX_FILE_SIZE_MB} MB")

    # Vérification du contenu du PDF
    try:
        PdfReader(io.BytesIO(content))
    except Exception:
        raise HTTPException(status_code=400, detail="Fichier PDF invalide.")

    def convert_pdf_to_images_sync():
        import zipfile
        import shutil
        
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                tmp_pdf.write(content)
                tmp_pdf_path = tmp_pdf.name
                logger.info(f"Created temp PDF: {tmp_pdf_path}")

            # Configuration optimale : utiliser les paramètres par défaut qui fonctionnent + format PNG
            logger.info("Starting PDF to images conversion...")
            images = convert_from_path(tmp_pdf_path, fmt='PNG')
            logger.info(f"Generated {len(images)} images")
            
            if len(images) == 0:
                raise Exception("No images generated from PDF")
                
            image_paths = []
            for i, img in enumerate(images):
                img_file = f"{tmp_pdf_path}_page_{i+1}.png"
                logger.info(f"Saving image {i+1}: {img_file} (size: {img.size})")
                img.save(img_file, "PNG")
                image_paths.append(img_file)
            
            # Créer une archive ZIP avec toutes les images
            zip_path = tmp_pdf_path + "_images.zip"
            logger.info(f"Creating ZIP archive: {zip_path}")
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for img_path in image_paths:
                    if os.path.exists(img_path):
                        logger.info(f"Adding to ZIP: {img_path}")
                        zipf.write(img_path, os.path.basename(img_path))
                    else:
                        logger.warning(f"Image not found: {img_path}")
            
            # Nettoyer le PDF temporaire
            if os.path.exists(tmp_pdf_path):
                os.remove(tmp_pdf_path)
                logger.info("Cleaned up temp PDF")
                
            return tmp_pdf_path, image_paths, zip_path
            
        except Exception as e:
            logger.error(f"Error in PDF to images conversion: {str(e)}")
            raise e

    loop = asyncio.get_event_loop()
    try:
        tmp_pdf_path, image_paths, zip_path = await asyncio.wait_for(loop.run_in_executor(None, convert_pdf_to_images_sync), timeout=60.0)
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Timeout dépassé. Traitement trop long.")
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur lors du traitement du fichier.")

    # Retourner l'archive ZIP avec toutes les images
    task = BackgroundTasks()
    for p in image_paths:
        task.add_task(remove_file, p)
    task.add_task(remove_file, tmp_pdf_path)
    task.add_task(remove_file, zip_path)
    return FileResponse(zip_path, filename="pdf_images.zip", media_type="application/zip", background=task)

# -------- OCR PDF --------
@app.post("/ocr-pdf")
@limiter.limit("10/minute")
async def ocr_pdf(request: Request, file: UploadFile):
    # Vérification du type de fichier
    allowed_extensions = ['.pdf']
    allowed_mimes = ['application/pdf']
    if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions) or file.content_type not in allowed_mimes:
        raise HTTPException(status_code=400, detail="Type de fichier non autorisé. Seuls les fichiers PDF sont acceptés.")

    # Vérification du nom de fichier
    if ".." in file.filename or "/" in file.filename or "\\" in file.filename:
        raise HTTPException(status_code=400, detail="Nom de fichier invalide.")

    content = await file.read()
    max_size = MAX_FILE_SIZE_MB * 1024 * 1024
    if len(content) > max_size:
        raise HTTPException(status_code=413, detail=f"Fichier trop volumineux. Taille maximale: {MAX_FILE_SIZE_MB} MB")

    # Vérification du contenu du PDF
    try:
        PdfReader(io.BytesIO(content))
    except Exception:
        raise HTTPException(status_code=400, detail="Fichier PDF invalide.")

    def ocr_pdf_sync():
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            tmp_pdf.write(content)
            tmp_pdf_path = tmp_pdf.name

        images = convert_from_path(tmp_pdf_path)
        full_text = ""
        for img in images:
            text = pytesseract.image_to_string(img)
            full_text += text + "\n\n"
        return tmp_pdf_path, full_text

    loop = asyncio.get_event_loop()
    try:
        tmp_pdf_path, full_text = await asyncio.wait_for(loop.run_in_executor(None, ocr_pdf_sync), timeout=60.0)
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Timeout dépassé. Traitement trop long.")
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur lors du traitement du fichier.")

    # Supprimer fichier PDF temporaire
    task = BackgroundTasks()
    task.add_task(remove_file, tmp_pdf_path)
    return {"status": "ok", "text": full_text, "cleanup": "file deleted after processing"}