# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0005_auto_20151226_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='runbase',
            name='card_sequence',
            field=models.ForeignKey(to='gsi.CardSequence', blank=True),
        ),
    ]
