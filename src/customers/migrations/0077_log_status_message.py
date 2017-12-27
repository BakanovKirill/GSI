# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0076_log_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='status_message',
            field=models.TextField(default=b''),
        ),
    ]
