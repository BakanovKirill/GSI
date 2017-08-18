# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0057_auto_20170811_1657'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attributesreport',
            old_name='statisctic',
            new_name='statistic',
        ),
        migrations.RenameField(
            model_name='customerinfopanel',
            old_name='statisctic',
            new_name='statistic',
        ),
        migrations.RenameField(
            model_name='datapolygons',
            old_name='statisctic',
            new_name='statistic',
        ),
    ]
