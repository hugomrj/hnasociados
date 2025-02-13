
from django.urls import path
from app.views.actividad_economica_views import (
    ActividadEconomicaCreateView,
    ActividadEconomicaDeleteView,
    ActividadEconomicaDetailView,
    ActividadEconomicaListView,
    ActividadEconomicaUpdateView
)


app_name = 'actividad_economica'

urlpatterns = [      

    path('list/', ActividadEconomicaListView.as_view(), name='list'),
    
    path('add/', ActividadEconomicaCreateView.as_view(), name='add'),
    path('edit/<int:pk>/', ActividadEconomicaUpdateView.as_view(),  name='edit'),
    path('delete/<int:pk>/', ActividadEconomicaDeleteView.as_view(), name='delete'), 

    path('detail/<int:pk>/', ActividadEconomicaDetailView.as_view(), name='detail'),

]     




