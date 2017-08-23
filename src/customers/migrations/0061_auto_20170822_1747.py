# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0060_timeseriesresults'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeseriesresults',
            name='customer_polygons',
            field=models.ForeignKey(related_name='ts_attributes', verbose_name=b'Customer Polygons', to='customers.CustomerPolygons'),
        ),
        migrations.AlterField(
            model_name='timeseriesresults',
            name='data_set',
            field=models.ForeignKey(related_name='ts_datasets', verbose_name=b'DataSet', to='customers.DataSet'),
        ),
        migrations.AlterField(
            model_name='timeseriesresults',
            name='result_year',
            field=models.CharField(max_length=4, verbose_name=b'Result Year'),
        ),
        migrations.AlterField(
            model_name='timeseriesresults',
            name='user',
            field=models.ForeignKey(related_name='time_series_user', verbose_name=b'User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='timeseriesresults',
            name='value_of_time_series',
            field=models.CharField(max_length=250, verbose_name=b'Value'),
        ),
    ]
