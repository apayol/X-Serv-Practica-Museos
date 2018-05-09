from django.db import models


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
    enlace = models.URLField(max_length=256)
    descripcion = models.TextField(max_length=512)
    horario = models.CharField(max_length=64)
    telefono = models.CharField(max_length=16)
    email = models.CharField(max_length=64)

    def __str__(self):
        return self.nombre

class Comentario(models.Model):
    usuario = models.CharField(max_length=32)
    texto = models.TextField(max_length=280)
    museo = models.ForeignKey(Museo)
    def __str__(self):
        return self.usuario + ", about: " + self.museo.nombre
