# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0034_auto_20160630_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='remap',
            name='refstats_scale',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
