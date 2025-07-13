from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from autenticazione.models import CustomUser
from utenti.models import Acquirente, Venditore


# Create your models here.
class Articolo(models.Model):
    class Categoria(models.TextChoices):
        GENERALE = 'GN', 'Generale'
        ELETTRONICA = 'EL', 'Elettronica'
        CIBO = 'CB', 'Cibo'
        CANCELLERIA = 'CA', 'Cancelleria'

    nome = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    prezzo = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    profilo = models.OneToOneField('Immagine', on_delete=models.PROTECT, related_name='immagine_profilo',
                                   blank=True, null=True)  # 'Immagine' perché i due modelli si contengono a vicenda
    venditore = models.ForeignKey(Venditore, on_delete=models.CASCADE)
    categoria = models.CharField(max_length=2, choices=Categoria.choices, default=Categoria.GENERALE)
    descrizione = models.TextField()
    num_articoli = models.IntegerField()
    sconto_percentuale = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    visualizzabile = models.BooleanField(default=True)

    def __str__(self):
        return 'articolo_' + str(self.pk) + '_' + self.nome

    class Meta:
        permissions = [
            ("puo_modificare_articolo", "Può modificare un'articolo"),
            ("puo_acquistare_articolo", "Può acquistare un'articolo"),
            ("puo_aggiungere_articolo", "Può aggiungere un'articolo"),
        ]


class Immagine(models.Model):
    immagine = models.ImageField()
    articolo = models.ForeignKey(Articolo, on_delete=models.CASCADE)

    def __str__(self):
        return 'immagine_' + str(self.pk) + '_' + self.articolo.nome



class Carrello(models.Model):
    articoli = models.ManyToManyField(Articolo)
    acquirente = models.OneToOneField(Acquirente, on_delete=models.CASCADE)

    def __str__(self):
        return 'carrello_utente_' + str(self.acquirente.pk) + '_'  # + self.utente.user.username

    class Meta:
        permissions = [
            ("puo_aggiungere_carrello", "Può aggiungere nel carrello un articolo"),
            ("puo_visualizzare_carrello", "Può visualizzare gli articoli nel carrello"),
        ]


class Ordine(models.Model):
    articolo = models.ForeignKey(Articolo, on_delete=models.PROTECT)
    acquirente = models.ForeignKey(Acquirente, on_delete=models.CASCADE)
    data_acquisto = models.DateField()
    prezzo_acquisto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])

    def __str__(self):
        return 'ordine_' + str(self.pk) + 'utente_' + str(self.acquirente.pk) + '_' + self.acquirente.user.username

    class Meta:
        permissions = [
            ("puo_visualizzare_ordini", "Può visualizzare i dettagli degli ordini"),
        ]



class Valutazione(models.Model):
    voto = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    ordine = models.OneToOneField(Ordine, on_delete=models.CASCADE)
    commento = models.TextField(default="L'acquirente non ha voluto lasciare un commento")

    def __str__(self):
        return 'valutazione_' + str(self.pk) + 'ordine_' + str(self.ordine.articolo_id)

    class Meta:
        permissions = [
            ("puo_valutare", "Può dare una valutazione ai propri ordini"),
        ]