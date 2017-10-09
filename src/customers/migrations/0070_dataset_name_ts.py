# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0069_timeseriesresults_attribute'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='name_ts',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
