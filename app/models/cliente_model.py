from django import forms
from django.db import models

from app.models.cliente_actividad_model import ClientesActividades, ClientesActividadesForm


class Cliente (models.Model):
    cliente = models.AutoField(primary_key=True)
    cedula = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    timbrado = models.CharField(max_length=50, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    negocio_servicio = models.CharField(max_length=200, blank=True, null=True)
    tarifa = models.BigIntegerField(blank=True, null=True) 
    usuario_set = models.CharField(max_length=50, blank=True, null=True)
    clave_set = models.CharField(max_length=50, blank=True, null=True)


    class Meta:
        db_table = 'clientes'




class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'cedula', 'nombre', 'apellido', 'timbrado', 'celular',
            'email', 'direccion', 'negocio_servicio', 'tarifa',
            'usuario_set', 'clave_set'
        ]

        def clean_tarifa(self):
            tarifa = self.cleaned_data.get('tarifa')
            
            # Manejo de valores vacíos o nulos
            if not tarifa:
                return None
                
            # Convertir a string si no lo es (por si viene como número)
            if not isinstance(tarifa, str):
                tarifa = str(tarifa)
            
            # Limpieza exhaustiva - solo conserva dígitos y signo negativo
            cleaned = ''.join(c for c in tarifa if c.isdigit() or c == '-')
            
            # Si no quedaron dígitos después de limpiar
            if not cleaned:
                return None
                
            # Conversión a entero con manejo de errores
            try:
                return int(cleaned)
            except (ValueError, TypeError):
                raise forms.ValidationError(
                    "Formato numérico inválido. Use números enteros (ej: 1000, 2,500 o 1 000). "
                    "No incluya símbolos de moneda o decimales."
                )
    

# Creamos un formset para las actividades
ClientesActividadesFormSet = forms.inlineformset_factory(
    Cliente,  # Modelo principal
    ClientesActividades,  # Modelo relacionado
    form=ClientesActividadesForm,  # Formulario para el modelo relacionado
    extra=1
)

