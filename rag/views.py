# rag/views.py
import requests
from django.http import JsonResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json

from rag.utils_rag import analizar_pregunta, ejecutar_funcion




def hora_actual(request):
    ahora = datetime.now()
    return JsonResponse({
        "hora": ahora.strftime("%H:%M:%S"),
        "fecha": ahora.strftime("%Y-%m-%d")
    })







@csrf_exempt
def generar_vanilla(request):
    if request.method == "POST":
        import requests
        json_prompt = request.body.decode("utf-8")
        API_URL = "https://anaojedae.pythonanywhere.com/generate/"
        try:
            r = requests.post(API_URL, data=json_prompt, headers={"Content-Type": "application/json"})
            return JsonResponse(r.json(), safe=False, status=r.status_code)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)






@csrf_exempt
def generate_rag(request):
    print("🟢 [INICIO] Petición recibida en generate_rag")

    if request.method != "POST":
        print("🔴 Método no permitido:", request.method)
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        # --- Leer body ---
        data = json.loads(request.body.decode("utf-8"))
        prompt = data.get("prompt", "")
        print("📝 Prompt recibido:", prompt)

        # --- Análisis local ---
        jsonObject = analizar_pregunta(prompt)
        print("📊 Resultado análisis:\n", json.dumps(jsonObject, indent=2, ensure_ascii=False))

        funcion = jsonObject.get("funcion", "")
        print(f"⚙️ Función detectada: {funcion}")

        # --- Ejecutar función local ---
        print(f"🚀 Intentando ejecutar función local '{funcion}'...")
        resultado = ejecutar_funcion( funcion, jsonObject)
        print("✅ Resultado local:", resultado)

        intencion = jsonObject.get("intencion", "")

        datos = data.get("datos", "")
        if isinstance(datos, dict):
            datos = json.dumps(datos, ensure_ascii=False)

        # --- Enviar a API externa (como en Java) ---
        API_URL = "https://japo.click/ia/generate_rag"
        payload = {
            "user_query": prompt,
            "context": intencion,
            "datos": json.dumps(resultado, ensure_ascii=False)
        }

        print("🌐 Enviando payload a API externa:", API_URL)
        print("📦 Payload:", payload)

        r = requests.post(API_URL, json=payload, timeout=20)
        print("🔄 Respuesta recibida:", r.status_code)

        respuesta_api = r.json()
        print("📨 Contenido de respuesta:", respuesta_api)

        return JsonResponse(respuesta_api, safe=False)

    except Exception as e:
        print("💥 Error en generate_rag:", str(e))
        return JsonResponse({"error": str(e)}, status=500)
