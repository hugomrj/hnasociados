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


from app.models.obligacion_model import Obligacion
from app.models.cliente_obligacion_model import ClientesObligaciones
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
    













class ClienteCreateView(LoginRequiredMixin, View):    
    template_name = FOLDER_TEMPLATE + '/add.html'
    
    def get(self, request, *args, **kwargs):
        # Inicializamos el formulario vacío para el GET
        form = ClienteForm()
        detalles = [] 
        detalles_timbrado = [] 

        obligaciones = Obligacion.objects.all()
        

        contexto = { 
            'form': form, 
            'detalles': detalles,
            "detalles_timbrado": detalles_timbrado,
            'obligaciones': obligaciones,
            'mostrar_accion': True,            
        }         
                    
        request.session['detalles'] = []
        request.session['detalles_timbrado'] = []
        request.session.modified = True  # Asegura que Django guarde el cambio


        return render(request, self.template_name, contexto )
    

    def post(self, request, *args, **kwargs):
        # Procesar el formulario cuando se envía
        print(f"Datos recibidos en POST: {request.POST}") 

        # Procesar el formulario cuando se envía
        form = ClienteForm(request.POST)

        # Obtener la lista de detalles de la sesión
        detalles = request.session.get('detalles', [])

        obligaciones = Obligacion.objects.all()
                
        if form.is_valid():
            # Guardamos el formulario si es válido
            cliente = form.save()

            # guardar detalles con cabecera de cliente  
     
            for detalle in detalles:
                ClientesObligaciones.objects.create(
                    cliente=cliente,  # Asociar al cliente recién creado
                    obligacion=detalle['codigo'] 
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
                'obligaciones': obligaciones,
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
        

        
        cliente_obligacion = ClientesObligaciones.objects.filter(cliente=registro).values("obligacion")


        # Crear una lista para almacenar los detalles
        detalles = []


        # Obtener todas las descripciones en una sola consulta
        obligaciones = Obligacion.objects.filter(
            obligacion__in=[d["obligacion"] for d in cliente_obligacion]
        ).values("obligacion", "descripcion")

        
        Obligacion_dict = {a["obligacion"]: a["descripcion"] for a in obligaciones}

        # Construir la lista de detalles
        for d in cliente_obligacion:
            obligacion_codigo = d["obligacion"]
            descripcion = Obligacion_dict.get(obligacion_codigo, "Sin descripción")

            detalles.append({
                "codigo": obligacion_codigo,
                "descripcion": descripcion
            })

        # Guardar la lista actualizada en la sesión
        request.session['detalles'] = detalles

        obligaciones = Obligacion.objects.all()
        
        contexto = { 
            'form': form, 
            'registro': registro,
            'detalles': detalles,
            'obligaciones': obligaciones,
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
        obligaciones = Obligacion.objects.all()



        if form.is_valid():
            # Guardar cambios si el formulario es válido
            form.save()
            
            
            ClientesObligaciones.objects.filter(cliente=cliente).delete()

            
            for detalle in detalles:
                ClientesObligaciones.objects.create(
                    cliente=cliente,  # Asociar al cliente recién creado
                    obligacion=detalle['codigo']  # Usar el código 
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
                'obligaciones': obligaciones,
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
            
            
            ClientesObligaciones.objects.filter(cliente=cliente).delete()

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











# ver si se usa
class ClienteDetailView(LoginRequiredMixin, View):    
    template_name = FOLDER_TEMPLATE + '/detail.html'

    def get(self, request, pk, *args, **kwargs):
        # Obtener el objeto a mostrar o devolver 404 si no existe
        registro = get_object_or_404(Cliente, pk=pk)
        form = ClienteForm(instance=registro) 

        
        cliente_obligacion = ClientesObligaciones.objects.filter(cliente=registro).values("obligacion")
        
        # Crear una lista para almacenar los detalles
        detalles = []

        # Obtener todas las descripciones en una sola consulta
        obligaciones = Obligacion.objects.filter(
            obligacion__in=[d["obligacion"] for d in cliente_obligacion]
        ).values("obligacion", "descripcion")

        
        obligacion_dict = {a["obligacion"]: a["descripcion"] for a in obligaciones}

        # Construir la lista de detalles
        for d in cliente_obligacion:
            codigo = d["obligacion"]
            descripcion = obligacion_dict.get(codigo, "Sin descripción")

            detalles.append({
                "codigo": codigo,
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

