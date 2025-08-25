# rag/views.py
import requests
from django.http import JsonResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

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






