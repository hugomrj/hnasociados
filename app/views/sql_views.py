import os
import subprocess
from django.http import HttpResponse
from django.conf import settings
import datetime
from django.contrib.auth.decorators import login_required


@login_required
def backup_sql(request):
    db = settings.DATABASES['default']

    file_name = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"

    command = [
        "pg_dump",
        "-h", db["HOST"],
        "-p", str(db["PORT"]),
        "-U", db["USER"],
        "-d", db["NAME"],
        "-F", "p"
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            env={"PGPASSWORD": db["PASSWORD"]}
        )
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"Error: {e.stderr}", status=500)

    response = HttpResponse(result.stdout, content_type="application/sql")
    response["Content-Disposition"] = f'attachment; filename="{file_name}"'
    return response






@login_required
def restore_database(request):
    # Archivo SQL fijo (lo cambiás manualmente)
    SQL_FILE = "/home/hugo/Descargas/backup_server.sql"

    # Si el archivo no existe o está vacío → no hacer nada
    if not SQL_FILE or not os.path.isfile(SQL_FILE) or os.path.getsize(SQL_FILE) == 0:
        return HttpResponse("Archivo SQL vacío o inexistente. No se realizó ninguna restauración.")

    db = settings.DATABASES['default']

    db_name = db["NAME"]
    db_user = db["USER"]
    db_host = db["HOST"]
    db_port = str(db["PORT"])
    db_pass = db["PASSWORD"]

    env = {"PGPASSWORD": db_pass}

    # 0. Cerrar conexiones activas
    terminate_cmd = [
        "psql",
        "-h", db_host,
        "-p", db_port,
        "-U", db_user,
        "-c",
        f"""
        SELECT pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE datname = '{db_name}'
        AND pid <> pg_backend_pid();
        """
    ]

    # 1. DROP DATABASE
    drop_cmd = [
        "psql", "-h", db_host, "-p", db_port,
        "-U", db_user,
        "-c", f"DROP DATABASE IF EXISTS {db_name};"
    ]

    # 2. CREATE DATABASE
    create_cmd = [
        "psql", "-h", db_host, "-p", db_port,
        "-U", db_user,
        "-c", f"CREATE DATABASE {db_name};"
    ]

    # 3. RESTORE DATABASE
    restore_cmd = [
        "psql", "-h", db_host, "-p", db_port,
        "-U", db_user,
        "-d", db_name,
        "-f", SQL_FILE
    ]

    try:
        subprocess.run(terminate_cmd, check=True, env=env)
        subprocess.run(drop_cmd, check=True, env=env)
        subprocess.run(create_cmd, check=True, env=env)
        subprocess.run(restore_cmd, check=True, env=env)
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"Error ejecutando restauración: {e.stderr}", status=500)

    return HttpResponse(f"Base restaurada correctamente desde {SQL_FILE}")