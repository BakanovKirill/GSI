# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_auto_20160303_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preproc',
            name='area',
            field=models.ForeignKey(blank=True, to='gsi.Area', null=True),
        ),
        migrations.AlterField(
            model_name='preproc',
            name='year_group',
            field=models.ForeignKey(blank=True, to='gsi.YearGroup', null=True),
        ),
    ]
