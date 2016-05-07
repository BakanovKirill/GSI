# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0020_rftrain_training'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rftrain',
            name='training',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
