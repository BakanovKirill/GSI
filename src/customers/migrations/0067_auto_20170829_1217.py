# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0066_dataset_is_ts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shelfdata',
            name='scale',
            field=models.FloatField(default=0.0, verbose_name=b'Scale'),
        ),
    ]
