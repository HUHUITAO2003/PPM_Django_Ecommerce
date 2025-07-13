import datetime
from collections import Counter

from django.contrib.auth.decorators import login_required, permission_required
from django.forms import modelformset_factory
from django.shortcuts import render, redirect

from shop.forms import ArticoloForm, ImmagineForm
from shop.models import Articolo, Ordine, Valutazione, Carrello, Immagine
from shop.templatetags.filters import calcolo_prezzo_scontato
from shop.utils import valutazione_media
from utenti.models import Portafoglio, Acquirente


# Create your views here.

@permission_required('shop.puo_visualizzare_ordini')
@login_required(login_url="/autenticazione/accedi/")
def ordini_view(request):
    acquirente = Acquirente.objects.get(user=request.user)
    ordini = Ordine.objects.filter(acquirente=acquirente).all()
    return render(request, "ordini.html", {'ordini': ordini})


@permission_required('shop.puo_valutare')
@login_required(login_url="/autenticazione/accedi/")
def valutazione_view(request, ordine_id):
    acquirente = Acquirente.objects.get(user=request.user)
    if Ordine.objects.filter(acquirente=acquirente).filter(id=ordine_id).count() == 0:
        return render(request, "errore.html", {'messaggio': "Non ha questo ordine"})
    else:
        return render(request, "valutazione.html", {'ordine_id': ordine_id})




def immagine_view(request):
    articolo = Articolo.objects.first()
    return render(request, 'immagine.html', {'articolo': articolo})


def errore_view(request, messaggio):
    return render(request, 'errore.html', {'messaggio': messaggio})


def ricerca_view(request):
    if request.method == 'GET':
        keywords = request.GET.get('keywords').split()
        articoli = []
        for k in keywords:
            articoli += list(Articolo.objects.filter(nome__icontains=k).filter(visualizzabile=True))
        num_comparse = Counter(articoli)
        num_comparse = sorted(num_comparse.items(), key=lambda x: x[1], reverse=True)
        articoli = [c[0] for c in num_comparse]
        return render(request, 'risultato.html', {'articoli': articoli})
    return render(request, 'errore.html')


def articolo_view(request, articolo_id):
    articolo = Articolo.objects.get(id=articolo_id)
    valutazione = valutazione_media(articolo_id)
    return render(request, 'articolo.html',
                  {'articolo': articolo, 'valutazione_media': valutazione[0], 'num_voti': valutazione[1]})


@permission_required('shop.puo_acquistare_articolo')
@login_required(login_url="/autenticazione/accedi/")
def acquista_view(request, articolo_id):
    articolo = Articolo.objects.get(id=articolo_id)
    acquirente = Acquirente.objects.filter(user=request.user).first()
    portafoglio = Portafoglio.objects.filter(acquirente=acquirente).first()
    if not portafoglio:
        return render(request, "errore.html", {'messaggio': "Portafoglio non trovato"})

    prezzo_scontato = calcolo_prezzo_scontato(articolo.prezzo, articolo.sconto_percentuale)

    if portafoglio.credito >= prezzo_scontato:
        portafoglio.credito -= prezzo_scontato
        portafoglio.save()
        Ordine.objects.create(
            articolo=articolo,
            acquirente=acquirente,
            data_acquisto=datetime.date.today(),
            prezzo_acquisto=prezzo_scontato
        )
        articolo.num_articoli -= 1
        articolo.save()
        acquirente.carrello.articoli.remove(articolo)
        return ordini_view(request)
    else:
        return render(request, "errore.html", {"messaggio": "Credito insufficiente"})

@permission_required('shop.puo_valutare')
@login_required(login_url="/autenticazione/accedi/")
def valuta_view(request, ordine_id):
    ordine = Ordine.objects.get(id=ordine_id)
    stelle = request.POST.get("stelle")
    commento = request.POST.get("commento")
    Valutazione.objects.create(ordine=ordine, voto=stelle, commento=commento)
    return ordini_view(request)


@permission_required('shop.puo_visualizzare_carrello')
@login_required(login_url="/autenticazione/accedi/")
def carrello_view(request):
    acquirente = Acquirente.objects.filter(user=request.user).first()
    carrello = Carrello.objects.filter(acquirente=acquirente).first()
    if carrello:
        articoli = carrello.articoli.all()
        valutazioni = [valutazione_media(articolo.id) for articolo in articoli]
        lista = [{"articolo" : articolo,"media": valutazione[0],"len": valutazione[1]} for articolo, valutazione in zip(articoli, valutazioni)]
    else:
        lista = []
    return render(request, "carrello.html", {'lista': lista })

@permission_required('shop.puo_aggiungere_carrello')
@login_required(login_url="/autenticazione/accedi/")
def aggiungi_carrello_view(request, articolo_id):
    acquirente = Acquirente.objects.get(user=request.user)
    articolo = Articolo.objects.get(id=articolo_id)
    carrello = Carrello.objects.filter(acquirente=acquirente).first()
    if carrello is None:
        carrello = Carrello.objects.create(acquirente=acquirente)
        carrello.articoli.add(articolo)
    else:
        carrello.articoli.add(articolo)
    return carrello_view(request)

@permission_required('shop.puo_aggiungere_articolo')
@login_required(login_url="/autenticazione/accedi/")
def aggiungi_articolo_view(request):
    ImmagineFormSet = modelformset_factory(Immagine, form=ImmagineForm, extra=3)
    if request.method == "POST":
        form = ArticoloForm(request.POST)
        i_form = ImmagineForm(request.POST, request.FILES)
        i_formset = ImmagineFormSet(request.POST, request.FILES, queryset=Immagine.objects.none())
        if form.is_valid() and i_form.is_valid() and i_formset.is_valid():
            articolo = form.save(commit=False)
            articolo.venditore = request.user.venditore
            articolo.save()
            immagine_profilo = i_form.save(commit=False)
            immagine_profilo.articolo = articolo
            immagine_profilo.save()
            articolo.profilo = immagine_profilo
            articolo.save(update_fields=["profilo"])
            for form in i_formset:
                if form.cleaned_data.get('immagine'):
                    immagine = form.save(commit=False)
                    immagine.articolo = articolo
                    immagine.save()
            return redirect("home_page")
    else:
        form = ArticoloForm()
        i_form = ImmagineForm()
        i_formset = ImmagineFormSet(queryset=Immagine.objects.none())
    return render(request, "aggiungi_articolo.html", {"form": form, "i_form":i_form, "i_formset": i_formset})


def miei_articoli_view(request):
    if request.method == 'GET':
        articoli = Articolo.objects.filter(venditore = request.user.venditore).all()
        num_comparse = Counter(articoli)
        num_comparse = sorted(num_comparse.items(), key=lambda x: x[1], reverse=True)
        articoli = [c[0] for c in num_comparse]
        return render(request, 'miei_articoli.html', {'articoli': articoli})
    return render(request, 'errore.html')