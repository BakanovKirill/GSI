# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0083_auto_20180103_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
    ]
