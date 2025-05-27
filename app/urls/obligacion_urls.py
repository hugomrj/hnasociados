
from django.urls import path
from app.views.obligacion_views import (
    ObligacionCreateView,
    ObligacionDeleteView,
    ObligacionDetailView,
    ObligacionListView,
    ObligacionUpdateView
)


app_name = 'obligacion'

urlpatterns = [      

    path('list/', ObligacionListView.as_view(), name='list'),
    
    path('add/', ObligacionCreateView.as_view(), name='add'),
    path('edit/<int:pk>/', ObligacionUpdateView.as_view(),  name='edit'),
    path('delete/<int:pk>/', ObligacionDeleteView.as_view(), name='delete'), 

    path('detail/<int:pk>/', ObligacionDetailView.as_view(), name='detail'),

]     




