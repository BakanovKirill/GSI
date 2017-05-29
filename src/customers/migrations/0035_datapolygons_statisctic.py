# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0034_auto_20170521_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='datapolygons',
            name='statisctic',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
    ]
