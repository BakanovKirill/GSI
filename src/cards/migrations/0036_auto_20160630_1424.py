# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0018_auto_20160601_2257'),
        ('cards', '0035_remap_refstats_scale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='remap',
            name='area',
        ),
        migrations.AddField(
            model_name='remap',
            name='year_group',
            field=models.ForeignKey(blank=True, to='gsi.YearGroup', null=True),
        ),
    ]
