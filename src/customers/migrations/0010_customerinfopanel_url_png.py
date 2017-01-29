# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0009_customerinfopanel_file_area_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerinfopanel',
            name='url_png',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
    ]
