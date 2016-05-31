# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0013_auto_20160530_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inputdatadirectory',
            name='name',
            field=models.CharField(unique=True, max_length=100),
        ),
    ]
