import subprocess

def convert_to_pdf(doc_path):
    """Converte o arquivo DOCX para PDF usando LibreOffice"""
    output_path = doc_path.replace('.docx', '.pdf')
    libreoffice_path = "D:\\Program Files\\LibreOffice\\program\\soffice.exe"  # Altere para o caminho correto
    subprocess.call([libreoffice_path, '--headless', '--convert-to', 'pdf', '--outdir', 'uploads', doc_path])
    return output_path
