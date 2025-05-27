from django import forms
from django.db import models


class Obligacion(models.Model):
    obligacion = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=120)

    class Meta:
        managed = False
        db_table = 'obligaciones'

    def __str__(self):
        return f"{self.obligacion} - {self.descripcion}"  # Representación legible



class ObligacionForm(forms.ModelForm):
    class Meta:
        model = Obligacion
        fields = ['obligacion', 'descripcion']

        
