
from django.urls import path

from app.views.cliente_views import (
    ClienteCreateView,
    ClienteDeleteView,
    ClienteDetailView,
    ClienteListView,
    ClienteUpdateView,

    ClienteDetalleCreateView,
    ClienteDetalleDeleteView
)




app_name = 'cliente'

urlpatterns = [      

    path('list/', ClienteListView.as_view(), name='list'),
    
    path('add/', ClienteCreateView.as_view(), name='add'),
    path('edit/<int:pk>/', ClienteUpdateView.as_view(),  name='edit'),
    path('delete/<int:pk>/', ClienteDeleteView.as_view(), name='delete'), 

    path('delete/<int:pk>/', ClienteDeleteView.as_view(), name='delete'), 
    path('detail/<int:pk>/', ClienteDetailView.as_view(), name='detail'),



    path('clientedetalle/', ClienteDetalleCreateView.as_view(), name='clientedetalle'),
    path('clientedetalledelete/<int:pk>/', ClienteDetalleDeleteView.as_view(), name='clientedetalledelete'),



]     


