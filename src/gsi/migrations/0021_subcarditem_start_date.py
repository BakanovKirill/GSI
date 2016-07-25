# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0020_subcarditem'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcarditem',
            name='start_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
