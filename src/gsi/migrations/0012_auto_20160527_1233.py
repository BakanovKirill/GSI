# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0011_auto_20160527_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='listtestfiles',
            name='date_modified',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='listtestfiles',
            name='size',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
