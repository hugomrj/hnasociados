import os
import subprocess
import shutil

# Detiene el script si ocurre un error
def run_command(command, shell=True):
    try:
        subprocess.run(command, shell=shell, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
        exit(1)

# Define la ruta del proyecto Django
PROJECT_PATH = "/srv/django/sueldosbeneficios"

# Elimina el directorio existente del proyecto Django (si existe)
if os.path.exists(PROJECT_PATH):
    print(f"Eliminando directorio existente en {PROJECT_PATH}...")
    shutil.rmtree(PROJECT_PATH)

# Cambia al directorio principal de proyectos Django
os.chdir("/srv/django")

# Clona el repositorio del proyecto desde GitLab
print("Clonando el repositorio...")
run_command("git clone https://gitlab.com/hugomrj/sueldosbeneficios.git")

# Cambia al directorio recién clonado
os.chdir(PROJECT_PATH)

# Crea un entorno virtual para el proyecto
print("Creando entorno virtual...")
run_command("python3 -m venv venv")

# Activa el entorno virtual
activate_script = os.path.join("venv", "bin", "activate")
activate_command = f"source {activate_script}"
print("Activando entorno virtual...")
run_command(activate_command)

# Actualiza pip en el entorno virtual
print("Actualizando pip...")
run_command("pip install --upgrade pip")

# Instala las dependencias del proyecto desde el archivo requirements.txt
print("Instalando dependencias...")
run_command("pip install -r requirements.txt")

# Ejecuta collectstatic para recopilar los archivos estáticos
print("Recopilando archivos estáticos...")
run_command("python manage.py collectstatic --noinput")

# Desactiva el entorno virtual (no es necesario en Python, pero lo dejamos por claridad)
print("Desactivando entorno virtual...")
deactivate_command = "deactivate"
run_command(deactivate_command)

# Sustituye el archivo .env.local por .env.prod
if os.path.exists(".env.prod"):
    print("Copiando .env.prod a .env.local...")
    shutil.copy(".env.prod", ".env.local")
else:
    print("Advertencia: No se encontró el archivo .env.prod")

# Recarga el daemon de systemctl para aplicar los cambios
print("Recargando systemctl daemon...")
run_command("sudo systemctl daemon-reload")

# Reinicia el servicio Gunicorn para que utilice la nueva configuración
print("Reiniciando Gunicorn...")
run_command("sudo systemctl restart gunicorn")

print("Actualización completada con éxito.")