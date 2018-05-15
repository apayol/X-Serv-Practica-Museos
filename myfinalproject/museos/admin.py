from django.contrib import admin

# Register your models here.

from museos.models import Museo
admin.site.register(Museo)

from museos.models import Comentario
admin.site.register(Comentario)

from museos.models import ConfigUsuario
admin.site.register(ConfigUsuario)

from museos.models import Favorito
admin.site.register(Favorito)
