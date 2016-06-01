# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0024_auto_20160601_0727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collate',
            name='input_scale_factor',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='collate',
            name='output_tile_subdir',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
