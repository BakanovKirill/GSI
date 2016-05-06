# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0010_auto_20160506_0836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rftrain',
            name='number_of_variable',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='rftrain',
            name='training',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
