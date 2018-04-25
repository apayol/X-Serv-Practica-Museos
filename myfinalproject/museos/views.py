from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def barra(request):
    respuesta = "Esta es la página principal"
    # Aquí aparecerán los 5 museos con más comentarios

    return HttpResponse(respuesta)
