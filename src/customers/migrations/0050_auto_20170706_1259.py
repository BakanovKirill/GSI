# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0049_auto_20170703_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerinfopanel',
            name='tif_path2',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lutfiles',
            name='filename',
            field=models.CharField(blank=True, max_length=300, null=True, choices=[(b'select', b'select'), (b'MMbreakpoints2.txt', b'MMbreakpoints2.txt'), (b'MMbreakpoints21.txt', b'MMbreakpoints21.txt')]),
        ),
    ]
