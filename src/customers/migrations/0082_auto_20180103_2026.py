# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0081_auto_20180103_1830'),
    ]

    operations = [
        migrations.RenameField(
            model_name='log',
            old_name='browser',
            new_name='request_user',
        ),
        migrations.RemoveField(
            model_name='log',
            name='command',
        ),
    ]
