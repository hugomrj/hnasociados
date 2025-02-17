from django.urls import path

from app.views.pago_views import PagoListView



app_name = 'pago'

urlpatterns = [      

    path('list/', PagoListView.as_view(), name='list'),
    path('list/<int:cliente>/', PagoListView.as_view(), name='list'),
    
]     
