# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0007_auto_20180509_1920'),
    ]

    operations = [
        migrations.RenameField(
            model_name='museo',
            old_name='direccion',
            new_name='via_nombre',
        ),
        migrations.AddField(
            model_name='museo',
            name='localidad',
            field=models.CharField(default=1, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='museo',
            name='postal',
            field=models.CharField(default=1, max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='museo',
            name='via_clase',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='museo',
            name='via_numero',
            field=models.CharField(default=1, max_length=16),
            preserve_default=False,
        ),
    ]
