from django.urls import path

from app.views.consultas.pagos_clientes import consulta_pagos_clientes
from app.views.consultas.pagos_recibidos import consulta_pagos_recibidos


app_name = 'consultas'

urlpatterns = [
    path('pagos_recibidos/', consulta_pagos_recibidos, name='pagos_recibidos'),
    path('pagos_clientes/', consulta_pagos_clientes, name='pagos_clientes'),
]