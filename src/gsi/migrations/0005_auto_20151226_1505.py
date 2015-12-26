# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gsi', '0004_auto_20151222_1343'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderedcarditem',
            options={'ordering': ('order',)},
        ),
        migrations.AlterField(
            model_name='runstep',
            name='card_item',
            field=models.ForeignKey(to='gsi.OrderedCardItem'),
        ),
    ]
