import subprocess
import tempfile
import zipfile
from io import BytesIO
import os

def convert_to_pdf(doc_path):
    """Converte o arquivo DOCX para PDF usando LibreOffice"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        output_pdf_path = tmp.name
        libreoffice_path = "/usr/bin/soffice"
        subprocess.call([libreoffice_path, '--headless', '--convert-to', 'pdf', '--outdir', tempfile.gettempdir(), doc_path])
    return output_pdf_path

def zip_pdfs(pdf_files):
    """Cria um arquivo zip contendo todos os PDFs gerados"""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for pdf_file in pdf_files:
            zip_file.write(pdf_file, os.path.basename(pdf_file))
    zip_buffer.seek(0)  # Volta o ponteiro ao início do buffer
    return zip_buffer