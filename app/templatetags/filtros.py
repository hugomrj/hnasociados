from django import template

register = template.Library()

@register.filter
def miles_puntos(value):
    try:
        value = int(value)
        return f"{value:,}".replace(",", ".")
    except:
        return value
