# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0055_auto_20170808_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerinfopanel',
            name='legend_path_old',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
