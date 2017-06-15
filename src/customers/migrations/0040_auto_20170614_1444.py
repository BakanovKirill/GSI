# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0039_countfiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='legend',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='lut_file',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='max_val',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
    ]
