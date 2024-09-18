import subprocess
import tempfile

def convert_to_pdf(doc_path):
    """Converte o arquivo DOCX para PDF usando LibreOffice"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        output_pdf_path = tmp.name
        libreoffice_path = "/usr/bin/soffice"
        subprocess.call([libreoffice_path, '--headless', '--convert-to', 'pdf', '--outdir', tempfile.gettempdir(), doc_path])
    return output_pdf_path
