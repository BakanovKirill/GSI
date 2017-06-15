# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0040_auto_20170614_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='legend',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Legend', blank=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='lut_file',
            field=models.CharField(max_length=250, null=True, verbose_name=b'LUT file', blank=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='max_val',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Maximum Value for colour scaling', blank=True),
        ),
    ]
