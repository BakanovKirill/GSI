# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0011_remove_customerinfopanel_polygon'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerinfopanel',
            name='polygon',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
    ]
