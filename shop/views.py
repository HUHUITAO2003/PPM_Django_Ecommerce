import datetime
from collections import Counter

from PIL import Image
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from shop.forms import ArticoloForm, ImmagineForm
from shop.models import Articolo, Ordine, Valutazione, Carrello, Immagine
from shop.templatetags.filters import calcolo_prezzo_scontato
from shop.utils import valutazione_media_articolo, valutazione_media_venditore
from utenti.models import Portafoglio, Acquirente


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
    valutazione = valutazione_media_articolo(articolo_id)
    valutazioni = Valutazione.objects.filter(ordine__articolo_id=articolo_id).all()
    return render(request, 'articolo.html',
                  {'articolo': articolo, 'valutazione_media': valutazione[0], 'num_voti': valutazione[1],
                   "valutazioni": valutazioni})


# Acquirente
@permission_required('shop.puo_acquistare_articolo')
def acquista_view(request, articolo_id):
    articolo = Articolo.objects.get(id=articolo_id)
    acquirente = Acquirente.objects.filter(user=request.user).first()
    portafoglio = Portafoglio.objects.filter(acquirente=acquirente).first()
    if not portafoglio:
        return render(request, "errore.html", {'messaggio': "Portafoglio non trovato"})

    prezzo_scontato = calcolo_prezzo_scontato(articolo.prezzo, articolo.sconto_percentuale)

    if portafoglio.credito < prezzo_scontato:
        return render(request, "errore.html", {"messaggio": "Credito insufficiente"})
    if articolo.num_articoli <= 0:
        return render(request, "errore.html", {"messaggio": "Articolo non disponibile"})

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
    if articolo in acquirente.carrello.articoli.all():
        acquirente.carrello.articoli.remove(articolo)
    return ordini_view(request)


@permission_required('shop.puo_visualizzare_ordini')
def ordini_view(request):
    acquirente = Acquirente.objects.get(user=request.user)
    ordini = Ordine.objects.filter(acquirente=acquirente).all()
    return render(request, "ordini.html", {'ordini': ordini})


@permission_required('shop.puo_valutare')
def valutazione_view(request, ordine_id):
    if request.method == "POST":
        ordine = Ordine.objects.get(id=ordine_id)
        voto = request.POST.get("stelle")
        commento = request.POST.get("commento")
        try:
            ordine.valutazione.voto = voto
            ordine.valutazione.commento = commento
            ordine.valutazione.save()
        except ObjectDoesNotExist:
            Valutazione.objects.create(ordine=ordine, voto=voto, commento=commento)
        return ordini_view(request)
    else:
        acquirente = Acquirente.objects.get(user=request.user)
        if Ordine.objects.filter(acquirente=acquirente).filter(id=ordine_id).count() == 0:
            return render(request, "errore.html", {'messaggio': "Non ha questo ordine"})
        else:
            return render(request, "valutazione.html", {'ordine_id': ordine_id})


@permission_required('shop.puo_aggiungere_carrello', raise_exception=True)
def aggiungi_carrello_view(request, articolo_id):
    acquirente = Acquirente.objects.get(user=request.user)
    articolo = Articolo.objects.get(id=articolo_id)
    carrello = Carrello.objects.filter(acquirente=acquirente).first()
    carrello.articoli.add(articolo)
    return carrello_view(request)


@permission_required('shop.puo_visualizzare_carrello')
def carrello_view(request):
    acquirente = Acquirente.objects.filter(user=request.user).first()
    carrello = Carrello.objects.filter(acquirente=acquirente).first()
    if carrello:
        articoli = carrello.articoli.all()
        valutazioni = [valutazione_media_articolo(articolo.id) for articolo in articoli]
        lista = [{"articolo": articolo, "media": valutazione[0], "len": valutazione[1]} for articolo, valutazione in
                 zip(articoli, valutazioni)]
    else:
        lista = []
    return render(request, "carrello.html", {'lista': lista})


@permission_required("shop.puo_eliminare_carrello_articolo")
def elimina_carrello_articolo_view(request, articolo_id):
    articolo = Articolo.objects.get(id=articolo_id)
    if articolo not in request.user.acquirente.carrello.articoli.all():
        return render(request, "errore.html", {"messaggio": "questo articolo non è presente nel tuo carrello."})
    request.user.acquirente.carrello.articoli.remove(articolo)
    return redirect("carrello")


