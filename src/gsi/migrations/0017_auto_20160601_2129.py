# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0016_auto_20160601_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='log_file_path',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='name',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
