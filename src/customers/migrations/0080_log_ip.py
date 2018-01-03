# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0079_auto_20171227_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='ip',
            field=models.CharField(max_length=250, null=True, verbose_name=b'IP', blank=True),
        ),
    ]