# Venditore
@permission_required('shop.puo_aggiungere_articolo')
def aggiungi_articolo_view(request):
    if request.method == "POST":
        form = ArticoloForm(request.POST)
        i_form = ImmagineForm(request.POST, request.FILES)
        if form.is_valid() and i_form.is_valid():
            articolo = form.save(commit=False)
            articolo.venditore = request.user.venditore
            articolo.save()
            immagine_profilo = i_form.save(commit=False)
            immagine_profilo.articolo = articolo
            immagine_profilo.save()
            articolo.profilo = immagine_profilo
            articolo.save(update_fields=["profilo"])
            immagini = request.FILES.getlist("immagini")
            for immagine in immagini:
                try:
                    img = Image.open(immagine)
                    img.verify()
                    img = Immagine(articolo=articolo, immagine=immagine)
                    img.save()
                except Exception:
                    immagini.remove(immagine)
            return redirect("home_page")
    else:
        form = ArticoloForm()
        form.fields.pop("profilo", None)
        i_form = ImmagineForm()
        i_form.fields["immagine"].label = "Immagine profilo"
    return render(request, "aggiungi_articolo.html", {"form": form, "i_form": i_form})


@permission_required('shop.puo_visualizzare_articoli_venditore')
def miei_articoli_view(request):
    if request.method == 'GET':
        articoli = Articolo.objects.filter(venditore=request.user.venditore).filter(visualizzabile=True).all()
        num_comparse = Counter(articoli)
        num_comparse = sorted(num_comparse.items(), key=lambda x: x[1], reverse=True)
        articoli = [c[0] for c in num_comparse]
        valutazione = valutazione_media_venditore(request.user.venditore.id)
        return render(request, 'miei_articoli.html',
                      {'articoli': articoli, 'valutazione_media': valutazione[0], 'num_voti': valutazione[1]})
    return render(request, 'errore.html')


@permission_required('shop.puo_modificare_articolo')
def modifica_articolo_view(request, articolo_id):
    articolo = Articolo.objects.get(id=articolo_id)
    if request.method == "POST":
        form = ArticoloForm(request.POST, instance=articolo)
        if form.is_valid():
            form.save()
            return redirect("articolo", articolo_id)
    else:
        if articolo.venditore == request.user.venditore:
            form = ArticoloForm(instance=articolo)
            form.fields["profilo"].queryset = Immagine.objects.filter(articolo=articolo).all()
            return render(request, "modifica_articolo.html", {"form": form, "articolo_id": articolo_id})
        else:
            return redirect("errore.html",
                            {"messaggio": "non puoi modificare i dati di un articolo di cui non sei venditore"})
    return render(request, "errore.html")


@permission_required("shop.puo_eliminare_articolo")
def elimina_articolo_view(request, articolo_id):
    articolo = Articolo.objects.get(id=articolo_id)
    if articolo.venditore != request.user.venditore:
        return render(request, "errore.html", {"messaggio": "non sei il venditore di questo articolo."})
    articolo.visualizzabile = False
    articolo.save()
    return redirect("miei_articoli")


@permission_required("shop.puo_modificare_articolo")
def modifica_immagini_view(request, articolo_id):
    articolo = Articolo.objects.get(id=articolo_id)

    if articolo.venditore != request.user.venditore:
        return render(request, "errore.html", {"messaggio": "Non sei il venditore dell’articolo."})

    immagini = Immagine.objects.filter(articolo=articolo).exclude(id=articolo.profilo.id).all()
    return render(request, "modifica_immagini.html", {"articolo": articolo, "immagini": immagini})


@permission_required("shop.puo_modificare_articolo")
def carica_immagini_view(request, articolo_id):
    articolo = Articolo.objects.get(id=articolo_id)
    if articolo.venditore != request.user.venditore:
        return render(request, "errore.html",
                      {"messaggio": "Non puoi caricare immagini ad articolo di cui non sei il venditore"})
    if request.method == "POST":
        immagini = request.FILES.getlist("immagini")
        for immagine in immagini:
            try:
                img = Image.open(immagine)
                img.verify()
                img = Immagine(articolo=articolo, immagine=immagine)
                img.save()
            except Exception:
                immagini.remove(immagine)
        return redirect("modifica_immagini", articolo_id=articolo_id)
    return render(request, "modifica_immagini.html")


@permission_required("shop.puo_modificare_articolo")
def elimina_immagine_view(request, articolo_id):
    articolo = Articolo.objects.get(id=articolo_id)
    if articolo.venditore != request.user.venditore:
        return render(request, "errore.html", {"messaggio": "non sei il venditore di questo articolo."})
    immagine_id = request.POST.get("elimina_id")
    immagine = Immagine.objects.get(id=immagine_id)
    immagine.delete()
    return redirect("modifica_immagini", articolo_id=articolo_id)
