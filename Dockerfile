FROM python:3.9-slim

# Instalar LibreOffice e suas dependências
RUN apt-get update && apt-get install -y libreoffice libreoffice-writer

# Instalar as dependências do Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar o código da aplicação para o container
COPY . .

# Definir o diretório de trabalho
WORKDIR /app

# if we have a packages.txt, install it here, uncomment the two lines below
# be aware that packages.txt must have LF endings only!
COPY packages.txt packages.txt
RUN xargs -a packages.txt apt-get install --yes

# Comando para rodar a aplicação Streamlit
CMD ["streamlit", "run", "app.py"]
