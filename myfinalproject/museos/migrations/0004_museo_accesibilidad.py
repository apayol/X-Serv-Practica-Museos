# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0003_auto_20180425_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='museo',
            name='accesibilidad',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
