# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0036_auto_20160630_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='remap',
            name='model_name',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
