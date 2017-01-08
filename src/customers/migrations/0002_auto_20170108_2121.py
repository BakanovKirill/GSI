# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShelfData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attribute_name', models.CharField(max_length=100, null=True, blank=True)),
                ('root_filename', models.CharField(max_length=100, null=True, blank=True)),
                ('units', models.CharField(max_length=100, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('category', models.ForeignKey(to='customers.Category')),
            ],
            options={
                'verbose_name_plural': 'Info Panel Mappings',
            },
        ),
        migrations.RemoveField(
            model_name='infopanelmapping',
            name='category',
        ),
        migrations.DeleteModel(
            name='InfoPanelMapping',
        ),
    ]
