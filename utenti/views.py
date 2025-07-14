from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render

from autenticazione.forms import CustomUserChangeForm
from utenti.forms import AcquirenteForm, PortafoglioForm, VenditoreForm


def profilo_view(request):
    if request.user.has_perm("utenti.puo_visualizzare_profilo_acquirente"):
        user = request.user
        user_form = CustomUserChangeForm(instance=user)
        acquirente_form = AcquirenteForm(instance=user.acquirente)
        portafoglio_form = PortafoglioForm(instance=user.acquirente.portafoglio)
        for field in user_form.fields:
            user_form.fields[field].disabled = True
        for field in acquirente_form.fields:
            acquirente_form.fields[field].disabled = True
        portafoglio_form.fields["credito"].disabled = True
        return render(request, "profilo.html",
                      {"forms": [user_form, acquirente_form, portafoglio_form]})
    elif request.user.has_perm("utenti.puo_visualizzare_profilo_venditore"):
        user = request.user
        user_form = CustomUserChangeForm(instance=user)
        venditore_form = VenditoreForm(instance=user.venditore)
        for field in user_form.fields:
            user_form.fields[field].disabled = True
        for field in venditore_form.fields:
            venditore_form.fields[field].disabled = True
        return render(request, "profilo.html",
                      {"forms": [user_form, venditore_form]})
    else:
        return render(request, "errore.html", {"messaggio": "non hai eseguito il login, non abbiamo il tuo profilo."})


@permission_required("utenti.puo_modificare_profilo_acquirente")
def modifica_profilo_acquirente_view(request):
    if request.method == "POST":
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        acquirente_form = AcquirenteForm(request.POST, instance=request.user.acquirente)
        if acquirente_form.is_valid() and user_form.is_valid():
            user_form.save()
            acquirente_form.save()
            portafoglio_form = PortafoglioForm(instance=request.user.acquirente.portafoglio)
            portafoglio_form.fields["credito"].disabled = True
            return profilo_view(request)
        else:
            return render(request, "errore.html")
    else:
        user = request.user
        user_form = CustomUserChangeForm(instance=user)
        acquirente_form = AcquirenteForm(instance=user.acquirente)
        portafoglio_form = PortafoglioForm(instance=user.acquirente.portafoglio)
        portafoglio_form.fields["credito"].disabled = True
        return render(request, "modifica_profilo_acquirente.html",
                      {"user_form": user_form, "acquirente_form": acquirente_form,
                       "portafoglio_form": portafoglio_form})


@permission_required('utenti.puo_aggiungere_credito')
def aggiungi_credito_view(request):
    codice_credito = {"4a44dc15364204a80fe80e9039455cc1608281820fe2b24f1e5233ade6af1dd5": 10,
                      "f5ca38f748a1d6eaf726b8a42fb575c3c71f1864a8143301782de13da2d9202b": 20,
                      "1a6562590ef19d1045d06c4055742d38288e9e6dcd71ccde5cee80f1d5a774eb": 50,
                      "ad57366865126e55649ecb23ae1d48887544976efea46a48eb5d85a6eeb4d306": 100,
                      "27badc983df1780b60c2b3fa9d3a19a00e46aac798451f0febdca52920faaddf": 200,
                      "0604cd3138feed202ef293e062da2f4720f77a05d25ee036a7a01c9cfcdd1f0a": 500}
    if request.method == "POST":
        codice_carta = request.POST['codice_carta']
        stato_ricarica = "fallito"
        for codice in codice_credito.keys():
            if codice == codice_carta:
                request.user.acquirente.portafoglio.credito += codice_credito[codice]
                request.user.acquirente.portafoglio.save()
                stato_ricarica = "successo"
        return render(request, "aggiungi_credito.html", {"stato_ricarica": stato_ricarica})
    else:
        return render(request, "aggiungi_credito.html")


@permission_required("utenti.puo_modificare_profilo_venditore")
def modifica_profilo_venditore_view(request):
    if request.method == "POST":
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        venditore_form = VenditoreForm(request.POST, instance=request.user.venditore)
        if venditore_form.is_valid() and user_form.is_valid():
            user_form.save()
            venditore_form.save()
            return profilo_view(request)
        else:
            print("\033[91mVenditoreForm errors:\033[0m", venditore_form.errors)
            print("\033[91mUserForm errors:\033[0m", user_form.errors)
            return render(request, "errore.html")
    else:
        user = request.user
        user_form = CustomUserChangeForm(instance=user)
        venditore_form = VenditoreForm(instance=user.venditore)
        return render(request, "modifica_profilo_venditore.html",
                      {"user_form": user_form, "venditore_form": venditore_form})