# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0022_auto_20160723_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcarditem',
            name='start_time',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
    ]
