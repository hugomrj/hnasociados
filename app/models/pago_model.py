from decimal import Decimal
from django import forms
from django.db import models

from app.models.obligacion_model import Obligacion
from app.models.cliente_model import Cliente



class Pago(models.Model):
    pago_id = models.AutoField(primary_key=True)
    fecha = models.DateField()
    monto = models.CharField() 
    obligacion = models.ForeignKey(Obligacion, models.DO_NOTHING)
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pagos'




class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['fecha', 'monto', 'obligacion']


    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        
        if isinstance(monto, str):
            monto = monto.replace('.', '')  # Elimina los puntos
            monto = monto.replace(',', '')  # Elimina la coma (si existe)
            
        
        return monto