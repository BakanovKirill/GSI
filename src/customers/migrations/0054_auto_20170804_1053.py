# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0053_auto_20170804_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lutfiles',
            name='legend',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name=b'Legend', choices=[(b'1', b'simple scale png'), (b'2', b'annotated scale')]),
        ),
    ]
