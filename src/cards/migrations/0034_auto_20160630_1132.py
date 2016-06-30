# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0018_auto_20160601_2257'),
        ('cards', '0033_auto_20160628_1826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='remap',
            name='refstats_scale',
        ),
        migrations.AddField(
            model_name='remap',
            name='area',
            field=models.ForeignKey(blank=True, to='gsi.Area', null=True),
        ),
        migrations.AddField(
            model_name='remap',
            name='conditional_max',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='remap',
            name='conditional_mean',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='remap',
            name='conditional_median',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='remap',
            name='conditional_min',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='remap',
            name='lower_quartile',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='remap',
            name='upper_quartile',
            field=models.BooleanField(default=False),
        ),
    ]
