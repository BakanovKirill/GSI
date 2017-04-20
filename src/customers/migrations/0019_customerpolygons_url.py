# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0018_dataterraserver_shapefile_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerpolygons',
            name='url',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
    ]
