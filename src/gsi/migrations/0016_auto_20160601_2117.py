# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0015_auto_20160530_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inputdatadirectory',
            name='full_path',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='inputdatadirectory',
            name='name',
            field=models.CharField(unique=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='listtestfiles',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
