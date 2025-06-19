
from django.urls import path


from app.views.cliente_views import (
    ClienteCreateView,
    ClienteDeleteView,
    ClienteDetailView,
    ClienteListView,
    ClienteUpdateView,

)

from app.views.cliente_obligacion_views import (
    ClienteObligacionCreateView,
    ClienteObligacionDeleteView
)


from app.views.cliente_timbrado_views import (
    ClienteTimbradoCreateView,
    ClienteTimbradoDeleteView
)


app_name = 'cliente'

urlpatterns = [      

    path('list/', ClienteListView.as_view(), name='list'),
    
    path('add/', ClienteCreateView.as_view(), name='add'),
    path('edit/<int:pk>/', ClienteUpdateView.as_view(),  name='edit'),
    path('delete/<int:pk>/', ClienteDeleteView.as_view(), name='delete'), 

    path('delete/<int:pk>/', ClienteDeleteView.as_view(), name='delete'), 
    path('detail/<int:pk>/', ClienteDetailView.as_view(), name='detail'),



    path('cliente_obligacion/', ClienteObligacionCreateView.as_view(), name='cliente_obligacion'),
    path('cliente_obligacion_delete/<int:pk>/', ClienteObligacionDeleteView.as_view(), name='cliente_obligacion_delete'),



    path('cliente_timbrado/', ClienteTimbradoCreateView.as_view(), name='cliente_timbrado'),
    path('cliente_timbrado_delete/<int:pk>/', ClienteTimbradoDeleteView.as_view(), name='cliente_timbrado_delete'),

]     


