# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('usuario', models.CharField(max_length=64)),
                ('texto', models.TextField(max_length=64)),
                ('museo', models.ForeignKey(to='museos.Museo')),
            ],
        ),
    ]
