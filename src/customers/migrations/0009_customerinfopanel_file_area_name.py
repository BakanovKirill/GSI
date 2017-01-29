# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0008_customerinfopanel'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerinfopanel',
            name='file_area_name',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
    ]
