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
