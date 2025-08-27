from django import forms
from django.db import models
from datetime import date

from app.models.cliente_obligacion_model import ClientesObligaciones, ClientesObligacionesForm


class Cliente (models.Model):
    cliente = models.AutoField(primary_key=True)
    cedula = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    celular = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    negocio_servicio = models.CharField(max_length=200, blank=True, null=True)

    tarifa = models.BigIntegerField(blank=False, null=False)
    fecha_ingreso = models.DateField(default=date.today)



    usuario_set = models.CharField(max_length=50, blank=True, null=True)
    clave_set = models.CharField(max_length=50, blank=True, null=True)




    class Meta:
        db_table = 'clientes'




class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = [
            'cedula', 'nombre', 'apellido', 'celular',
            'email', 'direccion', 'negocio_servicio', 'tarifa', 'fecha_ingreso',
            'usuario_set', 'clave_set',        ]



ClientesObligacionesFormSet = forms.inlineformset_factory(
    Cliente,  # Modelo principal
    ClientesObligaciones,  # Modelo relacionado
    form=ClientesObligacionesForm,  # Formulario para el modelo relacionado
    extra=1
)

