# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0024_auto_20170422_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='datapolygons',
            name='total',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='datapolygons',
            name='units',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
    ]
