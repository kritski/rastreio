# Dockerfile

# 1. Escolhe uma imagem base oficial do Python. A versão "slim" é mais leve.
FROM python:3.11-slim-bullseye

# 2. Define o diretório de trabalho dentro do contêiner.
WORKDIR /app

# 3. Define variáveis de ambiente para garantir que os logs do Python apareçam corretamente.
ENV PYTHONUNBUFFERED=1

# 4. Copia o arquivo de dependências primeiro.
# Isso aproveita o cache do Docker: se o arquivo não mudar, o passo de instalação não será executado novamente.
COPY requirements.txt .

# 5. Instala as dependências.
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia todo o resto do código da sua aplicação para o diretório de trabalho no contêiner.
COPY . .

# 7. Expõe a porta 8080, que é a porta padrão que o Fly.io espera que a aplicação escute.
EXPOSE 8080

# 8. Define o comando para iniciar a aplicação usando o servidor Gunicorn quando o contêiner for executado.
# Ele aponta para o objeto "app" dentro do arquivo "app.py".
CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "app:app"]
