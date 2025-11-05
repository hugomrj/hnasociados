import importlib
import traceback
import decimal
import datetime
import requests
import pkgutil
import rag.funciones 


def analizar_pregunta(pregunta: str) -> dict:
    
    API_URL = "https://japo.click/ia/analyze_question/"

    try:
        r = requests.post(API_URL, json={"question": pregunta}, timeout=20)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def buscar_clase_por_funcion(funcion_buscada: str):
    cache_funciones = {
        "Clientes": {"buscar_cliente": lambda x: "ejemplo resultado cliente"},
    }
    for clase, funciones in cache_funciones.items():
        if funcion_buscada in funciones:
            return clase
    return None






def ejecutar_funcion(funcion_nombre: str, json_params: dict):
    print("⚙️ [INICIO] ejecutar_funcion()")
    print(f"🔧 Buscando función: {funcion_nombre}")

    try:
        # Buscar en todos los módulos del paquete rag.funciones
        for _, module_name, _ in pkgutil.iter_modules(rag.funciones.__path__):
            full_module_name = f"rag.funciones.{module_name}"
            modulo = importlib.import_module(full_module_name)

            metodo = getattr(modulo, funcion_nombre, None)
            if callable(metodo):
                print(f"✅ Función encontrada en módulo: {full_module_name}")
                resultado = metodo(json_params)
                print("✅ Ejecución completada correctamente.")

                # Conversión de tipos no serializables
                def convertir(obj):
                    if isinstance(obj, decimal.Decimal):
                        return float(obj)
                    elif isinstance(obj, (datetime.date, datetime.datetime)):
                        return obj.isoformat()
                    elif isinstance(obj, dict):
                        return {k: convertir(v) for k, v in obj.items()}
                    elif isinstance(obj, list):
                        return [convertir(v) for v in obj]
                    return obj

                return convertir(resultado)

        # Si no se encontró en ningún módulo
        print(f"❌ No se encontró la función '{funcion_nombre}' en ningún módulo de rag.funciones")
        return f"❌ Error: la función '{funcion_nombre}' no existe"

    except Exception as e:
        print("💥 Excepción capturada al ejecutar la función:")
        traceback.print_exc()
        return f"❌ Error al ejecutar '{funcion_nombre}': {e}"