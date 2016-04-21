# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0007_auto_20160329_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='state',
            field=models.CharField(default=b'running', max_length=100, choices=[(b'created', b'Created'), (b'pending', b'Pending'), (b'running', b'Running'), (b'success', b'Success'), (b'fail', b'Fail')]),
        ),
    ]
