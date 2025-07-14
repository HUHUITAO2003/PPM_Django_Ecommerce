from django.contrib.auth.decorators import login_required
from django.urls import path

from utenti.views import profilo_view, aggiungi_credito_view, modifica_profilo_acquirente_view, \
    modifica_profilo_venditore_view

urlpatterns = [
    path("", login_required(profilo_view, login_url="/autenticazione/accedi/"), name="profilo"),
    path("modifica_profilo_acquirente",
         login_required(modifica_profilo_acquirente_view, login_url="/autenticazione/accedi/"),
         name="modifica_profilo_acquirente"),
    path("aggiungi_credito", login_required(aggiungi_credito_view, login_url="/autenticazione/accedi/"),
         name="aggiungi_credito"),
    path("modifica_profilo_venditore",
         login_required(modifica_profilo_venditore_view, login_url="/autenticazione/accedi/"),
         name="modifica_profilo_venditore"),
]
