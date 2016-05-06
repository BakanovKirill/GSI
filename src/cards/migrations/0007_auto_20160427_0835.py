# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0006_randomforest'),
    ]

    operations = [
        migrations.AddField(
            model_name='rftrain',
            name='number_of_thread',
            field=models.PositiveIntegerField(default=1, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='rftrain',
            name='number_of_variable',
            field=models.PositiveIntegerField(default=0, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='rftrain',
            name='training',
            field=models.PositiveIntegerField(default=0, null=True, blank=True),
        ),
    ]
