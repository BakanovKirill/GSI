# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0018_auto_20160601_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderedcarditem',
            name='number_sub_cards',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='orderedcarditem',
            name='run_parallel',
            field=models.BooleanField(default=False),
        ),
    ]
