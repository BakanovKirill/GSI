# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0006_auto_20160329_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='runbase',
            name='card_sequence',
            field=models.ForeignKey(blank=True, to='gsi.CardSequence', null=True),
        ),
    ]
