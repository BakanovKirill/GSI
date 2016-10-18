# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0002_logdebug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logdebug',
            name='user',
        ),
    ]
