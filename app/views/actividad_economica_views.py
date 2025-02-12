from datetime import datetime as dt
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models.actividad_economica_model import ActividadEconomica, ActividadEconomicaForm
from config import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages


class ActividadEconomicaListView (LoginRequiredMixin, View):

    template_name = 'app/actividad_economica/list.html'
    items_por_pagina = settings.ITEMS_POR_PAGINA  

    def get(self, request, *args, **kwargs):

        coleccion = ActividadEconomica.objects.all()  
        paginator = Paginator(coleccion, self.items_por_pagina)  

        page = request.GET.get('page', 1)
                
        try:
            lista = paginator.page(page)
        except PageNotAnInteger:
            lista = paginator.page(1)  # Página 1 por defecto
        except EmptyPage:
            lista = paginator.page(paginator.num_pages)  # Última página si la página es mayor que el total de páginas
        
        contexto = {
            'lista': lista,
        }

        return render(request, self.template_name, contexto)







class ActividadEconomicaCreateView(LoginRequiredMixin, View):
    template_name = 'app/actividad_economica/add.html'
    
    def get(self, request, *args, **kwargs):
        # Inicializamos el formulario vacío para el GET
        form = ActividadEconomicaForm()
        return render(request, self.template_name, {'form': form})
    




    def post(self, request, *args, **kwargs):
        # Procesar el formulario cuando se envía
        print(f"Datos recibidos en POST: {request.POST}") 

        # Procesar el formulario cuando se envía
        form = ActividadEconomicaForm(request.POST)
        
        if form.is_valid():
            # Guardamos el formulario si es válido
            form.save()

            message = 'El registro se ha agregado correctamente.'
            messages.success(request, message)

            # Redirigir a otra vista (puede ser una lista o éxito)
            return redirect('actividad_economica_list')  # Ajusta el nombre de la URL a tu caso
        
        else:
            # Si el formulario no es válido, manejar los errores
            error_message = 'Hubo un error al agregar el registro.'
            for field, field_errors in form.errors.items():
                for field_error in field_errors:
                    error_message += f'\n{field.capitalize()}: {field_error}'
            

            # Mostrar el error en la consola para depuración
            print(f"Error al agregar registro: {error_message}")

            messages.error(request, error_message)
        
        # Si el formulario no es válido, renderiza de nuevo con errores
        return render(request, self.template_name, {'form': form})
    







        
