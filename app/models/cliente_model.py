from django import forms
from django.db import models

from app.models.cliente_actividad_model import ClientesActividades, ClientesActividadesForm


class Cliente (models.Model):
    cliente = models.AutoField(primary_key=True)
    cedula = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    timbrado = models.CharField(max_length=50, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'clientes'




class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cedula', 'nombre', 'apellido', 'timbrado', 'celular', 'email', 'direccion']

        


    

# Creamos un formset para las actividades
ClientesActividadesFormSet = forms.inlineformset_factory(
    Cliente,  # Modelo principal
    ClientesActividades,  # Modelo relacionado
    form=ClientesActividadesForm,  # Formulario para el modelo relacionado
    extra=1
)

