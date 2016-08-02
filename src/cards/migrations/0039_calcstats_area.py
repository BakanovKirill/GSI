# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0023_subcarditem_start_time'),
        ('cards', '0038_calcstats_run_parallel'),
    ]

    operations = [
        migrations.AddField(
            model_name='calcstats',
            name='area',
            field=models.ForeignKey(blank=True, to='gsi.Area', null=True),
        ),
    ]
