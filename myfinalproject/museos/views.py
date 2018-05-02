from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

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

# Parsear de este link el xml, guardarlo en mi base de datos
    link = 'https://datos.madrid.es/portal/site/egob/menuitem.c05'
    link += 'c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=118f2fdbec'
    link += 'c63410VgnVCM1000000b205a0aRCRD&vgnextchannel=374512'
    link += 'b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default'

