from django import template

register = template.Library()

@register.filter
def calcolo_prezzo_scontato(prezzo, sconto):
    return prezzo - (prezzo * sconto /100)