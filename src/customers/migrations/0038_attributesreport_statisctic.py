# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0037_auto_20170525_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='attributesreport',
            name='statisctic',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
    ]
