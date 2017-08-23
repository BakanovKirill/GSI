# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0061_auto_20170822_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeseriesresults',
            name='result_date',
            field=models.DateField(verbose_name=b'Result Date'),
        ),
    ]
