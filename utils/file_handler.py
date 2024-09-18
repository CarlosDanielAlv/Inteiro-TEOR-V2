import os

def cleanup_files():
    # Função para limpar arquivos temporários após uso
    for file in os.listdir("uploads/"):
        os.remove(os.path.join("uploads/", file))
