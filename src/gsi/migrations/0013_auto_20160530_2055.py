# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0012_auto_20160527_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listtestfiles',
            name='input_data_directory',
            field=models.ForeignKey(related_name='data_directory', blank=True, to='gsi.InputDataDirectory'),
        ),
    ]
