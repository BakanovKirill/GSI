# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0056_customerinfopanel_legend_path_old'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerpolygons',
            name='text_kml',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lutfiles',
            name='lut_file',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name=b'LUT File', choices=[(b'select', b'select'), (b'16colours.txt', b'16colours.txt'), (b'green.txt', b'green.txt'), (b'MMbreakpoints2.txt', b'MMbreakpoints2.txt'), (b'MMbreakpoints21.txt', b'MMbreakpoints21.txt'), (b'blue.txt', b'blue.txt'), (b'Low-HighBreakpoints.txt', b'Low-HighBreakpoints.txt'), (b'red.txt', b'red.txt')]),
        ),
    ]
