from django.urls import path

from accounts.views import accedi_view, registrati_view, accesso_view, scelta_registrazione_view, \
    registrazione_acquirente_view

urlpatterns = [
    path("accedi", accedi_view, name="accedi"),
    path("accesso", accesso_view, name="accesso"),
    path("registrati", registrati_view, name="registrati"),
    path("scelta_registrazione", scelta_registrazione_view, name="scelta_registrazione"),
    path("registrazione_acquirente", registrazione_acquirente_view, name="registrazione_acquirente"),
]
