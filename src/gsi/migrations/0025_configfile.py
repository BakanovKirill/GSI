# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0024_auto_20160806_1646'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pathname', models.CharField(max_length=200, null=True, blank=True)),
                ('description', models.CharField(max_length=200, null=True, blank=True)),
                ('configuration_file', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Configuration Files',
            },
        ),
    ]
