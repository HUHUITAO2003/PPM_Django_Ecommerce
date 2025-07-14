from django.shortcuts import render

def home_page_view(request):
    return render(request, "index.html")

def errore_view(request, messaggio):
    return render(request, 'errore.html', {'messaggio': messaggio})

def custom_403_view(request, exception=None):
    return render(request, 'errore.html', {'messaggio': "non hai permessi per eseguire l'operazione"})