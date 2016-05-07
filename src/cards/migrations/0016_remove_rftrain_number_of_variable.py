# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0015_auto_20160507_2116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rftrain',
            name='number_of_variable',
        ),
    ]
