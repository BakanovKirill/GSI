# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_auto_20160302_0839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collate',
            name='area',
            field=models.ForeignKey(to='gsi.Area'),
        ),
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
            model_name='preproc',
            name='area',
            field=models.ForeignKey(to='gsi.Area', blank=True),
        ),
        migrations.AlterField(
            model_name='preproc',
            name='mode',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='preproc',
            name='year_group',
            field=models.ForeignKey(to='gsi.YearGroup', blank=True),
        ),
        migrations.AlterField(
            model_name='qrf',
            name='directory',
            field=models.CharField(max_length=300, blank=True),
        ),
        migrations.AlterField(
            model_name='qrf',
            name='interval',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='qrf',
            name='number_of_threads',
            field=models.IntegerField(default=1, blank=True),
        ),
        migrations.AlterField(
            model_name='qrf',
            name='number_of_trees',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='remap',
            name='color_table',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='remap',
            name='output',
            field=models.CharField(max_length=200, blank=True),
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
            name='scale',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='rfscore',
            name='QRFopts',
            field=models.CharField(max_length=300, blank=True),
        ),
        migrations.AlterField(
            model_name='rfscore',
            name='bias_corrn',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='rfscore',
            name='clean_name',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='rfscore',
            name='number_of_threads',
            field=models.IntegerField(default=1, blank=True),
        ),
        migrations.AlterField(
            model_name='rfscore',
            name='ref_target',
            field=models.CharField(max_length=100, blank=True),
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
            name='number_of_trees',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='rftrain',
            name='output_tile_subdir',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='rftrain',
            name='value',
            field=models.CharField(max_length=300, blank=True),
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
            field=models.CharField(max_length=300, blank=True),
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
            field=models.CharField(max_length=300, blank=True),
        ),
    ]
