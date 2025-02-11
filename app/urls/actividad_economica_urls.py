
from django.urls import path
from app.views.actividad_economica_views import ActividadEconomicaList


app_name = 'actividad_economica'

urlpatterns = [      

    path('list/', ActividadEconomicaList.as_view(), name='list'),

]     





