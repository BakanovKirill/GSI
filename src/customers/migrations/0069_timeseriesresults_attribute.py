# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0068_auto_20170905_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeseriesresults',
            name='attribute',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Attribute', blank=True),
        ),
    ]
