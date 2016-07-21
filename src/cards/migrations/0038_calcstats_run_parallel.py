# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0037_remap_model_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='calcstats',
            name='run_parallel',
            field=models.BooleanField(default=False),
        ),
    ]
