# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0058_auto_20170818_1723'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='countfiles',
            name='user',
        ),
        migrations.DeleteModel(
            name='CountFiles',
        ),
    ]
