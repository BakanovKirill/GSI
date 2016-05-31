# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0012_auto_20160527_1233'),
        ('cards', '0021_auto_20160507_2120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collate',
            name='input_file',
        ),
        migrations.AddField(
            model_name='collate',
            name='input_data_directory',
            field=models.ForeignKey(blank=True, to='gsi.InputDataDirectory', null=True),
        ),
        migrations.AddField(
            model_name='collate',
            name='input_files',
            field=models.ManyToManyField(to='gsi.ListTestFiles', null=True, blank=True),
        ),
    ]
