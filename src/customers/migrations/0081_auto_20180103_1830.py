# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0080_log_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='browser',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Browser', blank=True),
        ),
        migrations.AddField(
            model_name='log',
            name='command',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Command', blank=True),
        ),
        migrations.AddField(
            model_name='log',
            name='os_user',
            field=models.CharField(max_length=250, null=True, verbose_name=b'OS', blank=True),
        ),
    ]
