
from django.urls import path
from app.views.cliente_views import HolaMundoView

app_name = 'cliente'

urlpatterns = [
    
    path('hola/', HolaMundoView.as_view()),  # Para CBV
]

