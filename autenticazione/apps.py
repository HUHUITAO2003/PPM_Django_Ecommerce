from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class AutenticazioneConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'autenticazione'



@receiver(post_migrate)
def crea_gruppi(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission

    venditori, _ = Group.objects.get_or_create(name='Venditori')
    acquirenti, _ = Group.objects.get_or_create(name='Acquirenti')
    try:
        # Permessi per il gruppo acquirenti
        permessi_acquirenti = [
            "puo_visualizzare_ordini",
            "puo_valutare",
            "puo_acquistare_articolo",
            "puo_modificare_articolo",
            "puo_aggiungere_carrello",
            "puo_visualizzare_carrello",
            "puo_aggiungere_credito",
            "puo_visualizzare_profilo_acquirente",
            "puo_modificare_profilo_acquirente",
        ]

        for codename in permessi_acquirenti:
            permesso = Permission.objects.get(codename=codename)
            acquirenti.permissions.add(permesso)

        # Permessi per il gruppo venditori
        permessi_venditori = [
            "puo_visualizzare_profilo_venditore",
            "puo_modificare_profilo_venditore",
            "puo_aggiungere_articolo",
        ]

        for codename in permessi_venditori:
            permesso = Permission.objects.get(codename=codename)
            venditori.permissions.add(permesso)

    except Permission.DoesNotExist:
        pass  # oppure logga un messaggio
