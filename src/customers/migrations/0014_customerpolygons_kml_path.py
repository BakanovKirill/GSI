# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0013_auto_20170320_0724'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerpolygons',
            name='kml_path',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
    ]
