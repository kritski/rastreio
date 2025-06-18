# Dockerfile

# 1. Escolhe uma imagem base oficial do Python. A versão "slim" é mais leve.
FROM python:3.11-slim-bullseye

# 2. Define o diretório de trabalho dentro do contêiner.
WORKDIR /app

# 3. Define variáveis de ambiente para garantir que os logs do Python apareçam corretamente.
ENV PYTHONUNBUFFERED=1

# 4. Copia o arquivo de dependências primeiro.
COPY requirements.txt .

# 5. Instala as dependências.
RUN pip install --no-cache-dir -r requirements.txt

# --- INÍCIO DA CORREÇÃO DE DNS ---
# 6. Força a escrita dos servidores DNS do Google no arquivo de configuração do sistema.
#    Esta é a nossa tentativa mais forte para resolver o "NameResolutionError".
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf && echo "nameserver 8.8.4.4" >> /etc/resolv.conf
# --- FIM DA CORREÇÃO DE DNS ---

# 7. Copia todo o resto do código da sua aplicação para o diretório de trabalho.
COPY . .

# 8. Expõe a porta 8080, que é a porta padrão que o Fly.io espera.
EXPOSE 8080

# 9. Define o comando para iniciar a aplicação usando o servidor Gunicorn.
CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "app:app"]
