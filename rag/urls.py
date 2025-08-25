from django.urls import path
from . import views

urlpatterns = [
    path('hora/', views.hora_actual, name='hora_actual'),

    path('vanilla/', views.generar_vanilla, name='generar_vanilla'),
]
