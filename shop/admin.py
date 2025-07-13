from django.contrib import admin

from shop.models import Ordine, Valutazione, Carrello, Articolo, Immagine

# Register your models here.
admin.site.register(Ordine)
admin.site.register(Valutazione)
admin.site.register(Carrello)
admin.site.register(Articolo)
admin.site.register(Immagine)