# Usa a imagem oficial do Python 3.13 versão slim (mais leve)
FROM python:3.13-slim

# Define variáveis de ambiente
# PYTHONDONTWRITEBYTECODE: Previne o Python de escrever arquivos .pyc
# PYTHONUNBUFFERED: Garante que os logs sejam enviados direto para o terminal (importante para Docker)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema necessárias para o adaptador do Postgres (psycopg2)
RUN apt-get update && apt-get install -y \
    git \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requisitos e instala as dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto para dentro do container
COPY . .

# Expõe a porta que o Django/Gunicorn usará
EXPOSE 8000

# Comando padrão para iniciar a aplicação
# Usa 'sh -c' para rodar múltiplos comandos: migrar -> coletar estáticos -> iniciar servidor
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:8000"]
