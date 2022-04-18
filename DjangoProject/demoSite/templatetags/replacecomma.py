from django import template

register = template.Library()

@register.filter
def replacecomma(value):
    return value.replace(",",", ")
