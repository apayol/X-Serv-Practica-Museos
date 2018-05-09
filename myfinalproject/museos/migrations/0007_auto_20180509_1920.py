# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0006_auto_20180509_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='museo',
            name='direccion',
            field=models.CharField(max_length=256),
        ),
    ]
