from django import forms
from .models import Articolo, Immagine


class ArticoloForm(forms.ModelForm):
    class Meta:
        model = Articolo
        exclude = ['venditore', 'profilo']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'descrizione': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'visualizzabile': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ImmagineForm(forms.ModelForm):
    class Meta:
        model = Immagine
        fields = ['immagine']
        widgets = {
            'immagine': forms.ClearableFileInput()
        }