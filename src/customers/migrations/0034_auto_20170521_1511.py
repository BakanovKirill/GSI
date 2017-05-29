# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0033_auto_20170511_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerinfopanel',
            name='is_show',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customerinfopanel',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='customerpolygons',
            name='data_set',
            field=models.ForeignKey(related_name='shapefiles', verbose_name=b'DataSets', blank=True, to='customers.DataSet', null=True),
        ),
    ]
