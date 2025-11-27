"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include


from app.views.auth_views import Home, Login, Logout
from app.views.memo_views import MemoView


app_prefix = "hnasociados/"



# --- Define la vista directamente aquí ---
def hola_mundo_api(request):
    """
    Vista simple que retorna un JSON con un mensaje "Hola Mundo".
    """
    data = {
        'message': 'Hola Mundo desde la API - Prueba Directa' # Un mensaje ligeramente diferente para saber que es esta
    }
    return JsonResponse(data)




urlpatterns = [
    path(app_prefix, include([
        path("admin/", admin.site.urls),
        path("", Login.as_view(), name="login"),
        path("login/", Login.as_view(), name="login"),
        path("home/", Home.as_view(), name="home"),
        path("logout/", Logout.as_view(), name="logout"),
        path("obligacion/", include("app.urls.obligacion_urls")),
        path("cliente/", include("app.urls.cliente_urls")),
        path("pago/", include("app.urls.pago_urls")),
        path("calendario/", include("app.urls.calendario_urls")),

        # --- Añade la ruta directa para tu API Hola Mundo aquí ---
        # Esto creará una ruta en /hello/
        path("hola/", hola_mundo_api, name="hola_mundo_api_test"),

        path('consultas/', include('app.urls.consultas_urls')),
        path('reportes/', include('app.urls.reportes_urls')),
        path('rag/', include('rag.urls')),


   path('memo/', MemoView.as_view(), name='memo'),


    ])),
]







