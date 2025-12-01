from django.shortcuts import render
from django.db.models import Q

from app.models.cliente_model import Cliente
from app.models.pago_model import Pago
from datetime import date


from django.shortcuts import render
from django.db.models import Sum
from app.models.cliente_model import Cliente
from app.models.pago_model import Pago
from datetime import date, datetime
from calendar import monthrange

def reporte_pagos_clientes(request):
    cedula = (request.GET.get('cedula') or "").strip()

    # OBTENER TODOS LOS CLIENTES PARA EL SELECT
    clientes = Cliente.objects.all().order_by('nombre', 'apellido')

    cliente_seleccionado = None
    resumen_meses = []
    meses_atrasados = 0
    total_deuda = 0

    # Buscar cliente según cédula
    if cedula and cedula != "0":
        cliente_seleccionado = Cliente.objects.filter(cedula=cedula).first()

    # Si encontramos cliente → generar resumen de todos los meses
    if cliente_seleccionado:
        hoy = date.today()
        anio_actual = hoy.year
        mes_actual = hoy.month
        
        # Obtener fecha de ingreso del cliente - MANEJAR CASO None
        fecha_ingreso = cliente_seleccionado.fecha_ingreso
        
        # Si fecha_ingreso es None, usar fecha actual
        if fecha_ingreso is None:
            fecha_ingreso = hoy
            # Opcional: actualizar el registro en la base de datos
            # cliente_seleccionado.fecha_ingreso = hoy
            # cliente_seleccionado.save()
        
        mes_inicio = fecha_ingreso.month
        anio_inicio = fecha_ingreso.year
        
        # Generar lista de meses desde ingreso hasta actual
        resumen_meses = []
        
        # Recorrer desde mes de ingreso hasta mes actual
        anio = anio_inicio
        mes = mes_inicio
        
        while (anio < anio_actual) or (anio == anio_actual and mes <= mes_actual):
            # Buscar todos los pagos de este mes y año
            pagos_mes = Pago.objects.filter(
                cliente=cliente_seleccionado,
                anio_pago=anio,
                mes_pago=mes
            )
            
            # Calcular total pagado en el mes
            total_pagado_mes = 0
            for pago in pagos_mes:
                try:
                    total_pagado_mes += int(pago.monto)
                except (ValueError, TypeError):
                    # Si hay error en el monto, ignorar ese pago
                    continue
            
            # Determinar estado
            if total_pagado_mes >= cliente_seleccionado.tarifa:
                estado = "PAGADO"
            elif total_pagado_mes > 0:
                estado = "PARCIAL"
            else:
                estado = "PENDIENTE"
            
            # Verificar si está atrasado (meses anteriores no pagados)
            atrasado = False
            if estado != "PAGADO":
                # Si es un mes anterior al actual, está atrasado
                if (anio < anio_actual) or (anio == anio_actual and mes < mes_actual):
                    atrasado = True
                    meses_atrasados += 1
                    total_deuda += max(0, cliente_seleccionado.tarifa - total_pagado_mes)
            
            # Agregar al resumen
            resumen_meses.append({
                'anio': anio,
                'mes': mes,
                'mes_nombre': obtener_nombre_mes(mes),
                'pagos': pagos_mes,
                'total_pagado': total_pagado_mes,
                'estado': estado,
                'atrasado': atrasado,
                'tarifa': cliente_seleccionado.tarifa,
                'faltante': max(0, cliente_seleccionado.tarifa - total_pagado_mes),
            })
            
            # Avanzar al siguiente mes
            mes += 1
            if mes > 12:
                mes = 1
                anio += 1

    context = {
        'cedula': cedula,
        'cliente_seleccionado': cliente_seleccionado,
        'clientes': clientes,
        'resumen_meses': resumen_meses,
        'meses_atrasados': meses_atrasados,
        'total_deuda': total_deuda,
    }

    return render(request, 'reportes/pagos_clientes.html', context)

def obtener_nombre_mes(mes):
    meses = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    return meses.get(mes, '')