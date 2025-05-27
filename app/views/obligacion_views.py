from datetime import datetime as dt

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from config import settings
from app.models.obligacion_model import Obligacion, ObligacionForm


# Definir una variable global fuera de la clase
FOLDER_TEMPLATE = 'app/obligacion'

class ObligacionListView(LoginRequiredMixin, View):

    template_name = FOLDER_TEMPLATE + '/list.html'
    items_por_pagina = settings.ITEMS_POR_PAGINA  
    max_page_links = settings.MAX_PAGE_LINKS 

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip()  # Obtener parámetro de búsqueda
        coleccion = Obligacion.objects.all()

        if query:  # Si hay un término de búsqueda
            coleccion = coleccion.filter(
                Q(obligacion__icontains=query) | Q(descripcion__icontains=query)
            )

        paginator = Paginator(coleccion, self.items_por_pagina)
        page = request.GET.get('page', 1)

        try:
            lista = paginator.page(page)
        except PageNotAnInteger:
            lista = paginator.page(1)
        except EmptyPage:
            lista = paginator.page(paginator.num_pages)



        # Rango de páginas a mostrar 
        current_page = lista.number
        total_pages = paginator.num_pages
        
        start_page = max(current_page - self.max_page_links, 1)
        end_page = min(current_page + self.max_page_links, total_pages)

        # Páginas visibles
        page_range = range(start_page, end_page + 1)



        contexto = {
            'lista': lista,
            'q': query,  
            'page_range': page_range,
        }

        return render(request, self.template_name, contexto)





class ObligacionCreateView(LoginRequiredMixin, View):    
    template_name = FOLDER_TEMPLATE + '/add.html'
    
    def get(self, request, *args, **kwargs):
        # Inicializamos el formulario vacío para el GET
        form = ObligacionForm()
        return render(request, self.template_name, {'form': form})
    




    def post(self, request, *args, **kwargs):
        # Procesar el formulario cuando se envía
        print(f"Datos recibidos en POST: {request.POST}") 

        # Procesar el formulario cuando se envía
        form = ObligacionForm(request.POST)
        
        if form.is_valid():
            # Guardamos el formulario si es válido
            form.save()

            message = 'El registro se ha agregado correctamente.'
            messages.success(request, message)

            # Redirigir a otra vista (puede ser una lista o éxito)
            return redirect('obligacion:list')  
        
        else:
            # Si el formulario no es válido, manejar los errores
            error_message = ''
            for field, field_errors in form.errors.items():
                for field_error in field_errors:
                    error_message += f'\n{field.capitalize()}: {field_error}'
            

            # Mostrar el error en la consola para depuración
            print(f"Error al agregar registro: {error_message}")

            messages.error(request, error_message)
            
            # Si el formulario no es válido, renderiza de nuevo con errores
            return render(request, self.template_name, {'form': form})
        




        
class ObligacionUpdateView(LoginRequiredMixin, View):    
    template_name = FOLDER_TEMPLATE + '/edit.html'
    
    def get(self, request, pk, *args, **kwargs):
        # Obtener el objeto a editar o mostrar 404 si no existe
        registro = get_object_or_404(Obligacion, pk=pk)
        
        # Inicializar el formulario con la instancia existente
        form = ObligacionForm(instance=registro)

        contexto = { 
            'form': form, 
            'registro': registro
            }  

        return render(request, self.template_name, contexto)
    



    def post(self, request, pk, *args, **kwargs):
        # Obtener el objeto a editar
        registro = get_object_or_404(Obligacion, pk=pk)
        
        # Procesar formulario con los datos POST y la instancia
        form = ObligacionForm(request.POST, instance=registro)
        
        if form.is_valid():
            # Guardar cambios si el formulario es válido
            form.save()
            
            message = 'El registro se ha actualizado correctamente.'
            messages.success(request, message)
            return redirect('obligacion:list')
        
        else:
            # Manejar errores de validación
            error_message = ''
            for field, field_errors in form.errors.items():
                for field_error in field_errors:
                    error_message += f'\n{field.capitalize()}: {field_error}'
            
            messages.error(request, error_message)

               
            contexto = { 
                'form': form, 
                'registro': registro
                }         
            

            return render(
                request, 
                self.template_name, 
                {'form': form, 'object': contexto}
            )
        






class ObligacionDeleteView(LoginRequiredMixin, View):
    
    def post(self, request, pk):
        try:
            # Intentamos obtener el registro
            registro = get_object_or_404(Obligacion, pk=pk)
            # Si no hay error, eliminamos el registro
            registro.delete()

            # Agrega un mensaje de éxito
            messages.success(request, 'El registro ha sido eliminado correctamente.')

        except IntegrityError as e:
            # Si ocurre un error de integridad, mostramos un mensaje de error
            messages.error(request, f"Error al eliminar el registro: {str(e)}")

        except Exception as e:
            # Para otros errores, capturamos el error general
            messages.error(request, f"Hubo un problema al intentar eliminar el registro: {str(e)}")

        # Redirige a la URL obtenida
        return redirect('obligacion:list')









class ObligacionDetailView(LoginRequiredMixin, View):    
    template_name = FOLDER_TEMPLATE + '/detail.html'

    def get(self, request, pk, *args, **kwargs):
        # Obtener el objeto a mostrar o devolver 404 si no existe
        registro = get_object_or_404(Obligacion, pk=pk)
        form = ObligacionForm(instance=registro) 
        
        # Crear el contexto con el registro
        contexto = { 
            'form': form, 
            'registro': registro
            }  

        # Renderizar la plantilla con el contexto
        return render(request, self.template_name, contexto)

