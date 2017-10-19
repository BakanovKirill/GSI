# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0071_auto_20171009_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='attributesreport',
            name='attribute',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lutfiles',
            name='lut_file',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name=b'LUT File', choices=[(b'select', b'select'), (b'16colours.txt', b'16colours.txt'), (b'10colours.txt', b'10colours.txt'), (b'green.txt', b'green.txt'), (b'MMbreakpoints2.txt', b'MMbreakpoints2.txt'), (b'MMbreakpoints21.txt', b'MMbreakpoints21.txt'), (b'MM16colors.txt', b'MM16colors.txt'), (b'TEST1.txt', b'TEST1.txt'), (b'blue.txt', b'blue.txt'), (b'Low-HighBreakpoints.txt', b'Low-HighBreakpoints.txt'), (b'red.txt', b'red.txt'), (b'16colours.txt.old', b'16colours.txt.old')]),
        ),
    ]
