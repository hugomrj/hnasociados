from datetime import datetime as dt
from django.db.models.functions import Concat

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.db.models import Q, Value
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View


from app.models.actividad_economica_model import ActividadEconomica
from app.models.cliente_actividad_model import ClientesActividades
from app.models.cliente_model import Cliente, ClienteForm
from config import settings

# Definir una variable global fuera de la clase
FOLDER_TEMPLATE = 'app/cliente'

class ClienteListView(LoginRequiredMixin, View):
    template_name = FOLDER_TEMPLATE + '/list.html'
    items_por_pagina = settings.ITEMS_POR_PAGINA
    max_page_links = settings.MAX_PAGE_LINKS 

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip()
        coleccion = Cliente.objects.all()

        if query:
            # Concatenar los campos relevantes en una sola cadena
            coleccion = coleccion.annotate(
                full_text=Concat(
                    'nombre', Value(' '),
                    'apellido', Value(' '),
                    'cedula', Value(' '),
                    'timbrado', Value(' '),
                    'celular', Value(' '),
                    'email', Value(' '),
                    'direccion',
                )
            )

            # Filtrar por la concatenación
            coleccion = coleccion.filter(full_text__icontains=query)


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
    









class ClienteDetalleCreateView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        tipo = request.GET.get("tipo", "add") 
        template_name = f"{FOLDER_TEMPLATE}/{tipo}.html"  

        form = ClienteForm(request.POST)

        # Recuperar los detalles previos de la sesión o inicializarlos
        detalles = request.session.get('detalles', [])

        actividades = ActividadEconomica.objects.all()

        # Agregar los nuevos datos sin borrar los anteriores
        for key, value in request.POST.items():
            if key.startswith('codigo'):
                actividad_codigo = value
                descripcion = request.POST.get(f"descripcion{key[6:]}", '')
                
                nuevo_detalle = {
                    "codigo": actividad_codigo,
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
                "actividades": actividades,
                "mostrar_accion": True
            }

        if tipo == "edit":            
            cliente_id = request.POST.get('cliente_id')
            contexto = {
                "form": form,
                "detalles": detalles,
                "actividades": actividades,
                'cliente_id': cliente_id,
                "mostrar_accion": True
            }

        return render(request, template_name, contexto )








class ClienteDetalleDeleteView(LoginRequiredMixin, View):
    
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

        # Obtener el formulario y las actividades económicas
        form = ClienteForm(request.POST)
        actividades = ActividadEconomica.objects.all()

        # Contexto para renderizar la plantilla
        if tipo == "add":
            contexto = {
                "form": form,
                "detalles": detalles,
                "actividades": actividades,
                "mostrar_accion": True
            }

        if tipo == "edit":            
            cliente_id = request.POST.get('cliente_id')
            contexto = {
                "form": form,
                "detalles": detalles,
                "actividades": actividades,
                'cliente_id': cliente_id,
                "mostrar_accion": True
            }

        return render(request, template_name, contexto)











class ClienteCreateView(LoginRequiredMixin, View):    
    template_name = FOLDER_TEMPLATE + '/add.html'
    
    def get(self, request, *args, **kwargs):
        # Inicializamos el formulario vacío para el GET
        form = ClienteForm()
        detalles = [] 

        actividades = ActividadEconomica.objects.all()
        

        contexto = { 
            'form': form, 
            'detalles': detalles,
            'actividades': actividades,
            'mostrar_accion': True,            
        }         
                    
        request.session['detalles'] = []
        request.session.modified = True  # Asegura que Django guarde el cambio


        return render(request, self.template_name, contexto )
    

    def post(self, request, *args, **kwargs):
        # Procesar el formulario cuando se envía
        print(f"Datos recibidos en POST: {request.POST}") 

        # Procesar el formulario cuando se envía
        form = ClienteForm(request.POST)

        # Obtener la lista de detalles de la sesión
        detalles = request.session.get('detalles', [])

        actividades = ActividadEconomica.objects.all()
                
        if form.is_valid():
            # Guardamos el formulario si es válido
            cliente = form.save()

            # guardar detalles con cabecera de cliente  
            # Guardar los detalles de las actividades
            for detalle in detalles:
                ClientesActividades.objects.create(
                    cliente=cliente,  # Asociar al cliente recién creado
                    actividad=detalle['codigo']  # Usar el código de la actividad
                )

            # Limpiar la lista de detalles de la sesión después de guardar
            request.session['detalles'] = []

            message = 'El registro se ha agregado correctamente.'
            messages.success(request, message)

            # Redirigir a otra vista (puede ser una lista o éxito)
            return redirect('cliente:list')  
        
        else:
            # Si el formulario no es válido, manejar los errores
            error_message = ''
            for field, field_errors in form.errors.items():
                for field_error in field_errors:
                    error_message += f'\n{field.capitalize()}: {field_error}'
            

            # Mostrar el error en la consola para depuración
            print(f"Error al agregar registro: {error_message}")

            messages.error(request, error_message)

            contexto = { 
                'form': form, 
                'detalles': detalles,
                'actividades': actividades,
            }         
                        
            
            # Si el formulario no es válido, renderiza de nuevo con errores
            return render(request, self.template_name, contexto )
        








        
