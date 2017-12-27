# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0078_auto_20171227_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='shapefile',
            field=models.ForeignKey(related_name='results', verbose_name=b'Shapefile', blank=True, to='customers.CustomerPolygons', null=True),
        ),
    ]
