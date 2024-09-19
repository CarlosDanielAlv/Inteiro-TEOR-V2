# app.py
import streamlit as st
import pandas as pd
from services.doc_processor import generate_documents
from services.file_converter import zip_pdfs  # Importando a função de zipar PDFs
from PIL import Image


# Cabeçalho da aplicação
favicon = Image.open("favicon.png")  # Pode ser .ico, .png, .jpg, etc.

st.set_page_config(
    page_title="Gerador de Inteiro TEOR",
    page_icon=favicon,  # Favicon personalizado
    layout="centered"
)

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #3498DB; color: #fff;">
  <a class="navbar-brand" href="https://youtube.com/dataprofessor" target="_blank">Data Professor</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link disabled" href="#">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://youtube.com/dataprofessor" target="_blank">YouTube</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://twitter.com/thedataprof" target="_blank">Twitter</a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)

st.markdown('''# **Gerador de Inteiro TEOR**
Gere Inteiro TEOR DA R1 e R2.
''')

# Upload do arquivo Excel
uploaded_excel = st.file_uploader("Carregar arquivo Excel", type=["xlsx"])

# Inicializa a variável zip_buffer fora do formulário para verificá-la mais tarde
zip_buffer = None

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
                template_paths = [template_choices[modelo] for modelo in selected_template]

                # Chama a função para gerar os documentos passando o DataFrame lido
                documentos_gerados = generate_documents(df, template_paths)

                # Verificar se algum arquivo PDF foi gerado
                if not documentos_gerados:
                    st.error("Nenhum documento foi gerado.")
                else:
                    try:
                        # Gerar o arquivo zip
                        zip_buffer = zip_pdfs(documentos_gerados)
                        st.write("Arquivo ZIP gerado com sucesso.")
                    except Exception as e:
                        st.error(f"Erro ao gerar ZIP: {e}")

# O botão de download deve estar fora do st.form()
if zip_buffer:
    # Botão para baixar o arquivo zip
    st.download_button(
        label="Baixar Todos os PDFs",
        data=zip_buffer,  # Passando zip_buffer diretamente, já que ele contém os bytes
        file_name="documentos_gerados.zip",
        mime="application/zip"
    )


# Adicionar o footer com HTML e CSS embutido
footer = """
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #262730;
            color: #fff;
            text-align: center;
            padding: 10px;
            font-size: 14px;
        }
    </style>
    <div class="footer">
        <p>© 2024 - Todos os direitos reservados | Desenvolvido por Carlos Daniel da Silva Alves</p>
    </div>
"""
st.markdown(footer, unsafe_allow_html=True)

st.markdown("""
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
""", unsafe_allow_html=True)