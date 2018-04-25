from django.db import models

# Create your models here.

class Museo(models.Model):
    nombre = models.CharField(max_length=64)
    #ver atributos necesarios
    def __str__(self):
        return self.nombre

class Comentario(models.Model):
    usuario = models.CharField(max_length=32)
    texto = models.TextField(max_length=280)
    museo = models.ForeignKey(Museo)
    def __str__(self):
        return self.usuario + ", about: " + self.museo.nombre
