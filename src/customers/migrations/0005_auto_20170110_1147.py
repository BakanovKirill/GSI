# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_dataset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shelfdata',
            name='root_filename',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Root Filename', blank=True),
        ),
    ]
