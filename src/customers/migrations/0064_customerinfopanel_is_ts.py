# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0063_auto_20170822_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerinfopanel',
            name='is_ts',
            field=models.BooleanField(default=False),
        ),
    ]
