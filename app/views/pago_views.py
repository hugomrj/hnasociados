from datetime import datetime as dt

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View


from app.models.cliente_views_model import Cliente, ClienteForm
from config import settings

# Definir una variable global fuera de la clase
FOLDER_TEMPLATE = 'app/pago'

class PagoListView(LoginRequiredMixin, View):
    template_name = FOLDER_TEMPLATE + '/list.html'
    items_por_pagina = settings.ITEMS_POR_PAGINA  # Eliminar duplicado

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip()
        coleccion = Cliente.objects.all()

        if query:
            # Búsqueda en todos los campos del modelo
            coleccion = coleccion.filter(
                Q(cedula__icontains=query) |
                Q(nombre__icontains=query) |
                Q(apellido__icontains=query) |
                Q(timbrado__icontains=query) |
                Q(celular__icontains=query) |
                Q(email__icontains=query) |
                Q(direccion__icontains=query)
            )

        # Resto del código de paginación...
        paginator = Paginator(coleccion, self.items_por_pagina)
        page = request.GET.get('page', 1)

        try:
            lista = paginator.page(page)
        except PageNotAnInteger:
            lista = paginator.page(1)
        except EmptyPage:
            lista = paginator.page(paginator.num_pages)

        contexto = {
            'lista': lista,
            'q': query,
        }

        return render(request, self.template_name, contexto)
    


