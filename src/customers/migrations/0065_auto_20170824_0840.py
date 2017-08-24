# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0064_customerinfopanel_is_ts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerinfopanel',
            name='is_ts',
            field=models.BooleanField(default=False, verbose_name=b'Is Time Series'),
        ),
    ]
