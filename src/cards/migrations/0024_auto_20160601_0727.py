# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0023_auto_20160530_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collate',
            name='input_files',
            field=models.ManyToManyField(related_name='input_files', to='gsi.ListTestFiles', blank=True),
        ),
    ]
