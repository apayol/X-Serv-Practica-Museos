# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0005_auto_20180426_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='museo',
            name='barrio',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='museo',
            name='descripcion',
            field=models.TextField(default=1, max_length=512),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='museo',
            name='distrito',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='museo',
            name='email',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='museo',
            name='horario',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='museo',
            name='telefono',
            field=models.CharField(default=1, max_length=16),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='museo',
            name='accesibilidad',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='museo',
            name='direccion',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='museo',
            name='enlace',
            field=models.URLField(max_length=256),
        ),
    ]
