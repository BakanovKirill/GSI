# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.utils


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0008_auto_20160414_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='Satellite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            bases=(core.utils.UnicodeNameMixin, models.Model),
        ),
    ]
