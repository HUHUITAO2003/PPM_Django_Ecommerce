from django.contrib.auth.decorators import login_required
from django.urls import path

from shop.views import ordini_view, aggiungi_carrello_view, ricerca_view, articolo_view, acquista_view, \
    valutazione_view, carrello_view, aggiungi_articolo_view, miei_articoli_view, modifica_articolo_view, \
    modifica_immagini_view, carica_immagini_view, elimina_immagine_view, elimina_articolo_view, \
    elimina_carrello_articolo_view

urlpatterns = [
    path("ricerca/", ricerca_view, name="ricerca"),
    path("articolo/<int:articolo_id>/", articolo_view, name="articolo"),

    # Acquirente
    path("acquista/<int:articolo_id>/", login_required(acquista_view, login_url="/autenticazione/accedi/"),
         name="acquista"),
    path("ordini", login_required(ordini_view, login_url="/autenticazione/accedi/"), name="ordini"),
    path("valutazione/<int:ordine_id>/", login_required(valutazione_view, login_url="/autenticazione/accedi/"),
         name="valutazione"),
    path("aggiungi_carrello/<int:articolo_id>/",
         login_required(aggiungi_carrello_view, login_url="/autenticazione/accedi/"), name="aggiungi_carrello"),
    path("elimina_carrello_articolo/<int:articolo_id>",
         login_required(elimina_carrello_articolo_view, login_url="/autenticazione/accedi/"),
         name="elimina_carrello_articolo"),
    path("carrello/", login_required(carrello_view, login_url="/autenticazione/accedi/"), name="carrello"),

    # Venditore
    path("aggiungi_articolo/", login_required(aggiungi_articolo_view, login_url="/autenticazione/accedi/"),
         name="aggiungi_articolo"),
    path("miei_articoli", login_required(miei_articoli_view, login_url="/autenticazione/accedi/"),
         name="miei_articoli"),
    path("modifica_articolo/<int:articolo_id>",
         login_required(modifica_articolo_view, login_url="/autenticazione/accedi/"),
         name="modifica_articolo"),
    path("elimina_articolo/<int:articolo_id>",
         login_required(elimina_articolo_view, login_url="/autenticazione/accedi/"),
         name="elimina_articolo"),
    path("modifica_immagini/<int:articolo_id>",
         login_required(modifica_immagini_view, login_url="/autenticazione/accedi/"),
         name="modifica_immagini"),
    path("carica_immagini/<int:articolo_id>",
         login_required(carica_immagini_view, login_url="/autenticazione/accedi/"),
         name="carica_immagini"),
    path("elimina_immagine/<int:articolo_id>",
         login_required(elimina_immagine_view, login_url="/autenticazione/accedi/"),
         name="elimina_immagine"),
]
