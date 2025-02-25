
from django import forms
from django.db import models
from django.apps import apps  

class ClientesActividades(models.Model):
    cliente = models.ForeignKey("app.Cliente", 
                on_delete=models.CASCADE)  # ✅ Referencia por nombre de la app y modelo
    actividad = models.IntegerField()

    class Meta:
        db_table = 'clientes_actividades'


class ClientesActividadesForm(forms.ModelForm):
    class Meta:
        model = ClientesActividades
        fields = ['actividad']
