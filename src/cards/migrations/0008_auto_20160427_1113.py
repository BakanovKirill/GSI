# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0007_auto_20160427_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rftrain',
            name='number_of_trees',
            field=models.IntegerField(default=50, blank=True),
        ),
    ]
