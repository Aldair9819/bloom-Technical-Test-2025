FROM python:3.10.18-slim

# Cambiar a usuario root por problemas de permisos
USER root

# Instala dependencias necesarias para que pueda funcionar Google Chrome (todas las no listadas abajo)
# wget es necesario para descargar Google Chrome
# gnupg2 es necesario para verificar la firma del paquete de Chrome
# unzip es necesario para descomprimir archivos si es necesario
# iputils-ping es necesario para hacer ping a direcciones IP
RUN apt-get update && apt-get install -y \
    libvulkan1 \
    libxss1 \
    libappindicator3-1 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libasound2 \
    fonts-liberation \
    wget \   
    gnupg2 \
    unzip \
    iputils-ping \
    --no-install-recommends
    # --no-install-recommends evita instalar paquetes innecesarios



# Descarga e instala Google Chrome estable, para después borrar el instalador
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# Carpeta de trabajo
WORKDIR /app

# Copia requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto al iniciar el contenedor
ENTRYPOINT ["python", "-u"]
CMD ["app.py"]
