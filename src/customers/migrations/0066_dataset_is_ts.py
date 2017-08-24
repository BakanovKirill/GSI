# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0065_auto_20170824_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='is_ts',
            field=models.BooleanField(default=False, verbose_name=b'Is Time Series'),
        ),
    ]
