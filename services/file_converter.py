# file_converter.py

import subprocess
import tempfile
import zipfile
from io import BytesIO
import os

def convert_to_pdf(doc_path):
    """Converte o arquivo DOCX para PDF usando LibreOffice"""
    # Diretório temporário para salvar o PDF convertido
    output_dir = tempfile.gettempdir()
    libreoffice_path = "/usr/bin/soffice"

    try:
        # Comando para converter DOCX para PDF
        subprocess.run([libreoffice_path, '--headless', '--convert-to', 'pdf', '--outdir', output_dir, doc_path], check=True)
        
        # Obter o nome do arquivo PDF esperado
        pdf_file_name = os.path.basename(doc_path).replace('.docx', '.pdf')
        output_pdf_path = os.path.join(output_dir, pdf_file_name)
        
        # Verificar se o arquivo PDF foi realmente criado
        if not os.path.exists(output_pdf_path):
            raise FileNotFoundError(f"O arquivo PDF {output_pdf_path} não foi gerado.")

        return output_pdf_path

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Erro na conversão de DOCX para PDF: {e}")

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