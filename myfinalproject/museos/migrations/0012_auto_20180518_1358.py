# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('museos', '0011_auto_20180516_1410'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seleccionado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('museo', models.ForeignKey(to='museos.Museo')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='favorito',
            name='museo',
        ),
        migrations.RemoveField(
            model_name='favorito',
            name='usuario',
        ),
        migrations.AlterField(
            model_name='configusuario',
            name='color_fondo',
            field=models.CharField(max_length=10, default='#ffffff'),
        ),
        migrations.AlterField(
            model_name='configusuario',
            name='titulo',
            field=models.CharField(max_length=512, default=''),
        ),
        migrations.DeleteModel(
            name='Favorito',
        ),
    ]
