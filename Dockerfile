# Use the latest Python Version as the base image
FROM jupyter/scipy-notebook:python-3.10.11

USER root

#Ping y git 
RUN apt-get update \
    && apt-get -y install iputils-ping git


# Setup the working directory for the container
WORKDIR /app

#Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Install the Python dependencies using Python 
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
EXPOSE 8889

ENTRYPOINT [ "jupyter","notebook","--ip=0.0.0.0","--port=8889","--allow-root", "--no-browser" ]