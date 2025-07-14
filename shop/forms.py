from django import forms
from .models import Articolo, Immagine


class ArticoloForm(forms.ModelForm):
    class Meta:
        model = Articolo
        exclude = ['venditore', 'visualizzabile']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'descrizione': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class ImmagineForm(forms.ModelForm):
    class Meta:
        model = Immagine
        fields = ['immagine']
        widgets = {
            'immagine': forms.ClearableFileInput()
        }