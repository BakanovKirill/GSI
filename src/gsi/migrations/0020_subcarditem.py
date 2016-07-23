# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.utils


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0019_auto_20160721_0616'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCardItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('state', models.CharField(default=b'pending', max_length=100, choices=[(b'created', b'Created'), (b'pending', b'Pending'), (b'running', b'Running'), (b'success', b'Success'), (b'fail', b'Fail')])),
                ('run_id', models.PositiveIntegerField()),
                ('card_id', models.PositiveIntegerField()),
            ],
            bases=(core.utils.UnicodeNameMixin, models.Model),
        ),
    ]
