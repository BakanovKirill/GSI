# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0028_auto_20170728_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developmentpage',
            name='title',
            field=models.CharField(max_length=300),
        ),
    ]
