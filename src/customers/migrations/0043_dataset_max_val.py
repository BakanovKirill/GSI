# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0042_remove_dataset_max_val'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='max_val',
            field=models.PositiveIntegerField(default=100, null=True, verbose_name=b'Maximum Value for colour scaling', blank=True),
        ),
    ]