class ClienteUpdateView(LoginRequiredMixin, View):    
    template_name = FOLDER_TEMPLATE + '/edit.html'
    
    def get(self, request, pk, *args, **kwargs):
        # Obtener el objeto a editar o mostrar 404 si no existe
        registro = get_object_or_404(Cliente, pk=pk)
        
        # Inicializar el formulario con la instancia existente
        form = ClienteForm(instance=registro)
        

        # Obtener la lista de actividades del cliente
        cliente_actividad = ClientesActividades.objects.filter(cliente=registro).values("actividad")


        # Crear una lista para almacenar los detalles
        detalles = []


        # Obtener todas las descripciones en una sola consulta
        actividades = ActividadEconomica.objects.filter(
            actividad__in=[d["actividad"] for d in cliente_actividad]
        ).values("actividad", "descripcion")

        # Crear un diccionario {actividad_id: descripcion}
        actividad_dict = {a["actividad"]: a["descripcion"] for a in actividades}

        # Construir la lista de detalles
        for d in cliente_actividad:
            actividad_codigo = d["actividad"]
            descripcion = actividad_dict.get(actividad_codigo, "Sin descripción")

            detalles.append({
                "codigo": actividad_codigo,
                "descripcion": descripcion
            })

        # Guardar la lista actualizada en la sesión
        request.session['detalles'] = detalles

        actividades = ActividadEconomica.objects.all()
        
        contexto = { 
            'form': form, 
            'registro': registro,
            'detalles': detalles,
            'actividades': actividades,
            'cliente_id': registro.pk, 
            'mostrar_accion': True
            }  

        return render(request, self.template_name, contexto)
    



    def post(self, request, pk, *args, **kwargs):
        # Obtener el objeto a editar
        cliente = get_object_or_404(Cliente, pk=pk)
        

        # Procesar formulario con los datos POST y la instancia
        form = ClienteForm(request.POST, instance=cliente)
        
        # Obtener la lista de detalles de la sesión
        detalles = request.session.get('detalles', [])
        actividades = ActividadEconomica.objects.all()



        if form.is_valid():
            # Guardar cambios si el formulario es válido
            form.save()
            
            # Eliminar las actividades relacionadas con este cliente
            ClientesActividades.objects.filter(cliente=cliente).delete()

            # Guardar los detalles de las actividades
            for detalle in detalles:
                ClientesActividades.objects.create(
                    cliente=cliente,  # Asociar al cliente recién creado
                    actividad=detalle['codigo']  # Usar el código de la actividad
                )

            # Limpiar la lista de detalles de la sesión después de guardar
            request.session['detalles'] = []


            message = 'El registro se ha actualizado correctamente.'
            messages.success(request, message)
            return redirect('cliente:list')
        
        else:
            # Manejar errores de validación
            error_message = ''
            for field, field_errors in form.errors.items():
                for field_error in field_errors:
                    error_message += f'\n{field.capitalize()}: {field_error}'
            
            messages.error(request, error_message)
               
            
            contexto = { 
                'form': form, 
                'detalles': detalles,
                'actividades': actividades,
                'cliente_id': pk,  
                'registro': cliente,  
            }             
            

            return render(
                request, 
                self.template_name, contexto
            )
        










class ClienteDeleteView(LoginRequiredMixin, View):
    
    def post(self, request, pk):
        try:
            # Intentamos obtener el registro
            cliente = get_object_or_404(Cliente, pk=pk)
            
            # Eliminar las actividades relacionadas con este cliente
            ClientesActividades.objects.filter(cliente=cliente).delete()

            cliente.delete()

            # Agrega un mensaje de éxito
            messages.success(request, 'El registro ha sido eliminado correctamente.')

        except IntegrityError as e:
            # Si ocurre un error de integridad, mostramos un mensaje de error
            messages.error(request, f"Error al eliminar el registro: {str(e)}")

        except Exception as e:
            # Para otros errores, capturamos el error general
            messages.error(request, f"Hubo un problema al intentar eliminar el registro: {str(e)}")

        # Redirige a la URL obtenida
        return redirect('cliente:list')












class ClienteDetailView(LoginRequiredMixin, View):    
    template_name = FOLDER_TEMPLATE + '/detail.html'

    def get(self, request, pk, *args, **kwargs):
        # Obtener el objeto a mostrar o devolver 404 si no existe
        registro = get_object_or_404(Cliente, pk=pk)
        form = ClienteForm(instance=registro) 

        # Obtener la lista de actividades del cliente
        cliente_actividad = ClientesActividades.objects.filter(cliente=registro).values("actividad")
        
        # Crear una lista para almacenar los detalles
        detalles = []

        # Obtener todas las descripciones en una sola consulta
        actividades = ActividadEconomica.objects.filter(
            actividad__in=[d["actividad"] for d in cliente_actividad]
        ).values("actividad", "descripcion")

        # Crear un diccionario {actividad_id: descripcion}
        actividad_dict = {a["actividad"]: a["descripcion"] for a in actividades}

        # Construir la lista de detalles
        for d in cliente_actividad:
            actividad_codigo = d["actividad"]
            descripcion = actividad_dict.get(actividad_codigo, "Sin descripción")

            detalles.append({
                "codigo": actividad_codigo,
                "descripcion": descripcion
            })


        # Crear el contexto con el registro
        contexto = { 
            'form': form, 
            'registro': registro,
            'detalles': detalles,            
            'mostrar_accion': False
        }  

        # Renderizar la plantilla con el contexto
        return render(request, self.template_name, contexto)

