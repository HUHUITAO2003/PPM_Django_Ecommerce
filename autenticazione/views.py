from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from autenticazione.forms import CustomUserCreationForm
from utenti.models import Portafoglio, Acquirente, Venditore


def accedi_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect('home_page')
        else:
            return render(request, 'errore.html', {'messaggio': "form invalido"})
    else:
        form = AuthenticationForm()
    return render(request, 'accedi.html', {'form': form})


def registrazione_view(request):
    if request.method == "GET":
        ruolo = request.GET.get('ruolo')
        if ruolo == 'acquirente':
            return registrazione_acquirente_view(request)
        elif ruolo == 'venditore':
            return registrazione_venditore_view(request)
    return render(request, 'scelta_registrazione.html')


def registrazione_acquirente_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            indirizzo = request.POST['indirizzo']
            acquirente = Acquirente.objects.create(user=user, indirizzo=indirizzo)
            Portafoglio.objects.create(acquirente=acquirente, credito=0)

            group = Group.objects.get(name='Acquirenti')
            user.groups.add(group)
            return redirect('accedi')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registrati_acquirente.html', {'form': form})


def registrazione_venditore_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            denominazione = request.POST['denominazione']
            Venditore.objects.create(user=user, denominazione=denominazione)

            group = Group.objects.get(name='Venditori')
            user.groups.add(group)
            return redirect('accedi')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registrati_venditore.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home_page')