FROM python:3.9-slim

# Atualizar a lista de pacotes e instalar dependências básicas do sistema
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libxinerama1 \
    libxcursor1 \
    libxrandr2 \
    default-jre-headless \
    libreoffice-core-nogui \
    libreoffice-writer-nogui \
    libreoffice-java-common

# Definir o diretório de trabalho
WORKDIR /app

# Copiar e instalar pacotes do sistema (se existir o packages.txt)
COPY packages.txt /app/packages.txt
RUN xargs -a /app/packages.txt apt-get install --yes

# Copiar o arquivo requirements.txt e instalar dependências Python
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar o restante do código da aplicação para o diretório de trabalho
COPY . /app

# Comando para rodar a aplicação Streamlit
CMD ["streamlit", "run", "app.py"]
