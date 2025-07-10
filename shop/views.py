from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def acquisto_view(request, articolo_id):
    return HttpResponse("Acquisto view")