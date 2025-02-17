from django import forms
from django.db import models

from app.models.actividad_economica_model import ActividadEconomica
from app.models.cliente_views_model import Cliente


class Pagos(models.Model):
    pago_id = models.AutoField(primary_key=True)
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    actividad_economica = models.ForeignKey(ActividadEconomica, models.DO_NOTHING)
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pagos'
