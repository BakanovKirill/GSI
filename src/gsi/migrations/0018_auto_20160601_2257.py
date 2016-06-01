# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0017_auto_20160601_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listtestfiles',
            name='size',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
