from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Permitir acceso al login, admin y archivos estáticos
        if not request.user.is_authenticated and not (
            request.path.startswith(reverse('login')) or
            request.path.startswith('/admin/') or
            request.path.startswith('/static/')
        ):
            return redirect('login')
        return self.get_response(request)
