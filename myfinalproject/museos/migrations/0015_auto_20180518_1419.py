# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0014_auto_20180518_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seleccionado',
            name='usuario',
            field=models.ForeignKey(to='museos.ConfigUsuario'),
        ),
    ]
