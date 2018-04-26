# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0004_museo_accesibilidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='museo',
            name='direccion',
            field=models.TextField(default=0, max_length=280),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='museo',
            name='enlace',
            field=models.URLField(default=1, max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='museo',
            name='accesibilidad',
            field=models.BooleanField(max_length=280),
        ),
    ]
