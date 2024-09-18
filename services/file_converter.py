# file_converter.py

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

def zip_pdfs(pdf_files_with_auto):
    """Cria um arquivo zip contendo todos os PDFs gerados, renomeando conforme o número do auto"""
    zip_buffer = BytesIO()
    
    if not pdf_files_with_auto:
        raise ValueError("Nenhum PDF foi gerado para ser zipado.")
    
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for pdf_file, numero_auto in pdf_files_with_auto:
            if os.path.exists(pdf_file):
                # Renomeia o arquivo dentro do ZIP com base no número do auto
                zip_file.write(pdf_file, f"{numero_auto}.pdf")
            else:
                raise FileNotFoundError(f"Arquivo {pdf_file} não encontrado.")
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()