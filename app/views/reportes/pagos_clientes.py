from django.shortcuts import render
from django.db.models import Q

from app.models.cliente_model import Cliente
from app.models.pago_model import Pago


def reporte_pagos_clientes(request):
    anios = Pago.objects.values_list('anio_pago', flat=True).distinct().order_by('-anio_pago')

    anio = request.GET.get('anio')
    mes = request.GET.get('mes')
    cedula = request.GET.get('cedula') or ""
    cedula = str(cedula)


    clientes = Cliente.objects.all()

    cliente_seleccionado = None

    # Si la cédula NO está vacía y NO es "0"
    if cedula and cedula != "0":
        cliente_seleccionado = Cliente.objects.filter(cedula=cedula).first()


    if cliente_seleccionado:
        print("✔ Cliente existe:", cliente_seleccionado.nombre)
    else:
        print("✘ Cliente NO existe")



    context = {
        'clientes': clientes,
        'cliente_seleccionado': cliente_seleccionado,
        'cedula': cedula,
        'anios': anios,

        'anio': int(anio) if anio else None,
        'mes': int(mes) if mes else None,
    }

    return render(request, 'reportes/pagos_clientes.html', context)







