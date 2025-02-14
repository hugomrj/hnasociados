#!/bin/bash

# Detiene el script si ocurre un error
set -e

# Define la ruta del proyecto Django
PROJECT_PATH="/srv/django/sueldosbeneficios"

# Elimina el directorio existente del proyecto Django (si existe)
sudo rm -rf $PROJECT_PATH

# Cambia al directorio principal de proyectos Django
cd /srv/django

# Clona el repositorio del proyecto desde GitLab
git clone https://gitlab.com/hugomrj/sueldosbeneficios.git

# Cambia al directorio recién clonado
cd $PROJECT_PATH

# Crea un entorno virtual para el proyecto
python3 -m venv venv

# Activa el entorno virtual
source venv/bin/activate

# Actualiza pip en el entorno virtual
pip install --upgrade pip

# Instala las dependencias del proyecto desde el archivo requirements.txt
pip install -r requirements.txt

# Ejecuta collectstatic para recopilar los archivos estáticos
python manage.py collectstatic --noinput

# Desactiva el entorno virtual
deactivate

# Sustituye el archivo .env.local por .env.prod
cp .env.prod .env.local

# Recarga el daemon de systemctl para aplicar los cambios
sudo systemctl daemon-reload

# Reinicia el servicio Gunicorn para que utilice la nueva configuración
sudo systemctl restart gunicorn

echo "Actualización completada con éxito."
