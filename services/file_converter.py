import subprocess
import tempfile
import zipfile
from io import BytesIO
import os

def convert_to_pdf(docx_buffer):
    """Converte o arquivo DOCX (em memória) para PDF usando LibreOffice."""
    
    # Cria um arquivo temporário para o DOCX
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp_docx:
        tmp_docx.write(docx_buffer.getvalue())  # Escreve o conteúdo do buffer no arquivo temporário
        tmp_docx_path = tmp_docx.name  # Pega o caminho do arquivo temporário

    # Cria um nome temporário para o PDF
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_pdf:
        tmp_pdf_path = tmp_pdf.name  # Caminho para o PDF gerado

    # Caminho do LibreOffice no ambiente Linux do Streamlit Cloud
    libreoffice_path = "/usr/bin/soffice"

    # Chama o LibreOffice para converter o DOCX em PDF
    subprocess.call([
        libreoffice_path,
        '--headless',
        '--convert-to', 'pdf',
        '--outdir', tempfile.gettempdir(),
        tmp_docx_path
    ])

    # Lê o PDF gerado em memória (BytesIO)
    pdf_buffer = BytesIO()
    with open(tmp_pdf_path, 'rb') as f_pdf:
        pdf_buffer.write(f_pdf.read())  # Escreve o conteúdo do PDF no buffer
    pdf_buffer.seek(0)  # Volta o ponteiro do buffer para o início

    # Remove os arquivos temporários para evitar acúmulo
    try:
        os.remove(tmp_docx_path)
        os.remove(tmp_pdf_path)
    except Exception as e:
        print(f"Erro ao deletar arquivos temporários: {e}")

    return pdf_buffer

def zip_pdfs(pdf_files):
    """Cria um arquivo zip contendo todos os PDFs gerados"""
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for pdf_buffer, pdf_name in pdf_files:
            # Adiciona o PDF no ZIP diretamente do buffer
            zip_file.writestr(pdf_name, pdf_buffer.getvalue())
    
    zip_buffer.seek(0)  # Volta o ponteiro ao início do buffer
    return zip_buffer