# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0025_auto_20160601_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mergecsv',
            name='csv1',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='mergecsv',
            name='csv2',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='qrf',
            name='directory',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='qrf',
            name='interval',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='randomforest',
            name='aoi_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='randomforest',
            name='model',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='randomforest',
            name='mvrf',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='randomforest',
            name='run_set',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='remap',
            name='color_table',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='remap',
            name='file_spec',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='remap',
            name='output',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='remap',
            name='output_root',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='remap',
            name='output_suffix',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='remap',
            name='refstats_file',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='remap',
            name='refstats_scale',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='remap',
            name='roi',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='remap',
            name='scale',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='rfscore',
            name='QRFopts',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='rfscore',
            name='bias_corrn',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='rfscore',
            name='clean_name',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='rfscore',
            name='ref_target',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='rftrain',
            name='config_file',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='rftrain',
            name='input_scale_factor',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='rftrain',
            name='output_tile_subdir',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='rftrain',
            name='value',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='yearfilter',
            name='extend_start',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='yearfilter',
            name='filter',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='yearfilter',
            name='filter_output',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='yearfilter',
            name='input_directory',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='yearfilter',
            name='input_fourier',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='yearfilter',
            name='output_directory',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
