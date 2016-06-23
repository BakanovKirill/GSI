# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0031_auto_20160623_0819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calcstats',
            name='filter',
            field=models.FloatField(default=0, null=True, blank=True),
        ),
    ]
