from django import forms
from django.db import models


class ActividadEconomica(models.Model):
    actividad = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=120)

    class Meta:
        managed = False
        db_table = 'actividad_economica'

    def __str__(self):
        return f"{self.actividad} - {self.descripcion}"  # Representación legible



class ActividadEconomicaForm(forms.ModelForm):
    class Meta:
        model = ActividadEconomica
        fields = ['actividad', 'descripcion']

        
