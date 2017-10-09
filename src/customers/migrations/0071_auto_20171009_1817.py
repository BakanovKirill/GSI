# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0070_dataset_name_ts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='name_ts',
            field=models.CharField(max_length=300, null=True, verbose_name=b'Time Series Name', blank=True),
        ),
    ]
