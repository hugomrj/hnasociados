from django import forms
from django.db import models


class ActividadEconomica(models.Model):
    actividad = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=120)

    class Meta:
        managed = False
        db_table = 'actividad_economica'





class ActividadEconomicaForm(forms.ModelForm):
    class Meta:
        model = ActividadEconomica
        fields = ['actividad', 'descripcion']