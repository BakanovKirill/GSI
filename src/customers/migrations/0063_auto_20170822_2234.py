# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0062_auto_20170822_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeseriesresults',
            name='stat_code',
            field=models.CharField(max_length=25, verbose_name=b'Status Sub Directory'),
        ),
        migrations.AlterField(
            model_name='timeseriesresults',
            name='value_of_time_series',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Value', blank=True),
        ),
    ]
