# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0011_auto_20160506_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collate',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='mergecsv',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='preproc',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='qrf',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='randomforest',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='remap',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='rfscore',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='rftrain',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='yearfilter',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
