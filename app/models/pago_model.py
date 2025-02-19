from django import forms
from django.db import models

from app.models.actividad_economica_model import ActividadEconomica
from app.models.cliente_model import Cliente



class Pago(models.Model):
    pago_id = models.AutoField(primary_key=True)
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=0)
    actividad_economica = models.ForeignKey(ActividadEconomica, models.DO_NOTHING)
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pagos'




class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['fecha', 'monto', 'actividad_economica']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'monto': forms.NumberInput(), 
            'actividad_economica': forms.Select(),
        }

