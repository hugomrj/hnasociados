from django import forms
from django.db import models


class ClientesActividades(models.Model):
    cliente = models.IntegerField(blank=True, null=True)
    actividad = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clientes_actividades'