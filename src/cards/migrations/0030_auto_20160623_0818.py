# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0029_calcstats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calcstats',
            name='filter_out',
            field=models.CharField(default=b'0', max_length=100, null=True, blank=True, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3'), (b'4', b'4')]),
        ),
        migrations.AlterField(
            model_name='calcstats',
            name='period',
            field=models.CharField(default=b'year', max_length=100, null=True, blank=True, choices=[(b'year', b'Year'), (b'quarter', b'Quarter'), (b'month', b'Month'), (b'doy', b'Stats per Year')]),
        ),
    ]
