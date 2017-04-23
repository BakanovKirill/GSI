# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0022_auto_20170422_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datapolygons',
            name='customer_polygons',
            field=models.ForeignKey(related_name='data_polygons', verbose_name=b'Customer Polygons', blank=True, to='customers.CustomerPolygons', null=True),
        ),
    ]
