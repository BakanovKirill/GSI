# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0072_auto_20171018_2023'),
    ]

    operations = [
        migrations.AddField(
            model_name='lutfiles',
            name='allow_negatives',
            field=models.BooleanField(default=False, verbose_name=b'Allow negatives'),
        ),
    ]
