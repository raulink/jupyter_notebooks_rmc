# Usar la imagen base oficial de Python
FROM python:3.9

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar las dependencias necesarias
#RUN apt-get update && apt-get install -y \
#    python3-venv \
#    && apt-get clean
# Copiar los archivos necesarios al contenedor
COPY ./app /app

# Crear el entorno virtual
#RUN python3 -m venv venv

# Activar el entorno virtual, actualizar pip y setuptools
# RUN /bin/bash -c "source /app/venv/bin/activate && python3 -m pip install --upgrade pip setuptools"
RUN python --version

RUN pip install --upgrade pip
# --no-cache-dir
RUN pip install -r requirements.txt

# Instalar los requisitos
# RUN /bin/bash -c "source /app/venv/bin/activate && pip3 install -r requirements.txt"

# Hacer que run.sh sea ejecutable
RUN chmod +x /app/run.sh

# Ejecutar run.sh
CMD ["/app/run.sh"]
