# Use a imagem oficial do Python 3 como base
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo requirements.txt para o contêiner
COPY requirements.txt /app/requirements.txt

# Instala as dependências da aplicação
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos da aplicação para o contêiner
COPY . /app

# Expõe a porta padrão que a aplicação usará (se necessário)
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python3", "app.py"]
