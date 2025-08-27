from django import template
from django.utils import dateformat
import datetime

register = template.Library()

@register.filter
def miles_puntos(value):
    try:
        value = int(value)
        return f"{value:,}".replace(",", ".")
    except:
        return value





@register.filter
def to_date_input(value):
    """
    Convierte un valor a formato YYYY-MM-DD para inputs type="date"
    """
    if value is None or value == '':
        return ''
    
    # Si ya es un string en formato YYYY-MM-DD
    if isinstance(value, str) and len(value) == 10 and value[4] == '-' and value[7] == '-':
        return value
    
    # Si es un objeto date/datetime
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.strftime('%Y-%m-%d')
    
    # Si es un string en otro formato, intenta convertirlo
    try:
        from django.utils.dateparse import parse_date
        date_obj = parse_date(str(value))
        if date_obj:
            return date_obj.strftime('%Y-%m-%d')
    except:
        pass
    
    # Si no se puede convertir, devuelve el valor original
    return value