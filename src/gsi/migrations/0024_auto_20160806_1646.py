# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0023_subcarditem_start_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='area',
            options={'ordering': ['name']},
        ),
    ]
