# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0018_auto_20160507_2118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rftrain',
            name='training',
        ),
    ]
