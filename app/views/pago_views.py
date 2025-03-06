from datetime import datetime as dt

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View


from app.models.cliente_model import Cliente
from app.models.pago_model import Pago, PagoForm
from config import settings



FOLDER_TEMPLATE = 'app/pago'

class PagoListView(LoginRequiredMixin, View):
    template_name = FOLDER_TEMPLATE + '/list.html'
    items_por_pagina = settings.ITEMS_POR_PAGINA  
    max_page_links = settings.MAX_PAGE_LINKS 

    def get(self, request, *args, **kwargs):
        cedula = request.GET.get('cedula', 0)
        
        # Obtener el cliente filtrando por cédula
        cliente = Cliente.objects.filter(cedula=cedula).first()  # Obtiene el primer cliente que coincida

        
        if cliente:
            # Filtrar los pagos asociados a este cliente
            pagos = Pago.objects.filter(cliente=cliente).order_by('-fecha')
            cliente_id = cliente.pk  
        else:
            pagos = []
            cliente_id = 0


        paginator = Paginator(pagos, self.items_por_pagina)
        page = request.GET.get('page', 1)


        try:
            lista = paginator.page(page)
        except PageNotAnInteger:
            lista = paginator.page(1)
        except EmptyPage:
            lista = paginator.page(paginator.num_pages)


        # Obtener todos los clientes
        clientes = Cliente.objects.all()

        # Rango de páginas a mostrar 
        current_page = lista.number
        total_pages = paginator.num_pages

        start_page = max(current_page - self.max_page_links, 1)
        end_page = min(current_page + self.max_page_links, total_pages)

        # Páginas visibles
        page_range = range(start_page, end_page + 1)


        # Obtener los parámetros actuales de la URL sin "page"
        query_params = request.GET.copy()
        query_params.pop("page", None)  # Remueve el parámetro "page" si existe

        # Si 'cedula' existe, aseguramos que esté en los parámetros
        if cedula:
            query_params["cedula"] = cedula

        # Generar la parte de la URL con los parámetros actuales
        query_string = query_params.urlencode()


        contexto = {
            'clientes': clientes,  
            'cedula': cedula,
            'lista': lista,  
            'cliente_id': cliente_id,
            'page_range': page_range,
            'query_string': f"&{query_string}" if query_string else "",  
        }

        return render(request, self.template_name, contexto)





class PagoCreateView(LoginRequiredMixin, View):
    template_name = FOLDER_TEMPLATE + '/add.html'

    def get(self, request, *args, **kwargs):
        # Obtener el cliente por su ID de la URL
        cliente_id = self.kwargs['cliente_id']
        
        try:
            # Intentamos obtener el cliente por su ID
            cliente = Cliente.objects.get(pk=cliente_id)
        except Cliente.DoesNotExist:
            # Si el cliente no existe, redirigir a la lista de pagos con un mensaje de error
            messages.error(request, 'Cliente no encontrado.')
            return redirect('pago:list')  # Asegúrate de que este es el nombre correcto de la URL para la lista de pagos

        # Inicializamos el formulario vacío
        form = PagoForm()

        contexto = {
            'form': form,
            'cliente': cliente,
            'cliente_id': cliente_id
        }

        return render(request, self.template_name, contexto)



    def post(self, request, *args, **kwargs):
        # Obtener el cliente por su ID de la URL
        cliente_id = self.kwargs['cliente_id']
        
        try:
            # Intentamos obtener el cliente por su ID
            cliente = Cliente.objects.get(pk=cliente_id)
        except Cliente.DoesNotExist:
            # Si el cliente no existe, redirigir a la lista de pagos con un mensaje de error
            messages.error(request, 'Cliente no encontrado.')
            return redirect('pago:list')  # Asegúrate de que este es el nombre correcto de la URL para la lista de pagos

        # Inicializamos el formulario con los datos enviados por el usuario
        form = PagoForm(request.POST)

        if form.is_valid():
            # Si el formulario es válido, creamos una instancia de Pago sin guardarla aún
            pago = form.save(commit=False)
            # Asignamos el cliente al pago
            pago.cliente = cliente
            # Guardamos el pago en la base de datos
            pago.save()

            # Mensaje de éxito
            messages.success(request, 'Pago registrado correctamente.')
            return redirect(f"{reverse('pago:list')}?cedula={cliente.cedula}")


        else:
            # Si el formulario no es válido, manejar los errores
            error_message = ''
            for field, field_errors in form.errors.items():
                for field_error in field_errors:
                    error_message += f'\n{field.capitalize()}: {field_error}'

            messages.error(request, error_message)
            
            # Si el formulario no es válido, mostramos los errores
            contexto = {
                'form': form,
                'cliente': cliente,
                'cliente_id': cliente_id
            }

            # Si el formulario no es válido, renderiza de nuevo con errores
            return render(request, self.template_name, contexto )







        
class PagoUpdateView(LoginRequiredMixin, View):    
    template_name = FOLDER_TEMPLATE + '/edit.html'
    
    def get(self, request, pk, *args, **kwargs):
        # Obtener el objeto a editar o mostrar 404 si no existe
        registro = get_object_or_404(Pago, pk=pk)
        form = PagoForm(instance=registro) 

        contexto = { 
            'form': form, 
            'registro': registro,
            }  

        return render(request, self.template_name, contexto)
    


    def post(self, request, pk, *args, **kwargs):


        # Obtener el objeto a editar
        registro = get_object_or_404(Pago, pk=pk)
        
        # Procesar formulario con los datos POST y la instancia
        form = PagoForm(request.POST, instance=registro)
        
        if form.is_valid():
            # Guardar cambios si el formulario es válido
            form.save() 
            
            message = 'El registro se ha actualizado correctamente.'
            messages.success(request, message)            
            return redirect(f"{reverse('pago:list')}?cedula={registro.cliente.cedula}")
        
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
                

            return render(request, self.template_name,  contexto )
        





class PagoDetailView(LoginRequiredMixin, View):    
    template_name = FOLDER_TEMPLATE + '/detail.html'

    def get(self, request, pk, *args, **kwargs):
        # Obtener el objeto a mostrar o devolver 404 si no existe
        registro = get_object_or_404(Pago, pk=pk)
        form = PagoForm(instance=registro) 
        form.fields['monto'].initial = str(registro.monto)  
        
        # Crear el contexto con el registro
        contexto = { 
            'form': form, 
            'registro': registro
            }  
        

        # Renderizar la plantilla con el contexto
        return render(request, self.template_name, contexto)











class PagoDeleteView(LoginRequiredMixin, View):
    
    def post(self, request, pk):
        try:
            # Intentamos obtener el registro
            registro = get_object_or_404(Pago, pk=pk)
            cedula = registro.cliente.cedula

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
        return redirect(f"{reverse('pago:list')}?cedula={cedula}")




