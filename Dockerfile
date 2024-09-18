FROM python:3.9-slim

# Instalar dependências do sistema
RUN apt-get update && \
    apt-get install -y libreoffice libreoffice-writer default-jre-headless && \
    apt-get clean

# Definir diretório de trabalho
WORKDIR /app

# Copiar todos os arquivos do projeto
COPY . .

# Instalar dependências Python
RUN pip install -r requirements.txt

# Comando de inicialização
CMD ["streamlit", "run", "app.py"]
