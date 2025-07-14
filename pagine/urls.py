from django.urls import path

from pagine.views import home_page_view, errore_view

urlpatterns = [
    path("", home_page_view, name="home_page"),
    path("errore/", errore_view, name="errore"),
]
