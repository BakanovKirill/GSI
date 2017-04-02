# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0015_auto_20170331_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shelfdata',
            name='show_totals',
            field=models.BooleanField(default=True),
        ),
    ]
