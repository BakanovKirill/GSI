# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0026_datapolygons_data_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerpolygons',
            name='data_set',
            field=models.ForeignKey(related_name='data_set_customer_polygons', verbose_name=b'DataSet', blank=True, to='customers.DataSet', null=True),
        ),
        migrations.AlterField(
            model_name='datapolygons',
            name='data_set',
            field=models.ForeignKey(related_name='data_set_data_polygons', verbose_name=b'DataSet', blank=True, to='customers.DataSet', null=True),
        ),
    ]
