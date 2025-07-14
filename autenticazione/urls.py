from django.contrib.auth.decorators import login_required
from django.urls import path

from autenticazione.views import accedi_view, registrazione_acquirente_view, logout_view, registrazione_venditore_view, \
    registrazione_view

urlpatterns = [
    path("accedi/", accedi_view, name="accedi"),
    # path("accesso", accesso_view, name="accesso"),
    path("registrazione", registrazione_view, name="registrazione"),
    path("registrazione_acquirente", registrazione_acquirente_view, name="registrazione_acquirente"),
    path("registrazione_venditore", registrazione_venditore_view, name="registrazione_venditore"),
    path("logout", login_required(logout_view, login_url="/autenticazione/accedi/"), name="logout"),
]
