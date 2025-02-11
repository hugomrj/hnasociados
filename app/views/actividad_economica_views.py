from datetime import datetime as dt
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models.actividad_economica_model import ActividadEconomica
from config import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



class ActividadEconomicaList(LoginRequiredMixin, View):

    template_name = 'app/actividad_economica/list.html'
    items_por_pagina = settings.ITEMS_POR_PAGINA  

    def get(self, request):

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








