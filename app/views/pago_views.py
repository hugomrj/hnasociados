from datetime import datetime as dt

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View


from app.models.cliente_views_model import Cliente
from config import settings

FOLDER_TEMPLATE = 'app/pago'

class PagoListView(LoginRequiredMixin, View):
    template_name = FOLDER_TEMPLATE + '/list.html'
    items_por_pagina = settings.ITEMS_POR_PAGINA  

    def get(self, request, *args, **kwargs):
        cedula = request.GET.get('cedula', 0)
        print(cedula)

        # Obtener el cliente filtrando por cédula
        cliente = Cliente.objects.filter(cedula=cedula).first()  # Obtiene el primer cliente que coincida

        if cliente:
            # Filtrar los pagos asociados a este cliente
            pagos = Pagos.objects.filter(cliente=cliente)
        else:
            pagos = []

        # Obtener todos los clientes
        clientes = Cliente.objects.all()

        contexto = {
            'clientes': clientes,  
            'cedula': cedula,
            'pagos': pagos,  # Pasar los pagos al contexto
        }

        return render(request, self.template_name, contexto)
