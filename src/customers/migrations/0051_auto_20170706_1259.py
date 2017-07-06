# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0050_auto_20170706_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerinfopanel',
            name='tif_path',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
