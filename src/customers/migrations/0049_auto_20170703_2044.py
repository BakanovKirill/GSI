# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0048_shelfdata_lutfiles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lutfiles',
            name='filename',
            field=models.CharField(blank=True, max_length=300, null=True, choices=[(b'TifPng', b'TifPng'), (b'MMbreakpoints2.txt', b'MMbreakpoints2.txt'), (b'MMbreakpoints21.txt', b'MMbreakpoints21.txt')]),
        ),
        migrations.AlterField(
            model_name='shelfdata',
            name='lutfiles',
            field=models.ForeignKey(related_name='lut_files', verbose_name=b'LUT Files', blank=True, to='customers.LutFiles', null=True),
        ),
    ]
