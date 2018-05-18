from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, RequestContext
from .models import Museo, Comentario, ConfigUsuario, Seleccionado
from .parser import link_parse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


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
        
        # Para la barra de usuarios lateral
        lista_usuarios = ConfigUsuario.objects.all()

        c = RequestContext(request, {'titulo':titulo, 'filtrar': filtrar, 'museos': lista_museos,
                'usuarios': lista_usuarios})

    respuesta = template.render(c)
    return HttpResponse(respuesta)

@csrf_exempt
def todos(request):
    template = get_template ('miplantilla/todos.html')
    titulo = "Todos los museos"
    dist_elegido= ""
    if request.method == 'GET':
        lista_museos = Museo.objects.all()
        
        # opciones del desplegable
        lista_distritos = Museo.objects.order_by()  # distritos por orden
        lista_distritos = lista_distritos.values_list('distrito', flat=True).distinct()
        # formulario con elementos de base de datos
        filtrar = "<form action='/museos' method='POST'>"
        filtrar += "<select name='dist_elegido'>"
        for distr in lista_distritos:
            filtrar += "<option value='" + distr + "'>" + distr
            filtrar += "</option>"
        filtrar += "<input type= 'submit' value='Filtrar'>"
        filtrar += "</form>"


    elif request.method == "POST":
        dist_elegido = request.body.decode('utf-8').split("=")[1]
        titulo += " del distrito " + dist_elegido
        lista_museos = ""
        lista_distritos = Museo.objects.filter(distrito=dist_elegido)
        lista_museos = lista_distritos
        
        # opciones del desplegable
        lista_distritos = Museo.objects.order_by()
        lista_distritos = lista_distritos.values_list('distrito', flat=True).distinct()
        # formulario de elementos de base de datos
        filtrar = "<form action='/museos' method='POST'>"
        filtrar += "<select name='dist_elegido'>"
        for distr in lista_distritos:
            filtrar += "<option value='" + distr + "'>" + distr
            filtrar += "</option>"
        filtrar += "<input type= 'submit' value='Filtrar'>"
        filtrar += "</form>"
        #formulario para ver todos
        filtrar += "<form action='/museos' method='GET'>"
        filtrar += "<input type= 'submit' value='Volver a "
        filtrar += "mostrar TODOS los museos'></form>" 

    c = RequestContext(request, {'titulo':titulo, 'filtrar':filtrar, 'museos': lista_museos}) 
    
    respuesta = template.render(c)
    return HttpResponse(respuesta)

@csrf_exempt
def museo(request, id):
    template = get_template ('miplantilla/museo.html')
    museo_elegido = Museo.objects.get(id=id)
    titulo = museo_elegido
    #accesibilidad
    accesible = museo_elegido.accesibilidad
    if accesible == True:
        accesible = "Sí"
    else:
        accesible = "No"
    #comentarios
    lista_coments = Comentario.objects.all()
    coments_museo = lista_coments.filter(museo=museo_elegido)
    
    form = '' #Sin formulario si no authenticated
    if request.user.is_authenticated():
            #nuevo comentario si logged
            form = "<form action='/museos/" + str(id) + "' method='POST'>"
            form += "<input type= 'text' name='texto' size='80'>"
            form += "<input type= 'hidden' name='formulario' value='1'> "
            form += "<input type= 'submit' value='Enviar'>"
            form += "</form>"
    
            #añadir a mi selección de museos
    

    if request.method == "POST":
        nuevo_com = request.POST['formulario']
        if nuevo_com == "1":
            # Guardo en mi base de datos
            texto = request.POST['texto']
            nuevo_coment = Comentario(texto=texto, museo=museo_elegido)
            nuevo_coment.save()
            #Actualizo el numero de comentarios
            museo_elegido.num_comentarios = museo_elegido.num_comentarios + 1
            museo_elegido.save()
    
    
    c = RequestContext(request, {'titulo':titulo, 'museo': museo_elegido,
		 'accesible': accesible, 'comentarios': coments_museo, 'form': form}) 
    
    respuesta = template.render(c)
    return HttpResponse(respuesta)


def about(request):
    #Directamente en el html
    pass

@csrf_exempt
def login_form(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print("Autenticado como: " + str(user))
        # user devuelve None si no está autenticado
        if user is not None:
            if user.is_active:
                login(request, user)
                try: 
                    registrado = ConfigUsuario.objects.get(usuario=username)
                except ConfigUsuario.DoesNotExist: 
                    registrado = ConfigUsuario(usuario=username)
                    registrado.titulo = "Página de " + str(user) #inicializo el título
                    registrado.save() #lo guardo en mi models
                    print(registrado)

    return HttpResponseRedirect('/')


@csrf_exempt
def logout_form(request):
    if request.method == "POST":
        logout(request)
    return HttpResponseRedirect('/')


def usuario(request,user):
    template = get_template ('miplantilla/usuario.html')

    if request.method == "GET":
        try:
            pagina_usuario = ConfigUsuario.objects.get(usuario=user)
            titulo = pagina_usuario.titulo
                              
            contenido = "Museos favoritos de 5 en 5"            

            #if user.is_authenticated:
            #   contenido = "¿Desea cambiar algo en su configuración?"
            #   Form1:titulo, Form2:colorfondo,tamañoletra



        # si el recurso es incorrecto (nombre de usuario no registrado) 
        except ConfigUsuario.DoesNotExist: 
            titulo = "Esa página no existe."
            contenido = ""

    c = RequestContext(request, {'titulo': titulo, 'contenido': contenido}) 
    respuesta = template.render(c)
    return HttpResponse(respuesta)

