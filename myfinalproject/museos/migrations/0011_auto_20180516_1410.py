# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0010_auto_20180515_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configusuario',
            name='color_fondo',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='configusuario',
            name='tamaño_letra',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='configusuario',
            name='usuario',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='favorito',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='favorito',
            name='usuario',
            field=models.ForeignKey(to='museos.ConfigUsuario'),
        ),
        migrations.AlterField(
            model_name='museo',
            name='email',
            field=models.CharField(max_length=512),
        ),
        migrations.AlterField(
            model_name='museo',
            name='enlace',
            field=models.URLField(max_length=512),
        ),
        migrations.AlterField(
            model_name='museo',
            name='horario',
            field=models.CharField(max_length=512),
        ),
        migrations.AlterField(
            model_name='museo',
            name='telefono',
            field=models.CharField(max_length=512),
        ),
    ]
