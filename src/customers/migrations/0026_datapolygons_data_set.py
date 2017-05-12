# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0025_auto_20170505_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='datapolygons',
            name='data_set',
            field=models.ForeignKey(related_name='data_set', verbose_name=b'DataSet', blank=True, to='customers.DataSet', null=True),
        ),
    ]
