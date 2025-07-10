from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from articoli.models import Articolo
from utenti.models import Utente


# Create your models here.
class Ordine(models.Model):
    articolo = models.ForeignKey(Articolo, on_delete=models.PROTECT)
    utente = models.ForeignKey(Utente, on_delete=models.CASCADE)
    data_acquisto = models.DateField()
    prezzo_acquisto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])

    def __str__(self):
        return 'ordine_' + str(self.pk) + 'utente_' + str(self.utente.pk) + '_' + self.utente.username


class Valutazione(models.Model):
    voto = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    ordine = models.OneToOneField(Ordine, on_delete=models.CASCADE)

    def __str__(self):
        return 'valutazione_' + str(self.pk) + 'ordine_' + str(self.ordine.articolo_id)

class Portafoglio(models.Model):
    utente = models.OneToOneField(Utente, on_delete=models.CASCADE)
    credito = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0.0)])

    def __str__(self):
        return 'portafoglio_utente_' + str(self.utente.pk) + '_' + self.utente.username