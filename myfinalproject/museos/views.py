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
            formu = request.POST['accesible']
            if formu == "1":
                titulo = "Museos accesibles"
                lista_museos = lista_museos.filter(accesibilidad=True)
                filtrar = "<form method = 'POST'><button type='submit'"
                filtrar += "name='accesible' value=0>Mostrar museos con "
                filtrar += "más comentarios</button><br>"
            elif formu == "0":
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

@csrf_exempt
def usuario(request,user):
    template = get_template ('miplantilla/usuario.html')
    # Inicializo el id para hacer la qs y poder acceder por páginas
    id = request.GET.get('id')
    if id == None:
        id = 0
    else:
        id = int(id)
    
    try:
        pagina_usuario = ConfigUsuario.objects.get(usuario=user)
        titulo = pagina_usuario.titulo
        usuario = user
        total_museos_selec = Seleccionado.objects.filter(usuario=pagina_usuario).count()

        lista_museos = Seleccionado.objects.all() #todas las elecciones.
        #solo los seleccionados, de 5 en 5 por id.
        lista_museos_usuario = Seleccionado.objects.filter(usuario=pagina_usuario)[id:id+5]
        id += 5  # A siguiente página
         
        if id >= total_museos_selec and total_museos_selec < 5:
            id = -1 # Solo hay una página
        elif id >= total_museos_selec:
            id = 0  # Para volver al inicio
        
        # Botón para generar el canal XML de página usuario
        xml_usu_form = '<form method="GET" action="/'+usuario+'/xml">'
        xml_usu_form += '<button type="submit">Generar canal XML</button>'
        xml_usu_form += '</form>'

        # Botón para generar el canal JSON de página usuario
        json_usu_form = '<form method="GET" action="/'+usuario+'/json">'
        json_usu_form += '<button type="submit">Generar canal JSON</button>'
        json_usu_form += '</form>'
    
        form1 = ''
        form2 = ''
        # INTERFAZ PRIVADA: 
        # ha de estár autentificado y en su página
        if request.user.is_authenticated() and user == usuario:
            # Cambiar de título personal
            form1 = "<form action='/" + usuario + "'  method='POST'>"
            form1 += "<input type= 'text' name='nuevo_titulo' size='40'>"
            form1 += "<input type= 'hidden' name='formulario' value='1'> "
            form1 += "<input type= 'submit' value='Enviar'>"
            form1 += "</form>"
            # Cambiar estilo de CSS
            form2 = "<form action='/" + usuario + "'  method='POST'>"
            form2 += "Color de fondo: <input type= 'text' name='nuevo_color' size='10'>  "
            form2 += " Tamaño de letra (%): <input type= 'text' name='nueva_letra' size='10'>"
            form2 += "<input type= 'hidden' name='formulario' value='2'> "
            form2 += "<input type= 'submit' value='Enviar'>"
            form2 += "</form>" 
 
            if request.method == "POST":
                formu = request.POST['formulario']
                if formu == "1": # Si envío nuevo título
                    titulo = request.POST['nuevo_titulo']
                    # Actualizo el título
                    ConfigUsuario.objects.filter(usuario=request.user).update(titulo=titulo)
                elif formu == "2": # Si envío nuevo estilo
                    color = request.POST['nuevo_color']
                    letra = request.POST['nueva_letra']
                    # Actualizo el color de fondo
                    ConfigUsuario.objects.filter(usuario=request.user).update(color_fondo=color)
                    ConfigUsuario.objects.filter(usuario=request.user).update(tamaño_letra=letra)
    
    # si el recurso es incorrecto (nombre de usuario no registrado) 
    except ConfigUsuario.DoesNotExist: 
        titulo = "Error, url no existe"
        lista_museos_usuario = '' 
        usuario = ''
        form1 = ''
        form2 = ''
        id = ''
        xml_usu_form = ''
        json_usu_form = ''

    c = RequestContext(request, {'titulo': titulo, 'seleccionados': lista_museos_usuario, 
        'id': id, 'usuario': usuario, 'form1': form1, 'form2': form2, 'xml_usu_form': xml_usu_form,
        'json_usu_form': json_usu_form}) 

    respuesta = template.render(c)
    return HttpResponse(respuesta)

