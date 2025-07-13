from django.urls import path

from shop.views import ordini_view, aggiungi_carrello_view, ricerca_view, articolo_view, acquista_view, errore_view, \
    valutazione_view, valuta_view, carrello_view, aggiungi_articolo_view

urlpatterns = [
    path("acquista/<int:articolo_id>/", acquista_view, name="acquista"),
    path("ordini", ordini_view, name="ordini"),
    path("aggiungi_carrello/<int:articolo_id>/", aggiungi_carrello_view, name="aggiungi_carrello"),
    path("ricerca/", ricerca_view, name="ricerca"),
    path("articolo/<int:articolo_id>/", articolo_view, name="articolo"),
    path("valutazione/<int:ordine_id>/", valutazione_view, name="valutazione"),
    path("valuta/<int:ordine_id>/", valuta_view, name="valuta"),
    path("errore/", errore_view, name="errore"),
    path("carrello/", carrello_view, name="carrello"),
    path("aggiungi_articolo/", aggiungi_articolo_view, name="aggiungi_articolo"),
]
