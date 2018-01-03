# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0082_auto_20180103_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='request_user',
            field=models.CharField(max_length=250, null=True, verbose_name=b'User Request', blank=True),
        ),
    ]
