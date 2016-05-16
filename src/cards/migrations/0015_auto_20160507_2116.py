# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0014_rftrain_number_of_variable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rftrain',
            name='number_of_variable',
            field=models.PositiveIntegerField(default=1, null=True, blank=True),
        ),
    ]
