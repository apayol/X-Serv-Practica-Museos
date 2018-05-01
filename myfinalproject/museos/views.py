from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def inicio(request):
    respuesta = "Esta es la página principal"
    # Aquí aparecerán los 5 museos con más comentarios

    return HttpResponse(respuesta)

def todos(request):
    respuesta = "Se muestra un resumen de todos los museos de Madrid"
    # Aquí aparecerán TODOS los museos

    return HttpResponse(respuesta)

def about(request):
    respuesta = "Aquí viene la info de mi práctica, autoría..."
    return HttpResponse(respuesta)

def login_exito (request):
    respuesta = "Ha entrado como <b>" + request.user.username
    respuesta += "</b> exitosamente."
    return HttpResponse(respuesta)
