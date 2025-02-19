from django.urls import path

from app.views.pago_views import ( 
    PagoListView,
    PagoCreateView,
    PagoDetailView,
    PagoUpdateView
)

app_name = 'pago'

urlpatterns = [      

    path('list/', PagoListView.as_view(), name='list'),
    path('list/<int:cliente>/', PagoListView.as_view(), name='list'),
    path('edit/<int:pk>/', PagoUpdateView.as_view(),  name='edit'),


    path('add/<int:cliente_id>/', PagoCreateView.as_view(), name='add'),


    path('detail/<int:pk>/', PagoDetailView.as_view(), name='detail'),
    
]     
