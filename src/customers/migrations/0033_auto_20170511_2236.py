# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0032_auto_20170511_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datapolygons',
            name='customer_polygons',
            field=models.ForeignKey(related_name='attributes_shapefile', verbose_name=b'Customer Polygons', blank=True, to='customers.CustomerPolygons', null=True),
        ),
        migrations.AlterField(
            model_name='datapolygons',
            name='data_set',
            field=models.ForeignKey(related_name='attributes', verbose_name=b'DataSet', blank=True, to='customers.DataSet', null=True),
        ),
    ]
