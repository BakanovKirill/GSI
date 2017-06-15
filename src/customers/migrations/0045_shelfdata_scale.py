# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0044_auto_20170615_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='shelfdata',
            name='scale',
            field=models.PositiveIntegerField(default=0, verbose_name=b'Scale'),
        ),
    ]
