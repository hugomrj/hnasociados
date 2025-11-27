from django.urls import path

from app.views.reportes.pagos_clientes import reporte_pagos_clientes

app_name = 'reportes'

urlpatterns = [
    path('pagos_recibidos/', reporte_pagos_clientes, name='pagos_recibidos'),

]