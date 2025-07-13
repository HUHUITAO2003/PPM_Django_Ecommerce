from django.contrib import admin

from utenti.models import Portafoglio, Venditore, Acquirente

# Register your models here.
admin.site.register(Acquirente)
admin.site.register(Venditore)
admin.site.register(Portafoglio)