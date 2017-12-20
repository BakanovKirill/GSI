# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0075_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='message',
            field=models.TextField(default=b''),
        ),
    ]
