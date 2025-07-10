from django.urls import path
from .views import errore_view, ricerca_view, articolo_view

urlpatterns = [
    path("ricerca/", ricerca_view, name="ricerca"),
    path("articolo/<int:articolo_id>/", articolo_view, name="articolo"),

]
