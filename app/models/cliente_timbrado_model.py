
from django import forms
from django.db import models
from django.apps import apps  



class ClientesTimbrado(models.Model):
    #  id = models.AutoField()
    cliente = models.IntegerField(blank=True, null=True)
    timbrado = models.CharField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clientes_timbrado'






class ClientesTimbradoForm(forms.ModelForm):
    class Meta:
        model = ClientesTimbrado
        fields = '__all__'         
