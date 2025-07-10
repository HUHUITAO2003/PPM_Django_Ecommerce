from django.db import models

# Create your models here.
class Venditore(models.Model):
    denominazione = models.CharField(max_length=100, unique=True)
    valutazione_media = models.FloatField(default=0.0) # TODO mettere un "trigger" che ricalcola la valutazione per ogni nuova recensione
    email = models.EmailField()
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return 'venditore_' + str(self.pk) + '_' + self.denominazione
