
from django.urls import path

from app.views.cliente_views import (
    ClienteCreateView,
    ClienteDeleteView,
    ClienteDetailView,
    ClienteListView,
    ClienteUpdateView
)




app_name = 'cliente'

urlpatterns = [      

    path('list/', ClienteListView.as_view(), name='list'),
    
    path('add/', ClienteCreateView.as_view(), name='add'),
    path('edit/<int:pk>/', ClienteUpdateView.as_view(),  name='edit'),
    path('delete/<int:pk>/', ClienteDeleteView.as_view(), name='delete'), 

    path('delete/<int:pk>/', ClienteDeleteView.as_view(), name='delete'), 
    path('detail/<int:pk>/', ClienteDetailView.as_view(), name='detail'),

]     


