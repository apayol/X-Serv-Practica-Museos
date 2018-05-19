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
        dist_elegido = request.body.decode('utf-8').split("=")[1].replace("+", " ")
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
    
    #INTERFAZ PRIVADA
    form = '' #Sin formulario si no authenticated
    form2 = ''
    textoseleccion = ''
    if request.user.is_authenticated():
        #nuevo comentario si logged
        form = "<form action='/museos/" + str(id) + "' method='POST'>"
        form += "<input type= 'text' name='texto' size='80'>"
        form += "<input type= 'hidden' name='formulario' value='1'> "
        form += "<input type= 'submit' value='Enviar'>"
        form += "</form>"      
        
        select = ConfigUsuario.objects.get(usuario=request.user)
        if request.method == "GET":
            try: #Si ya está seleccionado
                Seleccionado.objects.get(usuario=select, museo=museo_elegido)
                textoseleccion = "PERTENECE A TU SELECCIÓN"
		          #borrar de mi selección de museos
                form2 = "<form action='/museos/" + str(id) + "' method='POST'>"
                form2 += "<input type= 'submit' value='Deseleccionar museo'>"
                form2 += "<input type= 'hidden' name='formulario' value='3'> "
                form2 += "</form>"
            
            except Seleccionado.DoesNotExist: #Si no está seleccionado
                textoseleccion = "¿AÑADIR A SELECCIONADOS?"
                #añadir a mi selección de museos
                form2 = "<form action='/museos/" + str(id) + "' method='POST'>"
                form2 += "<input type= 'submit' value='Seleccionar museo'>"
                form2 += "<input type= 'hidden' name='formulario' value='2'> "
                form2 += "</form>"
                    
        elif request.method == "POST":
            formu = request.POST['formulario']
            if formu == "1": # Si envío comentario
                # Guardo en mi base de datos el comentario
                texto = request.POST['texto']
                nuevo_coment = Comentario(texto=texto, museo=museo_elegido)
                nuevo_coment.save()
                #Actualizo el numero de comentarios
                museo_elegido.num_comentarios = museo_elegido.num_comentarios + 1
                museo_elegido.save()
                try: #Si ya está seleccionado
                    Seleccionado.objects.get(usuario=select, museo=museo_elegido)
                    textoseleccion = "PERTENECE A TU SELECCIÓN"
		              #borrar de mi selección de museos
                    form2 = "<form action='/museos/" + str(id) + "' method='POST'>"
                    form2 += "<input type= 'submit' value='Deseleccionar museo'>"
                    form2 += "<input type= 'hidden' name='formulario' value='3'> "
                    form2 += "</form>"
                except Seleccionado.DoesNotExist: #Si no está seleccionado
                    textoseleccion = "¿AÑADIR A SELECCIONADOS?"
                    #añadir a mi selección de museos
                    form2 = "<form action='/museos/" + str(id) + "' method='POST'>"
                    form2 += "<input type= 'submit' value='Seleccionar museo'>"
                    form2 += "<input type= 'hidden' name='formulario' value='2'> "
                    form2 += "</form>"
            elif formu == "2": # Si añado a selección
                # Guardo en mi base de datos la selección
                nueva_seleccion = Seleccionado(usuario=select, museo=museo_elegido)
                nueva_seleccion.save() 
                print("se ha añadido")
                textoseleccion = "PERTENECE A TU SELECCIÓN"
                form2 = "<form action='/museos/" + str(id) + "' method='POST'>"
                form2 += "<input type= 'submit' value='Deseleccionar museo'>"
                form2 += "<input type= 'hidden' name='formulario' value='3'> "
                form2 += "</form>"
            elif formu == "3": # Si borro de selección
                # Guardo en mi base de datos la deselección
                nueva_seleccion = Seleccionado.objects.get(usuario=select, museo=museo_elegido)
                nueva_seleccion.delete() 
                print("se ha borrado")
                textoseleccion = "¿AÑADIR A SELECCIONADOS?"
                form2 = "<form action='/museos/" + str(id) + "' method='POST'>"
                form2 += "<input type= 'submit' value='Seleccionar museo'>"
                form2 += "<input type= 'hidden' name='formulario' value='2'> "
                form2 += "</form>"             

    c = RequestContext(request, {'titulo':titulo, 'museo': museo_elegido,
		 'accesible': accesible, 'comentarios': coments_museo, 'form': form,
       'form2': form2, 'textoseleccion': textoseleccion}) 
    
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
    
    pagina = ''
    if request.method == "GET":
        try:
            pagina_usuario = ConfigUsuario.objects.get(usuario=user)
            titulo = pagina_usuario.titulo

            lista_museos = Seleccionado.objects.all() #todas las elecciones.
            lista_museos_usuario = Seleccionado.objects.filter(usuario=pagina_usuario)
            pagina = "0"
            print(lista_museos)
           
				#INTERFAZ PRIVADA
            if request.user.is_authenticated():
            #   contenido = "¿Desea cambiar algo en su configuración?"
            #   Form1:titulo, Form2:colorfondo,tamañoletra
                print("Permisos de usuario")

        # si el recurso es incorrecto (nombre de usuario no registrado) 
        except ConfigUsuario.DoesNotExist: 
            titulo = "Esa página no existe"
            lista_museos = ""
            pagina = ""

    c = RequestContext(request, {'titulo': titulo, 'seleccionados': lista_museos_usuario, 'pagina': pagina}) 

    respuesta = template.render(c)
    return HttpResponse(respuesta)

