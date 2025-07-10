from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def aggiungi_carrello_view(request, articolo_id):
    return HttpResponse("Aggiungi carrelllo view")