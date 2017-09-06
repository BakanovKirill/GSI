# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0067_auto_20170829_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeseriesresults',
            name='customer_polygons',
            field=models.ForeignKey(related_name='timeseries_attributes', verbose_name=b'Customer Polygons', to='customers.CustomerPolygons'),
        ),
        migrations.AlterField(
            model_name='timeseriesresults',
            name='data_set',
            field=models.ForeignKey(related_name='timeseries', verbose_name=b'DataSet', to='customers.DataSet'),
        ),
    ]
