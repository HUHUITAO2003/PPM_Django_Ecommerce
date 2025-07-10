from django.urls import path

from .views import aggiungi_carrello_view

urlpatterns = [
    path("aggiungi_carrello/<int:articolo_id>/", aggiungi_carrello_view, name="aggiungi_carrello"),
]
