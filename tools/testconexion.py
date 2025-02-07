import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db import connection

try:
    connection.ensure_connection()
    print("✅ Conexión exitosa a la base de datos")
except Exception as e:
    print(f"❌ Error de conexión: {e}")


# python tools/testconexion.py