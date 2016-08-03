# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0039_calcstats_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calcstats',
            name='filter',
            field=models.PositiveIntegerField(default=0, null=True, blank=True),
        ),
    ]
