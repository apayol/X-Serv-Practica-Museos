from museos.models import Seleccionado
from museos.models import ConfigUsuario
from museos.models import Comentario
from django.contrib import admin

# Register your models here.

from museos.models import Museo
admin.site.register(Museo)

admin.site.register(Comentario)

admin.site.register(ConfigUsuario)

admin.site.register(Seleccionado)
