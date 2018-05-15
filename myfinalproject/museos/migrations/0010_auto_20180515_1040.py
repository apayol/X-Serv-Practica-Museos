# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('museos', '0009_auto_20180515_1034'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorito',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('fecha', models.DateTimeField()),
                ('museo', models.ForeignKey(to='museos.Museo')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='favoritos',
            name='museo',
        ),
        migrations.RemoveField(
            model_name='favoritos',
            name='usuario',
        ),
        migrations.DeleteModel(
            name='Favoritos',
        ),
    ]
