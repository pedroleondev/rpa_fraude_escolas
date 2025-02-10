# Usando uma imagem oficial do Python
FROM python:3.10

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos do projeto para dentro do container
COPY . .

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Definir o comando padrão para rodar dentro do container

#ENTRYPOINT ["python", "main.py"]
CMD ["tail", "-f", "/dev/null"]
