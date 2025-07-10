from collections import Counter
from itertools import count

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from shop.utils import valutazione_media
from articoli.forms import ContattoForm, RicercaForm
from articoli.models import Articolo
from shop.models import Valutazione, Ordine


# Create your views here.
def immagine_view(request):
    articolo = Articolo.objects.first()
    return render(request, 'immagine.html', {'articolo': articolo})


def errore_view(request):
    return render(request, 'errore.html')


def ricerca_view(request):
    if request.method == 'GET':
        print(2)
        keywords = request.GET.get('keywords').split()
        articoli = []
        for k in keywords:
            articoli += list(Articolo.objects.filter(nome__icontains=k).filter(visualizzabile=True))
        numComparse = Counter(articoli)
        numComparse = sorted(numComparse.items(), key=lambda x: x[1], reverse=True)
        articoli = [c[0] for c in numComparse]
        return render(request, 'risultato.html', {'articoli': articoli})
    return render(request, 'errore.html')


def articolo_view(request, articolo_id):
    articolo = Articolo.objects.get(id=articolo_id)
    valutazione = valutazione_media(articolo_id)
    return render(request, 'articolo.html',
                  {'articolo': articolo, 'valutazione_media': valutazione[0], 'num_voti': valutazione[1]})
