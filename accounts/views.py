from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
def accedi_view(request):
    return render(request, 'accedi.html')

def accesso_view(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return redirect("home_page")
    else:
        return render(request, 'errore.html')

def scelta_registrazione_view(request):
    return render(request, 'scelta_registrazione.html')

def registrati_view(request):
    ruolo = request.GET.get('ruolo')
    if ruolo == 'acquirente':
        return render(request, 'registrati_acquirente.html')
    elif ruolo == 'venditore':
        return render(request, 'registrati_venditore.html')
    else:
        return render(request, 'errore.html')
