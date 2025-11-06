
import json
from django.db.models import Q, Value
from django.db.models.functions import Concat
from app.models.cliente_model import Cliente
from app.models.pago_model import Pago

def obtener_historial_cliente(params):
    """
    Retorna el historial de pagos de un cliente según el nombre o cédula recibidos.
    """

    datos = {"cliente": None, "historial": [], "resumen": {}}

    # intentar obtener nombre desde 'parametros'
    nombre_cliente = params.get("parametros", {}).get("nombre_cliente", "").strip()

    if not nombre_cliente:
        datos["error"] = "No se recibió el nombre o cédula del cliente."
        print("⚠️", datos["error"])
        return datos

    # reemplazar guiones bajos por espacios
    nombre_cliente = nombre_cliente.replace("_", " ")
    print("🧩 Buscando cliente:", nombre_cliente)

    # determinar si es texto o número
    if nombre_cliente.replace(" ", "").isalpha():
        # Buscar por nombre o apellido (coincidencia parcial)
        clientes = Cliente.objects.filter(
            Q(nombre__icontains=nombre_cliente) |
            Q(apellido__icontains=nombre_cliente) |
            Q(cedula__icontains=nombre_cliente) |
            Q(nombre__icontains=nombre_cliente.split()[0]) & Q(apellido__icontains=" ".join(nombre_cliente.split()[1:]))
        )
    else:
        # Buscar por número de cédula
        clientes = Cliente.objects.filter(cedula__icontains=nombre_cliente)

    total = clientes.count()
    if total == 0:
        datos["error"] = f"No se encontraron clientes para '{nombre_cliente}'."
        print("⚠️", datos["error"])
        return datos

    # Si hay demasiadas coincidencias, pedir más precisión
    if total > 3:
        datos["mensaje"] = f"Se encontraron {total} posibles coincidencias. Especifique mejor el nombre."
        datos["coincidencias"] = [
            {"nombre": c.nombre, "apellido": c.apellido, "cedula": c.cedula}
            for c in clientes[:5]
        ]
        print("⚠️", datos["mensaje"])
        return datos

    resultados = []
    for cliente in clientes:
        pagos = Pago.objects.filter(cliente=cliente).order_by("-anio_pago", "-mes_pago")

        historial = [
            {
                "anio": p.anio_pago,
                "mes": p.mes_pago,
                "fecha": p.fecha.strftime("%Y-%m-%d"),
                "monto": p.monto,
                "obs": p.obs or "",
            }
            for p in pagos
        ]

        total_pagado = sum(
            [float(p.monto) for p in pagos if str(p.monto).replace(".", "", 1).isdigit()],
            0.0,
        )

        resultados.append(
            {
                "cliente": {
                    "id": cliente.cliente,
                    "nombre": cliente.nombre,
                    "apellido": cliente.apellido,
                    "cedula": cliente.cedula,
                },
                "historial": historial,
                "resumen": {
                    "total_pagos": len(pagos),
                    "total_monto": total_pagado,
                },
            }
        )

    datos["resultado"] = resultados

    print("✅ Resultado generado:\n", json.dumps(datos, indent=2, ensure_ascii=False))
    return datos
