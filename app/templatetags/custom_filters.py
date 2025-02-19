# app/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def intcomma_dot(value):
    if value is None:
        return value
    
    # Aseguramos que el valor es un número entero, si no, lo convertimos
    value = int(value) 
    
    # Aplicamos el formato de miles y reemplazamos las comas por puntos
    value = f"{value:,}".replace(',', '.')
    
    return value
