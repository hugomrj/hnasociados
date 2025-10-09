from django.urls import path
from app.views.calendario_views import calendario_perpetuo

app_name = "calendario"

urlpatterns = [
    path("", calendario_perpetuo, name="list"),
]
