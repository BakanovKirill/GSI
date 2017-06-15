# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0043_dataset_max_val'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='lut_file',
        ),
        migrations.AddField(
            model_name='dataset',
            name='lutfile',
            field=models.CharField(default=b'running', max_length=50, choices=[(b'grey', b'Grey'), (b'red', b'Red'), (b'green', b'Green'), (b'yellow', b'Yellow'), (b'orange', b'Orange')]),
        ),
    ]
