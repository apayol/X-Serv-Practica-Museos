# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0002_comentario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='texto',
            field=models.TextField(max_length=280),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='usuario',
            field=models.CharField(max_length=32),
        ),
    ]
