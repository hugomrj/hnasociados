from django.shortcuts import render
from django.db.models import Q

from app.models.cliente_model import Cliente
from app.models.pago_model import Pago

def reporte_pagos_clientes(request):
    anios = Pago.objects.values_list('anio_pago', flat=True).distinct().order_by('-anio_pago')

    meses = [
        {'valor': 1, 'nombre': 'Enero'},
        {'valor': 2, 'nombre': 'Febrero'},
        {'valor': 3, 'nombre': 'Marzo'},
        {'valor': 4, 'nombre': 'Abril'},
        {'valor': 5, 'nombre': 'Mayo'},
        {'valor': 6, 'nombre': 'Junio'},
        {'valor': 7, 'nombre': 'Julio'},
        {'valor': 8, 'nombre': 'Agosto'},
        {'valor': 9, 'nombre': 'Septiembre'},
        {'valor': 10, 'nombre': 'Octubre'},
        {'valor': 11, 'nombre': 'Noviembre'},
        {'valor': 12, 'nombre': 'Diciembre'}
    ]

    estados = [
        {'valor': 'todos', 'nombre': 'Todos'},
        {'valor': 'pagado', 'nombre': 'Pagado'},
        {'valor': 'pendiente', 'nombre': 'Pendiente'}
    ]

    anio = request.GET.get('anio')
    mes = request.GET.get('mes')
    estado = request.GET.get('estado', 'todos')
    cedula = request.GET.get('cedula', '').strip()   # <-- NUEVO

    datos = []
    resumen = {'pagados': 0, 'pendientes': 0}

    if anio and mes:
        clientes = Cliente.objects.all().order_by('apellido', 'nombre')

        # aplicar filtro opcional por cédula
        if cedula:
            clientes = clientes.filter(cedula=cedula)

        pagos = Pago.objects.filter(
            anio_pago=anio,
            mes_pago=mes
        )

        pagos_dict = {pago.cliente_id: pago for pago in pagos}

        for cliente in clientes:
            pago = pagos_dict.get(cliente.cliente)
            pagado = pago is not None

            if estado == 'pagado' and not pagado:
                continue
            if estado == 'pendiente' and pagado:
                continue

            datos.append({
                'cliente': cliente,
                'pagado': pagado,
                'fecha_pago': pago.fecha if pago else None,
                'monto': pago.monto if pago else None,
                'obs': pago.obs if pago else None,
            })

            if pagado:
                resumen['pagados'] += 1
            else:
                resumen['pendientes'] += 1

    context = {
        'anios': anios,
        'meses': meses,
        'estados': estados,
        'anio': int(anio) if anio else None,
        'mes': int(mes) if mes else None,
        'estado': estado,
        'cedula': cedula,   
        'datos': datos,
        'resumen': resumen
    }

    return render(request, 'reportes/pagos_clientes.html', context)
