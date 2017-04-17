# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0017_dataterraserver'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataterraserver',
            name='shapefile_link',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
    ]
