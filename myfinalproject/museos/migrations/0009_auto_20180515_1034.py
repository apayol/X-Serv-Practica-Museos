# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('museos', '0008_auto_20180509_1952'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigUsuario',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('titulo', models.CharField(max_length=512)),
                ('tamaño_letra', models.CharField(max_length=512)),
                ('color_fondo', models.CharField(max_length=512)),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Favoritos',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('fecha', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='comentario',
            name='usuario',
        ),
        migrations.AddField(
            model_name='museo',
            name='num_comentarios',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='favoritos',
            name='museo',
            field=models.ForeignKey(to='museos.Museo'),
        ),
        migrations.AddField(
            model_name='favoritos',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
