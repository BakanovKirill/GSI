# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0021_auto_20170421_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datapolygons',
            name='customer_polygons',
            field=models.ForeignKey(related_name='customer_polygons', verbose_name=b'Customer Polygons', blank=True, to='customers.CustomerPolygons', null=True),
        ),
    ]
