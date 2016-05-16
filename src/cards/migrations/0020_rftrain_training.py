# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0019_remove_rftrain_training'),
    ]

    operations = [
        migrations.AddField(
            model_name='rftrain',
            name='training',
            field=models.PositiveIntegerField(default=0, null=True, blank=True),
        ),
    ]
