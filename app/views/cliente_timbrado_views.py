from datetime import datetime as dt


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q, Value

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
        detalles = request.session.get('detalles', [])

        obligaciones = Obligacion.objects.all()

        # Agregar los nuevos datos sin borrar los anteriores
        for key, value in request.POST.items():
            if key.startswith('codigo'):
                codigo = value
                descripcion = request.POST.get(f"descripcion{key[6:]}", '')
                
                nuevo_detalle = {
                    "codigo": codigo,
                    "descripcion": descripcion
                }
                
                # Evitar duplicados
                if nuevo_detalle not in detalles:
                    detalles.append(nuevo_detalle)

        # Guardar la lista actualizada en la sesión
        request.session['detalles'] = detalles

        if tipo == "add":
            contexto = {
                "form": form,
                "detalles": detalles,
                "obligaciones": obligaciones,
                "mostrar_accion": True
            }

        if tipo == "edit":            
            cliente_id = request.POST.get('cliente_id')
            contexto = {
                "form": form,
                "detalles": detalles,
                "obligaciones": obligaciones,
                'cliente_id': cliente_id,
                "mostrar_accion": True
            }

        return render(request, template_name, contexto )








class ClienteTimbradoDeleteView(LoginRequiredMixin, View):
    
    def post(self, request, pk):

        tipo = request.GET.get("tipo", "add") 
        template_name = f"{FOLDER_TEMPLATE}/{tipo}.html"  

        # Obtener la lista de detalles de la sesión
        detalles = request.session.get('detalles', [])
        print("Detalles:", detalles) 
        
        # Convertir el 'codigo' de cada elemento en detalles a entero
        for detalle in detalles:
            detalle['codigo'] = int(detalle['codigo'])          


        # Obtener el ID del item a borrar
        item_id = request.POST.get('item_id')
        print("item_id:", item_id) 

        item_id = int(item_id)  # Intentar convertir item_id a un entero


        # Filtrar la lista para eliminar el registro con el item_id especificado
        detalles = [detalle for detalle in detalles if detalle['codigo'] != item_id]

        print("Detalles:", detalles) 


        # Guardar la lista actualizada en la sesión
        request.session['detalles'] = detalles

        
        form = ClienteForm(request.POST)
        obligaciones = Obligacion.objects.all()

        # Contexto para renderizar la plantilla
        if tipo == "add":
            contexto = {
                "form": form,
                "detalles": detalles,
                "obligaciones": obligaciones,
                "mostrar_accion": True
            }

        if tipo == "edit":            
            cliente_id = request.POST.get('cliente_id')
            contexto = {
                "form": form,
                "detalles": detalles,
                "obligaciones": obligaciones,
                'cliente_id': cliente_id,
                "mostrar_accion": True
            }

        return render(request, template_name, contexto)