def xml_usuario(request, user):
    # Generar canal XML de la página de usuario.
    template = get_template('miplantilla/usuario_xml.xml')
    usuario = ConfigUsuario.objects.get(usuario=user)
    selecc_usuario = Seleccionado.objects.filter(usuario=usuario)  

    c = RequestContext(request, {'usuario': usuario, 'seleccionados': selecc_usuario})
    respuesta = template.render(c)
    return HttpResponse(respuesta, content_type="text/xml") #tipo xml

def json_usuario(request, user):
    # Generar canal JSON de la página de usuario.
    template = get_template('miplantilla/usuario_json.json')
    usuario = ConfigUsuario.objects.get(usuario=user)
    selecc_usuario = Seleccionado.objects.filter(usuario=usuario)  

    c = RequestContext(request, {'usuario': usuario, 'seleccionados': selecc_usuario})
    respuesta = template.render(c)
    return HttpResponse(respuesta, content_type="text/json") #tipo json

def xml_inicio(request):
    # Generar canal XML de la página de inicio.
    template = get_template('miplantilla/inicio_xml.xml')

    lista_museos = Museo.objects.all()
    lista_museos = lista_museos.exclude(num_comentarios=0)  # excluyo sin comentarios
    lista_museos = lista_museos.order_by('-num_comentarios')  # ordeno de mayor a menor
    lista_museos = lista_museos[0:5] 

    c = RequestContext(request, {'museos': lista_museos})
    respuesta = template.render(c)
    return HttpResponse(respuesta, content_type="text/xml") #tipo xml

def json_inicio(request):
    # Generar canal JSON de la página de inicio.
    template = get_template('miplantilla/inicio_json.json')

    lista_museos = Museo.objects.all()
    lista_museos = lista_museos.exclude(num_comentarios=0)  # excluyo sin comentarios
    lista_museos = lista_museos.order_by('-num_comentarios')  # ordeno de mayor a menor
    lista_museos = lista_museos[0:5] 

    c = RequestContext(request, {'museos': lista_museos})
    respuesta = template.render(c)
    return HttpResponse(respuesta, content_type="text/json") #tipo json

def rss_comentarios(request):
    #Generar rss con todos los comentarios. (Enlace desde inicio)
    template = get_template('miplantilla/rss_comentarios.rss')
    comentarios = Comentario.objects.all()

    c = RequestContext(request, {'comentarios': comentarios})
    respuesta = template.render(c)
    return HttpResponse(respuesta, content_type="text/rss")

@csrf_exempt
def registro(request):
    template = get_template('miplantilla/registro.html')
    if request.method == "GET":
        registro_form = "<form class='register' method='POST' action='/registro'>"
        registro_form += "<table><tr><td>Usuario:</td><td><input name='username'>"
        registro_form += "</td></tr><tr><td>Contraseña:</td><td>"
        registro_form += "<input name='password' type='password'></td></tr>"
        registro_form += "</table><input class='boton' type='submit' "
        registro_form += "value='Registrarme'></form>"
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        nuevo_usuario = User.objects.create_user(username=username, password=password)
        nuevo_usuario.save()
        registro_form = ""
        return HttpResponseRedirect('/')

    c = RequestContext(request, {'registro_form': registro_form})
    respuesta = template.render(c)
    return HttpResponse(respuesta)

def css(request, mi_css):
    if request.user.is_authenticated():
        #print("Cargando plantilla de usuario...")
        conf_usu = ConfigUsuario.objects.get(usuario=request.user)
        tamaño_letra = conf_usu.tamaño_letra
        color_fondo = conf_usu.color_fondo
        tamaño_letra = str(tamaño_letra) + '%'
    else:
        # plantilla por defecto
        tamaño_letra = '75%'
        color_fondo = 'white'

    template = get_template("miplantilla/css/style.css")
    c = Context({'tamaño_letra': tamaño_letra, 'color_fondo': color_fondo})
    respuesta = template.render(c)
    return HttpResponse(respuesta, content_type="text/css")

