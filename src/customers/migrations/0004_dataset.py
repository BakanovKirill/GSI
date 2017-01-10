# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_auto_20170108_2125'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=150, null=True, blank=True)),
                ('results_directory', models.CharField(max_length=150, null=True, blank=True)),
                ('shelf_data', models.ForeignKey(blank=True, to='customers.ShelfData', null=True)),
            ],
            options={
                'verbose_name_plural': 'DataSets',
            },
        ),
    ]
