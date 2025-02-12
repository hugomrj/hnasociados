
from django.urls import path
from app.views.actividad_economica_views import (
    ActividadEconomicaCreateView,
    ActividadEconomicaListView
)


app_name = 'actividad_economica'

urlpatterns = [      

    path('list/', ActividadEconomicaListView.as_view(), name='list'),
    path('add/', ActividadEconomicaCreateView.as_view(), name='add'),
]     





