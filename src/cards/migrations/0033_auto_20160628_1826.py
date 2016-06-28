# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0032_auto_20160623_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='calcstats',
            name='doy_variable',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='calcstats',
            name='filter_out',
            field=models.CharField(blank=True, max_length=100, null=True, choices=[(b'select', b'Select'), (b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3'), (b'4', b'4')]),
        ),
        migrations.AlterField(
            model_name='calcstats',
            name='period',
            field=models.CharField(default=b'year', max_length=100, null=True, blank=True, choices=[(b'year', b'Year'), (b'quarter', b'Quarter'), (b'month', b'Month'), (b'doy', b'Input a variable')]),
        ),
    ]
