
from django import forms
from django.db import models
from django.apps import apps  

class ClientesObligaciones(models.Model):
    cliente = models.ForeignKey("app.Cliente", 
                on_delete=models.CASCADE)  # ✅ Referencia por nombre de la app y modelo
    obligacion = models.IntegerField()

    class Meta:
        db_table = 'clientes_obligaciones'


class ClientesObligacionesForm(forms.ModelForm):
    class Meta:
        model = ClientesObligaciones
        fields = ['obligacion']
