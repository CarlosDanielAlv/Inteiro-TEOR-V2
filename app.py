import streamlit as st
import pandas as pd
from services.doc_processor import generate_documents
from utils.file_handler import cleanup_files

# Cabeçalho da aplicação
st.title('Gerador de Documentos e Conversor para PDF')

# Upload do arquivo Excel
uploaded_excel = st.file_uploader("Carregar arquivo Excel", type=["xlsx"])

# Verifica se o arquivo foi carregado
if uploaded_excel is not None:
    # Converte o arquivo Excel carregado em um DataFrame do Pandas
    df = pd.read_excel(uploaded_excel)

    # Seleção do modelo a ser utilizado
    template_choices = {
        'Inteiro Teor Defesa da Autuação': 'modelo_da.docx',
        'Decisão de Recurso Primeira Instância': 'modelo_r1.docx',
        'Decisão de Recurso Segunda Instância': 'modelo_r2.docx'
    }
    selected_template = st.selectbox("Selecione o modelo", list(template_choices.keys()))

    # Botão para gerar o documento
    if st.button("Gerar Documento"):
        # Chama a função para gerar os documentos passando o DataFrame lido
        documentos_gerados = generate_documents(df, [template_choices[selected_template]])

        # Exibe links para download dos PDFs gerados
        for docx_file in documentos_gerados:
            pdf_file = docx_file.replace('.docx', '.pdf')
            with open(pdf_file, "rb") as f:
                st.download_button("Baixar PDF", f, file_name=pdf_file)

        # Limpar arquivos temporários
        cleanup_files()
