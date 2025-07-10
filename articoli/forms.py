from django import forms

class RicercaForm(forms.Form):
    keyword = forms.CharField(max_length=120)

class ContattoForm(forms.Form):
    nome = forms.CharField(max_length=100)
    email = forms.EmailField()
    messaggio = forms.CharField(widget=forms.Textarea)