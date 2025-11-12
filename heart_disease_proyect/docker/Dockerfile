# docker/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación y modelo
COPY app/ ./app/

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Exponer puerto
EXPOSE 5000

# Comando para ejecutar la aplicación Flask en producción
CMD ["python", "app/api.py"]