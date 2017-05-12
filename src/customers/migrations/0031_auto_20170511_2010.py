# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0030_datapolygons_total_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerpolygons',
            name='data_set',
            field=models.ForeignKey(related_name='shapefile', verbose_name=b'Shapefiles', blank=True, to='customers.DataSet', null=True),
        ),
    ]
