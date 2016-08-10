# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0040_auto_20160803_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='calcstats',
            name='path_spec_location',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='preproc',
            name='path_spec_location',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
