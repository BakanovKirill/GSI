# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0052_auto_20170706_1300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lutfiles',
            name='filename',
        ),
        migrations.AddField(
            model_name='lutfiles',
            name='lut_file',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name=b'LUT File', choices=[(b'select', b'select'), (b'MMbreakpoints2.txt', b'MMbreakpoints2.txt'), (b'test.txt~', b'test.txt~'), (b'MMbreakpoints21.txt', b'MMbreakpoints21.txt'), (b'test.txt', b'test.txt')]),
        ),
        migrations.AddField(
            model_name='lutfiles',
            name='units',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Units', blank=True),
        ),
        migrations.AddField(
            model_name='lutfiles',
            name='val_scale',
            field=models.FloatField(default=1.0, verbose_name=b'Pixel Scale Factor for units'),
        ),
        migrations.AlterField(
            model_name='lutfiles',
            name='legend',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name=b'Legend', choices=[(1, b'simple scale png'), (2, b'annotated scale')]),
        ),
    ]
