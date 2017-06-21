# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0046_auto_20170615_2057'),
    ]

    operations = [
        migrations.CreateModel(
            name='LutFiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300, null=True, blank=True)),
                ('filename', models.CharField(max_length=300, null=True, blank=True)),
                ('max_val', models.PositiveIntegerField(default=100, verbose_name=b'Maximum Value for colour scaling')),
                ('legend', models.CharField(max_length=250, null=True, verbose_name=b'Legend', blank=True)),
            ],
            options={
                'verbose_name_plural': 'LUTFiles',
            },
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='legend',
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='lutfile',
        ),
        migrations.RemoveField(
            model_name='dataset',
            name='max_val',
        ),
    ]
