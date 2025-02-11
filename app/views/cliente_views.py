
from django.http import JsonResponse
from django.views import View


class HolaMundoView(View):
    def get(self, request):
        return JsonResponse({"mensaje": "Hola mundo"})