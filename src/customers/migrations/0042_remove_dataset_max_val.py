# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0041_auto_20170614_1458'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='max_val',
        ),
    ]
