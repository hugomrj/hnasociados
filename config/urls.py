# config/urls.py

from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include

from app.views.auth_views import CambiarPassword, Home, Login, Logout
from app.views.memo_views import MemoView
from app.views.sql_views import backup_sql, restore_database

# --- Define la vista directamente aquí ---
def hola_mundo_api(request):
    data = {
        'message': 'Hola Mundo desde la API - Prueba Directa'
    }
    return JsonResponse(data)

# ELIMINAMOS app_prefix = "hnasociados/" y el include anidado
urlpatterns = [
    # Administración
    path("admin/", admin.site.urls),
    
    # Autenticación y Home (en la raíz)
    path("", Login.as_view(), name="login"),
    path("login/", Login.as_view(), name="login"),
    path("home/", Home.as_view(), name="home"),
    path("logout/", Logout.as_view(), name="logout"),
    path("cambiar-password/", CambiarPassword.as_view(), name="password_change"),

    # Módulos de la aplicación
    path("obligacion/", include("app.urls.obligacion_urls")),
    path("cliente/", include("app.urls.cliente_urls")),
    path("pago/", include("app.urls.pago_urls")),
    path("calendario/", include("app.urls.calendario_urls")),
    path('consultas/', include('app.urls.consultas_urls')),
    path('reportes/', include('app.urls.reportes_urls')),
    path('rag/', include('rag.urls')),

    # Utilidades
    path("hola/", hola_mundo_api, name="hola_mundo_api_test"),
    path("backup-sql/", backup_sql, name="backup_sql"),
    path("restore-db/", restore_database, name="restore_database"),
    path('memo/', MemoView.as_view(), name='memo'),
]