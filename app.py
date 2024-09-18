import streamlit as st
import pandas as pd
from services.doc_processor import generate_documents
from services.file_converter import zip_pdfs  # Importando a função de zipar PDFs


# Cabeçalho da aplicação
st.title('Gerador de Documentos e Conversor para PDF')

# Upload do arquivo Excel
uploaded_excel = st.file_uploader("Carregar arquivo Excel", type=["xlsx"])

# Organizar todos os componentes dentro de um formulário
with st.form(key='document_form'):
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
        selected_template = st.multiselect("Selecione os modelos de documento", list(
        template_choices.keys()), placeholder="Selecione um ou mais modelos")

    # Botão para enviar o formulário (submit)
    submit_button = st.form_submit_button("Gerar Documentos")

    if submit_button and uploaded_excel is not None:
        if not selected_template:
            st.warning("Selecione pelo menos um modelo.")
        else:
            # Exibe um spinner enquanto os documentos estão sendo gerados
            with st.spinner('Gerando documentos...'):
                template_paths = [template_choices[modelo]
                                  for modelo in selected_template]
                
                # Chama a função para gerar os documentos passando o DataFrame lido
                documentos_gerados = generate_documents(df, template_paths)

                # Converter documentos gerados para PDF e zipá-los
                pdf_files = [docx_file.replace('.docx', '.pdf') for docx_file in documentos_gerados]
                st.write("Arquivos gerados:", pdf_files)

                 # Zipar os PDFs usando a função no file_converter
                try:
                    zip_buffer = zip_pdfs(pdf_files)
                    st.write("Conteúdo do ZIP gerado: ", zip_buffer.getvalue()[:100])
                    st.write("Arquivo ZIP gerado com sucesso.")
                except Exception as e:
                    st.error(f"Erro ao gerar ZIP: {e}")

                # Botão para baixar o arquivo zip
                st.download_button(
                    label="Baixar Todos os PDFs",
                    data=zip_buffer,
                    file_name="documentos_gerados.zip",
                    mime="application/zip"
                )
