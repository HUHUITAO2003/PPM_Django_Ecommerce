from shop.models import Valutazione


def valutazione_media_articolo(articolo_id):
    valutazione = Valutazione.objects.filter(ordine__articolo_id=articolo_id)
    tot = 0
    if valutazione.count() == 0:
        return 0.0, 0
    else:
        for v in valutazione:
            tot += v.voto
        return float(f"{tot / valutazione.count():.2g}"), valutazione.count()


def valutazione_media_venditore(venditore_id):
    valutazione = Valutazione.objects.filter(
        ordine__articolo__venditore_id=venditore_id,
        ordine__articolo__visualizzabile=True
    )
    tot = 0
    if valutazione.count() == 0:
        return 0.0, 0
    else:
        for v in valutazione:
            tot += v.voto
        return float(f"{tot / valutazione.count():.2g}"), valutazione.count()
