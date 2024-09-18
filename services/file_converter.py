import subprocess
import tempfile
import zipfile
from io import BytesIO
import os

def convert_to_pdf(doc_path, output_pdf_path):
    """Converte o arquivo DOCX para PDF usando LibreOffice e salva com o nome correto."""
    libreoffice_path = "/usr/bin/soffice"  # Certifique-se de que este caminho está correto para o LibreOffice
    # Chamando o LibreOffice para realizar a conversão
    subprocess.call([libreoffice_path, '--headless', '--convert-to', 'pdf', '--outdir', os.path.dirname(output_pdf_path), doc_path])
    
    # Retornar o caminho do PDF gerado
    return output_pdf_path

def zip_pdfs(pdf_files):
    """Cria um arquivo zip contendo todos os PDFs gerados"""
    zip_buffer = BytesIO()
    
    if not pdf_files:
        raise ValueError("Nenhum PDF foi gerado para ser zipado.")
    
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for pdf_file in pdf_files:
            if os.path.exists(pdf_file):
                zip_file.write(pdf_file, os.path.basename(pdf_file))
            else:
                raise FileNotFoundError(f"Arquivo {pdf_file} não encontrado.")
    
    zip_buffer.seek(0)  # Volta o ponteiro ao início do buffer
    return zip_buffer.getvalue()  # Retorna o conteúdo do buffer para o botão de download