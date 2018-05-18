# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0012_auto_20180518_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seleccionado',
            name='usuario',
            field=models.ForeignKey(to='museos.ConfigUsuario'),
        ),
    ]
