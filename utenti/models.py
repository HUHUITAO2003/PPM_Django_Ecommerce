from django.core.validators import MinValueValidator
from django.db import models

from autenticazione.models import CustomUser

# Create your models here.
class Venditore(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    denominazione = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return 'venditore_' + str(self.pk) + '_' + self.denominazione

    class Meta:
        permissions = [
            ("puo_visualizzare_profilo_venditore", "Può visualizzare il profilo del venditore"),
            ("puo_modificare_profilo_venditore", "Può modificare il profilo del venditore"),
        ]


class Acquirente(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    indirizzo = models.CharField(max_length=150)

    def __str__(self):
        return 'utente_' + str(self.pk) + '_' + self.user.username

    class Meta:
        permissions = [
            ("puo_visualizzare_profilo_acquirente", "Può visualizzare il profilo dell'acquirente"),
            ("puo_modificare_profilo_acquirente", "Può modificare il profilo dell'acquirente"),
        ]

class Portafoglio(models.Model):
    utente = models.OneToOneField(Acquirente, on_delete=models.CASCADE)
    credito = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0.0)])

    def __str__(self):
        return 'portafoglio_utente_' + str(self.utente.pk) + '_' + self.utente.user.username

    class Meta:
        permissions = [
            ("puo_aggiungere_credito", "Può inserire codice carta per aggiungere credito"),
        ]