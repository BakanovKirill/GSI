# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.utils


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0009_satellite'),
    ]

    operations = [
        migrations.CreateModel(
            name='InputDataDirectory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            bases=(core.utils.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ListTestFiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('input_data_directory', models.ForeignKey(to='gsi.InputDataDirectory')),
            ],
            bases=(core.utils.UnicodeNameMixin, models.Model),
        ),
    ]
