from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from .models import Museo
from .parser import link_parse


def inicio(request):
    respuesta = "Esta es la página principal"

    # SOLO CON BOTÓN "ACTUALIZAR"
    Museo.objects.all().delete() # Borro antigua base datos
    print ("Asignando los atributos de models Museo...")
    #link_parse() # Cargo la info de museos en mi base de datos
    
    c = Context({})
    template = get_template ('miplantilla/inicio.html')
    respuesta = template.render(c)

    # Aquí aparecerán los 5 museos con más comentarios

    return HttpResponse(respuesta)

def todos(request):
    respuesta = "Se muestra un resumen de todos los museos de Madrid"

    c = Context({})
    template = get_template ('miplantilla/todos.html')
    respuesta = template.render(c)
    # Aquí aparecerán TODOS los museos

    return HttpResponse(respuesta)

def about(request):

    pass


def login_exito (request):
    respuesta = "Ha entrado como <b>" + request.user.username
    respuesta += "</b> exitosamente."
    return HttpResponse(respuesta)

