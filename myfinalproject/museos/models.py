from django.db import models
from django.contrib.auth.models import User


class Museo(models.Model):
    nombre = models.CharField(max_length=64)
    accesibilidad = models.BooleanField(default=False)
    via_clase = models.CharField(max_length=64)
    via_nombre = models.CharField(max_length=256)
    via_numero = models.CharField(max_length=16)
    postal = models.CharField(max_length=16)
    localidad = models.CharField(max_length=32)
    barrio = models.CharField(max_length=64)
    distrito = models.CharField(max_length=64)
    enlace = models.URLField(max_length=512)
    descripcion = models.TextField(max_length=512)
    horario = models.CharField(max_length=512)
    telefono = models.CharField(max_length=512)
    email = models.CharField(max_length=512)
    num_comentarios = models.IntegerField(default=0)
    def __str__(self):
        return self.nombre

class Comentario(models.Model):
    texto = models.TextField(max_length=280)
    museo = models.ForeignKey(Museo)
    def __str__(self):
        return "Sobre: " + self.museo.nombre + ": " + self.texto

class ConfigUsuario(models.Model):
    usuario = models.CharField(max_length=16)
    titulo = models.CharField(max_length=512, default="")
    tamaño_letra = models.IntegerField(default=0)
    color_fondo = models.CharField(max_length=10, default='#ffffff')
    def __str__(self):
        return self.usuario

class Seleccionado(models.Model):
    usuario = models.ForeignKey(ConfigUsuario)
    museo = models.ForeignKey(Museo)
    fecha = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "Selección de: " + self.usuario.usuario
  
