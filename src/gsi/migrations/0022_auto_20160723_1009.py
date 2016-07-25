# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0021_subcarditem_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcarditem',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
