# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0045_shelfdata_scale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='max_val',
            field=models.PositiveIntegerField(default=100, verbose_name=b'Maximum Value for colour scaling'),
        ),
    ]
