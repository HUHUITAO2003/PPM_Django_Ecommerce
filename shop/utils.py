from shop.models import Valutazione


def valutazione_media(articolo_id):
    valutazione = Valutazione.objects.filter(ordine__articolo_id=articolo_id)
    tot = 0
    if valutazione.count() == 0:
        return 0.0, 0
    else:
        for v in valutazione:
            tot += v.voto
        return float(f"{tot/valutazione.count():.2g}"), valutazione.count()

