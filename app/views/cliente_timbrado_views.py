from datetime import datetime as dt


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q, Value

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View


from app.models.obligacion_model import Obligacion

from app.models.cliente_model import Cliente, ClienteForm
from config import settings

# Definir una variable global fuera de la clase
FOLDER_TEMPLATE = 'app/cliente'


class ClienteTimbradoCreateView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):


        tipo = request.GET.get("tipo", "add") 
        template_name = f"{FOLDER_TEMPLATE}/{tipo}.html"  

        form = ClienteForm(request.POST)

        # Recuperar los detalles previos de la sesión o inicializarlos
        detalles_timbrado = request.session.get('detalles_timbrado', [])
        detalles = request.session.get('detalles', [])  

        # Procesar datos del timbrado
        timbrado = request.POST.get('timbrado')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')


        # Obtener el máximo ID actual o empezar desde 1
        max_id = max([t['id'] for t in detalles_timbrado], default=0)
        nuevo_id = max_id + 1

        # Validar que existan los campos del timbrado
        if timbrado and fecha_inicio and fecha_fin:
            nuevo_timbrado = {
                'timbrado': timbrado,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'id': nuevo_id  # ID numérico autoincremental
            }

            # Evitar duplicados (opcional)
            if not any(t['timbrado'] == timbrado for t in detalles_timbrado):
                detalles_timbrado.append(nuevo_timbrado)
                request.session['detalles_timbrado'] = detalles_timbrado
                request.session.modified = True  # Asegurar que se guarde la sesión



        obligaciones = Obligacion.objects.all()

        if tipo == "add":
            contexto = {
                "form": form,
                "detalles_timbrado": detalles_timbrado,
                "detalles": detalles, 
                "obligaciones": obligaciones,
                "mostrar_accion": True
            }

        if tipo == "edit":            
            cliente_id = request.POST.get('cliente_id')
            contexto = {
                "form": form,
                "detalles_timbrado": detalles_timbrado,
                "detalles": detalles, 
                'cliente_id': cliente_id,
                "obligaciones": obligaciones,
                "mostrar_accion": True
            }



        print("\n--- DESPUÉS de procesar ---")
        print(f"Nuevo timbrado: {nuevo_timbrado}")
        print(f"Detalles actualizados: {request.session['detalles_timbrado']}")


        return render(request, template_name, contexto )








class ClienteTimbradoDeleteView(LoginRequiredMixin, View):
    
    def post(self, request, pk):

        print("Entra en delete timbrado")

        tipo = request.GET.get("tipo", "add") 
        template_name = f"{FOLDER_TEMPLATE}/{tipo}.html"  
        
        # Obtener el ID del ítem a eliminar (de POST, no de GET)
        item_id = request.POST.get('item_id')

        detalles_timbrado = request.session.get('detalles_timbrado', [])
        detalles = request.session.get('detalles', [])  
        
        
        # Filtrar para eliminar el ítem
        detalles_timbrado = [item for item in detalles_timbrado if str(item.get('id')) != str(item_id)]
        
        # Actualizar la sesión
        request.session['detalles_timbrado'] = detalles_timbrado
        request.session.modified = True
        
        print("Detalles después:", detalles_timbrado)


        # Guardar la lista actualizada en la sesión
        request.session['detalles_timbrado'] = detalles_timbrado

        
        form = ClienteForm(request.POST)
        obligaciones = Obligacion.objects.all()

        # Contexto para renderizar la plantilla
        if tipo == "add":
            contexto = {
                "form": form,                
                "detalles_timbrado": detalles_timbrado,
                "detalles": detalles, 
                "obligaciones": obligaciones,
                "mostrar_accion": True
            }

        if tipo == "edit":            
            cliente_id = request.POST.get('cliente_id')
            contexto = {
                "form": form,                
                "detalles_timbrado": detalles_timbrado,
                "detalles": detalles, 
                "obligaciones": obligaciones,
                'cliente_id': cliente_id,
                "mostrar_accion": True
            }

        return render(request, template_name, contexto)





