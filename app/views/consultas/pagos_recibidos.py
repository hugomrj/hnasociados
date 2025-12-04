# views_consultas.py
from django.shortcuts import render
from django.db.models import Sum
from datetime import date
from app.models.pago_model import Pago


def consulta_pagos_recibidos(request):
    
    anio_actual = date.today().year
    anio = int(request.GET.get('anio', anio_actual))

    MESES = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }

    anios = (
        Pago.objects.values_list('anio_pago', flat=True)
        .distinct()
        .order_by('-anio_pago')
    )

    pagos = (
        Pago.objects.filter(anio_pago=anio)
        .values('mes_pago')
        .annotate(total=Sum('monto'))
        .order_by('mes_pago')
    )

    totales = {MESES.get(p['mes_pago'], p['mes_pago']): p['total'] for p in pagos}
    total_anual = sum(totales.values())

    context = {
        'anio': anio,
        'anios': anios,
        'totales': totales,
        'total_anual': total_anual,
    }
    return render(request, 'consultas/pagos_recibidos.html', context)
