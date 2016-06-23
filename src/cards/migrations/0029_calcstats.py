# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.utils


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0018_auto_20160601_2257'),
        ('cards', '0028_auto_20160601_2354'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalcStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('output_tile_subdir', models.CharField(max_length=200)),
                ('period', models.CharField(default=b'year', max_length=100, choices=[(b'year', b'Year'), (b'quarter', b'Quarter'), (b'month', b'Month'), (b'doy', b'Stats per Year')])),
                ('filter', models.PositiveIntegerField(default=0, null=True, blank=True)),
                ('filter_out', models.CharField(default=b'0', max_length=100, choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3'), (b'4', b'4')])),
                ('input_fourier', models.CharField(max_length=200, null=True, blank=True)),
                ('out_dir', models.CharField(max_length=200, null=True, blank=True)),
                ('year_group', models.ForeignKey(blank=True, to='gsi.YearGroup', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(core.utils.UnicodeNameMixin, models.Model),
        ),
    ]
