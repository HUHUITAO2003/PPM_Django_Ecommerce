from django import template

register = template.Library()

@register.filter
def calcolo_prezzo_scontato(prezzo, sconto):
    return (prezzo * sconto /100)