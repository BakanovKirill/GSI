# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0008_auto_20160427_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rftrain',
            name='value',
            field=models.CharField(max_length=300),
        ),
    ]
