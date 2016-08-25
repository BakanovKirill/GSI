# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0041_auto_20160809_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='carditem',
            name='name',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
