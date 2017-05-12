# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0029_auto_20170511_0754'),
    ]

    operations = [
        migrations.AddField(
            model_name='datapolygons',
            name='total_area',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
    ]
