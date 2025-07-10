from django.contrib import admin

# Register your models here.

from .models import Articolo, Immagine

admin.site.register(Articolo)
admin.site.register(Immagine)