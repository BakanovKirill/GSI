# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0027_auto_20160601_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collate',
            name='input_scale_factor',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='collate',
            name='mode',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='collate',
            name='output_tile_subdir',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
