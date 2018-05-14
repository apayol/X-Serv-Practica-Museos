from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, RequestContext
from .models import Museo
from .parser import link_parse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def inicio(request):
    template = get_template ('miplantilla/inicio.html')
    museos = ""
    lista_museos = Museo.objects.all()
    #Museo.objects.all().delete() # Borro antigua base datos
    if len(lista_museos) == 0:
        if request.method == 'GET':
            cargar = "<form method = 'POST'><button type='submit'"
            cargar += "name='cargar' value=1>Cargar datos de museos"
            cargar += "</button><br>"
            c = RequestContext(request, {'cargar': cargar})
        elif request.method == 'POST':
            link_parse() # Cargo la info de museos en mi base de datos
            print ("Asignando los atributos de models Museo...")
            return HttpResponseRedirect('/')
    else:
        c = Context({})
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

