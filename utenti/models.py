from django.db import models

from articoli.models import Articolo


# Create your models here.
class Utente(models.Model):
    username = models.CharField(max_length=20)
    indirizzo = models.CharField(max_length=50)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    codice_fiscale = models.CharField(max_length=16)

    def __str__(self):
        return 'utente_' + str(self.pk) + '_' + self.username

class Carrello(models.Model):
    articoli = models.ManyToManyField(Articolo)
    utente = models.OneToOneField(Utente, on_delete=models.CASCADE)
    def __str__(self):
        return 'carrello_utente_' + str(self.utente.pk) + '_' + self.utente.username

