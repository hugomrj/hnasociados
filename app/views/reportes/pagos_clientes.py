from django.shortcuts import render, HttpResponse
from django.db.models import Q

from app.models.cliente_model import Cliente
from app.models.pago_model import Pago
from datetime import date
from django.template.loader import render_to_string


from django.shortcuts import render
from django.db.models import Sum
from app.models.cliente_model import Cliente
from app.models.pago_model import Pago
from datetime import date, datetime
from calendar import monthrange
from django.core.paginator import Paginator
from datetime import date, timedelta
from collections import defaultdict
from weasyprint import HTML


def obtener_nombre_mes(mes):
    """Función auxiliar para obtener nombre del mes"""
    meses = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    return meses.get(mes, '')

def reporte_pagos_clientes(request):
    cedula = (request.GET.get('cedula') or "").strip()
    page = request.GET.get('page', 1)
    pdf_mes = request.GET.get('pdf_mes')
    pdf_anio = request.GET.get('pdf_anio')

    # Obtener todos los clientes para el select
    clientes = Cliente.objects.all().order_by('nombre', 'apellido')

    cliente_seleccionado = None
    meses_atrasados = 0
    meses_paginados = None

    # Buscar cliente según cédula
    if cedula and cedula != "0":
        cliente_seleccionado = Cliente.objects.filter(cedula=cedula).first()

    # Si encontramos cliente
    if cliente_seleccionado:
        hoy = date.today()
        anio_actual = hoy.year
        mes_actual = hoy.month

        # Obtener todos los pagos del cliente
        todos_pagos = Pago.objects.filter(cliente=cliente_seleccionado)
        
        # Obtener meses únicos en los que ha realizado pagos
        meses_con_pagos = todos_pagos.values_list('anio_pago', 'mes_pago').distinct()
        
        # Preparar lista de resumen de meses
        resumen_meses = []
        
        for anio, mes in meses_con_pagos:
            pagos_del_mes = todos_pagos.filter(anio_pago=anio, mes_pago=mes)
            total_pagado = sum(int(pago.monto) for pago in pagos_del_mes)
            
            # Determinar estado
            if total_pagado == 0:
                estado = "PENDIENTE"
            elif total_pagado >= cliente_seleccionado.tarifa:
                estado = "PAGADO"
            else:
                estado = "PARCIAL"
            
            # Verificar si está atrasado
            atrasado = False
            if (anio < anio_actual) or (anio == anio_actual and mes < mes_actual):
                if estado != "PAGADO":
                    atrasado = True
                    meses_atrasados += 1

            resumen_meses.append({
                'anio': anio,
                'mes': mes,
                'mes_nombre': obtener_nombre_mes(mes),  # AQUÍ SE LLAMA A LA FUNCIÓN
                'pagos': pagos_del_mes,
                'total_pagado': total_pagado,
                'estado': estado,
                'atrasado': atrasado,
                'tarifa': cliente_seleccionado.tarifa,
                'faltante': max(0, cliente_seleccionado.tarifa - total_pagado),
            })

        # Ordenar los meses por año y mes descendente
        resumen_meses.sort(key=lambda x: (x['anio'], x['mes']), reverse=True)
        
        # Paginar los meses (10 por página)
        paginator = Paginator(resumen_meses, 10)
        meses_paginados = paginator.get_page(page)

        # Verificar si se solicita PDF para un mes específico
        if pdf_mes and pdf_anio:
            return generar_pdf_recibo_mes(cliente_seleccionado, int(pdf_mes), int(pdf_anio), resumen_meses)

    context = {
        'cedula': cedula,
        'cliente_seleccionado': cliente_seleccionado,
        'clientes': clientes,
        'meses_atrasados': meses_atrasados,
        'meses_paginados': meses_paginados,
    }

    return render(request, 'reportes/pagos_clientes.html', context)

def generar_pdf_recibo_mes(cliente, mes, anio, resumen_meses):
    """Genera un PDF con el recibo de un mes específico"""
    
    # Buscar el mes específico en el resumen
    mes_info = None
    for m in resumen_meses:
        if m['anio'] == anio and m['mes'] == mes:
            mes_info = m
            break
    
    if not mes_info:
        # Si no encuentra el mes, crear uno vacío
        mes_info = {
            'anio': anio,
            'mes': mes,
            'mes_nombre': obtener_nombre_mes(mes),  # AQUÍ TAMBIÉN SE LLAMA
            'pagos': [],
            'total_pagado': 0,
            'estado': "PENDIENTE",
            'atrasado': True,
            'tarifa': cliente.tarifa,
            'faltante': cliente.tarifa,
        }
    
    # Obtener pagos de este mes específico
    pagos_mes = Pago.objects.filter(cliente=cliente, anio_pago=anio, mes_pago=mes)
    
    # Calcular meses pendientes (atrasados hasta la fecha actual)
    hoy = date.today()
    anio_actual = hoy.year
    mes_actual = hoy.month
    
    meses_pendientes = []
    total_deuda = 0
    
    for m in resumen_meses:
        if m['atrasado']:
            meses_pendientes.append({
                'anio': m['anio'],
                'mes': m['mes'],
                'mes_nombre': m['mes_nombre'],
                'faltante': m['faltante']
            })
            total_deuda += m['faltante']
    
    context = {
        'fecha_impresion': hoy,
        'cliente': cliente,
        'mes_info': mes_info,
        'pagos_mes': pagos_mes,
        'meses_pendientes': meses_pendientes,
        'total_deuda': total_deuda,
    }
    
    # Renderizar el template HTML
    html_string = render_to_string('reportes/recibo_mes_pdf.html', context)
    
    # Crear respuesta PDF
    response = HttpResponse(content_type='application/pdf')
    filename = f"recibo_{cliente.cedula}_{mes_info['mes_nombre']}_{anio}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Generar PDF
    HTML(string=html_string).write_pdf(response)
    
    return response
