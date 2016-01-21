# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.utils


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CardItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('order', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Collate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('run_parallel', models.BooleanField(default=False)),
                ('mode', models.CharField(max_length=50)),
                ('input_file', models.CharField(max_length=200)),
                ('output_tile_subdir', models.CharField(max_length=200)),
                ('input_scale_factor', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Collate cards',
            },
            bases=(core.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MergeCSV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('csv1', models.CharField(max_length=200)),
                ('csv2', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'MergeCSV cards',
            },
            bases=(core.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='OrderedCardItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PreProc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('run_parallel', models.BooleanField(default=False)),
                ('mode', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'PreProc cards',
            },
            bases=(core.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='QRF',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('interval', models.CharField(max_length=100)),
                ('number_of_trees', models.IntegerField(default=0)),
                ('number_of_threads', models.IntegerField(default=1)),
                ('directory', models.CharField(max_length=300)),
            ],
            options={
                'verbose_name_plural': 'QRF cards',
            },
            bases=(core.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Remap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('run_parallel', models.BooleanField(default=False)),
                ('file_spec', models.CharField(max_length=200)),
                ('roi', models.CharField(max_length=200)),
                ('output_root', models.CharField(max_length=200)),
                ('output_suffix', models.CharField(max_length=200)),
                ('scale', models.CharField(max_length=200)),
                ('output', models.CharField(max_length=200)),
                ('color_table', models.CharField(max_length=200)),
                ('refstats_file', models.CharField(max_length=200)),
                ('refstats_scale', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Remap cards',
            },
            bases=(core.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RFScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('run_parallel', models.BooleanField(default=False)),
                ('bias_corrn', models.CharField(max_length=200)),
                ('number_of_threads', models.IntegerField(default=1)),
                ('QRFopts', models.CharField(max_length=300)),
                ('ref_target', models.CharField(max_length=100)),
                ('clean_name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'RFScore cards',
            },
            bases=(core.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RFTrain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('run_parallel', models.BooleanField(default=False)),
                ('number_of_trees', models.IntegerField(default=0)),
                ('value', models.CharField(max_length=300)),
                ('config_file', models.CharField(max_length=200)),
                ('output_tile_subdir', models.CharField(max_length=200)),
                ('input_scale_factor', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'RFTRain cards',
            },
            bases=(core.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='YearFilter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('run_parallel', models.BooleanField(default=False)),
                ('filetype', models.CharField(max_length=50)),
                ('filter', models.CharField(max_length=200)),
                ('filter_output', models.CharField(max_length=300)),
                ('extend_start', models.CharField(max_length=200)),
                ('input_fourier', models.CharField(max_length=200)),
                ('output_directory', models.CharField(max_length=300)),
                ('input_directory', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'YearFilter cards',
            },
            bases=(core.utils.UnicodeNameMixin, models.Model),
        ),
    ]
