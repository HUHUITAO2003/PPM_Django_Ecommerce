from django.urls import path

from shop.views import acquisto_view

urlpatterns = [
    path("acquisto/<int:articolo_id>/", acquisto_view, name="acquisto"),
]
