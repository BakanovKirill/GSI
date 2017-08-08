# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0054_auto_20170804_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerinfopanel',
            name='legend_path',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customerinfopanel',
            name='url_legend',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
