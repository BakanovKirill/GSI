# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0010_inputdatadirectory_listtestfiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='inputdatadirectory',
            name='full_path',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='inputdatadirectory',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='listtestfiles',
            name='input_data_directory',
            field=models.ForeignKey(related_name='data_directory', to='gsi.InputDataDirectory'),
        ),
        migrations.AlterField(
            model_name='listtestfiles',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
