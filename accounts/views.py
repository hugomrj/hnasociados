from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class login(View):    
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        # Cerrar sesión antes de mostrar la página de inicio de sesión
        logout(request)
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Cerrar sesión antes de intentar iniciar sesión nuevamente
        logout(request)        
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:                        
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Credenciales inválidas. Inténtalo de nuevo.')

        return redirect('login')  # Redirige al login si las credenciales son inválidas


class home(View, LoginRequiredMixin):
    template_name = 'accounts/home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
