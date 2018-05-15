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
    lista_museos = Museo.objects.all()
    #Museo.objects.all().delete() # Borro base datos

    if len(lista_museos) == 0:  # SIN MUSEOS
        if request.method == "GET":
            titulo = "Sin museos en la base de datos"
            cargar = "<form method = 'POST'><button type='submit'"
            cargar += "name='cargar' value=True>Cargar datos de museos"
            cargar += "</button><br>"
            c = RequestContext(request, {'titulo':titulo, 'cargar': cargar})
        elif request.method == 'POST':
            link_parse() # Cargo la info de museos en mi base de datos
            print ("Asignando los atributos de models Museo...")
            return HttpResponseRedirect('/')
    
    else:   # CON MUSEOS
      
        if request.method == "GET":
            titulo = "Museos con más comentarios"
            filtrar = "<form method = 'POST'><button type='submit'"
            filtrar += "name='accesible' value=1>Mostrar sólo museos "
            filtrar += "accesibles</button><br>"

        elif request.method == "POST":
            accesible = request.body.decode('utf-8').split("=")[1]
            if int(accesible) == 1:
                titulo = "Museos accesibles"
                lista_museos = lista_museos.filter(accesibilidad=True)
                filtrar = "<form method = 'POST'><button type='submit'"
                filtrar += "name='accesible' value=0>Mostrar museos con "
                filtrar += "más comentarios</button><br>"
            else:
                titulo = "Museos con más comentarios"
                filtrar = "<form method = 'POST'><button type='submit'"
                filtrar += "name='accesible' value=1>Mostrar sólo museos "
                filtrar += "accesibles</button><br>"

        lista_museos = lista_museos.exclude(num_comentarios=0)  # excluyo sin comentarios
        lista_museos = lista_museos.order_by('-num_comentarios')  # ordeno de mayor a menor
        lista_museos = lista_museos[0:5]  # los 5 primeros
        
        c = RequestContext(request, {'titulo':titulo, 'filtrar': filtrar, 'museos': lista_museos})

    respuesta = template.render(c)
    return HttpResponse(respuesta)

def todos(request):
    template = get_template ('miplantilla/todos.html')
    titulo = "Todos los museos"
    lista_museos = Museo.objects.all()

    c = RequestContext(request, {'titulo':titulo, 'museos': lista_museos}) 
    
    respuesta = template.render(c)
    return HttpResponse(respuesta)

def about(request):

    pass


def login_exito (request):
    respuesta = "Ha entrado como <b>" + request.user.username
    respuesta += "</b> exitosamente."
    return HttpResponse(respuesta)

