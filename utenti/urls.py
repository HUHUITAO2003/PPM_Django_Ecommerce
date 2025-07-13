from django.urls import path

from utenti.views import profilo_view, aggiungi_credito_view, modifica_profilo_acquirente_view

urlpatterns = [
    path("", profilo_view, name="profilo"),
    path("modifica_profilo_acquirente", modifica_profilo_acquirente_view, name="modifica_profilo_acquirente"),
    path("aggiungi_credito", aggiungi_credito_view, name="aggiungi_credito"),
]
