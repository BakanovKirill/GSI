# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_auto_20151215_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collate',
            name='area',
            field=models.ForeignKey(to='gsi.Area', blank=True),
        ),
        migrations.AlterField(
            model_name='collate',
            name='input_file',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='collate',
            name='input_scale_factor',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='collate',
            name='mode',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='collate',
            name='output_tile_subdir',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
