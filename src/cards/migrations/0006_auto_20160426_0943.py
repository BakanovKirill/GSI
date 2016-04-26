# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0005_auto_20160304_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='rftrain',
            name='number_of_thread',
            field=models.PositiveIntegerField(default=1, blank=True),
        ),
        migrations.AddField(
            model_name='rftrain',
            name='number_of_variable',
            field=models.PositiveIntegerField(default=0, blank=True),
        ),
        migrations.AddField(
            model_name='rftrain',
            name='training',
            field=models.PositiveIntegerField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='rftrain',
            name='number_of_trees',
            field=models.IntegerField(default=50, blank=True),
        ),
    ]
