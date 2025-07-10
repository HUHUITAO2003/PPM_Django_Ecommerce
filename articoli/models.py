from encodings import normalize_encoding
from symtable import Class

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from venditori.models import Venditore

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
    profilo = models.OneToOneField('Immagine', on_delete=models.PROTECT, related_name='immagine_profilo', null=True) #'Immagine' perché i due modelli si contengono a vicenda
    venditore = models.ForeignKey(Venditore, on_delete=models.CASCADE)
    categoria = models.CharField(max_length=2, choices=Categoria.choices, default=Categoria.GENERALE)
    descrizione = models.TextField()
    num_articoli = models.IntegerField()
    sconto_percentuale = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    visualizzabile = models.BooleanField(default=True)
    def __str__(self):
        return 'articolo_' + str(self.pk) + '_' + self.nome

class Immagine(models.Model):
    immagine = models.ImageField()
    articolo = models.ForeignKey(Articolo, on_delete=models.CASCADE)
    def __str__(self):
        return 'immagine_' + str(self.pk) + '_' + self.articolo.nome



