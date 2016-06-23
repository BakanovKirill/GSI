# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0030_auto_20160623_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calcstats',
            name='filter_out',
            field=models.CharField(blank=True, max_length=100, null=True, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3'), (b'4', b'4')]),
        ),
    ]
