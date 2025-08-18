import calendar
import datetime

from django import forms
from django.db import models
from app.models.cliente_model import Cliente



class Pago(models.Model):
    pago_id = models.AutoField(primary_key=True)
    fecha = models.DateField()
    monto = models.CharField() 
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING)
    mes_pago = models.SmallIntegerField()   # obligatorio
    anio_pago = models.SmallIntegerField()  # obligatorio

    class Meta:
        managed = False
        db_table = 'pagos'







class PagoForm(forms.ModelForm):

    mes_pago = forms.ChoiceField(
        choices=[(i, calendar.month_name[i]) for i in range(1, 13)],
        label="Mes del pago"
    )
    anio_pago = forms.IntegerField(
        label="Año del pago",
        initial=datetime.date.today().year,
        min_value=2000,  # por ejemplo
        max_value=datetime.date.today().year + 5
    )




    class Meta:
        model = Pago
        fields = ['fecha', 'monto', 'mes_pago', 'anio_pago']


    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        
        if isinstance(monto, str):
            monto = monto.replace('.', '')  # Elimina los puntos
            monto = monto.replace(',', '')  # Elimina la coma (si existe)
            
        
        return monto