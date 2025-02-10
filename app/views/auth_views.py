from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin # type: ignore



class Login(View):    
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        # Cerrar sesión antes de mostrar la página de inicio de sesión
        logout(request)
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Cerrar sesión antes de intentar iniciar sesión nuevamente
        logout(request)        
            
        username = request.POST.get('username')
        password = request.POST.get('password') 
        
        # Imprimir en la consola los valores de usuario y contraseña (para depuración)
        print(f"Intento de login: usuario={username} ")
        
        user = authenticate(request, username=username, password=password)        

        if user is not None:                        
            login(request, user)        
            return redirect('home')
        else:
            messages.error(request, 'Login incorrecto')
            
        # return render(request, self.template_name)
        # Retornar la respuesta para redirigir a la página de inicio de sesión
        return redirect('login')        





class Home(View, LoginRequiredMixin):
    template_name = 'home.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)




class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')
    
    
    
    
    