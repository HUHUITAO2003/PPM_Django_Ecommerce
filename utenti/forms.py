from django import forms
from utenti.models import Venditore, Acquirente, Portafoglio


class VenditoreForm(forms.ModelForm):
    class Meta:
        model = Venditore
        exclude = ["user"]

class AcquirenteForm(forms.ModelForm):
    class Meta:
        model = Acquirente
        exclude = ["user"]


class PortafoglioForm(forms.ModelForm):
    class Meta:
        model = Portafoglio
        exclude = ["acquirente"]
