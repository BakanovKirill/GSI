# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0031_auto_20170511_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerpolygons',
            name='data_set',
            field=models.ForeignKey(related_name='shapefiles', verbose_name=b'Shapefiles', blank=True, to='customers.DataSet', null=True),
        ),
    ]
