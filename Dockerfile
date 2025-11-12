# Imagen base
FROM python:3.10-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto al contenedor
COPY . /app

# Instalar dependencias
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Exponer el puerto de Streamlit
EXPOSE 8501

# Comando para iniciar el dashboard
CMD ["streamlit", "run", "dashboard/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
