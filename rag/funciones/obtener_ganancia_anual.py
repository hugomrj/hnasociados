# rag/funciones/obtener_ganancia_anual.py
import json
from datetime import date
from decimal import Decimal
from django.db.models import Sum

from app.models.pago_model import Pago



def obtener_ganancia_anual(params):
    """
    Calcula la ganancia anual según los parámetros recibidos.
    """
    print("📈 Ejecutando función: obtener_ganancia_anual")
    print("🧩 Parámetros recibidos:\n", json.dumps(params, indent=2, ensure_ascii=False))

    periodo = params.get("parametros", {}).get("periodo", "").lower()

    # Determinar año
    if periodo == "este_año":
        anio = date.today().year
    elif periodo.isdigit() and len(periodo) == 4:
        anio = int(periodo)
    else:
        anio = date.today().year  # valor por defecto



    print(f"📅 Año a consultar: {anio}")

    # Consultar pagos del año
    pagos = Pago.objects.filter(anio_pago=anio)
    total = pagos.aggregate(total=Sum("monto"))["total"] or 0

    # Convertir Decimal a float
    if isinstance(total, Decimal):
        total = float(total)


    # Formatear con separador de miles (sin decimales)
    total_formateado = f"{total:,.0f}".replace(",", ".")

    # Estructurar resultado
    datos = {
        "año": anio,
        "total": total_formateado,
        "moneda": "PYG",
        "detalle": {
            "cantidad_pagos": pagos.count()
        }
    }

    print("✅ Resultado generado:\n", json.dumps(datos, indent=2, ensure_ascii=False))
    return datos



# 🔹 Alias internos (simplemente llaman a la función principal)
def obtener_ganancia_ano_pasado(params):
    """
    Consulta la ganancia del año anterior.
    """
    print("📈 Ejecutando función: obtener_ganancia_ano_pasado")

    anio_pasado = date.today().year - 1
    print(f"📅 Año anterior: {anio_pasado}")

    # Insertar el año en los parámetros
    params["parametros"] = {"periodo": str(anio_pasado)}

    # Llamar a la función principal con el año ajustado
    return obtener_ganancia_anual(params)

